"""
Scalix SDK — Example 01: Basic Agent

Create a simple AI agent that can answer questions.
No Scalix account needed — runs in local mode.

Prerequisites:
    pip install scalix
    export SCALIX_API_KEY=your-key
"""

import asyncio
from scalix import Agent


async def main():
    # Create a simple agent — no tools, just conversation
    agent = Agent(
        model="scalix-world-ai",
        instructions="You are a helpful assistant that gives concise, clear answers.",
    )

    # Run the agent
    result = await agent.run("What are the top 3 programming languages in 2026?")
    print(result.output)


if __name__ == "__main__":
    asyncio.run(main())
