# Manual Test Log (Phase 6)

Use this checklist to validate the full pipeline with **live Groq** (optional) or **mock LLM** (`LLM_MOCK=true`). Record results in the table at the bottom.

## Prerequisites

```bash
# Terminal 1 — API (mock or Groq)
cd backend
set LLM_MOCK=true          # Windows CMD; use export on macOS/Linux
python -m uvicorn app.main:app --reload --port 8000

# Terminal 2 — UI
cd frontend
npm install
npm run dev
```

Open http://localhost:5173. Vite proxies `/api` → `http://localhost:8000`.

---

## Persona 1: High dining spend

| Field | Value |
|-------|--------|
| Annual income | ₹12,00,000 |
| PAN | `ABCDE1234F` |
| Mobile | `9876543210` |
| CIBIL | 780 |
| AA data | `data/synthetic/aa_dining_heavy.json` |

**Start backend with dining AA file:**

```bash
set AA_DATA_PATH=../data/synthetic/aa_dining_heavy.json
python -m uvicorn app.main:app --reload --port 8000
```

**Expected (mock LLM):** Top recommendations mention **dining** spend; cards like **My Zone**, **Flipkart**, or **ACE** (dining/food rewards) rank highly.

**Expected (live Groq):** Rank #1 explanation references high dining; `net_annual_benefit_inr` plausible vs ~₹1.5–2L annual dining × earn rate − fee.

**CLI smoke test:**

```bash
cd backend
set AA_DATA_PATH=../data/synthetic/aa_dining_heavy.json
python scripts/run_persona_recommendation.py dining
```

---

## Persona 2: High travel spend

| Field | Value |
|-------|--------|
| Annual income | ₹12,00,000 |
| PAN | `ABCDE1234F` |
| Mobile | `9876543210` |
| CIBIL | 780 |
| AA data | `data/synthetic/aa_travel_heavy.json` |

```bash
set AA_DATA_PATH=../data/synthetic/aa_travel_heavy.json
python -m uvicorn app.main:app --reload --port 8000
```

**Expected:** **Vistara**, **Magnus Lite**, or travel-heavy products rank above shopping-only cards; explanations cite travel category amounts.

```bash
python scripts/run_persona_recommendation.py travel
```

---

## Persona 3: Balanced spend

| Field | Value |
|-------|--------|
| Annual income | ₹12,00,000 |
| PAN | `ABCDE1234F` |
| Mobile | `9876543210` |
| CIBIL | 780 |
| AA data | `data/synthetic/aa_balanced.json` (or default `aa_transactions.json`) |

**Expected:** Mix of categories in explanations; **ACE** (utilities) or **Flipkart** (shopping) often competitive when utilities/shopping are strong in the default file.

```bash
python scripts/run_persona_recommendation.py balanced
```

---

## Edge case: No eligible cards (Phase 6.6)

| Field | Value |
|-------|--------|
| Annual income | ₹50,000 |
| CIBIL | 300 |
| AA | Connected |

**Expected API:** `404` with `NO_ELIGIBLE_CARDS`.

**Expected UI:** “No cards match your profile” page with **Edit Profile** button.

---

## Live Groq spot-check (Phase 6.5)

For each persona, run **once** with:

```bash
set LLM_MOCK=false
set GROQ_API_KEY=gsk_...
python scripts/run_persona_recommendation.py dining
```

Verify:

1. Response JSON has `rank`, `confidence_score`, `net_annual_benefit_inr`, `explanation` per card.
2. All `card_id` values exist in `data/processed/cards.json`.
3. Net benefit is order-of-magnitude reasonable (not negative unless fee >> rewards).

---

## Automated tests (Phase 6)

| Layer | Command |
|-------|---------|
| Unit + integration | `cd backend && python -m pytest` |
| Contract (mock LLM fixture) | `pytest tests/test_contract.py` |
| E2E (Playwright) | `cd frontend && npm run test:e2e` |

---

## Results log (fill when testing)

| Date | Tester | Persona | LLM mode | Top card #1 | Pass? | Notes |
|------|--------|---------|----------|-------------|-------|-------|
| | | Dining heavy | mock | | ☐ | |
| | | Travel heavy | mock | | ☐ | |
| | | Balanced | mock | | ☐ | |
| | | Dining heavy | Groq live | | ☐ | |
| | | Travel heavy | Groq live | | ☐ | |
| | | Balanced | Groq live | | ☐ | |
| | | No eligible (₹50k) | mock | N/A | ☐ | 404 + UI empty state |
