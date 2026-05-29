"""Build LLM prompts from user profile, spend, and eligible cards."""

from __future__ import annotations

import json
from typing import Any

from app.models.aa import SpendProfile
from app.models.card import CardProduct
from app.models.user import EligibleCard, UserProfile

SYSTEM_PROMPT = """You are an expert Axis Bank credit card advisor for a FreechargeBiz-style recommendation demo.

Rules:
- Recommend ONLY from the eligible_cards list in the user message. Never invent card IDs.
- Rank cards by fit for the user's spend_profile and annual_income_inr.
- confidence_score must be between 0 and 1 (e.g. 0.92 for strong fit).
- net_annual_benefit_inr = estimated annual rewards minus annual_fee_inr (can be negative).
- Tie each explanation to specific spend categories and amounts from spend_profile.
- Return ONLY valid JSON with this exact shape:
{{
  "recommendations": [
    {{
      "rank": 1,
      "card_id": "<id from eligible_cards>",
      "card_name": "<name>",
      "confidence_score": 0.0,
      "net_annual_benefit_inr": 0,
      "explanation": "<2-4 sentences>"
    }}
  ]
}}
- Include up to {top_n} recommendations, ordered by rank starting at 1.
"""


def _card_summary(card: CardProduct) -> dict[str, Any]:
    """Trim card fields sent to the LLM to control token usage."""
    return {
        "id": card.id,
        "name": card.name,
        "annual_fee_inr": card.annual_fee_inr,
        "default_earn_rate_percent": card.default_earn_rate_percent,
        "reward_categories": [
            {
                "category": rc.category,
                "rate_percent": rc.rate_percent,
                "monthly_cap_inr": rc.monthly_cap_inr,
            }
            for rc in card.reward_categories
        ],
        "highlights": card.highlights[:5],
    }


def build_user_payload(
    profile: UserProfile,
    spend: SpendProfile,
    eligible: list[EligibleCard],
) -> dict[str, Any]:
    return {
        "user_profile": {
            "annual_income_inr": profile.annual_income_inr,
            "cibil": profile.cibil,
            "aa_connected": profile.aa_connected,
        },
        "spend_profile": {
            "annual_by_category": spend.annual_by_category,
            "total_annual": spend.total_annual,
        },
        "eligible_cards": [_card_summary(item.card) for item in eligible],
    }


def build_messages(
    profile: UserProfile,
    spend: SpendProfile,
    eligible: list[EligibleCard],
    *,
    top_n: int = 3,
) -> list[dict[str, str]]:
    """Return OpenAI-style chat messages for the recommendation call."""
    system = SYSTEM_PROMPT.format(top_n=top_n)
    user_content = json.dumps(
        build_user_payload(profile, spend, eligible),
        ensure_ascii=False,
    )
    return [
        {"role": "system", "content": system},
        {"role": "user", "content": user_content},
    ]


def build_json_fix_messages(
    original_messages: list[dict[str, str]],
    invalid_response: str,
) -> list[dict[str, str]]:
    """Follow-up messages asking the model to repair malformed JSON."""
    return [
        *original_messages,
        {"role": "assistant", "content": invalid_response[:4000]},
        {
            "role": "user",
            "content": (
                "Your previous reply was not valid JSON. "
                "Return ONLY a corrected JSON object matching the schema "
                "from the system instructions. No markdown fences or prose."
            ),
        },
    ]
