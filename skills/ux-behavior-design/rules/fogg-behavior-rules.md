<!-- VERSION: 1.2.0 | DATE: 2026-03-04 | SOURCE: skills/ux-behavior-design/SKILL.md (v1.5.0), skills/ux-behavior-design/agents/ux-behavior-diagnostician.md (v1.2.0), Fogg (2009) DOI:10.1145/1541948.1541999, Fogg (2020) | PARENT: /ux-behavior-design sub-skill | REVISION: iter3 — heart_metric_mapping→affected_heart_dimension alignment, Convergence alignment category added to Intervention Matrix, template version ref updated to v1.4.0 -->

# Fogg B=MAP Behavior Methodology Rules

> Operational constraints and methodology rules for the `ux-behavior-diagnostician` agent. Provides B=MAP convergence model enforcement, motivation analysis rules, ability analysis rules (six simplicity factors), prompt analysis rules, bottleneck identification algorithm, intervention design rules, severity classification, confidence classification, output format requirements, and quality gate integration that complement the agent definition.

## Document Sections

| Section | Purpose |
|---------|---------|
| [B=MAP Convergence Model Rules](#bmap-convergence-model-rules) | Core behavioral model: convergence framing, action threshold, factor independence |
| [Motivation Analysis Rules](#motivation-analysis-rules) | Three motivator pairs, intrinsic/extrinsic/social dimensions, 1-5 scale anchors |
| [Ability Analysis Rules](#ability-analysis-rules) | Six simplicity factors, limiting factor identification, friction scoring |
| [Prompt Analysis Rules](#prompt-analysis-rules) | Three prompt types, assessment dimensions, type-state matching |
| [Bottleneck Identification Algorithm](#bottleneck-identification-algorithm) | 4-step elimination: prompt, ability, motivation, multiple; convergence_timing edge case |
| [Intervention Design Rules](#intervention-design-rules) | By bottleneck type, effort-to-impact prioritization, LOW confidence mandate |
| [Severity Classification Rules](#severity-classification-rules) | Critical/Major/Moderate thresholds with heuristic rationale |
| [Confidence Classification Rules](#confidence-classification-rules) | MEDIUM for bottleneck diagnosis, LOW for intervention recommendations |
| [Output Format Rules](#output-format-rules) | Required sections per bmap-diagnosis-template.md |
| [Quality Gate Integration](#quality-gate-integration) | S-014 scoring dimensions, >= 0.95 C4 threshold |
| [Related Files](#related-files) | Dependency matrix: upstream, downstream, and sibling references |
| [Self-Review Checklist](#self-review-checklist) | S-010 verification before output persistence |

---

## B=MAP Convergence Model Rules

The Fogg Behavior Model states that behavior occurs when Motivation, Ability, and Prompt converge above their respective thresholds at the same moment (Fogg, 2009; Fogg, 2020). This is a convergence model, NOT a multiplication model. All three factors must be simultaneously sufficient for the behavior to occur.

> **Source:** Fogg, B.J. (2009). "A Behavior Model for Persuasive Design." *Proceedings of the 4th International Conference on Persuasive Technology.* DOI: 10.1145/1541948.1541999. Fogg, B.J. (2020). *Tiny Habits: The Small Changes That Change Everything.* Houghton Mifflin Harcourt.

### Convergence Principles

| Principle | Description | Implication |
|-----------|-------------|-------------|
| **Simultaneous sufficiency** | All three factors (M, A, P) must exceed their respective thresholds at the same moment | A user with maximum motivation and perfect ability will NOT act without a prompt |
| **Factor independence** | Each factor has its own threshold; factors do not compensate for each other | High motivation cannot overcome a missing prompt; a well-timed prompt cannot overcome impossible friction |
| **Action line** | The motivation-ability plane contains a curved action line; users above the line act when prompted | The prompt must arrive when the user's motivation-ability position is above the action line |
| **Threshold, not magnitude** | Factors must be above threshold, not maximized; over-investing in one factor while another is below threshold wastes effort | Diagnose which factor is below threshold before intervening |

### Convergence Discipline

| ID | Rule | Tier | Consequence of Violation |
|----|------|------|--------------------------|
| BMAP-001 | The B=MAP model MUST be described and applied as a convergence model. NEVER describe behavior as the "product" or "multiplication" of M, A, and P. | HARD | Multiplication framing implies factors compensate for each other, contradicting Fogg's convergence model (Fogg, 2009) |
| BMAP-002 | All three factors (Motivation, Ability, Prompt) MUST be assessed for every target behavior. NEVER omit a factor from the analysis. | HARD | Omitting a factor risks missing the actual bottleneck; the convergence model requires all three to be evaluated |
| BMAP-003 | Factor assessments MUST be independent. NEVER adjust one factor's score based on another factor's score. A high motivation score does NOT justify inflating the ability score. | HARD | Cross-factor contamination produces inaccurate bottleneck identification |
| BMAP-004 | The target behavior MUST be defined in Fogg's statement format: "After [CONTEXT], I will [SPECIFIC BEHAVIOR]" (Fogg, 2020, Chapters 14-15). Vague behavior descriptions ("users will engage more", "improve conversion") are REJECTED. | HARD | Vague behavior definitions prevent meaningful factor assessment; the diagnostician cannot assess ability for an undefined action |
| BMAP-005 | When evidence indicates all three factors are above threshold but behavior still does not occur, classify as `convergence_timing` and escalate to further investigation. NEVER force a bottleneck classification when the evidence does not support one. | HARD | Forced classification when all factors appear sufficient violates P-022; convergence timing issues require contextual investigation beyond B=MAP |

---

## Motivation Analysis Rules

Motivation in the Fogg model operates through three core motivator pairs. Each pair represents a spectrum from a positive to a negative pole (Fogg, 2009).

> **Source:** Fogg (2009), Section 3: "Core Motivators."

### Motivator Pair Definitions

| Motivator Pair | High End | Low End | Assessment Question |
|---------------|----------|---------|---------------------|
| **Sensation** | Pleasure | Pain | Does the action produce immediate pleasure or relieve pain? |
| **Anticipation** | Hope | Fear | Does the user hope for reward or fear consequence? |
| **Belonging** | Acceptance | Rejection | Does the action increase social standing or prevent exclusion? |

### Motivation Dimension Definitions

| Dimension | Definition | Assessment Question |
|-----------|-----------|---------------------|
| **Intrinsic** | Internal drives: satisfaction, curiosity, mastery, autonomy | Does the user have an internal desire to perform this action? |
| **Extrinsic** | External incentives: rewards, punishments, progress indicators | Are there external motivators encouraging or discouraging the action? |
| **Social** | Peer influence: competition, collaboration, recognition, social proof | Does peer behavior or social norms influence the user's willingness? |

### Motivation Scoring Scale (1-5)

| Score | Anchor | Interpretation |
|-------|--------|----------------|
| 1 | Absent | No evidence of motivation in this dimension; actively aversive |
| 2 | Weak | Minimal motivation; below the action threshold |
| 3 | Borderline | Moderate motivation; at threshold; investigate further |
| 4 | Present | Clear motivation signals above threshold |
| 5 | Strong | Multiple converging evidence points for strong motivation |

### Motivation Discipline

| ID | Rule | Tier | Consequence of Violation |
|----|------|------|--------------------------|
| MOT-001 | All three motivator pairs (Sensation, Anticipation, Belonging) MUST be assessed with individual scores. No pair may remain unassessed. | HARD | Incomplete motivator pair coverage misses motivation bottleneck dimensions |
| MOT-002 | All three motivation dimensions (intrinsic, extrinsic, social) MUST be assessed with individual scores (1-5). | HARD | Dimension-level assessment is required for targeted intervention design |
| MOT-003 | Every motivation score MUST cite specific evidence or be explicitly marked as inferred. Scores without evidence or inference marking are REJECTED. | HARD | Unsupported scores violate P-001 (truth and accuracy) and prevent downstream validation |
| MOT-004 | When uncertain between two adjacent scores, MUST choose the LOWER score. Over-estimating motivation leads to missed bottlenecks (P-022). | HARD | Optimistic scoring masks motivation problems; the convergent elimination algorithm depends on accurate scores |
| MOT-005 | Motivation scores MUST NOT exceed 3 when the only evidence is team assumptions or general UX principles. Scores of 4-5 require direct evidence (analytics, user research, interview data). Source: P-001 (truth and accuracy); Fogg (2020) evidence-based scoring principle. | HARD | Prevents inflation of motivation scores from weak evidence; unsupported high scores violate P-001 and produce inaccurate bottleneck identification |
| MOT-006 | The overall motivation assessment MUST state whether motivation is "above threshold" or "below threshold" based on the dimension scores. Majority of dimensions at 1-2 indicates below threshold. | MEDIUM | Explicit threshold judgment is required for the elimination algorithm (Step 3) |

---

## Ability Analysis Rules

Ability in the Fogg model is inversely related to simplicity. The six simplicity factors represent distinct dimensions of friction (Fogg, 2009).

> **Source:** Fogg (2009), Section 4: "Simplicity as a Function of a Person's Scarcest Resource."

### Six Simplicity Factor Definitions

| Factor | Definition | Assessment Question | Example Friction |
|--------|-----------|---------------------|------------------|
| **Time** | How long the behavior takes | Does the action take more time than the user is willing to spend? | 12-field form when user expects 3 fields |
| **Money** | Financial cost of the behavior | Does the action require more money than expected? | Surprise shipping costs at checkout |
| **Physical Effort** | Bodily exertion required | Does the action require more physical effort than the user will expend? | Requiring camera access, photo upload, manual data entry on mobile |
| **Brain Cycles** | Cognitive load required | Does the action require more thinking than the user will invest? | Complex pricing tiers; unfamiliar terminology |
| **Social Deviance** | Social norm violation | Does the action require socially unacceptable behavior? | Publicly sharing salary; requesting social media permissions |
| **Non-Routine** | Habit departure | Does the action require changing an existing habit? | Switching from email to unfamiliar dashboard |

### Ability Scoring Scale (1-5)

| Score | Anchor | Interpretation |
|-------|--------|----------------|
| 1 | Extremely difficult | This factor creates severe friction; users cannot reasonably overcome it |
| 2 | Difficult | High friction; this factor is likely contributing to the bottleneck |
| 3 | Moderate | Borderline friction; warrants investigation |
| 4 | Easy | Low friction; this factor is not the primary obstacle |
| 5 | Trivial | Negligible friction; factor does not impede the behavior |

### Limiting Factor Principle

Per Fogg (2009), ability is governed by the scarcest resource at the moment of the prompt. The limiting simplicity factor is the factor with the lowest score. Improving any factor except the limiting one does not raise overall ability above the action threshold.

### Ability Discipline

| ID | Rule | Tier | Consequence of Violation |
|----|------|------|--------------------------|
| ABL-001 | All six simplicity factors MUST be assessed with individual scores (1-5). No factor may remain unassessed. | HARD | Incomplete factor coverage may miss the limiting factor |
| ABL-002 | The limiting simplicity factor (lowest-scoring among six) MUST be explicitly identified and documented. | HARD | The elimination algorithm (Step 2) requires the limiting factor for bottleneck diagnosis |
| ABL-003 | Every ability score MUST cite specific evidence or be explicitly marked as inferred. Scores without evidence or inference marking are REJECTED. | HARD | Unsupported scores violate P-001 and prevent downstream validation |
| ABL-004 | When uncertain between two adjacent scores, MUST choose the LOWER score. Over-estimating ability leads to missed friction bottlenecks (P-022). | HARD | Optimistic scoring masks ability problems |
| ABL-005 | When operating in Qualitative Assessment Mode (no quantitative data), ability scores MUST be disclosed as estimates based on interface artifact inspection, not measured user performance. | HARD | Undisclosed estimation accuracy violates P-022 |
| ABL-006 | The overall ability assessment MUST state whether ability is "above threshold" or "below threshold." A limiting factor score of 1-2 indicates below threshold. | MEDIUM | Explicit threshold judgment is required for the elimination algorithm (Step 2) |
| ABL-007 | For ability bottlenecks, the intervention MUST target the specific limiting simplicity factor, not ability in general. | HARD | Generic ability interventions may address non-limiting factors, wasting effort |

---

## Prompt Analysis Rules

Prompts are triggers that call users to action. The Fogg model identifies three prompt types, each appropriate for a specific motivation-ability state (Fogg, 2009).

> **Source:** Fogg (2009), Section 5: "Triggers."

### Prompt Type Definitions

| Prompt Type | User State | Mechanism | Design Implication |
|-------------|-----------|-----------|-------------------|
| **Spark** | High ability, low motivation | Triggers motivation (emotional appeal, social proof, fear of missing out) | User can do the action but needs a reason |
| **Facilitator** | High motivation, low ability | Reduces friction (pre-filled forms, one-click actions, simplified steps) | User wants to act but the action is too hard |
| **Signal** | High motivation, high ability | Simple reminder or notification (bell icon, push notification, calendar reminder) | User is both willing and able; needs a timely nudge |

### Prompt Assessment Dimensions

| Dimension | Values | Assessment Criterion |
|-----------|--------|---------------------|
| **Type match** | Appropriate / Mismatched / Absent | Is the prompt type correct for the user's motivation-ability state? |
| **Timing** | Appropriate / Mistimed / Absent | Does the prompt arrive when the user is ready to act? |
| **Placement** | Visible / Hidden / Competing | Is the prompt noticeable and actionable when it fires? |

### Prompt Discipline

| ID | Rule | Tier | Consequence of Violation |
|----|------|------|--------------------------|
| PRM-001 | Every prompt analysis MUST assess all three dimensions: type match, timing, and placement. | HARD | Incomplete prompt assessment misses prompt-related bottlenecks |
| PRM-002 | When no prompt exists for the target behavior, the type MUST be recorded as "Absent" and the prompt is classified as the primary bottleneck at Step 1 of the elimination algorithm. | HARD | An absent prompt means zero behavior regardless of motivation and ability (Fogg, 2020) |
| PRM-003 | The prompt type MUST be evaluated against the user's assessed motivation-ability state. A signal prompt for a low-motivation user is a type mismatch (should be a spark). A signal prompt for a low-ability user is a type mismatch (should be a facilitator). | HARD | Type-state mismatch means the prompt fails to address the user's actual constraint |
| PRM-004 | Prompt timing SHOULD be assessed relative to the moment when the user's motivation-ability position is above the action line. A prompt that arrives before the user has sufficient motivation or after the user has moved on is mistimed (Fogg, 2009, Section 5). | MEDIUM | Timing assessment without action-line reference misses the core B=MAP insight that prompts only trigger behavior when the user is above the action line |
| PRM-005 | When multiple prompts compete for attention at the same interaction point, placement MUST be classified as "Competing" and the dilution effect documented. | MEDIUM | Competing prompts reduce the effectiveness of each individual prompt |

---

## Bottleneck Identification Algorithm

The elimination algorithm tests factors in order of intervention difficulty (cheapest to hardest), halting at the first factor that fails (Fogg, 2020). This ordering prevents the divergent trap of investigating all factors equally when one is clearly the limiting constraint.

> **Source:** Fogg (2020), Chapters 2-3: intervention difficulty ordering. Fogg (2009): action threshold and factor convergence.

### 4-Step Elimination Procedure

**Step 1: Prompt Assessment (cheapest fix first)**
- Is the prompt present? If absent -> HALT: prompt is the primary bottleneck.
- Is the prompt correctly timed? If mistimed -> HALT: prompt is the primary bottleneck.
- Is the prompt type appropriate for the user's motivation-ability state? If mismatched -> HALT: prompt is the primary bottleneck.
- If prompt is present, timed, and type-appropriate -> PASS; proceed to Step 2.

**Step 2: Ability Assessment (most common bottleneck)**
- Identify the limiting simplicity factor (lowest-scoring among six).
- Limiting factor scores 1-2 -> HALT: ability is the primary bottleneck. Record the specific limiting factor and evidence chain.
- All factors score 3+ -> PASS; proceed to Step 3.

**Step 3: Motivation Assessment (hardest to change)**
- Majority of motivation dimensions score 1-2 -> HALT: motivation is the primary bottleneck. Record the specific dimensions below threshold and evidence.
- Motivation above threshold -> PASS; proceed to Step 4.

**Step 4: Multiple Bottleneck Assessment**
- Two or more factors at borderline (score 3) with none clearly below threshold -> classify as `multiple` bottleneck requiring coordinated interventions. Document which factors are borderline and recommend addressing the factor with the cheapest intervention first.
- **Edge case (convergence_timing):** If all factors score 4+ and behavior still does not occur, classify as `convergence_timing`. This indicates an external constraint not captured in the B=MAP model (e.g., environmental context, habit inertia, emotional state per Fogg, 2009). Escalate to further contextual investigation with the orchestrator.

### Algorithm Discipline

| ID | Rule | Tier | Consequence of Violation |
|----|------|------|--------------------------|
| ALG-001 | The elimination algorithm MUST execute steps in order (1 through 4). NEVER skip a step. NEVER reorder steps. | HARD | The ordering follows Fogg's intervention difficulty gradient; reordering biases toward harder interventions |
| ALG-002 | The algorithm MUST halt at the first step that fails. If Step 1 identifies a prompt bottleneck, Steps 2-4 do NOT execute as primary bottleneck identification (they MAY be noted as secondary observations). | HARD | Continuing past a clear bottleneck diffuses the diagnosis; the convergent approach requires a single primary finding |
| ALG-003 | Every step MUST record its result (Pass/Fail) with supporting evidence in the Elimination Algorithm Trace table. | HARD | The trace provides the evidence chain for the bottleneck classification and enables downstream review |
| ALG-004 | The `convergence_timing` classification MUST only be assigned when all three factors score 4+ AND the behavior does not occur. NEVER use `convergence_timing` as a default when the analysis is inconclusive. | HARD | `convergence_timing` indicates a genuine model boundary; using it as a fallback masks incomplete analysis |
| ALG-005 | For `multiple` bottleneck classification, the diagnosis MUST specify which factors are borderline and recommend addressing the cheapest-to-fix factor first. | MEDIUM | Unordered multiple bottleneck recommendations leave teams without a starting point |

---

## Intervention Design Rules

Interventions are targeted recommendations addressing the diagnosed bottleneck. All interventions are classified as LOW confidence because effectiveness depends on context-specific factors that analysis cannot capture (Fogg, 2020).

> **Source:** Fogg (2020), Chapters 2-3, 14-15: intervention categories aligned with bottleneck factors. Effort-to-impact prioritization derived from Fogg's intervention difficulty gradient.

### Intervention Category Matrix

| Bottleneck | Intervention Category | Example Interventions | Typical Effort |
|-----------|----------------------|----------------------|----------------|
| Prompt | Add, reposition, or retype the prompt | Add CTA where none exists; move above fold; change signal to spark | Low |
| Ability (Time) | Reduce time required | Pre-fill fields; reduce steps; add progress indicators | Low-Medium |
| Ability (Money) | Reduce or clarify cost | Show total upfront; offer free tier; defer payment | Medium |
| Ability (Physical Effort) | Reduce physical actions | Add autofill; one-click actions; optimize for mobile | Low-Medium |
| Ability (Brain Cycles) | Reduce cognitive load | Simplify language; add defaults; reduce choices | Medium |
| Ability (Social Deviance) | Normalize the behavior | Add social proof; anonymization options; privacy controls | Medium |
| Ability (Non-Routine) | Reduce habit disruption | Map to existing workflows; familiar UI patterns | Medium-High |
| Motivation | Increase motivation via design | Social proof; gamification; loss aversion; progress visualization | High |
| Convergence timing | Convergence alignment | Contextual trigger timing adjustment; habit stacking to co-locate prompt with existing behavior; environmental context redesign to synchronize M, A, and P above threshold simultaneously (Fogg, 2009) | Medium-High |
| Multiple | Coordinated multi-factor | Address lowest-scoring factor first; combine prompt redesign with simplification | High |

### Intervention Discipline

| ID | Rule | Tier | Consequence of Violation |
|----|------|------|--------------------------|
| INT-001 | Every diagnosis MUST produce 3-5 specific intervention recommendations. Fewer than 3 limits options; more than 5 diffuses focus. | HARD | Insufficient interventions leave teams without actionable alternatives; excessive interventions dilute priority signal |
| INT-002 | Every intervention MUST include: description, target factor, expected impact (High/Medium/Low), implementation effort (Low/Medium/High), classification (Direct/Supporting), and supporting reasoning. | HARD | Incomplete intervention entries are not actionable |
| INT-003 | Interventions MUST be prioritized by effort-to-impact ratio: low-effort, high-impact first. Prompt interventions before ability interventions before motivation interventions per Fogg's difficulty gradient (Fogg, 2020). | HARD | Unprioritized interventions lead teams to attempt the hardest fix first |
| INT-004 | ALL intervention recommendations MUST be marked with LOW synthesis confidence. Intervention effectiveness depends on context-specific factors that analysis cannot capture. | HARD | Presenting interventions without LOW confidence violates P-022; users may over-commit to untested recommendations |
| INT-005 | For ability bottlenecks, at least one intervention MUST target the specific limiting simplicity factor identified in the ability assessment. Generic ability interventions are insufficient. | HARD | Targeting a non-limiting factor wastes effort; only the limiting factor constrains overall ability |
| INT-006 | Each intervention MUST be classified as "Direct" (addresses the primary bottleneck factor) or "Supporting" (reinforces the primary intervention). At least one intervention MUST be Direct. | MEDIUM | Classification helps teams distinguish primary from secondary actions |
| INT-007 | The intervention section MUST include the REFERENCE-ONLY banner: "Intervention recommendations are directional based on B=MAP analysis. Effectiveness requires validation through user testing or A/B experimentation." | HARD | Omitting the banner understates the speculative nature of interventions |

---

## Severity Classification Rules

Bottleneck severity quantifies the impact of the diagnosed behavioral constraint. The classification uses three levels (Critical, Major, Moderate). There is no Minor classification -- if the behavior occurs more than half the expected rate, the B=MAP factors are likely above threshold and a formal bottleneck diagnosis is not warranted.

> **Source:** Severity thresholds are framework-internal heuristics derived from conversion rate analysis patterns. The 10% and 50% thresholds are calibration anchors for the /user-experience skill's target audience (tiny teams, 1-5 people).

### Severity Definitions

| Severity | Criterion | Interpretation |
|----------|-----------|----------------|
| **Critical** | Target behavior never occurs (zero conversion, or effectively zero) | Complete bottleneck: one or more B=MAP factors are entirely absent or fundamentally below threshold |
| **Major** | Conversion below 10% of the expected rate | Severe bottleneck: the primary factor is well below threshold; secondary factors may also be borderline |
| **Moderate** | Conversion between 10-50% of the expected rate | Significant bottleneck: the primary factor is below threshold but not absent; improvement is achievable |

### Severity Discipline

| ID | Rule | Tier | Consequence of Violation |
|----|------|------|--------------------------|
| SEV-001 | Every bottleneck diagnosis MUST include a severity classification (Critical, Major, or Moderate). | HARD | Severity omission prevents prioritization of behavioral issues |
| SEV-002 | Severity MUST be based on the conversion rate relative to the expected rate. When no expected rate is available, severity MUST be estimated from the factor scores and explicitly marked as estimated. | HARD | Severity without basis is unactionable; marking estimates complies with P-022 |
| SEV-003 | When operating in Qualitative Assessment Mode (no conversion data), severity SHOULD be derived from factor score patterns: all factors at 1-2 indicates Critical; limiting factor at 1-2 with others at 3+ indicates Major; multiple factors at 3 indicates Moderate. | MEDIUM | Inconsistent severity classification when operating qualitatively; teams cannot prioritize behavioral issues without a systematic severity estimate |

---

## Confidence Classification Rules

Every AI-generated judgment in the diagnosis output requires a confidence classification. These rules govern classification criteria and synthesis gate compliance.

> **Source:** `skills/user-experience/rules/synthesis-validation.md` (v1.1.0) Section "Confidence Classification" and Section "Sub-Skill Synthesis Output Map."

### Classification Criteria

| Classification | Criteria | Action | Example |
|---------------|----------|--------|---------|
| **HIGH** | Multiple data sources converge; validated by quantitative behavioral data AND qualitative evidence | Proceed with recommendation | Bottleneck diagnosis supported by funnel analytics + session recordings + user interview data |
| **MEDIUM** | Single-framework reasoning; B=MAP assessment based on available evidence without full empirical validation | Include "Validation Required" note | Bottleneck diagnosis from interface artifact analysis and partial behavioral data |
| **LOW** | Insufficient data; AI inference without empirical grounding; speculative assessment | Flag for human review before acting | Intervention recommendation based on diagnosed bottleneck without user testing |

### Judgment Types Requiring Classification

| Judgment Type | Description | Typical Confidence |
|---------------|-------------|-------------------|
| Target behavior scoping | Defining the behavior statement and observation scope | MEDIUM (depends on clarity of provided context) |
| Motivation dimension rating | Assessing intrinsic, extrinsic, social motivation on 1-5 scale | MEDIUM (B=MAP framework provides structure but rating involves interpretive judgment) |
| Motivator pair rating | Assessing Sensation, Anticipation, Belonging pairs | MEDIUM (pair assessment depends on available evidence quality) |
| Simplicity factor rating | Assessing each of the six ability factors on 1-5 scale | MEDIUM (interface inspection provides observable evidence; MEDIUM rather than HIGH because user perception may differ from inspected friction) |
| Limiting factor identification | Selecting the lowest-scoring simplicity factor | MEDIUM (deterministic within the scoring; confidence inherited from factor rating confidence) |
| Prompt type classification | Classifying prompt as Spark/Facilitator/Signal/Absent | MEDIUM (observable from interface artifacts when prompt exists) |
| Bottleneck classification | Identifying the primary bottleneck factor via elimination algorithm | MEDIUM (structured algorithm constrains interpretive variance; evidence-dependent) |
| Severity assignment | Classifying as Critical/Major/Moderate | MEDIUM when conversion data available; LOW when estimated from factor scores |
| Intervention recommendation | Specific intervention targeting diagnosed bottleneck | LOW (effectiveness depends on context-specific factors AI cannot capture) |
| Intervention prioritization | Ordering interventions by effort-to-impact ratio | LOW (effort and impact estimates are speculative without implementation context) |

### Behavior Design Confidence Dynamics

Behavior Design outputs follow a predictable confidence pattern because the B=MAP model structures the diagnosis but cannot replace empirical observation of actual user behavior:

- **Pre-intervention outputs** (factor assessments, bottleneck diagnosis, severity classification) are inherently MEDIUM -- the B=MAP framework provides structured analysis but factor ratings involve interpretive judgment
- **Intervention outputs** (specific recommendations, prioritization) are inherently LOW -- intervention effectiveness depends on implementation context, user segment specifics, and factors not observable in the analysis
- **Post-validation outputs** (if follow-up data is provided) may reach HIGH when the diagnosis converges with `/ux-heart-metrics` quantitative measurement

### Classification Discipline

| ID | Rule | Tier | Consequence of Violation |
|----|------|------|--------------------------|
| CLS-001 | Every AI judgment call in the Synthesis Judgments Summary MUST include a confidence classification (HIGH, MEDIUM, or LOW) and a one-line rationale. | HARD | Judgment calls without confidence classification cannot be validated by the downstream synthesis pipeline; P-022 violation |
| CLS-002 | NEVER classify an intervention recommendation as MEDIUM or HIGH. All intervention recommendations are LOW because effectiveness requires empirical validation. | HARD | Intervention classified MEDIUM/HIGH misleads teams into false confidence; intervention effectiveness requires empirical validation |
| CLS-003 | NEVER classify a factor rating as HIGH when the only evidence is interface artifact inspection or team-provided descriptions. HIGH requires quantitative behavioral data (analytics, session recordings, A/B test results) converging with qualitative evidence. | HARD | HIGH classification without quantitative data overstates certainty of factor rating; P-022 violation |
| CLS-004 | The minimum-confidence rule applies: when a single finding draws from multiple judgment types with different confidence levels, the finding's confidence is the LOWEST among all contributing judgments. Source: `skills/user-experience/rules/synthesis-validation.md` (v1.1.0) minimum-confidence aggregation rule. | HARD | Selecting a higher-than-minimum confidence for a composite finding overstates certainty; downstream synthesis inherits inflated confidence, masking data quality gaps |
| CLS-005 | Severity assignments based on estimated factor scores (no conversion data) MUST be classified as LOW, not MEDIUM. Only severity assignments based on actual conversion data qualify for MEDIUM. | HARD | Estimated severity at MEDIUM implies empirical grounding that does not exist; teams may over-commit resources to a severity level that is speculative |

---

## Output Format Rules

The diagnostician's output MUST follow the structure defined in `skills/ux-behavior-design/templates/bmap-diagnosis-template.md`. These rules enforce section completeness and format compliance.

> **Source:** `skills/ux-behavior-design/templates/bmap-diagnosis-template.md` (v1.4.0), SKILL.md [Output Specification].

### Required Sections

| Section | Level | Completeness Criteria |
|---------|-------|-----------------------|
| **Executive Summary** | L0 | Primary bottleneck factor stated; severity stated; top intervention described; 3-5 key findings listed |
| **Engagement Context** | L1 | Product name, target users, target behavior in Fogg format, observation scope, upstream inputs table, evidence inventory table, wave entry verification |
| **Behavior State Map** | L1 | Motivation table (3 pairs + 3 dimensions with scores and evidence); ability table (6 factors with scores, evidence, limiting marker); prompt table (type, timing, placement, match); action-line position |
| **Bottleneck Diagnosis** | L1 | Elimination algorithm trace (4 steps with Pass/Fail and evidence); primary bottleneck stated; severity stated; confidence with rationale |
| **Intervention Recommendations** | L1 | REFERENCE-ONLY banner; 3-5 interventions each with description, target factor, category, impact, effort, classification |
| **Strategic Implications** | L2 | Behavioral pattern analysis; systemic bottleneck trends; behavior design maturity; behavior change roadmap |
| **Synthesis Judgments Summary** | L1 | Every AI judgment call listed with classification type, confidence level, and rationale |
| **Handoff Data** | L1 | YAML block with from_agent, to_agent, task, success_criteria, artifacts, key_findings, confidence, criticality, ux_ext (bottleneck_factor, severity, affected_heart_dimension) |

### Output Format Discipline

| ID | Rule | Tier | Consequence of Violation |
|----|------|------|--------------------------|
| OUT-001 | All 8 required sections MUST be present in the output. Missing sections trigger self-review rejection. | HARD | Incomplete output fails the Completeness dimension of the quality gate |
| OUT-002 | The navigation table (H-23) MUST be present with anchor links to all 8 sections. | HARD | Missing navigation violates H-23; document rejected |
| OUT-003 | The Executive Summary MUST contain exactly 3-5 key findings bullets. Fewer than 3 is insufficient for cross-framework synthesis; more than 5 dilutes the summary. | MEDIUM | Cross-framework synthesis receives insufficient orientation data |
| OUT-004 | The Behavior State Map MUST include all scoring tables: motivation pairs (3 rows), motivation dimensions (3 rows), simplicity factors (6 rows), prompt assessment (4 rows), AND an explicit action-line position statement describing whether the user is above or below the action line and which factor(s) need to change. | HARD | Missing scoring tables or action-line position leaves the B=MAP assessment incomplete; downstream bottleneck diagnosis cannot execute without full factor data |
| OUT-005 | The Elimination Algorithm Trace MUST show all 4 steps (including Steps 3-4 as N/A if the algorithm halted earlier). | HARD | Omitted steps break the evidence chain for bottleneck classification; reviewers cannot verify the diagnosis |
| OUT-006 | The Handoff Data YAML MUST conform to `docs/schemas/handoff-v2.schema.json` and include the `ux_ext` extension fields for downstream `/ux-heart-metrics` consumption. | HARD | Non-conforming handoff data rejected by downstream `/ux-heart-metrics` agent |
| OUT-007 | When operating in Qualitative Assessment Mode, the degraded mode disclosure banner MUST appear immediately after the document header. | HARD | Undisclosed degraded mode violates P-022; Evidence Quality dimension receives a 0 score per QG-003 |

---

## Quality Gate Integration

Behavior Design facilitation output maps to the S-014 LLM-as-Judge rubric dimensions (`.context/rules/quality-enforcement.md` Section "Quality Gate") as follows:

### Dimension Mapping

| S-014 Dimension | Weight | Behavior Design Evaluation Criteria |
|-----------------|--------|-------------------------------------|
| **Completeness** | 0.20 | All 5 phases addressed; all 3 B=MAP factors assessed; all 3 motivator pairs and 3 dimensions rated; all 6 simplicity factors rated with limiting factor identified; prompt assessed on all 3 dimensions; elimination algorithm trace complete; 3-5 interventions produced; handoff data populated |
| **Internal Consistency** | 0.20 | Factor scores align with threshold judgments (above/below); bottleneck classification consistent with elimination algorithm trace; intervention target factor matches diagnosed bottleneck; severity consistent with conversion evidence; prompt type-state match consistent with motivation and ability scores |
| **Methodological Rigor** | 0.20 | B=MAP convergence model applied (not multiplication); Fogg's statement format used for target behavior; elimination algorithm executed in correct order (prompt -> ability -> motivation -> multiple); scoring scales anchored correctly; Fogg citations present for methodology claims |
| **Evidence Quality** | 0.15 | Every factor score cites specific evidence or marks inference explicitly; evidence quality classification (strong/moderate/weak) applied to behavioral data; no fabricated evidence; degraded mode disclosed when operating without quantitative data |
| **Actionability** | 0.15 | Interventions include effort and impact estimates; interventions prioritized by effort-to-impact; at least one intervention is Direct (addresses primary bottleneck); interventions target specific limiting factor (not generic); intervention section includes REFERENCE-ONLY banner |
| **Traceability** | 0.10 | Target behavior traces to engagement context; each factor score traces to cited evidence; bottleneck classification traces to elimination algorithm step; each intervention traces to diagnosed bottleneck factor; methodology claims cite Fogg (2009) or Fogg (2020); upstream heuristic findings cited where used |

### Scoring Discipline for Behavior Design

| ID | Rule | Tier | Consequence of Violation |
|----|------|------|--------------------------|
| QG-001 | The quality gate threshold applies to the overall diagnosis report, not to individual factor assessments or interventions. Baseline threshold: >= 0.92 (H-13 per `.context/rules/quality-enforcement.md` Section "Quality Gate", C2+). At C4 criticality (e.g., user-specified or auto-escalated per AE-002/AE-004), the threshold is >= 0.95 (governance source: PROJ-022 ORCHESTRATION.yaml C4 scoring specification). | HARD | Deliverable rejected per H-13; revision required |
| QG-002 | Completeness scoring MUST verify all three B=MAP factors are assessed. An output missing any factor receives a 0 on the Completeness dimension. | HARD | Completeness dimension zeroed; composite score drops below threshold |
| QG-003 | Evidence Quality scoring MUST penalize undisclosed degraded mode operation. If the agent operated in Qualitative Assessment Mode without the P-022 degraded mode banner, Evidence Quality receives a 0 score. | HARD | Evidence Quality dimension zeroed; P-022 violation |
| QG-004 | Internal Consistency scoring MUST verify that the bottleneck classification is logically consistent with the elimination algorithm trace. A classification of "ability" with a Step 2 result of "Pass" is a consistency failure. | HARD | Internal Consistency dimension penalized; logically inconsistent diagnoses cannot be trusted for downstream intervention design |

---

## Related Files

> Dependency matrix for operational traceability. Upstream files provide inputs or prerequisites; downstream files consume this rules file's outputs; sibling files share the same parent sub-skill.

| Relationship | File | Version | Purpose |
|-------------|------|---------|---------|
| **Parent SKILL.md** | `skills/ux-behavior-design/SKILL.md` | v1.5.0 | Sub-skill definition; methodology overview; agent routing |
| **Agent definition** | `skills/ux-behavior-design/agents/ux-behavior-diagnostician.md` | v1.2.0 | Agent frontmatter, system prompt, output section (handoff threshold) |
| **Governance YAML** | `skills/ux-behavior-design/agents/ux-behavior-diagnostician.governance.yaml` | v1.2.0 | Enforcement metadata: quality_threshold (0.95), quality_gate (S-014) |
| **Output template** | `skills/ux-behavior-design/templates/bmap-diagnosis-template.md` | v1.4.0 | Report template consumed by diagnostician agent |
| **Wave progression** | `skills/user-experience/rules/wave-progression.md` | v1.2.0 | Wave 4 (Advanced Analytics) entry conditions; Wave 3 completion is a prerequisite |
| **Synthesis validation** | `skills/user-experience/rules/synthesis-validation.md` | v1.1.0 | Confidence classification shared taxonomy; Sub-Skill Synthesis Output Map |
| **MCP coordination** | `skills/user-experience/rules/mcp-coordination.md` | unversioned -- tracked via git history | MCP integration; degraded-mode disclosure requirements |
| **Quality enforcement** | `.context/rules/quality-enforcement.md` | SSOT -- version tracked externally (v1.6.0 at time of writing) | S-014 dimension rubric; H-13 quality gate threshold (>= 0.92 baseline, >= 0.95 at C4) |

> **Wave 3 prerequisite:** This rules file governs agent behavior in Wave 4 (Advanced Analytics). Per `wave-progression.md`, Wave 3 (Design System) completion is required before Behavior Design executes, unless the bypass condition is met (existing user base with analytics data).

---

## Self-Review Checklist

Before persisting the report, the diagnostician MUST verify (S-010, H-15):

| # | Check | Rule Reference |
|---|-------|---------------|
| 1 | Target behavior is defined in Fogg's statement format: "After [CONTEXT], I will [SPECIFIC BEHAVIOR]" | BMAP-004 |
| 2 | B=MAP convergence framing used (NOT multiplication) | BMAP-001 |
| 3 | All three B=MAP factors assessed (motivation, ability, prompt) -- none omitted | BMAP-002 |
| 4 | Motivation assessment covers all three motivator pairs (Sensation, Anticipation, Belonging) with scores and evidence | MOT-001 |
| 5 | Motivation assessment covers all three dimensions (intrinsic, extrinsic, social) with scores and evidence | MOT-002 |
| 6 | Ability assessment covers all six simplicity factors with scores and evidence | ABL-001 |
| 7 | Limiting simplicity factor explicitly identified | ABL-002 |
| 8 | Prompt assessment includes type, timing, placement, and match to user state | PRM-001 |
| 9 | Elimination algorithm trace shows all 4 steps with Pass/Fail results and evidence | ALG-001, ALG-003 |
| 10 | Algorithm halted at first failing step (secondary observations noted separately if present) | ALG-002 |
| 11 | Bottleneck severity classified (Critical/Major/Moderate) | SEV-001 |
| 12 | Interventions (3-5) are prioritized by effort-to-impact with ALL marked LOW confidence | INT-001, INT-003, INT-004 |
| 13 | At least one intervention targets the specific limiting factor (for ability bottlenecks) | INT-005 |
| 14 | REFERENCE-ONLY banner present in intervention section | INT-007 |
| 15 | Synthesis Judgments Summary lists every AI judgment call with confidence classification | CLS-001 |
| 16 | Navigation table present with correct anchor links (H-23) | H-23 |
| 17 | Degraded mode disclosure present if operating without quantitative behavioral data | P-022, ABL-005 |
| 18 | Handoff data section populated for `/ux-heart-metrics` downstream consumption | OUT-006 |

---

*Rule file: fogg-behavior-rules.md*
*Version: 1.2.0*
*Parent sub-skill: /ux-behavior-design*
*Parent skill: /user-experience*
*Agent: ux-behavior-diagnostician*
*SSOT: `skills/ux-behavior-design/SKILL.md` (v1.5.0)*
*Created: 2026-03-04*
*Revised: 2026-03-04 (iter3 -- 3 cross-file consistency fixes per template-iter2-score.md)*

<!-- Traceability: PROJ-022 EPIC-004. Standards: H-23 (navigation), H-34 (agent-dev), H-13 (quality gate), SR-002 (input validation), SR-003 (output filtering). Methodology: Fogg, B.J. (2009) DOI:10.1145/1541948.1541999, Fogg, B.J. (2020) "Tiny Habits." Synthesis validation: skills/user-experience/rules/synthesis-validation.md. Quality gate: .context/rules/quality-enforcement.md. ORCHESTRATION: projects/PROJ-022-user-experience-skill/orchestration/ux-skill-build-20260303-001/ORCHESTRATION.yaml -->
<!-- VERSION: 1.2.0 | DATE: 2026-03-04 | SOURCE: skills/ux-behavior-design/SKILL.md (v1.5.0), skills/ux-behavior-design/agents/ux-behavior-diagnostician.md (v1.2.0), Fogg (2009) DOI:10.1145/1541948.1541999, Fogg (2020) "Tiny Habits" | REVISION: iter3 — 3 cross-file consistency fixes per template-iter2-score.md -->
