"""Tests for recommendation orchestrator (Phase 3)."""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from app.domain.exceptions import AANotConnectedError, LLMServiceError, NoEligibleCardsError
from app.models.user import UserProfile
from app.services.llm_client import LLMClient, MockLLMClient
from app.services.orchestrator import RecommendationOrchestrator, recommend


@pytest.fixture
def demo_profile() -> UserProfile:
    return UserProfile.from_raw(
        annual_income_inr=1_200_000,
        pan="ABCDE1234F",
        mobile="9876543210",
        aa_connected=True,
    )


@pytest.fixture
def mock_llm_client() -> MockLLMClient:
    fixture = Path(__file__).parent / "fixtures" / "mock_llm_response.json"
    return MockLLMClient(fixture_path=str(fixture))


def test_recommend_success(demo_profile: UserProfile, mock_llm_client: MockLLMClient) -> None:
    result = recommend(demo_profile, llm_client=mock_llm_client)

    assert len(result.recommendations) == 3
    assert result.recommendations[0].rank == 1
    assert result.recommendations[0].card_name
    assert result.recommendations[0].explanation
    assert result.meta.aa_connected is True
    assert result.meta.eligible_count >= 1


def test_aa_not_connected_raises() -> None:
    profile = UserProfile.from_raw(
        annual_income_inr=1_200_000,
        pan="ABCDE1234F",
        mobile="9876543210",
        aa_connected=False,
    )
    with pytest.raises(AANotConnectedError):
        recommend(profile, llm_client=MockLLMClient())


def test_no_eligible_cards_raises() -> None:
    profile = UserProfile.from_raw(
        annual_income_inr=50_000,
        pan="LOWCB1234L",
        mobile="9876543210",
        aa_connected=True,
    )
    with pytest.raises(NoEligibleCardsError):
        recommend(profile, llm_client=MockLLMClient())


class BrokenThenFixedLLM(LLMClient):
    def __init__(self, valid_json: str) -> None:
        self._valid = valid_json
        self.calls = 0

    def complete(self, messages: list[dict[str, str]]) -> str:
        self.calls += 1
        if self.calls == 1:
            return "not valid json {{"
        return self._valid


def test_llm_json_retry(demo_profile: UserProfile) -> None:
    fixture = Path(__file__).parent / "fixtures" / "mock_llm_response.json"
    valid = fixture.read_text(encoding="utf-8")
    client = BrokenThenFixedLLM(valid)

    result = RecommendationOrchestrator(llm_client=client).recommend(demo_profile)
    assert client.calls == 2
    assert len(result.recommendations) >= 1


class AlwaysBrokenLLM(LLMClient):
    def complete(self, messages: list[dict[str, str]]) -> str:
        return "{ broken"


def test_llm_json_retry_exhausted_raises(demo_profile: UserProfile) -> None:
    with pytest.raises(LLMServiceError, match="after retry"):
        RecommendationOrchestrator(llm_client=AlwaysBrokenLLM()).recommend(demo_profile)


def test_mock_llm_dynamic_client(demo_profile: UserProfile) -> None:
    """MockLLMClient without fixture builds JSON from eligible cards."""
    result = recommend(demo_profile, llm_client=MockLLMClient())
    assert len(result.recommendations) >= 1
    ids = {r.card_id for r in result.recommendations}
    assert ids.issubset(
        {
            "axis-neo",
            "axis-magnus-lite",
            "axis-flipkart",
            "axis-my-zone",
            "axis-ace",
            "axis-vistara",
        }
    )
