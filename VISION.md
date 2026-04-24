# Scalix World SDK — Vision Document

**Version**: 1.0
**Date**: March 19, 2026
**Status**: Foundation
**Codename**: Project Gravity (the pull factor)

---

## 1. Why We're Building This

Scalix has built a complete AI infrastructure platform — Router, Sandbox, ScalixDB, Hosting, Desktop App, AI Gateway — comparable to what Vercel offers in the web ecosystem. But we have a distribution problem: developers don't discover our products because we lack the open-source developer tool that pulls them in.

**Vercel's lesson**: Next.js (free, open-source) generated $200M ARR in platform revenue by being the framework that naturally led developers to Vercel's infrastructure. The Vercel AI SDK grew 36x in one year (47K → 1.7M npm downloads/day). The framework IS the distribution.

**Our gap**: We have all monetization and no pull. The Scalix World SDK is our pull factor — the free, open-source tool that makes developers discover and adopt Scalix infrastructure organically.

---

## 2. What Is the Scalix World SDK?

The Scalix World SDK is a **multi-language developer toolkit for building AI-powered applications and agents**. It is:

- **A framework** — for building AI agents with tools, memory, and orchestration
- **A client library** — for Scalix's managed services (Sandbox, Router, ScalixDB, Hosting)
- **A protocol bridge** — supporting MCP and A2A for ecosystem interoperability
- **A CLI** — for deploying and managing AI applications on Scalix

