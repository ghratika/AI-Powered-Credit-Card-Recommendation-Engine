"""API integration tests (Phase 4)."""

from __future__ import annotations

from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.services.llm_client import MockLLMClient


@pytest.fixture
def mock_llm_fixture() -> Path:
    return Path(__file__).parent / "fixtures" / "mock_llm_response.json"


@pytest.fixture
def client(mock_llm_fixture: Path, monkeypatch: pytest.MonkeyPatch) -> TestClient:
    monkeypatch.setattr(
        "app.services.orchestrator.get_llm_client",
        lambda: MockLLMClient(fixture_path=str(mock_llm_fixture)),
    )
    return TestClient(app)


def test_health(client: TestClient) -> None:
    response = client.get("/api/v1/health")
    assert response.status_code == 200
    assert response.json()["status"] in {"ok", "degraded"}


def test_aa_connect(client: TestClient) -> None:
    response = client.post("/api/v1/aa/connect")
    assert response.status_code == 200
    data = response.json()
    assert data["connected"] is True
    assert data["spend_profile_id"] == "demo-user-1"


def test_recommendations_success(client: TestClient) -> None:
    response = client.post(
        "/api/v1/recommendations",
        json={
            "annual_income_inr": 1_200_000,
            "pan": "ABCDE1234F",
            "mobile": "9876543210",
            "aa_connected": True,
        },
    )
    assert response.status_code == 200
    assert "X-Request-ID" in response.headers

    data = response.json()
    assert len(data["recommendations"]) == 3
    assert data["recommendations"][0]["card_id"] == "axis-ace"
    assert data["recommendations"][0]["reward_rate_percent"] == 5.0
    assert data["recommendations"][0]["apr_percent"] == 42.0
    assert data["meta"]["eligible_count"] >= 1
    assert data["meta"]["aa_connected"] is True


def test_recommendations_invalid_pan(client: TestClient) -> None:
    response = client.post(
        "/api/v1/recommendations",
        json={
            "annual_income_inr": 1_200_000,
            "pan": "invalid",
            "mobile": "9876543210",
            "aa_connected": True,
        },
    )
    assert response.status_code == 400
    body = response.json()
    assert body["error"]["code"] == "VALIDATION_ERROR"
    assert "request_id" in body


def test_recommendations_aa_not_connected(client: TestClient) -> None:
    response = client.post(
        "/api/v1/recommendations",
        json={
            "annual_income_inr": 1_200_000,
            "pan": "ABCDE1234F",
            "mobile": "9876543210",
            "aa_connected": False,
        },
    )
    assert response.status_code == 422
    assert response.json()["error"]["code"] == "AA_NOT_CONNECTED"


def test_recommendations_no_eligible_cards(client: TestClient) -> None:
    response = client.post(
        "/api/v1/recommendations",
        json={
            "annual_income_inr": 50_000,
            "pan": "LOWCB1234L",
            "mobile": "9876543210",
            "aa_connected": True,
        },
    )
    assert response.status_code == 404
    assert response.json()["error"]["code"] == "NO_ELIGIBLE_CARDS"
