"""Recommendation API and LLM response models."""

from __future__ import annotations

from datetime import datetime, timezone

from pydantic import BaseModel, Field


class CardRecommendation(BaseModel):
    """Single ranked card recommendation."""

    rank: int = Field(..., ge=1)
    card_id: str
    card_name: str
    image_url: str
    reward_rate_percent: float = Field(..., ge=0, description="Best earn rate from card catalog")
    apr_percent: float = Field(..., ge=0, description="Annual percentage rate from card catalog")
    confidence_score: float = Field(..., ge=0, le=1)
    net_annual_benefit_inr: float
    explanation: str = Field(..., min_length=1)


class RecommendationMeta(BaseModel):
    """Metadata about the recommendation run."""

    eligible_count: int = Field(..., ge=0)
    aa_connected: bool
    disclaimer: str = "Simulated recommendations for demonstration only."


class RecommendationResponse(BaseModel):
    """Final recommendation payload returned to clients."""

    recommendations: list[CardRecommendation]
    meta: RecommendationMeta
    generated_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
    )


class LLMRecommendationItem(BaseModel):
    """Raw recommendation item from LLM JSON (pre-normalization)."""

    rank: int | None = None
    card_id: str
    card_name: str | None = None
    confidence_score: float
    net_annual_benefit_inr: float
    explanation: str | None = None


class LLMRecommendationsPayload(BaseModel):
    """Expected top-level JSON from the LLM."""

    recommendations: list[LLMRecommendationItem]
