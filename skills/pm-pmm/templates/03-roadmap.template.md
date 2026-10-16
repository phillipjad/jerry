---
id: PM-PS-NNN
type: product-roadmap
agent: pm-product-strategist
status: draft
mode: discovery
risk_domain: value-risk
created: YYYY-MM-DD
last_validated: YYYY-MM-DD
version: 0.1.0
frameworks_applied:
  - Product Kata
  - Story Mapping
cross_refs: []
---

<!-- AGENT GUIDANCE (pm-product-strategist):
  DISCOVERY MODE: Complete sections 1–3. Theme-level roadmap only. No dates. Target 1–2 pages.
  DELIVERY MODE: Complete all sections. Apply Product Kata framing (current state → target condition → next step).
  Story Mapping: Backbone (user activities) + walking skeleton (minimum viable journey) per Jeff Patton.
  Product Kata: From Improvement Kata — target condition, current condition, obstacles, next step (experiment).
  Do NOT list features. List outcomes and themes. Features belong in the PRD (PM-PS-NNN).
  Cross-reference: This roadmap SHOULD reference the product-vision-strategy.md (PM-PS-NNN) that motivates it.
-->

# Product Roadmap: {Product Name}

> **Status:** DRAFT — Discovery mode. Not for executive presentation.
> **ID:** PM-PS-NNN
> **Agent:** pm-product-strategist
> **Risk Domain:** Value Risk — are we building toward the right outcomes?
> **Mode:** DISCOVERY

---

## Document Sections

