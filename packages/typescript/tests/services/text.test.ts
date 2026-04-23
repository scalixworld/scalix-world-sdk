import { describe, it, expect, vi, beforeEach, afterEach } from 'vitest';
import { TextService } from '../../src/services/text.js';

vi.mock('../../src/config.js', () => ({
  getConfig: () => ({ apiKey: 'test-key', baseUrl: 'https://api.scalix.world' }),
}));

function mockFetchJson(data: unknown, ok = true, status = 200) {
  global.fetch = vi.fn().mockResolvedValue({
    ok,
    status,
    json: () => Promise.resolve(data),
  });
}

describe('TextService', () => {
  let service: TextService;

  beforeEach(() => {
    service = new TextService();
    vi.restoreAllMocks();
  });

  afterEach(() => {
    vi.restoreAllMocks();
  });

  // ── sentiment() ─────────────────────────────────────────────

  it('sends POST /v1/text/sentiment and returns sentiment result', async () => {
    const mockResult = {
      sentiment: 'positive',
      score: 0.85,
      confidence: 0.92,
    };
    mockFetchJson(mockResult);

    const result = await service.sentiment('I love this product!');

    expect(global.fetch).toHaveBeenCalledWith(
      'https://api.scalix.world/v1/text/sentiment',
      expect.objectContaining({ method: 'POST' }),
    );

    const callArgs = vi.mocked(global.fetch).mock.calls[0];
    const body = JSON.parse(callArgs[1]!.body as string);
    expect(body.text).toBe('I love this product!');

    expect(result.sentiment).toBe('positive');
    expect(result.score).toBe(0.85);
    expect(result.confidence).toBe(0.92);
  });

  it('handles negative sentiment', async () => {
    mockFetchJson({ sentiment: 'negative', score: -0.7, confidence: 0.88 });

    const result = await service.sentiment('This is terrible');

    expect(result.sentiment).toBe('negative');
    expect(result.score).toBe(-0.7);
  });

  it('handles neutral sentiment', async () => {
    mockFetchJson({ sentiment: 'neutral', score: 0.05, confidence: 0.6 });

    const result = await service.sentiment('The weather is normal today');

    expect(result.sentiment).toBe('neutral');
  });

  // ── summarize() ─────────────────────────────────────────────

  it('sends POST /v1/text/summarize with text and options', async () => {
    const mockResult = {
      summary: 'AI is transforming industries worldwide.',
      original_length: 500,
      summary_length: 40,
      compression_ratio: 0.08,
      key_points: ['AI transformation', 'Global impact'],
    };
    mockFetchJson(mockResult);

    const longText = 'Artificial intelligence is rapidly transforming...';
    const result = await service.summarize(longText, {
      length: 'short',
      style: 'bullet',
    });

    expect(global.fetch).toHaveBeenCalledWith(
      'https://api.scalix.world/v1/text/summarize',
      expect.objectContaining({ method: 'POST' }),
    );

    const callArgs = vi.mocked(global.fetch).mock.calls[0];
    const body = JSON.parse(callArgs[1]!.body as string);
    expect(body.text).toBe(longText);
    expect(body.length).toBe('short');
    expect(body.style).toBe('bullet');

    expect(result.summary).toBe('AI is transforming industries worldwide.');
    expect(result.key_points).toHaveLength(2);
    expect(result.compression_ratio).toBe(0.08);
  });

  it('sends summarize without optional params', async () => {
    mockFetchJson({
      summary: 'Short summary',
      original_length: 100,
      summary_length: 13,
      compression_ratio: 0.13,
      key_points: [],
    });

    await service.summarize('Some text to summarize');

    const callArgs = vi.mocked(global.fetch).mock.calls[0];
    const body = JSON.parse(callArgs[1]!.body as string);
    expect(body.text).toBe('Some text to summarize');
    expect(body.length).toBeUndefined();
    expect(body.style).toBeUndefined();
  });

  it('supports paragraph style summarization', async () => {
    mockFetchJson({
      summary: 'A paragraph.',
      original_length: 200,
      summary_length: 12,
      compression_ratio: 0.06,
      key_points: ['main point'],
    });

    await service.summarize('Long text...', { length: 'long', style: 'paragraph' });

    const callArgs = vi.mocked(global.fetch).mock.calls[0];
    const body = JSON.parse(callArgs[1]!.body as string);
    expect(body.length).toBe('long');
    expect(body.style).toBe('paragraph');
  });

  // ── translate() ─────────────────────────────────────────────

  it('sends POST /v1/text/translate with target language', async () => {
    const mockResult = {
      translated_text: 'Bonjour le monde',
      source_language: 'en',
      target_language: 'fr',
      confidence: 0.95,
    };
    mockFetchJson(mockResult);

    const result = await service.translate('Hello world', 'fr');

    expect(global.fetch).toHaveBeenCalledWith(
      'https://api.scalix.world/v1/text/translate',
      expect.objectContaining({ method: 'POST' }),
    );

    const callArgs = vi.mocked(global.fetch).mock.calls[0];
    const body = JSON.parse(callArgs[1]!.body as string);
    expect(body.text).toBe('Hello world');
    expect(body.target_language).toBe('fr');
    expect(body.source_language).toBeUndefined();

    expect(result.translated_text).toBe('Bonjour le monde');
    expect(result.target_language).toBe('fr');
    expect(result.confidence).toBe(0.95);
  });

  it('sends translate with explicit source language', async () => {
    mockFetchJson({
      translated_text: 'Hola mundo',
      source_language: 'en',
      target_language: 'es',
      confidence: 0.98,
    });

    await service.translate('Hello world', 'es', { sourceLanguage: 'en' });

    const callArgs = vi.mocked(global.fetch).mock.calls[0];
    const body = JSON.parse(callArgs[1]!.body as string);
    expect(body.text).toBe('Hello world');
    expect(body.target_language).toBe('es');
    expect(body.source_language).toBe('en');
  });

  it('omits source_language when not provided', async () => {
    mockFetchJson({
      translated_text: 'Translated',
      source_language: 'auto',
      target_language: 'de',
      confidence: 0.9,
    });

    await service.translate('Some text', 'de');

    const callArgs = vi.mocked(global.fetch).mock.calls[0];
    const body = JSON.parse(callArgs[1]!.body as string);
    expect(body).not.toHaveProperty('source_language');
  });

  // ── Error handling ──────────────────────────────────────────

  it('throws on sentiment analysis failure', async () => {
    mockFetchJson(
      { error: { message: 'Text too long', code: 'text_too_long' } },
      false,
      400,
    );

    await expect(service.sentiment('x'.repeat(100000))).rejects.toThrow('Text too long');
  });

  it('throws on translation failure', async () => {
    mockFetchJson(
      { error: { message: 'Unsupported language pair', code: 'unsupported_lang' } },
      false,
      400,
    );

    await expect(service.translate('Hello', 'xx')).rejects.toThrow('Unsupported language pair');
  });
});
