"""FastAPI application entry point."""

from __future__ import annotations

import logging
import time
import uuid
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import Response as StarletteResponse

from app.api.errors import register_exception_handlers
from app.api.routes import aa, health, recommendations
from app.config import get_cors_origin_regex, get_cors_origins
from app.domain.ingestion import DataLoadError
from app.logging_config import configure_logging
from app.startup import validate_startup_config
import re

configure_logging()
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(_app: FastAPI):
    try:
        validate_startup_config()
    except DataLoadError as exc:
        logger.error("Startup validation failed: %s", exc)
        raise
    yield


app = FastAPI(
    title="AI Credit Card Recommendation API",
    description="FreechargeBiz-style Axis Bank card recommendations powered by Groq.",
    version="1.0.0",
    lifespan=lifespan,
)


# ---- Manual CORS middleware for bulletproof preflight handling ----

_allowed_origins: list[str] = get_cors_origins()
_origin_regex_str: str | None = get_cors_origin_regex()
_origin_regex: re.Pattern | None = (
    re.compile(_origin_regex_str) if _origin_regex_str else None
)

logger.info("CORS allowed_origins=%s", _allowed_origins)
logger.info("CORS origin_regex=%s", _origin_regex_str)


def _is_origin_allowed(origin: str) -> bool:
    """Check if origin is in the allow-list or matches the regex."""
    if origin in _allowed_origins:
        return True
    if _origin_regex and _origin_regex.fullmatch(origin):
        return True
    return False


class CORSAndLoggingMiddleware(BaseHTTPMiddleware):
    """Combined CORS + request-logging middleware.

    Handling CORS in one middleware avoids ordering issues between
    separate CORS and logging middlewares.
    """

    async def dispatch(self, request: Request, call_next):
        origin = request.headers.get("origin", "")
        request_id = request.headers.get("X-Request-ID") or str(uuid.uuid4())
        request.state.request_id = request_id
        started = time.perf_counter()

        # --- Preflight (OPTIONS) ---
        if request.method == "OPTIONS" and origin:
            if _is_origin_allowed(origin):
                response = StarletteResponse(
                    status_code=204,
                    headers={
                        "Access-Control-Allow-Origin": origin,
                        "Access-Control-Allow-Methods": "GET, POST, PUT, DELETE, OPTIONS, PATCH",
                        "Access-Control-Allow-Headers": request.headers.get(
                            "Access-Control-Request-Headers", "*"
                        ),
                        "Access-Control-Allow-Credentials": "true",
                        "Access-Control-Max-Age": "86400",
                    },
                )
            else:
                response = StarletteResponse(status_code=403)
            response.headers["X-Request-ID"] = request_id
            self._log_request(request, response, started, request_id)
            return response

        # --- Normal request ---
        response = await call_next(request)

        if origin and _is_origin_allowed(origin):
            response.headers["Access-Control-Allow-Origin"] = origin
            response.headers["Access-Control-Allow-Credentials"] = "true"
            response.headers["Vary"] = "Origin"

        response.headers["X-Request-ID"] = request_id
        self._log_request(request, response, started, request_id)
        return response

    @staticmethod
    def _log_request(request, response, started, request_id):
        duration_ms = int((time.perf_counter() - started) * 1000)
        logger.info(
            "request_complete request_id=%s method=%s path=%s status=%s duration_ms=%s",
            request_id,
            request.method,
            request.url.path,
            response.status_code,
            duration_ms,
        )


app.add_middleware(CORSAndLoggingMiddleware)

register_exception_handlers(app)


@app.get("/")
def root() -> dict[str, str]:
    """Landing page when visiting the Railway host in a browser."""
    return {
        "service": "AI Credit Card Recommendation API",
        "status": "running",
        "health": "/api/v1/health",
        "docs": "/docs",
        "recommendations": "POST /api/v1/recommendations",
    }


app.include_router(health.router, prefix="/api/v1")
app.include_router(aa.router, prefix="/api/v1")
app.include_router(recommendations.router, prefix="/api/v1")


