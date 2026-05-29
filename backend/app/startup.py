"""Startup validation — fail fast before serving traffic."""

from __future__ import annotations

import logging
from pathlib import Path

from app.config import get_aa_data_path, get_cards_data_path
from app.domain.ingestion import DataLoadError, log_data_counts_on_startup

logger = logging.getLogger(__name__)


def _require_data_file(path: Path, label: str) -> None:
    if not path.is_file():
        raise DataLoadError(
            f"{label} not found at {path}. "
            f"Set CARDS_DATA_PATH / AA_DATA_PATH or deploy data/ with the API."
        )


def validate_startup_config() -> None:
    """
    Verify required data files exist and load successfully.

    Raises ``DataLoadError`` if configuration is invalid (Phase 7.2).
    """
    cards_path = get_cards_data_path()
    aa_path = get_aa_data_path()

    logger.info("Validating data paths cards=%s aa=%s", cards_path, aa_path)
    _require_data_file(cards_path, "Card catalog")
    _require_data_file(aa_path, "AA transactions")

    log_data_counts_on_startup()
