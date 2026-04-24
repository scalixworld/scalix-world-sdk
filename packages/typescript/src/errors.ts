export class ScalixError extends Error {
  code?: string;
  status?: number;

  constructor(message: string, options?: { code?: string; status?: number }) {
    super(message);
    this.name = 'ScalixError';
    this.code = options?.code;
    this.status = options?.status;
  }
}

export class AuthenticationError extends ScalixError {
  constructor(message: string) {
    super(message, { code: 'AUTHENTICATION_ERROR', status: 401 });
    this.name = 'AuthenticationError';
  }
}

export class RateLimitError extends ScalixError {
  constructor(message: string) {
    super(message, { code: 'RATE_LIMIT_ERROR', status: 429 });
    this.name = 'RateLimitError';
  }
}
