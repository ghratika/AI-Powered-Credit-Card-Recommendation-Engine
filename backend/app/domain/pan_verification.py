"""Simulated PAN verification and internal CIBIL lookup."""

from __future__ import annotations

import hashlib

from app.domain.validators import MAX_CIBIL, MIN_CIBIL, validate_pan

# Known demo PAN → CIBIL mappings for predictable test personas.
DEMO_PAN_CIBIL: dict[str, int] = {
    "ABCDE1234F": 780,
    "LOWCB1234L": 300,
}


def lookup_cibil_from_pan(pan: str) -> int:
    """
    Simulate PAN verification and bureau CIBIL lookup.

    Validates PAN format first, then returns a deterministic demo score.
    """
    normalized = validate_pan(pan)

    known = DEMO_PAN_CIBIL.get(normalized)
    if known is not None:
        return known

    digest = hashlib.sha256(normalized.encode("utf-8")).digest()
    span = MAX_CIBIL - MIN_CIBIL + 1
    return MIN_CIBIL + (int.from_bytes(digest[:2], "big") % span)
