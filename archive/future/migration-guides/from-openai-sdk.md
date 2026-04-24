# Migrating from OpenAI SDK to Scalix

This guide shows how to convert OpenAI SDK (Agents SDK / Chat Completions) patterns to Scalix.

## Quick comparison

### Basic chat completion

**OpenAI SDK:**
```python
from openai import OpenAI

client = OpenAI()
response = client.chat.completions.create(
    model="gpt-4o",
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "Hello!"},
    ],
)
print(response.choices[0].message.content)
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

### Agent with tools (function calling)

**OpenAI SDK:**
```python
import json
from openai import OpenAI

client = OpenAI()

tools = [
    {
        "type": "function",
        "function": {
            "name": "get_weather",
            "description": "Get weather for a city",
            "parameters": {
                "type": "object",
                "properties": {"city": {"type": "string"}},
                "required": ["city"],
            },
        },
    }
]

def get_weather(city: str) -> str:
    return f"72°F in {city}"

messages = [{"role": "user", "content": "What's the weather in SF?"}]
response = client.chat.completions.create(model="gpt-4o", messages=messages, tools=tools)

# Manual tool execution loop
while response.choices[0].message.tool_calls:
    for tool_call in response.choices[0].message.tool_calls:
        if tool_call.function.name == "get_weather":
            args = json.loads(tool_call.function.arguments)
            result = get_weather(**args)
            messages.append(response.choices[0].message)
            messages.append({
                "role": "tool",
                "tool_call_id": tool_call.id,
                "content": result,
            })
    response = client.chat.completions.create(model="gpt-4o", messages=messages, tools=tools)

print(response.choices[0].message.content)
```

**Scalix:**
```python
from scalix import Agent, Tool

@Tool.function
def get_weather(city: str) -> str:
    """Get weather for a city."""
    return f"72°F in {city}"

agent = Agent(model="scalix-world-ai", tools=[get_weather])
result = await agent.run("What's the weather in SF?")
print(result.output)
```

### OpenAI Agents SDK (beta)

**OpenAI Agents SDK:**
```python
from agents import Agent, Runner

agent = Agent(
    name="Assistant",
    instructions="You are a helpful assistant.",
    model="gpt-4o",
)
result = Runner.run_sync(agent, "Hello!")
print(result.final_output)
```

**Scalix:**
```python
from scalix import Agent

agent = Agent(model="scalix-world-ai", instructions="You are a helpful assistant.")
result = await agent.run("Hello!")
print(result.output)
```

### Code execution

**OpenAI SDK:** Requires external setup (no built-in sandbox)

**Scalix:**
```python
from scalix import Agent, Tool

agent = Agent(
    model="scalix-world-ai",
    tools=[Tool.code_exec()],  # Docker locally, Firecracker in cloud
)
result = await agent.run("Calculate the 100th Fibonacci number")
```

## Key advantages of Scalix

| Feature | OpenAI SDK | Scalix |
|---------|------------|--------|
| Tool execution loop | Manual | Automatic |
| Multi-model support | OpenAI only | Scalix World AI, Scalix Advanced, BYOK |
| Code execution | External | Built-in (Docker + Firecracker) |
| Database | External | Built-in (SQLite + Postgres) |
| Multi-agent | Limited | Team + Pipeline orchestration |
| MCP/A2A protocols | No | Native |
| Deploy | External | `scalix deploy` |

## Step-by-step migration

1. **Install Scalix:** `pip install scalix`
2. **Set your Scalix API key** — `export SCALIX_API_KEY=sk_scalix_...`
3. **Replace chat completions** — use `Agent(model="scalix-world-ai").run(prompt)`
4. **Replace function calling** — use `@Tool.function` and let Scalix handle the loop
5. **Add more capabilities** — `Tool.code_exec()`, `Tool.sql()`, `Tool.web_search()`
