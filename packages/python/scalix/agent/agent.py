"""Core Agent class — the central abstraction of the Scalix SDK."""

from __future__ import annotations

import json
import logging
import time
from typing import Any, AsyncIterator

from scalix.config import get_config, ScalixConfig
from scalix.exceptions import ProviderError, ToolError
from scalix.types import (
    AgentResult,
    Message,
    Role,
    StreamEvent,
    StreamEventType,
    ToolCall,
    ToolCallResult,
    ToolDefinition,
    Usage,
)

logger = logging.getLogger("scalix.agent")


class Agent:
    """An AI agent that can reason, use tools, and maintain state.

    The agent runs an LLM in a loop: it sends messages to the model,
    executes any tool calls the model requests, feeds results back,
    and repeats until the model produces a final text response.

    Args:
        model: LLM model to use. "auto" lets Scalix Router choose optimally.
        instructions: System prompt defining the agent's behavior.
        tools: List of tools the agent can use.
        memory: Whether to persist conversation history across runs.
        max_turns: Maximum number of tool-use loops before stopping.
        temperature: Sampling temperature for LLM responses.
        timeout: Maximum execution time in seconds.

    Example:
        from scalix import Agent, Tool

        agent = Agent(
            model="claude-sonnet-4",
            instructions="You are a helpful data analyst.",
            tools=[Tool.code_exec(), Tool.web_search()],
        )

        result = await agent.run("Analyze the top trending GitHub repos")
        print(result.output)
    """

    def __init__(
        self,
        model: str = "auto",
        instructions: str = "",
        tools: list[Any] | None = None,
        memory: bool = False,
        max_turns: int = 10,
        temperature: float = 0.7,
        timeout: int = 300,
    ) -> None:
        self.model = model
        self.instructions = instructions
        self.tools = tools or []
        self.memory = memory
        self.max_turns = max_turns
        self.temperature = temperature
        self.timeout = timeout

        self._history: list[Message] = []
        self._config = get_config()
        self._llm_provider: Any = None
        self._tool_executor: Any = None

    def _get_llm_provider(self) -> Any:
        """Get the LLM provider (lazy initialization)."""
        if self._llm_provider is None:
            if self._config.is_cloud_mode:
                from scalix.providers.cloud.router import ScalixRouterProvider

                self._llm_provider = ScalixRouterProvider(self._config)
            else:
                from scalix.providers.local.direct_llm import DirectLLM

                self._llm_provider = DirectLLM(self._config)
        return self._llm_provider

    def _get_tool_executor(self) -> ToolExecutor:
        """Get the tool executor (lazy initialization)."""
        if self._tool_executor is None:
            self._tool_executor = ToolExecutor(self.tools, self._config)
        return self._tool_executor

    async def run(self, prompt: str, **kwargs: Any) -> AgentResult:
        """Execute the agent with the given prompt.

        The agent will call the LLM, execute any tool calls, and loop
        until it produces a final text response or hits max_turns.

        Args:
            prompt: The user's input prompt.
            **kwargs: Additional parameters passed to the LLM.

        Returns:
            AgentResult with the agent's output, messages, and tool call history.
        """
        llm = self._get_llm_provider()
        executor = self._get_tool_executor()

        # Build initial messages
        messages = self._build_messages(prompt)
        all_tool_results: list[ToolCallResult] = []
        total_usage = Usage()
        used_model: str | None = None

        # Get tool definitions for the LLM
        tool_defs = [t.definition.model_dump() for t in self.tools] if self.tools else None

        for turn in range(self.max_turns):
            logger.debug("Agent turn %d/%d", turn + 1, self.max_turns)

            # Call LLM
            response = await llm.chat(
                messages=messages,
                model=self.model,
                tools=tool_defs,
                temperature=self.temperature,
                **kwargs,
            )

            messages.append(response)

            # If no tool calls, we have the final response
            if not response.tool_calls:
                logger.debug("Agent finished with text response")
                break

            # Execute each tool call
            for tool_call in response.tool_calls:
                logger.debug("Executing tool: %s", tool_call.name)
                tool_result = await executor.execute(tool_call)
                all_tool_results.append(tool_result)

                # Add tool result as a message for the next LLM call
                result_content = (
                    json.dumps(tool_result.result)
                    if not isinstance(tool_result.result, str)
                    else tool_result.result
                )
                if tool_result.error:
                    result_content = f"Error: {tool_result.error}"

                messages.append(
                    Message(
                        role=Role.TOOL,
                        content=result_content,
                        tool_call_id=tool_call.id,
                        name=tool_call.name,
                    )
                )
        else:
            # Hit max_turns — get final response without tools
            logger.warning("Agent hit max_turns (%d), forcing final response", self.max_turns)
            response = await llm.chat(
                messages=messages,
                model=self.model,
                temperature=self.temperature,
                **kwargs,
            )
            messages.append(response)

        # Update memory
        if self.memory:
            self._history = messages.copy()

        # Extract final output
        final_output = messages[-1].content if messages else ""

        return AgentResult(
            output=final_output,
            messages=messages,
            tool_calls=all_tool_results,
            model=used_model,
            usage=total_usage if total_usage.total_tokens > 0 else None,
        )

    async def stream(self, prompt: str, **kwargs: Any) -> AsyncIterator[StreamEvent]:
        """Execute the agent and stream events as they occur.

        Yields StreamEvent objects for text deltas, tool calls, and results.

        Args:
            prompt: The user's input prompt.
            **kwargs: Additional parameters passed to the LLM.

        Yields:
            StreamEvent objects representing each step of execution.
        """
        llm = self._get_llm_provider()
        executor = self._get_tool_executor()
        messages = self._build_messages(prompt)
        tool_defs = [t.definition.model_dump() for t in self.tools] if self.tools else None

        for turn in range(self.max_turns):
            # If no tools or non-streaming needed, fall back to run
            if not self.tools:
                async for event in llm.stream_chat(
                    messages=messages,
                    model=self.model,
                    temperature=self.temperature,
                    **kwargs,
                ):
                    yield event
                return

            # With tools, we need the full response to check for tool calls
            response = await llm.chat(
                messages=messages,
                model=self.model,
                tools=tool_defs,
                temperature=self.temperature,
                **kwargs,
            )

            messages.append(response)

            if not response.tool_calls:
                # Stream the final text response
                yield StreamEvent(type=StreamEventType.TEXT_DELTA, data=response.content)
                yield StreamEvent(type=StreamEventType.DONE)
                return

            # Execute tools and stream their results
            for tool_call in response.tool_calls:
                yield StreamEvent(
                    type=StreamEventType.TOOL_CALL_START,
                    tool_name=tool_call.name,
                    tool_call_id=tool_call.id,
                    data=tool_call.arguments,
                )

                tool_result = await executor.execute(tool_call)

                result_content = (
                    json.dumps(tool_result.result)
                    if not isinstance(tool_result.result, str)
                    else tool_result.result
                )
                if tool_result.error:
                    result_content = f"Error: {tool_result.error}"

                yield StreamEvent(
                    type=StreamEventType.TOOL_RESULT,
                    tool_name=tool_call.name,
                    tool_call_id=tool_call.id,
                    data=result_content,
                )

                messages.append(
                    Message(
                        role=Role.TOOL,
                        content=result_content,
                        tool_call_id=tool_call.id,
                        name=tool_call.name,
                    )
                )

        yield StreamEvent(type=StreamEventType.DONE)

    def _build_messages(self, prompt: str) -> list[Message]:
        """Build the message list for an LLM call."""
        messages: list[Message] = []

        # System prompt
        if self.instructions:
            messages.append(Message(role=Role.SYSTEM, content=self.instructions))

        # History (if memory enabled)
        if self.memory and self._history:
            # Skip system message from history (we already added it)
            for msg in self._history:
                if msg.role != Role.SYSTEM:
                    messages.append(msg)

        # User prompt
        messages.append(Message(role=Role.USER, content=prompt))

        return messages

    def get_tool_definitions(self) -> list[ToolDefinition]:
        """Get JSON Schema definitions for all registered tools."""
        return [tool.definition for tool in self.tools]

    def clear_memory(self) -> None:
        """Clear the agent's conversation history."""
        self._history.clear()

    def __repr__(self) -> str:
        tool_names = [t.name for t in self.tools] if self.tools else []
        return (
            f"Agent(model={self.model!r}, "
            f"tools={tool_names}, "
            f"memory={self.memory})"
        )


