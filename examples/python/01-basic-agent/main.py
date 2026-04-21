"""
Scalix SDK — Example 01: Basic Agent

Create a simple AI agent that can answer questions.
No Scalix account needed — runs in local mode.

Prerequisites:
    pip install scalix
    export ANTHROPIC_API_KEY=your-key   # or OPENAI_API_KEY
"""

import asyncio
from scalix import Agent


async def main():
    # Create a simple agent — no tools, just conversation
    agent = Agent(
        model="claude-sonnet-4",
        instructions="You are a helpful assistant that gives concise, clear answers.",
    )

    # Run the agent
    result = await agent.run("What are the top 3 programming languages in 2026?")
    print(result.output)


if __name__ == "__main__":
    asyncio.run(main())
