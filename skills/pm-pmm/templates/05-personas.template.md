---
id: PM-CI-NNN
type: user-persona
agent: pm-customer-insight
status: draft
mode: discovery
risk_domain: value-risk
created: YYYY-MM-DD
last_validated: YYYY-MM-DD
version: 0.1.0
frameworks_applied:
  - JTBD
  - Customer Development
cross_refs: []
---

<!-- AGENT GUIDANCE (pm-customer-insight):
  DISCOVERY MODE: Sections 1–4. Hypothesis-based persona. Clearly marked as unvalidated.
  DELIVERY MODE: All sections. Evidence-based, validated with customer development interviews (n >= 5).
  Framework trace: Section 2 (JTBD jobs) is the anchor — all other sections elaborate the job context.
  Customer Development (Steve Blank): Persona must be grounded in "get out of the building" evidence, not assumptions.
  JTBD: Personas are not demographics — they are roles defined by the job being attempted.
  Disambiguation: This is a USER persona (product experience). Buyer persona (purchase decision) is buyer-persona.md.
  Staleness: Re-validate every 90 days. User behavior shifts with product and market changes.
-->

# User Persona: {Persona Name}

> **Status:** DRAFT — Discovery mode. Hypothesis-based. Not validated.
> **ID:** PM-CI-NNN
> **Agent:** pm-customer-insight
> **Risk Domain:** Value Risk — do we understand who our users are and what they need?
> **Mode:** DISCOVERY

---

## Document Sections

