"""Run a sample recommendation (Phase 3 smoke test)."""

from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from app.models.user import UserProfile
from app.services.orchestrator import recommend


def main() -> int:
    profile = UserProfile.from_raw(
        annual_income_inr=1_200_000,
        pan="ABCDE1234F",
        mobile="9876543210",
        aa_connected=True,
    )

    try:
        result = recommend(profile)
    except Exception as exc:
        print(f"Recommendation failed: {exc}", file=sys.stderr)
        return 1

    output = json.dumps(result.model_dump(mode="json"), indent=2, ensure_ascii=False)
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        print(output)
    except (AttributeError, UnicodeEncodeError):
        print(output.encode("utf-8", errors="replace").decode("utf-8"))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
