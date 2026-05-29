# Google Stitch Design Prompt — AI Credit Card Recommendation (FreechargeBiz)

Copy the prompt below into Google Stitch to generate frontend UI designs aligned with project scope and architecture.

---

## Prompt (copy from here)

Design a complete **mobile-first web application UI** for an **AI-Powered Axis Bank Credit Card Recommendation Engine** in the style of **FreechargeBiz** (B2B fintech product discovery). This is a demo app that helps users find the best Axis Bank credit card based on income, CIBIL, and simulated Account Aggregator (AA) spending data, with AI-generated rankings and explanations.

### Brand & visual identity (mandatory)

**Enforce the Freecharge Visual Identity strictly:**

| Token | Hex | Usage |
|-------|-----|--------|
| **Primary Orange** | `#FF6B35` | Primary CTAs, active states, progress fills, key highlights, “Connect AA” success accents |
| **Dark Navy** | `#0A192F` | Headings, body text, icons, nav labels, card titles, emphasis |
| **Off-white background** | `#F8F9FA` | Page backgrounds, section fills |
| **White** | `#FFFFFF` | Cards, input fields, modals, recommendation tiles |
| **Muted text** | `#6B7280` | Helper text, disclaimers, placeholders |
| **Success green** | `#10B981` | AA connected badge, validation success |
| **Error red** | `#EF4444` | Inline errors, toast errors |

- Typography: modern sans-serif (Inter, DM Sans, or similar). Clear hierarchy: bold navy headings, regular navy body.
- UI feel: **clean, trustworthy, professional fintech** — generous whitespace, rounded corners (12–16px on cards), subtle shadows on elevated cards, no clutter.
- Buttons: primary = solid `#FF6B35` with white label; secondary = white/navy outline on off-white; disabled = 40% opacity.
- Do **not** use purple gradients, generic bank blue, or unrelated brand colors.

### Product context

- **Partner bank:** Axis Bank only (8 credit cards: Neo, Magnus Lite, Flipkart, My Zone, ACE, Vistara, Magnus, Reserve).
- **AI-powered:** Recommendations are ranked by an LLM using spend patterns; show “AI-powered” subtly (small badge or sparkle icon in navy/orange).
- **Simulated AA:** User must “Connect Account Aggregator” before getting results — this is a **demo simulation**, not live banking.
- **Disclaimer (always visible on results):** “Simulated recommendations for demonstration only. Not financial advice.”

### User flow (design all screens)

```
Landing / Profile → Connect AA (simulated) → Loading (AI) → Results (top 3 cards)
```

1. **Landing / Profile input page**
   - Hero: “Find your best Axis Bank credit card” + subcopy about personalized AI recommendations from spending patterns.
   - Form fields:
     - Annual Income (₹) — numeric input
     - PAN Number — masked format hint `AAAAA9999A`
     - Mobile Number — 10-digit Indian mobile
     - CIBIL Score (optional) — slider or numeric 300–900, default 750
   - Section: **Account Aggregator** with explanatory copy (“Connect securely to analyze your spending patterns”).
   - Primary CTA: **“Connect Account Aggregator”** (orange) — shows connected state after tap (green check + “Connected · demo-user-1”).
   - Secondary CTA: **“Get Recommendations”** (orange, full-width) — **disabled** until AA is connected; enabled when connected.
   - Inline validation error states for invalid PAN/mobile/income (red helper text).
   - Top bar: FreechargeBiz-style logo placeholder + “Credit Card Advisor” in navy.

2. **Loading state (full-screen or inline overlay)**
   - Shown after “Get Recommendations” while AI processes (5–30 seconds).
   - Orange subtle pulse or progress animation.
   - Copy: “Analyzing your spend and matching Axis Bank cards…”
   - 3 skeleton recommendation card placeholders (shimmer on off-white).

3. **Results page**
   - Header: “Your top recommendations” + meta line “Based on ₹12L income · 6 eligible cards”.
   - **Ranked list (top 3 cards)**, each as a large card tile:
     - **Rank badge** (#1, #2, #3) — #1 gets orange accent border or ribbon.
     - **Card image** placeholder (credit card visual, 16:10 ratio).
     - **Card name** (e.g. “Axis Bank ACE Credit Card”) — navy, bold.
     - **Quick Stats row** (soft grey `#6B7280`, between card name and match score): horizontal row with icon + **Reward Rate** (e.g. “5%” from `reward_rate_percent`) and icon + **APR** (e.g. “42%” from `apr_percent`); subtle divider between items; must not compete visually with Match Score or Savings.
     - **Confidence score** — horizontal progress bar (orange fill) + label “92% match”.
     - **Net annual benefit** — prominent metric: “₹15,000 / year estimated savings” with small “after annual fee” sublabel.
     - **AI explanation** — 2–4 sentence paragraph in muted navy/gray, conversational tone example: “Your high utility spend aligns with 5% cashback on bill pay…”
     - Optional: expand “Why this card?” chevron.
   - Footer disclaimer bar (muted, small type).
   - Sticky bottom or top: **“Start over”** text link in navy.

4. **Error & empty states (design variants)**
   - **AA not connected (422):** toast or banner — “Connect Account Aggregator to get personalized results.”
   - **No eligible cards (404):** empty illustration + “No cards match your profile. Try adjusting income or CIBIL.”
   - **LLM / server error (502):** friendly error card + **“Retry”** orange button.
   - **Validation error (400):** field-level red borders + messages.

5. **Optional: AA connect success micro-modal**
   - Small modal/sheet: green check, “Account Aggregator connected”, “Analyzing demo spending profile”, dismiss CTA.

### Components to include in design system

- Text inputs with labels and ₹ prefix for income
- Primary / secondary / disabled buttons
- AA connection card (disconnected vs connected states)
- Recommendation card (rank 1–3 variants)
- Confidence progress bar
- Skeleton loaders
- Toast notifications (success/error)
- Disclaimer footer component
- Badge: “AI-powered”, “Best match”, “Simulated demo”

### Layout & responsiveness

- **Mobile first** (375px width primary artboard).
- **Desktop** (1280px): centered max-width container (~480–720px for form, ~960px for results grid or stacked cards).
- Touch-friendly tap targets (min 44px height on buttons).
- Safe areas for notched phones.

### Content & tone

- Voice: helpful, clear, confident — not salesy.
- Use **₹** for all money (Indian locale).
- Avoid jargon; explain AA in one simple sentence.
- Axis Bank co-branding: small “Powered by AI · Axis Bank cards only” subline.

### Technical hints for developers (annotate in design if possible)

- API: `POST /api/v1/recommendations`, `POST /api/v1/aa/connect`
- Results fields: `card_name`, `image_url`, `reward_rate_percent`, `apr_percent`, `confidence_score` (0–1 → show as %), `net_annual_benefit_inr`, `explanation`, `rank`
- Flow: form → connect AA → submit → loading → results

### Deliverables requested from Stitch

Generate high-fidelity mockups for:
1. Profile / landing (AA disconnected)
2. Profile / landing (AA connected, CTA enabled)
3. Loading state
4. Results — 3 recommendation cards (show rank #1 emphasized)
5. Error state (no eligible cards)
6. Mobile + desktop breakpoint for results page

**Style reference:** FreechargeBiz B2B fintech — orange energy, navy trust, off-white calm backgrounds. Modern, minimal, conversion-focused product discovery.

---

## End of prompt
