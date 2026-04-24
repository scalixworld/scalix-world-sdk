"""Audio service — transcription and text-to-speech."""

from __future__ import annotations

from typing import Any, BinaryIO

from scalix.services.base import BaseService


class AudioService(BaseService):
    async def transcribe(
        self, file: BinaryIO, *, language: str | None = None
    ) -> dict[str, Any]:
        files = {"file": file}
        data = {"language": language} if language else None
        return await self._request_multipart("/v1/audio/transcribe", files=files, data=data)

    async def speak(
        self, text: str, *, voice: str | None = None, language: str = "en", speed: float = 1.0
    ) -> dict[str, Any]:
        params: dict[str, Any] = {"text": text, "language": language, "speed": speed}
        if voice:
            params["voice"] = voice
        audio_bytes = await self._request_binary("POST", "/v1/audio/speak/kokoro", params=params)
        return {
            "audio": audio_bytes,
            "size_bytes": len(audio_bytes),
            "format": "wav",
            "text": text,
        }

    async def voices(self) -> dict[str, Any]:
        return await self._request("GET", "/v1/audio/kokoro/voices")

    async def languages(self) -> dict[str, Any]:
        return await self._request("GET", "/v1/audio/kokoro/languages")
