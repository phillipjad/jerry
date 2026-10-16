---
id: PM-CA-NNN
type: competitive-analysis
agent: pm-competitive-analyst
status: draft
mode: discovery
risk_domain: business-viability-risk
created: YYYY-MM-DD
last_validated: YYYY-MM-DD
version: 0.1.0
frameworks_applied:
  - Porter's Five Forces
  - SWOT
cross_refs: []
---

<!-- AGENT GUIDANCE (pm-competitive-analyst):
  DISCOVERY MODE: Sections 1–3. Landscape overview + SWOT. Target 1–2 pages.
  DELIVERY MODE: All sections. Full Porter's Five Forces + SWOT with evidence + strategic implications.
  Framework trace:
    Porter's Five Forces (Michael Porter, 1979): Competitive rivalry, threat of new entrants, threat of substitutes, bargaining power of suppliers, bargaining power of buyers.
    SWOT: Strengths, Weaknesses, Opportunities, Threats — matched to Porter forces for strategic response.
  Staleness: 60-day window. Competitive landscape changes with funding rounds, product launches, and pricing changes.
  Cross-reference: This analysis feeds battle-card.md and win-loss-analysis.md (cross_refs required in delivery mode).
  Intel sources: Use public sources only. No confidential competitive intelligence.
-->

# Competitive Analysis: {Market / Product Category}

> **Status:** DRAFT — Discovery mode.
> **ID:** PM-CA-NNN
> **Agent:** pm-competitive-analyst
> **Risk Domain:** Business Viability Risk — can we win in this market?
> **Mode:** DISCOVERY

---

## Document Sections

