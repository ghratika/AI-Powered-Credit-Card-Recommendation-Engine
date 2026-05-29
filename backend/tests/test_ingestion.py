"""Tests for data ingestion (Phase 1)."""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from app.domain.ingestion import DataLoadError, load_aa_transactions, load_cards
from app.models.aa import TransactionType
from app.models.card import CardProduct


def test_load_cards_success(cards_path: Path) -> None:
    cards = load_cards(use_cache=False, path=cards_path)

    assert len(cards) == 8
    assert all(isinstance(card, CardProduct) for card in cards)
    assert cards[0].id == "axis-neo"
    assert cards[-1].id == "axis-reserve"


def test_load_cards_missing_file(tmp_path: Path) -> None:
    missing = tmp_path / "missing.json"

    with pytest.raises(DataLoadError, match="not found"):
        load_cards(use_cache=False, path=missing)


def test_load_cards_invalid_json(tmp_path: Path) -> None:
    bad = tmp_path / "bad.json"
    bad.write_text("{ not json", encoding="utf-8")

    with pytest.raises(DataLoadError, match="Invalid JSON"):
        load_cards(use_cache=False, path=bad)


def test_load_cards_empty_array(tmp_path: Path) -> None:
    empty = tmp_path / "empty.json"
    empty.write_text("[]", encoding="utf-8")

    with pytest.raises(DataLoadError, match="No cards configured"):
        load_cards(use_cache=False, path=empty)


def test_load_cards_skips_invalid_row(tmp_path: Path) -> None:
    path = tmp_path / "mixed.json"
    path.write_text(
        json.dumps(
            [
                {
                    "id": "valid-card",
                    "name": "Valid",
                    "image_url": "/x.png",
                    "annual_fee_inr": 0,
                    "apr_percent": 40,
                    "min_income_inr": 100000,
                    "min_cibil": 700,
                    "reward_categories": [],
                    "default_earn_rate_percent": 1,
                    "highlights": [],
                },
                {"id": "missing-required-fields"},
            ]
        ),
        encoding="utf-8",
    )

    cards = load_cards(use_cache=False, path=path)
    assert len(cards) == 1
    assert cards[0].id == "valid-card"


def test_load_cards_all_invalid_raises(tmp_path: Path) -> None:
    path = tmp_path / "all_bad.json"
    path.write_text(json.dumps([{"id": "only-id"}]), encoding="utf-8")

    with pytest.raises(DataLoadError, match="No valid cards"):
        load_cards(use_cache=False, path=path)


def test_load_cards_uses_cache(cards_path: Path) -> None:
    first = load_cards(use_cache=True, path=cards_path)
    second = load_cards(use_cache=True, path=cards_path)
    assert first is second


def test_load_aa_transactions_success(aa_path: Path) -> None:
    payload = load_aa_transactions(use_cache=False, path=aa_path)

    assert payload.user_ref == "demo-user-1"
    assert len(payload.transactions) >= 50
    categories = {t.category for t in payload.transactions}
    assert "dining" in categories
    assert "travel" in categories
    assert "fuel" in categories
    assert "shopping" in categories
    assert "utilities" in categories


def test_aa_transactions_span_multiple_months(aa_path: Path) -> None:
    payload = load_aa_transactions(use_cache=False, path=aa_path)
    months = {t.date.strftime("%Y-%m") for t in payload.transactions}
    assert len(months) >= 12


def test_load_aa_missing_file(tmp_path: Path) -> None:
    missing = tmp_path / "missing_aa.json"

    with pytest.raises(DataLoadError, match="not found"):
        load_aa_transactions(use_cache=False, path=missing)


def test_load_aa_empty_transactions(tmp_path: Path) -> None:
    path = tmp_path / "empty_aa.json"
    path.write_text(
        json.dumps({"user_ref": "empty-user", "transactions": []}),
        encoding="utf-8",
    )

    payload = load_aa_transactions(use_cache=False, path=path)
    assert payload.user_ref == "empty-user"
    assert payload.transactions == []


def test_load_aa_skips_invalid_transaction(tmp_path: Path) -> None:
    path = tmp_path / "mixed_aa.json"
    path.write_text(
        json.dumps(
            {
                "user_ref": "u1",
                "transactions": [
                    {
                        "date": "2025-01-01",
                        "amount_inr": 500,
                        "category": "fuel",
                        "merchant": "Pump",
                        "type": "debit",
                    },
                    {"amount_inr": -100},
                ],
            }
        ),
        encoding="utf-8",
    )

    payload = load_aa_transactions(use_cache=False, path=path)
    assert len(payload.transactions) == 1
    assert payload.transactions[0].type == TransactionType.DEBIT


def test_reward_category_normalized_to_lowercase(cards_path: Path) -> None:
    cards = load_cards(use_cache=False, path=cards_path)
    ace = next(c for c in cards if c.id == "axis-ace")
    assert ace.reward_categories[0].category == "utilities"
