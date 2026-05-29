"""Tests for spend aggregation."""

from __future__ import annotations

from datetime import date

import pytest

from app.domain.ingestion import load_aa_transactions
from app.domain.spend_aggregator import build_spend_profile
from app.models.aa import Transaction, TransactionType


def _txn(
    day: str,
    amount: float,
    category: str,
    *,
    txn_type: TransactionType = TransactionType.DEBIT,
) -> Transaction:
    return Transaction(
        date=date.fromisoformat(day),
        amount_inr=amount,
        category=category,
        merchant="Test",
        type=txn_type,
    )


def test_empty_transactions() -> None:
    profile = build_spend_profile([])
    assert profile.annual_by_category == {}
    assert profile.total_annual == 0.0


def test_category_alias_food_maps_to_dining() -> None:
    profile = build_spend_profile(
        [
            _txn("2025-01-15", 1000, "food"),
            _txn("2025-02-15", 500, "dining"),
        ],
        annualize=False,
    )
    assert profile.annual_by_category["dining"] == 1500.0
    assert profile.total_annual == 1500.0


def test_credit_subtracts_from_category() -> None:
    profile = build_spend_profile(
        [
            _txn("2025-03-01", 1000, "shopping"),
            _txn("2025-03-02", 200, "shopping", txn_type=TransactionType.CREDIT),
        ],
        annualize=False,
    )
    assert profile.annual_by_category["shopping"] == 800.0


def test_unknown_category_maps_to_others() -> None:
    profile = build_spend_profile(
        [_txn("2025-04-01", 300, "misc_xyz")],
        annualize=False,
    )
    assert profile.annual_by_category["others"] == 300.0


def test_partial_year_annualized() -> None:
    """Two months of spend → multiply by 12/2 = 6."""
    profile = build_spend_profile(
        [
            _txn("2025-01-10", 1000, "fuel"),
            _txn("2025-02-10", 1000, "fuel"),
        ],
        annualize=True,
    )
    assert profile.annual_by_category["fuel"] == 12_000.0
    assert profile.total_annual == 12_000.0


def test_full_year_no_extra_annualization(aa_path) -> None:
    payload = load_aa_transactions(use_cache=False, path=aa_path)
    profile = build_spend_profile(payload.transactions)

    # Hand-check: sum debits minus credits per normalized category (12 distinct months).
    expected: dict[str, float] = {}
    for txn in payload.transactions:
        from app.domain.category_mapping import normalize_spend_category

        cat = normalize_spend_category(txn.category)
        signed = txn.amount_inr if txn.type == TransactionType.DEBIT else -txn.amount_inr
        expected[cat] = expected.get(cat, 0.0) + signed
    for cat in expected:
        expected[cat] = max(0.0, expected[cat])

    assert profile.annual_by_category == pytest.approx(
        {k: round(v, 2) for k, v in sorted(expected.items())},
        rel=0,
        abs=0.01,
    )
    assert profile.total_annual == pytest.approx(
        round(sum(profile.annual_by_category.values()), 2),
        rel=0,
        abs=0.01,
    )
    assert profile.total_annual > 0
    assert "dining" in profile.annual_by_category
    assert "utilities" in profile.annual_by_category


def test_aa_fixture_spans_twelve_months(aa_path) -> None:
    payload = load_aa_transactions(use_cache=False, path=aa_path)
    months = {(t.date.year, t.date.month) for t in payload.transactions}
    assert len(months) >= 12
