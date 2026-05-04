export class ScalixError extends Error {
  code?: string;
  status?: number;
  requestId?: string;

  constructor(message: string, options?: { code?: string; status?: number; requestId?: string }) {
    super(message);
    this.name = 'ScalixError';
    this.code = options?.code;
    this.status = options?.status;
    this.requestId = options?.requestId;
  }
}

export class AuthenticationError extends ScalixError {
  constructor(message: string, requestId?: string) {
    super(message, { code: 'AUTHENTICATION_ERROR', status: 401, requestId });
    this.name = 'AuthenticationError';
  }
}

export class BadRequestError extends ScalixError {
  constructor(message: string, requestId?: string) {
    super(message, { code: 'BAD_REQUEST', status: 400, requestId });
    this.name = 'BadRequestError';
  }
}

export class PermissionDeniedError extends ScalixError {
  constructor(message: string, requestId?: string) {
    super(message, { code: 'PERMISSION_DENIED', status: 403, requestId });
    this.name = 'PermissionDeniedError';
  }
}

export class NotFoundError extends ScalixError {
  constructor(message: string, requestId?: string) {
    super(message, { code: 'NOT_FOUND', status: 404, requestId });
    this.name = 'NotFoundError';
  }
}

export class ConflictError extends ScalixError {
  constructor(message: string, requestId?: string) {
    super(message, { code: 'CONFLICT', status: 409, requestId });
    this.name = 'ConflictError';
  }
}

export class UnprocessableEntityError extends ScalixError {
  constructor(message: string, requestId?: string) {
    super(message, { code: 'UNPROCESSABLE_ENTITY', status: 422, requestId });
    this.name = 'UnprocessableEntityError';
  }
}

export class RateLimitError extends ScalixError {
  constructor(message: string, requestId?: string) {
    super(message, { code: 'RATE_LIMIT_ERROR', status: 429, requestId });
    this.name = 'RateLimitError';
  }
}

export class InternalServerError extends ScalixError {
  constructor(message: string, requestId?: string) {
    super(message, { code: 'INTERNAL_SERVER_ERROR', status: 500, requestId });
    this.name = 'InternalServerError';
  }
}
