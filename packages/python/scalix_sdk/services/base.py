"""Base HTTP service for Scalix API calls."""

from __future__ import annotations

import asyncio
import random
from typing import Any

import httpx

from scalix_sdk.config import ScalixConfig
from scalix_sdk.exceptions import (
    AuthenticationError,
    BadRequestError,
    ConflictError,
    InternalServerError,
    NotFoundError,
    PermissionDeniedError,
    RateLimitError,
    ScalixError,
    UnprocessableEntityError,
)

_shared_client: httpx.AsyncClient | None = None

RETRYABLE_STATUS_CODES = {408, 409, 429, 500, 502, 503, 504}


def _get_client(timeout: float = 60.0) -> httpx.AsyncClient:
    global _shared_client
    if _shared_client is None or _shared_client.is_closed:
        _shared_client = httpx.AsyncClient(timeout=timeout)
    return _shared_client


def _backoff_delay(attempt: int, retry_after: float | None = None) -> float:
    if retry_after is not None:
        return retry_after
    base = min(0.5 * (2 ** attempt), 8.0)
    return base * (0.5 + random.random() * 0.5)


_STATUS_MAP = {
    400: BadRequestError,
    401: AuthenticationError,
    403: PermissionDeniedError,
    404: NotFoundError,
    409: ConflictError,
    422: UnprocessableEntityError,
    429: RateLimitError,
}


def _throw_for_status(status: int, message: str, request_id: str | None = None) -> None:
    cls = _STATUS_MAP.get(status)
    if cls:
        raise cls(message, request_id)
    if status >= 500:
        raise InternalServerError(message, request_id)
    raise ScalixError(message, status=status, request_id=request_id)


class BaseService:
    def __init__(self, config: ScalixConfig) -> None:
        self._config = config

    async def _request(
        self,
        method: str,
        path: str,
        json: dict[str, Any] | None = None,
        params: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        if not self._config.api_key:
            raise AuthenticationError("API key required. Pass api_key to Scalix().")

        url = f"{self._config.base_url}{path}"
        headers = {
            "Authorization": f"Bearer {self._config.api_key}",
            "Content-Type": "application/json",
        }

        last_error: Exception | None = None
        max_retries = self._config.max_retries

        for attempt in range(max_retries + 1):
            try:
                client = _get_client(self._config.timeout)
                resp = await client.request(method, url, headers=headers, json=json, params=params)
            except (httpx.ConnectError, httpx.TimeoutException) as exc:
                last_error = exc
                if attempt < max_retries:
                    await asyncio.sleep(_backoff_delay(attempt))
                    continue
                raise ScalixError(f"Connection failed: {exc}") from exc

            if resp.is_success:
                return resp.json()

            request_id = resp.headers.get("x-request-id")
            try:
                body = resp.json()
                msg = body.get("error", {}).get("message", f"Request failed: {resp.status_code}")
            except Exception:
                msg = f"Request failed: {resp.status_code}"

            if attempt < max_retries and resp.status_code in RETRYABLE_STATUS_CODES:
                retry_after_str = resp.headers.get("retry-after")
                retry_after = float(retry_after_str) if retry_after_str else None
                last_error = ScalixError(msg, status=resp.status_code, request_id=request_id)
                await asyncio.sleep(_backoff_delay(attempt, retry_after))
                continue

            _throw_for_status(resp.status_code, msg, request_id)

        raise last_error or ScalixError("Request failed after retries")

    async def _request_binary(
        self,
        method: str,
        path: str,
        params: dict[str, Any] | None = None,
        json: dict[str, Any] | None = None,
    ) -> bytes:
        if not self._config.api_key:
            raise AuthenticationError("API key required. Pass api_key to Scalix().")

        url = f"{self._config.base_url}{path}"
        headers = {"Authorization": f"Bearer {self._config.api_key}"}

        last_error: Exception | None = None
        max_retries = self._config.max_retries

        for attempt in range(max_retries + 1):
            try:
                client = _get_client(self._config.timeout)
                resp = await client.request(method, url, headers=headers, params=params, json=json)
            except (httpx.ConnectError, httpx.TimeoutException) as exc:
                last_error = exc
                if attempt < max_retries:
                    await asyncio.sleep(_backoff_delay(attempt))
                    continue
                raise ScalixError(f"Connection failed: {exc}") from exc

            if resp.is_success:
                return resp.content

            request_id = resp.headers.get("x-request-id")
            try:
                body = resp.json()
                msg = body.get("error", {}).get("message", f"Request failed: {resp.status_code}")
            except Exception:
                msg = f"Request failed: {resp.status_code}"

            if attempt < max_retries and resp.status_code in RETRYABLE_STATUS_CODES:
                retry_after_str = resp.headers.get("retry-after")
                retry_after = float(retry_after_str) if retry_after_str else None
                last_error = ScalixError(msg, status=resp.status_code, request_id=request_id)
                await asyncio.sleep(_backoff_delay(attempt, retry_after))
                continue

            _throw_for_status(resp.status_code, msg, request_id)

        raise last_error or ScalixError("Request failed after retries")

    async def _request_multipart(
        self,
        path: str,
        files: dict[str, Any],
        data: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        if not self._config.api_key:
            raise AuthenticationError("API key required.")

        url = f"{self._config.base_url}{path}"
        headers = {"Authorization": f"Bearer {self._config.api_key}"}

        last_error: Exception | None = None
        max_retries = self._config.max_retries

        for attempt in range(max_retries + 1):
            try:
                client = _get_client(self._config.timeout)
                resp = await client.post(url, headers=headers, files=files, data=data)
            except (httpx.ConnectError, httpx.TimeoutException) as exc:
                last_error = exc
                if attempt < max_retries:
                    await asyncio.sleep(_backoff_delay(attempt))
                    continue
                raise ScalixError(f"Connection failed: {exc}") from exc

            if resp.is_success:
                return resp.json()

            request_id = resp.headers.get("x-request-id")
            try:
                body = resp.json()
                msg = body.get("error", {}).get("message", f"Upload failed: {resp.status_code}")
            except Exception:
                msg = f"Upload failed: {resp.status_code}"

            if attempt < max_retries and resp.status_code in RETRYABLE_STATUS_CODES:
                retry_after_str = resp.headers.get("retry-after")
                retry_after = float(retry_after_str) if retry_after_str else None
                last_error = ScalixError(msg, status=resp.status_code, request_id=request_id)
                await asyncio.sleep(_backoff_delay(attempt, retry_after))
                continue

            _throw_for_status(resp.status_code, msg, request_id)

        raise last_error or ScalixError("Request failed after retries")
