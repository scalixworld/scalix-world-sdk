"""Scalix CLI — unified command-line tool for AI agent development.

Commands:
    scalix dev       — Start local development server
    scalix deploy    — Deploy agent to Scalix Cloud
    scalix logs      — Stream logs from deployed agent
    scalix init      — Initialize a new Scalix project
    scalix run       — Run an agent locally

Usage:
    pip install scalix[cli]
    scalix --help
"""

from __future__ import annotations

import sys
from typing import Any


def _lazy_import_click() -> Any:
    """Lazy import click to keep the base SDK dependency-free."""
    try:
        import click
        return click
    except ImportError:
        print(
            "Error: click package not installed.\n"
            "Run: pip install 'scalix[cli]'",
            file=sys.stderr,
        )
        sys.exit(1)


def main() -> None:
    """Entry point for the `scalix` CLI."""
    click = _lazy_import_click()

    @click.group()
    @click.version_option(package_name="scalix")
    def cli() -> None:
        """Scalix — Build, run, and deploy AI agents."""

    @cli.command()
    @click.option("--host", default="0.0.0.0", help="Bind address.")
    @click.option("--port", "-p", default=4000, type=int, help="Port number.")
    @click.option("--reload", is_flag=True, help="Auto-reload on file changes.")
    @click.argument("entry", default="agent.py")
    def dev(host: str, port: int, reload: bool, entry: str) -> None:
        """Start local development server.

        Loads the agent from ENTRY (default: agent.py) and serves it
        with MCP and A2A protocol endpoints for local testing.
        """
        import importlib.util
        import os

        entry_path = os.path.abspath(entry)
        if not os.path.exists(entry_path):
            click.echo(f"Error: {entry} not found.", err=True)
            sys.exit(1)

        click.echo(f"Starting Scalix dev server...")
        click.echo(f"  Entry: {entry_path}")
        click.echo(f"  Server: http://{host}:{port}")
        click.echo(f"  MCP: http://{host}:{port}/mcp")
        click.echo(f"  A2A: http://{host}:{port}/.well-known/agent.json")
        click.echo()

        # Load the agent module
        spec = importlib.util.spec_from_file_location("agent_module", entry_path)
        if spec is None or spec.loader is None:
            click.echo(f"Error: Cannot load {entry}", err=True)
            sys.exit(1)

        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)

        # Find the agent instance
        from scalix.agent.agent import Agent

        agent = None
        for attr_name in dir(module):
            obj = getattr(module, attr_name)
            if isinstance(obj, Agent):
                agent = obj
                break

        if agent is None:
            click.echo(
                "Error: No Agent instance found in the module.\n"
                "Define an agent: agent = Agent(model='claude-sonnet-4')",
                err=True,
            )
            sys.exit(1)

        # Start dev server with both MCP and A2A endpoints
        try:
            from aiohttp import web
        except ImportError:
            click.echo(
                "Error: aiohttp not installed.\n"
                "Run: pip install 'scalix[cli]'",
                err=True,
            )
            sys.exit(1)

        import asyncio
        import json

        from scalix.protocols.mcp_server import MCPServer
        from scalix.protocols.a2a_server import A2AServer

        mcp_server = MCPServer(agent=agent, tools=agent.tools or [])
        a2a_server = A2AServer(agent=agent)

        app = web.Application()

        # A2A endpoints
        async def agent_card_handler(request: Any) -> Any:
            base_url = f"{request.scheme}://{request.host}"
            card = a2a_server.get_agent_card(base_url=base_url)
            return web.json_response(card)

        async def a2a_handler(request: Any) -> Any:
            body = await request.json()
            response = await a2a_server.handle_jsonrpc(body)
            return web.json_response(response)

        # Health check
        async def health_handler(request: Any) -> Any:
            return web.json_response({
                "status": "ok",
                "agent": repr(agent),
                "mode": "development",
            })

        app.router.add_get("/.well-known/agent.json", agent_card_handler)
        app.router.add_post("/a2a", a2a_handler)
        app.router.add_get("/health", health_handler)

        click.echo(f"Agent loaded: {agent}")
        click.echo("Press Ctrl+C to stop.\n")
        web.run_app(app, host=host, port=port, print=lambda _: None)

    @cli.command()
    @click.argument("entry", default="agent.py")
    @click.option("--name", "-n", help="Deployment name (default: from agent).")
    @click.option("--env", "-e", default="production", help="Target environment.")
    @click.option("--region", "-r", default="us-east-1", help="Deployment region.")
    def deploy(entry: str, name: str | None, env: str, region: str) -> None:
        """Deploy an agent to Scalix Cloud.

        Packages the agent and deploys it to Scalix Hosting.
        Requires a Scalix API key: scalix.configure(api_key='...')
        """
        import os

        from scalix.config import get_config

        config = get_config()
        if not config.is_cloud_mode:
            click.echo(
                "Error: No API key configured.\n"
                "Set SCALIX_API_KEY or run: scalix.configure(api_key='...')",
                err=True,
            )
            sys.exit(1)

        entry_path = os.path.abspath(entry)
        if not os.path.exists(entry_path):
            click.echo(f"Error: {entry} not found.", err=True)
            sys.exit(1)

        deploy_name = name or os.path.splitext(os.path.basename(entry))[0]

        click.echo(f"Deploying '{deploy_name}' to Scalix Cloud...")
        click.echo(f"  Entry: {entry_path}")
        click.echo(f"  Environment: {env}")
        click.echo(f"  Region: {region}")
        click.echo()

        import asyncio
        import httpx

        async def _deploy() -> dict[str, Any]:
            async with httpx.AsyncClient(
                base_url=config.base_url,
                headers={
                    "Authorization": f"Bearer {config.api_key}",
                    "Content-Type": "application/json",
                },
                timeout=120.0,
            ) as client:
                # Read the entry file
                with open(entry_path) as f:
                    source_code = f.read()

                resp = await client.post(
                    "/api/hosting/deploy",
                    json={
                        "name": deploy_name,
                        "source": source_code,
                        "runtime": "python3.12",
                        "environment": env,
                        "region": region,
                    },
                )

                if resp.status_code != 200:
                    click.echo(f"Deploy failed: {resp.status_code} {resp.text}", err=True)
                    sys.exit(1)

                return resp.json()

        result = asyncio.run(_deploy())
        url = result.get("url", result.get("endpoint", ""))
        deploy_id = result.get("id", result.get("deployment_id", ""))

        click.echo(f"Deployed successfully!")
        click.echo(f"  ID: {deploy_id}")
        click.echo(f"  URL: {url}")
        click.echo(f"  A2A: {url}/.well-known/agent.json")

    @cli.command()
    @click.argument("deployment", required=False)
    @click.option("--follow", "-f", is_flag=True, help="Follow log output.")
    @click.option("--tail", "-n", default=100, type=int, help="Number of lines to show.")
    def logs(deployment: str | None, follow: bool, tail: int) -> None:
        """Stream logs from a deployed agent.

        If DEPLOYMENT is not specified, shows logs from the most recent deployment.
        """
        from scalix.config import get_config

        config = get_config()
        if not config.is_cloud_mode:
            click.echo("Error: No API key configured.", err=True)
            sys.exit(1)

        import asyncio
        import httpx

        async def _stream_logs() -> None:
            async with httpx.AsyncClient(
                base_url=config.base_url,
                headers={
                    "Authorization": f"Bearer {config.api_key}",
                    "Content-Type": "application/json",
                },
                timeout=None,
            ) as client:
                params: dict[str, Any] = {"tail": tail}
                if deployment:
                    params["deployment_id"] = deployment

                endpoint = "/api/hosting/logs"
                if follow:
                    # Use streaming for follow mode
                    async with client.stream("GET", endpoint, params=params) as resp:
                        if resp.status_code != 200:
                            click.echo(f"Failed to get logs: {resp.status_code}", err=True)
                            return
                        async for line in resp.aiter_lines():
                            click.echo(line)
                else:
                    resp = await client.get(endpoint, params=params)
                    if resp.status_code != 200:
                        click.echo(f"Failed to get logs: {resp.status_code}", err=True)
                        return
                    data = resp.json()
                    for log_line in data.get("logs", data.get("lines", [])):
                        if isinstance(log_line, dict):
                            ts = log_line.get("timestamp", "")
                            msg = log_line.get("message", "")
                            click.echo(f"{ts}  {msg}")
                        else:
                            click.echo(str(log_line))

        asyncio.run(_stream_logs())

    @cli.command()
    @click.argument("prompt")
    @click.option("--entry", "-e", default="agent.py", help="Agent entry file.")
    def run(prompt: str, entry: str) -> None:
        """Run an agent locally with a prompt.

        Example:
            scalix run "What's the weather in SF?" -e my_agent.py
        """
        import importlib.util
        import os

        entry_path = os.path.abspath(entry)
        if not os.path.exists(entry_path):
            click.echo(f"Error: {entry} not found.", err=True)
            sys.exit(1)

        spec = importlib.util.spec_from_file_location("agent_module", entry_path)
        if spec is None or spec.loader is None:
            click.echo(f"Error: Cannot load {entry}", err=True)
            sys.exit(1)

        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)

        from scalix.agent.agent import Agent

        agent = None
        for attr_name in dir(module):
            obj = getattr(module, attr_name)
            if isinstance(obj, Agent):
                agent = obj
                break

        if agent is None:
            click.echo("Error: No Agent instance found.", err=True)
            sys.exit(1)

        import asyncio

        result = asyncio.run(agent.run(prompt))
        click.echo(result.output)

    @cli.command()
    @click.argument("name", default="my-agent")
    def init(name: str) -> None:
        """Initialize a new Scalix agent project.

        Creates a project directory with a starter agent.py file.
        """
        import os

        project_dir = os.path.join(os.getcwd(), name)

        if os.path.exists(project_dir):
            click.echo(f"Error: Directory '{name}' already exists.", err=True)
            sys.exit(1)

        os.makedirs(project_dir)

        # Create starter agent.py
        agent_code = '''"""My Scalix Agent."""

from scalix import Agent, Tool

agent = Agent(
    model="auto",
    instructions="You are a helpful AI assistant.",
    tools=[
        Tool.code_exec(),
        Tool.web_search(),
    ],
)

if __name__ == "__main__":
    import asyncio

    result = asyncio.run(agent.run("Hello! What can you help me with?"))
    print(result.output)
'''

        with open(os.path.join(project_dir, "agent.py"), "w") as f:
            f.write(agent_code)

        # Create requirements.txt
        with open(os.path.join(project_dir, "requirements.txt"), "w") as f:
            f.write("scalix>=0.1.0\n")

        # Create .env.example
        with open(os.path.join(project_dir, ".env.example"), "w") as f:
            f.write(
                "# Scalix Cloud (optional — enables Sandbox, Router, ScalixDB)\n"
                "# SCALIX_API_KEY=sk-scalix-...\n\n"
                "# LLM Provider (at least one required for local mode)\n"
                "# ANTHROPIC_API_KEY=sk-ant-...\n"
                "# OPENAI_API_KEY=sk-...\n"
                "# GOOGLE_API_KEY=...\n"
            )

        click.echo(f"Created Scalix project: {name}/")
        click.echo(f"  agent.py           — Your agent definition")
        click.echo(f"  requirements.txt   — Python dependencies")
        click.echo(f"  .env.example       — Environment variables")
        click.echo()
        click.echo("Get started:")
        click.echo(f"  cd {name}")
        click.echo(f"  pip install -r requirements.txt")
        click.echo(f"  scalix run 'Hello!' -e agent.py")

    cli()


if __name__ == "__main__":
    main()
