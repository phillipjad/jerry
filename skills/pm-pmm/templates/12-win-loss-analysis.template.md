---
id: PM-CA-NNN
type: win-loss-analysis
agent: pm-competitive-analyst
status: draft
mode: discovery
risk_domain: business-viability-risk
created: YYYY-MM-DD
last_validated: YYYY-MM-DD
version: 0.1.0
frameworks_applied:
  - Win/Loss Methodology
cross_refs: []
---

<!-- AGENT GUIDANCE (pm-competitive-analyst):
  DISCOVERY MODE: Sections 1–3. Pattern summary from available deal data. Target 1–2 pages.
  DELIVERY MODE: All sections. Full cohort analysis, interview-based insights, trend analysis.
  Framework trace:
    Win/Loss Methodology: Structured analysis of closed deals to identify patterns, not individual deal explanations.
    Key principle: Individual deal post-mortems are anecdotes. Win/Loss analysis finds the PATTERN across deals.
    Cohort analysis: Segment wins and losses by segment, deal size, product line, and competitive scenario.
    Primary data: Third-party interviews with buyers who chose us AND buyers who chose competitors (interviewer ≠ sales rep).
  Staleness: 45-day window. Deal patterns reflect current market; older data misleads.
  Anti-pattern: Win/Loss reports that only interview lost deals are half the picture. Must analyze wins AND losses.
  Cross-reference: Feeds battle-card.md (update battle cards after each quarterly Win/Loss review).
-->

# Win/Loss Analysis: {Product / Segment / Period}

> **Status:** DRAFT — Discovery mode.
> **ID:** PM-CA-NNN
> **Agent:** pm-competitive-analyst
> **Risk Domain:** Business Viability Risk — why do we win and lose deals?
> **Mode:** DISCOVERY
> **Analysis Period:** {YYYY-MM-DD} to {YYYY-MM-DD}
> **Deals Analyzed:** {N} wins, {N} losses, {N} no decisions

---

## Document Sections

