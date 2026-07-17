"""Tests for the retry/backoff/idempotency transports."""

from __future__ import annotations

import httpx

from scalix_sdk._transport import (
    AsyncRetryTransport,
    RetryTransport,
    backoff_seconds,
    parse_retry_after,
)


def test_parse_retry_after_delta_seconds():
    assert parse_retry_after("2") == 2.0
    assert parse_retry_after("0") == 0.0
    assert parse_retry_after(None) is None
    assert parse_retry_after("soon") is None


def test_parse_retry_after_http_date():
    from email.utils import formatdate

    now = 1_700_000_000.0
    header = formatdate(now + 5, usegmt=True)  # RFC 1123 date, 5s in the future
    assert parse_retry_after(header, now) == 5.0


def test_backoff_grows_and_caps():
    no_jitter = lambda: 0.0  # noqa: E731 -> 50% of the term
    assert backoff_seconds(0, 0.5, 8.0, no_jitter) == 0.25
    assert backoff_seconds(1, 0.5, 8.0, no_jitter) == 0.5
    assert backoff_seconds(2, 0.5, 8.0, no_jitter) == 1.0
    assert backoff_seconds(10, 0.5, 8.0, no_jitter) == 4.0  # capped at 8 -> 50% floor


def test_retries_429_then_returns_200():
    calls = []

    def handler(request: httpx.Request) -> httpx.Response:
        calls.append(request)
        return httpx.Response(429) if len(calls) == 1 else httpx.Response(200, json={"ok": True})

    delays: list[float] = []
    transport = RetryTransport(
        httpx.MockTransport(handler),
        sleep=delays.append,
        rand=lambda: 0.0,
    )
    with httpx.Client(transport=transport) as client:
        response = client.post("https://api.scalix.world/x")

    assert response.status_code == 200
    assert len(calls) == 2
    assert len(delays) == 1


def test_stops_after_max_retries():
    calls = []

    def handler(request: httpx.Request) -> httpx.Response:
        calls.append(request)
        return httpx.Response(503)

    transport = RetryTransport(httpx.MockTransport(handler), max_retries=2, sleep=lambda _s: None)
    with httpx.Client(transport=transport) as client:
        response = client.get("https://api.scalix.world/x")

    assert response.status_code == 503
    assert len(calls) == 3  # initial + 2 retries


def test_does_not_retry_400():
    calls = []

    def handler(request: httpx.Request) -> httpx.Response:
        calls.append(request)
        return httpx.Response(400)

    transport = RetryTransport(httpx.MockTransport(handler), sleep=lambda _s: None)
    with httpx.Client(transport=transport) as client:
        response = client.get("https://api.scalix.world/x")

    assert response.status_code == 400
    assert len(calls) == 1


def test_honors_retry_after():
    calls = []

    def handler(request: httpx.Request) -> httpx.Response:
        calls.append(request)
        if len(calls) == 1:
            return httpx.Response(429, headers={"retry-after": "3"})
        return httpx.Response(200)

    delays: list[float] = []
    transport = RetryTransport(httpx.MockTransport(handler), sleep=delays.append)
    with httpx.Client(transport=transport) as client:
        client.get("https://api.scalix.world/x")

    assert delays == [3.0]


def test_idempotency_key_added_and_stable_across_retries():
    keys: list[str | None] = []

    def handler(request: httpx.Request) -> httpx.Response:
        keys.append(request.headers.get("idempotency-key"))
        return httpx.Response(429) if len(keys) == 1 else httpx.Response(200)

    transport = RetryTransport(
        httpx.MockTransport(handler), sleep=lambda _s: None, rand=lambda: 0.0
    )
    with httpx.Client(transport=transport) as client:
        client.post("https://api.scalix.world/x")

    assert keys[0] is not None
    assert keys[0] == keys[1]


def test_no_idempotency_key_on_get():
    seen: dict[str, str | None] = {}

    def handler(request: httpx.Request) -> httpx.Response:
        seen["key"] = request.headers.get("idempotency-key")
        return httpx.Response(200)

    transport = RetryTransport(httpx.MockTransport(handler))
    with httpx.Client(transport=transport) as client:
        client.get("https://api.scalix.world/x")

    assert seen["key"] is None


def test_idempotency_can_be_disabled():
    seen: dict[str, str | None] = {}

    def handler(request: httpx.Request) -> httpx.Response:
        seen["key"] = request.headers.get("idempotency-key")
        return httpx.Response(200)

    transport = RetryTransport(httpx.MockTransport(handler), idempotency=False)
    with httpx.Client(transport=transport) as client:
        client.post("https://api.scalix.world/x")

    assert seen["key"] is None


async def test_async_retries_429_then_200():
    calls = []

    def handler(request: httpx.Request) -> httpx.Response:
        calls.append(request)
        return httpx.Response(429) if len(calls) == 1 else httpx.Response(200, json={"ok": True})

    delays: list[float] = []

    async def fake_sleep(seconds: float) -> None:
        delays.append(seconds)

    transport = AsyncRetryTransport(
        httpx.MockTransport(handler), sleep=fake_sleep, rand=lambda: 0.0
    )
    async with httpx.AsyncClient(transport=transport) as client:
        response = await client.post("https://api.scalix.world/x")

    assert response.status_code == 200
    assert len(calls) == 2
    assert len(delays) == 1
