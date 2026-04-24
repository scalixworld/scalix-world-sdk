# Scalix SDK

**One SDK for chat, research, audio, text, RAG, documents, databases, and more.**

The Scalix SDK gives developers typed access to the full Scalix API. Available in Python and TypeScript.

## Quick Start

### Python
```bash
pip install scalix
```

```python
from scalix import Agent, Tool

agent = Agent(
    model="scalix-world-ai",
    tools=[Tool.code_exec(), Tool.web_search()],
)

result = await agent.run("Analyze trending GitHub repos and summarize the top 5")
print(result.output)
```

### TypeScript
```bash
npm install scalix
```

```typescript
import { Agent, Tool } from 'scalix';

const agent = new Agent({
  model: 'scalix-world-ai',
  tools: [Tool.codeExec(), Tool.webSearch()],
});

const result = await agent.run('Analyze trending GitHub repos and summarize the top 5');
console.log(result.output);
```

### Available Models

| Model | Description | Best For |
|-------|-------------|----------|
| `scalix-world-ai` | Default model — fast, balanced | General use, chat, quick tasks |
| `scalix-advanced` | Most capable model — deep reasoning | Complex analysis, coding, agents |

## How It Works

The SDK operates in two modes:

**Local Mode (free, no account)** — code runs in Docker, data in SQLite, LLM calls use your own API keys. Cost to Scalix: $0.

**Cloud Mode (Scalix account)** — code runs in Scalix Sandbox (Firecracker + GPU), data in ScalixDB (managed Postgres), LLM calls routed through Scalix Router. One line switches modes:

```python
import scalix
scalix.configure(api_key="sk_scalix_...")
# Everything now runs on Scalix infrastructure
```

## Features

| Feature | Local Mode | Cloud Mode |
|---------|-----------|------------|
| Agent framework | Yes | Yes |
| Code execution | Docker | Scalix Sandbox (Firecracker + GPU) |
| LLM routing | Direct API calls | Scalix Router (cost-optimized) |
| Persistence | SQLite | ScalixDB (managed Postgres) |
| Deployment | — | `scalix deploy` |
| Multi-agent | Yes | Yes |
| MCP/A2A support | Yes | Yes |
| Cost to you | Your API keys | Usage-based |

## Examples

| Example | Description |
|---------|-------------|
| [01-basic-agent](examples/python/01-basic-agent/) | Simple conversational agent |
| [02-code-execution](examples/python/02-code-execution/) | Agent that writes and runs code |
| [03-multi-agent](examples/python/03-multi-agent/) | Team of agents collaborating |
| [04-database](examples/python/04-database/) | Agent with SQL database access |
| [05-deploy](examples/python/05-deploy/) | Deploy to Scalix cloud |

## API Endpoints

In cloud mode, the SDK communicates with `https://api.scalix.world`. The full endpoint reference:

| Category | Method | Endpoint | Description |
|----------|--------|----------|-------------|
| Chat | POST | `/v1/chat/completions` | Chat completions (OpenAI-compatible) |
| Chat | GET | `/v1/models` | List available models |
| Research | POST | `/v1/research/search` | Web search |
| Research | POST | `/v1/research` | Standard research |
| Research | POST | `/v1/research/deep` | Deep research |
| Audio | POST | `/v1/audio/transcribe` | Speech-to-text (multipart) |
| Audio | POST | `/v1/audio/speak/kokoro` | Text-to-speech |
| Audio | GET | `/v1/audio/kokoro/voices` | Voice list |
| Audio | GET | `/v1/audio/kokoro/languages` | Supported languages |
| Text | POST | `/v1/text/sentiment` | Sentiment analysis |
| Text | POST | `/v1/text/summarize` | Summarize text |
| Text | POST | `/v1/text/translate` | Translate text |
| RAG | POST | `/v1/rag/upload` | Upload document (multipart) |
| RAG | POST | `/v1/rag/query` | Query documents |
| RAG | GET | `/v1/rag/documents` | List documents |
| RAG | DELETE | `/v1/rag/documents/{docId}` | Delete document |
| Storage | POST | `/v1/storage/upload-url` | Get presigned upload URL |
| DocGen | POST | `/v1/docgen/create` | Create document |
| DocGen | POST | `/v1/docgen/preview` | Preview document |
| DocGen | GET | `/v1/docgen/formats` | Supported formats |
| DocGen | GET | `/v1/docgen/templates` | Templates |
| DocGen | GET | `/v1/docgen/history` | Generation history |
| DocGen | GET | `/v1/docgen/download/{docId}` | Download document |
| DocGen | POST | `/v1/docgen/revise` | Revise document |
| DocGen | GET | `/v1/docgen/versions/{docId}` | Document versions |
| ScalixDB | * | `/api/scalixdb/databases/*` | Database management |
| Account | GET | `/health` | Service health check |
| Account | GET | `/api/dashboard/api-keys` | List your API keys |
| Account | POST | `/api/dashboard/api-keys` | Create API key |
| Account | DELETE | `/api/dashboard/api-keys/{id}` | Delete API key |
| Account | GET | `/api/billing/usage` | Usage & billing breakdown |

## Architecture

```
scalix (unified package)
├── Agent Framework        — Create and orchestrate AI agents
├── Tool System            — code_exec, sql, web_search, http, mcp, custom
├── Local Providers        — Docker sandbox, SQLite, direct LLM calls
├── Cloud Providers        — Scalix Sandbox, Router, ScalixDB, Hosting
└── Protocol Support       — MCP server, A2A interop
```

## Supported Languages

| Language | Type | Status |
|----------|------|--------|
| Python | Hand-crafted SDK (Layer 4) | Alpha |
| TypeScript | Hand-crafted SDK (Layer 4) | Alpha |
| Go, Java, C#, Swift, Rust, PHP | Auto-generated from OpenAPI (Layer 3) | Planned |
| Any language | REST API (Layer 2) | Available |

## Documentation

- [Vision Document](VISION.md) — Why we're building this and where it's going
- [Architecture](ARCHITECTURE.md) — Technical design and module structure
- [API Spec](spec/openapi/scalix-api.yml) — OpenAPI specification

## Contributing

We welcome contributions. See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

## License

MIT
