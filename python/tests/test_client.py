"""Integration tests for the hardened create_client factory.

Uses httpx.MockTransport (injected via the factory's `transport`/`async_transport`
override) so we exercise the full stack — retry transport, auth + UA headers,
idempotency, and typed error-raising — end to end, including through a real
generated operation.
"""

from __future__ import annotations

import httpx
import pytest

from scalix_sdk import AuthenticationError, create_client
from scalix_sdk._transport import USER_AGENT
from scalix_sdk.generated.api.database import execute_sql
from scalix_sdk.generated.models import SqlRequest


def test_factory_sets_user_agent_auth_and_idempotency():
    seen: dict[str, str | None] = {}

    def handler(request: httpx.Request) -> httpx.Response:
        seen["ua"] = request.headers.get("user-agent")
        seen["auth"] = request.headers.get("authorization")
        seen["idem"] = request.headers.get("idempotency-key")
        return httpx.Response(200, json={})

    client = create_client("scalix_sk_test", transport=httpx.MockTransport(handler))
    with client:
        client.get_httpx_client().post("https://api.scalix.world/x")

    assert seen["ua"] == USER_AGENT
    assert seen["auth"] == "Bearer scalix_sk_test"
    assert seen["idem"] is not None


def test_factory_raises_typed_error_by_default():
    def handler(_request: httpx.Request) -> httpx.Response:
        return httpx.Response(401, json={"error": "bad key"})

    client = create_client("scalix_sk_test", transport=httpx.MockTransport(handler))
    with client, pytest.raises(AuthenticationError):
        client.get_httpx_client().get("https://api.scalix.world/x")


def test_factory_raise_on_error_can_be_disabled():
    def handler(_request: httpx.Request) -> httpx.Response:
        return httpx.Response(404, json={"error": "missing"})

    client = create_client(
        "scalix_sk_test",
        transport=httpx.MockTransport(handler),
        raise_on_error=False,
    )
    with client:
        response = client.get_httpx_client().get("https://api.scalix.world/x")
    assert response.status_code == 404


def test_generated_operation_retries_and_carries_headers():
    """A real generated op (execute_sql) benefits from retry + auth + idempotency."""
    calls: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        calls.append(request)
        if len(calls) == 1:
            return httpx.Response(429)
        return httpx.Response(
            200, json={"columns": [], "rows": {}, "row_count": 0, "duration_ms": 1}
        )

    # base_delay tiny so the one retry doesn't add measurable wall time.
    from scalix_sdk._transport import RetryTransport

    client = create_client("scalix_sk_test")
    client.set_httpx_client(
        httpx.Client(
            base_url="https://api.scalix.world",
            headers={"User-Agent": USER_AGENT, "Authorization": "Bearer scalix_sk_test"},
            transport=RetryTransport(
                httpx.MockTransport(handler), base_delay=0.0, max_delay=0.0
            ),
            event_hooks={},
        )
    )

    execute_sql.sync_detailed(client=client, body=SqlRequest(query="SELECT 1"))

    assert len(calls) == 2  # retried the 429
    assert calls[1].headers.get("authorization") == "Bearer scalix_sk_test"
    assert calls[1].headers.get("user-agent") == USER_AGENT
    assert calls[0].headers.get("idempotency-key") == calls[1].headers.get("idempotency-key")


async def test_async_factory_client_works():
    def handler(_request: httpx.Request) -> httpx.Response:
        return httpx.Response(200, json={"ok": True})

    client = create_client("scalix_sk_test", async_transport=httpx.MockTransport(handler))
    async with client:
        response = await client.get_async_httpx_client().get("https://api.scalix.world/x")
    assert response.status_code == 200
