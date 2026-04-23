"""
Scalix SDK — Example 02: Code Execution

Create an agent that can write and execute Python code.

Local mode: code runs in Docker on your machine.
Cloud mode: code runs in Scalix Sandbox (Firecracker + GPU).

Prerequisites:
    pip install scalix[local]
    export SCALIX_API_KEY=your-key
    Docker must be running (for local mode)
"""

import asyncio
from scalix import Agent, Tool


async def main():
    # Agent with code execution capability
    agent = Agent(
        model="scalix-advanced",
        instructions="You are a data analyst. Write and execute Python code to answer questions.",
        tools=[
            Tool.code_exec(runtime="python", timeout=30),
        ],
    )

    result = await agent.run(
        "Generate a list of the first 20 Fibonacci numbers and calculate their average."
    )
    print(result.output)

    # Show what tools were called
    for tc in result.tool_calls:
        print(f"\n--- Tool: {tc.tool_name} ---")
        print(f"Result: {tc.result}")


if __name__ == "__main__":
    asyncio.run(main())
