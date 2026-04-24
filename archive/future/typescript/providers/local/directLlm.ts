/**
 * Direct LLM provider — calls OpenAI/Anthropic APIs directly.
 *
 * Used in local mode when no Scalix API key is configured.
 * The developer uses their own provider API keys.
 */

import { getConfig, dynamicImport, type ScalixConfig } from '../../config.js';
import { ConfigurationError } from '../../errors.js';
import type { LLMProvider } from '../base.js';
import type { Message, StreamEvent, ToolCall } from '../../types.js';

type ProviderName = 'openai' | 'anthropic' | 'google' | 'ollama';

/**
 * Direct LLM API calls using the developer's own API keys.
 *
 * Supports OpenAI, Anthropic, Google, and Ollama.
 * No Scalix infrastructure involved — zero cost to Scalix.
 */
export class DirectLLM implements LLMProvider {
  private config: ScalixConfig;
  private openaiClient: unknown = null;
  private anthropicClient: unknown = null;

  constructor(config?: ScalixConfig) {
    this.config = config ?? getConfig();
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
    const provider = this.detectProvider(model);
    const temperature = options?.temperature ?? 0.7;
    const tools = options?.tools;

    switch (provider) {
      case 'openai':
        return this.callOpenAI(messages, model, tools, temperature);
      case 'anthropic':
        return this.callAnthropic(messages, model, tools, temperature);
      case 'google':
        return this.callGoogle(messages, model, temperature);
      case 'ollama':
        return this.callOllama(messages, model, temperature);
      default:
        throw new ConfigurationError(
          `Cannot determine provider for model '${model}'. ` +
            'Set OPENAI_API_KEY, ANTHROPIC_API_KEY, or GOOGLE_API_KEY.',
        );
    }
  }

  async *streamChat(
    messages: Message[],
    model: string,
    options?: {
      tools?: Record<string, unknown>[];
      temperature?: number;
    },
  ): AsyncGenerator<StreamEvent> {
    const provider = this.detectProvider(model);
    const temperature = options?.temperature ?? 0.7;

    if (provider === 'openai') {
      yield* this.streamOpenAI(messages, model, temperature);
    } else if (provider === 'anthropic') {
      yield* this.streamAnthropic(messages, model, temperature);
    } else {
      throw new ConfigurationError(`Streaming not yet supported for provider '${provider}'`);
    }
  }

  // --- Provider Detection ---

  private detectProvider(model: string): ProviderName {
    const m = model.toLowerCase();

    // Scalix-branded models require a Scalix API key (cloud mode).
    // In local mode, fall through to BYOK provider detection.
    if (m.startsWith('scalix-') || m === 'auto') {
      if (this.config.googleApiKey) return 'google';
      if (this.config.anthropicApiKey) return 'anthropic';
      if (this.config.openaiApiKey) return 'openai';
      if (this.config.ollamaHost) return 'ollama';

      throw new ConfigurationError(
        'Scalix models require a Scalix API key (cloud mode) or a local provider key. ' +
          'Call configure({ apiKey: "sk_scalix_..." }) or set SCALIX_API_KEY.',
      );
    }

    // BYOK: detect provider from raw model name
    if (['gpt', 'o1', 'o3', 'o4'].some((p) => m.includes(p))) return 'openai';
    if (['claude', 'haiku', 'sonnet', 'opus'].some((p) => m.includes(p))) return 'anthropic';
    if (['gemini', 'palm'].some((p) => m.includes(p))) return 'google';
    if (this.config.ollamaHost) return 'ollama';

    if (this.config.openaiApiKey) return 'openai';
    if (this.config.anthropicApiKey) return 'anthropic';
    if (this.config.googleApiKey) return 'google';

    throw new ConfigurationError(
      'No LLM provider configured. Set SCALIX_API_KEY for cloud mode, ' +
        'or set OPENAI_API_KEY, ANTHROPIC_API_KEY, GOOGLE_API_KEY, or OLLAMA_HOST for local mode.',
    );
  }

  private resolveModel(model: string, provider: ProviderName): string {
    // Map Scalix-branded names to actual provider models for local mode
    const scalixLocalDefaults: Record<string, Record<ProviderName, string>> = {
      'scalix-world-ai': {
        openai: 'gpt-4o-mini',
        anthropic: 'claude-haiku-4-5-20251001',
        google: 'gemini-2.5-flash-lite',
        ollama: 'llama3.2',
      },
      'scalix-advanced': {
        openai: 'gpt-4o',
        anthropic: 'claude-sonnet-4-20250514',
        google: 'gemini-2.5-pro',
        ollama: 'llama3.2',
      },
      'auto': {
        openai: 'gpt-4o-mini',
        anthropic: 'claude-haiku-4-5-20251001',
        google: 'gemini-2.5-flash-lite',
        ollama: 'llama3.2',
      },
    };

    const mapping = scalixLocalDefaults[model.toLowerCase()];
    if (mapping) return mapping[provider] ?? model;

    return model;
  }

  // --- OpenAI ---

