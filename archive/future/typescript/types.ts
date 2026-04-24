/**
 * Shared type definitions for the Scalix SDK.
 */

// --- Enums ---

export type Role = 'system' | 'user' | 'assistant' | 'tool';

export type StreamEventType =
  | 'text_delta'
  | 'tool_call_start'
  | 'tool_call_delta'
  | 'tool_call_end'
  | 'tool_result'
  | 'agent_thinking'
  | 'done'
  | 'error';

// --- Messages ---

export interface Message {
  role: Role;
  content: string;
  name?: string;
  toolCallId?: string;
  toolCalls?: ToolCall[];
}

export interface ToolCall {
  id: string;
  name: string;
  arguments: Record<string, unknown>;
}

// --- Scalix Models ---

export type ScalixModel =
  | 'scalix-world-ai'
  | 'scalix-advanced'
  | 'auto';

export const ScalixModels = {
  WorldAI: 'scalix-world-ai' as const,
  Advanced: 'scalix-advanced' as const,
  Auto: 'auto' as const,
} as const;

// --- Agent ---

export interface AgentOptions {
  model?: ScalixModel | string;
  instructions?: string;
  tools?: import('./tools/base.js').Tool[];
  memory?: boolean;
  maxTurns?: number;
  temperature?: number;
  timeout?: number;
}

// --- Results ---

export interface AgentResult {
  output: string;
  messages: Message[];
  toolCalls: ToolCallResult[];
  model?: string;
  usage?: Usage;
}

export interface ToolCallResult {
  toolName: string;
  arguments: Record<string, unknown>;
  result: unknown;
  durationMs?: number;
  error?: string;
}

export interface Usage {
  promptTokens: number;
  completionTokens: number;
  totalTokens: number;
}

export interface TeamResult {
  output: string;
  agentResults: Record<string, AgentResult>;
  workflowLog: string[];
}

// --- Streaming ---

export interface StreamEvent {
  type: StreamEventType;
  data?: string | Record<string, unknown>;
  toolName?: string;
  toolCallId?: string;
}

// --- Tool Definitions ---

export interface ToolDefinition {
  name: string;
  description: string;
  parameters: Record<string, unknown>;
}

// --- Provider Types ---

export interface ModelInfo {
  id: string;
  name: string;
  provider: string;
  contextWindow?: number;
  maxOutputTokens?: number;
  supportsTools: boolean;
  supportsStreaming: boolean;
}

export interface SandboxResult {
  stdout: string;
  stderr: string;
  exitCode: number;
  files: string[];
  durationMs?: number;
}
