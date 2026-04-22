import { BaseService } from './base.js';

export interface DocumentResult {
  docId: string;
  content: string;
  format: string;
}

export interface DocGenOptions {
  format?: string;
  template?: string;
  maxLength?: number;
}

export class DocGenService extends BaseService {
  async create(prompt: string, options?: DocGenOptions): Promise<DocumentResult> {
    return this.request('POST', '/v1/docgen/create', {
      body: { prompt, ...options },
    });
  }

  async preview(prompt: string, options?: DocGenOptions): Promise<DocumentResult> {
    return this.request('POST', '/v1/docgen/preview', {
      body: { prompt, ...options },
    });
  }

  async formats(): Promise<{ formats: string[] }> {
    return this.request('GET', '/v1/docgen/formats');
  }

  async templates(): Promise<{ templates: Array<{ id: string; name: string; description: string }> }> {
    return this.request('GET', '/v1/docgen/templates');
  }

  async download(docId: string): Promise<Response> {
    return this.requestRaw('GET', `/v1/docgen/download/${encodeURIComponent(docId)}`);
  }

  async revise(docId: string, instructions: string): Promise<DocumentResult> {
    return this.request('POST', '/v1/docgen/revise', {
      body: { doc_id: docId, instructions },
    });
  }

  async history(): Promise<{ documents: Array<{ docId: string; prompt: string; createdAt: string }> }> {
    return this.request('GET', '/v1/docgen/history');
  }
}
