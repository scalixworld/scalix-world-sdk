import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest';
import { ScalixAuthClient } from '../src/client.js';

// Runs in the default node environment: the client guards all browser APIs
// (`window`, `localStorage`, `document.cookie`) behind `typeof` checks, so these
// tests exercise the request wiring — URLs, methods, bodies, and auth headers —
// against the live `/v1/auth/*` gateway surface without a DOM.

type Captured = { url: string; init: RequestInit };

function mockFetch(status: number, body: unknown) {
  const calls: Captured[] = [];
  const fn = vi.fn(async (url: string, init: RequestInit) => {
    calls.push({ url, init });
    return new Response(JSON.stringify(body), {
      status,
      headers: { 'content-type': 'application/json' },
    });
  });
  globalThis.fetch = fn as unknown as typeof fetch;
  return { calls };
}

const SESSION = {
  access_token: 'at_123',
  refresh_token: 'rt_456',
  expires_in: 3600,
  expires_at: new Date(Date.now() + 3_600_000).toISOString(),
  token_type: 'bearer',
};
const USER = {
  id: 'u_1',
  email: 'a@b.com',
  is_anonymous: false,
  raw_user_meta_data: {},
  created_at: '',
  updated_at: '',
};

function newClient(url = 'https://api.scalix.world') {
  // autoRefresh/persistSession off: no timers, no storage — deterministic in node.
  return new ScalixAuthClient({ url, autoRefresh: false, persistSession: false });
}

const realFetch = globalThis.fetch;
afterEach(() => {
  globalThis.fetch = realFetch;
});

describe('ScalixAuthClient request wiring', () => {
  it('signUp posts to /v1/auth/signup and stores the session', async () => {
    const { calls } = mockFetch(200, { user: USER, session: SESSION });
    const auth = newClient();
    const res = await auth.signUp('a@b.com', 'pw', { plan: 'free' });

    expect(calls[0].url).toBe('https://api.scalix.world/v1/auth/signup');
    expect(calls[0].init.method).toBe('POST');
    expect(JSON.parse(calls[0].init.body as string)).toEqual({
      email: 'a@b.com',
      password: 'pw',
      data: { plan: 'free' },
    });
    expect(res.session.access_token).toBe('at_123');
    expect(auth.getSession()?.access_token).toBe('at_123');
  });

  it('signInWithPassword posts to /v1/auth/login and then sends the bearer token', async () => {
    const { calls } = mockFetch(200, { user: USER, session: SESSION });
    const auth = newClient();
    await auth.signInWithPassword('a@b.com', 'pw');
    expect(calls[0].url).toBe('https://api.scalix.world/v1/auth/login');

    // Subsequent authenticated call carries Authorization from the stored session.
    mockFetch(200, USER);
    await auth.getUser();
    const g = (globalThis.fetch as unknown as { mock: { calls: unknown[][] } }).mock.calls[0];
    const headers = (g[1] as RequestInit).headers as Record<string, string>;
    expect(g[0]).toBe('https://api.scalix.world/v1/auth/user');
    expect(headers.Authorization).toBe('Bearer at_123');
  });

  it('signInWithOAuth posts to /v1/auth/oauth/authorize and returns the redirect url', async () => {
    const { calls } = mockFetch(200, { url: 'https://provider/oauth?x=1' });
    const auth = newClient();
    const { url } = await auth.signInWithOAuth('google', 'https://myapp/cb');

    expect(calls[0].url).toBe('https://api.scalix.world/v1/auth/oauth/authorize');
    expect(JSON.parse(calls[0].init.body as string)).toEqual({
      provider: 'google',
      redirect_url: 'https://myapp/cb',
    });
    expect(url).toBe('https://provider/oauth?x=1');
  });

  it('refreshSession posts the refresh_token to /v1/auth/refresh', async () => {
    mockFetch(200, { user: USER, session: SESSION });
    const auth = newClient();
    await auth.signInWithPassword('a@b.com', 'pw');

    const { calls } = mockFetch(200, { ...SESSION, access_token: 'at_new' });
    const session = await auth.refreshSession();
    expect(calls[0].url).toBe('https://api.scalix.world/v1/auth/refresh');
    expect(JSON.parse(calls[0].init.body as string)).toEqual({ refresh_token: 'rt_456' });
    expect(session?.access_token).toBe('at_new');
  });

  it('strips a trailing slash from the base url', async () => {
    const { calls } = mockFetch(200, { user: USER, session: SESSION });
    const auth = newClient('https://api.scalix.world/');
    await auth.signInWithPassword('a@b.com', 'pw');
    expect(calls[0].url).toBe('https://api.scalix.world/v1/auth/login');
  });

  it('emits SIGNED_IN then SIGNED_OUT to onAuthStateChange listeners', async () => {
    mockFetch(200, { user: USER, session: SESSION });
    const auth = newClient();
    const events: string[] = [];
    auth.onAuthStateChange((e) => events.push(e));

    await auth.signInWithPassword('a@b.com', 'pw');
    mockFetch(200, {});
    await auth.signOut();

    expect(events).toContain('SIGNED_IN');
    expect(events).toContain('SIGNED_OUT');
    expect(auth.getSession()).toBeNull();
  });

  it('surfaces the server error message on failure', async () => {
    mockFetch(401, { error: 'invalid credentials' });
    const auth = newClient();
    await expect(auth.signInWithPassword('a@b.com', 'bad')).rejects.toThrow('invalid credentials');
  });
});