  private async getOpenAIClient(): Promise<unknown> {
    if (!this.openaiClient) {
      try {
        const { OpenAI } = await dynamicImport('openai') as { OpenAI: new (opts: { apiKey?: string; baseURL?: string }) => unknown };
        this.openaiClient = new OpenAI({
          apiKey: this.config.openaiApiKey,
          ...(this.config.openaiBaseUrl && { baseURL: this.config.openaiBaseUrl }),
        });
      } catch {
        throw new ConfigurationError(
          'OpenAI package not installed. Run: npm install openai',
        );
      }
    }
    return this.openaiClient;
  }

  private async callOpenAI(
    messages: Message[],
    model: string,
    tools: Record<string, unknown>[] | undefined,
    temperature: number,
  ): Promise<Message> {
    const client = await this.getOpenAIClient() as {
      chat: {
        completions: {
          create: (req: Record<string, unknown>) => Promise<{
            choices: Array<{
              message: {
                content: string | null;
                tool_calls?: Array<{
                  id: string;
                  function: { name: string; arguments: string };
                }>;
              };
            }>;
          }>;
        };
      };
    };

    const resolvedModel = this.resolveModel(model, 'openai');
    const openaiMessages = this.toOpenAIMessages(messages);

    const request: Record<string, unknown> = {
      model: resolvedModel,
      messages: openaiMessages,
      temperature,
    };

    if (tools?.length) {
      request.tools = this.toOpenAITools(tools);
    }

    const response = await client.chat.completions.create(request);
    const choice = response.choices[0];

    let toolCalls: ToolCall[] | undefined;
    if (choice.message.tool_calls?.length) {
      toolCalls = choice.message.tool_calls.map((tc) => ({
        id: tc.id,
        name: tc.function.name,
        arguments: JSON.parse(tc.function.arguments),
      }));
    }

    return {
      role: 'assistant',
      content: choice.message.content ?? '',
      toolCalls,
    };
  }

