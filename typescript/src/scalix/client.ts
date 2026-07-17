/**
 * The hand-written ergonomics layer over the generated `@hey-api` client:
 * production-grade retry/backoff, idempotency, and an SDK-version User-Agent —
 * Stripe/Auth0-style defaults — without touching the generated core.
 *
 * Two entry points:
 *  - `createScalixClient(options)` — a fresh, isolated hardened `Client` you pass
 *    to any generated operation via its `{ client }` option.
 *  - `configureScalix(options)` — hardens the SHARED default client, so the bare
 *    exported operations (`executeSql(...)`, etc.) get retry/idempotency/UA too.
 */
import { client as defaultClient } from '../generated/client.gen.js';
import { createClient, createConfig } from '../generated/client/index.js';
import type { Client } from '../generated/client/index.js';
import { createRetryingFetch, type RetryOptions } from './retry.js';
import { createRequestMiddleware, scalixUserAgent } from './middleware.js';

export const DEFAULT_BASE_URL = 'https://api.scalix.world';

export interface ScalixClientOptions extends RetryOptions {
  /** Secret key / PAT. Sent as `Authorization: Bearer <apiKey>` on every request. */
  apiKey?: string;
  /** Override the API base URL. Default `https://api.scalix.world`. */
  baseUrl?: string;
  /** Custom fetch implementation to wrap with retry. Default `globalThis.fetch`. */
  fetch?: typeof fetch;
  /** Add `Idempotency-Key` to writes. Default true. */
  idempotency?: boolean;
  /** Full `User-Agent` override. */
  userAgent?: string;
  /** Suffix appended to the default `scalix-typescript/<version>` User-Agent. */
  userAgentSuffix?: string;
}

function applyHardening(client: Client, options: ScalixClientOptions): Client {
  const baseFetch = options.fetch ?? globalThis.fetch;

  client.setConfig({
    ...(options.baseUrl ? { baseUrl: options.baseUrl } : {}),
    ...(options.apiKey ? { headers: { Authorization: `Bearer ${options.apiKey}` } } : {}),
    fetch: createRetryingFetch(baseFetch, options),
  });

  client.interceptors.request.use(
    createRequestMiddleware({
      userAgent: options.userAgent ?? scalixUserAgent(options.userAgentSuffix),
      idempotency: options.idempotency,
    }),
  );

  return client;
}

/** Create a fresh hardened client. Pass it to operations via their `{ client }` option. */
export function createScalixClient(options: ScalixClientOptions = {}): Client {
  const client = createClient(createConfig({ baseUrl: options.baseUrl ?? DEFAULT_BASE_URL }));
  return applyHardening(client, options);
}

/**
 * Harden the SHARED default client used by the bare exported operations. Call once
 * at startup, then use `executeSql(...)`, `chatCompletion(...)`, etc. directly.
 */
export function configureScalix(options: ScalixClientOptions = {}): Client {
  return applyHardening(defaultClient, options);
}
