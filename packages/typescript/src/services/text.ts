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
}
