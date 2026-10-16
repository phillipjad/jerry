---
id: PM-BA-NNN
type: market-sizing
agent: pm-business-analyst
status: draft
mode: discovery
risk_domain: business-viability-risk
created: YYYY-MM-DD
last_validated: YYYY-MM-DD
version: 0.1.0
frameworks_applied:
  - TAM/SAM/SOM
cross_refs: []
---

<!-- AGENT GUIDANCE (pm-business-analyst):
  DISCOVERY MODE: Sections 1–3. Top-down TAM/SAM/SOM with stated sources. Target 1–2 pages.
  DELIVERY MODE: All sections. Bottoms-up validation of top-down. Triangulated with multiple methods.
  Framework trace: TAM/SAM/SOM (industry standard):
    TAM = Total Addressable Market (everyone who could theoretically buy)
    SAM = Serviceable Addressable Market (segment we can reach with our go-to-market)
    SOM = Serviceable Obtainable Market (realistic capture in 3 years given competition and resources)
  Two sizing approaches:
    Top-Down: Start from industry total, apply penetration rates. Faster, less rigorous.
    Bottoms-Up: Build from individual customers × price × volume. More defensible.
  Always triangulate: Use both methods. If they diverge > 2x, investigate why.
  Cite sources. Unsourced market size claims are rejected.
-->

# Market Sizing: {Market / Segment Name}

> **Status:** DRAFT — Discovery mode. Top-down estimates only.
> **ID:** PM-BA-NNN
> **Agent:** pm-business-analyst
> **Risk Domain:** Business Viability Risk — is the market large enough to justify investment?
> **Mode:** DISCOVERY

---

## Document Sections

