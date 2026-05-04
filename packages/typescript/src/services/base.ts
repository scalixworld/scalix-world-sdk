import type { ScalixConfig } from '../config.js';
import {
  AuthenticationError,
  BadRequestError,
  ConflictError,
  InternalServerError,
  NotFoundError,
  PermissionDeniedError,
  RateLimitError,
  ScalixError,
  UnprocessableEntityError,
} from '../errors.js';

const RETRYABLE_STATUS_CODES = new Set([408, 409, 429, 500, 502, 503, 504]);

function sleep(ms: number): Promise<void> {
  return new Promise(resolve => setTimeout(resolve, ms));
}

function backoffDelay(attempt: number, retryAfter?: number): number {
  if (retryAfter !== undefined) return retryAfter * 1000;
  const base = Math.min(0.5 * Math.pow(2, attempt), 8);
  return base * (0.5 + Math.random() * 0.5) * 1000;
}

function throwForStatus(
  status: number,
  message: string,
  requestId?: string,
): never {
  switch (status) {
    case 400: throw new BadRequestError(message, requestId);
    case 401: throw new AuthenticationError(message, requestId);
    case 403: throw new PermissionDeniedError(message, requestId);
    case 404: throw new NotFoundError(message, requestId);
    case 409: throw new ConflictError(message, requestId);
    case 422: throw new UnprocessableEntityError(message, requestId);
    case 429: throw new RateLimitError(message, requestId);
    default:
      if (status >= 500) throw new InternalServerError(message, requestId);
      throw new ScalixError(message, { status, requestId });
  }
}

export class BaseService {
  protected config: ScalixConfig;

  constructor(config: ScalixConfig) {
    this.config = config;
  }

  private get maxRetries(): number {
    return this.config.maxRetries ?? 2;
  }

  private get timeout(): number {
    return this.config.timeout ?? 60000;
  }

  protected async request<T>(
    method: string,
    path: string,
    options?: { body?: unknown; headers?: Record<string, string> },
  ): Promise<T> {
    if (!this.config.apiKey) {
      throw new AuthenticationError('API key required. Pass apiKey to new Scalix("sk_scalix_...").');
    }

    const url = `${this.config.baseUrl}${path}`;
    const headers: Record<string, string> = {
      Authorization: `Bearer ${this.config.apiKey}`,
      'Content-Type': 'application/json',
      ...options?.headers,
    };

    let lastError: Error | undefined;

    for (let attempt = 0; attempt <= this.maxRetries; attempt++) {
      if (attempt > 0) {
        await sleep(backoffDelay(attempt - 1, lastError instanceof RateLimitError ? undefined : undefined));
      }

      let resp: Response;
      try {
        resp = await fetch(url, {
          method,
          headers,
          ...(options?.body ? { body: JSON.stringify(options.body) } : {}),
          signal: AbortSignal.timeout(this.timeout),
        });
      } catch (err) {
        lastError = err instanceof Error ? err : new Error(String(err));
        if (attempt < this.maxRetries) continue;
        throw new ScalixError(`Connection failed: ${lastError.message}`);
      }

      if (resp.ok) {
        return resp.json() as Promise<T>;
      }

      const requestId = resp.headers.get('x-request-id') ?? undefined;
      const body = await resp.json().catch(() => ({})) as { error?: { message?: string; code?: string } };
      const message = body?.error?.message ?? `Request failed: ${resp.status}`;

      if (attempt < this.maxRetries && RETRYABLE_STATUS_CODES.has(resp.status)) {
        const retryAfter = resp.headers.get('retry-after');
        lastError = new ScalixError(message, { status: resp.status, requestId });
        await sleep(backoffDelay(attempt, retryAfter ? parseFloat(retryAfter) : undefined));
        continue;
      }

      throwForStatus(resp.status, message, requestId);
    }

    throw lastError ?? new ScalixError('Request failed after retries');
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

    let lastError: Error | undefined;

    for (let attempt = 0; attempt <= this.maxRetries; attempt++) {
      let resp: Response;
      try {
        resp = await fetch(url, {
          method,
          headers,
          ...(options?.body ? { body: JSON.stringify(options.body) } : {}),
          signal: AbortSignal.timeout(this.timeout),
        });
      } catch (err) {
        lastError = err instanceof Error ? err : new Error(String(err));
        if (attempt < this.maxRetries) {
          await sleep(backoffDelay(attempt));
          continue;
        }
        throw new ScalixError(`Connection failed: ${lastError.message}`);
      }

      if (resp.ok) return resp;

      const requestId = resp.headers.get('x-request-id') ?? undefined;
      const body = await resp.json().catch(() => ({})) as { error?: { message?: string; code?: string } };
      const message = body?.error?.message ?? `Request failed: ${resp.status}`;

      if (attempt < this.maxRetries && RETRYABLE_STATUS_CODES.has(resp.status)) {
        const retryAfter = resp.headers.get('retry-after');
        lastError = new ScalixError(message, { status: resp.status, requestId });
        await sleep(backoffDelay(attempt, retryAfter ? parseFloat(retryAfter) : undefined));
        continue;
      }

      throwForStatus(resp.status, message, requestId);
    }

    throw lastError ?? new ScalixError('Request failed after retries');
  }

  protected async requestMultipart<T>(
    path: string,
    formData: FormData,
  ): Promise<T> {
    if (!this.config.apiKey) {
      throw new AuthenticationError('API key required.');
    }

    const url = `${this.config.baseUrl}${path}`;
    let lastError: Error | undefined;

    for (let attempt = 0; attempt <= this.maxRetries; attempt++) {
      let resp: Response;
      try {
        resp = await fetch(url, {
          method: 'POST',
          headers: { Authorization: `Bearer ${this.config.apiKey}` },
          body: formData,
          signal: AbortSignal.timeout(this.timeout),
        });
      } catch (err) {
        lastError = err instanceof Error ? err : new Error(String(err));
        if (attempt < this.maxRetries) {
          await sleep(backoffDelay(attempt));
          continue;
        }
        throw new ScalixError(`Connection failed: ${lastError.message}`);
      }

      if (resp.ok) {
        return resp.json() as Promise<T>;
      }

      const requestId = resp.headers.get('x-request-id') ?? undefined;
      const body = await resp.json().catch(() => ({})) as { error?: { message?: string; code?: string } };
      const message = body?.error?.message ?? `Upload failed: ${resp.status}`;

      if (attempt < this.maxRetries && RETRYABLE_STATUS_CODES.has(resp.status)) {
        const retryAfter = resp.headers.get('retry-after');
        lastError = new ScalixError(message, { status: resp.status, requestId });
        await sleep(backoffDelay(attempt, retryAfter ? parseFloat(retryAfter) : undefined));
        continue;
      }

      throwForStatus(resp.status, message, requestId);
    }

    throw lastError ?? new ScalixError('Request failed after retries');
  }
}
