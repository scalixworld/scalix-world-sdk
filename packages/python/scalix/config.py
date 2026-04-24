"""Scalix SDK configuration."""

from __future__ import annotations

import os
from typing import Any

from pydantic import BaseModel, Field


class ScalixConfig(BaseModel):
    api_key: str | None = Field(default=None)
    base_url: str = Field(default="https://api.scalix.world")
    default_model: str = Field(default="scalix-world-ai")


_config: ScalixConfig | None = None


def configure(**kwargs: Any) -> ScalixConfig:
    global _config
    values: dict[str, Any] = {}
    env_mapping = {
        "SCALIX_API_KEY": "api_key",
        "SCALIX_BASE_URL": "base_url",
    }
    for env_var, config_key in env_mapping.items():
        env_value = os.environ.get(env_var)
        if env_value is not None:
            values[config_key] = env_value
    for key, value in kwargs.items():
        if value is not None:
            values[key] = value
    _config = ScalixConfig(**values)
    return _config


def get_config() -> ScalixConfig:
    global _config
    if _config is None:
        _config = configure()
    return _config
