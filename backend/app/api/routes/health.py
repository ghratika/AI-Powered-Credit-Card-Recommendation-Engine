"""Health check routes."""

from __future__ import annotations

from fastapi import APIRouter

from app.domain.ingestion import DataLoadError, load_cards

router = APIRouter(tags=["health"])


@router.get("/health")
def health_check() -> dict[str, str]:
    """Liveness probe."""
    try:
        load_cards()
        return {"status": "ok"}
    except DataLoadError:
        return {"status": "degraded"}
