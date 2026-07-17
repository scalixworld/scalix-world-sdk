import { describe, expect, it } from 'vitest';
import { createRequestMiddleware, scalixUserAgent } from '../src/scalix/middleware.js';
import { VERSION } from '../src/version.js';

describe('scalixUserAgent', () => {
  it('formats as scalix-typescript/<version>', () => {
    expect(scalixUserAgent()).toBe(`scalix-typescript/${VERSION}`);
    expect(scalixUserAgent('myapp/2.0')).toBe(`scalix-typescript/${VERSION} myapp/2.0`);
  });
});

describe('createRequestMiddleware', () => {
  it('adds User-Agent and Idempotency-Key on a POST', () => {
    const mw = createRequestMiddleware();
    const req = mw(new Request('https://api.scalix.world/v1/x', { method: 'POST' }));
    expect(req.headers.get('user-agent')).toBe(`scalix-typescript/${VERSION}`);
    expect(req.headers.get('idempotency-key')).toBeTruthy();
  });

  it('does NOT add an Idempotency-Key on a GET', () => {
    const mw = createRequestMiddleware();
    const req = mw(new Request('https://api.scalix.world/v1/x', { method: 'GET' }));
    expect(req.headers.get('user-agent')).toBe(`scalix-typescript/${VERSION}`);
    expect(req.headers.get('idempotency-key')).toBeNull();
  });

  it('adds an Idempotency-Key on PUT and PATCH', () => {
    const mw = createRequestMiddleware();
    for (const method of ['PUT', 'PATCH']) {
      const req = mw(new Request('https://api.scalix.world/v1/x', { method }));
      expect(req.headers.get('idempotency-key'), method).toBeTruthy();
    }
  });

  it('never overwrites a caller-supplied Idempotency-Key or User-Agent', () => {
    const mw = createRequestMiddleware();
    const req = mw(
      new Request('https://api.scalix.world/v1/x', {
        method: 'POST',
        headers: { 'Idempotency-Key': 'caller-key', 'User-Agent': 'caller-ua' },
      }),
    );
    expect(req.headers.get('idempotency-key')).toBe('caller-key');
    expect(req.headers.get('user-agent')).toBe('caller-ua');
  });

  it('can disable idempotency', () => {
    const mw = createRequestMiddleware({ idempotency: false });
    const req = mw(new Request('https://api.scalix.world/v1/x', { method: 'POST' }));
    expect(req.headers.get('idempotency-key')).toBeNull();
  });

  it('uses an injected key generator', () => {
    const mw = createRequestMiddleware({ generateIdempotencyKey: () => 'fixed-123' });
    const req = mw(new Request('https://api.scalix.world/v1/x', { method: 'POST' }));
    expect(req.headers.get('idempotency-key')).toBe('fixed-123');
  });
});
