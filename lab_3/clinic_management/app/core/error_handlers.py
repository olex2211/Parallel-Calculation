from datetime import datetime, timezone

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from app.core.exceptions import (
    BusinessRuleException,
    ConflictException,
    EntityNotFoundException,
)

_EXCEPTION_MAP: dict[type[Exception], tuple[int, str]] = {
    EntityNotFoundException: (404, "NOT_FOUND"),
    BusinessRuleException:  (422, "BUSINESS_RULE_VIOLATION"),
    ConflictException:      (409, "CONFLICT"),
}


def _build_error_body(
    request: Request, status_code: int, error: str, message: str,
) -> dict:
    return {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "status": status_code,
        "error": error,
        "message": message,
        "path": request.url.path,
    }


def register_exception_handlers(app: FastAPI) -> None:
    """Реєструє глобальні обробники помилок."""

    for exc_class, (status_code, error_code) in _EXCEPTION_MAP.items():
        app.add_exception_handler(
            exc_class,
            _make_handler(status_code, error_code),
        )

    @app.exception_handler(Exception)
    async def unhandled_exception_handler(
        request: Request, exc: Exception,
    ) -> JSONResponse:
        return JSONResponse(
            status_code=500,
            content=_build_error_body(
                request, 500, "INTERNAL_SERVER_ERROR",
                "An unexpected error occurred. Please try again later.",
            ),
        )


def _make_handler(status_code: int, error_code: str):
    async def handler(request: Request, exc: Exception) -> JSONResponse:
        return JSONResponse(
            status_code=status_code,
            content=_build_error_body(request, status_code, error_code, str(exc)),
        )
    return handler
