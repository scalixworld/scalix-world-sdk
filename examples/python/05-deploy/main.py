"""
Scalix SDK — Example 05: Deploy to Scalix

Deploy an agent to Scalix infrastructure for production use.
This example requires a Scalix account.

Prerequisites:
    pip install scalix[cloud]
    export SCALIX_API_KEY=sk-scalix-your-key
"""

import asyncio
import scalix
from scalix import Agent, Tool


async def main():
    # Connect to Scalix infrastructure
    scalix.configure(api_key="sk-scalix-your-key-here")

    # Create a production agent
    # - model="scalix-world-ai" → Scalix Router picks the best model
    # - code_exec with GPU → runs in Scalix Sandbox (Firecracker)
    # - sql with named DB → uses ScalixDB (managed Postgres)
    agent = Agent(
        model="scalix-world-ai",
        instructions="You are an AI research assistant for production use.",
        tools=[
            Tool.code_exec(runtime="python", gpu="t4"),
            Tool.sql(database="production-db"),
            Tool.web_search(),
        ],
    )

    # Run in cloud mode — uses Scalix infrastructure
    result = await agent.run("Analyze our latest user engagement metrics")
    print(result.output)
    print(f"Model used: {result.model}")
    print(f"Tokens: {result.usage}")


if __name__ == "__main__":
    asyncio.run(main())
