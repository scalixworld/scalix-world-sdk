"""Direct LLM provider — calls OpenAI/Anthropic/Google APIs directly.

Used in local mode when no Scalix API key is configured.
The developer uses their own provider API keys.
"""

from __future__ import annotations

import json
import logging
from typing import Any, AsyncIterator

from scalix.config import ScalixConfig, get_config
from scalix.exceptions import ConfigurationError, ModelNotFoundError
from scalix.providers.base import LLMProvider
from scalix.types import Message, Role, StreamEvent, StreamEventType, ToolCall

logger = logging.getLogger("scalix.providers.direct_llm")


class DirectLLM(LLMProvider):
    """Direct LLM API calls using the developer's own API keys.

    Supports OpenAI, Anthropic, Google, and Ollama.
    No Scalix infrastructure involved — zero cost to Scalix.
    """

    def __init__(self, config: ScalixConfig | None = None) -> None:
        self._config = config or get_config()
        self._openai_client: Any = None
        self._anthropic_client: Any = None

    async def chat(
        self,
        messages: list[Message],
        model: str,
        tools: list[dict[str, Any]] | None = None,
        temperature: float = 0.7,
        stream: bool = False,
        **kwargs: Any,
    ) -> Message:
        """Route to the appropriate provider based on model name."""
        provider = self._detect_provider(model)

        if provider == "openai":
            return await self._call_openai(messages, model, tools, temperature, **kwargs)
        elif provider == "anthropic":
            return await self._call_anthropic(messages, model, tools, temperature, **kwargs)
        elif provider == "google":
            return await self._call_google(messages, model, tools, temperature, **kwargs)
        elif provider == "ollama":
            return await self._call_ollama(messages, model, tools, temperature, **kwargs)
        else:
            raise ConfigurationError(
                f"Cannot determine provider for model '{model}'. "
                "Set OPENAI_API_KEY, ANTHROPIC_API_KEY, or GOOGLE_API_KEY."
            )

    async def stream_chat(
        self,
        messages: list[Message],
        model: str,
        tools: list[dict[str, Any]] | None = None,
        temperature: float = 0.7,
        **kwargs: Any,
    ) -> AsyncIterator[StreamEvent]:
        """Stream responses from the appropriate provider."""
        provider = self._detect_provider(model)

        if provider == "openai":
            async for event in self._stream_openai(messages, model, tools, temperature, **kwargs):
                yield event
        elif provider == "anthropic":
            async for event in self._stream_anthropic(
                messages, model, tools, temperature, **kwargs
            ):
                yield event
        else:
            raise ConfigurationError(f"Streaming not yet supported for provider '{provider}'")

    def _detect_provider(self, model: str) -> str:
        """Detect which provider a model belongs to."""
        model_lower = model.lower()

        if any(m in model_lower for m in ["gpt", "o1", "o3", "o4"]):
            return "openai"
        elif any(m in model_lower for m in ["claude", "haiku", "sonnet", "opus"]):
            return "anthropic"
        elif any(m in model_lower for m in ["gemini", "palm"]):
            return "google"
        elif self._config.ollama_host:
            return "ollama"
        elif model == "auto":
            # Auto-select based on available keys
            if self._config.anthropic_api_key:
                return "anthropic"
            elif self._config.openai_api_key:
                return "openai"
            elif self._config.google_api_key:
                return "google"
        elif self._config.openai_api_key:
            return "openai"
        elif self._config.anthropic_api_key:
            return "anthropic"
        elif self._config.google_api_key:
            return "google"

        raise ConfigurationError(
            "No LLM provider configured. Set one of: "
            "OPENAI_API_KEY, ANTHROPIC_API_KEY, GOOGLE_API_KEY, or OLLAMA_HOST"
        )

    def _resolve_model(self, model: str, provider: str) -> str:
        """Resolve 'auto' model to a concrete model name."""
        if model != "auto":
            return model

        defaults = {
            "openai": "gpt-4o",
            "anthropic": "claude-sonnet-4-20250514",
            "google": "gemini-2.5-flash",
            "ollama": "llama3.2",
        }
        return defaults.get(provider, model)

    # --- OpenAI ---

    def _get_openai_client(self) -> Any:
        if self._openai_client is None:
            try:
                from openai import AsyncOpenAI
            except ImportError:
                raise ConfigurationError(
                    "OpenAI package not installed. Run: pip install scalix[openai]"
                )
            kwargs: dict[str, Any] = {"api_key": self._config.openai_api_key}
            if self._config.openai_base_url:
                kwargs["base_url"] = self._config.openai_base_url
            self._openai_client = AsyncOpenAI(**kwargs)
        return self._openai_client

    async def _call_openai(
        self,
        messages: list[Message],
        model: str,
        tools: list[dict[str, Any]] | None,
        temperature: float,
        **kwargs: Any,
    ) -> Message:
        client = self._get_openai_client()
        model = self._resolve_model(model, "openai")

        openai_messages = self._to_openai_messages(messages)
        openai_tools = self._to_openai_tools(tools) if tools else None

        request: dict[str, Any] = {
            "model": model,
            "messages": openai_messages,
            "temperature": temperature,
        }
        if openai_tools:
            request["tools"] = openai_tools

        logger.debug("OpenAI request: model=%s, messages=%d", model, len(openai_messages))
        response = await client.chat.completions.create(**request)
        choice = response.choices[0]

        # Extract tool calls if present
        tool_calls: list[ToolCall] | None = None
        if choice.message.tool_calls:
            tool_calls = [
                ToolCall(
                    id=tc.id,
                    name=tc.function.name,
                    arguments=json.loads(tc.function.arguments),
                )
                for tc in choice.message.tool_calls
            ]

        return Message(
            role=Role.ASSISTANT,
            content=choice.message.content or "",
            tool_calls=tool_calls,
        )

    async def _stream_openai(
        self,
        messages: list[Message],
        model: str,
        tools: list[dict[str, Any]] | None,
        temperature: float,
        **kwargs: Any,
    ) -> AsyncIterator[StreamEvent]:
        client = self._get_openai_client()
        model = self._resolve_model(model, "openai")

        request: dict[str, Any] = {
            "model": model,
            "messages": self._to_openai_messages(messages),
            "temperature": temperature,
            "stream": True,
        }
        if tools:
            request["tools"] = self._to_openai_tools(tools)

        stream = await client.chat.completions.create(**request)
        async for chunk in stream:
            delta = chunk.choices[0].delta if chunk.choices else None
            if delta and delta.content:
                yield StreamEvent(type=StreamEventType.TEXT_DELTA, data=delta.content)

        yield StreamEvent(type=StreamEventType.DONE)

    def _to_openai_messages(self, messages: list[Message]) -> list[dict[str, Any]]:
        result = []
        for msg in messages:
            entry: dict[str, Any] = {"role": msg.role.value, "content": msg.content}
            if msg.tool_call_id:
                entry["tool_call_id"] = msg.tool_call_id
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
            if msg.name:
                entry["name"] = msg.name
            result.append(entry)
        return result

    def _to_openai_tools(self, tools: list[dict[str, Any]]) -> list[dict[str, Any]]:
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

    # --- Anthropic ---

    def _get_anthropic_client(self) -> Any:
        if self._anthropic_client is None:
            try:
                from anthropic import AsyncAnthropic
            except ImportError:
                raise ConfigurationError(
                    "Anthropic package not installed. Run: pip install scalix[anthropic]"
                )
            kwargs: dict[str, Any] = {"api_key": self._config.anthropic_api_key}
            if self._config.anthropic_base_url:
                kwargs["base_url"] = self._config.anthropic_base_url
            self._anthropic_client = AsyncAnthropic(**kwargs)
        return self._anthropic_client

    async def _call_anthropic(
        self,
        messages: list[Message],
        model: str,
        tools: list[dict[str, Any]] | None,
        temperature: float,
        **kwargs: Any,
    ) -> Message:
        client = self._get_anthropic_client()
        model = self._resolve_model(model, "anthropic")

        system_prompt, anthropic_messages = self._to_anthropic_messages(messages)
        anthropic_tools = self._to_anthropic_tools(tools) if tools else None

        request: dict[str, Any] = {
            "model": model,
            "messages": anthropic_messages,
            "max_tokens": kwargs.get("max_tokens", 4096),
            "temperature": temperature,
        }
        if system_prompt:
            request["system"] = system_prompt
        if anthropic_tools:
            request["tools"] = anthropic_tools

        logger.debug("Anthropic request: model=%s, messages=%d", model, len(anthropic_messages))
        response = await client.messages.create(**request)

        # Parse response — may contain text and/or tool_use blocks
        content_text = ""
        tool_calls: list[ToolCall] = []

        for block in response.content:
            if block.type == "text":
                content_text += block.text
            elif block.type == "tool_use":
                tool_calls.append(
                    ToolCall(
                        id=block.id,
                        name=block.name,
                        arguments=block.input if isinstance(block.input, dict) else {},
                    )
                )

        return Message(
            role=Role.ASSISTANT,
            content=content_text,
            tool_calls=tool_calls if tool_calls else None,
        )

    async def _stream_anthropic(
        self,
        messages: list[Message],
        model: str,
        tools: list[dict[str, Any]] | None,
        temperature: float,
        **kwargs: Any,
    ) -> AsyncIterator[StreamEvent]:
        client = self._get_anthropic_client()
        model = self._resolve_model(model, "anthropic")

        system_prompt, anthropic_messages = self._to_anthropic_messages(messages)

        request: dict[str, Any] = {
            "model": model,
            "messages": anthropic_messages,
            "max_tokens": kwargs.get("max_tokens", 4096),
            "temperature": temperature,
        }
        if system_prompt:
            request["system"] = system_prompt
        if tools:
            request["tools"] = self._to_anthropic_tools(tools)

        async with client.messages.stream(**request) as stream:
            async for text in stream.text_stream:
                yield StreamEvent(type=StreamEventType.TEXT_DELTA, data=text)

        yield StreamEvent(type=StreamEventType.DONE)

    def _to_anthropic_messages(
        self, messages: list[Message]
    ) -> tuple[str, list[dict[str, Any]]]:
        """Convert to Anthropic format. Extract system prompt separately."""
        system_prompt = ""
        anthropic_messages: list[dict[str, Any]] = []

        for msg in messages:
            if msg.role == Role.SYSTEM:
                system_prompt = msg.content
                continue

            if msg.role == Role.TOOL:
                anthropic_messages.append(
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "tool_result",
                                "tool_use_id": msg.tool_call_id,
                                "content": msg.content,
                            }
                        ],
                    }
                )
            elif msg.role == Role.ASSISTANT and msg.tool_calls:
                content: list[dict[str, Any]] = []
                if msg.content:
                    content.append({"type": "text", "text": msg.content})
                for tc in msg.tool_calls:
                    content.append(
                        {
                            "type": "tool_use",
                            "id": tc.id,
                            "name": tc.name,
                            "input": tc.arguments,
                        }
                    )
                anthropic_messages.append({"role": "assistant", "content": content})
            else:
                anthropic_messages.append(
                    {"role": msg.role.value, "content": msg.content}
                )

        return system_prompt, anthropic_messages

    def _to_anthropic_tools(self, tools: list[dict[str, Any]]) -> list[dict[str, Any]]:
        return [
            {
                "name": tool["name"],
                "description": tool.get("description", ""),
                "input_schema": tool.get("parameters", {"type": "object", "properties": {}}),
            }
            for tool in tools
        ]

    # --- Google ---

    async def _call_google(
        self,
        messages: list[Message],
        model: str,
        tools: list[dict[str, Any]] | None,
        temperature: float,
        **kwargs: Any,
    ) -> Message:
        """Call Google Generative AI API."""
        try:
            import google.generativeai as genai
        except ImportError:
            raise ConfigurationError(
                "Google AI package not installed. Run: pip install scalix[google]"
            )

        genai.configure(api_key=self._config.google_api_key)
        model_name = self._resolve_model(model, "google")
        gen_model = genai.GenerativeModel(model_name)

        # Build simple prompt from messages
        prompt_parts = []
        for msg in messages:
            prefix = {"system": "System: ", "user": "", "assistant": "Assistant: ", "tool": "Tool result: "}
            prompt_parts.append(f"{prefix.get(msg.role.value, '')}{msg.content}")

        response = await gen_model.generate_content_async(
            "\n\n".join(prompt_parts),
            generation_config={"temperature": temperature},
        )

        return Message(role=Role.ASSISTANT, content=response.text or "")

    # --- Ollama ---

    async def _call_ollama(
        self,
        messages: list[Message],
        model: str,
        tools: list[dict[str, Any]] | None,
        temperature: float,
        **kwargs: Any,
    ) -> Message:
        """Call local Ollama instance via OpenAI-compatible API."""
        try:
            from openai import AsyncOpenAI
        except ImportError:
            raise ConfigurationError(
                "OpenAI package needed for Ollama compatibility. Run: pip install scalix[openai]"
            )

        host = self._config.ollama_host or "http://localhost:11434"
        client = AsyncOpenAI(base_url=f"{host}/v1", api_key="ollama")
        model = self._resolve_model(model, "ollama")

        response = await client.chat.completions.create(
            model=model,
            messages=self._to_openai_messages(messages),
            temperature=temperature,
        )

        choice = response.choices[0]
        return Message(role=Role.ASSISTANT, content=choice.message.content or "")
