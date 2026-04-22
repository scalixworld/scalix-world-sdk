"""
Scalix World SDK — Build, run, and deploy AI agents.

Usage:
    from scalix import Agent, Tool, Database

    agent = Agent(
        model="claude-sonnet-4",
        tools=[Tool.code_exec(), Tool.web_search()],
    )

    result = await agent.run("Analyze trending GitHub repos")

Connect to Scalix infrastructure:
    import scalix
    scalix.configure(api_key="sk-scalix-...")
"""

from scalix._version import __version__
from scalix.config import configure, get_config, ScalixConfig
from scalix.agent.agent import Agent
from scalix.agent.orchestrator import Team, Pipeline
from scalix.tools.base import Tool
from scalix.providers.base import Database
from scalix.client import ScalixClient
from scalix.exceptions import (
    ScalixError,
    ConfigurationError,
    AuthenticationError,
    ProviderError,
    ToolError,
)

__all__ = [
    # Version
    "__version__",
    # Configuration
    "configure",
    "get_config",
    "ScalixConfig",
    # Client
    "ScalixClient",
    # Core
    "Agent",
    "Team",
    "Pipeline",
    "Tool",
    "Database",
    # Exceptions
    "ScalixError",
    "ConfigurationError",
    "AuthenticationError",
    "ProviderError",
    "ToolError",
]
