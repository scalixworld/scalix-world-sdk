"""Tool base class and built-in tool factories."""

from __future__ import annotations

from typing import Any, Callable

from scalix.types import ToolDefinition, ToolCallResult


class Tool:
    """Base class for all agent tools.

    Tools give agents the ability to execute code, query databases,
    search the web, and interact with external services.

    Use the static factory methods to create built-in tools:
        Tool.code_exec()    — Execute code in a sandbox
        Tool.sql()          — Query a database
        Tool.web_search()   — Search the web
        Tool.http()         — Make HTTP requests
        Tool.mcp()          — Import tools from an MCP server
        Tool.function()     — Wrap a Python function as a tool
    """

    def __init__(
        self,
        name: str,
        description: str,
        parameters: dict[str, Any] | None = None,
        execute_fn: Callable[..., Any] | None = None,
    ) -> None:
        self.name = name
        self.description = description
        self.parameters = parameters or {}
        self._execute_fn = execute_fn

    @property
    def definition(self) -> ToolDefinition:
        """Get the JSON Schema definition for this tool."""
        return ToolDefinition(
            name=self.name,
            description=self.description,
            parameters=self.parameters,
        )

    @property
    def has_execute_fn(self) -> bool:
        """Whether this tool has a custom execute function registered."""
        return self._execute_fn is not None

    async def execute(self, **params: Any) -> ToolCallResult:
        """Execute this tool with the given parameters."""
        if self._execute_fn is None:
            raise NotImplementedError(f"Tool '{self.name}' has no execute function")

        result = self._execute_fn(**params)
        if hasattr(result, "__await__"):
            result = await result

        return ToolCallResult(
            tool_name=self.name,
            arguments=params,
            result=result,
        )

    # --- Built-in Tool Factories ---

    @staticmethod
    def code_exec(
        runtime: str = "python",
        gpu: str | None = None,
        timeout: int = 30,
    ) -> Tool:
        """Create a code execution tool.

        In local mode: runs code in Docker or subprocess.
        In cloud mode: runs code in Scalix Sandbox (Firecracker + GPU).

        Args:
            runtime: Programming language runtime ("python", "node", "go", "rust").
            gpu: GPU type for cloud mode (None, "t4", "a100", "h100").
            timeout: Maximum execution time in seconds.
        """
        return Tool(
            name="code_exec",
            description=f"Execute {runtime} code in a secure sandbox environment.",
            parameters={
                "type": "object",
                "properties": {
                    "code": {
                        "type": "string",
                        "description": f"The {runtime} code to execute.",
                    },
                },
                "required": ["code"],
            },
        )

    @staticmethod
    def sql(database: str = "local") -> Tool:
        """Create a SQL query tool.

        In local mode: queries a local SQLite database.
        In cloud mode: queries a ScalixDB instance.

        Args:
            database: Database identifier. "local" for SQLite, or a ScalixDB name.
        """
        return Tool(
            name="sql",
            description="Execute a SQL query against the database.",
            parameters={
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "The SQL query to execute.",
                    },
                },
                "required": ["query"],
            },
        )

    @staticmethod
    def web_search(provider: str = "auto") -> Tool:
        """Create a web search tool.

        Args:
            provider: Search provider ("auto", "google", "bing", "duckduckgo").
        """
        return Tool(
            name="web_search",
            description="Search the web for information.",
            parameters={
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "The search query.",
                    },
                },
                "required": ["query"],
            },
        )

    @staticmethod
    def http(base_url: str | None = None) -> Tool:
        """Create an HTTP request tool.

        Args:
            base_url: Optional base URL for all requests.
        """
        return Tool(
            name="http",
            description="Make HTTP requests to external APIs.",
            parameters={
                "type": "object",
                "properties": {
                    "url": {"type": "string", "description": "The URL to request."},
                    "method": {
                        "type": "string",
                        "enum": ["GET", "POST", "PUT", "DELETE", "PATCH"],
                        "description": "HTTP method.",
                        "default": "GET",
                    },
                    "body": {"type": "object", "description": "Request body (for POST/PUT)."},
                },
                "required": ["url"],
            },
        )

    @staticmethod
    def mcp(server_url: str) -> list[Tool]:
        """Import tools from an MCP (Model Context Protocol) server.

        Connects to the MCP server, discovers available tools, and wraps
        each as a Scalix Tool with an execute function that calls the
        remote MCP tool.

        Args:
            server_url: URL of the MCP server (SSE endpoint).
                Example: "http://localhost:3000/sse"

        Returns:
            List of tools exposed by the MCP server.
        """
        import asyncio

        async def _discover() -> list[Tool]:
            return await Tool._mcp_discover(server_url)

        try:
            loop = asyncio.get_running_loop()
        except RuntimeError:
            loop = None

        if loop and loop.is_running():
            import concurrent.futures
            with concurrent.futures.ThreadPoolExecutor(max_workers=1) as pool:
                future = pool.submit(asyncio.run, _discover())
                return future.result()
        else:
            return asyncio.run(_discover())

    @staticmethod
    async def _mcp_discover(server_url: str) -> list[Tool]:
        """Async implementation of MCP tool discovery."""
        try:
            from mcp import ClientSession
            from mcp.client.sse import sse_client
        except ImportError:
            raise ImportError(
                "MCP package not installed. Run: pip install 'scalix[mcp]' "
                "or pip install mcp"
            )

        from contextlib import AsyncExitStack

        exit_stack = AsyncExitStack()
        tools: list[Tool] = []

        try:
            transport = await exit_stack.enter_async_context(
                sse_client(server_url)
            )
            read, write = transport
            session = await exit_stack.enter_async_context(
                ClientSession(read, write)
            )
            await session.initialize()

            response = await session.list_tools()

            for mcp_tool in response.tools:
                input_schema: dict[str, Any] = {}
                if hasattr(mcp_tool, "inputSchema") and mcp_tool.inputSchema:
                    input_schema = dict(mcp_tool.inputSchema)
                elif hasattr(mcp_tool, "input_schema") and mcp_tool.input_schema:
                    input_schema = dict(mcp_tool.input_schema)

                tool_name = mcp_tool.name

                async def _execute(
                    _server_url: str = server_url,
                    _tool_name: str = tool_name,
                    **kwargs: Any,
                ) -> Any:
                    async with AsyncExitStack() as stack:
                        t = await stack.enter_async_context(
                            sse_client(_server_url)
                        )
                        r, w = t
                        s = await stack.enter_async_context(
                            ClientSession(r, w)
                        )
                        await s.initialize()
                        result = await s.call_tool(_tool_name, kwargs)
                        if hasattr(result, "content") and result.content:
                            texts = []
                            for part in result.content:
                                if hasattr(part, "text"):
                                    texts.append(part.text)
                            return "\n".join(texts) if texts else str(result)
                        return str(result)

                tools.append(
                    Tool(
                        name=mcp_tool.name,
                        description=mcp_tool.description or f"MCP tool: {mcp_tool.name}",
                        parameters=input_schema,
                        execute_fn=_execute,
                    )
                )
        finally:
            await exit_stack.aclose()

        return tools

    @staticmethod
    def function(fn: Callable[..., Any]) -> Tool:
        """Wrap a Python function as an agent tool.

        The function's name, docstring, and type hints are used to
        generate the tool definition automatically.

        Args:
            fn: The function to wrap.

        Example:
            @Tool.function
            async def get_weather(city: str) -> str:
                \"\"\"Get the current weather for a city.\"\"\"
                ...
        """
        import inspect

        name = fn.__name__
        description = inspect.getdoc(fn) or f"Execute {name}"

        # Build parameters from type hints
        sig = inspect.signature(fn)
        properties: dict[str, Any] = {}
        required: list[str] = []

        for param_name, param in sig.parameters.items():
            param_type = "string"
            if param.annotation is int:
                param_type = "integer"
            elif param.annotation is float:
                param_type = "number"
            elif param.annotation is bool:
                param_type = "boolean"

            properties[param_name] = {"type": param_type}
            if param.default is inspect.Parameter.empty:
                required.append(param_name)

        parameters = {
            "type": "object",
            "properties": properties,
            "required": required,
        }

        return Tool(
            name=name,
            description=description,
            parameters=parameters,
            execute_fn=fn,
        )

    def __repr__(self) -> str:
        return f"Tool(name={self.name!r})"
