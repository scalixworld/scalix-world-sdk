import { describe, expect, it, vi } from 'vitest';
import {
  computeBackoffMs,
  createRetryingFetch,
  isRetryableStatus,
  parseRetryAfter,
} from '../src/scalix/retry.js';

const noSleep = async () => {};

function jsonResponse(status: number, body: unknown = {}, headers?: Record<string, string>): Response {
  return new Response(JSON.stringify(body), {
    status,
    headers: { 'content-type': 'application/json', ...headers },
  });
}

describe('isRetryableStatus', () => {
  it('retries 408, 429, and 5xx only', () => {
    expect(isRetryableStatus(408)).toBe(true);
    expect(isRetryableStatus(429)).toBe(true);
    expect(isRetryableStatus(500)).toBe(true);
    expect(isRetryableStatus(503)).toBe(true);
    expect(isRetryableStatus(200)).toBe(false);
    expect(isRetryableStatus(400)).toBe(false);
    expect(isRetryableStatus(401)).toBe(false);
    expect(isRetryableStatus(404)).toBe(false);
  });
});

describe('parseRetryAfter', () => {
  it('parses delta-seconds', () => {
    expect(parseRetryAfter('2')).toBe(2000);
    expect(parseRetryAfter('0')).toBe(0);
  });
  it('parses HTTP-date relative to now', () => {
    const now = Date.parse('2026-01-01T00:00:00Z');
    const future = new Date(now + 5000).toUTCString();
    expect(parseRetryAfter(future, now)).toBe(5000);
  });
  it('returns null for missing/garbage', () => {
    expect(parseRetryAfter(null)).toBeNull();
    expect(parseRetryAfter('soon')).toBeNull();
  });
});

describe('computeBackoffMs', () => {
  it('grows exponentially and is capped', () => {
    const noJitter = () => 0; // -> 50% of the exponential term
    expect(computeBackoffMs(0, 500, 8000, noJitter)).toBe(250);
    expect(computeBackoffMs(1, 500, 8000, noJitter)).toBe(500);
    expect(computeBackoffMs(2, 500, 8000, noJitter)).toBe(1000);
    // capped at maxDelayMs (8000) -> 50% floor = 4000
    expect(computeBackoffMs(10, 500, 8000, noJitter)).toBe(4000);
  });
  it('applies jitter within [50%,100%] of the term', () => {
    expect(computeBackoffMs(0, 1000, 8000, () => 1)).toBe(1000);
    expect(computeBackoffMs(0, 1000, 8000, () => 0)).toBe(500);
  });
});

describe('createRetryingFetch', () => {
  it('retries a 429 then returns the 200', async () => {
    const base = vi
      .fn<typeof fetch>()
      .mockResolvedValueOnce(jsonResponse(429))
      .mockResolvedValueOnce(jsonResponse(200, { ok: true }));
    const f = createRetryingFetch(base as unknown as typeof fetch, { sleep: noSleep });

    const res = await f(new Request('https://api.scalix.world/x', { method: 'POST' }));

    expect(base).toHaveBeenCalledTimes(2);
    expect(res.status).toBe(200);
    await expect(res.json()).resolves.toEqual({ ok: true });
  });

  it('retries 5xx up to maxRetries then returns the last response', async () => {
    const base = vi.fn<typeof fetch>().mockResolvedValue(jsonResponse(503));
    const f = createRetryingFetch(base as unknown as typeof fetch, { maxRetries: 2, sleep: noSleep });

    const res = await f(new Request('https://api.scalix.world/x'));

    expect(base).toHaveBeenCalledTimes(3); // initial + 2 retries
    expect(res.status).toBe(503);
  });

  it('does NOT retry a 400', async () => {
    const base = vi.fn<typeof fetch>().mockResolvedValue(jsonResponse(400));
    const f = createRetryingFetch(base as unknown as typeof fetch, { sleep: noSleep });

    const res = await f(new Request('https://api.scalix.world/x'));

    expect(base).toHaveBeenCalledTimes(1);
    expect(res.status).toBe(400);
  });

  it('honors Retry-After for the delay', async () => {
    const sleep = vi.fn(noSleep);
    const base = vi
      .fn<typeof fetch>()
      .mockResolvedValueOnce(jsonResponse(429, {}, { 'retry-after': '3' }))
      .mockResolvedValueOnce(jsonResponse(200));
    const f = createRetryingFetch(base as unknown as typeof fetch, { sleep });

    await f(new Request('https://api.scalix.world/x'));

    expect(sleep).toHaveBeenCalledWith(3000);
  });

  it('retries on a network error then succeeds', async () => {
    const base = vi
      .fn<typeof fetch>()
      .mockRejectedValueOnce(new TypeError('network down'))
      .mockResolvedValueOnce(jsonResponse(200, { ok: true }));
    const f = createRetryingFetch(base as unknown as typeof fetch, { sleep: noSleep });

    const res = await f(new Request('https://api.scalix.world/x'));

    expect(base).toHaveBeenCalledTimes(2);
    expect(res.status).toBe(200);
  });

  it('propagates a network error after exhausting retries', async () => {
    const base = vi.fn<typeof fetch>().mockRejectedValue(new TypeError('down'));
    const f = createRetryingFetch(base as unknown as typeof fetch, { maxRetries: 1, sleep: noSleep });

    await expect(f(new Request('https://api.scalix.world/x'))).rejects.toThrow('down');
    expect(base).toHaveBeenCalledTimes(2); // initial + 1 retry
  });
});
