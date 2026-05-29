"""Rule-based eligibility filtering (no LLM)."""

from __future__ import annotations

from app.models.card import CardProduct
from app.models.user import EligibleCard, UserProfile

RULE_MIN_INCOME = "min_income"
RULE_MIN_CIBIL = "min_cibil"


def filter_eligible_cards(
    catalog: list[CardProduct],
    profile: UserProfile,
) -> list[EligibleCard]:
    """
    Return cards the user qualifies for based on income and CIBIL.

    Boundaries are **inclusive** (E-03, E-33): income >= min_income_inr,
    cibil >= min_cibil.
    """
    eligible: list[EligibleCard] = []

    for card in catalog:
        passed: list[str] = []

        if profile.annual_income_inr < card.min_income_inr:
            continue
        passed.append(RULE_MIN_INCOME)

        if profile.cibil < card.min_cibil:
            continue
        passed.append(RULE_MIN_CIBIL)

        eligible.append(EligibleCard(card=card, passed_rules=passed))

    return eligible
