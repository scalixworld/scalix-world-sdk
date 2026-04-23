"""ScalixClient — unified access to all Scalix API services.

Example:
    from scalix import ScalixClient

    scalix = ScalixClient(api_key="sk-scalix-...")

    results = await scalix.research.search("quantum computing")
    image = await scalix.images.generate("A sunset over mountains")
    transcript = await scalix.audio.transcribe(audio_file)
"""

from __future__ import annotations

from typing import Any

from scalix.config import configure, get_config
from scalix.services.audio import AudioService
from scalix.services.images import ImagesService
from scalix.services.research import ResearchService


class ScalixClient:
    def __init__(self, api_key: str | None = None, **kwargs: Any) -> None:
        if api_key or kwargs:
            configure(api_key=api_key, **kwargs)
        config = get_config()
        self.audio = AudioService(config)
        self.images = ImagesService(config)
        self.research = ResearchService(config)

    def __repr__(self) -> str:
        return f"ScalixClient(base_url={self.research._config.base_url!r})"
