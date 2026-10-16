---
id: PM-CI-NNN
type: voc-report
agent: pm-customer-insight
status: draft
mode: discovery
risk_domain: value-risk
created: YYYY-MM-DD
last_validated: YYYY-MM-DD
version: 0.1.0
frameworks_applied:
  - Continuous Discovery
  - NPS/CSAT/CES
cross_refs: []
---

<!-- AGENT GUIDANCE (pm-customer-insight):
  DISCOVERY MODE: Sections 1–4. Summary of available signal sources. Identify top 3 themes. Target 1–2 pages.
  DELIVERY MODE: All sections. Full quantitative analysis + qualitative synthesis. Continuous Discovery loop closure.
  Continuous Discovery (Teresa Torres): Weekly customer touchpoints feeding an opportunity solution tree (OST).
     Signal sources: interviews, surveys, usage analytics, support tickets, social listening.
     OST structure: Desired outcomes → Opportunities → Solutions → Experiments.
  NPS: Net Promoter Score = % Promoters - % Detractors. Benchmark by category.
  CSAT: Customer Satisfaction Score. Transactional — tied to specific interactions.
  CES: Customer Effort Score. Predictive of churn. Lower effort = higher loyalty.
  Staleness: 60-day window (not standard 90-day). Customer sentiment shifts with product releases.
-->

# Voice of Customer Report: {Product/Feature Name} — {Time Period}

> **Status:** DRAFT — Discovery mode.
> **ID:** PM-CI-NNN
> **Agent:** pm-customer-insight
> **Risk Domain:** Value Risk — what are customers actually telling us?
> **Mode:** DISCOVERY
> **Report Period:** {YYYY-MM-DD} to {YYYY-MM-DD}

---

## Document Sections

