# Migrating from LangChain to Scalix

This guide shows how to convert common LangChain patterns to Scalix.

## Why migrate?

| Feature | LangChain | Scalix |
|---------|-----------|--------|
| Lines of code | 15-30 per agent | 5-10 per agent |
| Built-in sandbox | No | Yes (Docker + Firecracker) |
| Built-in database | No | Yes (SQLite + Postgres) |
| MCP/A2A protocols | Partial | Native |
| Local mode ($0) | N/A | Yes |
| Cloud mode (production) | N/A | Yes (Scalix infrastructure) |

## Quick comparison

### Basic agent

**LangChain:**
```python
from langchain_anthropic import ChatAnthropic
from langchain_core.messages import HumanMessage, SystemMessage
from langchain.agents import AgentExecutor, create_tool_calling_agent
from langchain_core.prompts import ChatPromptTemplate

llm = ChatAnthropic(model="claude-sonnet-4")
prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful assistant."),
    ("human", "{input}"),
    ("placeholder", "{agent_scratchpad}"),
])
agent = create_tool_calling_agent(llm, [], prompt)
executor = AgentExecutor(agent=agent, tools=[])
result = executor.invoke({"input": "Hello!"})
print(result["output"])
```

**Scalix:**
```python
from scalix import Agent

agent = Agent(
    model="scalix-world-ai",
    instructions="You are a helpful assistant.",
)
result = await agent.run("Hello!")
print(result.output)
```

### Agent with tools

**LangChain:**
```python
from langchain_community.tools import DuckDuckGoSearchRun
from langchain_experimental.tools import PythonREPLTool
from langchain.agents import AgentExecutor, create_tool_calling_agent

search = DuckDuckGoSearchRun()
python_repl = PythonREPLTool()

agent = create_tool_calling_agent(llm, [search, python_repl], prompt)
executor = AgentExecutor(agent=agent, tools=[search, python_repl])
```

**Scalix:**
```python
from scalix import Agent, Tool

agent = Agent(
    model="scalix-world-ai",
    tools=[Tool.web_search(), Tool.code_exec()],
)
```

### Custom tools

**LangChain:**
```python
from langchain_core.tools import tool

@tool
def get_weather(city: str) -> str:
    """Get the weather for a city."""
    return f"72°F in {city}"
```

**Scalix:**
```python
from scalix import Tool

@Tool.function
def get_weather(city: str) -> str:
    """Get the weather for a city."""
    return f"72°F in {city}"
```

### Multi-agent

**LangChain (LangGraph):**
```python
from langgraph.graph import StateGraph, MessagesState

graph = StateGraph(MessagesState)
graph.add_node("researcher", researcher_agent)
graph.add_node("writer", writer_agent)
graph.add_edge("researcher", "writer")
app = graph.compile()
result = app.invoke({"messages": [("user", "Write a report")]})
```

**Scalix:**
```python
from scalix import Agent, Team

team = Team(
    agents={"researcher": researcher, "writer": writer},
    workflow="researcher → writer",
)
result = await team.run("Write a report")
```

### Database

**LangChain:**
```python
from langchain_community.utilities import SQLDatabase
from langchain.chains import create_sql_query_chain

db = SQLDatabase.from_uri("sqlite:///my.db")
chain = create_sql_query_chain(llm, db)
```

**Scalix:**
```python
from scalix import Agent, Tool, Database

db = Database()  # SQLite, zero config
agent = Agent(model="scalix-world-ai", tools=[Tool.sql()])
```

## Step-by-step migration

1. **Install Scalix:** `pip install scalix`
2. **Replace agent creation** — use `Agent(model=..., tools=...)` instead of chains/graphs
3. **Replace tools** — use `Tool.code_exec()`, `Tool.web_search()`, `Tool.sql()`, or `@Tool.function`
4. **Replace multi-agent** — use `Team(agents=..., workflow=...)` instead of LangGraph
5. **Remove boilerplate** — Scalix handles prompt templates, output parsing, and execution loops
