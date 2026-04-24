"""Scalix SDK — Python client for the Scalix API."""

from scalix._version import __version__
from scalix.client import ScalixClient
from scalix.config import configure, get_config
from scalix.exceptions import (
    AuthenticationError,
    ScalixError,
)

__all__ = [
    "__version__",
    "ScalixClient",
    "configure",
    "get_config",
    "ScalixError",
    "AuthenticationError",
]
