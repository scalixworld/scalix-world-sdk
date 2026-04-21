"""Scalix SDK exception hierarchy."""


class ScalixError(Exception):
    """Base exception for all Scalix SDK errors."""

    def __init__(self, message: str, *, code: str | None = None) -> None:
        self.code = code
        super().__init__(message)


class ConfigurationError(ScalixError):
    """Raised when SDK configuration is invalid or incomplete."""


class AuthenticationError(ScalixError):
    """Raised when API key is invalid or missing for cloud operations."""


class ProviderError(ScalixError):
    """Base exception for provider-specific errors."""


class SandboxError(ProviderError):
    """Raised when code execution in sandbox fails."""


class SandboxTimeoutError(SandboxError):
    """Raised when sandbox execution exceeds timeout."""


class SandboxResourceError(SandboxError):
    """Raised when sandbox hits resource limits (memory, CPU, storage)."""


class RouterError(ProviderError):
    """Raised when LLM routing fails."""


class ModelNotFoundError(RouterError):
    """Raised when requested model is unavailable."""


class RateLimitError(RouterError):
    """Raised when rate limit is exceeded."""


class QuotaExceededError(RouterError):
    """Raised when usage quota is exceeded."""


class DatabaseError(ProviderError):
    """Raised when database operations fail."""


class ToolError(ScalixError):
    """Raised when tool execution fails."""


class DeploymentError(ScalixError):
    """Raised when deployment operations fail."""
