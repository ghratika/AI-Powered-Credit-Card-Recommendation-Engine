"""Credit card catalog models."""

from __future__ import annotations

from pydantic import BaseModel, Field, field_validator


class RewardCategory(BaseModel):
    """Reward earn rule for a spend category."""

    category: str = Field(..., min_length=1)
    rate_percent: float = Field(..., ge=0)
    monthly_cap_inr: float | None = Field(default=None, ge=0)

    @field_validator("category")
    @classmethod
    def normalize_category(cls, value: str) -> str:
        return value.strip().lower()


class CardProduct(BaseModel):
    """Axis Bank credit card product from the processed catalog."""

    id: str = Field(..., min_length=1)
    name: str = Field(..., min_length=1)
    image_url: str = Field(..., min_length=1)
    annual_fee_inr: float = Field(..., ge=0)
    apr_percent: float = Field(..., ge=0)
    min_income_inr: float = Field(..., ge=0)
    min_cibil: int = Field(default=0, ge=0, le=900)
    reward_categories: list[RewardCategory] = Field(default_factory=list)
    default_earn_rate_percent: float = Field(..., ge=0)
    highlights: list[str] = Field(default_factory=list)

    @field_validator("id")
    @classmethod
    def normalize_id(cls, value: str) -> str:
        return value.strip().lower()