It is **NOT**:
- A replacement for Sandbox or Router (it's a client that calls them)
- A product that competes with our paid offerings (it's a door to them)
- A walled garden (it works fully without Scalix infrastructure in local mode)

### The One-Line Pitch

> Build AI agents in 5 minutes. Deploy to production in one command. Works locally for free — scales on Scalix when you're ready.

---

## 3. Design Principles

### 3.1 Zero to Agent in 5 Minutes
A developer should go from `pip install scalix` to a working AI agent in under 5 minutes. No configuration files, no boilerplate, no account signup. If it takes longer, we've failed.

### 3.2 Works Anywhere, Better on Scalix
The SDK must work fully in local mode — Docker for sandboxing, SQLite for persistence, direct LLM API calls for routing. No Scalix account required. When developers choose to connect Scalix infrastructure, everything gets 10x better (Firecracker isolation, GPU compute, smart routing, managed Postgres), but it's never required.

### 3.3 The Upgrade Must Be Natural, Not Forced
Developers hit real walls — they need GPU for ML inference, they need Firecracker for production safety, they need routing for cost optimization. These are genuine needs that local mode can't solve. The upgrade to Scalix services is the path of least resistance, not a paywall shoved in their face.

### 3.4 Protocol-First, Not Library-First
Every capability is backed by a well-defined API. The Python and TypeScript SDKs are hand-crafted for the best DX. Every other language can use the REST API directly or auto-generated clients. No developer is ever locked out.

### 3.5 Respect Existing Ecosystems
Support MCP and A2A protocols so developers using LangChain, CrewAI, or OpenAI's tools can connect to Scalix infrastructure without switching frameworks. Meet developers where they are.

### 3.6 No Cannibalization
The SDK does not include or replace Sandbox, Router, or ScalixDB. It calls them as managed services. Local mode uses free alternatives (Docker, SQLite, direct API calls) that cost Scalix $0.

---

## 4. Target Users

### Primary: AI Application Developers
- Building AI agents, chatbots, copilots, automation tools
- Currently using LangChain/CrewAI/OpenAI SDK + gluing 3-5 services together
- Pain: too many tools, too much integration work, no unified deploy story

### Secondary: Web Developers Adding AI
- Building SaaS products with AI features (search, generation, analysis)
- Currently using Vercel AI SDK or raw OpenAI API
- Pain: need structured outputs, safe code execution, multi-model routing

### Tertiary: Enterprise Development Teams
- Building internal AI tools and agents
- Need self-hosted, air-gapped, compliance-ready infrastructure
- Currently evaluating LangChain Enterprise / AWS Bedrock Agents
- Pain: vendor lock-in, data sovereignty, cost opacity

### Also Served (via API/auto-generated SDKs):
- Go backend developers
- Java/C# enterprise developers
- Mobile developers (Swift/Kotlin)
- Any developer in any language via REST API

---

## 5. Architecture Overview

### The Four Layers

```
LAYER 4: HAND-CRAFTED SDKs (Python, TypeScript)
         Agent framework, tool system, local/cloud switching
         Best DX, full framework capabilities
              │
LAYER 3: AUTO-GENERATED SDKs (Go, Java, C#, Swift, Rust, PHP)
         Typed API clients generated from OpenAPI spec via Fern
         Good DX, API access, no agent framework
              │
LAYER 2: UNIVERSAL PROTOCOLS (REST, WebSocket, gRPC)
         Any language with HTTP can use Scalix
         Always works, no SDK dependency
              │
LAYER 1: ECOSYSTEM INTEROP (MCP, A2A)
         LangChain, CrewAI, OpenAI users connect without switching
         Standards-based, future-proof
```

### Local Mode vs Cloud Mode

```
                    LOCAL MODE (free)           CLOUD MODE (paid)
                    ─────────────────           ─────────────────
Code Execution      Docker container            Scalix Sandbox (Firecracker + GPU)
LLM Routing         Direct API calls            Scalix Router (smart routing + fine-tuning)
Persistence         SQLite file                 ScalixDB (managed Postgres)
Deployment          N/A (runs locally)          Scalix Hosting (Cloud Run + CDN)
LLM Access          Developer's own API keys    Scalix AI Gateway (managed keys)
Cost to Scalix      $0                          Usage-based revenue
```

### How the SDK Connects to Existing Products

```
scalix (unified SDK)
├── Agent Framework           → NEW (the pull factor)
├── Tool System               → NEW (abstractions for tools)
├── Local Providers            → NEW (Docker, SQLite, direct LLM)
└── Cloud Connectors
    ├── Sandbox client         → WRAPS existing scalix-sandbox SDK
    ├── Router client          → WRAPS existing scalix-router SDK
    ├── Database client        → NEW (calls existing Cloud API endpoints)
    ├── Hosting client         → NEW (calls existing Cloud API endpoints)
    └── Gateway client         → NEW (calls existing AI Gateway)
```

---

## 6. Product Boundaries: What's Free vs Paid

### Included in SDK (Free Forever)
- Agent framework (creation, orchestration, tool system)
- Local sandbox (Docker-based code execution)
- Local persistence (SQLite)
- Direct LLM provider calls (developer's own API keys)
- MCP and A2A protocol support
- CLI for local development
- All examples and documentation

### Requires Scalix Account (Paid)
- Scalix Sandbox (Firecracker isolation, GPU compute)
- Scalix Router (smart routing, fine-tuning, GPU orchestration)
- ScalixDB (managed Postgres with branching, HA, PITR)
- Scalix Hosting (deployment, CDN, custom domains)
- Scalix AI Gateway (managed LLM keys, cost tracking)

### Never Exposed via SDK (Enterprise Only)
- Router fine-tuning pipeline
- GPU orchestration console
- Deployment strategies (canary, blue-green, rolling)
- Multi-tenant RBAC
- Air-gapped deployment
- Enterprise SLA + dedicated infrastructure

---

## 7. Developer Experience (DX) Targets

### Installation
```bash
# Python
pip install scalix

# TypeScript
npm install scalix
```

### First Agent (Under 5 Minutes)
```python
from scalix import Agent, Tool

agent = Agent(
    model="scalix-world-ai",
    tools=[Tool.code_exec(), Tool.web_search()],
)

result = await agent.run("Find the top 5 trending GitHub repos and analyze them")
print(result)
```

### Connect to Scalix (One Line)
```python
import scalix
scalix.configure(api_key="sk_scalix_...")

# Same code, now uses Scalix Router + Sandbox + ScalixDB
```

### Deploy to Production (One Command)
```bash
$ scalix deploy --name my-agent
# Deployed to https://my-agent.scalix.app
```

### Multi-Agent Orchestration
```python
from scalix import Agent, Team

researcher = Agent(model="auto", tools=[Tool.web_search()])
analyst = Agent(model="auto", tools=[Tool.code_exec(), Tool.sql("my-db")])
writer = Agent(model="auto", tools=[Tool.text()])

team = Team(
    agents=[researcher, analyst, writer],
    workflow="researcher → analyst → writer",
)

report = await team.run("Create a market analysis report for Q1 2026")
```

### Database Integration
```python
from scalix import Database

# Local mode: SQLite
db = Database()

# Cloud mode: ScalixDB
db = Database("my-scalixdb-instance")

# Same API for both
await db.query("SELECT * FROM users WHERE active = true")
```

---

## 8. Competitive Positioning

### Our Moat: No One Else Has the Full Stack

| Capability | Scalix SDK | LangChain | CrewAI | OpenAI SDK | Vercel AI |
|------------|-----------|-----------|--------|------------|-----------|
| Simple agent API | Y | N (complex) | Y | Y | Y |
| Multi-provider | Y | Y | Y | N (OpenAI only) | Y |
| Built-in sandbox | Y | N | N | N | N |
| Built-in routing | Y | N | N | N | N |
| Built-in persistence | Y | N | N | N | N |
| One-command deploy | Y | N | N | N | Y (web only) |
| MCP + A2A native | Y | Partial | N | Partial | N |
| Self-hosted option | Y | N/A | N | N | N |
| TypeScript + Python | Y | Partial | N (Py only) | N (Py only) | N (TS only) |
| GPU support | Y | N | N | N | N |

### Positioning Statement
"The only AI SDK with built-in sandboxed execution, smart LLM routing, and one-command deployment. Works locally for free. Scales on Scalix when you're ready."

### Anti-Positioning (What We're NOT)
- NOT "a better LangChain" — we're simpler, not more complex
- NOT "another API wrapper" — we have infrastructure behind the SDK
- NOT "cloud-only" — works fully offline in local mode
- NOT "locked to Scalix" — works with any LLM provider, any deployment target

---

## 9. Go-to-Market Strategy

### Phase 1: Launch on GitHub + Hacker News
- Open-source the SDK on GitHub under MIT license
- Show HN post with compelling demo (agent that does something impressive in 5 lines)
- Target: 5K stars in first month

### Phase 2: Developer Content
- "Build X in 5 Minutes with Scalix" tutorial series
- Comparison posts: "Scalix vs LangChain", "Scalix vs CrewAI"
- YouTube/Twitter demos showing the DX
- Target: 15K stars by month 3

### Phase 3: Framework Integrations
- MCP server for Scalix (works with Claude Code, Cursor, etc.)
- A2A adapter for Scalix agents
- LangChain/CrewAI migration guides
- Target: 25K stars by month 6

### Phase 4: Community + Enterprise
- Community Slack/Discord
- Enterprise SDK features (audit logs, SSO, compliance)
- Partner with system integrators (TCS, Infosys, Accenture)
- Target: 50K stars by year 1

---

## 10. Revenue Impact Model

### Conversion Funnel

```
SDK Install (free)                    100,000 developers
    │
    ├── Build locally (free)           80,000 (80% retention)
    │
    ├── Connect Scalix account          8,000 (10% conversion)
    │   ├── Free plan                   4,000
    │   ├── Starter ($19/mo)            2,000  →  $38K/mo
    │   ├── Pro ($49/mo)                1,500  →  $73.5K/mo
    │   └── Team+ ($149+/mo)              500  →  $74.5K/mo
    │
    ├── Use Sandbox (usage-based)       2,000  →  $100-400K/mo
    │
    └── Enterprise Router deal            20   →  $50-200K/mo
                                          ──────────────────
                             Projected:   $336K-$786K/mo
                                          $4M-$9.4M/year
```

These are conservative estimates based on Vercel's conversion rates (5-10% free-to-paid) applied to a smaller but faster-growing market.

---

## 11. Success Metrics

### Year 1 Targets
| Metric | Target | Why It Matters |
|--------|--------|----------------|
| GitHub Stars | 50,000 | Developer mindshare and discoverability |
| Monthly Downloads (npm + PyPI) | 500,000 | Active developer adoption |
| SDK → Platform Conversion | 10% | Revenue generation |
| Sandbox Usage from SDK Users | $100K/mo | Validates the flywheel |
| Community Contributors | 100+ | Ecosystem health |
| Enterprise Deals via SDK | 5 | Validates enterprise path |

### North Star Metric
**Monthly Active SDK Users who connect at least one Scalix service.**
This measures the flywheel: free SDK → paid infrastructure.

---

## 12. Technical Milestones

### M1: Foundation (Current)
- [x] Repository structure
- [x] Vision document
- [ ] Architecture document
- [ ] Python package skeleton (pyproject.toml, entry points)
- [ ] TypeScript package skeleton (package.json, entry points)
- [ ] OpenAPI spec skeleton

### M2: Core Agent Framework
- [ ] Agent class with model integration
- [ ] Tool system (registry, execution, composition)
- [ ] Local providers (Docker sandbox, SQLite, direct LLM)
- [ ] Configuration system (local/cloud switching)
- [ ] Streaming support

### M3: Cloud Integration
- [ ] Scalix Sandbox connector (wraps existing SDK)
- [ ] Scalix Router connector (wraps existing SDK)
- [ ] ScalixDB client (new, calls Cloud API)
- [ ] Scalix Hosting client (new, calls Cloud API)
- [ ] Authentication + API key management

### M4: Protocol Support
- [ ] MCP server implementation
- [ ] A2A protocol support
- [ ] OpenAPI spec completion
- [ ] Auto-generated SDKs (Go, Java, C# via Fern)

### M5: CLI + Deploy
- [ ] Unified `scalix` CLI
- [ ] `scalix deploy` command
- [ ] `scalix dev` (local development server)
- [ ] `scalix logs` (streaming logs)

### M6: Polish + Launch
- [ ] Documentation site
- [ ] Example projects (5+ per language)
- [ ] Migration guides (from LangChain, CrewAI, OpenAI SDK)
- [ ] Performance benchmarks
- [ ] Security audit
- [ ] Public launch

---

## 13. Risks and Mitigations

| Risk | Severity | Mitigation |
|------|----------|------------|
| Market is crowded (LangChain, CrewAI, etc.) | Medium | Differentiate on integrated infrastructure, not just DX |
| LangChain dominance (130K stars) | Medium | LangChain is widely criticized; position as the simple alternative |
| OpenAI SDK locks developers to OpenAI | High | Emphasize multi-provider; many developers actively want to avoid lock-in |
| Execution bandwidth (building two SDKs) | High | Python first, TypeScript weeks later; share spec to prevent drift |
| SDK adopted but no platform conversion | Medium | Ensure cloud mode is genuinely 10x better, not just marginally nicer |
| Cannibalization of Sandbox/Router revenue | Low | SDK uses local substitutes (Docker/SQLite); paid products are untouched |
| Community doesn't contribute | Low | Start with good docs, clear contribution guidelines, responsive maintainers |

---

## 14. Open Questions

1. **Naming**: `scalix` (PyPI/npm) vs `scalix-sdk` vs `@scalix-world/sdk`? Need to check availability.
2. **License**: MIT (maximum adoption) vs Apache 2.0 (patent protection)?
3. **Monorepo vs Polyrepo**: Single repo for Python + TS, or separate repos?
4. **Local sandbox runtime**: Docker (requires Docker Desktop) vs subprocess (lighter but less isolated)?
5. **Default model**: What model should `Agent()` use with no config? Needs to be free/cheap.

---

*This document is the north star for the Scalix World SDK. Every technical decision, every feature prioritization, every design choice should trace back to the principles and goals outlined here.*
