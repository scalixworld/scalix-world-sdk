import { BaseService } from './base.js';

export interface RAGDocument {
  doc_id: string;
  filename: string;
  uploaded_at: string;
  size: number;
  status: 'indexed' | 'pending' | 'failed';
  chunk_count: number;
}

export interface RAGQueryResult {
  results: Array<{
    doc_id: string;
    chunk_id: string;
    content: string;
    similarity_score: number;
    metadata?: Record<string, unknown>;
  }>;
  total_results: number;
}

export interface RAGUploadResult {
  doc_id: string;
  filename: string;
  size: number;
  status: string;
  chunks: number;
}

export class RAGService extends BaseService {
  async upload(file: Blob, options?: { filename?: string }): Promise<RAGUploadResult> {
    const formData = new FormData();
    formData.append('file', file, options?.filename);
    return this.requestMultipart<RAGUploadResult>('/v1/rag/upload', formData);
  }

  async query(
    query: string,
    options?: { doc_ids?: string[]; top_k?: number },
  ): Promise<RAGQueryResult> {
    return this.request<RAGQueryResult>('POST', '/v1/rag/query', {
      body: { query, ...options },
    });
  }

  async documents(): Promise<{ documents: RAGDocument[]; total: number }> {
    return this.request('GET', '/v1/rag/documents');
  }

  async deleteDocument(docId: string): Promise<{ success: boolean }> {
    return this.request('DELETE', `/v1/rag/documents/${docId}`);
  }
}
