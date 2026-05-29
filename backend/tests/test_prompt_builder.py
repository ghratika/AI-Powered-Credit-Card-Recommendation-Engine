"""Tests for LLM prompt builder."""

from __future__ import annotations

import json

from app.domain.prompt_builder import build_messages, build_user_payload
from app.domain.spend_aggregator import build_spend_profile
from app.models.user import EligibleCard, UserProfile
from app.models.card import CardProduct


def _sample_card() -> CardProduct:
    return CardProduct(
        id="axis-ace",
        name="Axis Bank ACE",
        image_url="/assets/cards/axis-ace.svg",
        annual_fee_inr=499,
        apr_percent=42,
        min_income_inr=600000,
        min_cibil=750,
        reward_categories=[],
        default_earn_rate_percent=1.5,
        highlights=["5% utilities"],
    )


def test_build_user_payload_structure() -> None:
    profile = UserProfile.from_raw(
        annual_income_inr=1_200_000,
        pan="ABCDE1234F",
        mobile="9876543210",
        aa_connected=True,
    )
    spend = build_spend_profile([], annualize=False)
    eligible = [EligibleCard(card=_sample_card(), passed_rules=["min_income", "min_cibil"])]

    payload = build_user_payload(profile, spend, eligible)
    assert payload["user_profile"]["annual_income_inr"] == 1_200_000
    assert payload["eligible_cards"][0]["id"] == "axis-ace"
    assert "image_url" not in payload["eligible_cards"][0]


def test_build_messages_includes_system_rules() -> None:
    profile = UserProfile.from_raw(
        annual_income_inr=1_200_000,
        pan="ABCDE1234F",
        mobile="9876543210",
        aa_connected=True,
    )
    spend = build_spend_profile([], annualize=False)
    eligible = [EligibleCard(card=_sample_card(), passed_rules=["min_income"])]

    messages = build_messages(profile, spend, eligible, top_n=3)
    assert messages[0]["role"] == "system"
    assert "eligible_cards" in messages[0]["content"]
    user_data = json.loads(messages[1]["content"])
    assert len(user_data["eligible_cards"]) == 1