class ToolExecutor:
    """Executes tool calls by routing to the appropriate provider.

    Maps tool names to their execution backends:
    - code_exec → DockerSandbox (local) or ScalixSandbox (cloud)
    - sql → SQLiteProvider (local) or ScalixDB (cloud)
    - web_search → httpx-based search
    - http → httpx request
    - Custom tools → their registered execute functions
    """

    def __init__(self, tools: list[Any], config: ScalixConfig) -> None:
        self._tools = {tool.name: tool for tool in tools}
        self._config = config
        self._sandbox: Any = None
        self._database: Any = None

    async def execute(self, tool_call: ToolCall) -> ToolCallResult:
        """Execute a tool call and return the result."""
        start_time = time.monotonic()

        tool = self._tools.get(tool_call.name)
        if tool is None:
            return ToolCallResult(
                tool_name=tool_call.name,
                arguments=tool_call.arguments,
                result=None,
                error=f"Unknown tool: {tool_call.name}",
            )

        try:
            if tool_call.name == "code_exec":
                result = await self._execute_code(tool_call.arguments)
            elif tool_call.name == "sql":
                result = await self._execute_sql(tool_call.arguments)
            elif tool_call.name == "web_search":
                result = await self._execute_web_search(tool_call.arguments)
            elif tool_call.name == "http":
                result = await self._execute_http(tool_call.arguments)
            elif tool.has_execute_fn:
                # Custom tool with registered function
                result = await tool.execute(**tool_call.arguments)
                return result
            else:
                result = f"Tool '{tool_call.name}' has no execution handler"

            duration = (time.monotonic() - start_time) * 1000
            return ToolCallResult(
                tool_name=tool_call.name,
                arguments=tool_call.arguments,
                result=result,
                duration_ms=duration,
            )
        except Exception as e:
            duration = (time.monotonic() - start_time) * 1000
            logger.error("Tool '%s' failed: %s", tool_call.name, str(e))
            return ToolCallResult(
                tool_name=tool_call.name,
                arguments=tool_call.arguments,
                result=None,
                error=str(e),
                duration_ms=duration,
            )

    async def _get_sandbox(self) -> Any:
        """Get sandbox provider (lazy init)."""
        if self._sandbox is None:
            if self._config.is_cloud_mode:
                from scalix.providers.cloud.sandbox import ScalixSandboxProvider

                self._sandbox = ScalixSandboxProvider(self._config)
            else:
                from scalix.providers.local.docker_sandbox import DockerSandbox

                self._sandbox = DockerSandbox()
        return self._sandbox

    async def _get_database(self) -> Any:
        """Get database provider (lazy init)."""
        if self._database is None:
            from scalix.providers.local.sqlite_store import SQLiteProvider

            self._database = SQLiteProvider()
        return self._database

    async def _execute_code(self, arguments: dict[str, Any]) -> Any:
        """Execute code via sandbox provider."""
        sandbox = await self._get_sandbox()
        code = arguments.get("code", "")
        runtime = arguments.get("runtime", "python")
        result = await sandbox.execute(code=code, runtime=runtime)
        output = result.stdout
        if result.stderr:
            output += f"\nSTDERR:\n{result.stderr}"
        if result.exit_code != 0:
            output += f"\n[Exit code: {result.exit_code}]"
        return output

    async def _execute_sql(self, arguments: dict[str, Any]) -> Any:
        """Execute SQL via database provider."""
        db = await self._get_database()
        query = arguments.get("query", "")
        rows = await db.query(query)
        return rows

    async def _execute_web_search(self, arguments: dict[str, Any]) -> Any:
        """Execute web search via Scalix API or configurable endpoint."""
        import httpx
        from ..config import get_config

        query = arguments.get("query", "")
        config = get_config()
        headers: dict[str, str] = {"User-Agent": "Scalix-SDK/0.1"}

        if config.search_base_url:
            search_url = config.search_base_url
        else:
            search_url = f"{config.base_url}/v1/search"
        if config.api_key:
            headers["Authorization"] = f"Bearer {config.api_key}"

        async with httpx.AsyncClient(timeout=15.0) as client:
            resp = await client.get(
                search_url,
                params={"q": query},
                headers=headers,
            )
            return resp.text[:5000]

    async def _execute_http(self, arguments: dict[str, Any]) -> Any:
        """Execute HTTP request."""
        import httpx

        url = arguments.get("url", "")
        method = arguments.get("method", "GET").upper()
        body = arguments.get("body")

        async with httpx.AsyncClient(timeout=30.0) as client:
            resp = await client.request(method, url, json=body)
            return {"status": resp.status_code, "body": resp.text[:5000]}
