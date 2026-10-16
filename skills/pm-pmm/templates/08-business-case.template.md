---
id: PM-BA-NNN
type: business-case
agent: pm-business-analyst
status: draft
mode: discovery
risk_domain: business-viability-risk
created: YYYY-MM-DD
last_validated: YYYY-MM-DD
version: 0.1.0
frameworks_applied:
  - SaaS Metrics
  - Lean Canvas
  - NPV/IRR
  - Van Westendorp
cross_refs: []
---

<!-- AGENT GUIDANCE (pm-business-analyst):
  DISCOVERY MODE: Sections 1–4. Order-of-magnitude estimates only. Lean Canvas core 9 boxes. Target 1–2 pages.
  DELIVERY MODE: All sections. Full NPV/IRR model, SaaS metric projections, Van Westendorp pricing analysis.
  Framework trace:
    - Lean Canvas (Ash Maurya): 9-box model (Problem, Solution, UVP, Unfair Advantage, Customer Segments, Key Metrics, Channels, Cost Structure, Revenue Streams).
    - SaaS Metrics: ARR, MRR, NRR, GRR, CAC, LTV, LTV:CAC, Payback Period, Churn rate.
    - NPV/IRR: Net Present Value and Internal Rate of Return for investment decision.
    - Van Westendorp Price Sensitivity Meter: 4-question survey yielding acceptable price range.
  This document justifies investment. Must be honest about risks — optimistic-only cases fail scrutiny.
-->

# Business Case: {Initiative Name}

> **Status:** DRAFT — Discovery mode. Order-of-magnitude estimates only.
> **ID:** PM-BA-NNN
> **Agent:** pm-business-analyst
> **Risk Domain:** Business Viability Risk — does the unit economics work?
> **Mode:** DISCOVERY

---

## Document Sections

