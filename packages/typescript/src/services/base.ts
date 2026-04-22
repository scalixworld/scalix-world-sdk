import { getConfig, type ScalixConfig } from '../config.js';
import { AuthenticationError, ScalixError } from '../errors.js';

export class BaseService {
  protected config: ScalixConfig;

  constructor(config?: ScalixConfig) {
    this.config = config ?? getConfig();
  }

  protected async request<T>(
    method: string,
    path: string,
    options?: { body?: unknown; headers?: Record<string, string> },
  ): Promise<T> {
    if (!this.config.apiKey) {
      throw new AuthenticationError('API key required. Call configure({ apiKey: "..." }) first.');
    }

    const url = `${this.config.baseUrl}${path}`;
    const headers: Record<string, string> = {
      Authorization: `Bearer ${this.config.apiKey}`,
      'Content-Type': 'application/json',
      ...options?.headers,
    };

    const resp = await fetch(url, {
      method,
      headers,
      ...(options?.body ? { body: JSON.stringify(options.body) } : {}),
    });

    if (!resp.ok) {
      const body = await resp.json().catch(() => ({})) as { error?: { message?: string; code?: string } };
      throw new ScalixError(
        body?.error?.message ?? `Request failed: ${resp.status}`,
        { code: body?.error?.code },
      );
    }

    return resp.json() as Promise<T>;
  }

  protected async requestRaw(
    method: string,
    path: string,
    options?: { body?: unknown; headers?: Record<string, string> },
  ): Promise<Response> {
    if (!this.config.apiKey) {
      throw new AuthenticationError('API key required.');
    }

    const url = `${this.config.baseUrl}${path}`;
    const headers: Record<string, string> = {
      Authorization: `Bearer ${this.config.apiKey}`,
      'Content-Type': 'application/json',
      ...options?.headers,
    };

    const resp = await fetch(url, {
      method,
      headers,
      ...(options?.body ? { body: JSON.stringify(options.body) } : {}),
    });

    if (!resp.ok) {
      const body = await resp.json().catch(() => ({})) as { error?: { message?: string; code?: string } };
      throw new ScalixError(
        body?.error?.message ?? `Request failed: ${resp.status}`,
        { code: body?.error?.code },
      );
    }

    return resp;
  }

  protected async requestMultipart<T>(
    path: string,
    formData: FormData,
  ): Promise<T> {
    if (!this.config.apiKey) {
      throw new AuthenticationError('API key required.');
    }

    const url = `${this.config.baseUrl}${path}`;
    const resp = await fetch(url, {
      method: 'POST',
      headers: { Authorization: `Bearer ${this.config.apiKey}` },
      body: formData,
    });

    if (!resp.ok) {
      const body = await resp.json().catch(() => ({})) as { error?: { message?: string; code?: string } };
      throw new ScalixError(
        body?.error?.message ?? `Upload failed: ${resp.status}`,
        { code: body?.error?.code },
      );
    }

    return resp.json() as Promise<T>;
  }
}
