# Scalix World SDK

**Build AI agents in 5 minutes. Deploy to production in one command.**

The Scalix World SDK is a multi-language toolkit for building AI-powered applications and agents with built-in sandboxed code execution, smart LLM routing, and managed persistence. Works locally for free — scales on Scalix when you're ready.

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
scalix.configure(api_key="sk-scalix-...")
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
