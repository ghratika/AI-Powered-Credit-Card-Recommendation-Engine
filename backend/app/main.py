"""FastAPI application entry point."""

from __future__ import annotations

import logging
import re
import time
import uuid
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request

from app.api.errors import register_exception_handlers
from app.api.routes import aa, health, recommendations
from app.config import get_cors_origin_regex, get_cors_origins
from app.domain.ingestion import DataLoadError
from app.logging_config import configure_logging
from app.startup import validate_startup_config

configure_logging()
logger = logging.getLogger(__name__)


# ---- CORS configuration ----

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


# ---- Pure ASGI CORS middleware (bypasses all Starlette/BaseHTTPMiddleware issues) ----

class RawCORSMiddleware:
    """Raw ASGI middleware that handles CORS at the lowest level.

    This avoids all known issues with Starlette's BaseHTTPMiddleware
    and CORSMiddleware when combined with other middleware.
    """

    def __init__(self, app):
        self.app = app

    async def __call__(self, scope, receive, send):
        if scope["type"] != "http":
            await self.app(scope, receive, send)
            return

        # Parse headers from raw ASGI scope
        raw_headers = dict(scope.get("headers", []))
        origin = raw_headers.get(b"origin", b"").decode("latin-1")
        method = scope.get("method", "GET")

        logger.debug("CORS check: method=%s origin=%s path=%s", method, origin, scope.get("path"))

        # ---- OPTIONS preflight: respond immediately, never forward ----
        if method == "OPTIONS" and origin:
            allowed = _is_origin_allowed(origin)
            logger.info("CORS preflight: origin=%s allowed=%s path=%s", origin, allowed, scope.get("path"))

            if allowed:
                acr_headers = raw_headers.get(b"access-control-request-headers", b"*")
                response_headers = [
                    (b"access-control-allow-origin", origin.encode("latin-1")),
                    (b"access-control-allow-methods", b"GET, POST, PUT, DELETE, OPTIONS, PATCH"),
                    (b"access-control-allow-headers", acr_headers),
                    (b"access-control-allow-credentials", b"true"),
                    (b"access-control-max-age", b"86400"),
                    (b"content-length", b"0"),
                ]
                await send({"type": "http.response.start", "status": 204, "headers": response_headers})
                await send({"type": "http.response.body", "body": b""})
            else:
                await send({
                    "type": "http.response.start",
                    "status": 403,
                    "headers": [(b"content-length", b"0")],
                })
                await send({"type": "http.response.body", "body": b""})
            return

        # ---- Normal request: forward and inject CORS headers into response ----
        if origin and _is_origin_allowed(origin):
            cors_headers = [
                (b"access-control-allow-origin", origin.encode("latin-1")),
                (b"access-control-allow-credentials", b"true"),
                (b"vary", b"Origin"),
            ]

            async def send_with_cors(message):
                if message["type"] == "http.response.start":
                    headers = list(message.get("headers", []))
                    headers.extend(cors_headers)
                    message = {**message, "headers": headers}
                await send(message)

            await self.app(scope, receive, send_with_cors)
        else:
            await self.app(scope, receive, send)


# ---- App setup ----

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


# Request logging middleware (simple, cannot interfere with CORS)
@app.middleware("http")
async def request_logging_middleware(request: Request, call_next):
    request_id = request.headers.get("X-Request-ID") or str(uuid.uuid4())
    request.state.request_id = request_id
    started = time.perf_counter()
    response = await call_next(request)
    duration_ms = int((time.perf_counter() - started) * 1000)
    response.headers["X-Request-ID"] = request_id
    logger.info(
        "request_complete request_id=%s method=%s path=%s status=%s duration_ms=%s",
        request_id,
        request.method,
        request.url.path,
        response.status_code,
        duration_ms,
    )
    return response


# RawCORSMiddleware added LAST so it's the OUTERMOST layer.
# It intercepts OPTIONS before anything else sees the request.
app.add_middleware(RawCORSMiddleware)

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
