"""Account service — user info, budget, usage."""

from __future__ import annotations

from typing import Any

from scalix_sdk.services.base import BaseService


class AccountService(BaseService):

    async def health(self) -> dict[str, Any]:
        return await self._request("GET", "/health")

    async def info(self) -> dict[str, Any]:
        return await self._request("GET", "/v1/user/info")

    async def budget(self) -> dict[str, Any]:
        return await self._request("GET", "/v1/user/budget")

    async def usage(self) -> dict[str, Any]:
        return await self._request("GET", "/v1/user/stats")
