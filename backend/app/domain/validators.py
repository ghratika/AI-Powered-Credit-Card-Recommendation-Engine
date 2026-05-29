"""User profile input validation (Phase 2)."""

from __future__ import annotations

import re

from app.domain.exceptions import InputValidationError

PAN_PATTERN = re.compile(r"^[A-Z]{5}[0-9]{4}[A-Z]$")
MOBILE_PATTERN = re.compile(r"^[6-9]\d{9}$")

MIN_ANNUAL_INCOME_INR = 50_000
MAX_ANNUAL_INCOME_INR = 100_000_000
MIN_CIBIL = 300
MAX_CIBIL = 900
DEFAULT_CIBIL = 750


def normalize_pan(raw: str) -> str:
    """Strip separators and uppercase (U-14)."""
    cleaned = re.sub(r"[\s\-]", "", raw.strip())
    return cleaned.upper()


def validate_pan(raw: str) -> str:
    """Validate and return normalized PAN."""
    if not raw or not str(raw).strip():
        raise InputValidationError("PAN is required", field="pan")

    pan = normalize_pan(str(raw))
    if len(pan) != 10:
        raise InputValidationError("PAN must be 10 characters", field="pan")
    if not PAN_PATTERN.match(pan):
        raise InputValidationError(
            "PAN must match format AAAAA9999A (5 letters, 4 digits, 1 letter)",
            field="pan",
        )
    return pan


def normalize_mobile(raw: str | int) -> str:
    """Strip country code and non-digits (U-23, U-24)."""
    digits = re.sub(r"\D", "", str(raw).strip())
    if digits.startswith("91") and len(digits) == 12:
        digits = digits[2:]
    return digits


def validate_mobile(raw: str | int) -> str:
    """Validate and return 10-digit Indian mobile."""
    if raw is None or str(raw).strip() == "":
        raise InputValidationError("Mobile number is required", field="mobile")

    mobile = normalize_mobile(raw)
    if len(mobile) != 10:
        raise InputValidationError("Mobile number must be 10 digits", field="mobile")
    if not MOBILE_PATTERN.match(mobile):
        raise InputValidationError(
            "Mobile number must start with 6–9 and be 10 digits",
            field="mobile",
        )
    return mobile


def validate_annual_income(raw: float | int | str) -> float:
    """Validate annual income in INR (U-03–U-07)."""
    if raw is None or raw == "":
        raise InputValidationError("Annual income is required", field="annual_income_inr")

    try:
        income = float(raw)
    except (TypeError, ValueError) as exc:
        raise InputValidationError(
            "Annual income must be a number", field="annual_income_inr"
        ) from exc

    if income <= 0:
        raise InputValidationError("Income must be positive", field="annual_income_inr")
    if income < MIN_ANNUAL_INCOME_INR:
        raise InputValidationError(
            f"Income must be at least ₹{MIN_ANNUAL_INCOME_INR:,}",
            field="annual_income_inr",
        )
    if income > MAX_ANNUAL_INCOME_INR:
        raise InputValidationError(
            f"Income must not exceed ₹{MAX_ANNUAL_INCOME_INR:,}",
            field="annual_income_inr",
        )
    return income


def resolve_cibil(raw: int | None) -> int:
    """Return CIBIL score, applying demo default when omitted (U-30, U-31)."""
    if raw is None:
        return DEFAULT_CIBIL

    try:
        score = int(raw)
    except (TypeError, ValueError) as exc:
        raise InputValidationError("CIBIL must be an integer", field="cibil") from exc

    if score < MIN_CIBIL or score > MAX_CIBIL:
        raise InputValidationError(
            f"CIBIL must be between {MIN_CIBIL} and {MAX_CIBIL}",
            field="cibil",
        )
    return score
