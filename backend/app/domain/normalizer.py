"""Normalize and validate LLM recommendation output."""

from __future__ import annotations

import json
import logging
import re
from typing import Any

from pydantic import ValidationError

from app.models.card import CardProduct
from app.models.recommendation import (
    CardRecommendation,
    LLMRecommendationsPayload,
    RecommendationMeta,
    RecommendationResponse,
)
from app.models.user import UserProfile

logger = logging.getLogger(__name__)


def strip_json_fences(text: str) -> str:
    """Remove markdown code fences if present (L-17)."""
    stripped = text.strip()
    match = re.search(r"```(?:json)?\s*([\s\S]*?)\s*```", stripped, re.IGNORECASE)
    if match:
        return match.group(1).strip()
    return stripped


def parse_llm_json(raw: str) -> dict[str, Any]:
    """Parse LLM text into a JSON object."""
    cleaned = strip_json_fences(raw)
    return json.loads(cleaned)


def _best_reward_rate(card: CardProduct) -> float:
    """Highest earn rate across default and category-specific rewards."""
    rates = [card.default_earn_rate_percent]
    rates.extend(rc.rate_percent for rc in card.reward_categories)
    return max(rates) if rates else card.default_earn_rate_percent


def _clamp_confidence(value: float) -> float:
    if value > 1.0:
        if value <= 100.0:
            value = value / 100.0
    return max(0.0, min(1.0, value))


def normalize_recommendations(
    raw_payload: dict[str, Any],
    catalog_by_id: dict[str, CardProduct],
    *,
    top_n: int,
    profile: UserProfile,
    eligible_count: int,
) -> RecommendationResponse:
    """
    Validate LLM JSON, enrich from catalog, sort, and cap to top N.

    Drops recommendations whose card_id is not in the eligible catalog (L-04).
    """
    try:
        parsed = LLMRecommendationsPayload.model_validate(raw_payload)
    except ValidationError as exc:
        raise ValueError(f"LLM payload validation failed: {exc}") from exc

    normalized: list[CardRecommendation] = []
    for index, item in enumerate(parsed.recommendations):
        card = catalog_by_id.get(item.card_id.strip().lower())
        if card is None:
            logger.warning("Dropping unknown card_id from LLM output: %s", item.card_id)
            continue

        rank = item.rank if item.rank is not None else index + 1
        explanation = (item.explanation or "").strip()
        if not explanation:
            explanation = (
                f"Based on your spending pattern, {card.name} aligns with your "
                f"profile and reward categories."
            )

        normalized.append(
            CardRecommendation(
                rank=rank,
                card_id=card.id,
                card_name=card.name,
                image_url=card.image_url,
                reward_rate_percent=_best_reward_rate(card),
                apr_percent=card.apr_percent,
                confidence_score=_clamp_confidence(item.confidence_score),
                net_annual_benefit_inr=float(item.net_annual_benefit_inr),
                explanation=explanation,
            )
        )

    if not normalized:
        raise ValueError("No valid recommendations after normalization")

    normalized.sort(key=lambda r: r.rank)
    trimmed = normalized[:top_n]
    normalized = [
        rec.model_copy(update={"rank": index})
        for index, rec in enumerate(trimmed, start=1)
    ]

    return RecommendationResponse(
        recommendations=normalized,
        meta=RecommendationMeta(
            eligible_count=eligible_count,
            aa_connected=profile.aa_connected,
        ),
    )
