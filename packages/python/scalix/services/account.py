"""Account service — API key management, usage tracking, health check."""

from __future__ import annotations

from typing import Any

from scalix.services.base import BaseService


class AccountService(BaseService):

    async def health(self) -> dict[str, Any]:
        return await self._request("GET", "/health")

    # ── API Key Management ──

    async def list_api_keys(self) -> dict[str, Any]:
        return await self._request("GET", "/api/dashboard/api-keys")

    async def create_api_key(
        self,
        name: str,
        *,
        expires_at: str | None = None,
    ) -> dict[str, Any]:
        body: dict[str, Any] = {"name": name}
        if expires_at:
            body["expires_at"] = expires_at
        return await self._request("POST", "/api/dashboard/api-keys", json=body)

    async def delete_api_key(self, key_id: str) -> dict[str, Any]:
        return await self._request("DELETE", f"/api/dashboard/api-keys/{key_id}")

    # ── Usage & Billing ──

    async def usage(
        self,
        *,
        start_date: str | None = None,
        end_date: str | None = None,
    ) -> dict[str, Any]:
        params: dict[str, Any] = {}
        if start_date:
            params["start_date"] = start_date
        if end_date:
            params["end_date"] = end_date
        return await self._request("GET", "/api/billing/usage", params=params)
