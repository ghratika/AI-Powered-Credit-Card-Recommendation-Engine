"""Contract tests: mock LLM fixture validates against RecommendationResponse (Phase 6)."""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from app.domain.ingestion import load_cards
from app.domain.normalizer import normalize_recommendations, parse_llm_json
from app.models.recommendation import LLMRecommendationsPayload, RecommendationResponse
from app.models.user import UserProfile


@pytest.fixture
def mock_llm_fixture_path() -> Path:
    return Path(__file__).parent / "fixtures" / "mock_llm_response.json"


@pytest.fixture
def demo_profile() -> UserProfile:
    return UserProfile.from_raw(
        annual_income_inr=1_200_000,
        pan="ABCDE1234F",
        mobile="9876543210",
        aa_connected=True,
    )


def test_mock_llm_fixture_parses_as_llm_payload(mock_llm_fixture_path: Path) -> None:
    raw = json.loads(mock_llm_fixture_path.read_text(encoding="utf-8"))
    payload = LLMRecommendationsPayload.model_validate(raw)
    assert len(payload.recommendations) >= 1
    first = payload.recommendations[0]
    assert first.card_id
    assert 0 <= first.confidence_score <= 1 or first.confidence_score <= 100


def test_mock_llm_fixture_normalizes_to_recommendation_response(
    mock_llm_fixture_path: Path,
    demo_profile: UserProfile,
) -> None:
    cards = load_cards()
    catalog_by_id = {c.id: c for c in cards}
    raw = parse_llm_json(mock_llm_fixture_path.read_text(encoding="utf-8"))

    result = normalize_recommendations(
        raw,
        catalog_by_id,
        top_n=3,
        profile=demo_profile,
        eligible_count=6,
    )

    validated = RecommendationResponse.model_validate(result.model_dump())
    assert len(validated.recommendations) == 3

    for rec in validated.recommendations:
        assert rec.card_id in catalog_by_id
        assert rec.card_name
        assert rec.image_url.startswith("/")
        assert 0 <= rec.confidence_score <= 1
        assert rec.net_annual_benefit_inr >= 0
        assert len(rec.explanation) >= 1
        assert rec.reward_rate_percent >= 0
        assert rec.apr_percent >= 0

    assert validated.meta.eligible_count == 6
    assert validated.meta.aa_connected is True
    assert "simulated" in validated.meta.disclaimer.lower()
