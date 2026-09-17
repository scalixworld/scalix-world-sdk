"""Retrying httpx transports for the Scalix SDK.

Wraps the default httpx transport with exponential backoff + jitter on 429/5xx
(honoring ``Retry-After``) and stamps an ``Idempotency-Key`` on write requests so
retries of a POST/PUT/PATCH replay safely. Keeping this at the transport layer
means the retry loop reuses one request object, so the idempotency key is stable
across attempts. The SDK-version ``User-Agent`` is set on the client headers by
:func:`scalix_sdk.create_client`.
"""

from __future__ import annotations

import asyncio
import email.utils
import random
import time
import uuid
from datetime import timezone
from typing import TYPE_CHECKING

import httpx

from ._version import __version__

if TYPE_CHECKING:
    from collections.abc import Awaitable, Callable

USER_AGENT = f"scalix-python/{__version__}"

RETRYABLE_STATUS = frozenset({408, 429, 500, 502, 503, 504})
IDEMPOTENT_WRITE_METHODS = frozenset({"POST", "PUT", "PATCH"})
_RETRY_AFTER_CEILING_SECONDS = 60.0


def _is_retryable(status_code: int) -> bool:
    return status_code in RETRYABLE_STATUS or status_code >= 500


def parse_retry_after(value: str | None, now: float | None = None) -> float | None:
    """Parse a ``Retry-After`` header into seconds (delta-seconds or HTTP-date)."""
    if not value:
        return None
    value = value.strip()
    if value.isdigit():
        return max(0.0, float(value))
    try:
        parsed = email.utils.parsedate_to_datetime(value)
    except (TypeError, ValueError):
        return None
    if parsed is None:
        return None
    if parsed.tzinfo is None:
        parsed = parsed.replace(tzinfo=timezone.utc)
    reference = now if now is not None else time.time()
    return max(0.0, parsed.timestamp() - reference)


def backoff_seconds(attempt: int, base: float, cap: float, rand: Callable[[], float]) -> float:
    """Exponential backoff with jitter in [50%, 100%] of the capped term."""
    expo: float = min(cap, base * (2 ** attempt))
    return expo * (0.5 + rand() * 0.5)


def _add_idempotency_key(request: httpx.Request, enabled: bool) -> None:
    if not enabled:
        return
    method = request.method.upper()
    if method in IDEMPOTENT_WRITE_METHODS and "idempotency-key" not in request.headers:
        request.headers["idempotency-key"] = str(uuid.uuid4())


def _delay_for(
    response: httpx.Response, attempt: int, base: float, cap: float, rand: Callable[[], float]
) -> float:
    retry_after = parse_retry_after(response.headers.get("retry-after"))
    if retry_after is not None:
        return min(retry_after, _RETRY_AFTER_CEILING_SECONDS)
    return backoff_seconds(attempt, base, cap, rand)


class RetryTransport(httpx.BaseTransport):
    """Sync transport wrapper with retry/backoff + idempotency."""

    def __init__(
        self,
        wrapped: httpx.BaseTransport | None = None,
        *,
        max_retries: int = 2,
        base_delay: float = 0.5,
        max_delay: float = 8.0,
        idempotency: bool = True,
        rand: Callable[[], float] | None = None,
        sleep: Callable[[float], None] | None = None,
    ) -> None:
        self._wrapped = wrapped if wrapped is not None else httpx.HTTPTransport()
        self._max_retries = max_retries
        self._base_delay = base_delay
        self._max_delay = max_delay
        self._idempotency = idempotency
        self._rand = rand or random.random
        self._sleep = sleep or time.sleep

    def handle_request(self, request: httpx.Request) -> httpx.Response:
        _add_idempotency_key(request, self._idempotency)
        attempt = 0
        while True:
            response = self._wrapped.handle_request(request)
            if attempt >= self._max_retries or not _is_retryable(response.status_code):
                return response
            _drain(response)
            delay = _delay_for(response, attempt, self._base_delay, self._max_delay, self._rand)
            self._sleep(delay)
            attempt += 1

    def close(self) -> None:
        self._wrapped.close()


class AsyncRetryTransport(httpx.AsyncBaseTransport):
    """Async transport wrapper with retry/backoff + idempotency."""

    def __init__(
        self,
        wrapped: httpx.AsyncBaseTransport | None = None,
        *,
        max_retries: int = 2,
        base_delay: float = 0.5,
        max_delay: float = 8.0,
        idempotency: bool = True,
        rand: Callable[[], float] | None = None,
        sleep: Callable[[float], Awaitable[None]] | None = None,
    ) -> None:
        self._wrapped = wrapped if wrapped is not None else httpx.AsyncHTTPTransport()
        self._max_retries = max_retries
        self._base_delay = base_delay
        self._max_delay = max_delay
        self._idempotency = idempotency
        self._rand = rand or random.random
        self._sleep = sleep or asyncio.sleep

    async def handle_async_request(self, request: httpx.Request) -> httpx.Response:
        _add_idempotency_key(request, self._idempotency)
        attempt = 0
        while True:
            response = await self._wrapped.handle_async_request(request)
            if attempt >= self._max_retries or not _is_retryable(response.status_code):
                return response
            await _adrain(response)
            delay = _delay_for(response, attempt, self._base_delay, self._max_delay, self._rand)
            await self._sleep(delay)
            attempt += 1

    async def aclose(self) -> None:
        await self._wrapped.aclose()


def _drain(response: httpx.Response) -> None:
    """Consume + close a discarded response so the connection can be reused."""
    try:
        response.read()
    except Exception:
        pass
    finally:
        response.close()


async def _adrain(response: httpx.Response) -> None:
    try:
        await response.aread()
    except Exception:
        pass
    finally:
        await response.aclose()