| Section | Purpose | Mode |
|---------|---------|------|
| [1. Signal Sources](#1-signal-sources) | What data feeds this report | Both |
| [2. Quantitative Metrics](#2-quantitative-metrics) | NPS, CSAT, CES scores | Both |
| [3. Top Themes](#3-top-themes) | Synthesized customer feedback themes | Both |
| [4. Opportunity Summary](#4-opportunity-summary) | Actionable signal | Both |
| [5. Qualitative Deep Dive](#5-qualitative-deep-dive) | Interview and open-text synthesis | Delivery |
| [6. Opportunity Solution Tree](#6-opportunity-solution-tree) | Continuous Discovery OST | Delivery |
| [7. Experiment Log](#7-experiment-log) | What was tested based on prior VOC | Delivery |
| [8. Segment Breakdown](#8-segment-breakdown) | VOC differences across customer segments | Delivery |

---

## 1. Signal Sources

<!-- Continuous Discovery: Multiple signal sources prevent any single source from dominating the picture. -->
<!-- AGENT: List all available data sources for this report period. Mark gaps clearly. -->

| Source | Volume | Period | Quality | Coverage Gap? |
|--------|--------|--------|---------|---------------|
| Customer interviews | {N} interviews | {date range} | PRIMARY | {gap if any} |
| NPS survey | {N} responses | {date range} | HIGH | {gap if any} |
| CSAT survey | {N} responses | {date range} | HIGH | {gap if any} |
| CES survey | {N} responses | {date range} | HIGH | {gap if any} |
| Support tickets | {N} tickets | {date range} | MEDIUM | {gap if any} |
| Usage analytics | {N} users | {date range} | HIGH | {gap if any} |
| Social/review listening | {N} mentions | {date range} | LOW-MEDIUM | {gap if any} |

**Coverage Assessment:**
- Total customers represented: {N}
- % of total customer base: {X%}
- Segments with insufficient coverage: {list or "none"}

---

## 2. Quantitative Metrics

<!-- NPS/CSAT/CES: Track trends over time. Single-period snapshots mislead. -->

### Net Promoter Score (NPS)

| Metric | Current Period | Prior Period | Change | Industry Benchmark |
|--------|--------------|-------------|--------|-------------------|
| NPS | {-100 to +100} | {prior} | {+/- delta} | {benchmark} |
| % Promoters (9–10) | {%} | {%} | {delta} | — |
| % Passives (7–8) | {%} | {%} | {delta} | — |
| % Detractors (0–6) | {%} | {%} | {delta} | — |
| Response rate | {%} | {%} | {delta} | — |

**NPS Benchmark Context:**
> {NPS > 50 = excellent; 30–50 = good; 0–30 = needs work; < 0 = critical. Industry-specific benchmarks apply.}

### Customer Satisfaction Score (CSAT)

| Touchpoint | CSAT Score | Response Rate | Trend |
|-----------|-----------|--------------|-------|
| {touchpoint} | {1–5 or % satisfied} | {%} | ↑ / → / ↓ |

### Customer Effort Score (CES)

<!-- CES: "The product made it easy for me to handle my issue." 1=strongly disagree, 7=strongly agree. -->
<!-- CES > 5.0 is generally good. CES correlates more strongly with churn than NPS or CSAT. -->

| Interaction | CES Score | Trend | Churn Risk |
|------------|-----------|-------|-----------|
| {interaction type} | {1–7} | ↑ / → / ↓ | LOW / MEDIUM / HIGH |

---

## 3. Top Themes

<!-- Continuous Discovery: Theme synthesis converts raw signal into opportunities. -->
<!-- AGENT DISCOVERY: Identify top 3 themes. DELIVERY: Full theme taxonomy with evidence. -->

| # | Theme | Evidence Count | Signal Types | Customer Impact | Priority |
|---|-------|---------------|-------------|-----------------|---------|
| T-01 | {theme name and description} | {N} | Interviews / Surveys / Tickets / Analytics | HIGH/MED/LOW | P0/P1/P2 |
| T-02 | {theme} | {N} | {types} | {impact} | P0/P1/P2 |
| T-03 | {theme} | {N} | {types} | {impact} | P0/P1/P2 |

**Theme Confidence Levels:**
- HIGH: Confirmed in >= 3 signal sources OR by >= 30% of survey respondents
- MEDIUM: Confirmed in 1–2 signal sources OR 10–29% of respondents
- LOW: Mentioned in < 10% of signal or single source only

---

## 4. Opportunity Summary

<!-- AGENT: Translate themes into actionable opportunities. -->

**Headline Finding:**
> {One sentence: the most important thing customers are telling us right now.}

**Top 3 Opportunities:**

| # | Opportunity | Theme | Size (# customers) | Urgency | Recommended Action |
|---|------------|-------|---------------------|---------|-------------------|
| O-01 | {opportunity statement} | T-{XX} | {N customers} | HIGH/MED/LOW | {specific next action} |
| O-02 | {opportunity} | T-{XX} | {N} | {urgency} | {action} |
| O-03 | {opportunity} | T-{XX} | {N} | {urgency} | {action} |

**Risks Surfaced by VOC:**
> {Customer-reported risks to product success, churn signals, or competitive threats mentioned in feedback.}

---

<!-- DELIVERY MODE SECTIONS -->

## 5. Qualitative Deep Dive

<!-- AGENT DELIVERY: Synthesize interview and open-text data. Preserve voice — use actual quotes. -->

### Key Customer Quotes (by theme)

**Theme T-01: {Theme Name}**
> "{Quote 1}" — {customer segment / role}
> "{Quote 2}" — {customer segment / role}

**Theme T-02: {Theme Name}**
> "{Quote 1}" — {customer segment / role}

### Surprising or Counterintuitive Findings

> {What did customers tell you that contradicted internal assumptions? This section is often the most valuable.}

| Assumption | Customer Reality | Source |
|-----------|----------------|--------|
| We assumed {X} | Customers actually {Y} | {interview / survey source} |

---

## 6. Opportunity Solution Tree

<!-- Continuous Discovery (Teresa Torres): Opportunity Solution Tree links outcomes to opportunities to solutions to experiments. -->
<!-- AGENT DELIVERY: Build the OST from the top theme(s). -->

```
DESIRED OUTCOME
└── {North Star Metric or specific outcome goal}
    │
    ├── OPPORTUNITY: {opportunity from theme T-01}
    │   ├── Solution A: {potential solution}
    │   │   └── Experiment: {test to validate Solution A}
    │   └── Solution B: {potential solution}
    │       └── Experiment: {test to validate Solution B}
    │
    └── OPPORTUNITY: {opportunity from theme T-02}
        └── Solution C: {potential solution}
            └── Experiment: {test to validate Solution C}
```

**OST Prioritization:**
> The highest-opportunity node is {opportunity name} because {it affects N customers / has highest impact on North Star / is most underserved per ODI scores}.

---

## 7. Experiment Log

<!-- Continuous Discovery: Track what was tested based on prior VOC to close the learning loop. -->

| Experiment | Hypothesis | Start Date | Result | Learning |
|-----------|-----------|-----------|--------|---------|
| {experiment name} | If we {do X}, then {Y} will happen because {Z} | {date} | {outcome} | {what we learned} |

---

## 8. Segment Breakdown

<!-- AGENT DELIVERY: VOC often varies significantly by segment. Surface these differences. -->

| Segment | NPS | Top Theme | Unique Concern | Churn Risk |
|---------|-----|-----------|----------------|-----------|
| {segment 1} | {score} | {theme} | {segment-specific concern} | LOW/MED/HIGH |
| {segment 2} | {score} | {theme} | {concern} | {risk} |

**Segment Divergence:**
> {Note any cases where different segments want contradictory things. These divergences drive segmentation decisions.}
