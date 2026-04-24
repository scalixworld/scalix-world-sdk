# Scalix World SDK — Technical Architecture

**Version**: 1.0
**Date**: March 19, 2026

---

## 1. System Overview

```
┌─────────────────────────────────────────────────────────────────────┐
│                        DEVELOPER'S APPLICATION                      │
│                                                                     │
│   from scalix import Agent, Tool, Database                          │
│   agent = Agent(model="auto", tools=[Tool.code_exec()])             │
│   result = await agent.run("analyze this dataset")                  │
│                                                                     │
└───────────────────────────────┬─────────────────────────────────────┘
                                │
┌───────────────────────────────▼─────────────────────────────────────┐
│                        SCALIX SDK                                    │
│                                                                     │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────────────────┐  │
│  │    Agent      │  │    Tools     │  │    Configuration         │  │
│  │  Framework    │  │   System     │  │    (local/cloud switch)  │  │
│  └──────┬───────┘  └──────┬───────┘  └────────────┬─────────────┘  │
│         │                 │                        │                │
│  ┌──────▼─────────────────▼────────────────────────▼──────────────┐ │
│  │                    PROVIDER LAYER                               │ │
│  │                                                                 │ │
│  │  ┌─────────────────────┐     ┌──────────────────────────────┐  │ │
│  │  │    LOCAL PROVIDERS   │     │     CLOUD PROVIDERS          │  │ │
│  │  │                     │     │                              │  │ │
│  │  │  DockerSandbox      │     │  ScalixSandbox  ──→ Sandbox  │  │ │
│  │  │  SQLiteStore        │     │  ScalixRouter   ──→ Router   │  │ │
│  │  │  DirectLLM          │     │  ScalixDatabase ──→ ScalixDB │  │ │
│  │  │  LocalFileStore     │     │  ScalixHosting  ──→ Hosting  │  │ │
│  │  │                     │     │  ScalixGateway  ──→ Gateway  │  │ │
│  │  └─────────────────────┘     └──────────────────────────────┘  │ │
│  └────────────────────────────────────────────────────────────────┘ │
│                                                                     │
│  ┌──────────────────────────────────────────────────────────────┐   │
│  │                    PROTOCOL LAYER                             │   │
│  │   MCP Server  │  A2A Protocol  │  REST Client  │  WebSocket  │   │
│  └──────────────────────────────────────────────────────────────┘   │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

---

## 2. Core Modules

### 2.1 Agent Module

The Agent is the central abstraction. It represents an AI-powered entity that can reason, use tools, and maintain state.

```
agent/
├── agent.py          # Agent class — creation, configuration, execution
├── orchestrator.py   # Multi-agent orchestration (Team, Pipeline, Router)
├── memory.py         # Conversation history and long-term memory
├── streaming.py      # Streaming response handler
└── types.py          # Agent-specific type definitions
```

**Key Interfaces:**

```python
class Agent:
    """A single AI agent with tools and memory."""

    def __init__(
        self,
        model: str = "auto",                    # Model name or "auto" for routing
        instructions: str = "",                  # System prompt
        tools: list[Tool] = [],                  # Available tools
        memory: bool = False,                    # Enable conversation memory
        memory_store: MemoryStore | None = None, # Custom memory backend
        provider: Provider | None = None,        # Override default provider
    ): ...

    async def run(self, prompt: str, **kwargs) -> AgentResult: ...
    async def stream(self, prompt: str, **kwargs) -> AsyncIterator[StreamEvent]: ...


class Team:
    """Orchestrate multiple agents working together."""

    def __init__(
        self,
        agents: dict[str, Agent],              # Named agents
        workflow: str | Workflow = "sequential", # Execution strategy
    ): ...

    async def run(self, prompt: str, **kwargs) -> TeamResult: ...
```

### 2.2 Tool System

Tools give agents the ability to interact with the world — execute code, query databases, search the web, call APIs.

```
tools/
├── base.py           # Tool base class and registry
├── builtin.py        # Built-in tools (code_exec, web_search, sql, etc.)
├── mcp.py            # MCP tool adapter (import tools from MCP servers)
├── custom.py         # Custom tool definition helpers
└── types.py          # Tool-specific type definitions
```

**Key Interfaces:**

```python
class Tool:
    """Base class for all tools."""

    name: str
    description: str
    parameters: dict          # JSON Schema for tool parameters

    async def execute(self, **params) -> ToolResult: ...

    # Built-in tool factories
    @staticmethod
    def code_exec(
        runtime: str = "python",
        gpu: str | None = None,      # None (local), "t4", "a100", "h100"
        timeout: int = 30,
    ) -> Tool: ...

    @staticmethod
    def sql(database: str | Database = "local") -> Tool: ...

    @staticmethod
    def web_search(provider: str = "auto") -> Tool: ...

    @staticmethod
    def http(url: str, method: str = "GET") -> Tool: ...

    @staticmethod
    def mcp(server_url: str) -> list[Tool]: ...

    @staticmethod
    def function(fn: Callable) -> Tool:
        """Convert any Python function into a tool."""
        ...
