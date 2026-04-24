"""Shared type definitions for the Scalix SDK."""

from __future__ import annotations

from enum import Enum
from typing import Any

from pydantic import BaseModel, Field


# --- Enums ---


class Role(str, Enum):
    """Message roles in a conversation."""

    SYSTEM = "system"
    USER = "user"
    ASSISTANT = "assistant"
    TOOL = "tool"


class StreamEventType(str, Enum):
    """Types of events emitted during streaming."""

    TEXT_DELTA = "text_delta"
    TOOL_CALL_START = "tool_call_start"
    TOOL_CALL_DELTA = "tool_call_delta"
    TOOL_CALL_END = "tool_call_end"
    TOOL_RESULT = "tool_result"
    AGENT_THINKING = "agent_thinking"
    DONE = "done"
    ERROR = "error"


# --- Messages ---


class Message(BaseModel):
    """A message in an agent conversation."""

    role: Role
    content: str
    name: str | None = None
    tool_call_id: str | None = None
    tool_calls: list[ToolCall] | None = None


class ToolCall(BaseModel):
    """A tool call requested by the LLM."""

    id: str
    name: str
    arguments: dict[str, Any]


# --- Results ---


class AgentResult(BaseModel):
    """Result of an agent execution."""

    output: str
    messages: list[Message] = Field(default_factory=list)
    tool_calls: list[ToolCallResult] = Field(default_factory=list)
    model: str | None = None
    usage: Usage | None = None


class ToolCallResult(BaseModel):
    """Result of a single tool execution."""

    tool_name: str
    arguments: dict[str, Any]
    result: Any
    duration_ms: float | None = None
    error: str | None = None


class Usage(BaseModel):
    """Token usage information."""

    prompt_tokens: int = 0
    completion_tokens: int = 0
    total_tokens: int = 0


class TeamResult(BaseModel):
    """Result of a multi-agent team execution."""

    output: str
    agent_results: dict[str, AgentResult] = Field(default_factory=dict)
    workflow_log: list[str] = Field(default_factory=list)


# --- Streaming ---


class StreamEvent(BaseModel):
    """An event emitted during streaming agent execution."""

    type: StreamEventType
    data: str | dict[str, Any] | None = None
    tool_name: str | None = None
    tool_call_id: str | None = None


# --- Tool Definitions ---


class ToolDefinition(BaseModel):
    """Schema for a tool that an agent can use."""

    name: str
    description: str
    parameters: dict[str, Any] = Field(default_factory=dict)


# --- Provider Types ---


class ModelInfo(BaseModel):
    """Information about an available LLM model."""

    id: str
    name: str
    provider: str
    context_window: int | None = None
    max_output_tokens: int | None = None
    supports_tools: bool = True
    supports_streaming: bool = True


class SandboxResult(BaseModel):
    """Result of code execution in a sandbox."""

    stdout: str = ""
    stderr: str = ""
    exit_code: int = 0
    files: list[str] = Field(default_factory=list)
    duration_ms: float | None = None
