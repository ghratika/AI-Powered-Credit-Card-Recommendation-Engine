"""Tests for eligibility engine."""

from __future__ import annotations

import pytest

from app.domain.eligibility import RULE_MIN_CIBIL, RULE_MIN_INCOME, filter_eligible_cards
from app.domain.ingestion import load_cards
from app.models.user import UserProfile


@pytest.fixture
def catalog():
    return load_cards(use_cache=False)


@pytest.fixture
def demo_profile() -> UserProfile:
    return UserProfile.from_raw(
        annual_income_inr=1_200_000,
        pan="ABCDE1234F",
        mobile="9876543210",
        aa_connected=True,
    )


def test_demo_profile_has_eligible_cards(catalog, demo_profile: UserProfile) -> None:
    eligible = filter_eligible_cards(catalog, demo_profile)
    assert len(eligible) >= 1
    ids = {e.card.id for e in eligible}
    assert "axis-neo" in ids
    assert "axis-reserve" not in ids  # needs 2.4M income and 800 CIBIL


def test_demo_profile_eligible_count_deterministic(catalog, demo_profile: UserProfile) -> None:
    first = filter_eligible_cards(catalog, demo_profile)
    second = filter_eligible_cards(catalog, demo_profile)
    assert len(first) == len(second) == 6
    assert [e.card.id for e in first] == [e.card.id for e in second]


def test_income_exactly_at_minimum_is_eligible(catalog) -> None:
    profile = UserProfile(
        annual_income_inr=250_000,
        pan="ABCDE1234F",
        mobile="9876543210",
        cibil=700,
    )
    eligible = filter_eligible_cards(catalog, profile)
    assert any(e.card.id == "axis-neo" for e in eligible)


def test_income_one_below_minimum_excluded(catalog) -> None:
    profile = UserProfile(
        annual_income_inr=249_999,
        pan="ABCDE1234F",
        mobile="9876543210",
        cibil=700,
    )
    eligible = filter_eligible_cards(catalog, profile)
    assert not any(e.card.id == "axis-neo" for e in eligible)


def test_cibil_exactly_at_minimum_is_eligible(catalog) -> None:
    profile = UserProfile(
        annual_income_inr=1_200_000,
        pan="ABCDE1234F",
        mobile="9876543210",
        cibil=750,
    )
    eligible = filter_eligible_cards(catalog, profile)
    assert any(e.card.id == "axis-ace" for e in eligible)


def test_cibil_one_below_minimum_excluded(catalog) -> None:
    profile = UserProfile(
        annual_income_inr=1_200_000,
        pan="ABCDE1234F",
        mobile="9876543210",
        cibil=749,
    )
    eligible = filter_eligible_cards(catalog, profile)
    assert not any(e.card.id == "axis-ace" for e in eligible)


def test_no_eligible_cards_low_income_and_cibil(catalog) -> None:
    profile = UserProfile(
        annual_income_inr=50_000,
        pan="LOWCB1234L",
        mobile="9876543210",
        cibil=300,
    )
    eligible = filter_eligible_cards(catalog, profile)
    assert eligible == []


def test_passed_rules_populated(catalog, demo_profile: UserProfile) -> None:
    eligible = filter_eligible_cards(catalog, demo_profile)
    for item in eligible:
        assert RULE_MIN_INCOME in item.passed_rules
        assert RULE_MIN_CIBIL in item.passed_rules
