import { describe, it, expect, vi, beforeEach, afterEach } from 'vitest';
import { StorageService } from '../../src/services/storage.js';

vi.mock('../../src/config.js', () => ({
  getConfig: () => ({ apiKey: 'test-key', baseUrl: 'https://api.scalix.world' }),
}));

function mockFetchJson(data: unknown, ok = true, status = 200) {
  global.fetch = vi.fn().mockResolvedValue({
    ok,
    status,
    json: () => Promise.resolve(data),
  });
}

describe('StorageService', () => {
  let service: StorageService;

  beforeEach(() => {
    service = new StorageService();
    vi.restoreAllMocks();
  });

  afterEach(() => {
    vi.restoreAllMocks();
  });

  // ── getUploadUrl() ──────────────────────────────────────────

  it('sends POST /v1/storage/upload-url with mimeType', async () => {
    const mockResult = {
      uploadUrl: 'https://storage.scalix.world/upload/abc123?token=xyz',
      fileUrl: 'https://cdn.scalix.world/files/abc123.png',
    };
    mockFetchJson(mockResult);

    const result = await service.getUploadUrl('image/png');

    expect(global.fetch).toHaveBeenCalledWith(
      'https://api.scalix.world/v1/storage/upload-url',
      expect.objectContaining({
        method: 'POST',
        headers: expect.objectContaining({
          Authorization: 'Bearer test-key',
          'Content-Type': 'application/json',
        }),
      }),
    );

    const callArgs = vi.mocked(global.fetch).mock.calls[0];
    const body = JSON.parse(callArgs[1]!.body as string);
    expect(body.mimeType).toBe('image/png');
    expect(body.size).toBeUndefined();

    expect(result.uploadUrl).toContain('storage.scalix.world');
    expect(result.fileUrl).toContain('cdn.scalix.world');
  });

  it('sends POST /v1/storage/upload-url with mimeType and size', async () => {
    const mockResult = {
      uploadUrl: 'https://storage.scalix.world/upload/def456',
      fileUrl: 'https://cdn.scalix.world/files/def456.pdf',
    };
    mockFetchJson(mockResult);

    const result = await service.getUploadUrl('application/pdf', 5242880);

    const callArgs = vi.mocked(global.fetch).mock.calls[0];
    const body = JSON.parse(callArgs[1]!.body as string);
    expect(body.mimeType).toBe('application/pdf');
    expect(body.size).toBe(5242880);

    expect(result.uploadUrl).toBeDefined();
    expect(result.fileUrl).toBeDefined();
  });

  it('handles various mime types', async () => {
    mockFetchJson({ uploadUrl: 'https://up.test', fileUrl: 'https://file.test' });

    await service.getUploadUrl('video/mp4', 104857600);

    const body = JSON.parse(vi.mocked(global.fetch).mock.calls[0][1]!.body as string);
    expect(body.mimeType).toBe('video/mp4');
    expect(body.size).toBe(104857600);
  });

  // ── Error handling ──────────────────────────────────────────

  it('throws on upload URL failure', async () => {
    mockFetchJson(
      { error: { message: 'File too large', code: 'size_exceeded' } },
      false,
      413,
    );

    await expect(
      service.getUploadUrl('video/mp4', 10737418240),
    ).rejects.toThrow('File too large');
  });

  it('throws on unauthorized request', async () => {
    mockFetchJson(
      { error: { message: 'Invalid API key', code: 'unauthorized' } },
      false,
      401,
    );

    await expect(service.getUploadUrl('image/png')).rejects.toThrow('Invalid API key');
  });

  it('throws AuthenticationError when API key is missing', async () => {
    vi.resetModules();
    const { StorageService: FreshStorageService } = await import('../../src/services/storage.js');
    const noKeyService = new FreshStorageService({
      baseUrl: 'https://api.scalix.world',
      environment: 'development',
      logLevel: 'info',
      defaultModel: 'auto',
      sandboxMode: 'auto',
      databaseMode: 'auto',
    });

    await expect(noKeyService.getUploadUrl('image/png')).rejects.toThrow('API key required');
  });
});
