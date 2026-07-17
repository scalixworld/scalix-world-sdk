"""Tests for the typed error hierarchy and the raising event hooks."""

from __future__ import annotations

import httpx
import pytest

from scalix_sdk.errors import (
    AuthenticationError,
    InvalidRequestError,
    NotFoundError,
    RateLimitError,
    ServerError,
    _araise_on_error,
    _raise_on_error,
    error_from_response,
    raise_for_status,
)


def test_status_maps_to_typed_error():
    assert isinstance(error_from_response(httpx.Response(400)), InvalidRequestError)
    assert isinstance(error_from_response(httpx.Response(401)), AuthenticationError)
    assert isinstance(error_from_response(httpx.Response(404)), NotFoundError)
    assert isinstance(error_from_response(httpx.Response(429)), RateLimitError)
    assert isinstance(error_from_response(httpx.Response(500)), ServerError)
    assert isinstance(error_from_response(httpx.Response(503)), ServerError)


def test_error_carries_code_request_id_and_message():
    response = httpx.Response(
        401,
        json={"code": "AUTH_FAILED", "error": "bad key"},
        headers={"x-request-id": "req_1"},
    )
    err = error_from_response(response)
    assert err.status_code == 401
    assert err.code == "AUTH_FAILED"
    assert err.request_id == "req_1"
    assert "bad key" in str(err)


def test_raise_for_status_noop_on_success():
    raise_for_status(httpx.Response(200, json={"ok": True}))  # must not raise


def test_raise_for_status_raises_on_error():
    with pytest.raises(RateLimitError):
        raise_for_status(httpx.Response(429))


def test_sync_hook_raises_typed_error_through_client():
    def handler(_request: httpx.Request) -> httpx.Response:
        return httpx.Response(429, json={"error": "slow down"})

    client = httpx.Client(
        transport=httpx.MockTransport(handler),
        event_hooks={"response": [_raise_on_error]},
    )
    with client, pytest.raises(RateLimitError):
        client.get("https://api.scalix.world/x")


def test_sync_hook_passes_through_success():
    def handler(_request: httpx.Request) -> httpx.Response:
        return httpx.Response(200, json={"ok": True})

    client = httpx.Client(
        transport=httpx.MockTransport(handler),
        event_hooks={"response": [_raise_on_error]},
    )
    with client:
        response = client.get("https://api.scalix.world/x")
    assert response.json() == {"ok": True}


async def test_async_hook_raises_typed_error():
    def handler(_request: httpx.Request) -> httpx.Response:
        return httpx.Response(401, json={"error": "no"})

    client = httpx.AsyncClient(
        transport=httpx.MockTransport(handler),
        event_hooks={"response": [_araise_on_error]},
    )
    async with client:
        with pytest.raises(AuthenticationError):
            await client.get("https://api.scalix.world/x")
