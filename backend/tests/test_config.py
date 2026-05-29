"""Tests for Groq configuration."""

from app.config import get_cors_origin_regex, normalize_groq_base_url


def test_normalize_strips_openai_v1_suffix() -> None:
    assert (
        normalize_groq_base_url("https://api.groq.com/openai/v1")
        == "https://api.groq.com"
    )


def test_normalize_preserves_host_root() -> None:
    assert normalize_groq_base_url("https://api.groq.com") == "https://api.groq.com"


def test_normalize_empty_uses_default() -> None:
    assert normalize_groq_base_url("") == "https://api.groq.com"


def test_cors_origin_regex_unset(monkeypatch) -> None:
    monkeypatch.delenv("CORS_ORIGIN_REGEX", raising=False)
    assert get_cors_origin_regex() is None


def test_cors_origin_regex_set(monkeypatch) -> None:
    monkeypatch.setenv("CORS_ORIGIN_REGEX", r"https://.*\.vercel\.app")
    assert get_cors_origin_regex() == r"https://.*\.vercel\.app"
