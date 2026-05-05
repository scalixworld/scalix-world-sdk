"""Document generation service."""

from __future__ import annotations

from typing import Any

from scalix_sdk.services.base import BaseService


class DocGenService(BaseService):
    async def create(
        self,
        prompt: str,
        format: str = "pdf",
        *,
        template_id: str | None = None,
        style: str | None = None,
        language: str | None = None,
    ) -> dict[str, Any]:
        body: dict[str, Any] = {"prompt": prompt, "format": format}
        if template_id:
            body["template_id"] = template_id
        if style:
            body["style"] = style
        if language:
            body["language"] = language
        return await self._request("POST", "/v1/docgen/create", json=body)

    async def preview(
        self, prompt: str, format: str = "pdf", *, style: str | None = None
    ) -> dict[str, Any]:
        body: dict[str, Any] = {"prompt": prompt, "format": format}
        if style:
            body["style"] = style
        return await self._request("POST", "/v1/docgen/preview", json=body)

    async def formats(self) -> list[dict[str, Any]]:
        return await self._request("GET", "/v1/docgen/formats")

    async def templates(self) -> list[dict[str, Any]]:
        return await self._request("GET", "/v1/docgen/templates")

    async def history(
        self, *, limit: int | None = None, offset: int | None = None
    ) -> dict[str, Any]:
        params: dict[str, Any] = {}
        if limit is not None:
            params["limit"] = limit
        if offset is not None:
            params["offset"] = offset
        return await self._request("GET", "/v1/docgen/history", params=params)

    async def share(self, doc_id: str, target_email: str) -> dict[str, Any]:
        return await self._request(
            "POST", "/v1/docgen/share", json={"doc_id": doc_id, "target_email": target_email}
        )

    async def revise(self, doc_id: str, prompt: str) -> dict[str, Any]:
        return await self._request(
            "POST", "/v1/docgen/revise", json={"doc_id": doc_id, "prompt": prompt}
        )

    async def versions(self, doc_id: str) -> dict[str, Any]:
        return await self._request("GET", f"/v1/docgen/versions/{doc_id}")

    async def download(self, doc_id: str) -> bytes:
        return await self._request_binary("GET", f"/v1/docgen/download/{doc_id}")
