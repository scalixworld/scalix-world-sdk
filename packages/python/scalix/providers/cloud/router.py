"""Scalix Router provider — wraps the existing scalix-router SDK.

Provides intelligent LLM routing, cost optimization, and model management.
This is a thin wrapper that delegates to the existing scalix-router package.

The scalix-router SDK is synchronous, so we wrap calls with asyncio.to_thread.
"""

from __future__ import annotations

import asyncio
import json
import logging
from typing import Any, AsyncIterator

from scalix.config import ScalixConfig, get_config
from scalix.exceptions import AuthenticationError, ProviderError
from scalix.providers.base import LLMProvider
from scalix.types import Message, Role, StreamEvent, StreamEventType, ToolCall

logger = logging.getLogger("scalix.providers.cloud.router")


class ScalixRouterProvider(LLMProvider):
    """Route LLM calls through Scalix Router for cost optimization.

    Wraps the existing `scalix-router` Python SDK.
    Requires a Scalix API key (cloud mode).

    Features over DirectLLM:
    - Intelligent model routing ("auto" uses Scalix's router to pick optimal model)
    - Cost optimization and usage tracking
    - Rate limit management and retry logic
    - Fine-tuned model access
    - Enterprise features (audit logs, tenancy)
    """

    def __init__(self, config: ScalixConfig | None = None) -> None:
        self._config = config or get_config()
        if not self._config.is_cloud_mode:
            raise AuthenticationError(
                "Scalix Router requires an API key. "
                "Call scalix.configure(api_key='...') first."
            )
        self._client: Any = None

    def _get_client(self) -> Any:
        """Lazy-init the scalix-router client."""
        if self._client is None:
            try:
                from scalix_router import ScalixRouter
            except ImportError:
                raise ProviderError(
                    "scalix-router package not installed. "
                    "Run: pip install scalix[cloud]"
                )

            self._client = ScalixRouter(
                api_key=self._config.api_key,
                base_url=self._config.base_url,
            )
        return self._client

    async def chat(
        self,
        messages: list[Message],
        model: str,
        tools: list[dict[str, Any]] | None = None,
        temperature: float = 0.7,
        stream: bool = False,
        **kwargs: Any,
    ) -> Message:
        """Send chat completion through Scalix Router.

        The Router handles model selection when model="auto",
        applies cost optimization, and manages rate limits.
        """
        client = self._get_client()

        # Convert messages to the format scalix-router expects
        router_messages = self._to_router_messages(messages)

        # Build request kwargs
        request_kwargs: dict[str, Any] = {
            "messages": router_messages,
            "model": model if model != "auto" else "auto",
            "temperature": temperature,
        }

        if tools:
            request_kwargs["tools"] = self._to_openai_tools(tools)

        max_tokens = kwargs.get("max_tokens")
        if max_tokens:
            request_kwargs["max_tokens"] = max_tokens

        # scalix-router is synchronous — run in thread pool
        logger.debug("Router request: model=%s, messages=%d", model, len(router_messages))
        response = await asyncio.to_thread(
            lambda: client.chat_completion(**request_kwargs)
        )

        # Parse the response (OpenAI-compatible format)
        choice = response.choices[0] if hasattr(response, "choices") else response

        # Extract tool calls if present
        tool_calls: list[ToolCall] | None = None
        message_obj = choice.message if hasattr(choice, "message") else choice

        if hasattr(message_obj, "tool_calls") and message_obj.tool_calls:
            tool_calls = [
                ToolCall(
                    id=tc.id,
                    name=tc.function.name,
                    arguments=(
                        json.loads(tc.function.arguments)
                        if isinstance(tc.function.arguments, str)
                        else tc.function.arguments
                    ),
                )
                for tc in message_obj.tool_calls
            ]

        content = ""
        if hasattr(message_obj, "content") and message_obj.content:
            content = message_obj.content

        return Message(
            role=Role.ASSISTANT,
            content=content,
            tool_calls=tool_calls,
        )

    async def stream_chat(
        self,
        messages: list[Message],
        model: str,
        tools: list[dict[str, Any]] | None = None,
        temperature: float = 0.7,
        **kwargs: Any,
    ) -> AsyncIterator[StreamEvent]:
        """Stream chat completion through Scalix Router."""
        client = self._get_client()

        router_messages = self._to_router_messages(messages)

        request_kwargs: dict[str, Any] = {
            "messages": router_messages,
            "model": model if model != "auto" else "auto",
            "temperature": temperature,
            "stream": True,
        }

        if tools:
            request_kwargs["tools"] = self._to_openai_tools(tools)

        max_tokens = kwargs.get("max_tokens")
        if max_tokens:
            request_kwargs["max_tokens"] = max_tokens

        # Consume sync streaming iterator in a thread, then yield events
        def collect_stream() -> list[Any]:
            chunks = []
            for chunk in client.chat_completion(**request_kwargs):
                chunks.append(chunk)
            return chunks

        chunks = await asyncio.to_thread(collect_stream)

        for chunk in chunks:
            choice = chunk.choices[0] if hasattr(chunk, "choices") else chunk
            delta = choice.delta if hasattr(choice, "delta") else choice
            if hasattr(delta, "content") and delta.content:
                yield StreamEvent(type=StreamEventType.TEXT_DELTA, data=delta.content)

        yield StreamEvent(type=StreamEventType.DONE)

    def _to_router_messages(self, messages: list[Message]) -> list[dict[str, Any]]:
        """Convert SDK messages to the format scalix-router expects."""
        result = []
        for msg in messages:
            entry: dict[str, Any] = {"role": msg.role.value, "content": msg.content}
            if msg.tool_call_id:
                entry["tool_call_id"] = msg.tool_call_id
            if msg.name:
                entry["name"] = msg.name
            if msg.tool_calls:
                entry["tool_calls"] = [
                    {
                        "id": tc.id,
                        "type": "function",
                        "function": {
                            "name": tc.name,
                            "arguments": json.dumps(tc.arguments),
                        },
                    }
                    for tc in msg.tool_calls
                ]
            result.append(entry)
        return result

    def _to_openai_tools(self, tools: list[dict[str, Any]]) -> list[dict[str, Any]]:
        """Convert tool definitions to OpenAI function calling format."""
        return [
            {
                "type": "function",
                "function": {
                    "name": tool["name"],
                    "description": tool.get("description", ""),
                    "parameters": tool.get("parameters", {}),
                },
            }
            for tool in tools
        ]
