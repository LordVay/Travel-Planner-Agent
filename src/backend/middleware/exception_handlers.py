# Custom error screens / exception handlers for the API.
# Purpose: Never expose internal stack traces, model names, or server details to clients.
# All errors are sanitized into a consistent JSON format before reaching the caller.

import logging

from fastapi import Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException

logger = logging.getLogger("travelagent")


async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """Handles Pydantic validation failures (malformed input, failed sanitization).
    Returns field-level error messages without exposing internal model structure."""
    errors = []
    for error in exc.errors():
        errors.append({
            "field": ".".join(str(loc) for loc in error["loc"] if loc != "body"),
            "message": error["msg"],
        })
    return JSONResponse(
        status_code=422,
        content={"error": "Validation Error", "detail": errors},
    )


async def http_exception_handler(request: Request, exc: StarletteHTTPException):
    """Handles explicitly raised HTTP exceptions.
    For 4xx errors: shows the detail message (safe, developer-controlled).
    For 5xx errors: hides the real detail and returns a generic message."""
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": exc.detail if exc.status_code < 500 else "Internal Server Error",
        },
    )


async def unhandled_exception_handler(request: Request, exc: Exception):
    """Catch-all for unexpected crashes (unhandled exceptions).
    Logs the full traceback server-side for debugging, but returns only a
    generic message to the client — preventing information leakage."""
    logger.error(
        f"Unhandled exception on {request.method} {request.url.path}",
        exc_info=exc,
    )
    return JSONResponse(
        status_code=500,
        content={"error": "An unexpected error occurred. Please try again later."},
    )
