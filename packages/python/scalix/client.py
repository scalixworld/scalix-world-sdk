"""ScalixClient — unified access to all Scalix API services."""

from __future__ import annotations

from typing import Any

from scalix.config import configure, get_config
from scalix.services.account import AccountService
from scalix.services.audio import AudioService
from scalix.services.chat import ChatService
from scalix.services.database import DatabaseService
from scalix.services.docgen import DocGenService
from scalix.services.images import ImagesService
from scalix.services.rag import RAGService
from scalix.services.research import ResearchService
from scalix.services.storage import StorageService
from scalix.services.text import TextService


class ScalixClient:
    def __init__(self, api_key: str | None = None, **kwargs: Any) -> None:
        if api_key or kwargs:
            configure(api_key=api_key, **kwargs)
        config = get_config()
        self.account = AccountService(config)
        self.audio = AudioService(config)
        self.chat = ChatService(config)
        self.database = DatabaseService(config)
        self.docgen = DocGenService(config)
        self.images = ImagesService(config)
        self.rag = RAGService(config)
        self.research = ResearchService(config)
        self.storage = StorageService(config)
        self.text = TextService(config)

    def __repr__(self) -> str:
        return f"ScalixClient(base_url={self.account._config.base_url!r})"
