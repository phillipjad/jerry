<!-- VERSION: 1.2.0 | DATE: 2026-03-04 | SOURCE: skills/ux-kano-model/SKILL.md (v1.2.0), skills/ux-kano-model/agents/ux-kano-analyst.md | PARENT: /ux-kano-model sub-skill | REVISION: iter3 -- SQD-006 primacy/recency citation (Krosnick & Presser, 2010), LCY-004 section-level Matzler & Hinterhuber (1998) citation, SQD-007 respondent selection criteria, SPL-006 framework-internal convention label precision -->

# Kano Methodology Rules

> Operational constraints and methodology rules for the `ux-kano-analyst` agent. Provides 5x5 evaluation table enforcement, CS coefficient calculation discipline, sample size calibration, split detection, feature lifecycle assessment, priority matrix construction, confidence classification, and quality gate integration that complement the agent definition.

## Document Sections

| Section | Purpose |
|---------|---------|
| [Survey Question Design Rules](#survey-question-design-rules) | Functional/dysfunctional question pair format, language, completeness, partial-response handling |
| [5x5 Evaluation Table Rules](#5x5-evaluation-table-rules) | Functional x dysfunctional mapping to M/O/A/I/R/Q categories |
| [CS Coefficient Calculation Rules](#cs-coefficient-calculation-rules) | Better/Worse formulas, R/Q exclusion, range validation |
| [Sample Size Calibration Rules](#sample-size-calibration-rules) | Respondent count thresholds, confidence tier mapping |
| [Split Detection Rules](#split-detection-rules) | Majority threshold, resolution protocol, domain expert escalation |
| [Feature Lifecycle Rules](#feature-lifecycle-rules) | Attractive to Performance to Must-be migration, re-evaluation triggers |
| [Priority Matrix Construction Rules](#priority-matrix-construction-rules) | Better x-axis, Worse y-axis, 4-quadrant assignment, conflict detection |
| [Confidence Classification Rules](#confidence-classification-rules) | HIGH/MEDIUM/LOW mapping, synthesis judgment requirements |
| [Quality Gate Integration](#quality-gate-integration) | Score mapping to S-014 rubric dimensions |
| [Related Files](#related-files) | Dependency matrix: upstream, downstream, and sibling references |
| [Self-Review Checklist](#self-review-checklist) | S-010 verification before output persistence |

---

## Survey Question Design Rules

The functional/dysfunctional question pair is the foundational instrument of the Kano methodology. All downstream classification, CS coefficient computation, and priority matrix construction depend on question pair quality. Poorly phrased questions produce Questionable (Q) responses that degrade classification reliability.

> **Source:** Kano, Seraku, Takahashi, & Tsuji (1984) -- original functional/dysfunctional pair methodology. Berger, Blauth, Boger, et al. (1993) -- question pair design guidance and survey administration best practices.

### Question Pair Discipline

| ID | Rule | Tier | Consequence of Violation |
|----|------|------|--------------------------|
| SQD-001 | Every feature MUST have both a functional question ("How would you feel if this product had [feature X]?") and a dysfunctional question ("How would you feel if this product did NOT have [feature X]?"). Both questions MUST be present before the feature is included in the survey instrument. | HARD | Missing one half of the pair makes 5x5 table application impossible for that feature; classification cannot proceed |
| SQD-002 | Question language MUST be concrete and user-understandable: no developer jargon, no internal code names, no implementation details. Feature descriptions MUST be phrased in terms of user-observable behavior or outcomes. | HARD | Jargon-laden questions produce high Q (Questionable) response rates because respondents cannot understand what is being asked |
| SQD-003 | Questions MUST use balanced, neutral tone. Leading language (e.g., "How would you feel about the amazing new [X]?") and negative framing beyond the standard dysfunctional form MUST NOT be used. | HARD | Leading or biased phrasing skews response distributions toward the primed direction, invalidating classification |
| SQD-004 | Each question MUST be paired with the standardized 5-point response scale: (1) I like it, (2) I expect it, (3) I am neutral, (4) I can tolerate it, (5) I dislike it. Alternative or abbreviated scales MUST NOT be substituted. | HARD | Non-standard scales cannot be mapped to the 5x5 evaluation table without ambiguity; EVT-005 covers non-standard scale remediation but SQD-004 prevents the problem at the instrument level |
| SQD-005 | When a respondent answers the functional question but not the dysfunctional question (or vice versa) for a feature, the incomplete pair MUST be excluded from classification for that feature. The exclusion MUST be documented with "Partial response excluded: respondent {ID}, feature {name}, missing {functional/dysfunctional}" in the analysis notes. Partial responses MUST NOT be counted toward the feature's sample size. | HARD | Applying the 5x5 table requires both functional and dysfunctional answers; classifying on a single answer fabricates data (P-022 violation) |
| SQD-006 | Survey administration SHOULD randomize feature order across respondents to prevent order-effect bias. The first and last features in a fixed-order survey receive disproportionate attention (primacy/recency effects -- standard survey design practice; see Krosnick & Presser, 2010, for a comprehensive review of response order effects). | MEDIUM | Fixed ordering may bias classifications for features at survey extremes; randomization is standard survey methodology practice (Krosnick & Presser, 2010) |
| SQD-007 | Survey respondents SHOULD be representative of the engagement context's target user population. Convenience samples from internal team members SHOULD be used for survey instrument validation only, not for final classification. | MEDIUM | Non-representative respondent pools produce classifications that reflect internal assumptions rather than actual user satisfaction drivers |

---

## 5x5 Evaluation Table Rules

The 5x5 evaluation table is the core classification mechanism. Each respondent-feature pair maps to exactly one Kano category based on the intersection of functional and dysfunctional responses.

> **Source:** Kano, Seraku, Takahashi, & Tsuji (1984). Berger, Blauth, Boger, et al. (1993).

### Canonical Evaluation Table

| | **Dysfunc: Like** | **Dysfunc: Expect** | **Dysfunc: Neutral** | **Dysfunc: Tolerate** | **Dysfunc: Dislike** |
|---|---|---|---|---|---|
| **Func: Like** | Q | A | A | A | O |
| **Func: Expect** | R | I | I | I | M |
| **Func: Neutral** | R | I | I | I | M |
| **Func: Tolerate** | R | I | I | I | M |
| **Func: Dislike** | R | R | R | R | Q |

### Response Scale

| Response | Code | Meaning |
|----------|------|---------|
| I like it | 1 | Positive reaction to the feature state |
| I expect it | 2 | Considers this a basic expectation |
| I am neutral | 3 | No strong feeling either way |
| I can tolerate it | 4 | Mild negative reaction, but acceptable |
| I dislike it | 5 | Strong negative reaction |

### Evaluation Table Discipline

| ID | Rule | Tier | Consequence of Violation |
|----|------|------|--------------------------|
| EVT-001 | Every respondent-feature pair MUST be classified using the canonical 5x5 evaluation table. No alternative classification schemes permitted. | HARD | Non-standard classification breaks CS coefficient validity and cross-study comparability |
| EVT-002 | Every respondent-feature pair MUST map to exactly one category (M, O, A, I, R, or Q). No pair may remain unclassified. | HARD | Unclassified pairs distort aggregate distributions and CS coefficients |
| EVT-003 | The evaluation table MUST NOT be modified, extended, or reinterpreted. The cell values are fixed per Kano et al. (1984). | HARD | Modified tables produce non-standard classifications that invalidate the methodology |
| EVT-004 | R (Reverse) and Q (Questionable) responses MUST be retained in the classification distribution table. They are excluded from CS calculations only, not from the display. | HARD | Hiding R/Q responses conceals question clarity issues and user segment disagreement (P-022) |
| EVT-005 | When survey responses use non-standard scales (e.g., numeric 1-5 without labels), the agent MUST map responses to the canonical 5-point scale before applying the evaluation table. Ambiguous mappings MUST be flagged for user confirmation. | MEDIUM | Misaligned scale mapping produces incorrect classifications |

---

## CS Coefficient Calculation Rules

Customer Satisfaction (CS) coefficients quantify each feature's satisfaction potential and dissatisfaction risk.

> **Source:** Berger, Blauth, Boger, et al. (1993). Matzler & Hinterhuber (1998).

### Formulas

```
Better = (A + O) / (A + O + M + I)       Range: 0 to 1
Worse  = -(O + M) / (A + O + M + I)      Range: -1 to 0
```

Where A, O, M, I are the count of respondents classifying the feature in each category.

### Calculation Discipline

| ID | Rule | Tier | Consequence of Violation |
|----|------|------|--------------------------|
| CSC-001 | R (Reverse) and Q (Questionable) responses MUST be excluded from the CS coefficient denominator. The denominator is (A + O + M + I), not total respondents. | HARD | Including R/Q inflates the denominator and deflates coefficients, producing misleading priority signals |
| CSC-002 | Better coefficients MUST fall in the range [0.0, 1.0]. Worse coefficients MUST fall in the range [-1.0, 0.0]. Any value outside these ranges indicates a calculation error that MUST be corrected before output. | HARD | Out-of-range values indicate formula errors; publishing them propagates invalid data downstream |
| CSC-003 | When the denominator (A + O + M + I) equals zero for a feature (all responses are R or Q), CS coefficients MUST NOT be calculated. The feature MUST be flagged as "Unclassifiable -- all responses Reverse or Questionable" with a `[QUESTION CLARITY ISSUE]` marker. | HARD | Division by zero; fabricating coefficients violates P-022 |
| CSC-004 | Every CS coefficient output MUST show the calculation with A, O, M, I counts and explicit R/Q exclusion notation (e.g., "Better = (3+5)/(3+5+4+2) = 0.57; R=1, Q=0 excluded"). | HARD | Opaque calculations prevent verification and violate P-001 (evidence required) |
| CSC-005 | CS coefficient values SHOULD be rounded to two decimal places for display. The full-precision value SHOULD be retained in handoff data. | MEDIUM | Excessive precision implies false accuracy; insufficient precision loses ranking signal |

---

## Sample Size Calibration Rules

Survey sample size determines classification confidence and the scope of permissible claims.

> **Source:** Berger, Blauth, Boger, et al. (1993). The 20-respondent threshold is the cited minimum for statistically reliable Kano classification. The 5-8 respondent directional range is practitioner guidance consistent with Berger et al. discussion of small-sample analysis.

### Confidence Tier Mapping

| Respondent Count | Confidence Tier | Classification Quality | Permissible Claims |
|-----------------|-----------------|----------------------|-------------------|
| 0 | N/A | No classification possible | Survey design output only |
| 1-4 | Very Low | Individual preferences, not patterns | Label `[ANECDOTAL -- NOT FOR DESIGN DECISIONS]`; LOW confidence |
| 5-8 | MEDIUM | Directional signal; majority may shift | Classify with confidence disclosure; recommend expanding to 20+ |
| 9-19 | MEDIUM-HIGH | Increasingly stable | Classify; note statistical threshold not yet met |
| 20+ | HIGH | Statistically reliable (Berger et al., 1993) | Full confidence in classifications and CS coefficients |
| 50+ | Very High | Enables segment analysis | Full classification plus segment breakdowns (practitioner recommendation) |

### Sample Size Discipline

| ID | Rule | Tier | Consequence of Violation |
|----|------|------|--------------------------|
| SSC-001 | Every classification output MUST include a sample size disclosure stating the respondent count and corresponding confidence tier. | HARD | Omitting sample size conceals statistical limitations (P-022 violation) |
| SSC-002 | Classifications based on fewer than 5 respondents MUST carry `[ANECDOTAL -- NOT FOR DESIGN DECISIONS]` labels and LOW confidence. CS coefficients MUST be labeled "unreliable." | HARD | Presenting anecdotal data as reliable drives false-precision prioritization decisions |
| SSC-003 | Classifications based on 5-8 respondents MUST disclose "Directional only -- coefficients may shift with additional respondents" and carry MEDIUM confidence. | HARD | Omitting directional caveat misleads stakeholders into treating MEDIUM data as HIGH |
| SSC-004 | The agent MUST recommend expanding to 20+ respondents when the sample is below that threshold. This recommendation MUST appear in both the Executive Summary and the Sample Size Disclosure section. | MEDIUM | Without expansion guidance, teams may accept insufficient samples as final |
| SSC-005 | Segment analysis (breaking classifications by user segment) MUST NOT be performed with fewer than 50 respondents. Sub-segment classification with small samples produces unreliable distributions. | HARD | Segment analysis requires sufficient per-segment sample size; small total samples yield meaningless per-segment results |

---

## Split Detection Rules

A split classification occurs when no single Kano category commands a majority of respondent responses for a feature.

> **Source:** Berger, Blauth, Boger, et al. (1993) -- discussion of response distribution analysis and majority determination.

### Split Detection Discipline

| ID | Rule | Tier | Consequence of Violation |
|----|------|------|--------------------------|
| SPL-001 | A split classification is declared when no single category (M, O, A, I, R) exceeds 50% of responses for a feature. The 50% majority threshold is the conventional cutoff per Berger et al. (1993). | HARD | Without a consistent threshold, split detection is arbitrary and non-reproducible |
| SPL-002 | Split features MUST display the full distribution breakdown (M/O/A/I/R/Q counts and percentages) and be flagged with a `[SPLIT CLASSIFICATION]` marker. | HARD | Hiding distribution detail for split features prevents informed domain expert resolution |
| SPL-003 | Split features MUST include a domain expert resolution prompt with the marker `[DOMAIN EXPERT REQUIRED]`. The prompt MUST present the top two competing categories and suggest criteria for resolution (e.g., "This feature splits between Attractive (38%) and Performance (35%). Consider: Is competitive pressure making this an expected feature?"). | HARD | Without resolution guidance, split features stall prioritization decisions |
| SPL-004 | Split features SHOULD still be included in the CS coefficient analysis and priority matrix. Their positions SHOULD be marked with a "split" indicator on the matrix. | MEDIUM | Excluding split features from the matrix loses comparative information |
| SPL-005 | When Q (Questionable) responses exceed 10% for a feature, the feature MUST be flagged with `[QUESTION CLARITY ISSUE]` and the agent MUST provide rephrasing guidance for the functional/dysfunctional question pair. The 10% threshold is a practitioner convention; no published threshold exists in the primary Kano literature (Kano et al. 1984, Berger et al. 1993). Teams MAY calibrate this threshold based on survey instrument complexity and respondent familiarity, but MUST document any deviation. | HARD | High Q rates indicate respondents misunderstood the question; classification is unreliable until questions are rephrased |
| SPL-006 | When R (Reverse) responses exceed 20% for a feature, the feature MUST be flagged with `[DOMAIN EXPERT REQUIRED]` and the agent MUST note user-segment disagreement as the likely cause. High R rates indicate that different user segments have opposing expectations for the feature. The 20% threshold is a framework-internal convention (ux-kano-analyst.md Phase 4 step 3). | HARD | High R rates without segment investigation produce misleading majority classifications that mask fundamental user-segment disagreement; priority decisions based on the aggregate classification may satisfy one segment while alienating another |

---

## Feature Lifecycle Rules

Kano categories are not static. Features migrate across categories as products and markets mature.

> **Source:** Kano, Seraku, Takahashi, & Tsuji (1984). Matzler & Hinterhuber (1998).

### Migration Trajectory

```
Attractive (A)  --->  Performance (O)  --->  Must-be (M)
  "Delighter"         "Competitive"          "Table stakes"
   (novel)            (expected)              (baseline)
```

### Lifecycle Assessment Discipline

| ID | Rule | Tier | Consequence of Violation |
|----|------|------|--------------------------|
| LCY-001 | Lifecycle assessment MUST only be performed when product history is available (prior Kano analyses, known competitive changes, or documented feature maturity data). When no history is available, the lifecycle section MUST state: "Insufficient product history for lifecycle assessment." | HARD | Fabricating lifecycle stages without historical evidence violates P-022 |
| LCY-002 | Lifecycle predictions MUST be classified as MEDIUM confidence. Rationale: the migration direction (Attractive to Performance to Must-be) is well-documented (Matzler & Hinterhuber, 1998), but timing depends on competitive dynamics and market maturation rate that the agent cannot observe. MEDIUM is the appropriate floor because the pattern is validated but timing is domain-dependent -- HIGH would overstate precision, LOW would understate the documented directional evidence. See `skills/user-experience/rules/synthesis-validation.md` Section "Confidence Classification" for the taxonomy. | HARD | Overstating lifecycle prediction confidence misleads roadmap planning |
| LCY-003 | Features approaching transition boundaries (e.g., Attractive features with increasing Performance responses across surveys) SHOULD be flagged for re-evaluation with a recommended re-survey interval of 6-12 months or at the next competitive review cycle, whichever is sooner. The interval is a practitioner recommendation; teams SHOULD adjust based on market velocity (fast-moving markets may warrant 3-6 month intervals). | MEDIUM | Missing transition signals delays strategic response to competitive shifts |
| LCY-004 | The migration direction is one-way: Attractive to Performance to Must-be (Matzler & Hinterhuber, 1998, Section 3: "Integration of Kano's model into QFD," pp. 30-32, establishing the A→O→M trajectory as driven by competitive pressure and customer expectation normalization). NEVER predict reverse migration (Must-be to Attractive) without extraordinary evidence of market disruption. | HARD | Reverse migration contradicts the established Kano lifecycle model and produces unreliable predictions |
| LCY-005 | When comparing current classifications against prior analyses, the agent SHOULD document category shifts per feature with dates and respondent counts to establish migration velocity evidence. | MEDIUM | Without longitudinal tracking, lifecycle assessment remains speculative |

---

## Priority Matrix Construction Rules

The priority matrix plots features by their CS coefficients to visualize strategic positioning.

> **Source:** Berger, Blauth, Boger, et al. (1993). Matzler & Hinterhuber (1998).

### Axis Definitions

| Axis | Coefficient | Range | Interpretation |
|------|------------|-------|----------------|
| X-axis | Better | 0.0 to 1.0 | Higher = more satisfaction potential when feature is present |
| Y-axis | |Worse| (absolute value) | 0.0 to 1.0 | Higher = more dissatisfaction risk when feature is absent |

### 4-Quadrant Assignment

| Quadrant | Better | |Worse| | Feature Type | Strategy |
|----------|--------|--------|-------------|----------|
| Top-left | High (> 0.5) | Low (< 0.5) | Attractive (delighters) | Invest for differentiation; not urgent |
| Top-right | High (> 0.5) | High (> 0.5) | Performance (competitive) | Invest to stay competitive; high priority |
| Bottom-right | Low (< 0.5) | High (> 0.5) | Must-be (basics) | Implement immediately; absence causes dissatisfaction |
| Bottom-left | Low (< 0.5) | Low (< 0.5) | Indifferent | Deprioritize; no satisfaction impact |

### Matrix Construction Discipline

| ID | Rule | Tier | Consequence of Violation |
|----|------|------|--------------------------|
| PMC-001 | The priority matrix MUST use Better as the x-axis and |Worse| (absolute value) as the y-axis. Reversing or substituting axes produces an unreadable matrix. | HARD | Axis reversal inverts the quadrant semantics and produces incorrect strategic guidance |
| PMC-002 | All four quadrants MUST be labeled (Attractive, Performance, Must-be, Indifferent) with feature type names and strategy descriptions. | HARD | Unlabeled quadrants require interpretation that may be incorrect |
| PMC-003 | Every classified feature MUST appear on the priority matrix with its CS coefficient position. Features with split classifications SHOULD be marked with a distinct indicator. | HARD | Missing features create gaps in the prioritization landscape |
| PMC-004 | Features near quadrant boundaries (within 0.05 of the 0.5 threshold on either axis) MUST be flagged as boundary cases with a `[BOUNDARY]` marker. Boundary features SHOULD include a recommended action: (a) if sample size < 20, recommend collecting additional responses to stabilize the position; (b) if sample size >= 20, recommend classifying with the current quadrant but noting the boundary sensitivity in stakeholder-facing output. | MEDIUM | Near-boundary features may shift quadrants with additional data; flagging without action guidance stalls prioritization decisions |
| PMC-005 | The default quadrant boundary threshold is 0.5 on both axes. Domain-specific adjustments SHOULD be documented with rationale when applied. | MEDIUM | Undocumented threshold changes produce non-reproducible classifications |
| PMC-006 | Priority ranking MUST follow: Must-be (implement immediately) > Performance (high priority) > Attractive (medium priority) > Indifferent (deprioritize). Within each category, rank by |Worse| descending for Must-be/Performance and Better descending for Attractive. | HARD | Incorrect priority ordering leads to misallocated development effort |
| PMC-007 | When a feature's majority category (from the 5x5 table) conflicts with its CS-derived quadrant position, the conflict MUST be documented with both the table-derived category and the CS-derived quadrant. The conflict MUST be flagged with `[CATEGORY-QUADRANT MISMATCH]`. | MEDIUM | Undocumented mismatches create ambiguous prioritization signals |

---

## Confidence Classification Rules

Every AI-generated judgment in the output requires a confidence classification. These rules govern classification criteria and synthesis gate compliance.

> **Source:** `skills/user-experience/rules/synthesis-validation.md` Section "Confidence Classification" and Section "Sub-Skill Synthesis Output Map."

### Classification Criteria

| Classification | Criteria | Action | Example |
|---------------|----------|--------|---------|
| **HIGH** | 20+ respondents with clear majority; deterministic 5x5 table application; convergent with second framework finding | Proceed with recommendation | Statistical classification with 25 respondents and clear Must-be majority (65%) |
| **MEDIUM** | 5-8 respondent directional classification; CS coefficient interpretation; lifecycle stage assessment; single-framework reasoning | Include "Validation Required" note; withhold definitive recommendation | Directional classification with 7 respondents showing Attractive majority (55%) |
| **LOW** | Fewer than 5 respondents; split classification resolution; priority conflict interpretation requiring domain context | Flag for human review; `[DOMAIN EXPERT REQUIRED]` marker | Split feature with 40% Performance and 35% Attractive, no clear majority |

### Judgment Types Requiring Classification

| Judgment Type | Description | Typical Confidence |
|---------------|-------------|-------------------|
| Feature classification (20+ respondents) | Assigning majority Kano category from aggregated 5x5 results | HIGH (deterministic table + sufficient sample) |
| Feature classification (5-8 respondents) | Directional majority from small sample | MEDIUM (directional signal, may shift with more data) |
| CS coefficient interpretation | Determining quadrant position from Better/Worse values | MEDIUM (arithmetic is exact, but threshold interpretation involves judgment) |
| Priority ranking | Ordering features within and across quadrants | MEDIUM (ranking criteria are defined, but near-boundary cases involve judgment) |
| Feature lifecycle assessment | Predicting migration stage and trajectory | MEDIUM (pattern is documented, but timing is domain-dependent) |
| Split classification resolution | Recommending resolution for features with no majority | LOW (requires domain context AI cannot reliably provide) |
| Priority conflict interpretation | Resolving features with similar CS values or category-quadrant mismatches | LOW (requires business strategy and competitive knowledge) |

### Classification Discipline

| ID | Rule | Tier |
|----|------|------|
| CLS-001 | Every AI judgment call in the Synthesis Judgments Summary MUST include a confidence classification (HIGH, MEDIUM, or LOW) and a one-line rationale. | HARD |
| CLS-002 | Directional classifications (5-8 respondents) MUST NOT be classified as HIGH. Only statistical classifications (20+ respondents) with clear majorities qualify for HIGH. | HARD |
| CLS-003 | Split classification resolution recommendations MUST be classified as LOW. Resolution requires domain-specific judgment that AI cannot reliably provide from survey data alone. | HARD |
| CLS-004 | Feature lifecycle predictions MUST be classified as MEDIUM. The migration trajectory is documented but timing is domain-dependent. | HARD |
| CLS-005 | The minimum-confidence rule applies: when a single finding draws from multiple judgment types with different confidence levels, the finding's confidence is the LOWEST among all contributing judgments. | HARD |

---

## Quality Gate Integration

Kano Model output maps to the S-014 LLM-as-Judge rubric dimensions (`.context/rules/quality-enforcement.md` Section "Quality Gate") as follows:

### Dimension Mapping

| S-014 Dimension | Weight | Kano Model Evaluation Criteria |
|-----------------|--------|-------------------------------|
| **Completeness** | 0.20 | All features in input list classified (or documented as unclassifiable); CS coefficients calculated for all classifiable features; priority matrix includes all features; sample size disclosure present; split classification analysis present for all splits |
| **Internal Consistency** | 0.20 | CS coefficients mathematically consistent with classification table counts; priority matrix quadrant assignments match CS coefficient values; response distribution percentages sum to 100% per feature; priority ranking follows the defined ordering (Must-be > Performance > Attractive > Indifferent) |
| **Methodological Rigor** | 0.20 | Canonical 5x5 evaluation table applied without modification (Kano et al., 1984); R/Q excluded from CS calculation per Berger et al. (1993); sample size thresholds applied per calibration table; split detection uses 50% majority threshold; lifecycle assessment grounded in documented evidence |
| **Evidence Quality** | 0.15 | Every classification traces to respondent data with distribution counts; CS coefficient calculations show A/O/M/I values; sample size and confidence tier disclosed; no fabricated data; confidence classifications reflect actual data quality |
| **Actionability** | 0.15 | Priority ranking provides clear implementation ordering; domain expert prompts present for split features and priority conflicts; lifecycle re-evaluation recommendations with intervals; strategic implications include concrete roadmap guidance |
| **Traceability** | 0.10 | Every classification traces to the 5x5 evaluation table application; every CS coefficient traces to the formula with counts; every priority position traces to CS values; upstream inputs (JTBD, heuristic eval) cited where used; methodology sources referenced (Kano et al. 1984, Berger et al. 1993, Matzler & Hinterhuber 1998) |

### Scoring Discipline

| ID | Rule | Tier |
|----|------|------|
| QG-001 | The quality gate threshold applies to the overall classification report, not to individual feature classifications. Baseline threshold: >= 0.92 (H-13, C2+). For C4 deliverables (architecture/governance changes), the threshold is >= 0.95 per `quality-enforcement.md` criticality levels. | HARD |
| QG-002 | Completeness scoring MUST account for operating mode: when in survey design mode (no survey data), completeness is assessed against Phase 1-2 deliverables only, not the full 5-phase workflow. | MEDIUM |
| QG-003 | Evidence Quality scoring MUST penalize fabricated response data, inflated sample size claims, or omitted R/Q exclusion disclosure. | HARD |
| QG-004 | Internal Consistency scoring MUST verify that CS coefficients are arithmetically consistent with classification table counts and that priority rankings follow the defined ordering. | HARD |

---

## Related Files

> Dependency matrix for operational traceability. Upstream files provide inputs or prerequisites; downstream files consume this rules file's outputs; sibling files share the same parent sub-skill.

| Relationship | File | Version | Purpose |
|-------------|------|---------|---------|
| **Parent SKILL.md** | `skills/ux-kano-model/SKILL.md` | v1.2.0 | Sub-skill definition; methodology overview; agent routing |
| **Agent definition** | `skills/ux-kano-model/agents/ux-kano-analyst.md` | v1.1.0 | Agent frontmatter, system prompt, output section |
| **Governance YAML** | `skills/ux-kano-model/agents/ux-kano-analyst.governance.yaml` | v1.1.0 | Enforcement metadata: quality gate, tool tier |
| **Wave progression** | `skills/user-experience/rules/wave-progression.md` | unversioned | Wave 4 entry conditions; Wave 3 completion prerequisite |
| **Synthesis validation** | `skills/user-experience/rules/synthesis-validation.md` | v1.1.0 | Confidence classification taxonomy; Sub-Skill Synthesis Output Map |
| **Output templates** | `skills/ux-kano-model/templates/` | -- | Survey and feature priority templates consumed by agent |
| **Quality enforcement** | `.context/rules/quality-enforcement.md` | -- | S-014 dimension rubric; H-13 quality gate threshold |

### Requirements Traceability

> Maps rule groups to the SKILL.md sections and agent methodology phases that motivated them.

| Rule Group | SKILL.md Section | Agent Phase | Requirement Source |
|------------|-----------------|-------------|-------------------|
| SQD-001 through SQD-007 | Methodology > Survey Design, Execution Procedure > Phase 2 | Phase 2: Survey Design | Kano et al. (1984) functional/dysfunctional pair methodology; Krosnick & Presser (2010) survey order effects |
| EVT-001 through EVT-005 | Methodology > 5x5 Evaluation Table | Phase 3: Response Analysis | Kano et al. (1984), Berger et al. (1993) |
| CSC-001 through CSC-005 | Methodology > CS Coefficients | Phase 4: Priority Synthesis | Berger et al. (1993), Matzler & Hinterhuber (1998) |
| SSC-001 through SSC-005 | Methodology > Sample Size Considerations | Phase 3: Response Analysis | Berger et al. (1993) |
| SPL-001 through SPL-006 | Execution Procedure > Phase 3, Phase 4 | Phase 3-4: Analysis and Synthesis | Berger et al. (1993) |
| LCY-001 through LCY-005 | Cross-Framework Integration > Lifecycle | Phase 4: Priority Synthesis | Kano et al. (1984), Matzler & Hinterhuber (1998) |
| PMC-001 through PMC-007 | Methodology > Priority Matrix | Phase 4: Priority Synthesis | Berger et al. (1993), Matzler & Hinterhuber (1998) |
| CLS-001 through CLS-005 | Synthesis Hypothesis Confidence | Phase 5: Synthesis | synthesis-validation.md |
| QG-001 through QG-004 | Quality Gate Integration | All phases | quality-enforcement.md (H-13, S-014) |

---

## Self-Review Checklist

Before persisting the report, the analyst MUST verify (S-010, H-15):

| # | Check | Rule Reference |
|---|-------|---------------|
| 1 | Every feature has both functional and dysfunctional questions; language is concrete, non-jargon, balanced | SQD-001, SQD-002, SQD-003 |
| 2 | Each question uses the standardized 5-point response scale | SQD-004 |
| 3 | Partial responses (missing one half of the pair) are excluded and documented | SQD-005 |
| 4 | All features in the input list are classified or documented as unclassifiable with rationale | EVT-002 |
| 5 | The 5x5 evaluation table is correctly applied: each respondent-feature pair maps to exactly one category | EVT-001, EVT-002 |
| 6 | CS coefficients are calculated with R and Q responses excluded from the denominator | CSC-001 |
| 7 | CS coefficient calculations show A/O/M/I counts and R/Q exclusion notation | CSC-004 |
| 8 | Better values are in [0.0, 1.0] and Worse values are in [-1.0, 0.0] | CSC-002 |
| 9 | Sample size disclosure is present with respondent count and confidence tier | SSC-001 |
| 10 | Split classifications (no majority > 50%) are identified and flagged with resolution prompts | SPL-001, SPL-003 |
| 11 | High Q rates (> 10%) are flagged with question rephrasing guidance | SPL-005 |
| 12 | High R rates (> 20%) are flagged with user-segment disagreement note | SPL-006 |
| 13 | Priority matrix uses Better (x-axis) vs. |Worse| (y-axis) with all 4 quadrants labeled | PMC-001, PMC-002 |
| 14 | Priority ranking follows Must-be > Performance > Attractive > Indifferent ordering | PMC-006 |
| 15 | Feature lifecycle assessment is included when product history is available, or absence is documented | LCY-001 |
| 16 | Synthesis Judgments Summary lists every AI judgment call with confidence classification | CLS-001 |
| 17 | Navigation table is present with correct anchor links (H-23) | H-23 |
| 18 | Handoff data section is populated for downstream sub-skill consumption | -- |

---

*Rule file: kano-methodology-rules.md*
*Version: 1.2.0*
*Parent sub-skill: /ux-kano-model*
*Parent skill: /user-experience*
*Agent: ux-kano-analyst*
*SSOT: `skills/ux-kano-model/SKILL.md` (v1.2.0)*
*Created: 2026-03-04*
*Revised: 2026-03-04 (iter3)*

<!-- Traceability: PROJ-022 EPIC-005, Wave 4. Standards: H-23 (navigation), H-34 (agent-dev), SR-002 (input validation), SR-003 (output filtering). Methodology: Kano et al. (1984), Berger et al. (1993), Matzler & Hinterhuber (1998). Synthesis validation: skills/user-experience/rules/synthesis-validation.md. Quality gate: .context/rules/quality-enforcement.md. -->
<!-- VERSION: 1.2.0 | DATE: 2026-03-04 | SOURCE: skills/ux-kano-model/SKILL.md (v1.2.0), skills/ux-kano-model/agents/ux-kano-analyst.md | REVISION: iter3 -- SQD-006 primacy/recency citation, LCY-004 section-level citation, SQD-007 respondent selection, SPL-006 label precision -->