| Section | Purpose | Mode |
|---------|---------|------|
| [1. Executive Summary](#1-executive-summary) | Decision brief | Both |
| [2. Lean Canvas](#2-lean-canvas) | 9-box business model snapshot | Both |
| [3. Market Opportunity](#3-market-opportunity) | Addressable market summary | Both |
| [4. Financial Projections (Order of Magnitude)](#4-financial-projections-order-of-magnitude) | High-level estimates | Both |
| [5. SaaS Unit Economics](#5-saas-unit-economics) | Full metric projections | Delivery |
| [6. NPV / IRR Analysis](#6-npv--irr-analysis) | Investment return model | Delivery |
| [7. Pricing Analysis (Van Westendorp)](#7-pricing-analysis-van-westendorp) | Price sensitivity and range | Delivery |
| [8. Risk Assessment](#8-risk-assessment) | Downside and sensitivity analysis | Delivery |
| [9. Investment Decision](#9-investment-decision) | Recommendation with conditions | Delivery |

---

## 1. Executive Summary

<!-- AGENT: Lead with the decision required, not the analysis. The reader decides — your job is to equip them. -->

**Decision Required:**
> {State the specific investment decision being requested: build vs. buy, new product launch, feature investment, market expansion, etc.}

**Investment Ask:**
- Engineering: {$X or person-months}
- Marketing/Sales: {$X}
- Other: {$X}
- Total: {$X over {N} months}

**Expected Return (order of magnitude):**
- ARR impact: {$X–$Y range} by month {N}
- Payback period: {N months}
- NPV (3-year): {$X} at {discount rate}%

**Recommendation:** {INVEST / DO NOT INVEST / INVEST WITH CONDITIONS}

**Key Conditions:** {What must be true for this investment to be approved?}

---

## 2. Lean Canvas

<!-- Lean Canvas (Ash Maurya, adapted from Business Model Canvas): 9 boxes, optimized for validated learning. -->
<!-- AGENT: Complete all 9 boxes. Discovery mode: brief phrases. Delivery mode: full elaboration. -->

| Box | Content |
|-----|---------|
| **1. Problem** | Top 3 problems this solves: (1) {problem}, (2) {problem}, (3) {problem} |
| **2. Customer Segments** | Target: {segment}. Early adopters: {specific early adopter profile} |
| **3. Unique Value Proposition** | {Single, clear, compelling value statement} |
| **4. Solution** | Top 3 features/capabilities: (1) {capability}, (2) {capability}, (3) {capability} |
| **5. Channels** | Path to customers: {direct / indirect / partner / product-led} channels |
| **6. Revenue Streams** | How we make money: {pricing model} at {price point} |
| **7. Cost Structure** | Highest costs: {COGS, R&D, S&M breakdown} |
| **8. Key Metrics** | Measure success by: {north star metric} and {supporting metrics} |
| **9. Unfair Advantage** | Cannot be easily copied: {unique asset, capability, or network effect} |

---

## 3. Market Opportunity

<!-- Cross-reference market-sizing.md (PM-BA-NNN) for full TAM/SAM/SOM analysis. -->
<!-- AGENT DISCOVERY: Summary figures only. Reference market-sizing doc for full methodology. -->

| Level | Size | Basis |
|-------|------|-------|
| TAM (Total Addressable Market) | ${B/M} | {top-down estimate basis — source} |
| SAM (Serviceable Addressable Market) | ${B/M} | {our current reach basis} |
| SOM (Serviceable Obtainable Market) | ${M} | {realistic 3-year capture — basis} |

**Market Timing:**
> Why now? {Describe the market or technology shift that makes this the right time to invest.}

---

## 4. Financial Projections (Order of Magnitude)

<!-- AGENT DISCOVERY: Use ranges, not point estimates. State assumptions explicitly. -->

| Metric | Year 1 | Year 2 | Year 3 | Key Assumption |
|--------|--------|--------|--------|----------------|
| New ARR | ${X–Y}M | ${X–Y}M | ${X–Y}M | {assumption} |
| Total ARR | ${X–Y}M | ${X–Y}M | ${X–Y}M | {cumulative assumption} |
| Gross Margin | {X–Y}% | {X–Y}% | {X–Y}% | {COGS assumption} |
| Investment Required | ${X}M | ${X}M | ${X}M | {investment basis} |

**Base Case Assumption:** {Describe the most likely scenario underpinning these numbers}
**Bear Case:** {What happens if the most important assumption is wrong}
**Bull Case:** {What happens if everything goes better than expected}

---

<!-- DELIVERY MODE SECTIONS -->

## 5. SaaS Unit Economics

<!-- SaaS Metrics: The engine of SaaS financial health. Must model cohort-level behavior, not averages. -->
<!-- Key ratios: LTV:CAC >= 3x (healthy). Payback Period < 12 months (efficient). NRR > 100% (growing). -->

### Customer Acquisition

| Metric | Value | Basis / Calculation |
|--------|-------|---------------------|
| CAC (blended) | ${X} | {total S&M spend / new customers acquired} |
| CAC Payback Period | {N} months | {CAC / (ACV × Gross Margin)} |
| CAC by Channel | | |
| — Organic / PLG | ${X} | {basis} |
| — Outbound Sales | ${X} | {basis} |
| — Paid Marketing | ${X} | {basis} |

### Customer Retention and Expansion

| Metric | Current | Target | Benchmark |
|--------|---------|--------|-----------|
| Gross Revenue Retention (GRR) | {%} | {%} | SaaS median: ~80–87% |
| Net Revenue Retention (NRR) | {%} | {%} | Best-in-class: >120% |
| Logo Churn Rate (annual) | {%} | {%} | {category benchmark} |
| Expansion Rate | {%} | {%} | {basis} |

### Customer Lifetime Value

| Metric | Value | Calculation |
|--------|-------|-------------|
| ARPU (Average Revenue Per User) | ${X}/month | {basis} |
| Gross Margin per Customer | {%} | {basis} |
| Average Customer Lifetime | {N} months | {1 / monthly churn rate} |
| LTV | ${X} | {ARPU × Gross Margin × Lifetime} |
| LTV:CAC Ratio | {X}x | {LTV / CAC} — target >= 3x |

**Cohort Analysis:**
> {Describe expected cohort retention curve and expansion behavior. At month 12, what % of initial ARR remains? What % is NRR > 100%?}

---

## 6. NPV / IRR Analysis

<!-- NPV: Net Present Value of investment. Positive NPV = value-creating. -->
<!-- IRR: Internal Rate of Return. Compare to hurdle rate (typically WACC or alternative investment benchmark). -->

| Field | Value |
|-------|-------|
| Discount Rate (WACC) | {X}% |
| Investment Horizon | {N} years |
| Total Investment | ${X}M |
| NPV (base case) | ${X}M |
| NPV (bear case) | ${X}M |
| IRR | {X}% |
| Hurdle Rate | {X}% |
| Recommendation | INVEST (IRR > hurdle) / DO NOT INVEST (IRR < hurdle) |

**NPV Sensitivity Table:**

| Scenario | ARR Growth Assumption | Churn Assumption | NPV |
|---------|----------------------|-----------------|-----|
| Bull case | {X}% | {X}% | ${X}M |
| Base case | {X}% | {X}% | ${X}M |
| Bear case | {X}% | {X}% | ${X}M |

---

## 7. Pricing Analysis (Van Westendorp)

<!-- Van Westendorp Price Sensitivity Meter: 4-question survey. Identifies acceptable price range. -->
<!-- Questions: (1) Too cheap / quality concern, (2) Cheap / good value, (3) Expensive but would pay, (4) Too expensive / won't pay. -->
<!-- Points of intersection: PMC (Point of Marginal Cheapness), PME (Point of Marginal Expensiveness), IDP (Ideal Price Point), OWP (Optimal/Acceptable Range). -->

**Survey Results (n = {N} respondents):**

| Price Point | Van Westendorp Response |
|------------|------------------------|
| ${X} | Too cheap (n = {%}) |
| ${X} | Cheap/good value — Point of Marginal Cheapness (PMC) |
| ${X} | **Ideal Price Point (IDP)** — most common "acceptable" |
| ${X} | Expensive but would pay — Point of Marginal Expensiveness (PME) |
| ${X} | Too expensive — Ceiling |

**Acceptable Price Range:** ${PMC} to ${PME}
**Recommended Price Point:** ${X} (positioned {above/below/at} IDP because: {rationale})

---

## 8. Risk Assessment

| Risk | Likelihood | Impact | Mitigation | Residual Risk |
|------|-----------|--------|-----------|--------------|
| {risk} | HIGH/MED/LOW | HIGH/MED/LOW | {mitigation action} | HIGH/MED/LOW |

**Downside Scenario:**
> If {most impactful risk} materializes, the investment returns {negative NPV / break-even / reduced IRR}. At this point, the decision should be: {continue / pivot / exit criteria}.

---

## 9. Investment Decision

| Field | Value |
|-------|-------|
| **Recommendation** | INVEST / DO NOT INVEST / INVEST WITH CONDITIONS |
| **Confidence** | {0.0–1.0} |
| **Conditions for Investment** | {List required conditions, e.g., "Validate LTV:CAC with pilot cohort"} |
| **Review Checkpoint** | {Date or milestone when decision should be revisited} |
| **Exit Criteria** | {Conditions under which investment should be stopped} |

---

## Example: SaaS Observability Platform Business Case (Discovery Mode)

> The following is a brief example showing what a filled-in discovery-mode business case looks like for a hypothetical SaaS product.

```
## 1. Executive Summary

Decision Required: Invest $2.4M over 12 months to build and launch a
cloud-native observability platform targeting mid-market SRE teams.

Investment Ask:
- Engineering: $1.8M (12 engineers x 12 months)
- Marketing/Sales: $400K (launch + demand gen)
- Infrastructure: $200K (cloud + tooling)
- Total: $2.4M over 12 months

Expected Return (order of magnitude):
- ARR impact: $1.5M–$3M by month 18
- Payback period: 14–18 months
- NPV (3-year): $2.1M at 12% discount rate

Recommendation: INVEST WITH CONDITIONS
Key Conditions: Validate pricing with 50-customer beta; achieve 5% conversion on landing page.

## 2. Lean Canvas

| Box                    | Content                                                    |
|------------------------|------------------------------------------------------------|
| 1. Problem             | (1) MTTR too high, (2) tool sprawl, (3) alert fatigue     |
| 2. Customer Segments   | SRE teams at 200-2000 emp SaaS companies                  |
| 3. UVP                 | "Correlate logs, metrics, traces in one view. 5-min MTTR." |
| 4. Solution            | (1) Unified telemetry, (2) auto-correlation, (3) runbooks |
| 5. Channels            | Product-led (free tier) + outbound sales for Enterprise    |
| 6. Revenue Streams     | Usage-based: $9/host/month + $0.50/GB ingested            |
| 7. Cost Structure      | 60% R&D, 25% S&M, 15% G&A                                |
| 8. Key Metrics         | North star: median MTTR. Supporting: DAU, NRR, expansion   |
| 9. Unfair Advantage    | Patent-pending correlation engine; ex-Datadog founding team |

## 4. Financial Projections (Order of Magnitude)

| Metric             | Year 1      | Year 2      | Year 3      | Key Assumption          |
|--------------------|-------------|-------------|-------------|-------------------------|
| New ARR            | $0.8–1.2M   | $2.0–3.5M   | $4.0–6.0M   | 15% monthly lead growth |
| Total ARR          | $0.8–1.2M   | $2.8–4.7M   | $6.8–10.7M  | 90% GRR, 110% NRR      |
| Gross Margin       | 65–70%      | 70–75%      | 75–80%      | Scale economics on infra |
| Investment Required | $2.4M       | $1.8M       | $1.2M       | Team ramp, then sustain |

Bear Case: 50% of base ARR targets if PLG conversion underperforms (3% vs 5%).
Bull Case: 150% if enterprise channel closes 2 marquee logos in Q2.
```
