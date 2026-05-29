"""Tests for user input validators."""

from __future__ import annotations

import pytest

from app.domain.exceptions import InputValidationError
from app.domain.pan_verification import lookup_cibil_from_pan
from app.domain.validators import (
    DEFAULT_CIBIL,
    resolve_cibil,
    validate_annual_income,
    validate_mobile,
    validate_pan,
)
from app.models.user import UserProfile


def test_validate_pan_success() -> None:
    assert validate_pan("ABCDE1234F") == "ABCDE1234F"


def test_validate_pan_strips_separators() -> None:
    assert validate_pan("abcde-1234-f") == "ABCDE1234F"


def test_validate_pan_invalid_format() -> None:
    with pytest.raises(InputValidationError, match="PAN must match"):
        validate_pan("1234567890")


def test_validate_mobile_success() -> None:
    assert validate_mobile("9876543210") == "9876543210"


def test_validate_mobile_with_country_code() -> None:
    assert validate_mobile("+919876543210") == "9876543210"


def test_validate_mobile_invalid_series() -> None:
    with pytest.raises(InputValidationError, match="6–9"):
        validate_mobile("5876543210")


def test_validate_income_success() -> None:
    assert validate_annual_income(1_200_000) == 1_200_000.0


def test_validate_income_zero_rejected() -> None:
    with pytest.raises(InputValidationError, match="positive"):
        validate_annual_income(0)


def test_resolve_cibil_default() -> None:
    assert resolve_cibil(None) == DEFAULT_CIBIL


def test_resolve_cibil_out_of_range() -> None:
    with pytest.raises(InputValidationError):
        resolve_cibil(250)


def test_lookup_cibil_from_pan_demo() -> None:
    assert lookup_cibil_from_pan("ABCDE1234F") == 780
    assert lookup_cibil_from_pan("LOWCB1234L") == 300


def test_lookup_cibil_from_pan_deterministic() -> None:
    assert lookup_cibil_from_pan("FGHIJ5678K") == lookup_cibil_from_pan("FGHIJ5678K")
    assert 300 <= lookup_cibil_from_pan("FGHIJ5678K") <= 900


def test_user_profile_from_raw() -> None:
    profile = UserProfile.from_raw(
        annual_income_inr="1200000",
        pan="ABCDE1234F",
        mobile=9876543210,
        aa_connected=True,
    )
    assert profile.annual_income_inr == 1_200_000.0
    assert profile.cibil == 780
    assert profile.aa_connected is True
