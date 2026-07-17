"""Scalix SDK — the official Python client for Scalix Cloud.

The generated core is auto-generated from the OpenAPI spec (``sdk/openapi.json``,
itself generated from the gateway's utoipa annotations) via
``openapi-python-client``. Regenerate with ``scripts/generate.sh``; do NOT
hand-edit ``scalix_sdk/generated/``.

On top of the generated core, a thin hand-written layer adds Stripe/OpenAI-grade
defaults: retry with exponential backoff + jitter (honoring ``Retry-After``), an
``Idempotency-Key`` on writes, an SDK-version ``User-Agent``, and a typed error
hierarchy that is raised by default. Use :func:`create_client` to build a hardened
client; drop to :class:`AuthenticatedClient` for the raw generated behavior.
"""

from scalix_sdk._client import DEFAULT_BASE_URL, create_client
from scalix_sdk._version import __version__
from scalix_sdk.errors import (
    APIConnectionError,
    APIStatusError,
    AuthenticationError,
    ConflictError,
    InvalidRequestError,
    NotFoundError,
    PermissionDeniedError,
    RateLimitError,
    ScalixError,
    ServerError,
    UnprocessableEntityError,
    raise_for_status,
)
from scalix_sdk.generated import AuthenticatedClient, Client

__all__ = [
    # Client construction
    "create_client",
    "AuthenticatedClient",
    "Client",
    "DEFAULT_BASE_URL",
    "__version__",
    # Typed errors
    "ScalixError",
    "APIConnectionError",
    "APIStatusError",
    "InvalidRequestError",
    "AuthenticationError",
    "PermissionDeniedError",
    "NotFoundError",
    "ConflictError",
    "UnprocessableEntityError",
    "RateLimitError",
    "ServerError",
    "raise_for_status",
]
