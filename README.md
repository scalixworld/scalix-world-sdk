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
import os
from scalix_sdk import create_client
from scalix_sdk.generated.api.account import get_me

client = create_client(token=os.environ["SCALIX_API_KEY"])
me = get_me.sync(client=client)
```

Each SDK's own README ([TypeScript](./typescript/README.md) · [Python](./python/README.md)) covers retries, idempotency, typed errors, and the full function catalog.

Get an API key free at [console.scalix.world](https://console.scalix.world). Full API reference: [docs.scalix.world](https://docs.scalix.world) · Live OpenAPI 3.1 spec: [`api.scalix.world/openapi.json`](https://api.scalix.world/openapi.json).

## About this repository

**Scalix Cloud** is a proprietary, closed-source managed cloud platform owned by **Scalix World Pvt Ltd** (India) and licensed internationally via **Energy FW Ltd** (UK).

This repository is the public MIT source mirror for the official Scalix Cloud client SDKs, generated from the platform's OpenAPI specification and published regularly to **npm** (`@scalix-world/sdk`, `@scalix-world/auth`) and **PyPI** (`scalix-sdk`).

- **Issues and PRs are welcome here** — bug reports, typing fixes, and doc improvements are triaged and folded into the next release.
- The MCP server for AI agents is documented at [docs.scalix.world/mcp](https://docs.scalix.world/mcp) (`https://api.scalix.world/v1/mcp`).
- **Policies:** [Terms](https://scalix.world/terms) · [Privacy](https://scalix.world/privacy) · [Security](https://scalix.world/security)

## License

MIT — © 2026 Scalix World Pvt Ltd. See [LICENSE](./LICENSE).
