"""Scalix SDK — Python client for the Scalix platform."""

from scalix._version import __version__
from scalix.client import Scalix, ScalixClient
from scalix.config import ScalixConfig
from scalix.exceptions import (
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
