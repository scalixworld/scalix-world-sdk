import { describe, expect, it, vi } from 'vitest';
import { createScalixClient } from '../src/scalix/client.js';
import { VERSION } from '../src/version.js';
import { executeSql, getMe, putObject } from '../src/generated/index.js';

const noSleep = async () => {};

function json(status: number, body: unknown = {}, headers?: Record<string, string>): Response {
  return new Response(JSON.stringify(body), {
    status,
    headers: { 'content-type': 'application/json', ...headers },
  });
}

describe('createScalixClient end-to-end wiring', () => {
  it('uploads a Blob as raw non-UTF8 bytes', async () => {
    const payload = new Uint8Array([0, 255, 128, 254, 13, 10]);
    const seen: Request[] = [];
    const fakeFetch = vi.fn<typeof fetch>(async (input) => {
      seen.push(input as Request);
      return new Response(null, { status: 200 });
    });
    const client = createScalixClient({
      apiKey: 'scalix_sk_test',
      fetch: fakeFetch,
      sleep: noSleep,
    });

    await putObject({
      client,
      path: { bucket: 'test-bucket', key: 'folder/raw bytes?#.bin' },
      body: new Blob([payload]),
    });

    expect(seen).toHaveLength(1);
    expect(seen[0].method).toBe('PUT');
    expect(seen[0].url).toBe(
      'https://api.scalix.world/v1/storage/buckets/test-bucket/objects/folder%2Fraw%20bytes%3F%23.bin',
    );
    expect(seen[0].headers.get('content-type')).toBe('application/octet-stream');
    expect(new Uint8Array(await seen[0].arrayBuffer())).toEqual(payload);
  });

  it('sends Authorization, User-Agent, and an Idempotency-Key on a POST operation', async () => {
    const seen: Request[] = [];
    const fakeFetch = vi.fn<typeof fetch>(async (input) => {
      seen.push(input as Request);
      return json(200, { rows: [] });
    });

    const client = createScalixClient({
      apiKey: 'scalix_sk_test',
      fetch: fakeFetch as unknown as typeof fetch,
      sleep: noSleep,
    });

    await executeSql({ client, body: { query: 'SELECT 1' } });

    expect(seen).toHaveLength(1);
    const req = seen[0];
    expect(req.method).toBe('POST');
    expect(req.headers.get('authorization')).toBe('Bearer scalix_sk_test');
    expect(req.headers.get('user-agent')).toBe(`scalix-typescript/${VERSION}`);
    expect(req.headers.get('idempotency-key')).toBeTruthy();
  });

  it('replays a retried write with the SAME idempotency key', async () => {
    const keys: (string | null)[] = [];
    const fakeFetch = vi
      .fn<typeof fetch>()
      .mockImplementationOnce(async (input) => {
        keys.push((input as Request).headers.get('idempotency-key'));
        return json(429);
      })
      .mockImplementationOnce(async (input) => {
        keys.push((input as Request).headers.get('idempotency-key'));
        return json(200, { rows: [] });
      });

    const client = createScalixClient({
      apiKey: 'scalix_sk_test',
      fetch: fakeFetch as unknown as typeof fetch,
      sleep: noSleep,
    });

    await executeSql({ client, body: { query: 'SELECT 1' } });

    expect(fakeFetch).toHaveBeenCalledTimes(2);
    expect(keys).toHaveLength(2);
    expect(keys[0]).toBeTruthy();
    expect(keys[0]).toBe(keys[1]); // stable across the retry
  });

  it('does not attach an idempotency key to a GET operation', async () => {
    let seen: Request | undefined;
    const fakeFetch = vi.fn<typeof fetch>(async (input) => {
      seen = input as Request;
      return json(200, { user_id: 'u_1' });
    });

    const client = createScalixClient({
      apiKey: 'scalix_sk_test',
      fetch: fakeFetch as unknown as typeof fetch,
      sleep: noSleep,
    });

    await getMe({ client });

    expect(seen?.method).toBe('GET');
    expect(seen?.headers.get('idempotency-key')).toBeNull();
    expect(seen?.headers.get('authorization')).toBe('Bearer scalix_sk_test');
  });
});
