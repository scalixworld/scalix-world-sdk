"""Multi-agent orchestration — Team and Pipeline patterns."""

from __future__ import annotations

import asyncio
import logging
from typing import Any

from scalix.agent.agent import Agent
from scalix.types import AgentResult, TeamResult

logger = logging.getLogger("scalix.orchestrator")


class Team:
    """Orchestrate multiple agents working together on a task.

    Agents can work sequentially (pipeline), in parallel, or with
    dynamic routing based on the task.

    Supports three workflow modes:
    - "sequential" — agents run in dict insertion order, each receiving
      the previous agent's output
    - "parallel" — all agents run simultaneously on the same prompt,
      outputs are combined
    - "A → B → C" — explicit ordering with arrow syntax

    Args:
        agents: Named dictionary of agents.
        workflow: Execution strategy — "sequential", "parallel", or
                  a custom workflow string like "researcher → analyst → writer".

    Example:
        from scalix import Agent, Team, Tool

        researcher = Agent(model="auto", tools=[Tool.web_search()])
        analyst = Agent(model="auto", tools=[Tool.code_exec()])
        writer = Agent(model="auto")

        team = Team(
            agents={
                "researcher": researcher,
                "analyst": analyst,
                "writer": writer,
            },
            workflow="researcher → analyst → writer",
        )

        result = await team.run("Create a market analysis report")
    """

    def __init__(
        self,
        agents: dict[str, Agent],
        workflow: str = "sequential",
    ) -> None:
        self.agents = agents
        self.workflow = workflow
        self._order = self._parse_workflow(workflow)

    def _parse_workflow(self, workflow: str) -> list[str]:
        """Parse workflow string into an ordered list of agent names."""
        if workflow == "sequential":
            return list(self.agents.keys())
        elif workflow == "parallel":
            return list(self.agents.keys())
        else:
            # Parse arrow syntax: "researcher → analyst → writer"
            # Support both → and ->
            names = [
                name.strip()
                for name in workflow.replace("→", "->").split("->")
            ]
            # Validate all names exist
            for name in names:
                if name not in self.agents:
                    raise ValueError(
                        f"Agent '{name}' in workflow not found. "
                        f"Available: {list(self.agents.keys())}"
                    )
            return names

    async def run(self, prompt: str, **kwargs: Any) -> TeamResult:
        """Execute the team workflow with the given prompt.

        Args:
            prompt: The initial task prompt.
            **kwargs: Additional parameters passed to each agent.

        Returns:
            TeamResult with combined output from all agents.
        """
        if self.workflow == "parallel":
            return await self._run_parallel(prompt, **kwargs)
        else:
            return await self._run_sequential(prompt, **kwargs)

    async def _run_sequential(self, prompt: str, **kwargs: Any) -> TeamResult:
        """Run agents sequentially, each receiving the previous output."""
        agent_results: dict[str, AgentResult] = {}
        workflow_log: list[str] = []
        current_input = prompt

        for name in self._order:
            agent = self.agents[name]
            logger.debug("Team: running agent '%s'", name)
            workflow_log.append(f"Running agent: {name}")

            result = await agent.run(current_input, **kwargs)
            agent_results[name] = result
            workflow_log.append(f"Agent '{name}' completed: {len(result.output)} chars")

            # Pass this agent's output as input to the next agent
            current_input = (
                f"Previous agent ({name}) produced the following output:\n\n"
                f"{result.output}\n\n"
                f"Original task: {prompt}\n\n"
                f"Continue from where the previous agent left off."
            )

        # Final output is the last agent's output
        final_output = agent_results[self._order[-1]].output if self._order else ""

        return TeamResult(
            output=final_output,
            agent_results=agent_results,
            workflow_log=workflow_log,
        )

    async def _run_parallel(self, prompt: str, **kwargs: Any) -> TeamResult:
        """Run all agents in parallel on the same prompt."""
        agent_results: dict[str, AgentResult] = {}
        workflow_log: list[str] = ["Running all agents in parallel"]

        async def run_agent(name: str, agent: Agent) -> tuple[str, AgentResult]:
            logger.debug("Team (parallel): running agent '%s'", name)
            result = await agent.run(prompt, **kwargs)
            return name, result

        tasks = [
            run_agent(name, self.agents[name])
            for name in self._order
        ]
        results = await asyncio.gather(*tasks, return_exceptions=True)

        for item in results:
            if isinstance(item, BaseException):
                workflow_log.append(f"Agent failed: {item}")
                continue
            assert isinstance(item, tuple)
            name, result = item
            agent_results[name] = result
            workflow_log.append(f"Agent '{name}' completed: {len(result.output)} chars")

        # Combine all outputs
        combined_parts = []
        for name in self._order:
            if name in agent_results:
                combined_parts.append(
                    f"=== {name} ===\n{agent_results[name].output}"
                )

        return TeamResult(
            output="\n\n".join(combined_parts),
            agent_results=agent_results,
            workflow_log=workflow_log,
        )

    def __repr__(self) -> str:
        agent_names = list(self.agents.keys())
        return f"Team(agents={agent_names}, workflow={self.workflow!r})"


class Pipeline:
    """A linear chain of agents where each agent's output feeds the next.

    This is a simpler alternative to Team for straightforward sequential workflows.

    Args:
        steps: Ordered list of agents to execute in sequence.

    Example:
        from scalix import Agent, Pipeline

        pipeline = Pipeline(steps=[
            Agent(instructions="Extract key facts from the input"),
            Agent(instructions="Summarize the facts into bullet points"),
            Agent(instructions="Format as a professional report"),
        ])

        result = await pipeline.run("Raw data: ...")
    """

    def __init__(self, steps: list[Agent]) -> None:
        self.steps = steps

    async def run(self, prompt: str, **kwargs: Any) -> TeamResult:
        """Execute the pipeline sequentially.

        Each agent receives the previous agent's output as its prompt.

        Args:
            prompt: Input to the first agent in the pipeline.
            **kwargs: Additional parameters passed to each agent.

        Returns:
            TeamResult with output from the final agent.
        """
        agent_results: dict[str, AgentResult] = {}
        workflow_log: list[str] = []
        current_input = prompt

        for i, agent in enumerate(self.steps):
            step_name = f"step_{i}"
            logger.debug("Pipeline: running step %d/%d", i + 1, len(self.steps))
            workflow_log.append(f"Running step {i + 1}/{len(self.steps)}")

            result = await agent.run(current_input, **kwargs)
            agent_results[step_name] = result
            workflow_log.append(
                f"Step {i + 1} completed: {len(result.output)} chars"
            )

            # Feed output to next step
            current_input = result.output

        # Final output is the last step's output
        final_output = (
            agent_results[f"step_{len(self.steps) - 1}"].output
            if self.steps
            else ""
        )

        return TeamResult(
            output=final_output,
            agent_results=agent_results,
            workflow_log=workflow_log,
        )

    def __repr__(self) -> str:
        return f"Pipeline(steps={len(self.steps)} agents)"
