/**
 * Automatic retry with exponential backoff + jitter, honoring `Retry-After`.
 *
 * Implemented as a `fetch` wrapper so it composes cleanly under the generated
 * `@hey-api` client (which accepts a custom `fetch`). The layer never touches the
 * generated core — it wraps it. Idempotency-Key + User-Agent are added by the
 * request interceptor (see `middleware.ts`) BEFORE this wrapper runs, so a
 * retried write replays with the same idempotency key.
 */

/** Absolute ceiling for any single sleep, even if a server sends a huge `Retry-After`. */
const RETRY_AFTER_CEILING_MS = 60_000;

export interface RetryOptions {
  /** Max retry attempts after the initial request. Default 2 (3 total tries). */
  maxRetries?: number;
  /** Base backoff in ms (grows ~exponentially). Default 500. */
  baseDelayMs?: number;
  /** Max backoff in ms for the computed (non-`Retry-After`) path. Default 8000. */
  maxDelayMs?: number;
  /** Decide whether a status is retryable. Default: 408, 429, 5xx. */
  isRetryable?: (status: number) => boolean;
  /** Jitter source in [0,1). Default `Math.random`. Injectable for tests. */
  random?: () => number;
  /** Sleep function. Default `setTimeout`. Injectable for tests. */
  sleep?: (ms: number) => Promise<void>;
}

/** Retry on request-timeout, too-many-requests, and any server error. */
export function isRetryableStatus(status: number): boolean {
  return status === 408 || status === 429 || (status >= 500 && status <= 599);
}

/**
 * Parse an HTTP `Retry-After` header into milliseconds. Supports both the
 * delta-seconds form (`"120"`) and the HTTP-date form. Returns `null` when
 * absent or unparseable.
 */
export function parseRetryAfter(headerValue: string | null, nowMs: number = Date.now()): number | null {
  if (!headerValue) return null;
  const trimmed = headerValue.trim();
  if (/^\d+$/.test(trimmed)) {
    return Math.max(0, Number(trimmed) * 1000);
  }
  const dateMs = Date.parse(trimmed);
  if (!Number.isNaN(dateMs)) {
    return Math.max(0, dateMs - nowMs);
  }
  return null;
}

/**
 * Exponential backoff with "full-ish" jitter: the delay is uniformly sampled from
 * [50%, 100%] of `min(maxDelayMs, baseDelayMs * 2^attempt)`. Spreading retries
 * avoids a thundering herd while keeping a sensible floor.
 */
export function computeBackoffMs(
  attempt: number,
  baseDelayMs: number,
  maxDelayMs: number,
  random: () => number,
): number {
  const expo = Math.min(maxDelayMs, baseDelayMs * 2 ** attempt);
  return Math.round(expo * (0.5 + random() * 0.5));
}

const defaultSleep = (ms: number, signal: AbortSignal): Promise<void> =>
  new Promise((resolve, reject) => {
    const onDone = () => {
      signal.removeEventListener('abort', onAbort);
      resolve();
    };
    const timer = setTimeout(onDone, ms);
    const onAbort = () => {
      clearTimeout(timer);
      signal.removeEventListener('abort', onAbort);
      reject(signal.reason);
    };
    signal.addEventListener('abort', onAbort, { once: true });
    if (signal.aborted) onAbort();
  });

async function sleepUnlessAborted(
  ms: number,
  sleep: RetryOptions['sleep'],
  signal: AbortSignal,
): Promise<void> {
  if (!sleep) {
    await defaultSleep(ms, signal);
    return;
  }
  signal.throwIfAborted();

  let removeAbortListener = () => {};
  const aborted = new Promise<never>((_, reject) => {
    const onAbort = () => reject(signal.reason);
    signal.addEventListener('abort', onAbort, { once: true });
    removeAbortListener = () => signal.removeEventListener('abort', onAbort);
    // Close the race between the check above and listener registration.
    if (signal.aborted) onAbort();
  });

  try {
    await Promise.race([sleep(ms), aborted]);
  } finally {
    removeAbortListener();
  }
}

/**
 * Wrap a `fetch` implementation with retry/backoff. Retries `Retry-After`-aware
 * on retryable statuses and on network errors (thrown by `fetch`). The request
 * body is cloned per attempt so a POST can be safely replayed.
 */
export function createRetryingFetch(
  baseFetch: typeof fetch,
  options: RetryOptions = {},
): typeof fetch {
  const maxRetries = options.maxRetries ?? 2;
  const baseDelayMs = options.baseDelayMs ?? 500;
  const maxDelayMs = options.maxDelayMs ?? 8_000;
  const isRetryable = options.isRetryable ?? isRetryableStatus;
  const random = options.random ?? Math.random;
  const sleep = options.sleep;

  return async (input: RequestInfo | URL, init?: RequestInit): Promise<Response> => {
    // Normalize to a Request so the body can be cloned for each attempt.
    const original = input instanceof Request ? input : new Request(input, init);

    let attempt = 0;
    for (;;) {
      original.signal.throwIfAborted();
      try {
        // Clone per attempt: the original is never consumed, so it stays replayable.
        const response = await baseFetch(original.clone());
        if (attempt >= maxRetries || !isRetryable(response.status)) {
          return response;
        }
        const retryAfter = parseRetryAfter(response.headers.get('retry-after'));
        const delay =
          retryAfter !== null
            ? Math.min(retryAfter, RETRY_AFTER_CEILING_MS)
            : computeBackoffMs(attempt, baseDelayMs, maxDelayMs, random);
        // Drain the discarded body so the connection can be reused (undici).
        try {
          await response.arrayBuffer();
        } catch {
          /* ignore */
        }
        await sleepUnlessAborted(delay, sleep, original.signal);
        attempt += 1;
      } catch (error) {
        original.signal.throwIfAborted();
        // Network-level failure (fetch threw). Retry with plain backoff.
        if (attempt >= maxRetries) throw error;
        await sleepUnlessAborted(
          computeBackoffMs(attempt, baseDelayMs, maxDelayMs, random),
          sleep,
          original.signal,
        );
        attempt += 1;
      }
    }
  };
}
