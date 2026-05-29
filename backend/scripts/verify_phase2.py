"""Verify Phase 2 domain logic (run from backend/)."""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from app.domain.eligibility import filter_eligible_cards
from app.domain.ingestion import load_aa_transactions, load_cards
from app.domain.spend_aggregator import build_spend_profile
from app.models.user import UserProfile


def main() -> int:
    cards = load_cards()
    profile = UserProfile.from_raw(
        annual_income_inr=1_200_000,
        pan="ABCDE1234F",
        mobile="9876543210",
        aa_connected=True,
    )
    eligible = filter_eligible_cards(cards, profile)
    aa = load_aa_transactions()
    spend = build_spend_profile(aa.transactions)

    print(f"Eligible cards: {len(eligible)}")
    for item in eligible:
        print(f"  - {item.card.name}")

    print(f"Spend profile total (annual INR): {spend.total_annual:,.2f}")
    for category, amount in sorted(spend.annual_by_category.items()):
        print(f"  {category}: {amount:,.2f}")

    if not eligible or spend.total_annual <= 0:
        print("Phase 2 verification failed.", file=sys.stderr)
        return 1

    print("Phase 2 verification OK.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
