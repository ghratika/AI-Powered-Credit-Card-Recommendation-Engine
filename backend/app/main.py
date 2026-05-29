"""FastAPI application entry point."""

from __future__ import annotations

import logging
import time
import uuid
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware

from app.api.errors import register_exception_handlers
from app.api.routes import aa, health, recommendations
from app.config import get_cors_origin_regex, get_cors_origins
from app.domain.ingestion import DataLoadError
from app.logging_config import configure_logging
from app.startup import validate_startup_config

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

_cors_kwargs: dict = {
    "allow_credentials": True,
    "allow_methods": ["*"],
    "allow_headers": ["*"],
}
_origin_regex = get_cors_origin_regex()
if _origin_regex:
    _cors_kwargs["allow_origin_regex"] = _origin_regex
    _cors_kwargs["allow_origins"] = get_cors_origins()
else:
    _cors_kwargs["allow_origins"] = get_cors_origins()

app.add_middleware(CORSMiddleware, **_cors_kwargs)


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
