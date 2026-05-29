"""Tests for startup validation."""

from pathlib import Path

import pytest

from app.domain.ingestion import DataLoadError
from app.startup import validate_startup_config


def test_validate_startup_config_loads_data() -> None:
    validate_startup_config()


def test_validate_startup_config_missing_cards(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    missing = tmp_path / "missing_cards.json"
    monkeypatch.setenv("CARDS_DATA_PATH", str(missing))
    with pytest.raises(DataLoadError, match="Card catalog"):
        validate_startup_config()
