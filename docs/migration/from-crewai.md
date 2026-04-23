# Migrating from CrewAI to Scalix

This guide shows how to convert CrewAI patterns to Scalix.

## Quick comparison

### Basic agent

**CrewAI:**
```python
from crewai import Agent, Task, Crew

agent = Agent(
    role="Researcher",
    goal="Find information",
    backstory="You are an expert researcher.",
    llm="claude-sonnet-4",
)

task = Task(
    description="Research AI trends",
    expected_output="A summary",
    agent=agent,
)

crew = Crew(agents=[agent], tasks=[task])
result = crew.kickoff()
```

**Scalix:**
```python
from scalix import Agent

agent = Agent(
    model="scalix-world-ai",
    instructions="You are an expert researcher.",
)
result = await agent.run("Research AI trends")
```

### Multi-agent crew

**CrewAI:**
```python
from crewai import Agent, Task, Crew, Process

researcher = Agent(role="Researcher", goal="Research", backstory="...", llm="claude-sonnet-4")
writer = Agent(role="Writer", goal="Write", backstory="...", llm="claude-sonnet-4")

task1 = Task(description="Research AI", expected_output="Notes", agent=researcher)
task2 = Task(description="Write report", expected_output="Report", agent=writer)

crew = Crew(
    agents=[researcher, writer],
    tasks=[task1, task2],
    process=Process.sequential,
)
result = crew.kickoff()
```

**Scalix:**
```python
from scalix import Agent, Team

researcher = Agent(model="scalix-world-ai", instructions="You are a researcher.")
writer = Agent(model="scalix-world-ai", instructions="You are a writer.")

team = Team(
    agents={"researcher": researcher, "writer": writer},
    workflow="researcher → writer",
)
result = await team.run("Research AI and write a report")
```

### Tools

**CrewAI:**
```python
from crewai_tools import SerperDevTool, CodeInterpreterTool

agent = Agent(
    role="Analyst",
    tools=[SerperDevTool(), CodeInterpreterTool()],
)
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

**CrewAI:**
```python
from crewai.tools import tool

@tool("Get Weather")
def get_weather(city: str) -> str:
    """Get weather for a city."""
    return "72°F"
```

**Scalix:**
```python
from scalix import Tool

@Tool.function
def get_weather(city: str) -> str:
    """Get weather for a city."""
    return "72°F"
```

## Key differences

| Concept | CrewAI | Scalix |
|---------|--------|--------|
| Agent definition | `role` + `goal` + `backstory` | `model` + `instructions` |
| Task definition | Separate `Task` objects | Inline via `agent.run(prompt)` |
| Orchestration | `Crew` + `Process` | `Team` + `workflow` string |
| Parallel execution | `Process.parallel` | `workflow="parallel"` |
| Sequential | `Process.sequential` | `workflow="A → B → C"` |
| Built-in sandbox | No | Yes |
| Built-in database | No | Yes |
| Deploy to cloud | No | `scalix deploy` |

## Step-by-step migration

1. **Install Scalix:** `pip install scalix`
2. **Replace Agent** — combine `role`/`goal`/`backstory` into `instructions`
3. **Remove Task objects** — pass prompts directly to `agent.run()` or `team.run()`
4. **Replace Crew** — use `Team(agents=..., workflow=...)`
5. **Replace tools** — use built-in `Tool.*` factories or `@Tool.function`
