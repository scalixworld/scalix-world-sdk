/**
 * Scalix Router provider — calls the Scalix Router API for LLM routing.
 *
 * Provides intelligent model routing, cost optimization, and usage tracking.
 * Uses native fetch to call the OpenAI-compatible Router API.
 */

import { getConfig, isCloudMode, type ScalixConfig } from '../../config.js';
import { AuthenticationError, RouterError } from '../../errors.js';
import type { LLMProvider } from '../base.js';
import type { Message, StreamEvent, ToolCall } from '../../types.js';

/**
 * Route LLM calls through Scalix Router for cost optimization.
 *
 * Calls the Scalix Router API at /v1/chat/completions (OpenAI-compatible).
 * Requires a Scalix API key (cloud mode).
 *
 * Features over DirectLLM:
 * - Intelligent model routing ("auto" uses Scalix's router to pick optimal model)
 * - Cost optimization and usage tracking
 * - Rate limit management and retry logic
 * - Fine-tuned model access
 * - Enterprise features (audit logs, tenancy)
 */
export class ScalixRouterProvider implements LLMProvider {
  private config: ScalixConfig;

  constructor(config?: ScalixConfig) {
    this.config = config ?? getConfig();
    if (!isCloudMode()) {
      throw new AuthenticationError(
        "Scalix Router requires an API key. Call configure({ apiKey: 'sk-scalix-...' }) first.",
      );
    }
  }

  async chat(
    messages: Message[],
    model: string,
    options?: {
      tools?: Record<string, unknown>[];
      temperature?: number;
      stream?: boolean;
    },
  ): Promise<Message> {
    const temperature = options?.temperature ?? 0.7;
    const tools = options?.tools;

    const body: Record<string, unknown> = {
      model: model === 'auto' ? 'auto' : model,
      messages: this.toOpenAIMessages(messages),
      temperature,
    };

    if (tools?.length) {
      body.tools = this.toOpenAITools(tools);
    }

    const resp = await this.request('/v1/chat/completions', body);

    if (!resp.ok) {
      if (resp.status === 401) {
        throw new AuthenticationError('Invalid API key for Scalix Router');
      }
      const text = await resp.text();
      throw new RouterError(`Router request failed: ${resp.status} ${text}`);
    }

    const data = (await resp.json()) as {
      choices: Array<{
        message: {
          role: string;
          content: string | null;
          tool_calls?: Array<{
            id: string;
            function: { name: string; arguments: string };
          }>;
        };
      }>;
    };

    const choice = data.choices[0];

    let toolCalls: ToolCall[] | undefined;
    if (choice.message.tool_calls?.length) {
      toolCalls = choice.message.tool_calls.map((tc) => ({
        id: tc.id,
        name: tc.function.name,
        arguments: JSON.parse(tc.function.arguments) as Record<string, unknown>,
      }));
    }

    return {
      role: 'assistant',
      content: choice.message.content ?? '',
      toolCalls,
    };
  }

  async *streamChat(
    messages: Message[],
    model: string,
    options?: {
      tools?: Record<string, unknown>[];
      temperature?: number;
    },
  ): AsyncGenerator<StreamEvent> {
    const temperature = options?.temperature ?? 0.7;
    const tools = options?.tools;

    const body: Record<string, unknown> = {
      model: model === 'auto' ? 'auto' : model,
      messages: this.toOpenAIMessages(messages),
      temperature,
      stream: true,
    };

    if (tools?.length) {
      body.tools = this.toOpenAITools(tools);
    }

    const resp = await this.request('/v1/chat/completions', body);

    if (!resp.ok) {
      if (resp.status === 401) {
        throw new AuthenticationError('Invalid API key for Scalix Router');
      }
      const text = await resp.text();
      throw new RouterError(`Router stream request failed: ${resp.status} ${text}`);
    }

    if (!resp.body) {
      throw new RouterError('No response body for streaming request');
    }

    const reader = resp.body.getReader();
    const decoder = new TextDecoder();
    let buffer = '';

    try {
      while (true) {
        const { done, value } = await reader.read();
        if (done) break;

        buffer += decoder.decode(value, { stream: true });

        // Parse SSE lines
        const lines = buffer.split('\n');
        buffer = lines.pop() ?? '';

        for (const line of lines) {
          const trimmed = line.trim();
          if (!trimmed || !trimmed.startsWith('data: ')) continue;

          const payload = trimmed.slice(6);
          if (payload === '[DONE]') {
            yield { type: 'done' };
            return;
          }

          const chunk = JSON.parse(payload) as {
            choices: Array<{
              delta?: { content?: string };
              finish_reason?: string | null;
            }>;
          };

          const delta = chunk.choices[0]?.delta;
          if (delta?.content) {
            yield { type: 'text_delta', data: delta.content };
          }
        }
      }
    } finally {
      reader.releaseLock();
    }

    yield { type: 'done' };
  }

  private async request(path: string, body: Record<string, unknown>): Promise<Response> {
    const url = `${this.config.baseUrl}${path}`;
    return fetch(url, {
      method: 'POST',
      headers: {
        Authorization: `Bearer ${this.config.apiKey}`,
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(body),
    });
  }

  private toOpenAIMessages(messages: Message[]): Record<string, unknown>[] {
    return messages.map((msg) => {
      const entry: Record<string, unknown> = { role: msg.role, content: msg.content };
      if (msg.toolCallId) entry.tool_call_id = msg.toolCallId;
      if (msg.name) entry.name = msg.name;
      if (msg.toolCalls) {
        entry.tool_calls = msg.toolCalls.map((tc) => ({
          id: tc.id,
          type: 'function',
          function: { name: tc.name, arguments: JSON.stringify(tc.arguments) },
        }));
      }
      return entry;
    });
  }

  private toOpenAITools(tools: Record<string, unknown>[]): Record<string, unknown>[] {
    return tools.map((tool) => ({
      type: 'function',
      function: {
        name: tool.name,
        description: tool.description ?? '',
        parameters: tool.parameters ?? {},
      },
    }));
  }
}
