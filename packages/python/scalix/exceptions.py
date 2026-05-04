"""Scalix SDK exceptions."""

from __future__ import annotations


class ScalixError(Exception):
    def __init__(
        self,
        message: str,
        *,
        code: str | None = None,
        status: int | None = None,
        request_id: str | None = None,
    ) -> None:
        super().__init__(message)
        self.code = code
        self.status = status
        self.request_id = request_id


class BadRequestError(ScalixError):
    def __init__(self, message: str, request_id: str | None = None) -> None:
        super().__init__(message, code="BAD_REQUEST", status=400, request_id=request_id)


class AuthenticationError(ScalixError):
    def __init__(self, message: str, request_id: str | None = None) -> None:
        super().__init__(message, code="AUTHENTICATION_ERROR", status=401, request_id=request_id)


class PermissionDeniedError(ScalixError):
    def __init__(self, message: str, request_id: str | None = None) -> None:
        super().__init__(message, code="PERMISSION_DENIED", status=403, request_id=request_id)


class NotFoundError(ScalixError):
    def __init__(self, message: str, request_id: str | None = None) -> None:
        super().__init__(message, code="NOT_FOUND", status=404, request_id=request_id)


class ConflictError(ScalixError):
    def __init__(self, message: str, request_id: str | None = None) -> None:
        super().__init__(message, code="CONFLICT", status=409, request_id=request_id)


class UnprocessableEntityError(ScalixError):
    def __init__(self, message: str, request_id: str | None = None) -> None:
        super().__init__(message, code="UNPROCESSABLE_ENTITY", status=422, request_id=request_id)


class RateLimitError(ScalixError):
    def __init__(self, message: str, request_id: str | None = None) -> None:
        super().__init__(message, code="RATE_LIMIT_ERROR", status=429, request_id=request_id)


class InternalServerError(ScalixError):
    def __init__(self, message: str, request_id: str | None = None) -> None:
        super().__init__(message, code="INTERNAL_SERVER_ERROR", status=500, request_id=request_id)
