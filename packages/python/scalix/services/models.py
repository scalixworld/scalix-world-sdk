"""Models service — list and inspect available Scalix models."""

from __future__ import annotations

from typing import Any

from scalix.services.base import BaseService


class ModelsService(BaseService):
    async def list(self) -> list[dict[str, Any]]:
        resp = await self._request("GET", "/v1/models")
        return resp.get("data", [])

    async def get(self, model_id: str) -> dict[str, Any] | None:
        models = await self.list()
        return next((m for m in models if m.get("id") == model_id), None)
