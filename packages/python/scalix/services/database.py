"""ScalixDB service — managed database operations."""

from __future__ import annotations

from typing import Any

from scalix.services.base import BaseService


class DatabaseService(BaseService):
    _prefix = "/api/scalixdb"

    async def list_databases(self) -> dict[str, Any]:
        return await self._request("GET", f"{self._prefix}/databases")

    async def create_database(
        self, name: str, *, plan: str | None = None, region: str | None = None
    ) -> dict[str, Any]:
        body: dict[str, Any] = {"name": name}
        if plan:
            body["plan"] = plan
        if region:
            body["region"] = region
        return await self._request("POST", f"{self._prefix}/databases", json=body)

    async def get_database(self, db_id: str) -> dict[str, Any]:
        return await self._request("GET", f"{self._prefix}/databases/{db_id}")

    async def delete_database(self, db_id: str) -> dict[str, Any]:
        return await self._request("DELETE", f"{self._prefix}/databases/{db_id}")

    async def query(self, db_id: str, sql: str) -> dict[str, Any]:
        return await self._request(
            "POST", f"{self._prefix}/databases/{db_id}/query", json={"sql": sql}
        )

    async def explain(self, db_id: str, sql: str) -> dict[str, Any]:
        return await self._request(
            "POST", f"{self._prefix}/databases/{db_id}/explain", json={"sql": sql}
        )

    async def tables(self, db_id: str) -> dict[str, Any]:
        return await self._request("GET", f"{self._prefix}/databases/{db_id}/tables")

    async def columns(self, db_id: str, table_name: str) -> dict[str, Any]:
        return await self._request(
            "GET", f"{self._prefix}/databases/{db_id}/tables/{table_name}/columns"
        )

    async def list_backups(self, db_id: str) -> dict[str, Any]:
        return await self._request("GET", f"{self._prefix}/databases/{db_id}/backups")

    async def create_backup(self, db_id: str) -> dict[str, Any]:
        return await self._request("POST", f"{self._prefix}/databases/{db_id}/backups")

    async def restore_backup(self, db_id: str, backup_id: str) -> dict[str, Any]:
        return await self._request(
            "POST", f"{self._prefix}/databases/{db_id}/backups/{backup_id}/restore"
        )

    async def list_branches(self, db_id: str) -> dict[str, Any]:
        return await self._request("GET", f"{self._prefix}/databases/{db_id}/branches")

    async def create_branch(self, db_id: str, name: str) -> dict[str, Any]:
        return await self._request(
            "POST", f"{self._prefix}/databases/{db_id}/branches", json={"name": name}
        )

    async def metrics(self, db_id: str) -> dict[str, Any]:
        return await self._request("GET", f"{self._prefix}/databases/{db_id}/metrics")

    async def connection_string(self, db_id: str) -> dict[str, Any]:
        return await self._request("GET", f"{self._prefix}/databases/{db_id}/connection")
