# AI-Powered Credit Card Recommendation Engine

FreechargeBiz-style Axis Bank credit card recommendations using structured catalog data, synthetic Account Aggregator spend, and an LLM.

## Documentation

- [Project context](docs/context.md)
- [Architecture](docs/architecture.md)
- [Implementation plan](docs/implementation-plan.md)
- [Deployment (Vercel + Railway)](docs/deployment.md)
- [Manual test log (Phase 6)](docs/manual-test-log.md)
- [Edge cases](docs/edge-cases.md)
- [Data files](data/README.md)

## Quick start (full stack)

```bash
# Terminal 1 — API (mock LLM, no Groq key required)
cd backend
pip install -r requirements.txt
set LLM_MOCK=true
python -m uvicorn app.main:app --reload --port 8000

# Terminal 2 — UI (proxies /api → :8000)
cd frontend
npm install
npm run dev
```

Open http://localhost:5173 → connect AA → get recommendations.

## Phase 7: Deployment (Vercel + Railway)

| Service | Platform | Config |
|---------|----------|--------|
| Frontend | **Vercel** (`frontend/`) | `VITE_API_BASE_URL` → Railway `/api/v1` |
| Backend | **Railway** (root `Dockerfile`) | `GROQ_API_KEY`, `CORS_ORIGINS`, `CORS_ORIGIN_REGEX` |

Step-by-step: **[docs/deployment.md](docs/deployment.md)**.

**Demo profile (evaluators):**

| Field | Value |
|-------|-------|
| Annual income | `1200000` |
| PAN | `ABCDE1234F` |
| Mobile | `9876543210` |

Connect Account Aggregator before submit. Disclaimer appears on results.

---

## Phase 6: Integration & testing

| Task | Status |
|------|--------|
| Vite `/api` proxy → `:8000` | `frontend/vite.config.ts` |
| Playwright E2E | `frontend/e2e/*.spec.ts` |
| Contract test (mock LLM → schema) | `backend/tests/test_contract.py` |
| Manual personas | `docs/manual-test-log.md` + `data/synthetic/aa_*_heavy.json` |
| No eligible cards UI | `NoEligiblePage` + API 404 test |
| GitHub Actions CI | `.github/workflows/ci.yml` |

```bash
# Backend (unit + integration + contract)
cd backend
python -m pytest

# Frontend build
cd frontend
npm run build

# E2E (starts backend + Vite automatically)
cd frontend
npm install
npx playwright install chromium
npm run test:e2e
```

Persona CLI (mock or live Groq):

```bash
cd backend
set LLM_MOCK=true
python scripts/run_persona_recommendation.py dining
python scripts/run_persona_recommendation.py travel
python scripts/run_persona_recommendation.py balanced
```

---

## Phase 5: Frontend UI

React + Vite app with Freecharge design tokens (`frontend/src/styles/theme.css`), profile form, simulated AA connect, loading state, and results cards.

---

## Phase 4: REST API + Groq

```bash
cd backend
python -m pip install -r requirements.txt
python -m uvicorn app.main:app --reload --port 8000
```

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/v1/health` | GET | Liveness |
| `/api/v1/aa/connect` | POST | Simulated AA connect |
| `/api/v1/recommendations` | POST | Get recommendations |
| `/docs` | GET | OpenAPI Swagger UI |

Copy `.env.example` → `.env` and set `GROQ_API_KEY` for live Groq inference (`llama-3.3-70b-versatile`). Without a key, the API uses the mock LLM.

```bash
curl -X POST http://localhost:8000/api/v1/recommendations ^
  -H "Content-Type: application/json" ^
  -d "{\"annual_income_inr\":1200000,\"pan\":\"ABCDE1234F\",\"mobile\":\"9876543210\",\"aa_connected\":true,\"cibil\":780}"
```

---

## Phase 3: LLM integration & orchestration

End-to-end recommendation without HTTP:

| Module | Role |
|--------|------|
| `app/domain/prompt_builder.py` | System + user JSON prompts |
| `app/services/llm_client.py` | OpenAI client + `MockLLMClient` |
| `app/domain/normalizer.py` | Parse, validate, enrich LLM JSON |
| `app/services/orchestrator.py` | `recommend(profile)` pipeline |

```bash
cd backend
python -m pip install -r requirements.txt
python -m pytest
# Mock LLM (no API key):
python scripts/run_recommendation.py
# Live Groq:
set GROQ_API_KEY=gsk_...
set LLM_MOCK=false
python scripts/run_recommendation.py
```

---

## Phase 2: Deterministic domain logic

Rule-based preprocessing before the LLM:

| Module | Functions |
|--------|-----------|
| `app/models/user.py` | `UserProfile`, `EligibleCard` |
| `app/domain/validators.py` | PAN, mobile, income, CIBIL validation |
| `app/domain/eligibility.py` | `filter_eligible_cards()` |
| `app/domain/spend_aggregator.py` | `build_spend_profile()` |
| `app/domain/category_mapping.py` | `normalize_spend_category()` (e.g. `food` → `dining`) |

```bash
cd backend
python -m pytest
python scripts/verify_phase2.py
```

Demo profile (₹12L income, CIBIL 780) → **6 eligible cards**; AA spend aggregated across 12 months.

---

## Phase 1: Data foundation

### Layout

```
data/processed/cards.json          # 8 Axis Bank cards
data/synthetic/aa_transactions.json  # 12+ months synthetic AA spend
backend/app/models/                # Pydantic models
backend/app/domain/ingestion.py    # load_cards(), load_aa_transactions()
frontend/public/assets/cards/      # SVG placeholders per card
```

### Backend setup

```bash
cd backend
python -m pip install -r requirements.txt
python -m pytest
python scripts/verify_data.py
```

Optional environment overrides:

- `CARDS_DATA_PATH` — path to `cards.json`
- `AA_DATA_PATH` — path to `aa_transactions.json`

### Usage

```python
from app.domain.ingestion import load_cards, load_aa_transactions

cards = load_cards()           # list[CardProduct], cached
aa = load_aa_transactions()   # AAPayload with .transactions
```
