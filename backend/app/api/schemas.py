"""API request and response schemas."""

from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from app.models.recommendation import CardRecommendation, RecommendationMeta


class RecommendationRequest(BaseModel):
    """POST /api/v1/recommendations body."""

    model_config = ConfigDict(extra="ignore")

    annual_income_inr: float | int | str
    pan: str
    mobile: str | int
    aa_connected: bool = False


class ErrorDetail(BaseModel):
    code: str
    message: str


class ErrorResponse(BaseModel):
    error: ErrorDetail
    request_id: str


class AAConnectResponse(BaseModel):
    connected: bool = True
    spend_profile_id: str


class RecommendationResponseOut(BaseModel):
    """OpenAPI-facing recommendation response."""

    recommendations: list[CardRecommendation]
    meta: RecommendationMeta
    generated_at: datetime
