<!-- VERSION: 1.2.0 | DATE: 2026-03-04 | SOURCE: skills/ux-lean-ux/SKILL.md (v1.2.0), skills/ux-lean-ux/agents/ux-lean-ux-facilitator.md | PARENT: /ux-lean-ux sub-skill | REVISION: iter3 — ASM-008 severity-absent fallback, ICE citation clarification, Related Files version pinning from iter2 score (0.942) -->

# Lean UX Methodology Rules

> Operational constraints and methodology rules for the `ux-lean-ux-facilitator` agent. Provides Build-Measure-Learn cycle enforcement, hypothesis format validation, assumption mapping criteria, experiment type selection rules, ICE scoring discipline, validated learning documentation requirements, confidence classification rules, and quality gate integration that complement the agent definition.

## Document Sections

| Section | Purpose |
|---------|---------|
| [Build-Measure-Learn Cycle Rules](#build-measure-learn-cycle-rules) | Mandatory steps, ordering constraints, skip conditions, cycle duration limits |
| [Hypothesis Format Validation Rules](#hypothesis-format-validation-rules) | Canonical Lean UX format, required fields, validation criteria, lifecycle states |
| [Assumption Mapping Rules](#assumption-mapping-rules) | 4-quadrant placement criteria, boundary definitions, rating discipline |
| [Experiment Type Selection Rules](#experiment-type-selection-rules) | Selection criteria matrix for 7 experiment types, decision path |
| [ICE Scoring Rules](#ice-scoring-rules) | 1-10 scale anchors for Impact, Confidence, Ease; scoring discipline |
| [Validated Learning Documentation Rules](#validated-learning-documentation-rules) | Evidence requirements, pivot/persevere/kill decision criteria, learning format |
| [Confidence Classification Rules](#confidence-classification-rules) | HIGH/MEDIUM/LOW mapping criteria, synthesis judgment requirements |
| [Quality Gate Integration](#quality-gate-integration) | Score mapping to S-014 rubric dimensions |
| [Related Files](#related-files) | Dependency matrix: upstream, downstream, and sibling references |
| [Self-Review Checklist](#self-review-checklist) | S-010 verification before output persistence |

---

## Build-Measure-Learn Cycle Rules

The Build-Measure-Learn cycle is the core execution loop. These rules govern ordering, completeness, and termination.

> **Source:** Gothelf & Seiden (2021), Chapter 7. Ries (2011), "The Lean Startup." Build-Measure-Learn cycle foundation.

> **Wave 1 prerequisite:** Lean UX facilitation operates in Wave 2 (Data-Ready). When Wave 1 sub-skills (heuristic evaluation, JTBD analysis) have completed, their outputs feed into assumption mapping (ASM-007) and ICE Confidence scoring. See `skills/user-experience/rules/wave-progression.md` for wave entry conditions.

### Step Ordering

The facilitation workflow executes 5 steps in strict sequence. Every step MUST complete before the next begins.

| Step | Name | Predecessor | Output Required Before Advancing |
|------|------|-------------|----------------------------------|
| 1 | Hypothesis Generation | None | At least 1 hypothesis in `HYP-{NNN}` format with all 4 components |
| 2 | Assumption Mapping | Step 1 | Every hypothesis has at least 1 assumption placed in Q1-Q4 with rationale |
| 3 | MVP Experiment Design | Step 2 | Every Q1 assumption has a linked experiment design with success criteria |
| 4 | Validated Learning Documentation | Step 3 + experiment data | Every completed experiment has an `L-{NNN}` learning entry with evidence and decision |
| 5 | Synthesis and Report Generation | Step 4 (or Steps 1-3 if no experiment data) | Self-review checklist passes; report persisted to output location |

### Mandatory Rules

| ID | Rule | Tier | Consequence of Violation |
|----|------|------|--------------------------|
| BML-001 | Steps MUST execute in order (1 through 5). NEVER skip a step. | HARD | Untested assumptions propagate; experiment designs lack hypothesis grounding |
| BML-002 | Step 4 (Validated Learning) MUST NOT execute without experiment data. If no experiment data is provided, Steps 4-5 operate on Steps 1-3 output only. | HARD | Fabricated learning entries violate P-022 (no deception) |
| BML-003 | When `Cycle Scope` is provided, only the specified phases execute per the partial scope table below. If `Cycle Scope` is not one of the 5 valid values (`full-cycle`, `hypothesis-generation`, `assumption-mapping`, `experiment-design`, `learning-documentation`), the agent MUST reject the invocation with an error message listing the valid values. NEVER silently default to `full-cycle` on invalid input. | MEDIUM | Over-execution wastes context budget; under-execution produces incomplete output; silent defaults on invalid input violate P-022 |
| BML-004 | Cycles exceeding 4 weeks duration SHOULD be flagged as over-scoped. Recommend decomposing into smaller hypotheses. | MEDIUM | Large experiments delay learning; Lean UX targets 1-2 week experiment cycles per Gothelf & Seiden (2021), Chapter 6: "MVPs and Experiments." The 4-week outer bound is practitioner guidance for tiny teams (1-3 persons) where longer cycles risk context loss and deferred learning. |
| BML-005 | When a PIVOT decision in Step 4 generates new hypotheses, those hypotheses MUST be added to the backlog and scored before the next cycle begins. NEVER proceed with unscored pivot hypotheses. | HARD | Unscored hypotheses bypass prioritization; testing effort misallocated |
| BML-006 | Step 5 MUST NOT be skipped even for partial scope executions. Every invocation produces a persisted report. | HARD | Unpersisted output violates P-002 (file persistence) |

### Partial Scope Behavior

| Cycle Scope | Steps Executed | Prerequisites |
|-------------|----------------|---------------|
| `full-cycle` | Steps 1-5 | None (default) |
| `hypothesis-generation` | Step 1 + Step 5 (report) | None |
| `assumption-mapping` | Steps 1-2 + Step 5 | None (Step 1 generates hypotheses for Step 2) |
| `experiment-design` | Steps 1-3 + Step 5 | None (Steps 1-2 produce inputs for Step 3) |
| `learning-documentation` | Steps 4-5 | Prior experiment results REQUIRED via input field |

### Cycle Termination Conditions

| Condition | Action |
|-----------|--------|
| All ACTIVE hypotheses resolved (VALIDATED, INVALIDATED, or DEFERRED) | Proceed to Step 5 synthesis |
| PIVOT decision generates new hypotheses | Add to backlog, score, return to Step 1 for next cycle |
| No experiment data available for Step 4 | Produce Steps 1-3 output only; flag "experiment data pending" in report |
| Zero hypotheses generated from input | Return error to orchestrator requesting additional context (NEVER fabricate hypotheses) |

---

## Hypothesis Format Validation Rules

Every hypothesis MUST conform to the canonical Lean UX format. Malformed hypotheses are rejected during self-review (S-010).

> **Source:** Gothelf & Seiden (2021), Chapter 3: "Outcomes, Assumptions, and Hypotheses."

### Canonical Format

```
We believe [outcome]
for [users]
if [change]
because [evidence/reasoning]
```

### Required Components

| Component | Description | Validation Criterion | Rejection Criterion |
|-----------|-------------|---------------------|---------------------|
| **Outcome** | A measurable result expected from the change | Contains a quantifiable or observable metric (e.g., "15% increase in completion rate", "reduction in support tickets") | Vague outcomes ("improve the experience", "make it better"); no measurable dimension |
| **Users** | The specific user segment affected | Names a defined user segment (e.g., "first-time mobile buyers", "enterprise admins") | Generic references ("users", "people", "everyone"); no segment specificity |
| **Change** | The design change being tested | Describes a concrete, implementable modification (e.g., "simplify checkout to single page") | Abstract intentions ("improve the flow", "make it more intuitive"); no specific change |
| **Evidence** | The reasoning or prior data supporting the hypothesis | References specific data, prior findings, or methodology-grounded reasoning (e.g., "heuristic eval found 3 severity-3 navigation issues") | No reasoning provided; circular reasoning ("because we think it will work"); fabricated data |

### Hypothesis ID Format

| Field | Format | Example | Validation |
|-------|--------|---------|------------|
| Hypothesis ID | `HYP-{NNN}` | HYP-001, HYP-012 | Sequential within engagement; no gaps; no duplicates |
| Status | Enum | DRAFT | One of: DRAFT, ACTIVE, VALIDATED, INVALIDATED, DEFERRED |

### Lifecycle State Transitions

| From | To | Trigger | Required Evidence |
|------|-----|---------|-------------------|
| DRAFT | ACTIVE | Hypothesis selected for current Build-Measure-Learn cycle | ICE score assigned |
| ACTIVE | VALIDATED | Experiment result meets success criteria | Learning entry `L-{NNN}` with metric evidence |
| ACTIVE | INVALIDATED | Experiment result fails success criteria | Learning entry `L-{NNN}` with counter-evidence |
| ACTIVE | DEFERRED | Deprioritized during cycle (lower ICE, resource constraint) | One-line rationale in backlog |
| DEFERRED | ACTIVE | Re-prioritized in subsequent cycle | Updated ICE score |
| Any | -- | No backward transitions (VALIDATED/INVALIDATED are terminal) | -- |

### Validation Discipline

| ID | Rule | Tier |
|----|------|------|
| HYP-001 | Every hypothesis MUST include all 4 components (outcome, users, change, evidence). Hypotheses missing any component are REJECTED. | HARD |
| HYP-002 | The outcome component MUST contain a measurable or observable dimension. "Improve user experience" is NOT a valid outcome. | HARD |
| HYP-003 | The users component MUST name a specific segment. "Users" or "people" without qualification is NOT valid. | HARD |
| HYP-004 | The evidence component MUST NOT be fabricated. When no prior data exists, the evidence field SHOULD state the reasoning basis explicitly (e.g., "based on Lean UX heuristic: simplification reduces cognitive load"). | HARD |
| HYP-005 | Hypothesis IDs MUST be sequential within the engagement (`HYP-001`, `HYP-002`, ...) with no gaps. | MEDIUM |
| HYP-006 | Status transitions MUST follow the lifecycle state transition table. Backward transitions (e.g., VALIDATED to ACTIVE) are FORBIDDEN. | HARD |

---

## Assumption Mapping Rules

Assumptions extracted from hypotheses are placed into the 4-quadrant risk/knowledge framework. Quadrant placement determines experimentation priority.

> **Source:** Gothelf & Seiden (2021), Chapter 4: "Assumptions." 4-quadrant assumption mapping framework.

### Quadrant Definitions

| Quadrant | Name | Risk | Knowledge | Action | Priority |
|----------|------|------|-----------|--------|----------|
| **Q1** | Unknown + High Risk | HIGH | UNKNOWN | Test first -- riskiest unknowns that could invalidate the entire approach | HIGHEST |
| **Q2** | Known + High Risk | HIGH | KNOWN | Monitor -- validated but high-impact; revisit if conditions change | MEDIUM |
| **Q3** | Known + Low Risk | LOW | KNOWN | Accept -- validated and low-impact; no action needed | LOW |
| **Q4** | Unknown + Low Risk | LOW | UNKNOWN | Defer -- unknown but low-impact; test only if resources allow | LOWEST |

### Quadrant Boundary Criteria

| Axis | HIGH Classification | LOW Classification |
|------|--------------------|--------------------|
| **Risk** | Assumption failure would invalidate the hypothesis, block a core user flow, or require significant rework (> 1 sprint of effort to recover) | Assumption failure would require minor adjustments, affect secondary flows only, or be recoverable within a single sprint |
| **Knowledge** | KNOWN: Direct evidence exists (prior experiment data, analytics, user research findings, heuristic eval severity >= 2 findings) | UNKNOWN: No direct evidence; based on team intuition, analogies from other products, or general UX principles |

### Assumption Category Classification

Each assumption MUST be classified into exactly one category:

| Category | Definition | Upstream Source (if available) |
|----------|-----------|-------------------------------|
| **Value** | "Users want this outcome" -- relates to whether the change delivers desired value | JTBD job statements, switch forces |
| **Usability** | "Users can accomplish this task" -- relates to whether users can execute the change | Heuristic evaluation findings (severity >= 2) |
| **Feasibility** | "We can build this within constraints" -- relates to technical implementation viability | Engineering estimates, technical constraints |

### Mapping Discipline

| ID | Rule | Tier |
|----|------|------|
| ASM-001 | Every assumption MUST be placed in exactly one quadrant (Q1, Q2, Q3, or Q4). No assumption may remain unplaced. | HARD |
| ASM-002 | Every quadrant placement MUST include a one-line rationale explaining the risk and knowledge assessment. Placements without rationale are REJECTED. | HARD |
| ASM-003 | When uncertain between adjacent quadrants, MUST place the assumption in the HIGHER-risk quadrant. Under-estimating risk leads to untested critical assumptions. | HARD |
| ASM-004 | Every assumption MUST be classified into exactly one category: Value, Usability, or Feasibility. | HARD |
| ASM-005 | Assumption movement between quadrants SHOULD be tracked when evidence accumulates (e.g., Q1 to Q2 after experiment validation). Movement records include: assumption text, from-quadrant, to-quadrant, evidence triggering the move. | MEDIUM |
| ASM-006 | Q1 assumptions MUST have at least one linked experiment design (EXP-{NNN}) before the cycle advances past Step 3. Untested Q1 assumptions represent unmitigated risk. | HARD |
| ASM-007 | When upstream heuristic evaluation findings with severity >= 2 are available, they SHOULD be mapped as usability assumptions. When JTBD job statements are available, they SHOULD inform value assumption generation. | MEDIUM |
| ASM-008 | When upstream heuristic evaluation findings are provided WITHOUT severity ratings, treat ALL such findings as severity-unknown and place them in Q1 (Known-Uncertain) for manual triage. Document the missing severity as a MEDIUM confidence judgment in the Synthesis Judgments Summary. Consequence: unrated findings are not silently dropped, and the assumption map explicitly surfaces the severity gap for human review. | MEDIUM |

---

## Experiment Type Selection Rules

The facilitator selects from 7 experiment types based on hypothesis characteristics, available resources, and desired confidence level.

> **Source:** Gothelf & Seiden (2021), Chapter 7. Ries (2011). Croll & Yoskovitz (2013), "Lean Analytics," Chapter 10: "Deciding What to Build" (experiment design patterns and measurement strategies).

### Experiment Type Matrix

| Experiment Type | Best For | Confidence Yield | Duration | Cost | Minimum User Base |
|----------------|----------|-----------------|----------|------|-------------------|
| **A/B Test** | Quantitative outcome validation with sufficient traffic | HIGH | 1-4 weeks | Medium | Sufficient traffic for statistical power |
| **Fake Door Test** | Demand validation before building | MEDIUM | 1-2 weeks | Low | Existing traffic to host page |
| **Concierge MVP** | Value validation for complex workflows | MEDIUM | 2-4 weeks | Medium | 5-15 participants |
| **Wizard of Oz** | Usability and value validation for AI/automation features | MEDIUM | 1-2 weeks | Medium | 5-10 participants |
| **Paper Prototype** | Usability validation for early-stage concepts | LOW-MEDIUM | 1-3 days | Low | 5 participants |
| **Smoke Test** | Market demand validation | MEDIUM | 1-2 weeks | Low | Existing traffic or ad spend |
| **One-Question Survey** | Specific assumption validation | LOW | 1-3 days | Low | Existing user base for distribution |

### Selection Decision Path

The facilitator MUST apply the following decision criteria in order. The first matching criterion determines the experiment type:

| Priority | Condition | Recommended Experiment | Rationale |
|----------|-----------|----------------------|-----------|
| 1 | Sufficient traffic AND narrow, measurable hypothesis | **A/B Test** | Highest confidence; quantitative validation |
| 2 | Feature does not exist yet AND demand question | **Fake Door Test** or **Smoke Test** | Validate demand before building; fake door for in-product, smoke test for pre-product |
| 3 | Complex workflow hypothesis AND need to test value | **Concierge MVP** | Human-delivered service validates value proposition without engineering investment |
| 4 | AI/automation feature hypothesis AND need to test usability+value | **Wizard of Oz** | Simulates automated experience with human backend; validates interaction patterns |
| 5 | Early concept stage AND need to test usability | **Paper Prototype** | Fastest usability signal at lowest cost; suitable for concept validation |
| 6 | Single specific assumption AND need fast answer | **One-Question Survey** | Minimal overhead for narrow assumption validation |
| 7 (residual) | No single priority (1-6) matches exclusively, OR multiple priorities partially match | Apply **EXP-007**: select the experiment type with the highest confidence yield achievable within the team's resource constraints. Document the selection rationale in the Synthesis Judgments Summary. | Ensures no hypothesis falls through the decision path without an experiment type assignment |

### Selection Discipline

| ID | Rule | Tier |
|----|------|------|
| EXP-001 | Every experiment design MUST reference a linked hypothesis ID (`HYP-{NNN}`). Experiments without hypothesis linkage are REJECTED. | HARD |
| EXP-002 | Every experiment design MUST include measurable success criteria: specific metric + threshold (e.g., "checkout completion rate increases by >= 10% over control"). Success criteria without a numeric threshold or observable criterion are REJECTED. | HARD |
| EXP-003 | Q1 assumptions MUST use experiment types with MEDIUM or HIGH confidence yield. LOW-confidence experiments (one-question survey, paper prototype alone) are insufficient for high-risk unknowns unless combined with a follow-up higher-confidence experiment in the same cycle. | HARD |
| EXP-004 | Experiment type selection MUST consider team resource constraints. NEVER recommend an A/B test when the team lacks sufficient traffic for statistical power. NEVER recommend a concierge MVP when the team cannot commit 2-4 weeks of manual service delivery. | HARD |
| EXP-005 | Experiment IDs MUST follow the format `EXP-{NNN}`, sequential within the engagement with no gaps. | MEDIUM |
| EXP-006 | Each experiment design MUST document: experiment type, description, linked hypothesis ID, duration estimate, sample size requirements (if quantitative), success criteria (metric + threshold), and measurement method. Missing fields trigger self-review rejection. | HARD |
| EXP-007 | When multiple experiment types could apply, the facilitator SHOULD recommend the type with the highest confidence yield achievable within the team's resource constraints. Document the selection rationale in the Synthesis Judgments Summary. | MEDIUM |

---

## ICE Scoring Rules

ICE (Impact, Confidence, Ease) scoring prioritizes hypotheses in the backlog. The framework originates from the growth hacking community (Sean Ellis, GrowthHackers, circa 2015), adapted here for Lean UX hypothesis prioritization.

### Scale Anchors

Each dimension uses a 1-10 integer scale. The following anchors define the scale boundaries and midpoint.

> **Attribution note:** No canonical primary source exists for the ICE scoring framework; it is attributed to Sean Ellis through practitioner channels (GrowthHackers.com community, circa 2015). No peer-reviewed citation is available. The specific percentage thresholds (Impact), evidence tier descriptions (Confidence), and effort-time boundaries (Ease) are author operationalizations adapted from the Sean Ellis / GrowthHackers ICE framework principles for tiny-team Lean UX contexts. The original ICE framework defines the three dimensions and 1-10 scale but does not prescribe specific anchor thresholds; these anchors are Jerry-specific calibrations for the /user-experience skill's target audience (1-3 person product teams).

#### Impact (How many users are affected and how significantly?)

| Score | Anchor | Definition |
|-------|--------|------------|
| 1 | Minimal | Affects < 1% of users OR negligible behavior change |
| 2-3 | Low | Affects 1-10% of users with minor behavior change |
| 4-5 | Moderate | Affects ~25% of users with moderate behavior change |
| 6-7 | Significant | Affects ~50% of users with notable behavior change |
| 8-9 | High | Affects ~75% of users with significant behavior change |
| 10 | Transformative | Affects > 75% of users with fundamental behavior change |

#### Confidence (How much evidence supports this hypothesis?)

| Score | Anchor | Definition |
|-------|--------|------------|
| 1 | Gut feeling | No data, no analogies, no prior research; pure team intuition |
| 2-3 | Weak signal | Anecdotal evidence, single user complaint, informal observation |
| 4-5 | Indirect evidence | Analytics trends, competitor benchmarks, related heuristic findings, general UX principles |
| 6-7 | Moderate evidence | User research findings (interviews, surveys), heuristic evaluation severity >= 2 findings, JTBD job statements |
| 8-9 | Strong evidence | Prior Build-Measure-Learn cycle data, A/B test results from related experiments |
| 10 | Direct validation | Statistically significant A/B test data directly testing this hypothesis |

#### Ease (How quickly can we test this hypothesis?)

| Score | Anchor | Definition |
|-------|--------|------------|
| 1 | Very difficult | > 1 month of engineering/design effort to build the experiment |
| 2-3 | Difficult | 2-4 weeks effort; requires significant coordination or new infrastructure |
| 4-5 | Moderate | 1-2 weeks effort; requires moderate coordination |
| 6-7 | Easy | 3-5 days effort; uses existing tools with minor setup |
| 8-9 | Very easy | 1-2 days effort; uses existing tools directly |
| 10 | Trivial | < 1 day; can test with a simple survey or existing analytics |

### Composite Score Calculation

```
ICE Score = (Impact + Confidence + Ease) / 3
```

Range: 1.0 to 10.0. Hypotheses with higher ICE scores are tested first.

### Tiebreaking

When ICE scores are tied (identical composite scores), prefer the hypothesis in the higher-risk assumption quadrant: Q1 > Q2 > Q4 > Q3.

### Scoring Discipline

| ID | Rule | Tier |
|----|------|------|
| ICE-001 | Every hypothesis in the backlog MUST have an ICE score assigned before it transitions from DRAFT to ACTIVE. | HARD |
| ICE-002 | When uncertain between two adjacent scores on any dimension, MUST choose the LOWER score. Over-estimating ICE scores leads to misallocated experimentation effort (P-022 compliance). | HARD |
| ICE-003 | ICE scores MUST be re-scored after each Build-Measure-Learn cycle. Evidence from completed experiments changes Confidence levels for related hypotheses. | HARD |
| ICE-004 | The Confidence dimension MUST NOT score above 5 when the only evidence is team intuition or general UX principles. Scores of 6+ require methodology-grounded evidence (user research, heuristic findings, analytics data). | HARD |
| ICE-005 | The Ease dimension MUST account for actual team size and resources. A 1-person team SHOULD NOT score Ease identically to a 5-person team for the same experiment. **Calibration example:** A Concierge MVP requiring 2 weeks of manual service delivery scores Ease 4-5 for a 3-person team (moderate coordination) but Ease 2-3 for a 1-person team (sole operator cannot sustain manual delivery alongside other work). When team size is not explicitly stated, assume a 1-3 person team per the /user-experience skill's tiny-team target audience. | MEDIUM |
| ICE-006 | Each dimension score MUST be an integer (1-10). No fractional scores. The composite ICE score is the arithmetic mean and MAY be fractional. | MEDIUM |
| ICE-007 | PIVOT hypotheses generated from Step 4 MUST be scored before the next cycle begins. They enter the backlog as DRAFT with a new ICE score. | HARD |

---

## Validated Learning Documentation Rules

Every completed Build-Measure-Learn cycle produces a validated learning entry. These rules govern evidence requirements and decision criteria.

> **Source:** Gothelf & Seiden (2021), Chapter 7. Ries (2011), "The Lean Startup," Chapter 7: "Measure."

### Learning Entry Format

```markdown
### Learning L-{NNN}: {brief description}

- **Hypothesis:** HYP-{NNN} -- {hypothesis statement}
- **Experiment:** {experiment type} -- {experiment description}
- **Duration:** {start date} to {end date}
- **Success Criteria:** {what was measured and the threshold}
- **Result:** VALIDATED | INVALIDATED
- **Evidence:** {specific data, metrics, or observations supporting the result}
- **Decision:** PIVOT | PERSEVERE | KILL
- **Next Action:** {what changes based on this learning}
```

### Required Fields

| Field | Requirement | Rejection Criterion |
|-------|-------------|---------------------|
| Learning ID | Sequential `L-{NNN}` within the engagement | Non-sequential, duplicate, or missing ID |
| Hypothesis | Must reference a valid `HYP-{NNN}` with the full hypothesis statement | Invalid hypothesis reference; missing statement |
| Experiment | Must name the experiment type and describe what was tested | Missing experiment type or description |
| Duration | Start and end dates (or "in progress" if ongoing) | Missing date information |
| Success Criteria | Must restate the metric and threshold from the experiment design | Missing metric or threshold; criteria that differ from experiment design without explanation |
| Result | Exactly one of: VALIDATED or INVALIDATED | Missing result; ambiguous result; result without success criteria comparison |
| Evidence | Specific data, metrics, or observations that support the result classification | Absent evidence; generic assertions ("it worked"); claims without data reference |
| Decision | Exactly one of: PIVOT, PERSEVERE, or KILL | Missing decision; decision inconsistent with result |
| Next Action | Concrete next step based on the decision | Vague actions ("do more research"); actions that contradict the decision |

### Evidence Quality Standard

Evidence MUST reference specific, observable data points. Acceptable evidence includes:
- "Checkout completion rate increased from 23% to 31% (n=450, p<0.05) over 2-week A/B test period"
- "3 of 5 Wizard of Oz participants completed the workflow without assistance; 2 required prompting at the payment step"
- "Fake door click-through rate was 2.1% (below 5% threshold); 89 unique visitors during test period"

Unacceptable evidence includes:
- "Users seemed to like it" (subjective, no specific observation)
- "The experiment was successful" (circular, no data)
- "We feel confident this works" (opinion, no measurement)

### Decision Criteria

| Decision | When to Apply | Required Evidence | Consequence |
|----------|---------------|-------------------|-------------|
| **PERSEVERE** | Hypothesis validated -- experiment met success criteria | Metric data meeting or exceeding the defined threshold | Continue in validated direction; feed validated hypothesis to downstream HEART Metrics for ongoing measurement |
| **PIVOT** | Hypothesis partially validated or invalidated with useful learning -- evidence points to a different approach | Specific learning that informs a new hypothesis direction; data showing which aspect failed and which succeeded | Generate new hypotheses based on learning; add to backlog with new ICE scores; return to Step 1 |
| **KILL** | Hypothesis invalidated with strong counter-evidence -- no viable alternative direction identified | Clear metric failure AND no secondary findings suggesting an alternative | Archive the hypothesis and learning entry; remove from active backlog; do NOT generate replacement hypotheses from this direction |

### Documentation Discipline

| ID | Rule | Tier |
|----|------|------|
| VLD-001 | Every completed experiment MUST produce exactly one learning entry (`L-{NNN}`). No experiment goes undocumented. | HARD |
| VLD-002 | The Result field MUST be determined by comparing experiment data against the pre-defined success criteria. NEVER classify a result as VALIDATED without evidence meeting the threshold. | HARD |
| VLD-003 | The Decision field MUST be consistent with the Result: VALIDATED results lead to PERSEVERE or (rarely) PIVOT; INVALIDATED results lead to PIVOT or KILL. A PERSEVERE decision on an INVALIDATED result is FORBIDDEN. | HARD |
| VLD-004 | PIVOT decisions MUST generate at least one new hypothesis. The new hypothesis MUST reference the learning entry that triggered the pivot (e.g., "because L-003 showed users failed at payment step"). | HARD |
| VLD-005 | KILL decisions MUST include a one-line rationale explaining why no pivot is viable. KILL without rationale is REJECTED. | HARD |
| VLD-006 | Learning IDs MUST be sequential within the engagement (`L-001`, `L-002`, ...) with no gaps. | MEDIUM |
| VLD-007 | When no experiment data is available (Cycle Scope is not `learning-documentation` and no prior results provided), Step 4 MUST NOT produce learning entries. NEVER fabricate experiment results (P-022). | HARD |
| VLD-008 | Handoff Data MUST include only hypotheses with status VALIDATED or INVALIDATED. DRAFT, ACTIVE, and DEFERRED hypotheses MUST NOT appear in handoff output to downstream sub-skills (e.g., HEART Metrics). This ensures downstream consumers receive only experimentally resolved propositions. | HARD |

---

## Confidence Classification Rules

Every AI-generated judgment in the facilitation output requires a confidence classification. These rules govern classification criteria and synthesis gate compliance.

> **Source:** `skills/user-experience/rules/synthesis-validation.md` Section "Confidence Classification" and Section "Sub-Skill Synthesis Output Map."

### Classification Criteria

| Classification | Criteria | Action | Example |
|---------------|----------|--------|---------|
| **HIGH** | Multiple data sources converge; validated by prior experiment evidence OR direct user research data | Proceed with recommendation | ICE score based on A/B test data + heuristic eval findings + analytics trends |
| **MEDIUM** | Single-framework reasoning; assumption-based assessment without empirical validation | Include "Validation Required" note; withhold definitive recommendation | Assumption quadrant placement based on team-provided context and general UX principles |
| **LOW** | Insufficient data; speculative assessment; AI inference without empirical grounding | Flag for human review before acting | Hypothesis generated from AI pattern matching without user research or prior experiment data |

### Judgment Types Requiring Classification

The following AI judgment call types MUST each carry a confidence classification in the Synthesis Judgments Summary:

| Judgment Type | Description | Typical Confidence |
|---------------|-------------|-------------------|
| Assumption quadrant placement | Assigning an assumption to Q1, Q2, Q3, or Q4 | MEDIUM (AI risk/knowledge assessment without direct user data) |
| Hypothesis prioritization | ICE scoring and backlog ordering | MEDIUM (scoring involves estimation; re-scores after experiments may reach HIGH) |
| Experiment type recommendation | Selecting which experiment type to use | MEDIUM (selection criteria are methodology-grounded but context-dependent) |
| Hypothesis generation | Creating hypothesis statements from provided input | MEDIUM (secondary-research-derived; Lean UX methodology treats hypotheses as unvalidated by design) |
| Upstream data integration | Incorporating heuristic eval findings or JTBD data into assumptions | HIGH when upstream data has severity >= 2 or strength >= 3; MEDIUM otherwise |
| Pivot direction recommendation | Suggesting new hypothesis direction after INVALIDATED result | LOW (pivot direction requires domain context and user empathy that AI lacks) |

### Lean UX Confidence Dynamics

Lean UX outputs are intentionally MEDIUM confidence because the methodology's purpose is to generate testable propositions. Confidence increases only when:

1. A hypothesis completes a Build-Measure-Learn cycle and transitions to VALIDATED with supporting experiment evidence (individual hypothesis -> MEDIUM)
2. A validated hypothesis converges with a second framework's findings (e.g., HEART Metrics confirms with quantitative measurement -> HIGH)

This means:
- **Pre-experiment outputs** (hypothesis backlogs, assumption maps, experiment designs) are inherently MEDIUM
- **Post-experiment outputs** (validated learning entries with metric evidence) are MEDIUM for individual findings, potentially HIGH when convergent with other frameworks
- **Pivot recommendations** are LOW because they require domain-specific judgment

### Classification Discipline

| ID | Rule | Tier |
|----|------|------|
| CLS-001 | Every AI judgment call in the Synthesis Judgments Summary MUST include a confidence classification (HIGH, MEDIUM, or LOW) and a one-line rationale. | HARD |
| CLS-002 | NEVER classify a pre-experiment judgment (assumption placement, hypothesis generation, experiment recommendation) as HIGH unless multiple independent data sources converge. | HARD |
| CLS-003 | When upstream sub-skill data is available (heuristic findings severity >= 2, JTBD strength >= 3), the integration judgment MAY be classified as HIGH. When upstream data is absent, the judgment MUST be MEDIUM or LOW. | MEDIUM |
| CLS-004 | Pivot direction recommendations MUST be classified as LOW. Pivot direction requires domain-specific judgment that AI cannot reliably provide from secondary research alone. | HARD |
| CLS-005 | The minimum-confidence rule applies: when a single finding draws from multiple judgment types with different confidence levels, the finding's confidence is the LOWEST among all contributing judgments. | HARD |

---

## Quality Gate Integration

Lean UX facilitation output maps to the S-014 LLM-as-Judge rubric dimensions (`.context/rules/quality-enforcement.md` Section "Quality Gate") as follows:

### Dimension Mapping

| S-014 Dimension | Weight | Lean UX Evaluation Criteria |
|-----------------|--------|----------------------------|
| **Completeness** | 0.20 | All 5 methodology steps addressed (or valid partial scope); all hypotheses have 4 components; all assumptions mapped to quadrants; all Q1 assumptions have linked experiments; all completed experiments have learning entries |
| **Internal Consistency** | 0.20 | Hypothesis IDs, experiment IDs, and learning IDs are sequential and cross-referenced correctly; ICE scores align with evidence levels; decisions (pivot/persevere/kill) are consistent with experiment results; assumption quadrant placements are consistent with stated risk/knowledge rationale |
| **Methodological Rigor** | 0.20 | Canonical Lean UX format followed; Build-Measure-Learn cycle ordering enforced; ICE scoring anchors applied consistently; experiment type selection matches decision criteria; assumption categories correctly classified |
| **Evidence Quality** | 0.15 | Hypothesis evidence fields cite specific data or methodology-grounded reasoning; learning entries contain specific metrics or observations; no fabricated data; confidence classifications reflect actual evidence availability |
| **Actionability** | 0.15 | Experiment designs include measurable success criteria with numeric thresholds; remediation paths are concrete; next actions are specific and implementable; ICE scores enable clear prioritization decisions |
| **Traceability** | 0.10 | Every hypothesis traces to an assumption; every experiment traces to a hypothesis; every learning entry traces to an experiment; upstream data sources cited where used; methodology sources referenced |

### Scoring Discipline for Lean UX

| ID | Rule | Tier |
|----|------|------|
| QG-001 | The quality gate threshold applies to the overall facilitation report, not to individual hypotheses or experiments. Baseline threshold: >= 0.92 (H-13, C2+). At C4 criticality (e.g., user-specified or auto-escalated), the threshold is >= 0.95. | HARD |
| QG-002 | Completeness scoring MUST account for partial scope: when `Cycle Scope` limits execution to specific steps, completeness is assessed against the scoped steps only, not the full 5-step workflow. **Denominator mechanics:** The scoring denominator is the number of steps in the partial scope table row for the given Cycle Scope value, plus Step 5 (report). Examples: `hypothesis-generation` scope = 2-step denominator (Step 1 + Step 5); `experiment-design` scope = 4-step denominator (Steps 1-3 + Step 5). Each step is scored as complete (1) or incomplete (0); completeness = completed steps / denominator. | MEDIUM |
| QG-003 | Evidence Quality scoring MUST penalize fabricated or circular evidence in hypothesis statements, assumption rationale, and learning entries. | HARD |
| QG-004 | Internal Consistency scoring MUST verify that decision fields (pivot/persevere/kill) are logically consistent with result fields (validated/invalidated) per VLD-003. | HARD |

---

## Related Files

> Dependency matrix for operational traceability. Upstream files provide inputs or prerequisites; downstream files consume this rules file's outputs; sibling files share the same parent sub-skill.

| Relationship | File | Version | Purpose |
|-------------|------|---------|---------|
| **Parent SKILL.md** | `skills/ux-lean-ux/SKILL.md` | v1.2.0 | Sub-skill definition; methodology overview; agent routing |
| **Agent definition** | `skills/ux-lean-ux/agents/ux-lean-ux-facilitator.md` | v1.1.0 | Agent frontmatter, system prompt, output section (handoff threshold) |
| **Governance YAML** | `skills/ux-lean-ux/agents/ux-lean-ux-facilitator.governance.yaml` | v1.1.0 | Enforcement metadata: quality_threshold (0.95), quality_gate (S-014) |
| **Wave progression** | `skills/user-experience/rules/wave-progression.md` | unversioned -- tracked via git history | Wave 2 (Data-Ready) entry conditions; Wave 1 completion is a prerequisite for Lean UX invocation |
| **Synthesis validation** | `skills/user-experience/rules/synthesis-validation.md` | v1.1.0 | Confidence classification shared taxonomy; Sub-Skill Synthesis Output Map |
| **MCP runbook** | `skills/user-experience/rules/mcp-coordination.md` | unversioned -- tracked via git history | Miro MCP integration; degraded-mode disclosure requirements |
| **Output templates** | `skills/ux-lean-ux/templates/` | -- | Report template consumed by facilitator agent |
| **Quality enforcement** | `.context/rules/quality-enforcement.md` | -- | S-014 dimension rubric; H-13 quality gate threshold (>= 0.92 baseline, >= 0.95 at C4) |

> **Wave 1 prerequisite:** This rules file governs agent behavior in Wave 2 (Data-Ready). Per `wave-progression.md`, Wave 1 (Foundation) completion is required before Lean UX facilitation executes. When Wave 1 outputs (heuristic evaluation findings, JTBD job statements) are available, they feed into assumption mapping (ASM-007) and ICE Confidence scoring.

---

## Self-Review Checklist

Before persisting the report, the facilitator MUST verify (S-010, H-15):

| # | Check | Rule Reference |
|---|-------|---------------|
| 1 | All hypotheses follow the canonical Lean UX format (all 4 components present) | HYP-001 |
| 2 | Every hypothesis has a unique, sequential `HYP-{NNN}` ID with no gaps | HYP-005 |
| 3 | Every hypothesis has an ICE score before transitioning to ACTIVE | ICE-001 |
| 4 | Every assumption has a quadrant placement (Q1-Q4) with one-line rationale | ASM-001, ASM-002 |
| 5 | Every assumption is classified into exactly one category (Value/Usability/Feasibility) | ASM-004 |
| 6 | Every Q1 assumption has at least one linked experiment design | ASM-006 |
| 7 | Every experiment design has measurable success criteria (metric + threshold) | EXP-002, EXP-006 |
| 8 | Every completed experiment has a learning entry with evidence and decision | VLD-001 |
| 9 | No learning entries exist without corresponding experiment data | VLD-007 |
| 10 | Decision fields are consistent with result fields (no PERSEVERE on INVALIDATED) | VLD-003 |
| 11 | The Synthesis Judgments Summary lists every AI judgment call with confidence classification | CLS-001 |
| 12 | The navigation table is present with correct anchor links (H-23) | H-23 |
| 13 | Degraded mode disclosure is present if operating without Miro MCP | P-022 |
| 14 | Handoff Data includes only VALIDATED or INVALIDATED hypotheses | VLD-008 |
| 15 | PIVOT hypotheses from Step 4 are added to the backlog with ICE scores | BML-005, ICE-007 |

---

*Rule file: lean-ux-methodology-rules.md*
*Version: 1.2.0*
*Parent sub-skill: /ux-lean-ux*
*Parent skill: /user-experience*
*Agent: ux-lean-ux-facilitator*
*SSOT: `skills/ux-lean-ux/SKILL.md` (v1.2.0)*
*Created: 2026-03-04*

<!-- Traceability: PROJ-022 EPIC-002, FEAT-009. Standards: H-23 (navigation), H-34 (agent-dev), SR-002 (input validation), SR-003 (output filtering). Methodology: Gothelf & Seiden (2021), Ries (2011), Croll & Yoskovitz (2013), Sean Ellis / GrowthHackers (circa 2015). Synthesis validation: skills/user-experience/rules/synthesis-validation.md. Quality gate: .context/rules/quality-enforcement.md. ORCHESTRATION: projects/PROJ-022-user-experience-skill/orchestration/ux-skill-build-20260303-001/ORCHESTRATION.yaml -->
<!-- VERSION: 1.2.0 | DATE: 2026-03-04 | SOURCE: skills/ux-lean-ux/SKILL.md (v1.2.0), skills/ux-lean-ux/agents/ux-lean-ux-facilitator.md, Gothelf & Seiden (2021), Ries (2011), Croll & Yoskovitz (2013) Ch.10, Sean Ellis / GrowthHackers (circa 2015) | REVISION: iter3 — ASM-008 severity-absent fallback, ICE citation clarification, Related Files version pinning from iter2 score (0.942) -->
