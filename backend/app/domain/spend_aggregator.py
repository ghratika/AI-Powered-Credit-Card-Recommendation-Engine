"""Aggregate synthetic AA transactions into an annual spend profile."""

from __future__ import annotations

from collections import defaultdict
from datetime import date

from app.domain.category_mapping import normalize_spend_category
from app.models.aa import SpendProfile, Transaction, TransactionType

# Treat spans shorter than this many distinct months as partial-year data.
PARTIAL_YEAR_MONTH_THRESHOLD = 12


def _distinct_months(dates: list[date]) -> int:
    if not dates:
        return 0
    return len({(d.year, d.month) for d in dates})


def _annualization_factor(months_covered: int) -> float:
    """
    Scale partial-period totals to an estimated annual figure (S-07).

    Full 12+ calendar months in data → factor 1.0 (sum is already annual).
    """
    if months_covered <= 0:
        return 1.0
    if months_covered >= PARTIAL_YEAR_MONTH_THRESHOLD:
        return 1.0
    return 12.0 / months_covered


def build_spend_profile(
    transactions: list[Transaction],
    *,
    annualize: bool = True,
) -> SpendProfile:
    """
    Sum spend by normalized category and compute total annual spend.

    - Debits add to category totals; credits subtract (S-08).
    - Categories are normalized via :func:`normalize_spend_category`.
    - Partial-year data is annualized when fewer than 12 months are present.
    """
    if not transactions:
        return SpendProfile(annual_by_category={}, total_annual=0.0)

    totals: dict[str, float] = defaultdict(float)
    dates: list[date] = []

    for txn in transactions:
        dates.append(txn.date)
        category = normalize_spend_category(txn.category)
        signed = txn.amount_inr if txn.type == TransactionType.DEBIT else -txn.amount_inr
        totals[category] += signed

    # Do not allow negative category totals after refunds.
    for category, amount in list(totals.items()):
        totals[category] = max(0.0, amount)

    months = _distinct_months(dates)
    factor = _annualization_factor(months) if annualize else 1.0

    annual_by_category = {
        category: round(amount * factor, 2)
        for category, amount in sorted(totals.items())
    }
    total_annual = round(sum(annual_by_category.values()), 2)

    return SpendProfile(
        annual_by_category=annual_by_category,
        total_annual=total_annual,
    )


def months_in_date_range(start: date, end: date) -> int:
    """Helper for tests: inclusive month span between two dates."""
    if end < start:
        return 0
    return (end.year - start.year) * 12 + (end.month - start.month) + 1
