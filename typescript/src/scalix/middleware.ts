/**
 * Request middleware for the hardening layer: an SDK-version `User-Agent` and an
 * `Idempotency-Key` on write requests. Installed as a `@hey-api` request
 * interceptor, which runs once per logical request (before the retrying fetch),
 * so retries of a write replay with the SAME idempotency key.
 */
import { VERSION } from '../version.js';

/** Methods that create/mutate server state and should carry an idempotency key. */
export const IDEMPOTENT_WRITE_METHODS: ReadonlySet<string> = new Set(['POST', 'PUT', 'PATCH']);

/** `scalix-typescript/<version>`, optionally with a caller-supplied suffix. */
export function scalixUserAgent(suffix?: string): string {
  const base = `scalix-typescript/${VERSION}`;
  return suffix ? `${base} ${suffix}` : base;
}

function defaultIdempotencyKey(): string {
  const c = (globalThis as { crypto?: { randomUUID?: () => string } }).crypto;
  if (c?.randomUUID) return c.randomUUID();
  // Fallback for runtimes without WebCrypto (older Node). Not cryptographically
  // strong, but idempotency keys only need to be unique per client-generated write.
  return `idem_${Date.now().toString(36)}_${Math.random().toString(36).slice(2, 12)}`;
}

export interface RequestMiddlewareOptions {
  /** Full `User-Agent` override. When set, `userAgentSuffix` is ignored. */
  userAgent?: string;
  /** Add `Idempotency-Key` to POST/PUT/PATCH. Default true. */
  idempotency?: boolean;
  /** Idempotency-key generator. Default WebCrypto `randomUUID`. */
  generateIdempotencyKey?: () => string;
}

/**
 * Build a `@hey-api` request interceptor `(request) => request`. Mutates the
 * request's headers in place (headers on a fetch `Request` are mutable). Existing
 * caller-set headers win — we never overwrite a `User-Agent` or `Idempotency-Key`
 * the caller already provided.
 */
export function createRequestMiddleware(options: RequestMiddlewareOptions = {}) {
  const userAgent = options.userAgent ?? scalixUserAgent();
  const idempotency = options.idempotency ?? true;
  const generateKey = options.generateIdempotencyKey ?? defaultIdempotencyKey;

  return (request: Request): Request => {
    if (!request.headers.has('user-agent')) {
      // Browsers forbid setting User-Agent and will throw/ignore — that's fine,
      // the browser's own UA is used and this matters mostly for server-side Node.
      try {
        request.headers.set('User-Agent', userAgent);
      } catch {
        /* forbidden header in this runtime */
      }
    }

    if (
      idempotency &&
      IDEMPOTENT_WRITE_METHODS.has(request.method.toUpperCase()) &&
      !request.headers.has('idempotency-key')
    ) {
      request.headers.set('Idempotency-Key', generateKey());
    }

    return request;
  };
}
