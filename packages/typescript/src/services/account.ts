import { BaseService } from './base.js';

export interface UserInfo {
  id: string;
  email: string;
  name?: string;
  plan: string;
  createdAt?: string;
}

export interface UserBudget {
  creditsUsed: number;
  creditsLimit: number;
  creditsRemaining: number;
  resetDate?: string;
}

export interface UserUsage {
  month: string;
  totalRequests: number;
  totalTokens: number;
  breakdown: Record<string, unknown>;
}

export class AccountService extends BaseService {

  async health(): Promise<Record<string, unknown>> {
    return this.request('GET', '/health');
  }

  async info(): Promise<UserInfo> {
    return this.request<UserInfo>('GET', '/v1/user/info');
  }

  async budget(): Promise<UserBudget> {
    return this.request<UserBudget>('GET', '/v1/user/budget');
  }

  async usage(): Promise<UserUsage> {
    return this.request<UserUsage>('GET', '/v1/user/stats');
  }
}
