"""Map domain exceptions to HTTP error responses."""

from __future__ import annotations

from fastapi import Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from app.api.schemas import ErrorDetail, ErrorResponse
from app.domain.exceptions import (
    AANotConnectedError,
    DataUnavailableError,
    DomainError,
    InputValidationError,
    LLMServiceError,
    NoEligibleCardsError,
)


def _request_id(request: Request) -> str:
    return getattr(request.state, "request_id", "unknown")


def _error_response(
    request: Request,
    *,
    status_code: int,
    code: str,
    message: str,
) -> JSONResponse:
    body = ErrorResponse(
        error=ErrorDetail(code=code, message=message),
        request_id=_request_id(request),
    )
    return JSONResponse(status_code=status_code, content=body.model_dump())


def register_exception_handlers(app) -> None:
    @app.exception_handler(InputValidationError)
    async def input_validation_handler(
        request: Request, exc: InputValidationError
    ) -> JSONResponse:
        return _error_response(
            request,
            status_code=400,
            code="VALIDATION_ERROR",
            message=str(exc),
        )

    @app.exception_handler(RequestValidationError)
    async def pydantic_validation_handler(
        request: Request, exc: RequestValidationError
    ) -> JSONResponse:
        errors = exc.errors()
        message = errors[0]["msg"] if errors else "Invalid request body"
        return _error_response(
            request,
            status_code=400,
            code="VALIDATION_ERROR",
            message=message,
        )

    @app.exception_handler(AANotConnectedError)
    async def aa_not_connected_handler(
        request: Request, exc: AANotConnectedError
    ) -> JSONResponse:
        return _error_response(
            request,
            status_code=422,
            code=exc.code,
            message=exc.message,
        )

    @app.exception_handler(NoEligibleCardsError)
    async def no_eligible_handler(
        request: Request, exc: NoEligibleCardsError
    ) -> JSONResponse:
        return _error_response(
            request,
            status_code=404,
            code=exc.code,
            message=exc.message,
        )

    @app.exception_handler(LLMServiceError)
    async def llm_error_handler(request: Request, exc: LLMServiceError) -> JSONResponse:
        return _error_response(
            request,
            status_code=502,
            code=exc.code,
            message=exc.message,
        )

    @app.exception_handler(DataUnavailableError)
    async def data_unavailable_handler(
        request: Request, exc: DataUnavailableError
    ) -> JSONResponse:
        return _error_response(
            request,
            status_code=503,
            code=exc.code,
            message=exc.message,
        )

    @app.exception_handler(DomainError)
    async def domain_error_handler(request: Request, exc: DomainError) -> JSONResponse:
        return _error_response(
            request,
            status_code=500,
            code=exc.code,
            message=exc.message,
        )

    @app.exception_handler(Exception)
    async def unhandled_handler(request: Request, exc: Exception) -> JSONResponse:
        return _error_response(
            request,
            status_code=500,
            code="INTERNAL_ERROR",
            message="An unexpected error occurred.",
        )
