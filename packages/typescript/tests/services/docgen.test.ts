import { describe, it, expect, vi, beforeEach, afterEach } from 'vitest';
import { DocGenService } from '../../src/services/docgen.js';
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

describe('DocGenService', () => {
  let service: DocGenService;

  beforeEach(() => {
    service = new DocGenService(config);
    vi.restoreAllMocks();
  });

  afterEach(() => {
    vi.restoreAllMocks();
  });

  // ── create() ────────────────────────────────────────────────

  it('sends POST /v1/docgen/create with all options', async () => {
    const mockResult = {
      status: 'completed',
      doc_id: 'doc-789',
      format: 'pdf',
      download_url: 'https://api.scalix.world/v1/docgen/download/doc-789',
      created_at: '2026-04-20T12:00:00Z',
      size_bytes: 4096,
    };
    mockFetchJson(mockResult);

    const result = await service.create({
      prompt: 'Generate a quarterly report',
      format: 'pdf',
      template_id: 'tmpl-1',
      style: 'professional',
      language: 'en',
    });

    expect(global.fetch).toHaveBeenCalledWith(
      'https://api.scalix.world/v1/docgen/create',
      expect.objectContaining({ method: 'POST' }),
    );

    const callArgs = vi.mocked(global.fetch).mock.calls[0];
    const body = JSON.parse(callArgs[1]!.body as string);
    expect(body.prompt).toBe('Generate a quarterly report');
    expect(body.format).toBe('pdf');
    expect(body.template_id).toBe('tmpl-1');
    expect(body.style).toBe('professional');
    expect(body.language).toBe('en');

    expect(result.doc_id).toBe('doc-789');
    expect(result.status).toBe('completed');
    expect(result.size_bytes).toBe(4096);
  });

  it('sends create with only required fields', async () => {
    mockFetchJson({ status: 'completed', doc_id: 'doc-1', format: 'xlsx', download_url: '/dl', created_at: '2026-01-01' });

    await service.create({ prompt: 'Budget spreadsheet', format: 'xlsx' });

    const callArgs = vi.mocked(global.fetch).mock.calls[0];
    const body = JSON.parse(callArgs[1]!.body as string);
    expect(body.prompt).toBe('Budget spreadsheet');
    expect(body.format).toBe('xlsx');
    expect(body.template_id).toBeUndefined();
  });

  // ── preview() ───────────────────────────────────────────────

  it('sends POST /v1/docgen/preview and returns html_content', async () => {
    mockFetchJson({ html_content: '<h1>Preview</h1><p>Report content</p>' });

    const result = await service.preview({
      prompt: 'Generate a summary',
      format: 'html',
      style: 'casual',
    });

    expect(global.fetch).toHaveBeenCalledWith(
      'https://api.scalix.world/v1/docgen/preview',
      expect.objectContaining({ method: 'POST' }),
    );

    const callArgs = vi.mocked(global.fetch).mock.calls[0];
    const body = JSON.parse(callArgs[1]!.body as string);
    expect(body.prompt).toBe('Generate a summary');
    expect(body.format).toBe('html');
    expect(body.style).toBe('casual');

    expect(result.html_content).toContain('<h1>Preview</h1>');
  });

  // ── formats() ───────────────────────────────────────────────

  it('calls GET /v1/docgen/formats', async () => {
    const mockFormats = [
      {
        format: 'pdf',
        mime_type: 'application/pdf',
        description: 'PDF document',
        max_size_bytes: 10485760,
        supported_styles: ['professional', 'casual'],
      },
      {
        format: 'docx',
        mime_type: 'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
        description: 'Word document',
        max_size_bytes: 10485760,
        supported_styles: ['professional'],
      },
    ];
    mockFetchJson(mockFormats);

    const result = await service.formats();

    expect(global.fetch).toHaveBeenCalledWith(
      'https://api.scalix.world/v1/docgen/formats',
      expect.objectContaining({ method: 'GET' }),
    );
    expect(result).toHaveLength(2);
    expect(result[0].format).toBe('pdf');
  });

  // ── templates() ─────────────────────────────────────────────

  it('calls GET /v1/docgen/templates', async () => {
    const mockTemplates = [
      {
        id: 'tmpl-1',
        name: 'Quarterly Report',
        description: 'Standard quarterly report',
        category: 'business',
        format: 'pdf',
        tags: ['report', 'quarterly'],
      },
    ];
    mockFetchJson(mockTemplates);

    const result = await service.templates();

    expect(global.fetch).toHaveBeenCalledWith(
      'https://api.scalix.world/v1/docgen/templates',
      expect.objectContaining({ method: 'GET' }),
    );
    expect(result).toHaveLength(1);
    expect(result[0].id).toBe('tmpl-1');
    expect(result[0].tags).toContain('report');
  });

  // ── history() ───────────────────────────────────────────────

  it('calls GET /v1/docgen/history with limit and offset', async () => {
    mockFetchJson({
      documents: [{ doc_id: 'doc-1', status: 'completed', format: 'pdf', download_url: '/dl', created_at: '2026-01-01' }],
      total: 10,
    });

    const result = await service.history({ limit: 5, offset: 10 });

    expect(global.fetch).toHaveBeenCalledWith(
      'https://api.scalix.world/v1/docgen/history?limit=5&offset=10',
      expect.objectContaining({ method: 'GET' }),
    );
    expect(result.documents).toHaveLength(1);
    expect(result.total).toBe(10);
  });

  it('calls GET /v1/docgen/history without query params when none provided', async () => {
    mockFetchJson({ documents: [], total: 0 });

    await service.history();

    expect(global.fetch).toHaveBeenCalledWith(
      'https://api.scalix.world/v1/docgen/history',
      expect.objectContaining({ method: 'GET' }),
    );
  });

  it('calls GET /v1/docgen/history with only limit', async () => {
    mockFetchJson({ documents: [], total: 0 });

    await service.history({ limit: 20 });

    expect(global.fetch).toHaveBeenCalledWith(
      'https://api.scalix.world/v1/docgen/history?limit=20',
      expect.objectContaining({ method: 'GET' }),
    );
  });

  // ── download() ──────────────────────────────────────────────

  it('calls GET /v1/docgen/download/:docId and returns raw Response', async () => {
    const mockResp = {
      ok: true,
      status: 200,
      json: () => Promise.resolve({}),
      headers: new Headers({ 'content-type': 'application/pdf' }),
    };
    global.fetch = vi.fn().mockResolvedValue(mockResp);

    const result = await service.download('doc-789');

    expect(global.fetch).toHaveBeenCalledWith(
      'https://api.scalix.world/v1/docgen/download/doc-789',
      expect.objectContaining({ method: 'GET' }),
    );
    // download returns the raw Response
    expect(result).toBe(mockResp);
  });

  // ── revise() ────────────────────────────────────────────────

  it('sends POST /v1/docgen/revise with doc_id and prompt', async () => {
    const mockResult = {
      status: 'completed',
      doc_id: 'doc-789-v2',
      format: 'pdf',
      download_url: '/dl/doc-789-v2',
      created_at: '2026-04-20T13:00:00Z',
    };
    mockFetchJson(mockResult);

    const result = await service.revise('doc-789', 'Make it more concise');

    expect(global.fetch).toHaveBeenCalledWith(
      'https://api.scalix.world/v1/docgen/revise',
      expect.objectContaining({ method: 'POST' }),
    );

    const callArgs = vi.mocked(global.fetch).mock.calls[0];
    const body = JSON.parse(callArgs[1]!.body as string);
    expect(body.doc_id).toBe('doc-789');
    expect(body.prompt).toBe('Make it more concise');

    expect(result.doc_id).toBe('doc-789-v2');
  });

  // ── versions() ──────────────────────────────────────────────

  it('calls GET /v1/docgen/versions/:docId', async () => {
    const mockVersions = {
      versions: [
        { version_id: 'v1', created_at: '2026-04-20T12:00:00Z' },
        { version_id: 'v2', created_at: '2026-04-20T13:00:00Z' },
      ],
    };
    mockFetchJson(mockVersions);

    const result = await service.versions('doc-789');

    expect(global.fetch).toHaveBeenCalledWith(
      'https://api.scalix.world/v1/docgen/versions/doc-789',
      expect.objectContaining({ method: 'GET' }),
    );
    expect(result.versions).toHaveLength(2);
    expect(result.versions[0].version_id).toBe('v1');
  });

  // ── Error handling ──────────────────────────────────────────

  it('throws on create failure', async () => {
    mockFetchJson(
      { error: { message: 'Unsupported format', code: 'invalid_format' } },
      false,
      400,
    );

    await expect(
      service.create({ prompt: 'Test', format: 'xlsx' }),
    ).rejects.toThrow('Unsupported format');
  });
});
