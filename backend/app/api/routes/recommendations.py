"""Recommendation API routes."""

from __future__ import annotations

import logging
import time

from fastapi import APIRouter, Request

from app.api.schemas import RecommendationRequest, RecommendationResponseOut
from app.domain.exceptions import InputValidationError
from app.models.user import UserProfile
from app.services.orchestrator import RecommendationOrchestrator

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/recommendations", tags=["recommendations"])


def _mask_pan(pan: str) -> str:
    if len(pan) < 10:
        return "****"
    return f"{pan[:5]}****{pan[-1]}"


def _build_profile(body: RecommendationRequest) -> UserProfile:
    try:
        return UserProfile.from_raw(
            annual_income_inr=body.annual_income_inr,
            pan=body.pan,
            mobile=body.mobile,
            aa_connected=body.aa_connected,
        )
    except InputValidationError:
        raise
    except Exception as exc:
        raise InputValidationError(str(exc)) from exc


@router.post("", response_model=RecommendationResponseOut)
def create_recommendations(
    body: RecommendationRequest,
    request: Request,
) -> RecommendationResponseOut:
    """
    Generate personalized Axis Bank credit card recommendations.

    Requires ``aa_connected: true`` (use ``POST /api/v1/aa/connect`` to simulate).
    Live inference uses Groq when ``GROQ_API_KEY`` is set; otherwise mock LLM.
    """
    profile = _build_profile(body)
    request_id = getattr(request.state, "request_id", "unknown")

    logger.info(
        "recommendation_request request_id=%s pan=%s aa_connected=%s",
        request_id,
        _mask_pan(profile.pan),
        profile.aa_connected,
    )

    started = time.perf_counter()
    result = RecommendationOrchestrator().recommend(profile)
    groq_latency_ms = int((time.perf_counter() - started) * 1000)

    logger.info(
        "recommendation_success request_id=%s eligible_count=%s groq_latency_ms=%s",
        request_id,
        result.meta.eligible_count,
        groq_latency_ms,
    )

    return RecommendationResponseOut(
        recommendations=result.recommendations,
        meta=result.meta,
        generated_at=result.generated_at,
    )