| Section | Purpose | Mode |
|---------|---------|------|
| [1. Competitive Landscape Overview](#1-competitive-landscape-overview) | Who the competitors are | Both |
| [2. SWOT Analysis](#2-swot-analysis) | Our position relative to market | Both |
| [3. Competitor Profiles](#3-competitor-profiles) | Quick-reference competitor snapshots | Both |
| [4. Porter's Five Forces](#4-porters-five-forces) | Structural market forces analysis | Delivery |
| [5. Competitive Positioning Map](#5-competitive-positioning-map) | Two-axis perceptual map | Delivery |
| [6. Differentiation Analysis](#6-differentiation-analysis) | Where we win and lose | Delivery |
| [7. Strategic Implications](#7-strategic-implications) | What this means for product and GTM | Delivery |

---

## 1. Competitive Landscape Overview

<!-- AGENT DISCOVERY: Categorize competitors by type. -->

**Market Category:** {Define the competitive category — what battle are we in?}

### Competitor Categories

| Category | Description | Key Players |
|----------|-------------|------------|
| Direct Competitors | Same product category, same customer segment, similar price | {list} |
| Indirect Competitors | Different product, same job-to-be-done | {list} |
| Substitute Solutions | Non-product alternatives (spreadsheets, manual processes, do nothing) | {list} |
| Potential Entrants | Well-resourced players who could enter this market | {list} |

**Competitive Intensity:**
> {Low / Medium / High — brief rationale}

---

## 2. SWOT Analysis

<!-- SWOT: Match internal factors (S/W) to external factors (O/T). Most useful when S/O and W/T strategies are paired. -->
<!-- AGENT DISCOVERY: Complete all four quadrants. DELIVERY: Add strategic response for each quadrant. -->

### Strengths (Internal Advantages)

| # | Strength | Evidence | Strategic Relevance |
|---|---------|---------|---------------------|
| S-01 | {strength description} | {how we know this is real} | {why it matters in this market} |
| S-02 | {strength} | {evidence} | {relevance} |

### Weaknesses (Internal Vulnerabilities)

| # | Weakness | Evidence | Risk Level |
|---|---------|---------|-----------|
| W-01 | {weakness description} | {evidence} | HIGH/MED/LOW |
| W-02 | {weakness} | {evidence} | {level} |

### Opportunities (External Tailwinds)

| # | Opportunity | Window | Capture Requirement |
|---|------------|--------|---------------------|
| O-01 | {opportunity} | {short/medium/long term} | {what we need to do to capture it} |
| O-02 | {opportunity} | {window} | {requirement} |

### Threats (External Risks)

| # | Threat | Likelihood | Impact | Mitigation |
|---|--------|-----------|--------|-----------|
| T-01 | {threat} | HIGH/MED/LOW | HIGH/MED/LOW | {mitigation strategy} |
| T-02 | {threat} | {likelihood} | {impact} | {mitigation} |

### SWOT Strategic Pairings

| Pairing | Strategy |
|---------|---------|
| S-O (Use strengths to capture opportunities) | {strategy} |
| W-O (Address weaknesses to enable opportunities) | {strategy} |
| S-T (Use strengths to mitigate threats) | {strategy} |
| W-T (Minimize weaknesses, avoid threats) | {strategy} |

---

## 3. Competitor Profiles

<!-- AGENT DISCOVERY: 3–5 key competitors. One row per competitor. DELIVERY: Expand to full profiles. -->

| Competitor | Category | Founding/Stage | Est. ARR | Core Strength | Core Weakness | Price Positioning |
|-----------|---------|---------------|---------|---------------|---------------|------------------|
| {competitor 1} | Direct | {year / Series X} | ${X}M | {strength} | {weakness} | {lower/similar/higher than us} |
| {competitor 2} | Direct | {stage} | ${X}M | {strength} | {weakness} | {positioning} |
| {competitor 3} | Indirect | {stage} | ${X}M | {strength} | {weakness} | {positioning} |

---

<!-- DELIVERY MODE SECTIONS -->

## 4. Porter's Five Forces

<!-- Porter's Five Forces (1979): Structural analysis of competitive intensity. Each force rates HIGH/MED/LOW and is evidence-based. -->
<!-- AGENT DELIVERY: Rate and evidence each force. High force = unfavorable market structure. -->

### Force 1: Competitive Rivalry

**Rating:** HIGH / MEDIUM / LOW

| Evidence | Supporting Data | Implication |
|---------|----------------|-------------|
| Number of competitors | {N} direct competitors | {more = higher rivalry} |
| Market growth rate | {X}% CAGR | {slow growth = higher rivalry} |
| Product differentiation | {low/medium/high} | {low = commodity pressure} |
| Exit barriers | {low/high} | {high barriers = competitors fight to stay} |

**Force Summary:** {2–3 sentences on competitive rivalry dynamics}

### Force 2: Threat of New Entrants

**Rating:** HIGH / MEDIUM / LOW

| Barrier to Entry | Strength | Evidence |
|-----------------|---------|---------|
| Capital requirements | HIGH/MED/LOW | {build cost, time to market} |
| Network effects | HIGH/MED/LOW | {whether existing players have network advantages} |
| Brand / switching costs | HIGH/MED/LOW | {evidence of lock-in} |
| Regulatory | HIGH/MED/LOW | {compliance requirements} |
| Incumbent advantages | HIGH/MED/LOW | {data, relationships, distribution} |

**Force Summary:** {Why the threat of new entrants is high/medium/low}

### Force 3: Threat of Substitutes

**Rating:** HIGH / MEDIUM / LOW

| Substitute | Adoption Indicator | Price/Performance vs. Us | Switch Cost |
|-----------|-------------------|--------------------------|------------|
| {substitute 1} | {usage data or signals} | {comparison} | LOW/MED/HIGH |
| {substitute 2} | {indicator} | {comparison} | {cost} |

**Force Summary:** {Substitute threat narrative}

### Force 4: Bargaining Power of Buyers

**Rating:** HIGH / MEDIUM / LOW

| Factor | Rating | Evidence |
|--------|--------|---------|
| Buyer concentration | HIGH/MED/LOW | {% of ARR in top N customers} |
| Switching cost for buyers | HIGH/MED/LOW | {integration depth, data portability} |
| Price sensitivity | HIGH/MED/LOW | {win/loss pricing signal, NPS on pricing} |
| Buyer information | HIGH/MED/LOW | {transparency of pricing, comparison sites} |

**Force Summary:** {Buyer power narrative}

### Force 5: Bargaining Power of Suppliers

**Rating:** HIGH / MEDIUM / LOW

| Supplier Category | Concentration | Switching Cost | Power Level |
|------------------|--------------|----------------|------------|
| Cloud infrastructure | LOW (3 major options) | MEDIUM | LOW |
| {other key supplier} | {concentration} | {cost} | {power} |

**Force Summary:** {Supplier power narrative}

### Five Forces Summary

| Force | Rating | Strategic Implication |
|-------|--------|-----------------------|
| Competitive Rivalry | H/M/L | {implication} |
| Threat of New Entrants | H/M/L | {implication} |
| Threat of Substitutes | H/M/L | {implication} |
| Buyer Power | H/M/L | {implication} |
| Supplier Power | H/M/L | {implication} |
| **Overall Market Attractiveness** | **H/M/L** | **{overall verdict}** |

---

## 5. Competitive Positioning Map

<!-- Perceptual Map: Two-axis map showing where competitors are positioned. Reveals white space. -->

**Axes Selection:**
> X-axis: {dimension 1 — choose a dimension that matters to buyers, e.g., "ease of use"}
> Y-axis: {dimension 2 — choose a second dimension, e.g., "feature depth"}

**Positioning:**

```
High {Y-axis}
        ^
        |  [Competitor A]          [Competitor B]
        |
        |              [US - TARGET POSITION]
        |
        |  [Competitor C]   [Competitor D]
        +--------------------------> High {X-axis}
Low {Y-axis}    Low {X-axis}
```

**White Space Identified:**
> {Describe any unoccupied positions in the map that represent an opportunity.}

---

## 6. Differentiation Analysis

| Capability | Us | Competitor A | Competitor B | Buyer Importance |
|-----------|-----|-------------|-------------|-----------------|
| {capability 1} | ✅ Strong | ⚠️ Partial | ❌ Absent | HIGH/MED/LOW |
| {capability 2} | ⚠️ Partial | ✅ Strong | ✅ Strong | HIGH/MED/LOW |

**Where We Win:**
> {2–3 sentences on our genuine differentiated advantages}

**Where We Lose:**
> {Be honest. Where do competitors outperform us? This drives the product roadmap.}

---

## 7. Strategic Implications

| Force / Finding | Recommended Response | Owner | Timeline |
|----------------|---------------------|-------|---------|
| {force or SWOT finding} | {specific strategic response} | {product / GTM / eng} | {horizon} |

**Top Priority:** {Single most important strategic action based on this analysis}

---

## Example: SaaS Observability Platform Competitive Analysis (Discovery Mode)

> The following is a brief example showing what a filled-in discovery-mode competitive analysis looks like for a hypothetical SaaS product.

```
## 1. Competitive Landscape Overview

Market Category: Cloud-native observability platforms for mid-market SRE teams

| Category           | Description                              | Key Players                    |
|--------------------|------------------------------------------|--------------------------------|
| Direct Competitors | Full-stack observability, same segment   | Datadog, New Relic, Grafana    |
| Indirect           | APM-only or log-only tools               | Splunk, Elastic, Honeycomb     |
| Substitutes        | DIY Prometheus + Grafana + ELK stack     | Open-source self-hosted        |
| Potential Entrants | Cloud providers expanding native tooling | AWS CloudWatch, Azure Monitor  |

Competitive Intensity: HIGH — 8+ funded competitors, consolidation ongoing.

## 2. SWOT Analysis (Summary)

Strengths: Single-pane correlation engine (no competitor unifies all 3 signals natively).
Weaknesses: No brand recognition; late entrant in a crowded market.
Opportunities: Mid-market underserved by Datadog pricing ($23/host/month vs. our $9).
Threats: Datadog could release a mid-market tier; Grafana Cloud gaining traction.

## 3. Competitor Profiles

| Competitor  | Category | Stage     | Est. ARR | Core Strength      | Core Weakness         | Price     |
|-------------|----------|-----------|----------|--------------------|-----------------------|-----------|
| Datadog     | Direct   | Public    | $2.1B    | Brand + breadth    | Expensive for <500 emp| Higher    |
| New Relic   | Direct   | Public    | $900M    | Free tier + usage  | Complex pricing       | Similar   |
| Grafana Labs| Direct   | Series D  | $250M    | OSS community      | Enterprise features   | Lower     |
```
