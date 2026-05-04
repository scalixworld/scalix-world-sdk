import { describe, it, expect, vi, beforeEach, afterEach } from 'vitest';
import { RAGService } from '../../src/services/rag.js';
import type { ScalixConfig } from '../../src/config.js';

const config: ScalixConfig = { apiKey: 'test-key', baseUrl: 'https://api.scalix.world' };

function mockFetchJson(data: unknown, ok = true, status = 200) {
  global.fetch = vi.fn().mockResolvedValue({
    ok,
    status,
    headers: new Headers(),
    json: () => Promise.resolve(data),
  });
}

describe('RAGService', () => {
  let service: RAGService;

  beforeEach(() => {
    service = new RAGService(config);
    vi.restoreAllMocks();
  });

  afterEach(() => {
    vi.restoreAllMocks();
  });

  // ── upload() ────────────────────────────────────────────────

  it('sends multipart POST /v1/rag/upload with file', async () => {
    const mockResult = {
      doc_id: 'doc-123',
      filename: 'test.pdf',
      size: 1024,
      status: 'pending',
      chunks: 5,
    };
    mockFetchJson(mockResult);

    const file = new Blob(['file content'], { type: 'application/pdf' });
    const result = await service.upload(file, { filename: 'test.pdf' });

    expect(global.fetch).toHaveBeenCalledWith(
      'https://api.scalix.world/v1/rag/upload',
      expect.objectContaining({
        method: 'POST',
        headers: expect.objectContaining({
          Authorization: 'Bearer test-key',
        }),
      }),
    );

    // Verify FormData was sent (no Content-Type header for multipart)
    const callArgs = vi.mocked(global.fetch).mock.calls[0];
    const headers = callArgs[1]!.headers as Record<string, string>;
    expect(headers['Content-Type']).toBeUndefined();
    expect(callArgs[1]!.body).toBeInstanceOf(FormData);

    expect(result.doc_id).toBe('doc-123');
    expect(result.chunks).toBe(5);
  });

  it('uploads file without optional filename', async () => {
    mockFetchJson({ doc_id: 'doc-456', filename: 'blob', size: 100, status: 'pending', chunks: 1 });

    const file = new Blob(['data']);
    await service.upload(file);

    const callArgs = vi.mocked(global.fetch).mock.calls[0];
    expect(callArgs[1]!.body).toBeInstanceOf(FormData);
  });

  // ── query() ─────────────────────────────────────────────────

  it('sends POST /v1/rag/query with query and options', async () => {
    const mockResult = {
      results: [
        {
          doc_id: 'doc-1',
          chunk_id: 'chunk-1',
          content: 'Relevant content',
          similarity_score: 0.92,
          metadata: { page: 3 },
        },
      ],
      total_results: 1,
    };
    mockFetchJson(mockResult);

    const result = await service.query('What is AI?', {
      doc_ids: ['doc-1', 'doc-2'],
      top_k: 5,
    });

    expect(global.fetch).toHaveBeenCalledWith(
      'https://api.scalix.world/v1/rag/query',
      expect.objectContaining({ method: 'POST' }),
    );

    const callArgs = vi.mocked(global.fetch).mock.calls[0];
    const body = JSON.parse(callArgs[1]!.body as string);
    expect(body.query).toBe('What is AI?');
    expect(body.doc_ids).toEqual(['doc-1', 'doc-2']);
    expect(body.top_k).toBe(5);

    expect(result.results).toHaveLength(1);
    expect(result.results[0].similarity_score).toBe(0.92);
    expect(result.total_results).toBe(1);
  });

  it('sends query without optional params', async () => {
    mockFetchJson({ results: [], total_results: 0 });

    await service.query('Search text');

    const callArgs = vi.mocked(global.fetch).mock.calls[0];
    const body = JSON.parse(callArgs[1]!.body as string);
    expect(body.query).toBe('Search text');
    expect(body.doc_ids).toBeUndefined();
    expect(body.top_k).toBeUndefined();
  });

  // ── documents() ─────────────────────────────────────────────

  it('calls GET /v1/rag/documents', async () => {
    const mockDocs = {
      documents: [
        {
          doc_id: 'doc-1',
          filename: 'report.pdf',
          uploaded_at: '2026-01-01T00:00:00Z',
          size: 2048,
          status: 'indexed',
          chunk_count: 12,
        },
      ],
      total: 1,
    };
    mockFetchJson(mockDocs);

    const result = await service.documents();

    expect(global.fetch).toHaveBeenCalledWith(
      'https://api.scalix.world/v1/rag/documents',
      expect.objectContaining({ method: 'GET' }),
    );
    expect(result.documents).toHaveLength(1);
    expect(result.documents[0].status).toBe('indexed');
    expect(result.total).toBe(1);
  });

  // ── deleteDocument() ────────────────────────────────────────

  it('calls DELETE /v1/rag/documents/:docId', async () => {
    mockFetchJson({ success: true });

    const result = await service.deleteDocument('doc-abc');

    expect(global.fetch).toHaveBeenCalledWith(
      'https://api.scalix.world/v1/rag/documents/doc-abc',
      expect.objectContaining({ method: 'DELETE' }),
    );
    expect(result.success).toBe(true);
  });

  // ── Error handling ──────────────────────────────────────────

  it('throws on upload failure', async () => {
    mockFetchJson(
      { error: { message: 'File too large', code: 'file_too_large' } },
      false,
      413,
    );

    const file = new Blob(['big data']);
    await expect(service.upload(file)).rejects.toThrow('File too large');
  });

  it('throws on query failure', async () => {
    mockFetchJson(
      { error: { message: 'No documents indexed', code: 'no_documents' } },
      false,
      400,
    );

    await expect(service.query('search')).rejects.toThrow('No documents indexed');
  });
});
