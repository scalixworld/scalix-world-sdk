"""Storage service — presigned upload URLs."""

from __future__ import annotations

from typing import Any

from scalix_sdk.services.base import BaseService


class StorageService(BaseService):
    async def get_upload_url(
        self, mime_type: str, *, size: int | None = None
    ) -> dict[str, Any]:
        body: dict[str, Any] = {"mimeType": mime_type}
        if size is not None:
            body["size"] = size
        return await self._request("POST", "/v1/storage/upload-url", json=body)