| Section | Purpose | Mode |
|---------|---------|------|
| [1. Market Definition](#1-market-definition) | What market is being sized | Both |
| [2. TAM/SAM/SOM Summary](#2-tamsamsom-summary) | Summary table with figures | Both |
| [3. Top-Down Sizing](#3-top-down-sizing) | Industry-to-segment approach | Both |
| [4. Bottoms-Up Sizing](#4-bottoms-up-sizing) | Customer-unit economics approach | Delivery |
| [5. Triangulation and Reconciliation](#5-triangulation-and-reconciliation) | Comparing methods and explaining gaps | Delivery |
| [6. Market Growth Analysis](#6-market-growth-analysis) | CAGR and growth drivers | Delivery |
| [7. Competitive Landscape Size Allocation](#7-competitive-landscape-size-allocation) | How the market is currently split | Delivery |

---

## 1. Market Definition

<!-- AGENT: Sloppy market definition leads to sloppy numbers. Define with precision before sizing. -->

**Market Name:** {Name the specific market being sized}

**Market Boundaries:**

| Dimension | In Scope | Out of Scope |
|-----------|----------|-------------|
| Product Category | {what product/service type} | {adjacent categories excluded} |
| Customer Type | {B2B / B2C / B2B2C; company size, sector} | {excluded customer types} |
| Geography | {regions/countries included} | {excluded regions} |
| Price Tier | {price range included} | {excluded tiers} |

**Market Definition Rationale:**
> {Explain why this specific boundary was chosen. What makes this the right unit of analysis?}

**Data Sources:**
| Source | Date | Used For |
|--------|------|---------|
| {analyst firm / report name} | {year} | {TAM / SAM / SOM / growth} |
| {source} | {year} | {usage} |

---

## 2. TAM/SAM/SOM Summary

| Level | Definition | Size | Growth Rate | Methodology |
|-------|-----------|------|------------|-------------|
| **TAM** | Total market if we had 100% market share of all possible buyers | ${X}B | {X}% CAGR | Top-down / Bottoms-up |
| **SAM** | Portion we can serve given our GTM, geography, and ICP | ${X}B | {X}% CAGR | Top-down |
| **SOM** | Realistic 3-year capture given competition and resource constraints | ${X}M | — | Bottoms-up |

**SOM Capture Timeline:**

| Year | SOM $ Captured | % of SAM | Basis |
|------|---------------|---------|-------|
| Year 1 | ${X}M | {X}% | {assumption: new logos at $X ACV} |
| Year 2 | ${X}M | {X}% | {assumption: retention + expansion} |
| Year 3 | ${X}M | {X}% | {assumption: market position established} |

---

## 3. Top-Down Sizing

<!-- Top-Down: Start from industry total, apply filters to reach SAM and SOM. -->
<!-- AGENT: Every number needs a source. Every penetration rate needs a rationale. -->

### TAM (Top-Down)

| Step | Calculation | Result | Source |
|------|------------|--------|--------|
| Industry total spend | {description} | ${X}B | {analyst report, year} |
| × Relevance filter | {% of spend on our category} | ${X}B | {rationale} |
| = **TAM** | | **${X}B** | |

### SAM (Top-Down)

| Step | Calculation | Result | Rationale |
|------|------------|--------|-----------|
| TAM | | ${X}B | |
| × Geography filter | {% of TAM in our target geos} | ${X}B | {why this geography coverage} |
| × Segment filter | {% matching our ICP} | ${X}B | {ICP definition basis} |
| × Price tier filter | {% in our price range} | ${X}B | {price tier rationale} |
| = **SAM** | | **${X}B** | |

### SOM (Top-Down Cross-Check)

| Step | Calculation | Result | Rationale |
|------|------------|--------|-----------|
| SAM | | ${X}B | |
| × Realistic penetration | {X}% in 3 years | ${X}M | {competitive context for this rate} |
| = **SOM (Top-Down)** | | **${X}M** | |

---

<!-- DELIVERY MODE SECTIONS -->

## 4. Bottoms-Up Sizing

<!-- Bottoms-Up: Build from units × price. More defensible; grounded in customer economics. -->
<!-- AGENT DELIVERY: Independent of top-down. Should broadly confirm or explain divergence. -->

### Customer Count Estimate

| Customer Type | Total Universe | Addressable % | Addressable Count | Basis |
|--------------|---------------|--------------|------------------|-------|
| {customer segment 1} | {N} companies/people | {X}% | {N} | {source or rationale} |
| {customer segment 2} | {N} | {X}% | {N} | {basis} |
| **Total Addressable Customers** | | | **{N}** | |

### Revenue Per Customer

| Segment | ACV (Annual Contract Value) | Assumptions |
|---------|---------------------------|------------|
| {segment 1} | ${X}/year | {seats × price, or flat rate basis} |
| {segment 2} | ${X}/year | {basis} |
| **Blended ACV** | **${X}/year** | {weighted average} |

### Bottoms-Up SAM and SOM

| Level | Calculation | Result |
|-------|------------|--------|
| SAM (Bottoms-Up) | {N} addressable customers × ${X} ACV | **${X}B** |
| Year 3 SOM (Bottoms-Up) | {N} wins at {X}% penetration × ${X} ACV | **${X}M** |

---

## 5. Triangulation and Reconciliation

<!-- AGENT DELIVERY: If top-down and bottoms-up diverge by > 2x, explain why. This is the most important analytical step. -->

| Method | SAM | SOM (Year 3) |
|--------|-----|-------------|
| Top-Down | ${X}B | ${X}M |
| Bottoms-Up | ${X}B | ${X}M |
| **Variance** | {X}% | {X}% |
| **Accepted Estimate** | **${X}B** | **${X}M** |

**Reconciliation Rationale:**
> {Explain the variance and which estimate is more reliable. Bottoms-up is typically the floor; top-down sets the ceiling. State which you use and why.}

---

## 6. Market Growth Analysis

| Driver | CAGR Impact | Source |
|--------|------------|--------|
| {growth driver 1} | {+/- X%} | {source} |
| {growth driver 2} | {+/- X%} | {source} |

**Market CAGR:** {X}% (sourced from {analyst firm, year})

**Tailwinds:**
- {market trend accelerating demand}
- {regulatory or technology driver}

**Headwinds:**
- {market force that could slow growth}

---

## 7. Competitive Landscape Size Allocation

<!-- AGENT DELIVERY: How is the current SAM divided among players? This sets realistic SOM expectations. -->

| Player | Estimated Market Share | ARR / Revenue | Share Basis |
|--------|----------------------|--------------|------------|
| {competitor 1} | {X}% | ${X}M | {public revenue / estimate from analyst / channel intel} |
| {competitor 2} | {X}% | ${X}M | {basis} |
| {our company} | {X}% | ${X}M | {current position} |
| Fragmented / Other | {X}% | ${X}M | {residual} |
| **Total SAM** | **100%** | **${X}B** | |

**Market Structure:**
> {Oligopoly / Fragmented / Emerging / Consolidating — describe market structure and implication for our SOM target}
