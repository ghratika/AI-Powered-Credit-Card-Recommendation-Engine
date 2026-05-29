"""Verify Phase 1 data loads successfully (run from backend/)."""

from __future__ import annotations

import logging
import sys
from pathlib import Path

# Allow `python scripts/verify_data.py` without installing the package.
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from app.domain.ingestion import log_data_counts_on_startup

logging.basicConfig(level=logging.INFO, format="%(levelname)s %(message)s")


def main() -> int:
    try:
        log_data_counts_on_startup()
    except Exception as exc:
        print(f"Data verification failed: {exc}", file=sys.stderr)
        return 1
    print("Data verification OK.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