```

### 2.3 Provider Layer

Providers are the backend implementations that execute operations. The SDK ships with two sets of providers: Local (free) and Cloud (Scalix-managed).

```
providers/
├── __init__.py       # Provider registry and auto-detection
├── base.py           # Abstract provider interfaces
├── local/
│   ├── docker_sandbox.py    # Code execution via Docker
│   ├── subprocess_sandbox.py # Code execution via subprocess (lighter)
│   ├── sqlite_store.py      # Persistence via SQLite
│   ├── direct_llm.py        # Direct calls to OpenAI/Anthropic/Google APIs
│   └── file_store.py        # File-based storage
└── cloud/
    ├── sandbox.py           # Wraps scalix-sandbox SDK
    ├── router.py            # Wraps scalix-router SDK
    ├── database.py          # ScalixDB client (new, REST-based)
    ├── hosting.py           # Scalix Hosting client (new, REST-based)
    └── gateway.py           # Scalix AI Gateway client
```

**Provider Selection Logic:**

```python
# Automatic provider selection based on configuration
def resolve_provider(config: ScalixConfig) -> ProviderSet:
    if config.api_key:
        # Cloud mode: use Scalix infrastructure
        return ProviderSet(
            sandbox=ScalixSandbox(config),
            llm=ScalixRouter(config),
            database=ScalixDatabase(config),
            hosting=ScalixHosting(config),
        )
    else:
        # Local mode: use local alternatives
        return ProviderSet(
            sandbox=DockerSandbox() if docker_available() else SubprocessSandbox(),
            llm=DirectLLM(),      # Uses OPENAI_API_KEY, ANTHROPIC_API_KEY, etc.
            database=SQLiteStore(),
            hosting=None,          # No deployment in local mode
        )
```

### 2.4 Configuration System

```
config.py   # Central configuration management
```

**Configuration Hierarchy (lowest to highest priority):**
1. Defaults (local mode, no API keys)
2. Config file (`~/.scalix/config.json` or `scalix.config.json` in project)
3. Environment variables (`SCALIX_API_KEY`, `SCALIX_PROJECT_ID`, etc.)
4. Programmatic (`scalix.configure(api_key="...")`)

```python
# Environment Variables
SCALIX_API_KEY          # Enables cloud mode
SCALIX_PROJECT_ID       # Project identifier
SCALIX_ENVIRONMENT      # "development" | "staging" | "production"
SCALIX_LOG_LEVEL        # "debug" | "info" | "warn" | "error"

# LLM Provider Keys (for local mode)
OPENAI_API_KEY          # Direct OpenAI access
ANTHROPIC_API_KEY       # Direct Anthropic access
GOOGLE_API_KEY          # Direct Google AI access
OLLAMA_HOST             # Local Ollama instance
```

---

## 3. Data Flow

### 3.1 Agent Execution Flow

```
agent.run("analyze sales data")
        │
        ▼
