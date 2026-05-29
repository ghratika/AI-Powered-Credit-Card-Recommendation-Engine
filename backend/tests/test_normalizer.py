"""Tests for LLM response normalizer."""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from app.domain.ingestion import load_cards
from app.domain.normalizer import normalize_recommendations, parse_llm_json, strip_json_fences
from app.models.user import UserProfile


@pytest.fixture
def catalog_by_id():
    cards = load_cards(use_cache=False)
    return {c.id: c for c in cards}


@pytest.fixture
def profile() -> UserProfile:
    return UserProfile.from_raw(
        annual_income_inr=1_200_000,
        pan="ABCDE1234F",
        mobile="9876543210",
        aa_connected=True,
    )


@pytest.fixture
def fixture_payload() -> dict:
    path = Path(__file__).parent / "fixtures" / "mock_llm_response.json"
    return json.loads(path.read_text(encoding="utf-8"))


def test_parse_llm_json_strips_fences() -> None:
    raw = '```json\n{"recommendations": []}\n```'
    assert parse_llm_json(raw) == {"recommendations": []}


def test_normalize_enriches_from_catalog(catalog_by_id, profile, fixture_payload) -> None:
    result = normalize_recommendations(
        fixture_payload,
        catalog_by_id,
        top_n=3,
        profile=profile,
        eligible_count=6,
    )
    assert len(result.recommendations) == 3
    top = result.recommendations[0]
    assert top.card_id == "axis-ace"
    assert top.image_url.endswith("axis-ace.svg")
    assert top.reward_rate_percent == 5.0
    assert top.apr_percent == 42.0
    assert 0 <= top.confidence_score <= 1
    assert result.meta.eligible_count == 6


def test_normalize_drops_unknown_card_id(catalog_by_id, profile, fixture_payload) -> None:
    payload = dict(fixture_payload)
    payload["recommendations"] = [
        *payload["recommendations"],
        {
            "rank": 99,
            "card_id": "fake-card",
            "card_name": "Fake",
            "confidence_score": 0.5,
            "net_annual_benefit_inr": 100,
            "explanation": "Should be dropped.",
        },
    ]
    result = normalize_recommendations(
        payload,
        catalog_by_id,
        top_n=5,
        profile=profile,
        eligible_count=6,
    )
    assert all(r.card_id != "fake-card" for r in result.recommendations)


def test_normalize_clamps_percentage_confidence(catalog_by_id, profile) -> None:
    payload = {
        "recommendations": [
            {
                "rank": 1,
                "card_id": "axis-ace",
                "confidence_score": 92,
                "net_annual_benefit_inr": 1000,
                "explanation": "Test",
            }
        ]
    }
    result = normalize_recommendations(
        payload,
        catalog_by_id,
        top_n=1,
        profile=profile,
        eligible_count=1,
    )
    assert result.recommendations[0].confidence_score == pytest.approx(0.92)


def test_normalize_empty_after_drop_raises(catalog_by_id, profile) -> None:
    with pytest.raises(ValueError):
        normalize_recommendations(
            {"recommendations": [{"card_id": "unknown", "confidence_score": 0.5, "net_annual_benefit_inr": 0}]},
            catalog_by_id,
            top_n=3,
            profile=profile,
            eligible_count=1,
        )
