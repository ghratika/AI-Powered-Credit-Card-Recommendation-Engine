"""User profile and eligibility result models."""

from __future__ import annotations

from pydantic import BaseModel, Field, field_validator

from app.domain.pan_verification import lookup_cibil_from_pan
from app.domain.validators import (
    validate_annual_income,
    validate_mobile,
    validate_pan,
)
from app.models.card import CardProduct


class UserProfile(BaseModel):
    """Validated user financial profile for recommendations."""

    annual_income_inr: float = Field(..., gt=0)
    pan: str = Field(..., min_length=10, max_length=10)
    mobile: str = Field(..., min_length=10, max_length=10)
    cibil: int = Field(default=750, ge=300, le=900)
    aa_connected: bool = False

    @classmethod
    def from_raw(
        cls,
        *,
        annual_income_inr: float | int | str,
        pan: str,
        mobile: str | int,
        aa_connected: bool = False,
    ) -> UserProfile:
        """Parse and validate raw API/form values."""
        normalized_pan = validate_pan(pan)
        return cls(
            annual_income_inr=validate_annual_income(annual_income_inr),
            pan=normalized_pan,
            mobile=validate_mobile(mobile),
            cibil=lookup_cibil_from_pan(normalized_pan),
            aa_connected=bool(aa_connected),
        )


class EligibleCard(BaseModel):
    """Credit card that passed eligibility rules."""

    card: CardProduct
    passed_rules: list[str] = Field(default_factory=list)
