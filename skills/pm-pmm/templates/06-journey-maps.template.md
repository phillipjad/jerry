---
id: PM-CI-NNN
type: customer-journey-map
agent: pm-customer-insight
status: draft
mode: discovery
risk_domain: value-risk
created: YYYY-MM-DD
last_validated: YYYY-MM-DD
version: 0.1.0
frameworks_applied:
  - Moments of Truth
  - Service Blueprint
cross_refs: []
---

<!-- AGENT GUIDANCE (pm-customer-insight):
  DISCOVERY MODE: Sections 1–3. 3–5 stage journey. Identify the most critical moments of truth. Target 1–2 pages.
  DELIVERY MODE: All sections. Full stage analysis, emotional arc, touchpoint inventory, service blueprint layer.
  Moments of Truth (Jan Carlzon): Focus on the moments where customer perception of brand and product is formed.
     First Moment of Truth (FMOT): First encounter with product/brand.
     Second Moment of Truth (SMOT): Experience of using the product.
     Zero Moment of Truth (ZMOT): Pre-purchase research and social proof.
  Service Blueprint: Extends journey map "below the line" — shows frontstage (customer-visible) and backstage (internal) actions.
  Cross-reference: This map SHOULD reference the user-persona.md that anchors the journey.
-->

# Customer Journey Map: {Persona Name} — {Job/Scenario Name}

> **Status:** DRAFT — Discovery mode.
> **ID:** PM-CI-NNN
> **Agent:** pm-customer-insight
> **Risk Domain:** Value Risk — where does the customer experience succeed and fail?
> **Mode:** DISCOVERY

---

## Document Sections

