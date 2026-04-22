import { BaseService } from './base.js';

export interface SentimentResult {
  sentiment: 'positive' | 'negative' | 'neutral' | 'mixed';
  score: number;
  confidence: number;
}

export interface SummaryResult {
  summary: string;
}

export interface TranslationResult {
  translation: string;
  detectedLanguage?: string;
}

export class TextService extends BaseService {
  async sentiment(text: string): Promise<SentimentResult> {
    return this.request('POST', '/v1/text/sentiment', { body: { text } });
  }

  async summarize(text: string, options?: { maxLength?: number }): Promise<SummaryResult> {
    return this.request('POST', '/v1/text/summarize', {
      body: { text, max_length: options?.maxLength },
    });
  }

  async translate(text: string, options: { targetLanguage: string; sourceLanguage?: string }): Promise<TranslationResult> {
    return this.request('POST', '/v1/text/translate', {
      body: {
        text,
        target_language: options.targetLanguage,
        source_language: options.sourceLanguage,
      },
    });
  }
}
