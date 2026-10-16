---
id: PM-PS-NNN
type: use-case-specs
agent: pm-product-strategist
status: draft
mode: discovery
risk_domain: value-risk
created: YYYY-MM-DD
last_validated: YYYY-MM-DD
version: 0.1.0
frameworks_applied:
  - JTBD
cross_refs: []
---

<!-- AGENT GUIDANCE (pm-product-strategist):
  DISCOVERY MODE: Complete sections 1–3. One use case, happy path only. Target 1 page.
  DELIVERY MODE: All sections. Full main flow, alternate flows, exception flows, and pre/post conditions.
  Framework trace: Every use case must derive from a JTBD job statement in the parent PRD (cross_refs).
  Use case naming: Actor + Goal format (e.g., "User exports report to PDF").
  This is a PM-level use case spec — behavioral, not technical. Implementation details belong in eng stories.
-->

# Use Case Specifications: {Feature/Product Name}

> **Status:** DRAFT — Discovery mode.
> **ID:** PM-PS-NNN
> **Agent:** pm-product-strategist
> **Risk Domain:** Value Risk — do these use cases deliver the JTBD outcomes?
> **Mode:** DISCOVERY

---

## Document Sections

| Section | Purpose | Mode |
|---------|---------|------|
| [1. Use Case Registry](#1-use-case-registry) | Index of all use cases | Both |
| [2. Actor Definitions](#2-actor-definitions) | Who participates in these use cases | Both |
| [3. Use Cases (Discovery)](#3-use-cases-discovery) | Happy path flows | Both |
| [4. Alternate Flows](#4-alternate-flows) | Valid variations from main flow | Delivery |
| [5. Exception Flows](#5-exception-flows) | Error and edge-case handling | Delivery |
| [6. Use Case Relationships](#6-use-case-relationships) | Include, extend, generalize | Delivery |

---

## 1. Use Case Registry

<!-- AGENT: List all use cases this spec covers. Discovery: primary use cases only. Delivery: full registry. -->

| UC ID | Use Case Name | Actor | JTBD Job Trace | Priority |
|-------|--------------|-------|----------------|----------|
| UC-01 | {Actor + Goal} | {actor} | J-{XX} in PM-PS-NNN | P0/P1/P2 |
| UC-02 | {Actor + Goal} | {actor} | J-{XX} | P0/P1/P2 |

---

## 2. Actor Definitions

<!-- JTBD: Actors map to the "who" in job statements. Actors have roles, not demographics (demographics belong in user-persona.md). -->

| Actor | Role | Permissions | Relationship to Job |
|-------|------|-------------|---------------------|
| {actor name} | {what this actor does in the system} | {what they can and cannot do} | {which JTBD jobs they're trying to accomplish} |

**Primary Actor:** {The actor whose goal drives the use case}
**Supporting Actors:** {Actors whose behavior enables or constrains the primary actor}
**System:** {The product or system being specified}

---

## 3. Use Cases (Discovery)

<!-- AGENT DISCOVERY: Complete one full use case below. Duplicate this block for each additional use case. -->
<!-- AGENT: Use plain language. No technical implementation details. Describe behavior, not mechanism. -->

### UC-01: {Actor + Goal}

**JTBD Job Statement:**
> When {situation}, I want to {action} so I can {outcome}. (From: PM-PS-{NNN}, J-{XX})

**Preconditions:**
- {condition that must be true before this use case can begin}
- {condition 2}

**Trigger:**
> {The event or actor action that initiates this use case}

**Main Success Scenario (Happy Path):**

| Step | Actor | Action | System Response |
|------|-------|--------|----------------|
| 1 | {actor} | {what the actor does} | {what the system does in response} |
| 2 | {actor} | {what the actor does} | {what the system does in response} |
| 3 | {actor} | {what the actor does} | {what the system does in response} |
| N | {actor} | {final action} | {system confirms success} |

**Postconditions (Success):**
- {state of the system after successful completion}
- {state of the actor's context after success}

**Discovery Mode Notes:**
> {Key risks, open questions, or assumptions about this use case that need validation}

---

<!-- DELIVERY MODE SECTIONS -->

## 4. Alternate Flows

<!-- AGENT DELIVERY: Alternate flows are valid alternative paths through the use case — not errors. -->

### UC-01 Alternate Flow A: {Name}

**Divergence Point:** After Step {N} in main success scenario.

**Condition:** {what condition causes the flow to diverge}

| Step | Actor | Action | System Response |
|------|-------|--------|----------------|
| {N}a | {actor} | {alternate action} | {system response} |
| {N}b | {actor} | {action} | {system response — merges back at Step M or has own postcondition} |

**Postcondition:** {outcome of this alternate flow}

---

## 5. Exception Flows

<!-- AGENT DELIVERY: Exception flows handle errors, invalid inputs, system failures. -->

### UC-01 Exception Flow E1: {Exception Name}

**Divergence Point:** At Step {N} in main success scenario.

**Condition:** {what error condition triggers this exception}

| Step | Actor | Action | System Response |
|------|-------|--------|----------------|
| {N}e | System | {detects error} | {error handling response} |
| {N+1}e | {actor} | {actor's response to error} | {system's next response} |

**Resolution Options:**
- Option 1: {how user can recover}
- Option 2: {alternate resolution}

**Postcondition:** {state of system and actor after exception handling}

---

## 6. Use Case Relationships

<!-- UML Use Case relationships: «include» (always invoked), «extend» (conditionally invoked), generalization. -->

| Relationship | Type | Description |
|-------------|------|-------------|
| UC-01 «include» UC-{XX} | Include | {UC-01 always invokes UC-XX as a sub-behavior} |
| UC-{XX} «extend» UC-01 | Extend | {UC-XX adds optional behavior to UC-01 under condition Y} |
| UC-{XX} generalizes UC-{YY} | Generalization | {UC-XX is a specialization of the abstract use case UC-YY} |

**Use Case Diagram (textual):**

```
Actors: {Actor A}, {Actor B}
Primary Use Cases: UC-01, UC-02, UC-03
«include»: UC-01 → UC-04 (authentication)
«extend»: UC-05 → UC-01 (premium feature)
```
