import { describe, it, expect, vi, beforeEach, afterEach } from 'vitest';
import { ChatService } from '../../src/services/chat.js';

vi.mock('../../src/config.js', () => ({
  getConfig: () => ({ apiKey: 'test-key', baseUrl: 'https://api.scalix.world' }),
}));

function mockFetchJson(data: unknown, ok = true, status = 200) {
  global.fetch = vi.fn().mockResolvedValue({
    ok,
    status,
    json: () => Promise.resolve(data),
    body: null,
  });
}

describe('ChatService', () => {
  let service: ChatService;

  beforeEach(() => {
    service = new ChatService();
    vi.restoreAllMocks();
  });

  afterEach(() => {
    vi.restoreAllMocks();
  });

  // ── complete() ──────────────────────────────────────────────

  it('sends POST /v1/chat/completions with correct params', async () => {
    const mockResponse = {
      id: 'chatcmpl-1',
      object: 'chat.completion',
      created: 1700000000,
      model: 'gpt-4o',
      choices: [
        {
          index: 0,
          message: { role: 'assistant', content: 'Hello there!' },
          finish_reason: 'stop',
        },
      ],
      usage: { prompt_tokens: 10, completion_tokens: 5, total_tokens: 15 },
    };
    mockFetchJson(mockResponse);

    const result = await service.complete({
      model: 'gpt-4o',
      messages: [{ role: 'user', content: 'Hello' }],
    });

    expect(global.fetch).toHaveBeenCalledWith(
      'https://api.scalix.world/v1/chat/completions',
      expect.objectContaining({
        method: 'POST',
        headers: expect.objectContaining({
          Authorization: 'Bearer test-key',
          'Content-Type': 'application/json',
        }),
      }),
    );

    // Verify body includes stream: false
    const callArgs = vi.mocked(global.fetch).mock.calls[0];
    const body = JSON.parse(callArgs[1]!.body as string);
    expect(body.stream).toBe(false);
    expect(body.model).toBe('gpt-4o');
    expect(body.messages).toEqual([{ role: 'user', content: 'Hello' }]);

    expect(result.id).toBe('chatcmpl-1');
    expect(result.choices[0].message.content).toBe('Hello there!');
    expect(result.usage.total_tokens).toBe(15);
  });

  it('passes optional parameters (temperature, max_tokens, top_p)', async () => {
    mockFetchJson({ id: '1', choices: [], usage: {} });

    await service.complete({
      model: 'gpt-4o',
      messages: [{ role: 'user', content: 'Hi' }],
      temperature: 0.7,
      max_tokens: 100,
      top_p: 0.9,
    });

    const callArgs = vi.mocked(global.fetch).mock.calls[0];
    const body = JSON.parse(callArgs[1]!.body as string);
    expect(body.temperature).toBe(0.7);
    expect(body.max_tokens).toBe(100);
    expect(body.top_p).toBe(0.9);
  });

  // ── stream() ────────────────────────────────────────────────

  it('parses SSE stream events and yields content', async () => {
    const sseData = [
      'data: {"choices":[{"delta":{"content":"Hello"}}]}\n\n',
      'data: {"choices":[{"delta":{"content":" world"}}]}\n\n',
      'data: [DONE]\n\n',
    ].join('');

    const encoder = new TextEncoder();
    let pushed = false;
    const readable = new ReadableStream<Uint8Array>({
      start(controller) {
        controller.enqueue(encoder.encode(sseData));
        pushed = true;
        controller.close();
      },
    });

    global.fetch = vi.fn().mockResolvedValue({
      ok: true,
      status: 200,
      json: () => Promise.resolve({}),
      body: readable,
    });

    const chunks: string[] = [];
    for await (const chunk of service.stream({
      model: 'gpt-4o',
      messages: [{ role: 'user', content: 'Hi' }],
    })) {
      chunks.push(chunk);
    }

    expect(chunks).toEqual(['Hello', ' world']);

    // Verify stream: true was sent in the body
    const callArgs = vi.mocked(global.fetch).mock.calls[0];
    const body = JSON.parse(callArgs[1]!.body as string);
    expect(body.stream).toBe(true);
  });

  it('handles SSE stream with chunks split across reads', async () => {
    const encoder = new TextEncoder();
    const part1 = 'data: {"choices":[{"delta":{"content":"He';
    const part2 = 'llo"}}]}\n\ndata: [DONE]\n\n';

    let readCount = 0;
    const readable = new ReadableStream<Uint8Array>({
      pull(controller) {
        if (readCount === 0) {
          controller.enqueue(encoder.encode(part1));
          readCount++;
        } else if (readCount === 1) {
          controller.enqueue(encoder.encode(part2));
          readCount++;
        } else {
          controller.close();
        }
      },
    });

    global.fetch = vi.fn().mockResolvedValue({
      ok: true,
      status: 200,
      json: () => Promise.resolve({}),
      body: readable,
    });

    const chunks: string[] = [];
    for await (const chunk of service.stream({
      model: 'gpt-4o',
      messages: [{ role: 'user', content: 'Hi' }],
    })) {
      chunks.push(chunk);
    }

    expect(chunks).toEqual(['Hello']);
  });

  it('skips events with no delta content', async () => {
    const sseData = [
      'data: {"choices":[{"delta":{}}]}\n\n',
      'data: {"choices":[{"delta":{"content":"OK"}}]}\n\n',
      'data: [DONE]\n\n',
    ].join('');

    const encoder = new TextEncoder();
    const readable = new ReadableStream<Uint8Array>({
      start(controller) {
        controller.enqueue(encoder.encode(sseData));
        controller.close();
      },
    });

    global.fetch = vi.fn().mockResolvedValue({
      ok: true,
      status: 200,
      json: () => Promise.resolve({}),
      body: readable,
    });

    const chunks: string[] = [];
    for await (const chunk of service.stream({
      model: 'gpt-4o',
      messages: [{ role: 'user', content: 'Hi' }],
    })) {
      chunks.push(chunk);
    }

    expect(chunks).toEqual(['OK']);
  });

  it('returns nothing when response body is null', async () => {
    global.fetch = vi.fn().mockResolvedValue({
      ok: true,
      status: 200,
      json: () => Promise.resolve({}),
      body: null,
    });

    const chunks: string[] = [];
    for await (const chunk of service.stream({
      model: 'gpt-4o',
      messages: [{ role: 'user', content: 'Hi' }],
    })) {
      chunks.push(chunk);
    }

    expect(chunks).toEqual([]);
  });

  // ── models() ────────────────────────────────────────────────

  it('calls GET /v1/models and returns data array', async () => {
    const mockModels = {
      data: [
        { id: 'gpt-4o', name: 'GPT-4o' },
        { id: 'claude-3.5-sonnet', name: 'Claude 3.5 Sonnet' },
      ],
    };
    mockFetchJson(mockModels);

    const result = await service.models();

    expect(global.fetch).toHaveBeenCalledWith(
      'https://api.scalix.world/v1/models',
      expect.objectContaining({ method: 'GET' }),
    );
    expect(result).toEqual(mockModels.data);
    expect(result).toHaveLength(2);
  });

  // ── Error handling ──────────────────────────────────────────

  it('throws ScalixError on non-ok response', async () => {
    mockFetchJson(
      { error: { message: 'Rate limit exceeded', code: 'rate_limit' } },
      false,
      429,
    );

    await expect(
      service.complete({
        model: 'gpt-4o',
        messages: [{ role: 'user', content: 'Hi' }],
      }),
    ).rejects.toThrow('Rate limit exceeded');
  });

  it('throws ScalixError with status when error body has no message', async () => {
    global.fetch = vi.fn().mockResolvedValue({
      ok: false,
      status: 500,
      json: () => Promise.reject(new Error('not json')),
    });

    await expect(
      service.complete({
        model: 'gpt-4o',
        messages: [{ role: 'user', content: 'Hi' }],
      }),
    ).rejects.toThrow('Request failed: 500');
  });

  it('throws AuthenticationError when API key is missing', async () => {
    vi.resetModules();
    const { ChatService: FreshChatService } = await import('../../src/services/chat.js');
    const noKeyService = new FreshChatService({
      baseUrl: 'https://api.scalix.world',
      environment: 'development',
      logLevel: 'info',
      defaultModel: 'auto',
      sandboxMode: 'auto',
      databaseMode: 'auto',
    });

    await expect(
      noKeyService.complete({
        model: 'gpt-4o',
        messages: [{ role: 'user', content: 'Hi' }],
      }),
    ).rejects.toThrow('API key required');
  });
});