| Section | Purpose | Mode |
|---------|---------|------|
| [1. Roadmap Context (Product Kata)](#1-roadmap-context-product-kata) | Current state, target condition, obstacles | Both |
| [2. Outcome Themes](#2-outcome-themes) | Now / Next / Later thematic areas | Both |
| [3. Story Map Backbone](#3-story-map-backbone) | User activities driving the roadmap | Both |
| [4. Walking Skeleton](#4-walking-skeleton) | Minimum viable journey | Delivery |
| [5. Milestone Grid](#5-milestone-grid) | Delivery timeline with outcome targets | Delivery |
| [6. Roadmap Assumptions](#6-roadmap-assumptions) | Dependencies and bets | Delivery |
| [7. Roadmap Governance](#7-roadmap-governance) | How the roadmap is updated | Delivery |

---

## 1. Roadmap Context (Product Kata)

<!-- Product Kata (Melissa Perri, from Toyota Improvement Kata): Frames the roadmap as a series of experiments toward a target condition. -->
<!-- AGENT: Do NOT list features here. Describe the gap between current state and target condition. -->

### Target Condition (12-month horizon)

> What does the product experience look like for customers in 12 months?
> {Describe the target state in terms of customer behavior and outcomes, not features.}

**Target metrics:**
- {North Star Metric}: from {current value} to {target value}
- {Secondary Metric}: from {current value} to {target value}

### Current Condition

> What is the product's actual state today?
> {Describe current customer experience — where it succeeds and falls short of target condition.}

**Current metrics:**
- {North Star Metric}: {current value}
- {Secondary Metric}: {current value}

### Obstacle Register

<!-- Product Kata: Name the obstacles standing between current and target conditions. Obstacles drive the next steps. -->

| # | Obstacle | Impact on Reaching Target | Addressable? |
|---|---------|--------------------------|-------------|
| O-01 | {obstacle description} | {how it blocks target condition} | Yes / No / Partially |
| O-02 | {obstacle description} | {how it blocks target condition} | Yes / No / Partially |

### Next Step (Current Experiment)

> What is the very next thing we will try, and what do we expect to learn?
> {Describe the current sprint or quarter's focus as an experiment.}

**Experiment:** {experiment description}
**Expected result:** {what we predict will happen}
**Learning threshold:** {minimum result that validates we're on track}

---

## 2. Outcome Themes

<!-- AGENT: Group roadmap work by outcome themes, not features. Themes map to Obstacles from Product Kata. -->
<!-- Now = committed; Next = likely; Later = options. Avoid date commitments in discovery mode. -->

### Now (Current Quarter)

| Theme | Obstacle Addressed | Success Metric | Status |
|-------|-------------------|----------------|--------|
| {theme name} | O-{XX} | {metric and target} | In Progress / Planned |

### Next (Next Quarter)

| Theme | Obstacle Addressed | Success Metric | Confidence |
|-------|-------------------|----------------|-----------|
| {theme name} | O-{XX} | {metric and target} | High / Medium / Low |

### Later (6–12 Months)

| Theme | Strategic Bet | Conditions Required | Review Trigger |
|-------|--------------|---------------------|----------------|
| {theme name} | {from vision strategy} | {what must be true before committing} | {event that triggers review} |

---

## 3. Story Map Backbone

<!-- Story Mapping (Jeff Patton): Backbone = user activities (verb phrases) in left-to-right narrative flow. -->
<!-- AGENT: The backbone shows the user's journey, NOT the product's features. One row of user activities. -->
<!-- AGENT DISCOVERY: Backbone activities only. DELIVERY: Full story map including body and walking skeleton. -->

### User Narrative Sequence

> {Describe the user's journey in one sentence: "A user {starts here}, then {activity 2}, then {activity 3}, ultimately achieving {goal}."}

**Backbone Activities (left to right = user time sequence):**

| Step | User Activity | User Goal | Current Experience | Target Experience |
|------|--------------|-----------|-------------------|------------------|
| 1 | {verb phrase, e.g., "Discover product"} | {user's goal at this step} | {today} | {desired} |
| 2 | {verb phrase, e.g., "Configure account"} | {user's goal at this step} | {today} | {desired} |
| 3 | {verb phrase} | {user's goal at this step} | {today} | {desired} |
| 4 | {verb phrase} | {user's goal at this step} | {today} | {desired} |

---

<!-- DELIVERY MODE SECTIONS -->

## 4. Walking Skeleton

<!-- Story Mapping: Walking skeleton = the minimum set of stories that delivers a complete (if thin) user journey. -->
<!-- AGENT DELIVERY: For each backbone activity, identify the minimum viable story that makes the full journey possible. -->

| Backbone Activity | Walking Skeleton Story | Outcome Enabled | RICE Score |
|------------------|----------------------|-----------------|-----------|
| {activity 1} | {minimum story — not the ideal, but the minimum viable} | {what outcome this unlocks} | {score} |
| {activity 2} | {minimum story} | {outcome} | {score} |

**Walking Skeleton Release:** The stories above, delivered together, enable {describe the thin but complete experience}.

---

## 5. Milestone Grid

<!-- AGENT DELIVERY: Milestone = outcome target, not feature delivery. Tied to Product Kata target conditions. -->

| Milestone | Target Date | Outcome Target | Leading Metric | Go/No-Go Gate |
|-----------|------------|----------------|---------------|---------------|
| M-01: {milestone name} | {YYYY-QN} | {outcome in customer terms} | {leading metric and target} | {decision criteria} |
| M-02: {milestone name} | {YYYY-QN} | {outcome} | {metric} | {criteria} |

**Milestone Dependencies:**
- M-02 requires M-01 because: {dependency rationale}

---

## 6. Roadmap Assumptions

| # | Assumption | Type | If Wrong: Impact | Validation Method |
|---|-----------|------|-----------------|-------------------|
| A-01 | {assumption} | Customer / Technology / Business | HIGH / MEDIUM / LOW | {how to validate before committing to milestone} |
| A-02 | {assumption} | Customer / Technology / Business | HIGH / MEDIUM / LOW | {validation method} |

---

## 7. Roadmap Governance

| Review Type | Frequency | Trigger for Change | Decision Authority |
|-------------|-----------|-------------------|-------------------|
| Theme review | Weekly | Obstacle eliminated or new obstacle discovered | Product Manager |
| Milestone review | Monthly | Metric target missed or exceeded significantly | Product + Engineering |
| Full roadmap reset | Quarterly | Strategic bet invalidated | VP Product + stakeholders |

**What the roadmap is NOT:**
- A feature commitment list
- A date commitment to engineering
- A replacement for sprint planning
