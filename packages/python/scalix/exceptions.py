"""Scalix SDK exceptions."""


class ScalixError(Exception):
    def __init__(self, message: str, *, code: str | None = None, status: int | None = None) -> None:
        super().__init__(message)
        self.code = code
        self.status = status


class AuthenticationError(ScalixError):
    def __init__(self, message: str) -> None:
        super().__init__(message, code="AUTHENTICATION_ERROR", status=401)


class RateLimitError(ScalixError):
    def __init__(self, message: str) -> None:
        super().__init__(message, code="RATE_LIMIT_ERROR", status=429)
