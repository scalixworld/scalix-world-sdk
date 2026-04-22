"""Document generation service."""

from __future__ import annotations

from typing import Any

from scalix.services.base import BaseService


class DocGenService(BaseService):
    async def create(
        self,
        prompt: str,
        *,
        format: str | None = None,
        template: str | None = None,
    ) -> dict[str, Any]:
        body: dict[str, Any] = {"prompt": prompt}
        if format:
            body["format"] = format
        if template:
            body["template"] = template
        return await self._request("POST", "/v1/docgen/create", json=body)

    async def preview(self, prompt: str, **kwargs: Any) -> dict[str, Any]:
        return await self._request("POST", "/v1/docgen/preview", json={"prompt": prompt, **kwargs})

    async def formats(self) -> dict[str, Any]:
        return await self._request("GET", "/v1/docgen/formats")

    async def templates(self) -> dict[str, Any]:
        return await self._request("GET", "/v1/docgen/templates")

    async def download(self, doc_id: str) -> dict[str, Any]:
        return await self._request("GET", f"/v1/docgen/download/{doc_id}")

    async def revise(self, doc_id: str, instructions: str) -> dict[str, Any]:
        return await self._request(
            "POST", "/v1/docgen/revise", json={"doc_id": doc_id, "instructions": instructions}
        )

    async def history(self) -> dict[str, Any]:
        return await self._request("GET", "/v1/docgen/history")
