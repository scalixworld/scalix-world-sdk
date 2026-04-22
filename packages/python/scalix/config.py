"""Scalix SDK configuration management.

Configuration priority (lowest to highest):
1. Defaults (local mode)
2. Config file (~/.scalix/config.json or scalix.config.json)
3. Environment variables
4. Programmatic via scalix.configure()
"""

from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Any

from pydantic import BaseModel, Field


class ScalixConfig(BaseModel):
    """SDK configuration."""

    # Authentication
    api_key: str | None = Field(default=None, description="Scalix API key for cloud mode")
    project_id: str | None = Field(default=None, description="Scalix project identifier")

    # Environment
    environment: str = Field(default="development", description="development | staging | production")
    base_url: str = Field(default="https://api.scalix.world", description="Scalix API base URL")

    # Logging
    log_level: str = Field(default="info", description="debug | info | warn | error")

    # Provider preferences
    default_model: str = Field(default="auto", description="Default LLM model")
    sandbox_mode: str = Field(
        default="auto", description="auto | docker | subprocess | cloud"
    )
    database_mode: str = Field(default="auto", description="auto | sqlite | cloud")

    # LLM provider keys and endpoints (for local/BYOK mode)
    openai_api_key: str | None = Field(default=None)
    openai_base_url: str | None = Field(default=None, description="Override OpenAI API base URL")
    anthropic_api_key: str | None = Field(default=None)
    anthropic_base_url: str | None = Field(default=None, description="Override Anthropic API base URL")
    google_api_key: str | None = Field(default=None)
    google_base_url: str | None = Field(default=None, description="Override Google AI base URL")
    ollama_host: str | None = Field(default=None)
    search_base_url: str | None = Field(default=None, description="Override search endpoint")

    @property
    def is_cloud_mode(self) -> bool:
        """Check if SDK is configured for cloud mode (Scalix infrastructure)."""
        return self.api_key is not None

    @property
    def is_local_mode(self) -> bool:
        """Check if SDK is running in local mode."""
        return self.api_key is None


# Global configuration singleton
_config: ScalixConfig | None = None


def configure(**kwargs: Any) -> ScalixConfig:
    """Configure the Scalix SDK.

    Call this once at the start of your application to set up
    cloud mode or override defaults.

    Args:
        api_key: Scalix API key (enables cloud mode)
        project_id: Scalix project identifier
        environment: "development", "staging", or "production"
        base_url: Scalix API base URL
        log_level: "debug", "info", "warn", or "error"
        default_model: Default LLM model name or "auto"
        sandbox_mode: "auto", "docker", "subprocess", or "cloud"
        database_mode: "auto", "sqlite", or "cloud"

    Returns:
        The updated ScalixConfig instance.

    Example:
        import scalix
        scalix.configure(api_key="sk-scalix-...")
    """
    global _config
    _config = _load_config(**kwargs)
    return _config


def get_config() -> ScalixConfig:
    """Get current SDK configuration. Initializes with defaults if not configured."""
    global _config
    if _config is None:
        _config = _load_config()
    return _config


def _load_config(**overrides: Any) -> ScalixConfig:
    """Load configuration from all sources with proper priority."""
    # 1. Start with defaults
    values: dict[str, Any] = {}

    # 2. Load from config file
    config_file = _find_config_file()
    if config_file:
        with open(config_file) as f:
            file_values = json.load(f)
            values.update(file_values)

    # 3. Load from environment variables
    env_mapping = {
        "SCALIX_API_KEY": "api_key",
        "SCALIX_PROJECT_ID": "project_id",
        "SCALIX_ENVIRONMENT": "environment",
        "SCALIX_BASE_URL": "base_url",
        "SCALIX_LOG_LEVEL": "log_level",
        "SCALIX_DEFAULT_MODEL": "default_model",
        "SCALIX_SANDBOX_MODE": "sandbox_mode",
        "SCALIX_DATABASE_MODE": "database_mode",
        "OPENAI_API_KEY": "openai_api_key",
        "OPENAI_BASE_URL": "openai_base_url",
        "ANTHROPIC_API_KEY": "anthropic_api_key",
        "ANTHROPIC_BASE_URL": "anthropic_base_url",
        "GOOGLE_API_KEY": "google_api_key",
        "GOOGLE_BASE_URL": "google_base_url",
        "OLLAMA_HOST": "ollama_host",
        "SCALIX_SEARCH_URL": "search_base_url",
    }

    for env_var, config_key in env_mapping.items():
        env_value = os.environ.get(env_var)
        if env_value is not None:
            values[config_key] = env_value

    # 4. Apply programmatic overrides (highest priority)
    for key, value in overrides.items():
        if value is not None:
            values[key] = value

    return ScalixConfig(**values)


def _find_config_file() -> Path | None:
    """Find the nearest config file."""
    # Check project-local config first
    local_config = Path("scalix.config.json")
    if local_config.exists():
        return local_config

    # Check home directory
    home_config = Path.home() / ".scalix" / "config.json"
    if home_config.exists():
        return home_config

    return None
