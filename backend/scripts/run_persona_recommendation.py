"""Run recommendation for a Phase 6 manual-test persona (dining / travel / balanced)."""

from __future__ import annotations

import json
import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from app.domain.ingestion import clear_data_cache
from app.models.user import UserProfile
from app.services.orchestrator import recommend

PERSONAS: dict[str, str] = {
    "dining": "aa_dining_heavy.json",
    "travel": "aa_travel_heavy.json",
    "balanced": "aa_balanced.json",
    "default": "aa_transactions.json",
}


def main() -> int:
    persona = (sys.argv[1] if len(sys.argv) > 1 else "balanced").lower()
    if persona not in PERSONAS:
        print(f"Unknown persona '{persona}'. Choose: {', '.join(PERSONAS)}", file=sys.stderr)
        return 2

    root = Path(__file__).resolve().parents[2]
    aa_path = root / "data" / "synthetic" / PERSONAS[persona]
    os.environ["AA_DATA_PATH"] = str(aa_path)
    clear_data_cache()

    profile = UserProfile.from_raw(
        annual_income_inr=1_200_000,
        pan="ABCDE1234F",
        mobile="9876543210",
        aa_connected=True,
    )

    print(f"Persona: {persona}  AA: {aa_path.name}", file=sys.stderr)

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
