import { BaseService } from './base.js';

export class AccountService extends BaseService {

  async health(): Promise<Record<string, unknown>> {
    return this.request('GET', '/health');
  }

  // ── API Key Management ──

  async listApiKeys(): Promise<Record<string, unknown>> {
    return this.request('GET', '/api/dashboard/api-keys');
  }

  async createApiKey(options: {
    name: string;
    expiresAt?: string;
  }): Promise<Record<string, unknown>> {
    const body: Record<string, unknown> = { name: options.name };
    if (options.expiresAt) body.expires_at = options.expiresAt;
    return this.request('POST', '/api/dashboard/api-keys', { body });
  }

  async deleteApiKey(keyId: string): Promise<Record<string, unknown>> {
    return this.request('DELETE', `/api/dashboard/api-keys/${keyId}`);
  }

  // ── Usage & Billing ──

  async usage(options?: {
    startDate?: string;
    endDate?: string;
  }): Promise<Record<string, unknown>> {
    const params = new URLSearchParams();
    if (options?.startDate) params.set('start_date', options.startDate);
    if (options?.endDate) params.set('end_date', options.endDate);
    const qs = params.toString();
    return this.request('GET', `/api/billing/usage${qs ? `?${qs}` : ''}`);
  }
}
