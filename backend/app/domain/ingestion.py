"""Load and validate card catalog and synthetic AA transaction data."""

from __future__ import annotations

import json
import logging
from pathlib import Path
from typing import Any

from pydantic import ValidationError

from app.config import get_aa_data_path, get_cards_data_path
from app.models.aa import AAPayload, Transaction
from app.models.card import CardProduct

logger = logging.getLogger(__name__)

_cards_cache: list[CardProduct] | None = None
_aa_cache: AAPayload | None = None


class DataLoadError(Exception):
    """Raised when required data files are missing or unusable."""


def clear_data_cache() -> None:
    """Clear in-memory caches (useful in tests)."""
    global _cards_cache, _aa_cache
    _cards_cache = None
    _aa_cache = None


def _read_json_file(path: Path) -> Any:
    if not path.is_file():
        raise DataLoadError(f"Data file not found: {path}")
    try:
        text = path.read_text(encoding="utf-8")
        return json.loads(text)
    except json.JSONDecodeError as exc:
        raise DataLoadError(f"Invalid JSON in {path}: {exc}") from exc
    except OSError as exc:
        raise DataLoadError(f"Cannot read data file {path}: {exc}") from exc


def _parse_cards(raw: Any, source: Path) -> list[CardProduct]:
    if not isinstance(raw, list):
        raise DataLoadError(f"Expected a JSON array in {source}")

    if len(raw) == 0:
        raise DataLoadError(f"No cards configured in {source}")

    cards: list[CardProduct] = []
    for index, item in enumerate(raw):
        try:
            cards.append(CardProduct.model_validate(item))
        except ValidationError as exc:
            logger.warning(
                "Skipping invalid card at index %s in %s: %s",
                index,
                source,
                exc.errors(),
            )

    if not cards:
        raise DataLoadError(f"No valid cards after validation in {source}")

    return cards


def load_cards(*, use_cache: bool = True, path: Path | None = None) -> list[CardProduct]:
    """
    Load Axis Bank card catalog from JSON.

    Results are cached in memory after the first successful load.
    """
    global _cards_cache

    if use_cache and _cards_cache is not None:
        return _cards_cache

    file_path = path or get_cards_data_path()
    raw = _read_json_file(file_path)
    cards = _parse_cards(raw, file_path)

    logger.info("Loaded %s credit card(s) from %s", len(cards), file_path)

    if use_cache:
        _cards_cache = cards

    return cards


def _parse_aa_payload(raw: Any, source: Path) -> AAPayload:
    if not isinstance(raw, dict):
        raise DataLoadError(f"Expected a JSON object in {source}")

    user_ref = raw.get("user_ref")
    if not user_ref or not isinstance(user_ref, str):
        raise DataLoadError(f"Missing or invalid user_ref in {source}")

    raw_transactions = raw.get("transactions", [])
    if not isinstance(raw_transactions, list):
        raise DataLoadError(f"transactions must be an array in {source}")

    transactions: list[Transaction] = []
    for index, item in enumerate(raw_transactions):
        try:
            transactions.append(Transaction.model_validate(item))
        except ValidationError as exc:
            logger.warning(
                "Skipping invalid transaction at index %s in %s: %s",
                index,
                source,
                exc.errors(),
            )

    return AAPayload(user_ref=user_ref.strip(), transactions=transactions)


def load_aa_transactions(
    *, use_cache: bool = True, path: Path | None = None
) -> AAPayload:
    """
    Load synthetic Account Aggregator transaction payload from JSON.

    Results are cached in memory after the first successful load.
    """
    global _aa_cache

    if use_cache and _aa_cache is not None:
        return _aa_cache

    file_path = path or get_aa_data_path()
    raw = _read_json_file(file_path)
    payload = _parse_aa_payload(raw, file_path)

    logger.info(
        "Loaded %s transaction(s) for user_ref=%s from %s",
        len(payload.transactions),
        payload.user_ref,
        file_path,
    )

    if use_cache:
        _aa_cache = payload

    return payload


def log_data_counts_on_startup() -> None:
    """Load catalog and AA data; log counts (for application startup)."""
    cards = load_cards()
    aa = load_aa_transactions()
    logger.info(
        "Data ingestion ready: cards=%s, aa_transactions=%s, user_ref=%s",
        len(cards),
        len(aa.transactions),
        aa.user_ref,
    )
