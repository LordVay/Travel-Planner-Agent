# FastAPI application entry point with security middleware stack.
# This file wires together: CORS restriction, rate limiting, input validation,
# custom error handlers, and structured logging — forming the security layer.

import logging

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded

from .api.backend_api import router as backend_router
from .config.back_config import Settings
from .middleware.rate_limit import limiter
from .middleware.exception_handlers import (
    validation_exception_handler,
    http_exception_handler,
    unhandled_exception_handler,
)
from .middleware.logging_config import setup_logging

# Initialize structured logging before anything else so all startup messages are captured
setup_logging()
logger = logging.getLogger("travelagent")

# Load configuration from .env and warn if API keys need rotation
settings = Settings()
settings.warn_if_keys_not_rotated()

app = FastAPI(
    title="TravelAgent API",
    # Disable Swagger docs in production to avoid exposing API structure publicly
    docs_url="/docs" if settings.API_HOST == "localhost" else None,
    redoc_url=None,
)

# CORS: Restrict which domains can call this API (prevents unauthorized cross-origin requests)
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origin_list,  # Configured via CORS_ORIGINS in .env
    allow_credentials=True,
    allow_methods=["POST"],         # Only POST is used — blocks GET/PUT/DELETE from other origins
    allow_headers=["Content-Type"],
)

# Rate limiting: Prevents API abuse by capping requests per IP (returns 429 when exceeded)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# Custom error handlers: Sanitize all error responses to prevent information leakage
app.add_exception_handler(RequestValidationError, validation_exception_handler)
app.add_exception_handler(StarletteHTTPException, http_exception_handler)
app.add_exception_handler(Exception, unhandled_exception_handler)

# Register API routes
app.include_router(backend_router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app="src.backend.main:app", host=settings.API_HOST, port=settings.API_PORT)
