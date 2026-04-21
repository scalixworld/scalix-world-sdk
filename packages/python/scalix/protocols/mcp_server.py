"""MCP (Model Context Protocol) server — expose Scalix agents and tools.

Allows any MCP-compatible client (Claude Code, Cursor, Windsurf, etc.)
to use Scalix agents and tools via the standard MCP protocol.

Usage:
    from scalix import Agent, Tool
    from scalix.protocols import MCPServer

    agent = Agent(model="claude-sonnet-4", tools=[Tool.code_exec()])
    server = MCPServer(agent=agent)
    server.start()  # stdio transport (default for CLI tools)
"""

from __future__ import annotations

import asyncio
import json
import logging
from typing import Any, TYPE_CHECKING

if TYPE_CHECKING:
    from scalix.agent.agent import Agent
    from scalix.tools.base import Tool

logger = logging.getLogger("scalix.protocols.mcp")


class MCPServer:
    """Expose Scalix agents and tools as an MCP server.

    This allows any MCP-compatible client to discover and invoke
    Scalix tools, or run the agent directly via a "run_agent" tool.

    Args:
        agent: Optional Scalix Agent to expose. When provided, a
            "run_agent" tool is registered that invokes the agent.
        tools: Optional list of additional Scalix Tools to expose.
            Each tool is registered as an MCP tool.
        name: Server name shown to MCP clients.
    """

    def __init__(
        self,
        agent: Agent | None = None,
        tools: list[Tool] | None = None,
        name: str = "scalix",
    ) -> None:
        self._agent = agent
        self._tools = tools or []
        self._name = name
        self._mcp: Any = None

    def _build_server(self) -> Any:
        """Build the FastMCP server with registered tools."""
        if self._mcp is not None:
            return self._mcp

        try:
            from mcp.server.fastmcp import FastMCP
        except ImportError:
            raise ImportError(
                "MCP package not installed. Run: pip install 'scalix[mcp]' "
                "or pip install mcp"
            )

        mcp = FastMCP(name=self._name)

        # Register each Scalix Tool as an MCP tool
        for tool in self._tools:
            self._register_tool(mcp, tool)

        # If an agent is provided, register a "run_agent" tool
        if self._agent is not None:
            self._register_agent_tool(mcp, self._agent)

        self._mcp = mcp
        return mcp

    def _register_tool(self, mcp: Any, tool: Tool) -> None:
        """Register a Scalix Tool as an MCP tool."""
        tool_name = tool.name
        tool_description = tool.description
        tool_obj = tool

        # Build the parameter schema for MCP
        properties = tool.parameters.get("properties", {})
        required = tool.parameters.get("required", [])

        @mcp.tool(name=tool_name, description=tool_description)
        async def _mcp_tool_handler(
            **kwargs: Any,
            _tool_obj: Any = tool_obj,
        ) -> str:
            """Dynamically registered MCP tool handler."""
            if _tool_obj.has_execute_fn:
                result = await _tool_obj.execute(**kwargs)
                return json.dumps(result.result, default=str)
            else:
                # Return the arguments as-is for tools without execute fns
                # (the agent's tool executor handles routing)
                return json.dumps(
                    {"tool": _tool_obj.name, "arguments": kwargs},
                    default=str,
                )

    def _register_agent_tool(self, mcp: Any, agent: Agent) -> None:
        """Register the agent's run() method as an MCP tool."""
        agent_ref = agent

        @mcp.tool(
            name="run_agent",
            description=(
                f"Run the Scalix agent"
                + (f": {agent_ref.instructions[:100]}" if agent_ref.instructions else "")
                + ". Send a prompt and get the agent's response."
            ),
        )
        async def _run_agent(prompt: str) -> str:
            """Run the Scalix agent with the given prompt."""
            result = await agent_ref.run(prompt)
            return result.output

    def start(self, transport: str = "stdio") -> None:
        """Start the MCP server.

        Args:
            transport: Transport mechanism. "stdio" for local CLI tools,
                "sse" for remote HTTP connections.
        """
        mcp = self._build_server()
        logger.info("Starting MCP server '%s' with transport '%s'", self._name, transport)
        mcp.run(transport=transport)

    async def start_async(self, transport: str = "stdio") -> None:
        """Start the MCP server asynchronously."""
        mcp = self._build_server()
        logger.info("Starting MCP server '%s' (async) with transport '%s'", self._name, transport)
        # FastMCP.run() handles the event loop, so for async contexts
        # we run it in a thread to avoid blocking
        await asyncio.to_thread(mcp.run, transport=transport)

    def get_app(self) -> Any:
        """Get the ASGI app for mounting on an existing server.

        Returns an ASGI application that can be mounted on FastAPI/Starlette.

        Example:
            from fastapi import FastAPI
            app = FastAPI()
            mcp_server = MCPServer(agent=my_agent)
            app.mount("/mcp", mcp_server.get_app())
        """
        mcp = self._build_server()
        return mcp.sse_app()

    def __repr__(self) -> str:
        tool_count = len(self._tools) + (1 if self._agent else 0)
        return f"MCPServer(name={self._name!r}, tools={tool_count})"
