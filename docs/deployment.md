# Deployment (Phase 7)

Split deployment: **frontend on Vercel**, **backend on Railway**.

```
Browser → Vercel (static React) → Railway (FastAPI + Groq + data/)
```

## Prerequisites

- [Groq API key](https://console.groq.com/)
- GitHub repo connected to [Railway](https://railway.com/) and [Vercel](https://vercel.com/)

---

## 1. Deploy backend (Railway)

1. Create a new Railway project → **Deploy from GitHub repo**.
2. Use the **repository root** (Dockerfile and `data/` must be in the build context).
3. Railway detects `railway.toml` and builds with the root `Dockerfile`.
4. Set **Variables** (Railway dashboard → service → Variables):

| Variable | Required | Example |
|----------|----------|---------|
| `GROQ_API_KEY` | Yes (or `LLM_MOCK=true` for demo) | `gsk_...` |
| `GROQ_MODEL` | No | `llama-3.3-70b-versatile` |
| `LLM_MOCK` | No | `false` |
| `CORS_ORIGINS` | Yes | `https://your-app.vercel.app` |
| `CORS_ORIGIN_REGEX` | Recommended | `https://.*\.vercel\.app` |
| `LOG_FORMAT` | No | `json` |
| `TOP_N_RECOMMENDATIONS` | No | `3` |

5. Deploy and copy the public URL (e.g. `https://ai-powered-credit-card-recommendation-engine-production.up.railway.app`).
6. Verify (do **not** use the bare domain root alone before the root route exists):
   - `GET https://<railway-host>/api/v1/health` → `{"status":"ok"}`
   - `GET https://<railway-host>/` → service info JSON
   - `https://<railway-host>/docs` → Swagger UI

Visiting only `https://<railway-host>/` on older deploys without a root route returned `{"detail":"Not Found"}` — that is normal; the API lives under `/api/v1/`.

**Note:** `CARDS_DATA_PATH` and `AA_DATA_PATH` default to `/app/data/...` inside the Docker image. Do not change unless you mount custom data.

---

## 2. Deploy frontend (Vercel)

1. Import the same GitHub repo in Vercel.
2. Set **Root Directory** to `frontend`.
3. Framework preset: **Vite** (or use `frontend/vercel.json`).
4. Add **Environment Variable**:

| Name | Value |
|------|--------|
| `VITE_API_BASE_URL` | `https://<railway-host>/api/v1` |

5. Deploy. Open the Vercel URL and run the full flow (profile → AA connect → recommendations).

6. If you use a **custom domain** on Vercel, add that origin to Railway `CORS_ORIGINS`.

---

## 3. Local production-like check

```bash
# Terminal 1 — API
cd backend
set LLM_MOCK=true
python -m uvicorn app.main:app --port 8000

# Terminal 2 — UI pointing at local API
cd frontend
set VITE_API_BASE_URL=http://127.0.0.1:8000/api/v1
npm run build
npm run preview
```

---

## 4. Security checklist

- Never commit `.env` or `GROQ_API_KEY`.
- Keep Groq key only on Railway (server-side).
- `VITE_*` variables are exposed to the browser — only use public API URLs there.

---

## 5. Demo credentials (evaluators)

| Field | Example |
|-------|---------|
| Annual income | `1200000` (₹12L) |
| PAN | `ABCDE1234F` |
| Mobile | `9876543210` |

Connect Account Aggregator before submitting. See [manual-test-log.md](./manual-test-log.md) for persona scenarios.
