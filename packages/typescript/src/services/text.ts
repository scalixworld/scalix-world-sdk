import { BaseService } from './base.js';

export interface SentimentResult {
  sentiment: 'positive' | 'negative' | 'neutral';
  score: number;
  confidence: number;
}

export interface SummaryResult {
  summary: string;
  original_length: number;
  summary_length: number;
  compression_ratio: number;
  key_points: string[];
}

export interface TranslationResult {
  translated_text: string;
  source_language: string;
  target_language: string;
  confidence: number;
}

export interface GrammarResult {
  corrected_text: string;
  corrections: Array<{ original: string; corrected: string; rule?: string }>;
}

export interface AutocompleteResult {
  completions: string[];
}

export interface VectorSearchContext {
  text: string;
  [key: string]: unknown;
}

export interface VectorSearchResult {
  results: Array<{ content: string; score: number; metadata?: Record<string, unknown> }>;
  total: number;
}

export class TextService extends BaseService {
  async sentiment(text: string): Promise<SentimentResult> {
    return this.request<SentimentResult>('POST', '/v1/text/sentiment', {
      body: { text },
    });
  }

  async summarize(
    text: string,
    options?: { length?: 'short' | 'medium' | 'long'; style?: 'bullet' | 'paragraph' },
  ): Promise<SummaryResult> {
    return this.request<SummaryResult>('POST', '/v1/text/summarize', {
      body: { text, ...options },
    });
  }

  async translate(
    text: string,
    targetLanguage: string,
    options?: { sourceLanguage?: string },
  ): Promise<TranslationResult> {
    return this.request<TranslationResult>('POST', '/v1/text/translate', {
      body: {
        text,
        target_language: targetLanguage,
        ...(options?.sourceLanguage ? { source_language: options.sourceLanguage } : {}),
      },
    });
  }

  async grammar(text: string): Promise<GrammarResult> {
    return this.request<GrammarResult>('POST', '/v1/text/grammar', {
      body: { text },
    });
  }

  async autocomplete(
    text: string,
    options?: { maxCompletions?: number },
  ): Promise<AutocompleteResult> {
    return this.request<AutocompleteResult>('POST', '/v1/text/autocomplete', {
      body: { text, ...options },
    });
  }

  async vectorSearch(
    query: string,
    context: VectorSearchContext[],
    options?: { topK?: number; threshold?: number },
  ): Promise<VectorSearchResult> {
    return this.request<VectorSearchResult>('POST', '/v1/text/vector-search', {
      body: { query, context, ...options },
    });
  }
}