| Section | Purpose | Mode |
|---------|---------|------|
| [1. Journey Context](#1-journey-context) | Persona, scenario, and scope | Both |
| [2. Journey Stages](#2-journey-stages) | Stage-by-stage experience map | Both |
| [3. Moments of Truth](#3-moments-of-truth) | Critical experience inflection points | Both |
| [4. Emotional Arc](#4-emotional-arc) | Sentiment curve across stages | Delivery |
| [5. Touchpoint Inventory](#5-touchpoint-inventory) | Every customer interaction catalogued | Delivery |
| [6. Service Blueprint Layer](#6-service-blueprint-layer) | Frontstage / backstage / support actions | Delivery |
| [7. Opportunity Map](#7-opportunity-map) | Prioritized improvement areas | Delivery |

---

## 1. Journey Context

| Field | Value |
|-------|-------|
| **Persona** | {Persona name} (see PM-CI-{NNN}) |
| **Journey Scenario** | {Describe the specific scenario being mapped — start and end states} |
| **Journey Trigger** | {What causes this persona to start this journey?} |
| **Journey End State** | {What does success look like at journey completion?} |
| **Journey Frequency** | {How often does this persona take this journey?} |
| **Scope** | {What is included and excluded from this journey map?} |

---

## 2. Journey Stages

<!-- AGENT DISCOVERY: Define 3–5 stages. Each stage is a meaningful phase of the customer's experience. -->
<!-- Stages are named from the CUSTOMER's perspective, not the company's process steps. -->

| Stage | Customer Goal | Actions | Touchpoints | Sentiment |
|-------|-------------|---------|-------------|-----------|
| {Stage 1 Name} | {what the customer is trying to accomplish} | {what they do} | {channels/systems they interact with} | 😊/😐/😟 |
| {Stage 2 Name} | {customer goal} | {actions} | {touchpoints} | 😊/😐/😟 |
| {Stage 3 Name} | {customer goal} | {actions} | {touchpoints} | 😊/😐/😟 |

**Sentiment Key:** 😊 Positive / 😐 Neutral / 😟 Frustrated

---

## 3. Moments of Truth

<!-- Moments of Truth (Jan Carlzon): The 15 seconds of customer interaction that form lasting impressions. -->
<!-- FMOT = first encounter with product/brand, SMOT = in-use experience, ZMOT = pre-purchase research. -->
<!-- AGENT DISCOVERY: Identify the 2–3 most critical moments. DELIVERY: Full inventory. -->

| Moment | Type | Stage | What Happens | Current Experience | Impact on Perception |
|--------|------|-------|-------------|-------------------|--------------------|
| {Moment name} | ZMOT / FMOT / SMOT | {Stage N} | {description} | {positive / neutral / negative + why} | {how this shapes customer perception} |
| {Moment name} | {type} | {stage} | {description} | {experience} | {impact} |

**Most Critical Moment:**
> {Name the single most important moment in this journey and explain why it has outsized impact on customer loyalty and perception.}

---

<!-- DELIVERY MODE SECTIONS -->

## 4. Emotional Arc

<!-- AGENT DELIVERY: Track emotional state numerically across all stages to identify the journey's peaks and valleys. -->
<!-- Emotional score: -3 (very frustrated) to +3 (very delighted). 0 = neutral. -->

| Stage | Emotional Score | Dominant Emotion | Key Driver |
|-------|----------------|-----------------|-----------|
| {Stage 1} | {-3 to +3} | {frustrated / neutral / satisfied / delighted} | {what drives this emotion} |
| {Stage 2} | {score} | {emotion} | {driver} |

**Journey Emotional Narrative:**
> {Describe the overall arc: does the journey start well and deteriorate? Start poorly and recover? Flat throughout? Describe in 2–3 sentences.}

**Key Insight:**
> The {biggest emotional drop / peak} occurs at {stage}, driven by {cause}. This is the highest-leverage intervention point.

---

## 5. Touchpoint Inventory

<!-- AGENT DELIVERY: Catalogue every point where the customer interacts with the product or brand. -->

| # | Touchpoint | Stage | Channel | Owned By | Customer Effort | Satisfaction |
|---|-----------|-------|---------|---------|-----------------|-------------|
| T-01 | {touchpoint name} | {Stage N} | Web / Mobile / Email / Phone / In-person | {team/system} | Low / Medium / High | {1–10} |
| T-02 | {touchpoint} | {stage} | {channel} | {owner} | {effort} | {score} |

**High-Effort Touchpoints (CES > 7):**
> These touchpoints have the highest abandonment and dissatisfaction risk:
> - {touchpoint}: {why effort is high}

---

## 6. Service Blueprint Layer

<!-- Service Blueprint (Shostack, 1984): Extends journey map to show internal operations that support customer experience. -->
<!-- Line of interaction: customer ↔ frontstage | Line of visibility: frontstage ↔ backstage | Line of internal interaction: backstage ↔ support -->

### Frontstage Actions (Customer-Visible)

> What do customers see, hear, and interact with at each stage?

| Stage | Frontstage Actions | Responsible Team | Tools/Systems |
|-------|-------------------|-----------------|---------------|
| {Stage 1} | {actions visible to customer} | {team} | {systems} |

### Backstage Actions (Internal, Not Visible to Customer)

> What internal processes and systems must work correctly to deliver the frontstage experience?

| Stage | Backstage Actions | Responsible Team | Dependencies |
|-------|------------------|-----------------|-------------|
| {Stage 1} | {internal actions} | {team} | {upstream dependencies} |

### Support Processes

> What enabling processes, systems, or policies make the backstage actions possible?

| Process | Supports | Owner | Maturity |
|---------|---------|-------|---------|
| {process name} | {which backstage/frontstage actions} | {owner} | {mature / developing / absent} |

**Failure Points (where backstage failure causes frontstage customer impact):**
- {failure scenario}: {frontstage impact on customer}

---

## 7. Opportunity Map

<!-- AGENT DELIVERY: Prioritize improvements using the emotional arc and touchpoint inventory. -->

| Opportunity | Stage | Type | Impact | Effort | Priority |
|------------|-------|------|--------|--------|---------|
| {opportunity description} | {stage} | Remove pain / Add delight / Reduce effort | HIGH/MED/LOW | HIGH/MED/LOW | P0/P1/P2 |

**Top 3 Opportunities (Discovery Recommendations):**
1. {Highest priority} — {brief rationale}
2. {Second priority}
3. {Third priority}
