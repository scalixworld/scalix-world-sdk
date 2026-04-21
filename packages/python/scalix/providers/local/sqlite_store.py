"""SQLite persistence provider — local database for development.

Used in local mode as a free alternative to ScalixDB.
A single file on disk — no managed Postgres needed.

Uses aiosqlite for async operations, with a fallback to stdlib sqlite3
if aiosqlite is not installed.
"""

from __future__ import annotations

import logging
import sqlite3
from typing import Any

from scalix.providers.base import DatabaseProvider

logger = logging.getLogger("scalix.providers.sqlite_store")


class SQLiteProvider(DatabaseProvider):
    """SQLite-based database for local development.

    Cost to Scalix: $0 (runs entirely on developer's machine).

    Supports both async (via aiosqlite) and sync (via stdlib sqlite3)
    execution. The sync path wraps calls in asyncio.to_thread for
    non-blocking behavior.
    """

    def __init__(self, db_path: str = "scalix_local.db") -> None:
        self.db_path = db_path
        self._aiosqlite_available: bool | None = None
        self._sync_conn: sqlite3.Connection | None = None

    def _check_aiosqlite(self) -> bool:
        """Check if aiosqlite is available."""
        if self._aiosqlite_available is None:
            try:
                import aiosqlite  # noqa: F401

                self._aiosqlite_available = True
            except ImportError:
                self._aiosqlite_available = False
                logger.debug(
                    "aiosqlite not installed — using sqlite3 with asyncio.to_thread. "
                    "Install aiosqlite for better async performance: pip install aiosqlite"
                )
        return bool(self._aiosqlite_available)

    async def query(self, sql: str, params: list[Any] | None = None) -> list[dict[str, Any]]:
        """Execute a SQL query and return results as list of dicts."""
        if self._check_aiosqlite():
            return await self._query_aiosqlite(sql, params)
        else:
            return await self._query_sync(sql, params)

    async def execute(self, sql: str, params: list[Any] | None = None) -> int:
        """Execute a SQL statement and return affected row count."""
        if self._check_aiosqlite():
            return await self._execute_aiosqlite(sql, params)
        else:
            return await self._execute_sync(sql, params)

    # --- aiosqlite path ---

    async def _query_aiosqlite(self, sql: str, params: list[Any] | None) -> list[dict[str, Any]]:
        import aiosqlite

        async with aiosqlite.connect(self.db_path) as db:
            db.row_factory = aiosqlite.Row
            async with db.execute(sql, params or []) as cursor:
                rows = await cursor.fetchall()
                if not rows:
                    return []
                columns = [desc[0] for desc in cursor.description] if cursor.description else []
                return [dict(zip(columns, row)) for row in rows]

    async def _execute_aiosqlite(self, sql: str, params: list[Any] | None) -> int:
        import aiosqlite

        async with aiosqlite.connect(self.db_path) as db:
            cursor = await db.execute(sql, params or [])
            await db.commit()
            return cursor.rowcount

    # --- stdlib sqlite3 fallback (wrapped in asyncio.to_thread) ---

    def _get_sync_conn(self) -> sqlite3.Connection:
        conn = self._sync_conn
        if conn is None:
            conn = sqlite3.connect(self.db_path)
            conn.row_factory = sqlite3.Row
            self._sync_conn = conn
        return conn

    def _query_sync_impl(self, sql: str, params: list[Any] | None) -> list[dict[str, Any]]:
        conn = self._get_sync_conn()
        cursor = conn.execute(sql, params or [])
        rows = cursor.fetchall()
        if not rows:
            return []
        columns = [desc[0] for desc in cursor.description] if cursor.description else []
        return [dict(zip(columns, row)) for row in rows]

    def _execute_sync_impl(self, sql: str, params: list[Any] | None) -> int:
        conn = self._get_sync_conn()
        cursor = conn.execute(sql, params or [])
        conn.commit()
        return cursor.rowcount

    async def _query_sync(self, sql: str, params: list[Any] | None) -> list[dict[str, Any]]:
        import asyncio

        return await asyncio.to_thread(lambda: self._query_sync_impl(sql, params))

    async def _execute_sync(self, sql: str, params: list[Any] | None) -> int:
        import asyncio

        return await asyncio.to_thread(lambda: self._execute_sync_impl(sql, params))

    async def close(self) -> None:
        """Close the database connection."""
        conn = self._sync_conn
        if conn is not None:
            conn.close()
            self._sync_conn = None

    def __del__(self) -> None:
        conn = self._sync_conn
        if conn is not None:
            conn.close()
