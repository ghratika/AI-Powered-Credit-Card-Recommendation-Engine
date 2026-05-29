"""Simulated Account Aggregator routes."""

from __future__ import annotations

from fastapi import APIRouter

from app.api.schemas import AAConnectResponse
from app.domain.exceptions import DataUnavailableError
from app.domain.ingestion import DataLoadError, load_aa_transactions

router = APIRouter(prefix="/aa", tags=["account-aggregator"])


@router.post("/connect", response_model=AAConnectResponse)
def connect_aa() -> AAConnectResponse:
    """Simulate AA consent and return the synthetic spend profile id."""
    try:
        payload = load_aa_transactions()
    except DataLoadError as exc:
        raise DataUnavailableError(str(exc)) from exc

    return AAConnectResponse(connected=True, spend_profile_id=payload.user_ref)
