"""LLM provider clients — Groq for live calls, mock for CI/local."""

from __future__ import annotations

import json
import logging
from abc import ABC, abstractmethod

from app.config import (
    get_groq_api_key,
    get_groq_base_url,
    get_groq_model,
    normalize_groq_base_url,
    use_llm_mock,
    LLM_MAX_TOKENS,
    LLM_TEMPERATURE,
    LLM_TIMEOUT_SECONDS,
)

logger = logging.getLogger(__name__)


class LLMClient(ABC):
    """Abstract LLM client returning raw assistant text."""

    @abstractmethod
    def complete(self, messages: list[dict[str, str]]) -> str:
        """Send chat messages and return assistant content."""


class GroqLLMClient(LLMClient):
    """Groq chat completions with JSON response format."""

    def __init__(
        self,
        *,
        api_key: str,
        model: str | None = None,
        base_url: str | None = None,
        timeout: int = LLM_TIMEOUT_SECONDS,
        temperature: float = LLM_TEMPERATURE,
        max_tokens: int = LLM_MAX_TOKENS,
    ) -> None:
        from groq import Groq

        resolved_base = normalize_groq_base_url(base_url) if base_url else get_groq_base_url()
        self._client = Groq(api_key=api_key, base_url=resolved_base)
        self._model = model or get_groq_model()
        self._timeout = timeout
        self._temperature = temperature
        self._max_tokens = max_tokens

    def complete(self, messages: list[dict[str, str]]) -> str:
        response = self._client.chat.completions.create(
            model=self._model,
            messages=messages,
            response_format={"type": "json_object"},
            temperature=self._temperature,
            max_tokens=self._max_tokens,
            timeout=self._timeout,
        )
        content = response.choices[0].message.content
        if not content:
            raise RuntimeError("Groq returned empty content")
        return content


class MockLLMClient(LLMClient):
    """Deterministic LLM for tests and local runs without a Groq API key."""

    def __init__(self, fixture_path: str | None = None) -> None:
        self._fixture_path = fixture_path

    def complete(self, messages: list[dict[str, str]]) -> str:
        if self._fixture_path:
            from pathlib import Path

            return Path(self._fixture_path).read_text(encoding="utf-8")

        user_msg = next(
            (m["content"] for m in reversed(messages) if m["role"] == "user"),
            "{}",
        )
        payload = json.loads(user_msg)
        eligible = payload.get("eligible_cards", [])
        spend = payload.get("spend_profile", {}).get("annual_by_category", {})

        recommendations = []
        for rank, card in enumerate(eligible[:3], start=1):
            card_id = card["id"]
            top_category = max(spend, key=spend.get, default="spending") if spend else "spending"
            annual_fee = card.get("annual_fee_inr", 0)
            benefit = max(5000, spend.get(top_category, 0) * 0.05) - annual_fee
            recommendations.append(
                {
                    "rank": rank,
                    "card_id": card_id,
                    "card_name": card["name"],
                    "confidence_score": round(0.95 - (rank - 1) * 0.08, 2),
                    "net_annual_benefit_inr": round(benefit, 2),
                    "explanation": (
                        f"Your annual {top_category} spend of ₹{spend.get(top_category, 0):,.0f} "
                        f"pairs well with {card['name']} reward categories."
                    ),
                }
            )

        return json.dumps({"recommendations": recommendations}, ensure_ascii=False)


def get_llm_client() -> LLMClient:
    """Factory: mock if configured or no key; otherwise Groq."""
    if use_llm_mock():
        logger.info("Using mock LLM client (LLM_MOCK=true)")
        return MockLLMClient()

    api_key = get_groq_api_key()
    if not api_key:
        logger.warning("GROQ_API_KEY not set; using mock LLM client")
        return MockLLMClient()

    logger.info(
        "Using Groq LLM client (model=%s, base_url=%s)",
        get_groq_model(),
        get_groq_base_url(),
    )
    return GroqLLMClient(api_key=api_key, model=get_groq_model())
