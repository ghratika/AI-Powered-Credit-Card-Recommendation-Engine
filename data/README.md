# Data Files (Phase 1)

## `processed/cards.json`

Curated **Axis Bank** credit card catalog (8 products). Fields:

| Field | Description |
|-------|-------------|
| `id` | Unique slug (e.g. `axis-ace`) |
| `name` | Display name |
| `image_url` | Path under `frontend/public` (e.g. `/assets/cards/axis-ace.png`) |
| `annual_fee_inr` | Annual fee in INR |
| `apr_percent` | APR |
| `min_income_inr` | Minimum annual income for eligibility |
| `min_cibil` | Minimum CIBIL score |
| `reward_categories` | Category earn rates and optional monthly caps |
| `default_earn_rate_percent` | Base earn rate |
| `highlights` | Marketing bullets for LLM context |

## `synthetic/aa_transactions.json`

Simulated **Account Aggregator** payload for `demo-user-1`:

- 12+ months of transactions (Apr 2025 – Mar 2026)
- Categories: `dining`, `travel`, `fuel`, `shopping`, `utilities`, `others`
- Includes one `credit` (refund) row for edge-case testing

### Phase 6 persona files (manual / Groq testing)

| File | Persona | Use with |
|------|---------|----------|
| `aa_dining_heavy.json` | High dining spend | `AA_DATA_PATH` + `run_persona_recommendation.py dining` |
| `aa_travel_heavy.json` | High travel spend | `AA_DATA_PATH` + `run_persona_recommendation.py travel` |
| `aa_balanced.json` | Balanced categories | `AA_DATA_PATH` + `run_persona_recommendation.py balanced` |

See [docs/manual-test-log.md](../docs/manual-test-log.md) for the full checklist.

## Loading in code

```python
from app.domain.ingestion import load_cards, load_aa_transactions

cards = load_cards()
aa = load_aa_transactions()
```

Override paths with `CARDS_DATA_PATH` and `AA_DATA_PATH` environment variables.
