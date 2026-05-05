"""Scalix SDK — Python client for the Scalix platform."""

from scalix_sdk._version import __version__
from scalix_sdk.client import Scalix, ScalixClient
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

__all__ = [
    "__version__",
    "Scalix",
    "ScalixClient",
    "ScalixConfig",
    "ScalixError",
    "AuthenticationError",
    "BadRequestError",
    "ConflictError",
    "InternalServerError",
    "NotFoundError",
    "PermissionDeniedError",
    "RateLimitError",
    "UnprocessableEntityError",
]
