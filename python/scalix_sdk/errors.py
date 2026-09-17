"""Typed error hierarchy for the Scalix SDK.

The generated ``openapi-python-client`` returns documented error bodies and only
raises ``generated.errors.UnexpectedStatus`` for *undocumented* statuses — so it
is easy to forget to check for errors. This module provides a Stripe/OpenAI-style
typed hierarchy plus httpx response event hooks (installed by
:func:`scalix_sdk.create_client`) that raise the right subclass on any ``>= 400``
response, making error-raising the ergonomic default.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import httpx

__all__ = [
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
    "error_from_response",
    "raise_for_status",
]


class ScalixError(Exception):
    """Base class for every error raised by the Scalix SDK."""


class APIConnectionError(ScalixError):
    """A network-level failure occurred before a response was received."""

    def __init__(
        self, message: str = "Connection error", *, request: httpx.Request | None = None
    ) -> None:
        super().__init__(message)
        self.request = request


class APIStatusError(ScalixError):
    """Base class for all HTTP error responses (status >= 400).

    Attributes:
        status_code: the HTTP status.
        response: the raw httpx response.
        code: the stable machine-readable code from the error envelope, if present.
        request_id: the ``x-request-id`` correlation id, if present.
        body: the parsed JSON error envelope, if the body was JSON.
    """

    def __init__(self, message: str, *, response: httpx.Response) -> None:
        super().__init__(message)
        self.response = response
        self.status_code = response.status_code
        self.request_id = response.headers.get("x-request-id")
        self.code: str | None = None
        self.body: dict[str, object] | None = None
        try:
            data = response.json()
        except Exception:
            return
        if isinstance(data, dict):
            self.body = data
            code = data.get("code")
            self.code = code if isinstance(code, str) else None


class InvalidRequestError(APIStatusError):
    """400 — the request was malformed or failed validation."""


class AuthenticationError(APIStatusError):
    """401 — the API key is missing or invalid."""


class PermissionDeniedError(APIStatusError):
    """403 — the caller is not permitted to perform this action."""


class NotFoundError(APIStatusError):
    """404 — the requested resource does not exist."""


class ConflictError(APIStatusError):
    """409 — the request conflicts with the current state."""


class UnprocessableEntityError(APIStatusError):
    """422 — the request was well-formed but semantically invalid."""


class RateLimitError(APIStatusError):
    """429 — the caller has been rate limited."""


class ServerError(APIStatusError):
    """5xx — the server failed to fulfil an apparently valid request."""


_STATUS_MAP: dict[int, type[APIStatusError]] = {
    400: InvalidRequestError,
    401: AuthenticationError,
    403: PermissionDeniedError,
    404: NotFoundError,
    409: ConflictError,
    422: UnprocessableEntityError,
    429: RateLimitError,
}


def error_from_response(response: httpx.Response) -> APIStatusError:
    """Map an error response to the most specific typed error."""
    cls = _STATUS_MAP.get(response.status_code)
    if cls is None:
        cls = ServerError if response.status_code >= 500 else APIStatusError
    message = _message_for(response)
    return cls(message, response=response)


def _message_for(response: httpx.Response) -> str:
    try:
        data = response.json()
        if isinstance(data, dict):
            detail = data.get("error") or data.get("message")
            if isinstance(detail, str) and detail:
                return f"{response.status_code} {detail}"
    except Exception:
        pass
    return f"{response.status_code} {response.reason_phrase or 'Error'}"


def raise_for_status(response: httpx.Response) -> None:
    """Raise the matching typed error if the response is an error (status >= 400)."""
    if response.status_code >= 400:
        raise error_from_response(response)


def _raise_on_error(response: httpx.Response) -> None:
    """Sync httpx response event hook — reads the body then raises on >= 400."""
    if response.status_code >= 400:
        response.read()
        raise error_from_response(response)


async def _araise_on_error(response: httpx.Response) -> None:
    """Async httpx response event hook — reads the body then raises on >= 400."""
    if response.status_code >= 400:
        await response.aread()
        raise error_from_response(response)
