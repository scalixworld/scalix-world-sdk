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
    const params = new URLSearchParams({ query });
    if (options?.maxResults != null) params.set('max_results', String(options.maxResults));
    return this.request<SearchResult>('POST', `/v1/research/search?${params}`);
  }

  async research(query: string): Promise<ResearchResult> {
    return this.request('POST', '/v1/research', { body: { query } });
  }

  async deep(query: string): Promise<ResearchResult> {
    return this.request('POST', '/v1/research/deep', { body: { query } });
  }
}