  private async *streamOpenAI(
    messages: Message[],
    model: string,
    temperature: number,
  ): AsyncGenerator<StreamEvent> {
    const client = await this.getOpenAIClient() as {
      chat: {
        completions: {
          create: (req: Record<string, unknown>) => Promise<AsyncIterable<{
            choices: Array<{ delta?: { content?: string } }>;
          }>>;
        };
      };
    };

    const resolvedModel = this.resolveModel(model, 'openai');

    const stream = await client.chat.completions.create({
      model: resolvedModel,
      messages: this.toOpenAIMessages(messages),
      temperature,
      stream: true,
    });

    for await (const chunk of stream as AsyncIterable<{
      choices: Array<{ delta?: { content?: string } }>;
    }>) {
      const delta = chunk.choices[0]?.delta;
      if (delta?.content) {
        yield { type: 'text_delta', data: delta.content };
      }
    }

    yield { type: 'done' };
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

  // --- Anthropic ---

  private async getAnthropicClient(): Promise<unknown> {
    if (!this.anthropicClient) {
      try {
        const { default: Anthropic } = await dynamicImport('@anthropic-ai/sdk') as { default: new (opts: { apiKey?: string; baseURL?: string }) => unknown };
        this.anthropicClient = new Anthropic({
          apiKey: this.config.anthropicApiKey,
          ...(this.config.anthropicBaseUrl && { baseURL: this.config.anthropicBaseUrl }),
        });
      } catch {
        throw new ConfigurationError(
          'Anthropic package not installed. Run: npm install @anthropic-ai/sdk',
        );
      }
    }
    return this.anthropicClient;
  }

  private async callAnthropic(
    messages: Message[],
    model: string,
    tools: Record<string, unknown>[] | undefined,
    temperature: number,
  ): Promise<Message> {
    const client = await this.getAnthropicClient() as {
      messages: {
        create: (req: Record<string, unknown>) => Promise<{
          content: Array<
            | { type: 'text'; text: string }
            | { type: 'tool_use'; id: string; name: string; input: Record<string, unknown> }
          >;
        }>;
      };
    };

    const resolvedModel = this.resolveModel(model, 'anthropic');
    const { systemPrompt, messages: anthropicMessages } = this.toAnthropicMessages(messages);

    const request: Record<string, unknown> = {
      model: resolvedModel,
      messages: anthropicMessages,
      max_tokens: 4096,
      temperature,
    };

    if (systemPrompt) request.system = systemPrompt;
    if (tools?.length) request.tools = this.toAnthropicTools(tools);

    const response = await client.messages.create(request);

    let contentText = '';
    const toolCalls: ToolCall[] = [];

    for (const block of response.content) {
      if (block.type === 'text') {
        contentText += block.text;
      } else if (block.type === 'tool_use') {
        toolCalls.push({
          id: block.id,
          name: block.name,
          arguments: block.input,
        });
      }
    }

    return {
      role: 'assistant',
      content: contentText,
      toolCalls: toolCalls.length > 0 ? toolCalls : undefined,
    };
  }

  private async *streamAnthropic(
    messages: Message[],
    model: string,
    temperature: number,
  ): AsyncGenerator<StreamEvent> {
    const client = await this.getAnthropicClient() as {
      messages: {
        stream: (req: Record<string, unknown>) => {
          on: (event: string, cb: (e: { type: string; text?: string }) => void) => unknown;
          finalMessage: () => Promise<unknown>;
          [Symbol.asyncIterator](): AsyncIterator<{ type: string; delta?: { text?: string } }>;
        };
      };
    };

    const resolvedModel = this.resolveModel(model, 'anthropic');
    const { systemPrompt, messages: anthropicMessages } = this.toAnthropicMessages(messages);

    const request: Record<string, unknown> = {
      model: resolvedModel,
      messages: anthropicMessages,
      max_tokens: 4096,
      temperature,
    };

    if (systemPrompt) request.system = systemPrompt;

    const stream = client.messages.stream(request);

    for await (const event of stream) {
      if (event.type === 'content_block_delta' && event.delta?.text) {
        yield { type: 'text_delta', data: event.delta.text };
      }
    }

    yield { type: 'done' };
  }

  private toAnthropicMessages(messages: Message[]): {
    systemPrompt: string;
    messages: Record<string, unknown>[];
  } {
    let systemPrompt = '';
    const anthropicMessages: Record<string, unknown>[] = [];

    for (const msg of messages) {
      if (msg.role === 'system') {
        systemPrompt = msg.content;
        continue;
      }

      if (msg.role === 'tool') {
        anthropicMessages.push({
          role: 'user',
          content: [
            {
              type: 'tool_result',
              tool_use_id: msg.toolCallId,
              content: msg.content,
            },
          ],
        });
      } else if (msg.role === 'assistant' && msg.toolCalls?.length) {
        const content: Record<string, unknown>[] = [];
        if (msg.content) content.push({ type: 'text', text: msg.content });
        for (const tc of msg.toolCalls) {
          content.push({
            type: 'tool_use',
            id: tc.id,
            name: tc.name,
            input: tc.arguments,
          });
        }
        anthropicMessages.push({ role: 'assistant', content });
      } else {
        anthropicMessages.push({ role: msg.role, content: msg.content });
      }
    }

    return { systemPrompt, messages: anthropicMessages };
  }

  private toAnthropicTools(tools: Record<string, unknown>[]): Record<string, unknown>[] {
    return tools.map((tool) => ({
      name: tool.name,
      description: tool.description ?? '',
      input_schema: tool.parameters ?? { type: 'object', properties: {} },
    }));
  }

  // --- Google ---

  private async callGoogle(
    messages: Message[],
    model: string,
    temperature: number,
  ): Promise<Message> {
    let genai: { GoogleGenerativeAI: new (key: string) => {
      getGenerativeModel: (opts: { model: string }) => {
        generateContent: (req: { contents: unknown[]; generationConfig: unknown }) => Promise<{
          response: { text: () => string };
        }>;
      };
    }};

    try {
      genai = await dynamicImport('@google/generative-ai') as typeof genai;
    } catch {
      throw new ConfigurationError(
        'Google AI package not installed. Run: npm install @google/generative-ai',
      );
    }

    const resolvedModel = this.resolveModel(model, 'google');
    const client = new genai.GoogleGenerativeAI(this.config.googleApiKey ?? '');
    const genModel = client.getGenerativeModel({ model: resolvedModel });

    // Build simple prompt from messages
    const promptParts = messages.map((msg) => {
      const prefix: Record<string, string> = {
        system: 'System: ',
        user: '',
        assistant: 'Assistant: ',
        tool: 'Tool result: ',
      };
      return `${prefix[msg.role] ?? ''}${msg.content}`;
    });

    const result = await genModel.generateContent({
      contents: [{ role: 'user', parts: [{ text: promptParts.join('\n\n') }] }],
      generationConfig: { temperature },
    });

    return {
      role: 'assistant',
      content: result.response.text() ?? '',
    };
  }

  // --- Ollama ---

  private async callOllama(
    messages: Message[],
    model: string,
    temperature: number,
  ): Promise<Message> {
    let OpenAI: new (opts: { baseURL: string; apiKey: string }) => {
      chat: {
        completions: {
          create: (req: Record<string, unknown>) => Promise<{
            choices: Array<{ message: { content: string | null } }>;
          }>;
        };
      };
    };

    try {
      ({ OpenAI } = await dynamicImport('openai') as any);
    } catch {
      throw new ConfigurationError(
        'OpenAI package needed for Ollama compatibility. Run: npm install openai',
      );
    }

    const host = this.config.ollamaHost ?? 'http://localhost:11434';
    const client = new OpenAI({ baseURL: `${host}/v1`, apiKey: 'ollama' });
    const resolvedModel = this.resolveModel(model, 'ollama');

    const response = await client.chat.completions.create({
      model: resolvedModel,
      messages: this.toOpenAIMessages(messages),
      temperature,
    });

    return {
      role: 'assistant',
      content: response.choices[0].message.content ?? '',
    };
  }
}
