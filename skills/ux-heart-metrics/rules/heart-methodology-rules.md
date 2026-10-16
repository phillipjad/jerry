<!-- VERSION: 1.2.0 | DATE: 2026-03-04 | SOURCE: skills/ux-heart-metrics/SKILL.md, skills/ux-heart-metrics/agents/ux-heart-analyst.md | PARENT: /ux-heart-metrics sub-skill | REVISION: iter2 quality gate revisions (unnamed benchmark citations converted to Fallback Step 3, version alignment with SKILL.md, self-review item 9 SI-006 misattribution fix, P-020 constitution path, MP-009 effort format) -->

# HEART Methodology Rules

> Operational constraints and methodology rules for the `ux-heart-analyst` agent. Provides HEART dimension selection criteria, GSM process rules, threshold fallback methodology, confidence classification, goal adjudication, signal-to-metric edge case handling, dashboard specification rules, and the GSM worksheet template. This file is the SSOT for how the ux-heart-analyst agent applies the HEART framework.

## Document Sections

| Section | Purpose |
|---------|---------|
| [Workflow Phase Sequencing Rules](#workflow-phase-sequencing-rules) | Explicit phase-order constraints for the 5-phase GSM sequential workflow |
| [HEART Dimension Selection Rules](#heart-dimension-selection-rules) | When to include/exclude each dimension; lifecycle stage alignment |
| [GSM Process Rules](#gsm-process-rules) | Goal definition, signal identification, and metric specification rules |
| [Threshold Fallback Methodology](#threshold-fallback-methodology) | 4-step graduated approach when industry benchmarks are unavailable |
| [Measurement Plan Mode Rules](#measurement-plan-mode-rules) | Trigger condition, P-022 disclosure, output modifications when no analytics infrastructure |
| [Confidence Classification Rules](#confidence-classification-rules) | HIGH/MEDIUM/LOW for metric thresholds; REFERENCE-ONLY tagging |
| [Goal Adjudication Rules](#goal-adjudication-rules) | Tie-breaking when multiple goals exist per dimension |
| [Signal-to-Metric Edge Cases](#signal-to-metric-edge-cases) | Single signal/multiple metrics, no signal available |
| [Dashboard Specification Rules](#dashboard-specification-rules) | Metric card format, visualization types, refresh frequency |
| [Quality Gate Integration](#quality-gate-integration) | How scores map to S-014 rubric dimensions |
| [GSM Worksheet Template](#gsm-worksheet-template) | Combined GSM worksheet, metric card template, and worked examples |
| [Self-Review Checklist](#self-review-checklist) | S-010 verification before output persistence |
| [References](#references) | Source citations and traceability |

---

## Workflow Phase Sequencing Rules

The HEART metrics analysis follows a 5-phase sequential workflow. Phases MUST execute in order -- no phase may be skipped or reordered. Each phase produces intermediate artifacts that feed the next phase. This section is the rules SSOT for phase ordering; the agent definition `<methodology>` section provides detailed activities per phase.

> **Source:** Phase structure derived from the GSM sequential discipline (Rodden, Hutchinson & Fu, 2010) applied at the macro-workflow level.

### Phase Order Constraint

| Rule ID | Rule | Consequence of Violation |
|---------|------|-------------------------|
| WF-001 | Phases MUST execute in the sequence: Phase 1 (Context Gathering) then Phase 2 (Dimension Selection) then Phase 3 (GSM Execution) then Phase 4 (Threshold Setting) then Phase 5 (Dashboard Specification) | Producing metrics (Phase 3) without dimension selection (Phase 2) yields metrics for the wrong dimensions; setting thresholds (Phase 4) without metric formulas (Phase 3) produces meaningless targets |
| WF-002 | Each phase MUST complete before the next phase begins -- partial phase outputs MUST NOT be carried forward as complete | Downstream phases operating on incomplete upstream data propagate gaps; GSM traceability chain breaks |
| WF-003 | Phase 1 (Context Gathering) MUST determine whether Measurement Plan mode applies (analytics infrastructure = "none") before Phase 2 begins | Measurement Plan mode affects output modifications in all subsequent phases; late detection causes rework |
| WF-004 | Phase 3 (GSM Execution) MUST follow the internal GSM sequence: Goal Definition (3a) then Signal Identification (3b) then Metric Specification (3c) per [GSM Process Rules](#gsm-process-rules) | Specifying metrics without goals violates the GSM process and breaks the traceability chain (Goal to Signal to Metric) |

### Phase Summary

| Phase | Name | Input | Output | Rules Governing Content |
|-------|------|-------|--------|------------------------|
| 1 | Context Gathering | UX CONTEXT handoff data | Context brief: domain, feature scope, data source inventory, measurement maturity | Input validation rules in agent definition `<input>` section |
| 2 | Dimension Selection | Context brief from Phase 1 | Selected dimensions with inclusion/exclusion rationale | [HEART Dimension Selection Rules](#heart-dimension-selection-rules) (DS-001 through DS-006) |
| 3 | GSM Execution | Selected dimensions from Phase 2 | GSM tables per dimension (Goals, Signals, Metrics) | [GSM Process Rules](#gsm-process-rules) (GD-001 through GD-006, SI-001 through SI-006, MS-001 through MS-008) |
| 4 | Threshold Setting | Metric specifications from Phase 3 | Baseline and threshold table per metric | [Threshold Fallback Methodology](#threshold-fallback-methodology), [Measurement Plan Mode Rules](#measurement-plan-mode-rules) |
| 5 | Dashboard Specification | Metrics and thresholds from Phases 3-4 | Dashboard specification with metric cards, visualization types, drill-downs | [Dashboard Specification Rules](#dashboard-specification-rules) (DF-001 through DF-004, DL-001 through DL-004) |

---

## HEART Dimension Selection Rules

The HEART framework provides five complementary dimensions for measuring user experience. Not all five dimensions apply to every product or feature -- dimension selection is a deliberate analytical step, not a default inclusion.

> **Source:** Rodden, K., Hutchinson, H., & Fu, X. (2010). "Measuring the User Experience on a Large Scale: User-Centered Metrics for Web Applications." Proceedings of CHI '10, ACM.

### Dimension Definitions

| Dimension | Definition | Measures | Example Signal |
|-----------|-----------|----------|---------------|
| **Happiness** | Subjective user satisfaction and attitudes | How users feel about the product | NPS score, satisfaction survey rating, sentiment in feedback |
| **Engagement** | User involvement and interaction depth | How much users interact with the product | Session frequency, feature usage depth, time on task (when desirable) |
| **Adoption** | New user uptake and feature discovery | How many new users start using the product/feature | New user signups, feature first-use rate, onboarding completion |
| **Retention** | Continued usage over time | How many users keep coming back | Week-over-week active user ratio, churn rate, renewal rate |
| **Task Success** | Effectiveness, efficiency, and error rate | How well users accomplish their goals | Task completion rate, time-on-task, error rate, abandonment rate |

### Lifecycle Stage Alignment

The product lifecycle stage determines which HEART dimensions receive priority. This mapping is the primary selection heuristic.

| Lifecycle Stage | Primary Dimensions | Secondary Dimensions | Rationale |
|----------------|-------------------|---------------------|-----------|
| **New product** (pre-launch to 6 months) | Adoption, Task Success | Happiness | New products must prove users can find and successfully use the product before measuring ongoing engagement or retention |
| **Growing** (6 months to 2 years) | Engagement, Adoption | Task Success, Happiness | Growing products need to deepen user involvement while continuing to attract new users |
| **Mature** (2+ years, stable user base) | Engagement, Retention | Happiness, Task Success | Mature products must retain existing users and keep them actively engaged |
| **Declining** (user loss trend) | Retention, Happiness | Task Success | Declining products must understand why users leave and whether remaining users are satisfied |

### Dimension Inclusion Rules

Each HEART dimension MUST be assessed against both inclusion and exclusion criteria below. A dimension is included when it meets ANY inclusion criterion (DS-001 through DS-003). A dimension is excluded only when it meets an exclusion criterion (DS-004, DS-005) AND the exclusion is documented per the [Exclusion Documentation Format](#exclusion-documentation-format).

**Inclusion criteria** -- a dimension is included when ANY of the following apply:

| Rule ID | Rule | Applies When |
|---------|------|-------------|
| DS-001 | **Include** a dimension when it is a Primary dimension for the product's lifecycle stage | Always -- lifecycle stage is the first selection filter |
| DS-002 | **Include** a dimension when upstream sub-skill findings specifically reference it (e.g., heuristic evaluation findings mapped to a HEART category) | Upstream handoff data references the dimension |
| DS-003 | **Include** a dimension when the user explicitly requests it, regardless of lifecycle alignment | User authority (P-020) overrides lifecycle-based selection |

**Exclusion criteria** -- a dimension is excluded only when the following apply AND the exclusion is documented:

| Rule ID | Rule | Applies When |
|---------|------|-------------|
| DS-004 | **Exclude** a dimension when no data source exists or can be instrumented for that dimension AND the team has no capacity to create instrumentation | Resource constraint; document in exclusion rationale |
| DS-005 | **Exclude** a dimension when the analysis scope is feature-level and the dimension applies only at product-level (e.g., Retention for a single form redesign) | Feature-level analysis; document scope mismatch |

**Capacity constraint:**

| Rule ID | Rule | Applies When |
|---------|------|-------------|
| DS-006 | **Limit** to 2-3 dimensions for tiny teams (1-5 people) to keep measurement manageable | Team capacity constraint; select the 2-3 highest-priority dimensions |

### Exclusion Documentation Format

Every excluded dimension MUST be documented in the HEART Dimension Selection table with an explicit rationale:

```markdown
| Dimension | Selected | Rationale |
|-----------|----------|-----------|
| Retention | No | Feature-level analysis (checkout flow); Retention is a product-level metric not applicable to a single feature (DS-005) |
```

### All-Five Override

When the user explicitly requests all five dimensions (P-020: `docs/governance/JERRY_CONSTITUTION.md`), the analyst MUST comply but SHOULD note capacity implications: "All 5 HEART dimensions selected per user request. For tiny teams (1-5 people), monitoring 5 dimensions simultaneously requires significant analytics investment. Consider prioritizing 2-3 dimensions for initial instrumentation and adding remaining dimensions in subsequent measurement cycles."

---

## GSM Process Rules

The Goals-Signals-Metrics (GSM) process is the core analytical workflow applied sequentially for each selected HEART dimension. The three steps (Goal, Signal, Metric) MUST execute in order -- no step may be skipped or reordered.

> **Source:** Rodden, K., Hutchinson, H., & Fu, X. (2010). "Measuring the User Experience on a Large Scale." Proceedings of CHI '10.

### Goal Definition Rules

| Rule ID | Rule | Consequence of Violation |
|---------|------|-------------------------|
| GD-001 | Each selected HEART dimension MUST have exactly one goal statement | Multiple goals per dimension create ambiguous measurement targets; see [Goal Adjudication Rules](#goal-adjudication-rules) for tie-breaking |
| GD-002 | Goals MUST describe user outcomes, not business outcomes | "Users complete checkout with confidence" not "Increase revenue" -- business outcomes are consequences of UX improvement, not goals the HEART framework measures |
| GD-003 | Goals MUST be specific to the selected HEART dimension | A Task Success goal must relate to task completion, efficiency, or error rates -- not to satisfaction (Happiness) or frequency of use (Engagement) |
| GD-004 | Goals SHOULD be time-bounded where possible | "Users complete onboarding within their first session" is preferable to "Users complete onboarding" -- time bounding enables threshold setting |
| GD-005 | Goals MUST align with the product's current lifecycle stage | A new product goal should reference adoption or task completion; a mature product goal should reference retention or engagement depth |
| GD-006 | Goals MUST NOT reference specific metric values | "Users complete checkout" not "85% of users complete checkout" -- quantification belongs in the Metric step, not the Goal step |

**Goal format:**
```
[HEART Dimension] Goal: [User-centered outcome statement]
```

**Example (compliant):**
```
Task Success Goal: Users complete the checkout process without encountering errors or needing help.
```

**Example (non-compliant -- violates GD-002):**
```
Task Success Goal: Increase checkout conversion rate to drive revenue growth.
```

### Signal Identification Rules

| Rule ID | Rule | Consequence of Violation |
|---------|------|-------------------------|
| SI-001 | Each goal MUST have 2-4 identified signals | Fewer than 2 creates single-point-of-failure measurement; more than 4 creates measurement overhead for tiny teams |
| SI-002 | Each signal MUST be classified as Leading or Lagging | Signal classification determines whether the metric is predictive or confirmatory; omitting classification prevents correct dashboard interpretation |
| SI-003 | At least one signal per goal MUST be a Lagging signal (outcome confirmation) | Without a lagging signal, the team cannot confirm whether the goal was actually achieved -- only predict that it might be |
| SI-004 | Signals MUST describe observable user behaviors, not internal system states | "User clicks Submit button" is observable; "Server processes request" is a system state -- HEART measures user experience, not system performance |
| SI-005 | Signal observability MUST be assessed against available data sources | Flag signals that cannot be observed with current instrumentation; see [Signal-to-Metric Edge Cases](#signal-to-metric-edge-cases) for handling |
| SI-006 | Signals from upstream sub-skill findings (e.g., heuristic evaluation severity >= 2 findings) SHOULD be incorporated when available | Upstream findings provide evidence-grounded signal candidates that strengthen the GSM chain |

**Signal types:**

| Type | Definition | Use Case | Example |
|------|-----------|----------|---------|
| **Leading** | Behavior that predicts future goal achievement | Early warning indicator; short feedback loop | Feature exploration rate (predicts adoption) |
| **Lagging** | Behavior that confirms past goal achievement | Outcome validation; confirms improvement | 30-day retention rate (confirms ongoing value) |

### Metric Specification Rules

| Rule ID | Rule | Consequence of Violation |
|---------|------|-------------------------|
| MS-001 | Each signal MUST map to exactly one metric | One-to-one signal-to-metric mapping maintains traceability; see [Signal-to-Metric Edge Cases](#signal-to-metric-edge-cases) for exceptions |
| MS-002 | Every metric MUST include all eight specification fields: Metric Name, HEART Dimension, Formula, Data Source, Measurement Frequency, Target Threshold, Alerting Condition, Baseline | Incomplete specifications cannot be implemented by engineering teams -- missing any field creates ambiguity |
| MS-003 | Formulas MUST be precise and calculable | "(Completed / Initiated) * 100" not "Completion percentage" -- formulas must be unambiguous enough for an engineer to implement |
| MS-004 | Data Sources MUST reference specific analytics events or survey instruments | "Analytics event: `checkout_completed`" not "Analytics" -- specificity enables instrumentation |
| MS-005 | When a data source does not yet exist, the metric MUST be flagged as requiring instrumentation | Flag format: "Data Source: TBD -- requires instrumentation of `{event_name}` event" |
| MS-006 | Target Thresholds MUST cite their derivation source | Industry benchmark citation, baseline measurement reference, or Threshold Fallback Methodology step number -- see [Threshold Fallback Methodology](#threshold-fallback-methodology) |
| MS-007 | Alerting Conditions MUST specify both the threshold value and the duration before alert fires | "< 75% for 3 consecutive days" not "Below target" -- duration prevents noise from single-day fluctuations |
| MS-008 | Baselines MUST include the measurement date range when available, or "TBD: measure before launch" when not | Date ranges enable trend analysis; TBD flags signal pending instrumentation |

---

## Threshold Fallback Methodology

When no baseline data exists for setting metric thresholds, follow this 4-step graduated approach. Each step is attempted in order; proceed to the next step only when the current step cannot be applied.

> **Source:** Adapted from Rodden et al. (2010) GSM process guidance. Industry benchmark sources: Baymard Institute (e-commerce), Reichheld (2003) / Bain & Company (NPS).

| Step | Action | When to Use | Example |
|------|--------|-------------|---------|
| 1 | **Use industry benchmarks** from published studies as starting point | Published benchmarks exist for the product type and metric category | Baymard Institute reports 69.8% average cart abandonment rate for e-commerce; set checkout completion target at >= 70% (inverted abandonment) |
| 2 | **Run a 2-week baseline measurement** to establish a stable starting point before setting improvement targets | No published benchmarks match the product type, or the team wants product-specific data | "Measure checkout completion rate daily for 14 days to establish baseline before setting improvement target" |
| 3 | **Set initial target as baseline + 10-15% improvement** over the measured or benchmarked value | Baseline (measured or benchmarked) is available; no domain-specific target exists | Baseline: 78% checkout completion; target: 85-90% (10-15% improvement) |
| 4 | **Review and adjust after first measurement cycle** (typically 4-6 weeks of data collection) | Initial target is set; first cycle of real measurement data is available for recalibration | "After 6 weeks, actual data shows 82% baseline; revise target from 85% to 90% based on observed trajectory" |

### Threshold Fallback Documentation

Every threshold MUST document which step of the fallback methodology was applied:

```markdown
| Metric | Target Threshold | Threshold Source | Fallback Step |
|--------|-----------------|------------------|---------------|
| Checkout Completion Rate | >= 85% | Baymard Institute e-commerce benchmark | Step 1 (industry benchmark) |
| Feature Discovery Rate | >= 60% | TBD -- pending 2-week baseline | Step 2 (baseline measurement) |
| Onboarding Completion Rate | >= 80% | Internal baseline (72%) + 12% improvement | Step 3 (baseline + improvement) |
```

### Fallback Constraints

| Constraint | Rule |
|------------|------|
| **Step 1 benchmark recency** | Industry benchmarks older than 3 years SHOULD be flagged: "Benchmark from {year}; verify current values." Cite specific publication (e.g., "Baymard Institute, UX Benchmark dataset, 2024") |
| **Step 2 minimum duration** | Baseline measurement MUST be at minimum 2 weeks (14 days) to capture weekly cyclical patterns |
| **Step 3 improvement range** | Improvement targets MUST be in the 10-15% range. Below 10% is likely noise; above 15% risks setting unachievable targets without structural changes |
| **Step 4 cycle duration** | First measurement cycle SHOULD be 4-6 weeks; MUST be at minimum 4 weeks for threshold recalibration |

---

## Measurement Plan Mode Rules

When the product has no analytics infrastructure (no event tracking, no dashboards, no data collection), the HEART analyst operates in Measurement Plan mode. This section defines the trigger condition, required disclosures, and output modifications for this mode.

> **Source:** Agent definition `<input>` section defines the mode activation logic; this section is the rules SSOT for mode behavior and P-022 disclosure requirements.

### Trigger Condition

| Rule ID | Rule | Consequence of Violation |
|---------|------|-------------------------|
| MP-001 | Measurement Plan mode MUST activate when the Analytics Infrastructure input field is "none" or absent | Proceeding without mode activation produces output that references unavailable data sources, misleading the team |
| MP-002 | Phase 1 (Context Gathering) MUST determine mode activation before Phase 2 begins (see WF-003) | Late detection requires rework of all downstream phase outputs |
| MP-003 | If the user provides analytics infrastructure information after initial mode activation, the analyst MAY exit Measurement Plan mode for subsequent phases -- but already-produced output MUST be revised to reflect the updated infrastructure context | Prevents stale mode-based output from persisting alongside non-mode output |

### P-022 Disclosure Requirement

| Rule ID | Rule |
|---------|------|
| MP-004 | The output MUST include the following disclosure header immediately after the UX Context section when Measurement Plan mode is active: |

**Required disclosure text (verbatim):**
```markdown
> **[MEASUREMENT PLAN MODE]** No analytics infrastructure detected. This output defines
> what to measure and how to instrument it. Current-state metric values are unavailable
> until instrumentation is implemented and baseline data is collected.
```

| Rule ID | Rule |
|---------|------|
| MP-005 | The disclosure text MUST NOT be paraphrased, shortened, or omitted -- P-022 requires explicit disclosure of the mode to prevent the team from treating the output as if current-state data were available |

### Output Modifications in Measurement Plan Mode

When Measurement Plan mode is active, the following output modifications apply:

| Rule ID | Modification | Standard Behavior | Measurement Plan Behavior |
|---------|-------------|-------------------|--------------------------|
| MP-006 | Metric specifications become instrumentation recommendations | Metrics reference existing data sources | Metrics specify what events to instrument, with `[INSTRUMENTATION REQUIRED]` tag on each Data Source field |
| MP-007 | Baseline field is always "TBD: measure after instrumentation" | Baseline may reference existing measurement | Baseline is uniformly "TBD: measure after instrumentation" with recommended measurement duration (minimum 2 weeks per Threshold Fallback Step 2) |
| MP-008 | Threshold values carry `[REFERENCE-ONLY]` AND `[PRE-INSTRUMENTATION]` tags | Thresholds carry `[REFERENCE-ONLY]` only | Double-tagged to distinguish pre-instrumentation estimates from post-instrumentation LOW-confidence values |
| MP-009 | Dashboard specification includes an instrumentation priority section | Dashboard specification assumes data availability | Dashboard specification includes: (a) instrumentation priority ordering (which events to implement first), (b) estimated implementation effort per metric -- effort SHOULD be expressed as t-shirt sizes (XS, S, M, L, XL) or story points, consistent with the team's estimation practice; default to t-shirt sizes when team practice is unknown, (c) recommended instrumentation sequence for incremental rollout |
| MP-010 | The on_send handoff MUST set `measurement_plan_mode: true` | `measurement_plan_mode: false` | Downstream consumers must know this output represents a measurement plan, not a measurement report |

### Validation Rules

| Rule ID | Rule |
|---------|------|
| MP-011 | Self-Review Checklist item 8 MUST verify that the MP-004 disclosure header is present when Measurement Plan mode is active |
| MP-012 | Every metric Data Source field MUST include the `[INSTRUMENTATION REQUIRED]` tag in Measurement Plan mode (MP-006) |

---

## Confidence Classification Rules

All HEART outputs carry confidence classifications per P-022 (no deception about confidence). Confidence is assigned at the output-type level, not the individual metric level.

> **Source:** `skills/user-experience/rules/synthesis-validation.md` [Confidence Classification] and [Sub-Skill Synthesis Output Map].

### Confidence Assignments

| Output Type | Confidence | Rationale | Tag |
|-------------|-----------|-----------|-----|
| Dimension selection rationale | MEDIUM | Lifecycle-stage alignment is methodologically grounded but context-dependent | -- |
| Goal-metric mapping interpretation | MEDIUM | GSM process is methodologically grounded (Rodden et al., 2010) but application to specific product context involves AI judgment | -- |
| Signal identification and classification | MEDIUM | Signal identification draws on established UX measurement patterns but requires context-specific validation | -- |
| Metric formula specification | MEDIUM | Formulas follow standard analytics definitions but data source availability varies by product | -- |
| Metric threshold recommendation | LOW | Threshold values require domain-specific benchmarking data unavailable in training data | `[REFERENCE-ONLY]` |
| Alerting condition specification | LOW | Alert thresholds depend on product-specific variance patterns that require historical data | `[REFERENCE-ONLY]` |
| Dashboard layout and visualization | MEDIUM | Layout follows established visualization best practices (Few, 2006) but requires product-specific customization | -- |

### REFERENCE-ONLY Tagging Rules

| Rule ID | Rule |
|---------|------|
| CR-001 | All threshold values (Target Threshold and Alerting Condition fields) MUST be tagged with `[REFERENCE-ONLY]` in the output |
| CR-002 | The Baseline and Thresholds section MUST include the header tag: `## Baseline and Thresholds [REFERENCE-ONLY]` |
| CR-003 | The `[REFERENCE-ONLY]` tag MUST NOT be applied to MEDIUM-confidence outputs (dimension selection, goal-metric mappings, metric formulas) |
| CR-004 | Every `[REFERENCE-ONLY]` tagged section MUST include the disclosure: "Threshold values reflect AI synthesis from industry benchmarks and the Threshold Fallback Methodology. They do not constitute validated targets for your product. Calibrate against your own baseline data." |

### Confidence Advancement

Confidence MAY be advanced when validation evidence is provided:

| From | To | Required Validation |
|------|-----|-------------------|
| LOW (threshold) | MEDIUM | Domain-specific baseline measurement (4+ weeks) OR published industry benchmark with matched context |
| MEDIUM (goal-metric) | HIGH | 2+ weeks of actual metric data from the product, OR expert review by analytics practitioner, OR A/B test baseline |

Confidence MUST NOT be advanced without the corresponding validation evidence. LOW is permanent within a single engagement without evidence (see `skills/user-experience/rules/synthesis-validation.md` [Classification Immutability]).

---

## Goal Adjudication Rules

When multiple goals are plausible for a single HEART dimension, the analyst MUST select exactly one goal (GD-001) using the following adjudication protocol.

### Adjudication Protocol

| Step | Action | Decision Criterion |
|------|--------|-------------------|
| 1 | **Lifecycle alignment** | Select the goal most directly tied to the product's current lifecycle stage (GD-005). A new product's Task Success goal should focus on first-time task completion, not expert efficiency. |
| 2 | **Upstream evidence** | If upstream sub-skill findings (heuristic evaluation, behavior design) point to a specific problem area, select the goal aligned with that problem. Evidence-backed goals take precedence over inferred goals. |
| 3 | **Measurability** | If Steps 1 and 2 do not differentiate, select the goal for which signals are more readily observable with available data sources. A measurable goal is more valuable than an aspirational but unmeasurable goal. |
| 4 | **User input** | If Steps 1-3 do not differentiate, present both goals to the user and let them decide (P-020). |

### Rejected Alternative Documentation

All rejected goal alternatives MUST be documented in the GSM worksheet notes:

```markdown
| HEART Dimension | Goal | Signal | Metric | Data Source | Threshold | Confidence | Notes |
|-----------------|------|--------|--------|-------------|-----------|------------|-------|
| Task Success | Users complete checkout without errors | ... | ... | ... | ... | MEDIUM | **Rejected alternative:** "Users complete checkout quickly" -- rejected because current lifecycle stage (new product) prioritizes completion over speed (Step 1: lifecycle alignment) |
```

---

## Signal-to-Metric Edge Cases

The standard GSM process assumes a one-to-one mapping from signal to metric (MS-001). The following edge cases require specific handling.

### Single Signal, Multiple Metrics

**When it occurs:** A single observable behavior can be measured in multiple meaningful ways (e.g., "checkout completion" can be measured as completion rate, completion time, and error-free completion rate).

**Handling:**

| Rule ID | Rule |
|---------|------|
| SE-001 | When a single signal maps to multiple potential metrics, select the metric with the **shortest feedback loop** for iteration decisions |
| SE-002 | If the short-feedback-loop metric and a longer-feedback-loop metric both provide distinct value, the analyst MAY specify both but MUST designate one as **Primary** and others as **Secondary** |
| SE-003 | The Primary metric is the one that appears in the dashboard metric card; Secondary metrics appear in the drill-down |

**Example:**
- Signal: "User completes checkout"
- Primary metric: Checkout Completion Rate (short feedback loop -- daily)
- Secondary metric: Error-Free Checkout Completion Rate (narrower, requires error tracking -- weekly)

### No Signal Available

**When it occurs:** A goal has been defined for a HEART dimension, but no observable user behavior can be identified with current instrumentation or reasonable instrumentation investment.

**Handling:**

| Rule ID | Rule |
|---------|------|
| SE-004 | Flag the dimension as having a **measurement gap**: "No observable signal identified for {dimension} goal. This dimension requires instrumentation investment before metrics can be tracked." |
| SE-005 | DO NOT fabricate signals to fill the gap -- absence of a signal is a valid analytical finding (P-022) |
| SE-006 | Include a **recommended instrumentation** note describing what event tracking or survey instrument would need to be implemented to make the signal observable |
| SE-007 | If the measurement gap makes the dimension unmeasurable, recommend reconsidering dimension selection -- an unmeasurable dimension consumes team attention without producing actionable data |

**Example:**
```markdown
### Measurement Gap: Happiness

Goal: Users feel confident in the product's reliability.
Signal: No observable signal -- no survey instrument deployed, no feedback mechanism available.
Recommended Instrumentation: Deploy in-app NPS survey (Reichheld, 2003) triggered after 3rd session. Estimated implementation: 2-3 days with survey tool integration (e.g., Hotjar, Qualtrics).
```

### Multiple Signals, One Metric

**When it occurs:** Two or more distinct signals converge to inform a single composite metric.

**Handling:**

| Rule ID | Rule |
|---------|------|
| SE-008 | Composite metrics MUST document all contributing signals in the GSM table |
| SE-009 | The metric formula MUST make the composition explicit (e.g., weighted average, boolean AND) |
| SE-010 | Each contributing signal MUST independently classify as Leading or Lagging |

---

## Dashboard Specification Rules

The dashboard specification translates metric definitions into implementable visualization guidance. Dashboard layout follows metric visualization best practices per Few (2006) and HEART-specific metric card organization per Rodden et al. (2010).

> **Sources:** Few, S. (2006). *Information Dashboard Design.* Analytics Press. Rodden, K., Hutchinson, H., & Fu, X. (2010). "Measuring the User Experience on a Large Scale." Proceedings of CHI '10.

### Metric Card Format

Each metric in the dashboard MUST be specified as a metric card with the following fields:

| Field | Description | Required |
|-------|-------------|----------|
| **Metric Name** | Display name for the metric card | Yes |
| **HEART Dimension** | Which HEART dimension this card belongs to | Yes |
| **Current Value** | The current metric value (or "Pending Baseline" if not yet measured) | Yes |
| **Target** | Target threshold value with `[REFERENCE-ONLY]` tag | Yes |
| **Trend** | Visualization type for temporal trend | Yes |
| **Alert Status** | Current alert state: Normal, Warning, Critical | Yes |
| **Drill-Down Path** | What detail is accessible when the user clicks the card | Yes |
| **Refresh Frequency** | How often the metric value updates | Yes |

### Visualization Type Selection

| Metric Pattern | Recommended Visualization | Rationale |
|---------------|--------------------------|-----------|
| Rate or percentage (e.g., completion rate) | **Time series line chart** with target line overlay | Shows trend direction relative to target; reveals cyclical patterns |
| Count (e.g., new signups, error count) | **Bar chart** (daily/weekly) or **counter** with delta | Counts are discrete; bars communicate volume better than lines |
| Duration (e.g., time-on-task) | **Time series line chart** with percentile bands (p50, p90) | Percentile bands reveal distribution; median alone hides outlier behavior |
| Score (e.g., NPS, satisfaction rating) | **Gauge** with target zone or **time series** with confidence interval | Gauge for current snapshot; time series for trend monitoring |
| Funnel (e.g., multi-step task completion) | **Funnel chart** with drop-off percentages per step | Reveals where in the process users abandon; pinpoints intervention points |

### Refresh Frequency Rules

| Rule ID | Rule |
|---------|------|
| DF-001 | Metrics based on event tracking SHOULD refresh daily at minimum |
| DF-002 | Metrics based on surveys or feedback SHOULD refresh on the survey collection cadence (weekly, monthly) |
| DF-003 | Alerting conditions MUST evaluate on the metric's refresh frequency -- an alert cannot fire faster than the data updates |
| DF-004 | Dashboard specifications MUST document data latency: the expected delay between user action and metric update |

### Dashboard Layout Rules

| Rule ID | Rule |
|---------|------|
| DL-001 | Metrics MUST be grouped by HEART dimension in the dashboard layout |
| DL-002 | Within each dimension group, the Primary metric (per SE-002) appears first |
| DL-003 | Each dimension group MUST display its goal statement as a header above the metric cards |
| DL-004 | The dashboard MUST include a summary row showing overall HEART health: one indicator per selected dimension showing whether the dimension is on-target, at-risk, or below-target |

---

## Quality Gate Integration

HEART methodology output is evaluated against the S-014 LLM-as-Judge rubric when quality scoring is applied (H-17). The following table maps HEART-specific output characteristics to the six S-014 dimensions.

> **Source:** `.context/rules/quality-enforcement.md` [Quality Gate].

| S-014 Dimension | Weight | HEART-Specific Scoring Criteria |
|-----------------|--------|---------------------------------|
| **Completeness** | 0.20 | All selected HEART dimensions have complete GSM tables (Goal, Signals, Metrics). Every metric has all 8 specification fields. Dimension selection covers all 5 dimensions (included and excluded with rationale). |
| **Internal Consistency** | 0.20 | Goals align with the correct HEART dimension (GD-003). Signals are classified consistently as Leading/Lagging. Metric formulas are calculable from the named data sources. Threshold fallback steps are applied in order. |
| **Methodological Rigor** | 0.20 | GSM process followed sequentially (Goal then Signal then Metric). Dimension selection aligned to lifecycle stage. Threshold Fallback Methodology steps applied correctly. Goal adjudication protocol followed when multiple goals are plausible. |
| **Evidence Quality** | 0.15 | Industry benchmarks cite specific publications with dates (e.g., "Baymard Institute, 2024"). HEART framework references cite Rodden et al. (2010). NPS references cite Reichheld (2003). Threshold sources documented per MS-006. |
| **Actionability** | 0.15 | Metric specifications are implementable by engineering teams (formulas precise, data sources named, frequencies specified). Dashboard specification includes visualization types and drill-down paths. Measurement gaps include recommended instrumentation. |
| **Traceability** | 0.10 | Every metric traces back through Signal to Goal to HEART Dimension. Upstream sub-skill finding references include Finding IDs. Confidence classifications present on all output types per [Confidence Classification Rules](#confidence-classification-rules). |

### Scoring Note

When scoring HEART output, S-014 evaluators SHOULD verify:
1. The GSM chain is unbroken: every Metric has a Signal, every Signal has a Goal, every Goal has a Dimension
2. No threshold value is presented without a `[REFERENCE-ONLY]` tag (CR-001)
3. Goal-metric mappings are classified as MEDIUM confidence, not HIGH (unless validated per [Confidence Advancement](#confidence-advancement))
4. The Synthesis Judgments Summary enumerates all significant AI inferences

---

## GSM Worksheet Template

The GSM worksheet is the primary working artifact for the HEART metrics analysis. The analyst populates one worksheet per selected HEART dimension.

### Worksheet Template

```markdown
## GSM Worksheet: {HEART Dimension}

| HEART Dimension | Goal | Signal | Metric | Data Source | Threshold | Confidence | Notes |
|-----------------|------|--------|--------|-------------|-----------|------------|-------|
| {Dimension} | {User-centered outcome statement} | {Signal 1: observable behavior} ({Leading/Lagging}) | {Metric name} | {Specific event or instrument} | {Target value} [REFERENCE-ONLY] | {MEDIUM or LOW} | {Rejected alternatives, adjudication rationale, measurement gaps} |
| {Dimension} | (same goal -- one per dimension) | {Signal 2: observable behavior} ({Leading/Lagging}) | {Metric name} | {Specific event or instrument} | {Target value} [REFERENCE-ONLY] | {MEDIUM or LOW} | |
```

### Metric Card Template

For each metric specified in the GSM worksheet, produce a metric card specification for the dashboard:

```markdown
### Metric Card: {Metric Name}

| Field | Value |
|-------|-------|
| **Metric Name** | {Display name} |
| **HEART Dimension** | {Happiness / Engagement / Adoption / Retention / Task Success} |
| **Current Value** | {Value with date range, or "Pending Baseline"} |
| **Target** | {Threshold value} [REFERENCE-ONLY] |
| **Trend** | {Visualization type: time series, bar chart, gauge, funnel} |
| **Alert Status** | {Normal / Warning / Critical} |
| **Drill-Down Path** | {What detail is accessible: segment breakdown, time range, funnel step} |
| **Refresh Frequency** | {Daily / Weekly / On survey collection cadence} |
| **Data Latency** | {Expected delay between user action and metric update} |
```

### Worked Examples

The following worked examples demonstrate a populated GSM worksheet row for each HEART dimension.

#### Happiness -- E-Commerce Post-Purchase Satisfaction

| HEART Dimension | Goal | Signal | Metric | Data Source | Threshold | Confidence | Notes |
|-----------------|------|--------|--------|-------------|-----------|------------|-------|
| Happiness | Users feel satisfied with their purchase experience | Post-purchase satisfaction survey response (Lagging) | Post-Purchase NPS | In-app NPS survey triggered after order confirmation (Reichheld, 2003) | >= 40 NPS [REFERENCE-ONLY] | LOW | Threshold based on Bain & Company / Reichheld (2003) e-commerce NPS benchmark. Rejected alternative: "Users feel confident in product selection" -- rejected (lifecycle alignment: mature product prioritizes overall satisfaction over decision confidence). |
| Happiness | (same goal) | Positive sentiment in support tickets (Leading) | Support Ticket Sentiment Ratio | NLP sentiment analysis on support ticket text | >= 70% positive [REFERENCE-ONLY] | LOW | Requires NLP sentiment tool instrumentation. |

#### Engagement -- SaaS Feature Depth

| HEART Dimension | Goal | Signal | Metric | Data Source | Threshold | Confidence | Notes |
|-----------------|------|--------|--------|-------------|-----------|------------|-------|
| Engagement | Users actively use core features beyond basic functionality | Number of distinct features used per session (Lagging) | Feature Breadth Score | Analytics event: `feature_used` with feature_name property | >= 3 features/session [REFERENCE-ONLY] | LOW | No published benchmark for feature breadth; threshold set via Fallback Step 3 (baseline + 15% improvement). |
| Engagement | (same goal) | Repeat visits within 7-day window (Leading) | 7-Day Return Rate | Analytics event: `session_start` with user_id | >= 60% [REFERENCE-ONLY] | LOW | Threshold requires 2-week baseline measurement (Fallback Step 2). |

#### Adoption -- Mobile App Onboarding

| HEART Dimension | Goal | Signal | Metric | Data Source | Threshold | Confidence | Notes |
|-----------------|------|--------|--------|-------------|-----------|------------|-------|
| Adoption | New users successfully complete onboarding and reach their first value moment | Onboarding flow completion (Lagging) | Onboarding Completion Rate | Analytics event: `onboarding_completed` / `onboarding_started` | >= 75% [REFERENCE-ONLY] | LOW | Threshold derived via Fallback Step 3: team-consensus estimate based on domain experience; no published onboarding completion benchmark available. Document as provisional -- revisit when real adoption data available after 2-week baseline (Fallback Step 2). |
| Adoption | (same goal) | First meaningful action after onboarding (Leading) | Time to First Value | Analytics event: `first_value_action` timestamp - `signup` timestamp | <= 5 minutes [REFERENCE-ONLY] | LOW | "First value action" must be defined per product context. |

#### Retention -- Subscription Product Monthly Return

| HEART Dimension | Goal | Signal | Metric | Data Source | Threshold | Confidence | Notes |
|-----------------|------|--------|--------|-------------|-----------|------------|-------|
| Retention | Users continue to find value and return to the product month over month | Active usage in consecutive 30-day periods (Lagging) | 30-Day Rolling Retention Rate | Analytics: count of users active in current 30-day window who were also active in prior 30-day window | >= 45% [REFERENCE-ONLY] | LOW | Threshold derived via Fallback Step 3: team-consensus estimate based on domain experience; no specific SaaS retention benchmark publication cited. Document as provisional -- calibrate against own baseline after 4-week measurement period (Fallback Step 4). |
| Retention | (same goal) | Engagement depth trend over time (Leading) | Session Frequency Trend | Analytics event: `session_start` count per user per week, 4-week rolling average | Non-declining trend [REFERENCE-ONLY] | LOW | Leading indicator: declining session frequency predicts churn. |

#### Task Success -- Checkout Flow Completion

| HEART Dimension | Goal | Signal | Metric | Data Source | Threshold | Confidence | Notes |
|-----------------|------|--------|--------|-------------|-----------|------------|-------|
| Task Success | Users complete the checkout process without encountering errors or needing help | Checkout completion without error display (Lagging) | Checkout Completion Rate | Analytics event: `checkout_completed` / `checkout_initiated` | >= 85% [REFERENCE-ONLY] | LOW | Baymard Institute e-commerce checkout usability benchmark (Baymard Institute, 2024); calibrate against own baseline. |
| Task Success | (same goal) | Time from cart to confirmation page (Leading) | Checkout Duration (p50) | Analytics: timestamp delta `checkout_initiated` to `checkout_completed` | <= 3 minutes (p50) [REFERENCE-ONLY] | LOW | Duration threshold derived from Fallback Step 3 (baseline + 15% improvement target). |

---

## Self-Review Checklist

Before persisting the HEART metrics output, the analyst MUST verify all items in this checklist (S-010, H-15).

| # | Check | Rule IDs | Rejection Criterion |
|---|-------|----------|---------------------|
| 1 | All 5 HEART dimensions assessed in the Dimension Selection table (included or excluded with rationale) | DS-001 through DS-006 | Any dimension missing from the selection table |
| 2 | Every selected dimension has a complete GSM table (Goal + 2-4 Signals + Metrics) | GD-001, SI-001, MS-001 | Incomplete GSM chain for any selected dimension |
| 3 | Every metric has all 8 specification fields populated | MS-002 | Any specification field missing or containing only placeholder text |
| 4 | Every threshold value tagged with `[REFERENCE-ONLY]` | CR-001, CR-004 | Any threshold value without the tag |
| 5 | Every threshold documents its Fallback Methodology step | MS-006 | Any threshold without derivation source |
| 6 | Goal-metric mappings classified as MEDIUM confidence; thresholds classified as LOW | CR-003 | Incorrect confidence classification |
| 7 | Navigation table present with all anchors resolving correctly | H-23 | Missing or broken navigation table |
| 8 | Measurement Plan mode disclosure present if analytics infrastructure is unavailable | MP-004, MP-005, MP-011 | Missing disclosure when no analytics infrastructure |
| 9 | Synthesis Judgments Summary lists each AI judgment call | Quality Gate Integration; `skills/user-experience/rules/synthesis-validation.md` | Missing or empty Synthesis Judgments Summary |
| 10 | Handoff data section populated for downstream sub-skill consumption | MP-010 | Missing or empty handoff data |
| 11 | Goal adjudication documented for any dimension where multiple goals were considered | GD-001 | Adjudication decisions undocumented |
| 12 | Signal-to-metric edge cases handled per [Signal-to-Metric Edge Cases](#signal-to-metric-edge-cases) rules | SE-001 through SE-010 | Fabricated signals (SE-005 violation) or undocumented measurement gaps |
| 13 | Dashboard specification includes metric cards, visualization types, drill-down paths, and refresh frequencies | DF-001 through DF-004, DL-001 through DL-004 | Incomplete dashboard specification |
| 14 | Workflow phases executed in correct order (Phase 1 through Phase 5) | WF-001, WF-002 | Any phase skipped or reordered |

---

## References

### Primary Methodology

| Citation Key | Full Reference |
|-------------|---------------|
| Rodden, Hutchinson & Fu, 2010 | Rodden, K., Hutchinson, H., & Fu, X. (2010). "Measuring the User Experience on a Large Scale: User-Centered Metrics for Web Applications." Proceedings of CHI '10, ACM. Primary source for the HEART framework and GSM process. |
| Reichheld, 2003 | Reichheld, F.F. (2003). "The One Number You Need to Grow." *Harvard Business Review*, 81(12), 46-54. Originally developed at Bain & Company with Satmetrix Systems. Source for Net Promoter Score (NPS) methodology and industry benchmarks. |
| Few, 2006 | Few, S. (2006). *Information Dashboard Design: The Effective Visual Communication of Data.* Analytics Press. Source for metric visualization best practices and dashboard layout principles. |
| Baymard Institute | Baymard Institute. "UX Benchmark" dataset (2020-2024). Available at https://baymard.com/ux-benchmark. Source for e-commerce checkout usability benchmarks including cart abandonment rates. Note: practitioners should verify current benchmark values against the latest dataset release. |

### Framework Standards

| Standard | Location |
|----------|----------|
| Quality Enforcement SSOT | `.context/rules/quality-enforcement.md` |
| Agent Development Standards (H-34) | `.context/rules/agent-development-standards.md` |
| Synthesis Validation Rules | `skills/user-experience/rules/synthesis-validation.md` |
| Agent Definition | `skills/ux-heart-metrics/agents/ux-heart-analyst.md` |
| Agent Governance | `skills/ux-heart-metrics/agents/ux-heart-analyst.governance.yaml` |
| Parent SKILL.md | `skills/ux-heart-metrics/SKILL.md` |
| Parent Skill | `skills/user-experience/SKILL.md` |

---

*Rule file: heart-methodology-rules.md*
*Version: 1.2.0*
*Parent sub-skill: /ux-heart-metrics*
*Parent skill: /user-experience*
*Agent: ux-heart-analyst*
*SSOT: `skills/ux-heart-metrics/SKILL.md`*
*Created: 2026-03-04*
*Revised: 2026-03-04*

<!-- Traceability: PROJ-022 EPIC-003, Wave 2. Standards: H-23 (navigation), H-34 (agent-dev), SR-002 (input validation), SR-003 (output filtering), H-13 (quality gate), H-15 (self-review). Methodology: Rodden, Hutchinson & Fu (2010), Reichheld (2003), Few (2006), Baymard Institute (2020-2024). ORCHESTRATION: projects/PROJ-022-user-experience-skill/orchestration/ux-skill-build-20260303-001/ORCHESTRATION.yaml -->
<!-- VERSION: 1.2.0 | DATE: 2026-03-04 | SOURCE: skills/ux-heart-metrics/SKILL.md, skills/ux-heart-metrics/agents/ux-heart-analyst.md, Rodden et al. (2010), Reichheld (2003), Few (2006), Baymard Institute (2020-2024) | REVISION: iter2 quality gate revisions (unnamed benchmark citations converted to Fallback Step 3, version alignment with SKILL.md, self-review item 9 fix, P-020 constitution path, MP-009 effort format) -->
