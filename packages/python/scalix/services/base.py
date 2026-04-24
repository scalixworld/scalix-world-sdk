"""Base HTTP service for Scalix API calls."""

from __future__ import annotations

from typing import Any

from scalix.config import ScalixConfig, get_config
from scalix.exceptions import AuthenticationError, ScalixError


class BaseService:
    def __init__(self, config: ScalixConfig | None = None) -> None:
        self._config = config or get_config()

    async def _request(
        self,
        method: str,
        path: str,
        json: dict[str, Any] | None = None,
        params: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        import httpx

        if not self._config.api_key:
            raise AuthenticationError("API key required. Call configure(api_key='...') first.")

        url = f"{self._config.base_url}{path}"
        headers = {
            "Authorization": f"Bearer {self._config.api_key}",
            "Content-Type": "application/json",
        }

        async with httpx.AsyncClient(timeout=60.0) as client:
            resp = await client.request(
                method, url, headers=headers, json=json, params=params
            )

        if not resp.is_success:
            try:
                body = resp.json()
                msg = body.get("error", {}).get("message", f"Request failed: {resp.status_code}")
            except Exception:
                msg = f"Request failed: {resp.status_code}"
            raise ScalixError(msg)

        return resp.json()

    async def _request_binary(
        self,
        method: str,
        path: str,
        params: dict[str, Any] | None = None,
        json: dict[str, Any] | None = None,
    ) -> bytes:
        import httpx

        if not self._config.api_key:
            raise AuthenticationError("API key required. Call configure(api_key='...') first.")

        url = f"{self._config.base_url}{path}"
        headers = {"Authorization": f"Bearer {self._config.api_key}"}

        async with httpx.AsyncClient(timeout=120.0) as client:
            resp = await client.request(
                method, url, headers=headers, params=params, json=json
            )

        if not resp.is_success:
            try:
                body = resp.json()
                msg = body.get("error", {}).get("message", f"Request failed: {resp.status_code}")
            except Exception:
                msg = f"Request failed: {resp.status_code}"
            raise ScalixError(msg)

        return resp.content

    async def _request_multipart(
        self,
        path: str,
        files: dict[str, Any],
        data: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        import httpx

        if not self._config.api_key:
            raise AuthenticationError("API key required.")

        url = f"{self._config.base_url}{path}"
        headers = {"Authorization": f"Bearer {self._config.api_key}"}

        async with httpx.AsyncClient(timeout=120.0) as client:
            resp = await client.post(url, headers=headers, files=files, data=data)

        if not resp.is_success:
            try:
                body = resp.json()
                msg = body.get("error", {}).get("message", f"Upload failed: {resp.status_code}")
            except Exception:
                msg = f"Upload failed: {resp.status_code}"
            raise ScalixError(msg)

        return resp.json()
