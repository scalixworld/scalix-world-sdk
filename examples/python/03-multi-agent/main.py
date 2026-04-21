"""
Scalix SDK — Example 03: Multi-Agent Team

Create a team of agents that collaborate on a task.
Each agent has a specific role and expertise.

Prerequisites:
    pip install scalix[local]
    export ANTHROPIC_API_KEY=your-key
"""

import asyncio
from scalix import Agent, Team, Tool


async def main():
    # Define specialized agents
    researcher = Agent(
        model="auto",
        instructions="You are a research specialist. Find and summarize key information.",
        tools=[Tool.web_search()],
    )

    analyst = Agent(
        model="auto",
        instructions="You are a data analyst. Analyze data and extract insights using code.",
        tools=[Tool.code_exec()],
    )

    writer = Agent(
        model="auto",
        instructions="You are a technical writer. Create clear, structured reports.",
    )

    # Create a team with a sequential workflow
    team = Team(
        agents={
            "researcher": researcher,
            "analyst": analyst,
            "writer": writer,
        },
        workflow="researcher → analyst → writer",
    )

    # Run the team
    result = await team.run(
        "Research the current state of AI agent frameworks, "
        "analyze their GitHub star growth, and write a brief report."
    )

    print(result.output)
    print(f"\nWorkflow log: {result.workflow_log}")


if __name__ == "__main__":
    asyncio.run(main())
