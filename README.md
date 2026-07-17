# Scalix Cloud SDKs

Official SDK source mirrors for [Scalix Cloud](https://scalix.world) — the agent-native cloud platform: database, functions, AI, storage, auth and more, behind one API key.

| SDK | Package | Install | Docs |
|---|---|---|---|
| [TypeScript](./typescript) | [`@scalix-world/sdk`](https://www.npmjs.com/package/@scalix-world/sdk) | `npm install @scalix-world/sdk` | [docs.scalix.world/sdks/typescript](https://docs.scalix.world/sdks/typescript) |
| [Python](./python) | [`scalix-sdk`](https://pypi.org/project/scalix-sdk/) | `pip install scalix-sdk` | [docs.scalix.world/sdks/python](https://docs.scalix.world/sdks/python) |
| [Auth (TS)](./auth) | [`@scalix-world/auth`](https://www.npmjs.com/package/@scalix-world/auth) | `npm install @scalix-world/auth` | [docs.scalix.world/auth](https://docs.scalix.world/auth) |

## Quick start

```ts
import { configureScalix, executeSql, getMe } from "@scalix-world/sdk";

configureScalix({ apiKey: process.env.SCALIX_API_KEY });
const me = await getMe();
```

```python
from scalix_sdk import create_client
from scalix_sdk.generated.api.account import get_me

client = create_client(token=os.environ["SCALIX_API_KEY"])
me = get_me.sync(client=client)
```

Each SDK's own README ([TypeScript](./typescript/README.md) · [Python](./python/README.md)) covers retries, idempotency, typed errors, and the full function catalog.

Get an API key free at [console.scalix.world](https://console.scalix.world). Full API reference: [docs.scalix.world](https://docs.scalix.world) · Live OpenAPI 3.1 spec: [`api.scalix.world/openapi.json`](https://api.scalix.world/openapi.json).

## About this repository

This is the public source mirror for the Scalix SDKs. The SDK clients are generated from the platform's OpenAPI specification and developed in the Scalix platform monorepo; this mirror is refreshed with each release, and **releases ship to npm and PyPI** (currently `1.3.4`).

- **Issues and PRs are welcome here** — bug reports, typing fixes, and doc improvements are triaged and folded into the next release.
- The MCP server for AI agents is documented at [docs.scalix.world/mcp](https://docs.scalix.world/mcp) (`https://api.scalix.world/v1/mcp`).

## License

MIT — see [LICENSE](./LICENSE).