| Section | Purpose | Mode |
|---------|---------|------|
| [1. Persona Summary](#1-persona-summary) | Quick-reference overview | Both |
| [2. Jobs to Be Done](#2-jobs-to-be-done) | JTBD job statements and outcomes | Both |
| [3. Context and Situation](#3-context-and-situation) | When and where this persona works | Both |
| [4. Frustrations and Pain Points](#4-frustrations-and-pain-points) | Current experience failures | Both |
| [5. Customer Development Evidence](#5-customer-development-evidence) | Interview data and validation | Delivery |
| [6. Behavioral Patterns](#6-behavioral-patterns) | Observable habits and tendencies | Delivery |
| [7. Decision Criteria](#7-decision-criteria) | How this persona evaluates solutions | Delivery |
| [8. Success Looks Like](#8-success-looks-like) | Desired outcomes when job is done | Delivery |

---

## 1. Persona Summary

<!-- AGENT DISCOVERY: Fill in all fields. Mark unvalidated fields with [HYPOTHESIS]. -->

| Field | Value |
|-------|-------|
| **Name** | {Memorable name — not a demographic label} |
| **Role** | {Job title or functional role in the context of product use} |
| **Primary Job** | {One sentence: the main job this persona is trying to get done} |
| **Segment** | {Which customer segment this persona represents} |
| **Validation Status** | HYPOTHESIS (discovery) / VALIDATED (delivery — n={interview count}) |

**Persona Quote:**
> "{A real or representative quote that captures this persona's worldview and frustration.}"

**Day in the Life (2–3 sentences):**
> {Brief narrative of a typical day for this persona, specifically around the job your product addresses.}

---

## 2. Jobs to Be Done

<!-- JTBD Framework: Jobs are stable over time; solutions change. Define the functional, emotional, and social jobs. -->
<!-- AGENT: Job statements follow the structure: "When [situation], I want to [motivation/action], so I can [expected outcome]." -->

### Primary Functional Job

| Field | Statement |
|-------|-----------|
| **Job Statement** | When {situation}, I want to {action}, so I can {outcome}. |
| **Job Frequency** | {daily / weekly / occasionally / ad hoc} |
| **Current Solution** | {how this persona accomplishes this job today} |
| **Solution Satisfaction** | {1-10, where 10 = perfectly satisfied with current solution} |

### Secondary Functional Jobs (Related Jobs)

| # | Job Statement | Frequency | Satisfaction |
|---|--------------|-----------|-------------|
| J-02 | When {situation}, I want to {action}, so I can {outcome}. | {freq} | {1–10} |
| J-03 | When {situation}, I want to {action}, so I can {outcome}. | {freq} | {1–10} |

### Emotional Job

> When completing the primary job, this persona wants to feel: {emotional state}
> They want to avoid feeling: {negative emotional state}

### Social Job

> When completing this job, this persona wants to be perceived as: {social perception}

### Desired Outcomes (ODI)

<!-- Outcome-Driven Innovation: Outcomes are the metrics customers use to measure job success. -->

| # | Desired Outcome Statement | Importance (1–10) | Satisfaction (1–10) | Opportunity Score |
|---|--------------------------|-------------------|--------------------|-------------------|
| O-01 | Minimize the time it takes to {action} | {score} | {score} | {I + (I - S)} |
| O-02 | Increase the likelihood that {result} | {score} | {score} | {score} |

**Opportunity Score interpretation:** Score > 10 = underserved; Score 10–6 = appropriately served; Score < 6 = overserved.

---

## 3. Context and Situation

<!-- AGENT: Context defines the "When" in the JTBD job statement. Rich context improves solution design. -->

**Work Environment:**
- Setting: {office / remote / field / mobile-primary}
- Tools used alongside this product: {list key tools in their workflow}
- Collaboration pattern: {solo / team / cross-functional / external}

**Trigger Situations:**
> {Describe the specific situations that cause this persona to attempt the primary job.}

| Trigger | Frequency | Urgency |
|---------|-----------|---------|
| {trigger event} | {daily/weekly} | {high / medium / low} |
| {trigger event} | {frequency} | {urgency} |

**Constraints:**
- Time: {time constraints that affect how they approach the job}
- Access: {systems, permissions, or resources they may not have}
- Skills: {relevant capability gaps or proficiencies}

---

## 4. Frustrations and Pain Points

<!-- AGENT DISCOVERY: List observed or hypothesized friction points in current state. -->

| # | Pain Point | Severity | Frequency | Root Cause |
|---|-----------|---------|-----------|-----------|
| P-01 | {description of pain} | HIGH / MED / LOW | {how often} | {underlying cause if known} |
| P-02 | {description of pain} | HIGH / MED / LOW | {how often} | {root cause} |

**Current Workarounds:**
> {Describe how this persona works around the most severe pain points today. Workarounds reveal what they need.}

---

<!-- DELIVERY MODE SECTIONS -->

## 5. Customer Development Evidence

<!-- Customer Development (Steve Blank): Persona must be grounded in real customer interviews. -->
<!-- AGENT DELIVERY: Document the interview evidence that validates this persona. Minimum 5 interviews. -->

| Interview # | Date | Role | Key Quote | Job Confirmed? |
|------------|------|------|-----------|----------------|
| I-01 | {date} | {interviewee role} | "{key quote}" | Yes / Partial / No |
| I-02 | {date} | {role} | "{quote}" | Yes / Partial / No |

**Pattern Summary:**
- Jobs confirmed by >= {N} interviews: {list confirmed jobs}
- Jobs present in some interviews only: {list partial jobs with counts}
- Jobs refuted: {list if any, with evidence}

**Invalidated Assumptions:**
> {List assumptions about this persona that interview data refuted. Tracking invalidations is as important as confirmations.}

---

## 6. Behavioral Patterns

<!-- AGENT DELIVERY: Observable behaviors — things this persona consistently does. Behaviors predict product usage. -->

| Behavior | Trigger | Frequency | Product Implication |
|---------|---------|-----------|---------------------|
| {observable behavior} | {what causes it} | {how often} | {design/feature implication} |

**Technology Adoption Profile:**
- Innovator / Early Adopter / Early Majority / Late Majority / Laggard
- Evidence: {why you classified them this way}

---

## 7. Decision Criteria

<!-- AGENT DELIVERY: How does this persona evaluate and choose solutions? -->

| Criterion | Weight | Current Benchmark | What "Good" Looks Like |
|-----------|--------|------------------|------------------------|
| {criterion 1} | HIGH / MED / LOW | {what they use today} | {what would exceed expectations} |
| {criterion 2} | HIGH / MED / LOW | {benchmark} | {description} |

**Decision Process:**
> {Describe how this persona makes a decision to adopt or change a solution. Who else is involved? What steps?}

---

## 8. Success Looks Like

<!-- AGENT DELIVERY: Define what this persona would say and do differently if the product fully nails their job. -->

**If the primary job is perfectly done, this persona will:**
- Say: "{quote they'd give after a great experience}"
- Do: {observable behavior change}
- Stop doing: {current workaround they'd abandon}
- Recommend to: {who they'd tell}

**NPS Promoter Condition:**
> This persona becomes a promoter when: {specific conditions that drive advocacy}
