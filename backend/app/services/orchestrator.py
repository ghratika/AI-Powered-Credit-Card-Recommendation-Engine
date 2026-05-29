"""Recommendation pipeline orchestration."""

from __future__ import annotations

import json
import logging
from typing import Any

from app.config import get_top_n_recommendations
from app.domain.eligibility import filter_eligible_cards
from app.domain.exceptions import (
    AANotConnectedError,
    LLMServiceError,
    NoEligibleCardsError,
)
from app.domain.exceptions import DataUnavailableError
from app.domain.ingestion import DataLoadError, load_aa_transactions, load_cards
from app.domain.normalizer import normalize_recommendations, parse_llm_json
from app.domain.prompt_builder import build_json_fix_messages, build_messages
from app.domain.spend_aggregator import build_spend_profile
from app.models.recommendation import RecommendationResponse
from app.models.user import UserProfile
from app.services.llm_client import LLMClient, get_llm_client

logger = logging.getLogger(__name__)


class RecommendationOrchestrator:
    """Coordinates ingestion → eligibility → spend → LLM → normalization."""

    def __init__(self, llm_client: LLMClient | None = None) -> None:
        self._llm = llm_client or get_llm_client()

    def recommend(self, profile: UserProfile) -> RecommendationResponse:
        if not profile.aa_connected:
            raise AANotConnectedError()

        try:
            catalog = load_cards()
            aa_payload = load_aa_transactions()
        except DataLoadError as exc:
            raise DataUnavailableError(str(exc)) from exc
        eligible = filter_eligible_cards(catalog, profile)

        if not eligible:
            raise NoEligibleCardsError()

        spend = build_spend_profile(aa_payload.transactions)
        top_n = get_top_n_recommendations()
        messages = build_messages(profile, spend, eligible, top_n=top_n)
        catalog_by_id = {card.id: card for card in catalog}

        raw_text = self._call_llm_with_json_retry(messages)
        try:
            raw_json: dict[str, Any] = parse_llm_json(raw_text)
        except (json.JSONDecodeError, TypeError) as exc:
            raise LLMServiceError("Failed to parse LLM response as JSON") from exc

        try:
            return normalize_recommendations(
                raw_json,
                catalog_by_id,
                top_n=top_n,
                profile=profile,
                eligible_count=len(eligible),
            )
        except ValueError as exc:
            raise LLMServiceError(str(exc)) from exc

    def _call_llm_with_json_retry(self, messages: list[dict[str, str]]) -> str:
        """Call LLM once; on invalid JSON, retry with a fix prompt (L-01)."""
        last_text = ""
        current_messages = messages

        for attempt in range(2):
            try:
                last_text = self._llm.complete(current_messages)
                parse_llm_json(last_text)
                return last_text
            except json.JSONDecodeError:
                logger.warning("LLM returned invalid JSON on attempt %s", attempt + 1)
                if attempt == 0:
                    current_messages = build_json_fix_messages(messages, last_text)
                else:
                    raise LLMServiceError(
                        "Failed to obtain valid JSON from LLM after retry"
                    ) from None
            except Exception as exc:
                logger.exception("LLM call failed")
                raise LLMServiceError("LLM provider request failed") from exc

        raise LLMServiceError("Failed to obtain valid JSON from LLM")


def recommend(profile: UserProfile, *, llm_client: LLMClient | None = None) -> RecommendationResponse:
    """Convenience wrapper for a single recommendation run."""
    return RecommendationOrchestrator(llm_client=llm_client).recommend(profile)
