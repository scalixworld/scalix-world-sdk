import { BaseService } from './base.js';

export interface ChatMessage {
  role: 'user' | 'assistant' | 'system';
  content: string;
}

export interface ChatCompletionOptions {
  model: string;
  messages: ChatMessage[];
  stream?: boolean;
  temperature?: number;
  max_tokens?: number;
  top_p?: number;
}

export interface ChatCompletionResult {
  id: string;
  object: string;
  created: number;
  model: string;
  choices: Array<{
    index: number;
    message: ChatMessage;
    finish_reason: string;
  }>;
  usage: {
    prompt_tokens: number;
    completion_tokens: number;
    total_tokens: number;
  };
}

export class ChatService extends BaseService {
  async complete(options: ChatCompletionOptions): Promise<ChatCompletionResult> {
    return this.request<ChatCompletionResult>('POST', '/v1/chat/completions', {
      body: { ...options, stream: false },
    });
  }

  async *stream(options: Omit<ChatCompletionOptions, 'stream'>): AsyncGenerator<string> {
    const resp = await this.requestRaw('POST', '/v1/chat/completions', {
      body: { ...options, stream: true },
    });

    const reader = resp.body?.getReader();
    if (!reader) return;

    const decoder = new TextDecoder();
    let buffer = '';

    try {
      while (true) {
        const { done, value } = await reader.read();
        if (done) break;

        buffer += decoder.decode(value, { stream: true });
        const lines = buffer.split('\n');
        buffer = lines.pop() ?? '';

        for (const line of lines) {
          const trimmed = line.trim();
          if (!trimmed || !trimmed.startsWith('data: ')) continue;
          const payload = trimmed.slice(6);
          if (payload === '[DONE]') return;
          try {
            const parsed = JSON.parse(payload) as {
              choices?: Array<{ delta?: { content?: string } }>;
            };
            const content = parsed.choices?.[0]?.delta?.content;
            if (content) yield content;
          } catch {
            // skip malformed chunks
          }
        }
      }
    } finally {
      reader.releaseLock();
    }
  }

  async models(): Promise<Array<{ id: string; name: string }>> {
    const resp = await this.request<{ data: Array<{ id: string; name: string }> }>('GET', '/v1/models');
    return resp.data;
  }
}
