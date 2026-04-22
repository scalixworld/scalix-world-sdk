import { BaseService } from './base.js';

export interface UploadResult {
  docId: string;
  filename: string;
  status: string;
}

export interface QueryResult {
  answer: string;
  sources?: Array<{ docId: string; content: string; score: number }>;
}

export interface DocumentInfo {
  docId: string;
  filename: string;
  uploadedAt: string;
  status: string;
}

export class RAGService extends BaseService {
  async upload(file: Blob, options?: { filename?: string }): Promise<UploadResult> {
    const formData = new FormData();
    formData.append('file', file, options?.filename);
    return this.requestMultipart<UploadResult>('/v1/rag/upload', formData);
  }

  async query(query: string, options?: { docIds?: string[] }): Promise<QueryResult> {
    return this.request('POST', '/v1/rag/query', {
      body: { query, doc_ids: options?.docIds },
    });
  }

  async listDocuments(): Promise<{ documents: DocumentInfo[] }> {
    return this.request('GET', '/v1/rag/documents');
  }

  async deleteDocument(docId: string): Promise<void> {
    await this.request('DELETE', `/v1/rag/documents/${encodeURIComponent(docId)}`);
  }
}
