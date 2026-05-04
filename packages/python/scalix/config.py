"""Scalix SDK configuration."""

from __future__ import annotations

from pydantic import BaseModel, Field


class ScalixConfig(BaseModel):
    api_key: str = Field(default="")
    base_url: str = Field(default="https://api.scalix.world")
    max_retries: int = Field(default=2)
    timeout: float = Field(default=60.0)
