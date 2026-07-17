"""Factory for a hardened, production-grade Scalix client.

Assembles the generated :class:`AuthenticatedClient` with:
  - retry/backoff transports (429/5xx, ``Retry-After``-aware),
  - an ``Idempotency-Key`` on writes,
  - an SDK-version ``User-Agent``,
  - typed error-raising on ``>= 400`` responses (the ergonomic default).

The generated client builds its sync + async httpx clients from a single shared
``httpx_args`` dict, so a single transport can't serve both. Instead we build both
httpx clients explicitly (with the matching sync/async transport + raise hook) and
inject them via ``set_httpx_client`` / ``set_async_httpx_client``.
"""

from __future__ import annotations

import httpx

from ._transport import USER_AGENT, AsyncRetryTransport, RetryTransport
from .errors import _araise_on_error, _raise_on_error
from .generated import AuthenticatedClient

DEFAULT_BASE_URL = "https://api.scalix.world"

__all__ = ["create_client", "DEFAULT_BASE_URL"]


def create_client(
    token: str,
    *,
    base_url: str = DEFAULT_BASE_URL,
    max_retries: int = 2,
    timeout: float = 30.0,
    raise_on_error: bool = True,
    idempotency: bool = True,
    verify_ssl: bool = True,
    transport: httpx.BaseTransport | None = None,
    async_transport: httpx.AsyncBaseTransport | None = None,
) -> AuthenticatedClient:
    """Create a hardened :class:`AuthenticatedClient`.

    Args:
        token: your Scalix API key (``scalix_sk_...`` or ``scalix_pat_...``).
        base_url: API base URL. Defaults to ``https://api.scalix.world``.
        max_retries: retries after the initial attempt on 429/5xx. Default 2.
        timeout: per-request timeout in seconds. Default 30.
        raise_on_error: raise a typed error on ``>= 400``. Default True.
        idempotency: send an ``Idempotency-Key`` on writes. Default True.
        verify_ssl: verify TLS certificates. Default True.
        transport / async_transport: advanced — the underlying transport to wrap
            with retries (e.g. for proxies or tests). Defaults to httpx's own.
    """
    headers = {"User-Agent": USER_AGENT}
    httpx_timeout = httpx.Timeout(timeout)

    sync_client = httpx.Client(
        base_url=base_url,
        headers={**headers, "Authorization": f"Bearer {token}"},
        timeout=httpx_timeout,
        verify=verify_ssl,
        transport=RetryTransport(
            transport,
            max_retries=max_retries,
            idempotency=idempotency,
        ),
        event_hooks={"response": [_raise_on_error]} if raise_on_error else {},
    )

    async_client = httpx.AsyncClient(
        base_url=base_url,
        headers={**headers, "Authorization": f"Bearer {token}"},
        timeout=httpx_timeout,
        verify=verify_ssl,
        transport=AsyncRetryTransport(
            async_transport,
            max_retries=max_retries,
            idempotency=idempotency,
        ),
        event_hooks={"response": [_araise_on_error]} if raise_on_error else {},
    )

    client = AuthenticatedClient(base_url=base_url, token=token, verify_ssl=verify_ssl)
    client.set_httpx_client(sync_client)
    client.set_async_httpx_client(async_client)
    return client
