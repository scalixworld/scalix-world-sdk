import { describe, it, expect, vi, beforeEach, afterEach } from 'vitest';
import { ModelsService } from '../../src/services/models.js';
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

describe('ModelsService', () => {
  let service: ModelsService;

  beforeEach(() => {
    service = new ModelsService(config);
    vi.restoreAllMocks();
  });

  afterEach(() => {
    vi.restoreAllMocks();
  });

  it('calls GET /v1/models and returns data array', async () => {
    const mockModels = {
      data: [
        { id: 'scalix-world-ai', object: 'model', created: 1700000000, owned_by: 'scalix', context_window: 128000, max_output_tokens: 8192, description: 'Scalix World AI', plan_required: 'free' },
        { id: 'scalix-world-advanced', object: 'model', created: 1700000000, owned_by: 'scalix', context_window: 200000, max_output_tokens: 16384, description: 'Scalix World Advanced', plan_required: 'pro' },
      ],
    };
    mockFetchJson(mockModels);

    const result = await service.list();

    expect(global.fetch).toHaveBeenCalledWith(
      'https://api.scalix.world/v1/models',
      expect.objectContaining({ method: 'GET' }),
    );
    expect(result).toEqual(mockModels.data);
    expect(result).toHaveLength(2);
    expect(result[0].plan_required).toBe('free');
    expect(result[1].context_window).toBe(200000);
  });

  it('get() returns a specific model by ID', async () => {
    const mockModels = {
      data: [
        { id: 'scalix-world-ai', object: 'model', created: 1700000000, owned_by: 'scalix', context_window: 128000, max_output_tokens: 8192, description: 'Scalix World AI', plan_required: 'free' },
        { id: 'scalix-world-advanced', object: 'model', created: 1700000000, owned_by: 'scalix', context_window: 200000, max_output_tokens: 16384, description: 'Scalix World Advanced', plan_required: 'pro' },
      ],
    };
    mockFetchJson(mockModels);

    const model = await service.get('scalix-world-advanced');
    expect(model).toBeDefined();
    expect(model!.id).toBe('scalix-world-advanced');
    expect(model!.plan_required).toBe('pro');
  });

  it('get() returns undefined for unknown model', async () => {
    mockFetchJson({ data: [] });
    const model = await service.get('nonexistent');
    expect(model).toBeUndefined();
  });

  it('throws ScalixError on non-ok response', async () => {
    mockFetchJson(
      { error: { message: 'Unauthorized', code: 'auth_error' } },
      false,
      401,
    );

    await expect(service.list()).rejects.toThrow('Unauthorized');
  });

  it('throws AuthenticationError when API key is missing', async () => {
    const noKeyService = new ModelsService({ apiKey: '', baseUrl: 'https://api.scalix.world' });
    await expect(noKeyService.list()).rejects.toThrow('API key required');
  });
});
