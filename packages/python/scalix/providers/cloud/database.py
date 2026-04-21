"""ScalixDB provider — managed Postgres via Scalix Cloud API.

Provides managed PostgreSQL with branching, HA, PITR, and auto-scaling.
Calls the existing Cloud API endpoints for database operations.

Uses httpx for async HTTP requests to the ScalixDB API.
"""

from __future__ import annotations

import logging
from typing import Any

from scalix.config import ScalixConfig, get_config
from scalix.exceptions import AuthenticationError, DatabaseError
from scalix.providers.base import DatabaseProvider

logger = logging.getLogger("scalix.providers.cloud.database")


class ScalixDatabaseProvider(DatabaseProvider):
    """Query ScalixDB managed Postgres instances.

    Calls the ScalixDB Cloud API at /api/scalixdb/databases/:id/query.
    Requires a Scalix API key (cloud mode).

    Advantages over SQLiteProvider:
    - Managed PostgreSQL (not SQLite)
    - Branching (create dev copies of production data)
    - High availability with automatic failover
    - Point-in-time recovery
    - Auto-scaling
    - Backups and monitoring
    """

    def __init__(self, database_name: str, config: ScalixConfig | None = None) -> None:
        self.database_name = database_name
        self._config = config or get_config()
        if not self._config.is_cloud_mode:
            raise AuthenticationError(
                "ScalixDB requires an API key. "
                "Call scalix.configure(api_key='...') first."
            )
        self._database_id: str | None = None
        self._client: Any = None

    async def _get_client(self) -> Any:
        """Get or create the httpx async client."""
        if self._client is None:
            try:
                import httpx
            except ImportError:
                raise DatabaseError(
                    "httpx package not installed. "
                    "Run: pip install scalix[cloud]"
                )

            self._client = httpx.AsyncClient(
                base_url=self._config.base_url,
                headers={
                    "Authorization": f"Bearer {self._config.api_key}",
                    "Content-Type": "application/json",
                },
                timeout=30.0,
            )
        return self._client

    async def _resolve_database_id(self) -> str:
        """Resolve database name to database ID via API."""
        if self._database_id is not None:
            return self._database_id

        client = await self._get_client()

        # List databases and find by name
        resp = await client.get("/api/scalixdb/databases")

        if resp.status_code == 401:
            raise AuthenticationError("Invalid API key for ScalixDB")
        if resp.status_code != 200:
            raise DatabaseError(
                f"Failed to list databases: {resp.status_code} {resp.text}"
            )

        data = resp.json()
        databases = data.get("databases", data.get("data", []))

        for db in databases:
            name = db.get("name", db.get("database_name", ""))
            if name == self.database_name:
                self._database_id = db.get("id", db.get("database_id", ""))
                return self._database_id

        raise DatabaseError(
            f"Database '{self.database_name}' not found. "
            f"Create it in the Scalix dashboard or via the API."
        )

    async def query(self, sql: str, params: list[Any] | None = None) -> list[dict[str, Any]]:
        """Execute a SQL query against ScalixDB and return results.

        Args:
            sql: SQL query string.
            params: Optional query parameters for parameterized queries.

        Returns:
            List of result rows as dictionaries.
        """
        client = await self._get_client()
        db_id = await self._resolve_database_id()

        body: dict[str, Any] = {"query": sql}
        if params:
            body["params"] = params

        logger.debug("ScalixDB query: database=%s, sql=%s", self.database_name, sql[:100])
        resp = await client.post(f"/api/scalixdb/databases/{db_id}/query", json=body)

        if resp.status_code == 401:
            raise AuthenticationError("Invalid API key for ScalixDB")
        if resp.status_code == 403:
            raise DatabaseError(
                f"Access denied to database '{self.database_name}'"
            )
        if resp.status_code == 404:
            raise DatabaseError(
                f"Database '{self.database_name}' not found"
            )
        if resp.status_code != 200:
            error_msg = resp.text
            try:
                error_data = resp.json()
                error_msg = error_data.get("error", {}).get("message", error_msg)
            except Exception:
                pass
            raise DatabaseError(f"Query failed: {error_msg}")

        data = resp.json()

        # The API returns rows in various formats — normalize to list of dicts
        rows = data.get("rows", data.get("results", data.get("data", [])))
        columns = data.get("columns", data.get("fields", []))

        if rows and columns and isinstance(rows[0], list):
            # Rows are arrays, columns are separate — zip them
            col_names = [c.get("name", c) if isinstance(c, dict) else c for c in columns]
            return [dict(zip(col_names, row)) for row in rows]
        elif rows and isinstance(rows[0], dict):
            # Already dict format
            return rows
        else:
            return rows if rows else []

    async def execute(self, sql: str, params: list[Any] | None = None) -> int:
        """Execute a SQL statement against ScalixDB and return affected row count.

        Args:
            sql: SQL statement (INSERT, UPDATE, DELETE, CREATE, etc.).
            params: Optional query parameters.

        Returns:
            Number of affected rows.
        """
        client = await self._get_client()
        db_id = await self._resolve_database_id()

        body: dict[str, Any] = {"query": sql}
        if params:
            body["params"] = params

        logger.debug("ScalixDB execute: database=%s, sql=%s", self.database_name, sql[:100])
        resp = await client.post(f"/api/scalixdb/databases/{db_id}/query", json=body)

        if resp.status_code == 401:
            raise AuthenticationError("Invalid API key for ScalixDB")
        if resp.status_code == 403:
            raise DatabaseError(
                f"Access denied to database '{self.database_name}'"
            )
        if resp.status_code != 200:
            error_msg = resp.text
            try:
                error_data = resp.json()
                error_msg = error_data.get("error", {}).get("message", error_msg)
            except Exception:
                pass
            raise DatabaseError(f"Execute failed: {error_msg}")

        data = resp.json()
        return data.get("rows_affected", data.get("rowCount", 0))

    async def close(self) -> None:
        """Close the HTTP client."""
        if self._client is not None:
            await self._client.aclose()
            self._client = None