┌─ Agent Loop ─────────────────────────────────────────────────┐
│                                                               │
│  1. Prepare messages (system prompt + user prompt + history)  │
│                   │                                           │
│                   ▼                                           │
│  2. Call LLM (via Router or DirectLLM)                       │
│                   │                                           │
│                   ▼                                           │
│  3. LLM returns response                                     │
│     ├── Text response → return to user                       │
│     └── Tool call → execute tool                             │
│                   │                                           │
│                   ▼                                           │
│  4. Execute tool (via Sandbox or local)                      │
│                   │                                           │
│                   ▼                                           │
│  5. Append tool result to messages                           │
│                   │                                           │
│                   ▼                                           │
│  6. Loop back to step 2 (until LLM returns text or max_turns)│
│                                                               │
└───────────────────────────────────────────────────────────────┘
```

### 3.2 Local Mode Flow

```
agent.run("run this python code")
    │
    ├── LLM call ──→ Direct to Anthropic API (developer's key)
    │                 No Scalix infrastructure involved
    │
    ├── Tool: code_exec ──→ Docker container on developer's machine
    │                        Or subprocess if Docker unavailable
    │
    ├── Tool: sql ──→ SQLite file in project directory
    │
    └── Result returned to developer

    Cost to Scalix: $0
    Cost to developer: LLM API usage only
```

### 3.3 Cloud Mode Flow

```
scalix.configure(api_key="sk_scalix_...")

agent.run("run this python code")
    │
    ├── LLM call ──→ Scalix Router ──→ Best model (cost/quality optimized)
    │                 Smart routing, fallbacks, budget controls
    │
    ├── Tool: code_exec ──→ Scalix Sandbox ──→ Firecracker microVM
    │                        GPU available, VM isolation, auto-scaling
    │
    ├── Tool: sql ──→ ScalixDB ──→ Managed Postgres
    │                  Branching, HA, PITR, connection pooling
    │
    └── Result returned to developer

    Revenue: Usage-based (Sandbox) + Plan-based (Router, DB)
```

---

## 4. Package Structure

### 4.1 Python Package

```
packages/python/
├── pyproject.toml                    # Package configuration
├── scalix/
│   ├── __init__.py                   # Public API: Agent, Tool, Database, configure
│   ├── _version.py                   # Version string
│   ├── config.py                     # Configuration management
│   ├── types.py                      # Shared type definitions
│   ├── exceptions.py                 # Custom exceptions
│   │
│   ├── agent/
│   │   ├── __init__.py
│   │   ├── agent.py                  # Agent class
│   │   ├── orchestrator.py           # Team, Pipeline orchestration
│   │   ├── memory.py                 # Memory management
│   │   └── streaming.py              # Stream handling
│   │
│   ├── tools/
│   │   ├── __init__.py
│   │   ├── base.py                   # Tool base class
│   │   ├── builtin.py                # code_exec, web_search, sql, etc.
│   │   ├── mcp.py                    # MCP tool adapter
│   │   └── custom.py                 # @tool decorator for custom tools
│   │
│   ├── providers/
│   │   ├── __init__.py               # Provider registry
│   │   ├── base.py                   # Abstract interfaces
│   │   ├── local/
│   │   │   ├── __init__.py
│   │   │   ├── docker_sandbox.py     # Docker-based code execution
│   │   │   ├── subprocess_sandbox.py # Subprocess fallback
│   │   │   ├── sqlite_store.py       # SQLite persistence
│   │   │   ├── direct_llm.py        # Direct LLM API calls
│   │   │   └── file_store.py         # Local file storage
│   │   └── cloud/
│   │       ├── __init__.py
│   │       ├── sandbox.py            # Scalix Sandbox client
│   │       ├── router.py             # Scalix Router client
│   │       ├── database.py           # ScalixDB client
│   │       ├── hosting.py            # Scalix Hosting client
│   │       └── gateway.py            # Scalix AI Gateway client
│   │
│   └── protocols/
│       ├── __init__.py
│       ├── mcp_server.py             # Expose agent as MCP server
│       └── a2a.py                    # A2A protocol support
│
└── tests/
    ├── test_agent.py
    ├── test_tools.py
    ├── test_providers/
    └── test_protocols/
```

### 4.2 TypeScript Package

```
packages/typescript/
├── package.json
├── tsconfig.json
├── src/
│   ├── index.ts                      # Public API exports
│   ├── config.ts                     # Configuration management
│   ├── types.ts                      # TypeScript type definitions
│   ├── errors.ts                     # Custom error classes
│   │
│   ├── agent/
│   │   ├── index.ts
│   │   ├── agent.ts                  # Agent class
│   │   ├── orchestrator.ts           # Team, Pipeline orchestration
│   │   ├── memory.ts                 # Memory management
│   │   └── streaming.ts              # Stream handling
│   │
│   ├── tools/
│   │   ├── index.ts
│   │   ├── base.ts                   # Tool base class
│   │   ├── builtin.ts                # Built-in tools
│   │   ├── mcp.ts                    # MCP tool adapter
│   │   └── custom.ts                 # Custom tool helpers
│   │
│   ├── providers/
│   │   ├── index.ts                  # Provider registry
│   │   ├── base.ts                   # Abstract interfaces
│   │   ├── local/
│   │   │   ├── dockerSandbox.ts
│   │   │   ├── subprocessSandbox.ts
│   │   │   ├── sqliteStore.ts
│   │   │   ├── directLlm.ts
│   │   │   └── fileStore.ts
│   │   └── cloud/
│   │       ├── sandbox.ts
│   │       ├── router.ts
│   │       ├── database.ts
│   │       ├── hosting.ts
│   │       └── gateway.ts
│   │
│   └── protocols/
│       ├── mcpServer.ts
│       └── a2a.ts
│
└── tests/
    ├── agent.test.ts
    ├── tools.test.ts
    └── providers/
```

---

## 5. API Specification (OpenAPI)

The OpenAPI spec at `spec/openapi/scalix-api.yml` is the **single source of truth** for:
- All Scalix API endpoints
- Request/response schemas
- Auto-generated SDKs in Go, Java, C#, Swift, Rust, PHP (via Fern)

```
spec/
├── openapi/
│   └── scalix-api.yml          # Complete OpenAPI 3.1 specification
├── protobuf/
│   └── scalix.proto            # gRPC service definitions (future)
└── schemas/
    ├── agent.yml               # Agent-related schemas
    ├── tool.yml                # Tool-related schemas
    ├── sandbox.yml             # Sandbox schemas (re-export existing)
    ├── router.yml              # Router schemas (re-export existing)
    ├── database.yml            # Database schemas
    └── common.yml              # Shared types (errors, pagination, etc.)
```

---

## 6. Protocol Support

### 6.1 MCP (Model Context Protocol)
Scalix agents and tools can be exposed as MCP servers, allowing any MCP-compatible client (Claude Code, Cursor, etc.) to use Scalix infrastructure.

```python
# Expose a Scalix agent as an MCP server
from scalix.protocols import MCPServer

server = MCPServer(
    agent=my_agent,
    tools=[Tool.code_exec(), Tool.sql("my-db")],
)
server.start(port=3000)

# Now any MCP client can connect:
# mcp://localhost:3000
```

### 6.2 A2A (Agent-to-Agent Protocol)
Scalix agents can communicate with agents built on other frameworks via Google's A2A protocol.

```python
from scalix.protocols import A2AServer

a2a = A2AServer(agent=my_agent)
a2a.start()

# External agents can discover and collaborate with this agent
```

---

## 7. Error Handling

```python
# Exception hierarchy
ScalixError                          # Base exception
├── ConfigurationError               # Invalid config, missing keys
├── ProviderError                    # Provider-specific errors
│   ├── SandboxError                 # Code execution failures
│   │   ├── SandboxTimeoutError      # Execution timeout
│   │   └── SandboxResourceError     # Resource limits exceeded
│   ├── RouterError                  # Model routing failures
│   │   ├── ModelNotFoundError       # Requested model unavailable
│   │   ├── RateLimitError           # Rate limit exceeded
│   │   └── QuotaExceededError       # Usage quota exceeded
│   └── DatabaseError                # Database operation failures
├── ToolError                        # Tool execution failures
├── AuthenticationError              # Invalid or missing API key
└── DeploymentError                  # Deployment failures
```

---

## 8. Security Model

### Local Mode
- No Scalix communication — all data stays on developer's machine
- LLM API keys managed by developer (env vars or config)
- Docker provides process-level isolation for code execution
- SQLite database is a local file

### Cloud Mode
- All communication over TLS 1.3
- API key authentication (Bearer token)
- Scalix Sandbox provides VM-level isolation (Firecracker)
- ScalixDB encryption at rest (AES-256)
- No data retention on Scalix Gateway (privacy-first)
- Configurable data residency (GCP regions)

### SDK Security
- No telemetry or analytics without explicit opt-in
- No data sent to Scalix without API key configured
- Dependencies audited and pinned
- Regular security updates

---

## 9. Testing Strategy

### Unit Tests
- Agent logic, tool system, provider interfaces
- Mock all external dependencies (LLM APIs, Docker, network)
- Target: 90% coverage for core modules

### Integration Tests
- Local providers (Docker sandbox, SQLite, direct LLM)
- Cloud providers (against Scalix staging environment)
- MCP/A2A protocol compliance

### End-to-End Tests
- Full agent execution in local mode
- Full agent execution in cloud mode
- Multi-agent orchestration
- Deploy + run workflow

### Compatibility Tests
- Python 3.10, 3.11, 3.12, 3.13
- Node.js 18, 20, 22
- Docker Desktop, Colima, Podman
- macOS, Linux, Windows

---

## 10. Dependencies

### Python SDK
**Required:**
- `httpx` >= 0.25.0 — HTTP client (async)
- `pydantic` >= 2.5.0 — Data validation and serialization

**Optional:**
- `docker` — Docker SDK (for local sandbox)
- `aiosqlite` — Async SQLite (for local persistence)
- `openai` — OpenAI API client (for local mode)
- `anthropic` — Anthropic API client (for local mode)
- `google-generativeai` — Google AI client (for local mode)
- `websockets` — WebSocket support (for streaming)

### TypeScript SDK
**Required:**
- None (zero required dependencies for core)

**Optional:**
- `dockerode` — Docker API client (for local sandbox)
- `better-sqlite3` — SQLite driver (for local persistence)
- `openai` — OpenAI API client (for local mode)
- `@anthropic-ai/sdk` — Anthropic client (for local mode)
- `ws` — WebSocket support
