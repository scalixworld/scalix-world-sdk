"""Text utilities — sentiment, summarization, translation."""

from __future__ import annotations

from typing import Any

from scalix.services.base import BaseService


class TextService(BaseService):
    async def sentiment(self, text: str) -> dict[str, Any]:
        return await self._request("POST", "/v1/text/sentiment", json={"text": text})

    async def summarize(
        self,
        text: str,
        *,
        length: str | None = None,
        style: str | None = None,
    ) -> dict[str, Any]:
        body: dict[str, Any] = {"text": text}
        if length:
            body["length"] = length
        if style:
            body["style"] = style
        return await self._request("POST", "/v1/text/summarize", json=body)

    async def translate(
        self,
        text: str,
        target_language: str,
        *,
        source_language: str | None = None,
    ) -> dict[str, Any]:
        body: dict[str, Any] = {"text": text, "target_language": target_language}
        if source_language:
            body["source_language"] = source_language
        return await self._request("POST", "/v1/text/translate", json=body)
