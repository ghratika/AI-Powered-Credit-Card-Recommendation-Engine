"""Map AA merchant categories to card reward category labels."""

from __future__ import annotations

# Aliases → canonical category used in spend profiles and card rewards.
CATEGORY_ALIASES: dict[str, str] = {
    "food": "dining",
    "restaurant": "dining",
    "restaurants": "dining",
    "ecommerce": "shopping",
    "online_shopping": "shopping",
    "retail": "shopping",
    "bills": "utilities",
    "utility": "utilities",
    "bill_pay": "utilities",
    "petrol": "fuel",
    "gas": "fuel",
    "groceries": "shopping",
    "grocery": "shopping",
    "entertainment": "others",
    "health": "others",
    "education": "others",
    "transfer": "others",
    "atm": "others",
}

CANONICAL_CATEGORIES = frozenset(
    {"dining", "travel", "fuel", "shopping", "utilities", "others"}
)


def normalize_spend_category(raw: str) -> str:
    """
    Normalize a transaction category for aggregation.

    Unknown labels map to ``others`` (edge case S-03).
    """
    key = raw.strip().lower().replace(" ", "_").replace("-", "_")
    if key in CANONICAL_CATEGORIES:
        return key
    return CATEGORY_ALIASES.get(key, "others")
