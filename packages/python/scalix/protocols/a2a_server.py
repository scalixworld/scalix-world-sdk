"""A2A (Agent-to-Agent Protocol) server — expose Scalix agents to other agents.

Implements Google's A2A protocol, allowing external agents built on any
framework (LangChain, CrewAI, OpenAI, etc.) to discover and collaborate
with Scalix agents.

Endpoints:
    GET  /.well-known/agent.json  — Agent Card (discovery)
    POST /                        — JSON-RPC 2.0 message handling

Usage:
    from scalix import Agent, Tool
    from scalix.protocols import A2AServer

    agent = Agent(model="claude-sonnet-4", tools=[Tool.code_exec()])
    a2a = A2AServer(agent=agent)
    a2a.start(port=5000)
"""

from __future__ import annotations

import asyncio
import json
import logging
import uuid
from typing import Any, TYPE_CHECKING

if TYPE_CHECKING:
    from scalix.agent.agent import Agent

logger = logging.getLogger("scalix.protocols.a2a")


class A2AServer:
    """Expose a Scalix agent via the A2A protocol.

    Implements the core A2A specification:
    - Agent Card at /.well-known/agent.json for discovery
    - JSON-RPC 2.0 request handling for message/send
    - Task lifecycle management (working → completed/failed)

    Args:
        agent: The Scalix Agent to expose.
        name: Agent name for the Agent Card.
        description: Agent description for discovery.
        version: Agent version string.
        skills: List of skill descriptors. Auto-generated from agent if omitted.
    """

    def __init__(
        self,
        agent: Agent,
        name: str | None = None,
        description: str | None = None,
        version: str = "1.0.0",
        skills: list[dict[str, Any]] | None = None,
    ) -> None:
        self._agent = agent
        self._name = name or "scalix-agent"
        self._description = description or agent.instructions or "A Scalix AI agent"
        self._version = version
        self._skills = skills or self._auto_skills()
        self._tasks: dict[str, dict[str, Any]] = {}

    def _auto_skills(self) -> list[dict[str, Any]]:
        """Auto-generate skill descriptors from the agent's tools."""
        skills = []
        if self._agent.instructions:
            skills.append({
                "id": "general",
                "name": "General Assistant",
                "description": self._agent.instructions[:200],
            })
        for tool in (self._agent.tools or []):
            skills.append({
                "id": tool.name,
                "name": tool.name,
                "description": tool.description,
            })
        return skills or [{"id": "default", "name": "Agent", "description": self._description}]

    def get_agent_card(self, base_url: str = "http://localhost:5000") -> dict[str, Any]:
        """Build the A2A Agent Card for discovery.

        Returns:
            Agent Card as a dictionary, served at /.well-known/agent.json.
        """
        return {
            "name": self._name,
            "description": self._description,
            "url": base_url,
            "version": self._version,
            "capabilities": {
                "streaming": False,
                "pushNotifications": False,
            },
            "defaultInputModes": ["text/plain"],
            "defaultOutputModes": ["text/plain"],
            "skills": self._skills,
        }

    async def handle_jsonrpc(self, request: dict[str, Any]) -> dict[str, Any]:
        """Handle an incoming JSON-RPC 2.0 request.

        Supports:
            message/send — Send a message to the agent and get a response.
            tasks/get    — Get the current state of a task.
            tasks/cancel — Cancel a running task.

        Args:
            request: JSON-RPC 2.0 request body.

        Returns:
            JSON-RPC 2.0 response.
        """
        method = request.get("method", "")
        params = request.get("params", {})
        rpc_id = request.get("id", 1)

        try:
            if method == "message/send":
                result = await self._handle_message_send(params)
            elif method == "tasks/get":
                result = self._handle_tasks_get(params)
            elif method == "tasks/cancel":
                result = self._handle_tasks_cancel(params)
            else:
                return {
                    "jsonrpc": "2.0",
                    "id": rpc_id,
                    "error": {
                        "code": -32601,
                        "message": f"Method not found: {method}",
                    },
                }

            return {
                "jsonrpc": "2.0",
                "id": rpc_id,
                "result": result,
            }

        except Exception as e:
            logger.exception("A2A request failed: %s", method)
            return {
                "jsonrpc": "2.0",
                "id": rpc_id,
                "error": {
                    "code": -32000,
                    "message": str(e),
                },
            }

    async def _handle_message_send(self, params: dict[str, Any]) -> dict[str, Any]:
        """Handle message/send — run the agent and return the result."""
        message = params.get("message", {})
        parts = message.get("parts", [])

        # Extract text content from parts
        prompt_parts = []
        for part in parts:
            if isinstance(part, dict) and part.get("type") == "text":
                prompt_parts.append(part.get("text", ""))
            elif isinstance(part, str):
                prompt_parts.append(part)

        prompt = "\n".join(prompt_parts) or str(message.get("content", ""))

        # Generate task ID
        task_id = str(uuid.uuid4())
        context_id = params.get("contextId", str(uuid.uuid4()))

        # Track the task
        self._tasks[task_id] = {
            "id": task_id,
            "contextId": context_id,
            "status": {"state": "working"},
        }

        try:
            # Run the agent
            result = await self._agent.run(prompt)

            # Build A2A response
            artifacts = [
                {
                    "parts": [{"type": "text", "text": result.output}],
                }
            ]

            self._tasks[task_id]["status"] = {"state": "completed"}
            self._tasks[task_id]["artifacts"] = artifacts

            return {
                "id": task_id,
                "contextId": context_id,
                "status": {"state": "completed"},
                "artifacts": artifacts,
            }

        except Exception as e:
            self._tasks[task_id]["status"] = {
                "state": "failed",
                "message": str(e),
            }
            raise

    def _handle_tasks_get(self, params: dict[str, Any]) -> dict[str, Any]:
        """Handle tasks/get — return current task state."""
        task_id = params.get("id", "")
        task = self._tasks.get(task_id)
        if not task:
            raise ValueError(f"Task not found: {task_id}")
        return task

    def _handle_tasks_cancel(self, params: dict[str, Any]) -> dict[str, Any]:
        """Handle tasks/cancel — cancel a running task."""
        task_id = params.get("id", "")
        task = self._tasks.get(task_id)
        if not task:
            raise ValueError(f"Task not found: {task_id}")
        task["status"] = {"state": "canceled"}
        return task

    def start(self, host: str = "0.0.0.0", port: int = 5000) -> None:
        """Start the A2A server using aiohttp or a simple HTTP server.

        Args:
            host: Bind address.
            port: Port number.
        """
        try:
            from aiohttp import web
        except ImportError:
            raise ImportError(
                "aiohttp package not installed. Run: pip install aiohttp"
            )

        app = web.Application()
        base_url = f"http://{host}:{port}"

        async def agent_card_handler(request: Any) -> Any:
            card = self.get_agent_card(base_url=base_url)
            return web.json_response(card)

        async def jsonrpc_handler(request: Any) -> Any:
            body = await request.json()
            response = await self.handle_jsonrpc(body)
            return web.json_response(response)

        app.router.add_get("/.well-known/agent.json", agent_card_handler)
        app.router.add_post("/", jsonrpc_handler)

        logger.info("Starting A2A server at %s:%d", host, port)
        web.run_app(app, host=host, port=port)

    def get_app(self) -> Any:
        """Get the ASGI/WSGI app for mounting on an existing server.

        Returns an aiohttp Application for advanced deployment scenarios.
        """
        try:
            from aiohttp import web
        except ImportError:
            raise ImportError(
                "aiohttp package not installed. Run: pip install aiohttp"
            )

        app = web.Application()

        async def agent_card_handler(request: Any) -> Any:
            base_url = f"{request.scheme}://{request.host}"
            card = self.get_agent_card(base_url=base_url)
            return web.json_response(card)

        async def jsonrpc_handler(request: Any) -> Any:
            body = await request.json()
            response = await self.handle_jsonrpc(body)
            return web.json_response(response)

        app.router.add_get("/.well-known/agent.json", agent_card_handler)
        app.router.add_post("/", jsonrpc_handler)
        return app

    def __repr__(self) -> str:
        return (
            f"A2AServer(name={self._name!r}, "
            f"skills={len(self._skills)})"
        )