| Section | Purpose | Mode |
|---------|---------|------|
| [1. Win/Loss Summary](#1-winloss-summary) | Aggregate deal outcome metrics | Both |
| [2. Win Patterns](#2-win-patterns) | Why we win | Both |
| [3. Loss Patterns](#3-loss-patterns) | Why we lose | Both |
| [4. Cohort Analysis](#4-cohort-analysis) | Outcomes by segment, size, competitor | Delivery |
| [5. Buyer Interview Insights](#5-buyer-interview-insights) | First-person buyer evidence | Delivery |
| [6. Trend Analysis](#6-trend-analysis) | How patterns are changing over time | Delivery |
| [7. Action Recommendations](#7-action-recommendations) | What to change in product, sales, and marketing | Delivery |

---

## 1. Win/Loss Summary

<!-- AGENT DISCOVERY: Aggregate rates and top-line findings. -->

### Deal Outcome Metrics

| Metric | This Period | Prior Period | Change |
|--------|------------|-------------|--------|
| Total deals evaluated | {N} | {N} | {+/-N} |
| Win rate (overall) | {X}% | {X}% | {delta} |
| Loss rate | {X}% | {X}% | {delta} |
| No decision / lost to status quo | {X}% | {X}% | {delta} |

### Win Rate by Competitive Scenario

| Scenario | Win Rate | Deal Count |
|---------|---------|-----------|
| Head-to-head vs. {Competitor A} | {X}% | {N} |
| Head-to-head vs. {Competitor B} | {X}% | {N} |
| Evaluated alongside multiple competitors | {X}% | {N} |
| Sole vendor evaluated | {X}% | {N} |
| Replacing existing solution (displacement) | {X}% | {N} |

**Win Rate Trend:**
> Win rate is {improving / declining / stable} MoM. {One sentence explanation of trend driver.}

---

## 2. Win Patterns

<!-- Win/Loss Methodology: Wins tell you what to double down on. -->
<!-- AGENT: Patterns, not individual deals. How many wins cite this factor? -->

### Top Win Factors

| # | Win Factor | % Wins Citing This | Evidence Type |
|---|-----------|-------------------|--------------|
| W-01 | {what caused us to win} | {X}% | Buyer interview / Deal notes / Survey |
| W-02 | {win factor} | {X}% | {evidence type} |
| W-03 | {win factor} | {X}% | {evidence type} |

**Anatomy of a Typical Win:**

> {Describe in 2–3 sentences the typical profile of a deal we win. What segment? What competitive situation? What tipped it?}

**Champion Profile (Who Drives Our Wins):**
> Internal champion: {title / role}
> Key buying signal: {what they say that predicts a win}
> Deal velocity: {average days from discovery to close on wins}

---

## 3. Loss Patterns

<!-- Win/Loss Methodology: Losses tell you what to fix. Face them honestly. -->

### Top Loss Factors

| # | Loss Factor | % Losses Citing This | Actionable? |
|---|------------|---------------------|-------------|
| L-01 | {what caused us to lose} | {X}% | Yes (product gap) / Yes (sales execution) / Partially / No (price/segment) |
| L-02 | {loss factor} | {X}% | {actionable?} |
| L-03 | {loss factor} | {X}% | {actionable?} |

**Anatomy of a Typical Loss:**

> {Describe the typical profile of a deal we lose. What went wrong? Was it product, sales, pricing, or wrong segment?}

**Lost to Status Quo:**
> {X}% of deals are lost to "no decision" or "keep doing it manually." This means:
> {Interpretation: Is our category too early? Is the pain insufficient? Is our sales motion creating too much friction?}

### Loss Classification

| Loss Type | % of Losses | Definition |
|-----------|------------|-----------|
| Lost to competitor (feature) | {X}% | Competitor had a capability we lacked |
| Lost to competitor (price) | {X}% | Competitor offered lower price |
| Lost to competitor (relationship) | {X}% | Incumbent advantage or existing relationship |
| Lost to status quo | {X}% | Prospect chose to do nothing |
| Lost to wrong segment | {X}% | We were wrong prospect type for our ICP |
| Lost to sales execution | {X}% | We had the right product but failed in the sale |

---

<!-- DELIVERY MODE SECTIONS -->

## 4. Cohort Analysis

<!-- AGENT DELIVERY: Segment win rates to find where we're strongest and weakest. -->

### Win Rate by Customer Segment

| Segment | Win Rate | Deal Count | Trend | Recommended Action |
|---------|---------|-----------|-------|--------------------|
| {Segment 1: e.g., SMB} | {X}% | {N} | ↑/→/↓ | {action} |
| {Segment 2: e.g., Mid-Market} | {X}% | {N} | ↑/→/↓ | {action} |
| {Segment 3: e.g., Enterprise} | {X}% | {N} | ↑/→/↓ | {action} |

### Win Rate by Deal Size

| ACV Range | Win Rate | Deal Count | Key Driver |
|-----------|---------|-----------|-----------|
| < ${X}K | {X}% | {N} | {what drives win/loss at this size} |
| ${X}K – ${X}K | {X}% | {N} | {driver} |
| > ${X}K | {X}% | {N} | {driver} |

### Win Rate by Use Case

| Use Case | Win Rate | Notes |
|---------|---------|-------|
| {use case 1} | {X}% | {why we win or lose here} |
| {use case 2} | {X}% | {notes} |

---

## 5. Buyer Interview Insights

<!-- Win/Loss Methodology: Interviews with actual buyers = highest quality data. Must be done by neutral third party or non-sales researcher. -->
<!-- AGENT DELIVERY: Synthesize interview evidence. Preserve voice — use actual buyer quotes. -->

**Interviews Conducted:** {N} wins, {N} losses, {N} no decisions
**Interviewer:** {Name / role — must be non-sales to avoid bias}

### Buyers Who Chose Us (Wins)

**Themes from buyer interviews:**
> {Theme 1}: "{Quote}" — {buyer role, company size, segment}
> {Theme 2}: "{Quote}" — {buyer role, company size, segment}

**Decision Criteria Ranked by Winners:**
| Rank | Criterion | % Citing as Primary | Avg. Score (Us vs. Competitor) |
|------|-----------|--------------------|---------------------------------|
| 1 | {criterion} | {X}% | {our score / competitor score} |
| 2 | {criterion} | {X}% | {scores} |

### Buyers Who Chose Competitors (Losses)

**Themes from buyer interviews:**
> {Theme 1}: "{Quote}" — {buyer role, company size, segment}
> {Theme 2}: "{Quote}" — {buyer role, company size, segment}

**Decision Criteria Ranked by Losers:**
| Rank | Criterion | % Citing as Primary | Why We Fell Short |
|------|-----------|--------------------|--------------------|
| 1 | {criterion} | {X}% | {specific gap that drove the loss} |
| 2 | {criterion} | {X}% | {gap} |

---

## 6. Trend Analysis

<!-- AGENT DELIVERY: How are win/loss patterns changing? Trends are actionable; snapshots are historical. -->

| Metric | 6 Months Ago | 3 Months Ago | This Period | Trend | Implication |
|--------|-------------|-------------|------------|-------|-------------|
| Win rate vs. {Competitor A} | {X}% | {X}% | {X}% | ↑/→/↓ | {what's changing and why} |
| Average deal cycle (wins) | {N} days | {N} days | {N} days | ↑/→/↓ | {implication} |
| Price sensitivity in losses | {X}% | {X}% | {X}% | ↑/→/↓ | {implication} |

**Emerging Pattern:**
> {The most significant trend this period that needs immediate attention.}

---

## 7. Action Recommendations

| Finding | Recommended Action | Owner | Priority | Expected Impact |
|---------|-------------------|-------|---------|-----------------|
| {loss pattern L-01} | {specific action — product / sales / marketing} | {product / enablement / PMM} | P0/P1/P2 | {expected win rate improvement} |
| {win pattern W-01} | {double down action} | {owner} | {priority} | {impact} |

**Quarterly Priorities:**
1. {Highest-impact action} — {owner} — Target: {metric improvement}
2. {Second priority}
3. {Third priority}

**Battle Card Update Required:**
> Based on this analysis, the following battle cards need updating:
> - vs. {Competitor A}: Update Section {N} — {what changed}
