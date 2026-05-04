"""Scalix — unified client for the Scalix platform.

Chat completions delegate to the OpenAI SDK (Scalix's API is OpenAI-compatible).
Platform services (research, RAG, database, etc.) use a native HTTP client.
"""

from __future__ import annotations

import warnings
from typing import Any

from openai import OpenAI

from scalix.config import ScalixConfig
from scalix.services.account import AccountService
from scalix.services.audio import AudioService
from scalix.services.docgen import DocGenService
from scalix.services.images import ImagesService
from scalix.services.models import ModelsService
from scalix.services.rag import RAGService
from scalix.services.research import ResearchService
from scalix.services.storage import StorageService
from scalix.services.text import TextService


class Scalix:
    """Unified client for the Scalix platform.

    ``scalix.completions`` gives full OpenAI-compatible chat (tools, vision, streaming).
    The rest of the client gives access to Scalix-only platform services.
    """

    def __init__(
        self,
        api_key: str,
        *,
        base_url: str = "https://api.scalix.world",
        max_retries: int = 2,
        timeout: float = 60.0,
    ) -> None:
        openai_base = f"{base_url}/v1" if not base_url.endswith("/v1") else base_url
        base = base_url.removesuffix("/v1").rstrip("/")
        config = ScalixConfig(api_key=api_key, base_url=base, max_retries=max_retries, timeout=timeout)

        self.openai = OpenAI(
            base_url=openai_base,
            api_key=api_key,
            default_headers={"User-Agent": "Scalix-SDK/2.0"},
        )
        self.completions = self.openai.chat.completions

        self.account = AccountService(config)
        self.audio = AudioService(config)
        self.docgen = DocGenService(config)
        self.images = ImagesService(config)
        self.models = ModelsService(config)
        self.rag = RAGService(config)
        self.research = ResearchService(config)
        self.storage = StorageService(config)
        self.text = TextService(config)

    def __repr__(self) -> str:
        return f"Scalix(base_url={self.account._config.base_url!r})"


def ScalixClient(api_key: str | None = None, **kwargs: Any) -> Scalix:
    """Deprecated: Use ``Scalix`` instead."""
    warnings.warn("ScalixClient is deprecated, use Scalix instead", DeprecationWarning, stacklevel=2)
    if api_key is None:
        raise ValueError("api_key is required")
    return Scalix(api_key, **kwargs)
