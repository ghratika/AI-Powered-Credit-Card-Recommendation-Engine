# Project Context: AI-Powered Credit Card Recommendation Engine

This document captures the full context from the project problem statement. Use it as the single source of truth for scope, workflow, and deliverables when building the application.

---

## Overview

**Use case:** FreechargeBiz-style credit card recommendation  
**Goal:** Build an AI-powered service that suggests the best **Axis Bank** credit card for a user by combining structured card data with a **Large Language Model (LLM)**.

The system must intelligently recommend cards based on the user's financial profile, eligibility, and simulated spending patterns—not only static rules.

---

## Core Objective

Design and implement an application that:

| Capability | Description |
|------------|-------------|
| User inputs | Accept **Annual Income**, **PAN**, and **Mobile** |
| Card catalog | Use a curated, structured dataset of **Axis Bank** credit cards |
| Spending simulation | Use **synthetic Account Aggregator (AA)** transaction data (provided by developer/system) to mimic real spending |
| AI layer | Use an **LLM** for personalized, human-like recommendations and **savings simulations** |
| UX | Display clear, actionable results to the user |

---

## System Workflow

### 1. Data Ingestion

- Load Axis Bank product data from **`data/processed/cards.json`**
- Ingest synthetic **Account Aggregator (AA)** transaction payload (developer/system supplied)
- Extract fields such as:
  - Card name
  - Annual fee
  - Reward categories
  - APR
  - Other product attributes as needed for ranking and simulation

### 2. User Input

Collect:

- **Annual Income**
- **PAN Number**
- **Mobile Number**
- **Account Aggregator connection** (simulated trigger—no live AA integration required for the exercise)

### 3. Integration Layer

- **Filter** credit cards by eligibility (e.g. **Income**, **CIBIL** where applicable)
- **Merge** filtered card list with AA transaction data
- **Prepare** structured context for the LLM
- **Design prompts** so the LLM can:
  - Reason over cards vs. spending
  - Rank options
  - Simulate reward ROI

### 4. Recommendation Engine (LLM)

The LLM should:

- **Rank** credit cards by fit for the user
- **Explain** why each recommendation matches the user's spending patterns
- **Calculate / simulate** total annual rewards (**net benefit**)

### 5. Output Display

Present top recommendations in a user-friendly format including:

| Field | Purpose |
|-------|---------|
| Card name & image | Identification and trust |
| Confidence score | Strength of fit |
| Net annual benefit | Rewards simulator outcome |
| AI-generated explanation | Why this card fits the user |

---

## Data & Integration Assumptions

- **Cards:** Structured JSON at `data/processed/cards.json` (Axis Bank products only)
- **Transactions:** Synthetic AA data—not production Account Aggregator; supplied to simulate categories and spend volume
- **Eligibility:** Filter on income and CIBIL (and any other fields present in card data)
- **LLM:** Central to ranking, explanation, and reward simulation—not a optional add-on

---

## High-Level Architecture (Conceptual)

```
User Input (Income, PAN, Mobile, AA trigger)
        │
        ▼
Data Ingestion (cards.json + synthetic AA payload)
        │
        ▼
Integration Layer (eligibility filter + merge + prompt build)
        │
        ▼
LLM Recommendation Engine (rank, explain, simulate rewards)
        │
        ▼
Output UI (top cards, scores, net benefit, explanations)
```

---

## Success Criteria (Implicit from Problem Statement)

1. End-to-end flow from user input through LLM to displayed recommendations  
2. Recommendations grounded in **structured card data** and **AA-style spend patterns**  
3. Outputs include **ranking**, **confidence**, **net annual benefit**, and **natural-language rationale**  
4. Experience suitable for a **FreechargeBiz**-style product discovery flow  

---

## Out of Scope (Unless Extended Later)

- Live Account Aggregator or bank API integration  
- Non–Axis Bank card catalogs  
- Production PAN/mobile verification or regulatory compliance beyond simulation  

---

## Source

Derived from `docs/problemStatement.txt` — AI-Powered Credit Card Recommendation Engine (FreechargeBiz Use Case).
