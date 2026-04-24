"""Abstract provider interfaces and Database convenience class."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any, AsyncIterator

from scalix.types import AgentResult, Message, SandboxResult, StreamEvent


class LLMProvider(ABC):
    """Abstract interface for LLM providers."""

    @abstractmethod
    async def chat(
        self,
        messages: list[Message],
        model: str,
        tools: list[dict[str, Any]] | None = None,
        temperature: float = 0.7,
        stream: bool = False,
        **kwargs: Any,
    ) -> Message:
        """Send a chat completion request."""
        ...

    @abstractmethod
    async def stream_chat(
        self,
        messages: list[Message],
        model: str,
        tools: list[dict[str, Any]] | None = None,
        temperature: float = 0.7,
        **kwargs: Any,
    ) -> AsyncIterator[StreamEvent]:
        """Stream a chat completion response."""
        ...


class SandboxProvider(ABC):
    """Abstract interface for code execution providers."""

    @abstractmethod
    async def execute(
        self,
        code: str,
        runtime: str = "python",
        timeout: int = 30,
        gpu: str | None = None,
    ) -> SandboxResult:
        """Execute code in a sandbox environment."""
        ...


class DatabaseProvider(ABC):
    """Abstract interface for database providers."""

    @abstractmethod
    async def query(self, sql: str, params: list[Any] | None = None) -> list[dict[str, Any]]:
        """Execute a SQL query and return results."""
        ...

    @abstractmethod
    async def execute(self, sql: str, params: list[Any] | None = None) -> int:
        """Execute a SQL statement and return affected row count."""
        ...


class Database:
    """Convenience class for database access.

    In local mode (no name): uses SQLite.
    In cloud mode (with name): uses ScalixDB.

    Args:
        name: ScalixDB instance name. None for local SQLite.

    Example:
        # Local SQLite
        db = Database()

        # ScalixDB managed instance
        db = Database("my-scalixdb")

        results = await db.query("SELECT * FROM users")
    """

    def __init__(self, name: str | None = None) -> None:
        self.name = name
        self._provider: DatabaseProvider | None = None

    async def _get_provider(self) -> DatabaseProvider:
        """Lazily initialize the database provider."""
        if self._provider is None:
            from scalix.config import get_config

            config = get_config()

            if self.name and config.is_cloud_mode:
                from scalix.providers.cloud.database import ScalixDatabaseProvider

                self._provider = ScalixDatabaseProvider(self.name, config)
            else:
                from scalix.providers.local.sqlite_store import SQLiteProvider

                self._provider = SQLiteProvider(self.name or "scalix_local.db")

        return self._provider

    async def query(self, sql: str, params: list[Any] | None = None) -> list[dict[str, Any]]:
        """Execute a SQL query and return results."""
        provider = await self._get_provider()
        return await provider.query(sql, params)

    async def execute(self, sql: str, params: list[Any] | None = None) -> int:
        """Execute a SQL statement and return affected row count."""
        provider = await self._get_provider()
        return await provider.execute(sql, params)

    def __repr__(self) -> str:
        mode = "cloud" if self.name else "local"
        name = self.name or "sqlite"
        return f"Database(name={name!r}, mode={mode!r})"
