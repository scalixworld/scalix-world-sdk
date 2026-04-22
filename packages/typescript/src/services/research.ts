import { BaseService } from './base.js';

export interface SearchResult {
  results: Array<{
    title: string;
    url: string;
    snippet: string;
  }>;
}

export interface ResearchResult {
  answer: string;
  sources?: Array<{ title: string; url: string }>;
}

export class ResearchService extends BaseService {
  async search(query: string, options?: { maxResults?: number }): Promise<SearchResult> {
    return this.request('POST', '/v1/research/search', {
      body: { query, max_results: options?.maxResults },
    });
  }

  async research(query: string): Promise<ResearchResult> {
    return this.request('POST', '/v1/research', { body: { query } });
  }

  async deep(query: string): Promise<ResearchResult> {
    return this.request('POST', '/v1/research/deep', { body: { query } });
  }
}
