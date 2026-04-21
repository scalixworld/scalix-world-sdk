/**
 * Scalix SDK error hierarchy.
 */

export class ScalixError extends Error {
  code?: string;

  constructor(message: string, options?: { code?: string }) {
    super(message);
    this.name = 'ScalixError';
    this.code = options?.code;
  }
}

export class ConfigurationError extends ScalixError {
  constructor(message: string) {
    super(message, { code: 'CONFIGURATION_ERROR' });
    this.name = 'ConfigurationError';
  }
}

export class AuthenticationError extends ScalixError {
  constructor(message: string) {
    super(message, { code: 'AUTHENTICATION_ERROR' });
    this.name = 'AuthenticationError';
  }
}

export class ProviderError extends ScalixError {
  constructor(message: string, code?: string) {
    super(message, { code: code ?? 'PROVIDER_ERROR' });
    this.name = 'ProviderError';
  }
}

export class SandboxError extends ProviderError {
  constructor(message: string) {
    super(message, 'SANDBOX_ERROR');
    this.name = 'SandboxError';
  }
}

export class RouterError extends ProviderError {
  constructor(message: string) {
    super(message, 'ROUTER_ERROR');
    this.name = 'RouterError';
  }
}

export class ToolError extends ScalixError {
  constructor(message: string) {
    super(message, { code: 'TOOL_ERROR' });
    this.name = 'ToolError';
  }
}

export class DeploymentError extends ScalixError {
  constructor(message: string) {
    super(message, { code: 'DEPLOYMENT_ERROR' });
    this.name = 'DeploymentError';
  }
}
