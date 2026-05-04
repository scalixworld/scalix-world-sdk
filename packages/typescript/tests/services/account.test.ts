import { describe, it, expect, vi, beforeEach, afterEach } from 'vitest';
import { AccountService } from '../../src/services/account.js';
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

describe('AccountService', () => {
  let service: AccountService;

  beforeEach(() => {
    service = new AccountService(config);
    vi.restoreAllMocks();
  });

  afterEach(() => {
    vi.restoreAllMocks();
  });

  it('health() calls GET /health', async () => {
    mockFetchJson({ status: 'ok', version: '2.0.0' });

    const result = await service.health();

    expect(global.fetch).toHaveBeenCalledWith(
      'https://api.scalix.world/health',
      expect.objectContaining({ method: 'GET' }),
    );
    expect(result.status).toBe('ok');
  });

  it('info() calls GET /v1/user/info', async () => {
    const mockUser = {
      id: 'user-123',
      email: 'dev@example.com',
      name: 'Test User',
      plan: 'pro',
      createdAt: '2026-01-01T00:00:00Z',
    };
    mockFetchJson(mockUser);

    const result = await service.info();

    expect(global.fetch).toHaveBeenCalledWith(
      'https://api.scalix.world/v1/user/info',
      expect.objectContaining({ method: 'GET' }),
    );
    expect(result.id).toBe('user-123');
    expect(result.plan).toBe('pro');
  });

  it('budget() calls GET /v1/user/budget', async () => {
    const mockBudget = {
      creditsUsed: 1500,
      creditsLimit: 10000,
      creditsRemaining: 8500,
      resetDate: '2026-06-01',
    };
    mockFetchJson(mockBudget);

    const result = await service.budget();

    expect(global.fetch).toHaveBeenCalledWith(
      'https://api.scalix.world/v1/user/budget',
      expect.objectContaining({ method: 'GET' }),
    );
    expect(result.creditsRemaining).toBe(8500);
  });

  it('usage() calls GET /v1/user/stats', async () => {
    const mockUsage = {
      month: '2026-05',
      totalRequests: 420,
      totalTokens: 125000,
      breakdown: { ai: 300, research: 100, docgen: 20 },
    };
    mockFetchJson(mockUsage);

    const result = await service.usage();

    expect(global.fetch).toHaveBeenCalledWith(
      'https://api.scalix.world/v1/user/stats',
      expect.objectContaining({ method: 'GET' }),
    );
    expect(result.totalRequests).toBe(420);
  });

  it('throws AuthenticationError when API key is missing', async () => {
    const noKeyService = new AccountService({ apiKey: '', baseUrl: 'https://api.scalix.world' });
    await expect(noKeyService.info()).rejects.toThrow('API key required');
  });
});
