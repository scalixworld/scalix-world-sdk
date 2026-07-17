# Scalix SDK — Python

The official Python client for **Scalix Cloud** — one API key for AI inference,
database, functions, storage, KV, auth, registry, and every platform service.

This client is **generated** from the OpenAPI spec (`sdk/openapi.json`, produced from
the gateway's `utoipa` annotations) via
[`openapi-python-client`](https://github.com/openapi-generators/openapi-python-client)
(attrs + httpx). **Do not hand-edit `scalix_sdk/generated/`.**

## Installation

```bash
pip install scalix-sdk
```

Get an API key from the [Scalix console](https://console.scalix.world/org/keys)
(sign up at [console.scalix.world](https://console.scalix.world)). Full guides live at
[docs.scalix.world](https://docs.scalix.world/sdks/python).

## Usage

Operations are grouped by tag under `scalix_sdk.generated.api.<tag>`; each has
`sync` / `sync_detailed` / `asyncio` callables:

```python
from scalix_sdk import AuthenticatedClient
from scalix_sdk.generated.api.account import get_me  # see generated/api/ for all tags

client = AuthenticatedClient(base_url="https://api.scalix.world", token="scalix_sk_...")
me = get_me.sync(client=client)
```

## Production-grade defaults (retry, idempotency, typed errors)

`create_client()` returns an `AuthenticatedClient` hardened with Stripe/OpenAI-style
defaults, without changing the generated core:

- **Automatic retry** with exponential backoff + jitter on `429`/`5xx`, honoring
  the `Retry-After` header.
- **`Idempotency-Key`** on every write (`POST`/`PUT`/`PATCH`), stable across
  retries — safe replays for billing/provisioning calls.
- **SDK-version `User-Agent`** (`scalix-python/<version>`).
- **Typed errors raised by default** — `AuthenticationError`, `RateLimitError`,
  `InvalidRequestError`, `NotFoundError`, `ServerError`, … (all subclass
  `ScalixError`), instead of the generic `UnexpectedStatus`.

```python
from scalix_sdk import create_client, RateLimitError
from scalix_sdk.generated.api.database import execute_sql
from scalix_sdk.generated.models import SqlRequest

client = create_client(token="scalix_sk_...", max_retries=3)

try:
    result = execute_sql.sync_detailed(client=client, body=SqlRequest(query="SELECT NOW()"))
except RateLimitError as err:
    print("rate limited; request id:", err.request_id)
```

`create_client` configures both the sync and async underlying clients, so
`asyncio` / `asyncio_detailed` calls are hardened too. Pass `raise_on_error=False`
to keep the raw generated behavior (documented error bodies returned, not raised).

## Regenerating

After the API (OpenAPI spec) changes:

```bash
bash scripts/generate.sh
```

CI's `SDK/CLI codegen drift-guard` enforces that the committed client matches
`sdk/openapi.json`.

## License

MIT
