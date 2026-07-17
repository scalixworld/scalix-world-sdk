/**
 * Scalix SDK — the official TypeScript client for Scalix Cloud.
 *
 * The generated core is auto-generated from the OpenAPI spec (`sdk/openapi.json`,
 * itself generated from the gateway's utoipa annotations) via `@hey-api/openapi-ts`.
 * Regenerate with `npm run generate:ts`. Do NOT hand-edit `src/generated/`.
 *
 * On top of the generated core, a thin hand-written hardening layer (`src/scalix/`)
 * adds Stripe/Auth0-grade defaults: automatic retry with exponential backoff +
 * jitter (honoring `Retry-After`), an `Idempotency-Key` on write requests, and an
 * SDK-version `User-Agent`. Use `configureScalix()` to harden the shared default
 * client, or `createScalixClient()` for an isolated instance.
 *
 * @packageDocumentation
 */

// Generated core: every operation, its types, and the error/response envelopes.
export * from './generated/index.js';

// Generated client factory + default instance (not re-exported by the generated
// index) — so callers can build/inspect clients directly. `Options` is omitted
// here because it already comes through `export *` above (avoids a duplicate).
export { client } from './generated/client.gen.js';
export { createClient, createConfig } from './generated/client/index.js';
export type { Client, ClientOptions, Config, RequestResult } from './generated/client/index.js';

// Hardening layer.
export { createScalixClient, configureScalix, DEFAULT_BASE_URL } from './scalix/client.js';
export type { ScalixClientOptions } from './scalix/client.js';
export {
  createRetryingFetch,
  isRetryableStatus,
  parseRetryAfter,
  computeBackoffMs,
} from './scalix/retry.js';
export type { RetryOptions } from './scalix/retry.js';
export {
  createRequestMiddleware,
  scalixUserAgent,
  IDEMPOTENT_WRITE_METHODS,
} from './scalix/middleware.js';
export type { RequestMiddlewareOptions } from './scalix/middleware.js';

// SDK version (single source of truth: repo-root VERSION file).
export { VERSION } from './version.js';
