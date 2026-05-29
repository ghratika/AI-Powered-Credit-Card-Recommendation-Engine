"""Application configuration and default data paths."""

from __future__ import annotations

import os
from pathlib import Path

# Load .env from repository root when present.
try:
    from dotenv import load_dotenv

    load_dotenv(Path(__file__).resolve().parents[2] / ".env")
except ImportError:
    pass


def get_project_root() -> Path:
    """Repository root (parent of ``backend/``)."""
    return Path(__file__).resolve().parents[2]


PROJECT_ROOT = get_project_root()

DEFAULT_CARDS_PATH = PROJECT_ROOT / "data" / "processed" / "cards.json"
DEFAULT_AA_PATH = PROJECT_ROOT / "data" / "synthetic" / "aa_transactions.json"

DEFAULT_GROQ_MODEL = "llama-3.3-70b-versatile"
# Groq SDK appends `/openai/v1/...` paths; base must be the host root only.
DEFAULT_GROQ_BASE_URL = "https://api.groq.com"


def normalize_groq_base_url(url: str) -> str:
    """
    Normalize Groq base URL for the official SDK.

    The SDK requests ``/openai/v1/chat/completions`` relative to base_url.
    If base_url already ends with ``/openai/v1``, paths are doubled and Groq
    returns 404 (``/openai/v1/openai/v1/chat/completions``).
    """
    cleaned = url.strip().rstrip("/")
    if not cleaned:
        return DEFAULT_GROQ_BASE_URL
    suffix = "/openai/v1"
    if cleaned.endswith(suffix):
        cleaned = cleaned[: -len(suffix)]
    return cleaned.rstrip("/") or DEFAULT_GROQ_BASE_URL


def get_cards_data_path() -> Path:
    override = os.getenv("CARDS_DATA_PATH")
    return Path(override) if override else DEFAULT_CARDS_PATH


def get_aa_data_path() -> Path:
    override = os.getenv("AA_DATA_PATH")
    return Path(override) if override else DEFAULT_AA_PATH


def get_groq_api_key() -> str | None:
    key = os.getenv("GROQ_API_KEY", "").strip() or os.getenv("LLM_API_KEY", "").strip()
    return key or None


def get_groq_model() -> str:
    return os.getenv("GROQ_MODEL", "").strip() or os.getenv(
        "LLM_MODEL", DEFAULT_GROQ_MODEL
    )


def get_groq_base_url() -> str:
    raw = (
        os.getenv("GROQ_BASE_URL", "").strip()
        or os.getenv("LLM_BASE_URL", "").strip()
        or DEFAULT_GROQ_BASE_URL
    )
    return normalize_groq_base_url(raw)


def get_top_n_recommendations() -> int:
    raw = os.getenv("TOP_N_RECOMMENDATIONS", "3")
    try:
        value = int(raw)
    except ValueError:
        return 3
    return max(1, min(value, 10))


def use_llm_mock() -> bool:
    return os.getenv("LLM_MOCK", "").lower() in {"1", "true", "yes"}


def get_cors_origins() -> list[str]:
    raw = os.getenv("CORS_ORIGINS", "http://localhost:5173,http://127.0.0.1:5173")
    return [origin.strip() for origin in raw.split(",") if origin.strip()]


def get_cors_origin_regex() -> str | None:
    """Optional regex for preview deploys (e.g. ``https://.*\\.vercel\\.app``)."""
    raw = os.getenv("CORS_ORIGIN_REGEX", "").strip()
    return raw or None


LLM_TIMEOUT_SECONDS = int(os.getenv("LLM_TIMEOUT_SECONDS", "60"))
LLM_TEMPERATURE = float(os.getenv("LLM_TEMPERATURE", "0.3"))
LLM_MAX_TOKENS = int(os.getenv("LLM_MAX_TOKENS", "2048"))

# Legacy aliases for backward compatibility.
get_llm_api_key = get_groq_api_key
get_llm_model = get_groq_model
get_llm_base_url = get_groq_base_url
