# Scalix SDK — TypeScript

The official TypeScript client for **Scalix Cloud** — one API key for AI inference,
database, functions, storage, KV, auth, registry, and every platform service.

This client is **generated** from the OpenAPI spec (`sdk/openapi.json`, produced from
the gateway's `utoipa` annotations) via [`@hey-api/openapi-ts`](https://heyapi.dev).
Every endpoint is a typed function. **Do not hand-edit `src/generated/`.**

## Installation

```bash
npm install @scalix-world/sdk
```

Get an API key from the [Scalix console](https://console.scalix.world/org/keys)
(sign up at [console.scalix.world](https://console.scalix.world)). Full guides live at
[docs.scalix.world](https://docs.scalix.world/sdks/typescript).

## Usage

Each API operation is an exported, fully-typed function (see the full list in
`src/generated`). Pass your base URL + API key in the options:

```typescript
import { getMe, listFunctions } from '@scalix-world/sdk';

const opts = {
  baseUrl: 'https://api.scalix.world',
  headers: { Authorization: 'Bearer scalix_sk_...' },
};

const me = await getMe(opts);
const fns = await listFunctions(opts);
```

## Production-grade defaults (retry, idempotency, User-Agent)

On top of the generated core, a thin hand-written layer adds Stripe/Auth0-style
resilience without changing the generated code:

- **Automatic retry** with exponential backoff + jitter on `429` and `5xx`,
  honoring the `Retry-After` header (and retrying transient network errors).
- **`Idempotency-Key`** on every write (`POST`/`PUT`/`PATCH`), stable across
  retries — safe replays for billing/provisioning calls.
- **SDK-version `User-Agent`** (`scalix-typescript/<version>`) for server-side
  observability.

Harden the shared default client once, then use the bare operations:

```typescript
import { configureScalix, executeSql } from '@scalix-world/sdk';

configureScalix({ apiKey: process.env.SCALIX_API_KEY });

const { data } = await executeSql({ body: { query: 'SELECT NOW()' } });
```

Or create an isolated client and pass it per call:

```typescript
import { createScalixClient, listFunctions } from '@scalix-world/sdk';

const client = createScalixClient({
  apiKey: process.env.SCALIX_API_KEY,
  maxRetries: 3, // default 2
});

const fns = await listFunctions({ client });
```

The package ships **dual ESM + CommonJS** builds, so both `import` and `require`
consumers are supported.

## Regenerating

After the API (OpenAPI spec) changes:

```bash
npm run generate:ts   # @hey-api/openapi-ts + tsc typecheck
```

CI's `SDK/CLI codegen drift-guard` enforces that the committed client matches
`sdk/openapi.json`.

## License

MIT
