---
id: PM-PS-NNN
type: prd
agent: pm-product-strategist
status: draft
mode: discovery
risk_domain: value-risk
created: YYYY-MM-DD
last_validated: YYYY-MM-DD
version: 0.1.0
frameworks_applied:
  - RICE
  - JTBD
  - Kano
cross_refs: []
---

<!-- AGENT GUIDANCE (pm-product-strategist):
  DISCOVERY MODE: Complete sections 1–5 only. Target 1–2 pages. Use RICE for priority scoring.
  DELIVERY MODE: Complete all sections including 6–9. Apply full JTBD and Kano analysis.
  Framework trace: Every requirement row must cite JTBD job-to-be-done statement.
  Quality gate: delivery mode requires /adversary score >= 0.95 before status: final.
-->

# Product Requirements Document: {Product/Feature Name}

> **Status:** DRAFT — Discovery mode. Not for executive presentation.
> **ID:** PM-PS-NNN
> **Agent:** pm-product-strategist
> **Risk Domain:** Value Risk — does this solve the right problem?
> **Mode:** DISCOVERY

---

## Document Sections

| Section | Purpose | Mode |
|---------|---------|------|
| [1. Problem Statement](#1-problem-statement) | JTBD core job definition | Both |
| [2. Strategic Context](#2-strategic-context) | Why now, why us | Both |
| [3. User Stories (JTBD)](#3-user-stories-jtbd) | Job statements and outcomes | Both |
| [4. RICE Priority Scoring](#4-rice-priority-scoring) | Feature prioritization | Both |
| [5. Kano Classification](#5-kano-classification) | Feature type mapping | Both |
| [6. Detailed Requirements](#6-detailed-requirements) | Full requirement specs | Delivery |
| [7. Acceptance Criteria](#7-acceptance-criteria) | Testable conditions | Delivery |
| [8. Out of Scope](#8-out-of-scope) | Explicit exclusions | Delivery |
| [9. Open Questions](#9-open-questions) | Unresolved decisions | Delivery |

---

## 1. Problem Statement

<!-- JTBD Framework: Define the core functional, emotional, and social jobs users are trying to accomplish. -->
<!-- AGENT: State the job in the canonical JTBD format: "When [situation], I want to [motivation], so I can [expected outcome]." -->

**Core Functional Job:**
> When {situation}, users want to {motivation}, so they can {expected outcome}.

**Emotional Job:**
> {How users want to feel when accomplishing this job}

**Social Job:**
> {How users want to be perceived by others when accomplishing this job}

**Problem Magnitude:**
- Affected users: {estimate}
- Frequency: {daily / weekly / occasionally}
- Current workaround: {describe or "none"}
- Pain severity: {low / medium / high / critical}

---

## 2. Strategic Context

<!-- Playing to Win / North Star: Connect this PRD to the product's north star metric and strategic choices. -->
<!-- AGENT: This section validates Business Viability Risk — will this advance our strategic position? -->

**North Star Alignment:**
> How does this feature advance the product's north star metric?
> North Star Metric: {metric name and current value}
> Expected impact: {+X% improvement or qualitative advancement}

**Strategic Choice (Playing to Win):**
> Where to play: {market segment / customer segment this targets}
> How to win: {unique right to win this specific job-to-be-done}

**Success Metrics:**
| Metric | Baseline | Target | Measurement Method |
|--------|---------|--------|-------------------|
| {metric 1} | {value} | {value} | {method} |
| {metric 2} | {value} | {value} | {method} |

---

## 3. User Stories (JTBD)

<!-- JTBD Framework: Each user story derives from a specific job statement. -->
<!-- AGENT DISCOVERY: List 3–5 primary job statements. DELIVERY: Comprehensive list with outcome metrics. -->

### Primary Job Statements

| # | Job Statement | Outcome Metric | Priority |
|---|--------------|----------------|----------|
| J-01 | When {situation}, I want to {action} so I can {outcome} | {measurable metric} | P0/P1/P2 |
| J-02 | When {situation}, I want to {action} so I can {outcome} | {measurable metric} | P0/P1/P2 |
| J-03 | When {situation}, I want to {action} so I can {outcome} | {measurable metric} | P0/P1/P2 |

### Desired Outcomes (ODI — Outcome-Driven Innovation)

<!-- AGENT: For each job, list the desired outcomes users use to measure success. -->

| Job | Desired Outcome | Underserved (1–10) | Importance (1–10) |
|-----|-----------------|-------------------|--------------------|
| J-01 | {outcome statement} | {score} | {score} |

---

## 4. RICE Priority Scoring

<!-- RICE Framework: Reach × Impact × Confidence ÷ Effort -->
<!-- AGENT: Score each feature/initiative in this PRD. RICE score drives Section 6 ordering. -->

| Feature | Reach | Impact | Confidence | Effort | **RICE Score** | Priority Rank |
|---------|-------|--------|-----------|--------|----------------|---------------|
| {feature 1} | {users/quarter} | {0.25/0.5/1/2/3} | {0–100%} | {person-weeks} | **{R×I×C/E}** | P{N} |
| {feature 2} | {users/quarter} | {0.25/0.5/1/2/3} | {0–100%} | {person-weeks} | **{R×I×C/E}** | P{N} |

**RICE Scoring Guide:**
- Reach: estimated users reached per quarter
- Impact: 3=massive, 2=high, 1=medium, 0.5=low, 0.25=minimal
- Confidence: % confidence in reach and impact estimates
- Effort: total person-weeks across all functions

---

## 5. Kano Classification

<!-- Kano Model: Classify features by satisfaction impact (threshold, performance, excitement). -->
<!-- AGENT: Kano classification determines what must be included vs. what drives delight. -->

| Feature | Kano Category | Rationale |
|---------|--------------|-----------|
| {feature 1} | Threshold (Must-Have) | {why this is a baseline expectation} |
| {feature 2} | Performance (More = Better) | {why satisfaction scales linearly with quality} |
| {feature 3} | Excitement (Delighter) | {why users don't expect it but love it when present} |
| {feature 4} | Indifferent | {why users don't care either way} |

**Kano Categories:**
- **Threshold:** Must-have. Absence causes dissatisfaction; presence is expected.
- **Performance:** Satisfaction scales linearly with quality.
- **Excitement:** Unexpected features that create strong positive reactions.
- **Indifferent:** Users are neutral regardless of presence or absence.

---

<!-- DELIVERY MODE SECTIONS — Complete for delivery mode only -->

## 6. Detailed Requirements

<!-- AGENT DELIVERY: Full requirement specifications. Each requirement traces to a JTBD job statement (J-XX). -->

### Functional Requirements

| ID | Requirement | JTBD Trace | Priority | Acceptance Criteria |
|----|-------------|-----------|----------|---------------------|
| FR-01 | {requirement statement} | J-{XX} | P0/P1/P2 | {testable condition} |
| FR-02 | {requirement statement} | J-{XX} | P0/P1/P2 | {testable condition} |

### Non-Functional Requirements

| ID | Requirement | Category | Metric |
|----|-------------|---------|--------|
| NFR-01 | {requirement} | Performance / Security / Reliability / Scalability | {measurable metric} |

---

## 7. Acceptance Criteria

<!-- AGENT DELIVERY: BDD-style acceptance criteria per H-20. Each maps to a functional requirement. -->

**Format:** Given [context] / When [action] / Then [expected outcome]

| FR | Scenario | Given | When | Then |
|----|---------|-------|------|------|
| FR-01 | Happy path | {context} | {action} | {outcome} |
| FR-01 | Error case | {context} | {invalid action} | {error outcome} |

---

## 8. Out of Scope

<!-- AGENT DELIVERY: Explicit exclusions prevent scope creep. -->

The following are explicitly OUT OF SCOPE for this PRD:

| Item | Rationale | Future Consideration? |
|------|-----------|----------------------|
| {item 1} | {why excluded} | Yes / No / Future PRD |
| {item 2} | {why excluded} | Yes / No / Future PRD |

---

## 9. Open Questions

<!-- AGENT DELIVERY: Track unresolved decisions that could affect requirements. -->

| # | Question | Owner | Due Date | Impact if Unresolved |
|---|---------|-------|----------|----------------------|
| Q-01 | {question} | {owner} | {date} | {impact} |

---

## Example: SaaS Observability Platform PRD (Discovery Mode)

> The following is a brief example showing what a filled-in discovery-mode PRD looks like for a hypothetical SaaS product.

```
## 1. Problem Statement

Core Functional Job:
> When a site reliability engineer is responding to an incident at 3 AM,
> they want to correlate logs, metrics, and traces in a single view,
> so they can reduce MTTR from 45 minutes to under 5 minutes.

Emotional Job: Feel confident and in control during high-pressure incidents.
Social Job: Be seen by their team as the engineer who resolves issues fastest.

Problem Magnitude:
- Affected users: ~12,000 SREs at mid-market companies (200-2000 employees)
- Frequency: 3-5 incidents/week per team
- Current workaround: Tab-switching between Datadog, PagerDuty, and Kibana
- Pain severity: HIGH

## 4. RICE Priority Scoring

| Feature          | Reach  | Impact | Confidence | Effort  | RICE Score | Rank |
|------------------|--------|--------|------------|---------|------------|------|
| Unified view     | 12,000 | 3      | 80%        | 12 wks  | 2,400      | P0   |
| Auto-correlation | 8,000  | 2      | 60%        | 16 wks  | 600        | P1   |
| Runbook linking  | 5,000  | 1      | 70%        | 4 wks   | 875        | P1   |
```
