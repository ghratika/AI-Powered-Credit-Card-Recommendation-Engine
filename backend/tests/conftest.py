"""Pytest fixtures."""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from app.domain.ingestion import clear_data_cache


@pytest.fixture(autouse=True)
def reset_ingestion_cache() -> None:
    clear_data_cache()
    yield
    clear_data_cache()


@pytest.fixture
def project_root() -> Path:
    return Path(__file__).resolve().parents[2]


@pytest.fixture
def cards_path(project_root: Path) -> Path:
    return project_root / "data" / "processed" / "cards.json"


@pytest.fixture
def aa_path(project_root: Path) -> Path:
    return project_root / "data" / "synthetic" / "aa_transactions.json"


@pytest.fixture
def tmp_cards_file(tmp_path: Path) -> Path:
    path = tmp_path / "cards.json"
    path.write_text(
        json.dumps(
            [
                {
                    "id": "test-card",
                    "name": "Test Card",
                    "image_url": "/assets/cards/test.png",
                    "annual_fee_inr": 0,
                    "apr_percent": 42.0,
                    "min_income_inr": 100000,
                    "min_cibil": 650,
                    "reward_categories": [],
                    "default_earn_rate_percent": 1.0,
                    "highlights": [],
                }
            ]
        ),
        encoding="utf-8",
    )
    return path


@pytest.fixture
def tmp_aa_file(tmp_path: Path) -> Path:
    path = tmp_path / "aa.json"
    path.write_text(
        json.dumps(
            {
                "user_ref": "test-user",
                "transactions": [
                    {
                        "date": "2025-06-01",
                        "amount_inr": 1000,
                        "category": "dining",
                        "merchant": "Cafe",
                        "type": "debit",
                    }
                ],
            }
        ),
        encoding="utf-8",
    )
    return path
