"""Chat completion service — LLM inference."""

from __future__ import annotations

from typing import Any, AsyncIterator

from scalix.services.base import BaseService


class ChatService(BaseService):
    async def complete(
        self,
        messages: list[dict[str, str]],
        model: str = "scalix-world-ai",
        *,
        temperature: float | None = None,
        max_tokens: int | None = None,
        top_p: float | None = None,
    ) -> dict[str, Any]:
        body: dict[str, Any] = {"model": model, "messages": messages, "stream": False}
        if temperature is not None:
            body["temperature"] = temperature
        if max_tokens is not None:
            body["max_tokens"] = max_tokens
        if top_p is not None:
            body["top_p"] = top_p
        return await self._request("POST", "/v1/chat/completions", json=body)

    async def stream(
        self,
        messages: list[dict[str, str]],
        model: str = "scalix-world-ai",
        *,
        temperature: float | None = None,
        max_tokens: int | None = None,
    ) -> AsyncIterator[str]:
        import httpx

        body: dict[str, Any] = {"model": model, "messages": messages, "stream": True}
        if temperature is not None:
            body["temperature"] = temperature
        if max_tokens is not None:
            body["max_tokens"] = max_tokens

        url = f"{self._config.base_url}/v1/chat/completions"
        headers = {
            "Authorization": f"Bearer {self._config.api_key}",
            "Content-Type": "application/json",
        }

        async with httpx.AsyncClient(timeout=120.0) as client:
            async with client.stream("POST", url, headers=headers, json=body) as resp:
                async for line in resp.aiter_lines():
                    if not line.startswith("data: "):
                        continue
                    payload = line[6:]
                    if payload == "[DONE]":
                        return
                    try:
                        import json
                        parsed = json.loads(payload)
                        content = parsed.get("choices", [{}])[0].get("delta", {}).get("content")
                        if content:
                            yield content
                    except Exception:
                        continue

    async def models(self) -> list[dict[str, Any]]:
        data = await self._request("GET", "/v1/models")
        return data.get("data", [])
