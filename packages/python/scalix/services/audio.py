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
        self, text: str, *, voice: str | None = None, format: str | None = None
    ) -> dict[str, Any]:
        body: dict[str, Any] = {"text": text}
        if voice:
            body["voice"] = voice
        if format:
            body["format"] = format
        return await self._request("POST", "/v1/audio/speak/kokoro", json=body)

    async def voices(self) -> dict[str, Any]:
        return await self._request("GET", "/v1/audio/kokoro/voices")

    async def languages(self) -> dict[str, Any]:
        return await self._request("GET", "/v1/audio/kokoro/languages")
