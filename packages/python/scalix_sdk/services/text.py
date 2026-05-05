"""Text utilities — sentiment, summarization, translation, grammar, autocomplete, vector search."""

from __future__ import annotations

from typing import Any

from scalix_sdk.services.base import BaseService


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

    async def grammar(self, text: str) -> dict[str, Any]:
        return await self._request("POST", "/v1/text/grammar", json={"text": text})

    async def autocomplete(
        self,
        text: str,
        *,
        max_completions: int | None = None,
    ) -> dict[str, Any]:
        body: dict[str, Any] = {"text": text}
        if max_completions is not None:
            body["max_completions"] = max_completions
        return await self._request("POST", "/v1/text/autocomplete", json=body)

    async def vector_search(
        self,
        query: str,
        context: list[dict[str, Any]],
        *,
        top_k: int | None = None,
        threshold: float | None = None,
    ) -> dict[str, Any]:
        body: dict[str, Any] = {"query": query, "context": context}
        if top_k is not None:
            body["top_k"] = top_k
        if threshold is not None:
            body["threshold"] = threshold
        return await self._request("POST", "/v1/text/vector-search", json=body)
