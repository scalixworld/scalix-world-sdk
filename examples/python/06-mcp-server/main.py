"""
Scalix SDK — Example 06: MCP Server

Expose your Scalix agent as an MCP server that Claude Code,
Cursor, Windsurf, and other MCP clients can connect to.

Prerequisites:
    pip install scalix[mcp]
    export ANTHROPIC_API_KEY=your-key

Usage:
    python main.py                          # stdio mode (for Claude Code)
    Add to Claude Code settings:
      "mcpServers": {
        "scalix-agent": {
          "command": "python",
          "args": ["main.py"]
        }
      }
"""

import asyncio
from scalix import Agent, Tool
from scalix.protocols import MCPServer


# Define a custom tool
@Tool.function
def calculate_compound_interest(principal: float, rate: float, years: int) -> float:
    """Calculate compound interest on an investment."""
    return principal * (1 + rate / 100) ** years


# Create agent with tools
agent = Agent(
    model="auto",
    instructions="You are a financial analyst assistant.",
    tools=[
        Tool.code_exec(),
        calculate_compound_interest,
    ],
)

# Expose as MCP server
server = MCPServer(
    agent=agent,
    tools=[calculate_compound_interest],
    name="financial-analyst",
)

if __name__ == "__main__":
    server.start()  # stdio transport (default)
