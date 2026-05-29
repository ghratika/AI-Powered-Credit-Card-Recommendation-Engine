"""Account Aggregator (synthetic) transaction models."""

from __future__ import annotations

from datetime import date
from enum import Enum

from pydantic import BaseModel, Field, field_validator


class TransactionType(str, Enum):
    DEBIT = "debit"
    CREDIT = "credit"


class Transaction(BaseModel):
    """Single synthetic AA transaction."""

    date: date
    amount_inr: float = Field(..., gt=0)
    category: str = Field(..., min_length=1)
    merchant: str = Field(..., min_length=1)
    type: TransactionType = TransactionType.DEBIT

    @field_validator("category")
    @classmethod
    def normalize_category(cls, value: str) -> str:
        return value.strip().lower()


class AAPayload(BaseModel):
    """Synthetic Account Aggregator file payload."""

    user_ref: str = Field(..., min_length=1)
    transactions: list[Transaction] = Field(default_factory=list)


class SpendProfile(BaseModel):
    """Aggregated annual spend by category (populated in Phase 2)."""

    annual_by_category: dict[str, float] = Field(default_factory=dict)
    total_annual: float = Field(default=0, ge=0)
