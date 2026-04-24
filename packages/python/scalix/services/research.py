"""Research and web search service."""

from __future__ import annotations

from typing import Any

from scalix.services.base import BaseService


class ResearchService(BaseService):
    async def search(
        self, query: str, *, max_results: int | None = None
    ) -> dict[str, Any]:
        params: dict[str, Any] = {"query": query}
        if max_results:
            params["max_results"] = max_results
        return await self._request("POST", "/v1/research/search", params=params)

    async def research(self, query: str) -> dict[str, Any]:
        return await self._request("POST", "/v1/research", json={"query": query})

    async def deep(self, query: str) -> dict[str, Any]:
        return await self._request("POST", "/v1/research/deep", json={"query": query})
