"""Image generation service."""

from __future__ import annotations

from typing import Any

from scalix_sdk.services.base import BaseService


class ImagesService(BaseService):
    async def generate(
        self,
        prompt: str,
        *,
        model: str | None = None,
        size: str | None = None,
        n: int | None = None,
    ) -> dict[str, Any]:
        body: dict[str, Any] = {"prompt": prompt}
        if model:
            body["model"] = model
        if size:
            body["size"] = size
        if n:
            body["n"] = n
        return await self._request("POST", "/v1/images/generate", json=body)

    async def generate_async(self, prompt: str, **kwargs: Any) -> dict[str, Any]:
        body: dict[str, Any] = {"prompt": prompt, **kwargs}
        return await self._request("POST", "/v1/images/generate/queue", json=body)

    async def get_job(self, job_id: str) -> dict[str, Any]:
        return await self._request("GET", f"/v1/images/jobs/{job_id}")

    async def get_job_result(self, job_id: str) -> dict[str, Any]:
        return await self._request("GET", f"/v1/images/jobs/{job_id}/result")

    async def models(self) -> dict[str, Any]:
        return await self._request("GET", "/v1/images/models")
