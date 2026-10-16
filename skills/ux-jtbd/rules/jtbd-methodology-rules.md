<!-- VERSION: 1.3.0 | DATE: 2026-03-04 | SOURCE: skills/ux-jtbd/SKILL.md, skills/ux-jtbd/agents/ux-jtbd-analyst.md | PARENT: /ux-jtbd sub-skill | REVISION: iter4 quality fixes -- inline quality-enforcement.md citation in Confidence Classification, Moesta-Spiek (2014) added to References, Decision Basis footer, Job Statement Rules inline citation, visible metadata block -->

# JTBD Methodology Rules

> **Version:** 1.3.0 | **Date:** 2026-03-04 | **Status:** COMPLETE

> Decision rules and methodology constraints for the `ux-jtbd-analyst` agent. Complements the agent definition body with detailed validation rules, classification criteria, scoring formulas, and anti-pattern detection that are too granular for the agent's `<methodology>` section. The agent definition references this file; this file is the authoritative source for JTBD methodology constraints.

## Document Sections

| Section | Purpose |
|---------|---------|
| [Job Statement Rules](#job-statement-rules) | Canonical format, validation, and anti-patterns |
| [Job Classification Rules](#job-classification-rules) | Functional, social, emotional classification criteria |
| [Opportunity Scoring Rules](#opportunity-scoring-rules) | Ulwick ODI formula, thresholds, sample size guidance |
| [Switch Force Analysis Rules](#switch-force-analysis-rules) | Moesta four forces model, rating scale, net force calculation |
| [Confidence Classification Rules](#confidence-classification-rules) | HIGH/MEDIUM/LOW criteria and escalation |
| [Scope Rules](#scope-rules) | Job count limits, consolidation, parent-child hierarchies |
| [Source Authority Rules](#source-authority-rules) | Tier 1/2/3 evidence classification and citation requirements |
| [References](#references) | Bibliographic citations for core JTBD methodology sources |

---

## Job Statement Rules

All job statements produced by the `ux-jtbd-analyst` MUST follow the canonical three-part format. Source: Christensen (2016) [Tier 2] -- canonical job statement structure.

### Canonical Format

```
"When I am [situation], I want to [motivation], so I can [expected outcome]."
```

| Clause | Purpose | Validation Rule |
|--------|---------|-----------------|
| **Situation** (`When I am...`) | The context or circumstance triggering the job | MUST describe a specific, observable triggering condition. MUST NOT be a permanent state (e.g., "When I am a manager" is invalid; "When I am preparing a quarterly report" is valid). |
| **Motivation** (`I want to...`) | The core action the user wants to accomplish | MUST describe the user's desired action, NOT a product feature. MUST be solution-agnostic -- no product names, UI elements, or implementation details. |
| **Expected Outcome** (`so I can...`) | The desired end state or benefit | MUST describe a measurable or observable result. MUST NOT be vague (e.g., "so I can be happy" is invalid; "so I can submit the report before the deadline" is valid). |

### Validation Rules

| Rule | Enforcement | Example (Pass) | Example (Fail) |
|------|-------------|----------------|-----------------|
| All three clauses present | HARD -- reject statement if any clause missing | "When I am onboarding a new hire, I want to assign training modules, so I can track their completion within the first week." | "I want to assign training modules." (missing situation and outcome) |
| User perspective | HARD -- must use first person ("I") | "When I am reviewing pull requests..." | "When the system processes pull requests..." |
| Solution-agnostic | HARD -- no product or technology references | "...I want to compare code changes side by side..." | "...I want to use the GitHub diff viewer..." |
| Single dimension | HARD -- one job type per statement | Functional only OR social only OR emotional only | "...I want to track tasks AND feel confident..." (mixed functional + emotional) |
| Stable over time | MEDIUM -- jobs should reflect enduring motivations | "...I want to share progress with stakeholders..." | "...I want to update the Jira board..." (tool-specific, not stable) |
| Outcome measurability | MEDIUM -- outcome should be verifiable | "...so I can reduce onboarding time to under 3 days." | "...so I can have a better experience." |

### Anti-Patterns

| Anti-Pattern | Detection Signal | Correction |
|-------------|------------------|------------|
| **Solution-embedded statement** | Motivation clause contains a product name, brand, UI element, or technology | Remove the product reference; restate as the underlying user goal. "I want to use Slack to message my team" becomes "I want to quickly communicate status to my team." |
| **Vague outcome** | Outcome clause uses abstract terms without observable criteria ("be better", "improve things", "have a good experience") | Replace with a specific, measurable result. Ask: "How would the user know they achieved this outcome?" |
| **Missing context** | Situation clause is absent or states a permanent condition rather than a triggering circumstance | Add a specific triggering event or context. "When I am a project manager" becomes "When I am starting a new project sprint." |
| **Feature masquerading as job** | The entire statement describes a product feature rather than a user need | Reframe by asking: "Why does the user want this feature? What job is it hired to do?" |
| **Compound job** | Statement contains multiple motivations joined by "and" or "while" | Split into separate job statements, each targeting one dimension. |
| **Provider perspective** | Statement uses "the user" or "customers" instead of first person | Rewrite in first person. Job statements describe the user's own experience. |

---

## Job Classification Rules

Every job statement MUST be classified into exactly one of three types. Source: Christensen (2016) [Tier 2] -- functional, social, and emotional job dimensions.

### Classification Criteria

| Type | Definition | Decision Test | Language Signals |
|------|-----------|--------------|-----------------|
| **Functional** | The practical task the user wants to accomplish | "What is the user trying to get done?" Answer describes an observable action or outcome. | Action verbs: organize, find, create, compare, complete, track, submit, resolve |
| **Social** | How the user wants to be perceived by others | "How does the user want to appear to others?" Answer references reputation, status, belonging, or professional identity. | Perception language: appear, impress, demonstrate, show, be seen as, be recognized for |
| **Emotional** | How the user wants to feel during or after the job | "How does the user want to feel?" Answer references an internal emotional state. | Feeling language: feel confident, feel in control, feel relieved, avoid anxiety, feel accomplished |

### Decision Procedure

Apply the following in order:

1. **Check for emotional language first.** If the outcome clause primarily describes an internal feeling state, classify as Emotional.
2. **Check for social language second.** If the outcome clause primarily describes how others perceive the user, classify as Social.
3. **Default to Functional.** If the outcome describes an observable action, task completion, or measurable result, classify as Functional.

### Mixed-Type Handling

When a job statement contains signals from multiple types:

| Scenario | Rule | Example |
|----------|------|---------|
| Functional + Emotional overlap | Split into two separate statements. The functional statement captures the task; the emotional statement captures the feeling. | "I want to submit the report on time so I can feel relieved" splits into: (1) Functional: "...so I can meet the submission deadline" and (2) Emotional: "...so I can feel relieved that the work is complete." |
| Functional + Social overlap | Split into two separate statements. The functional statement captures the task; the social statement captures the perception goal. | "I want to present clean dashboards so I can impress leadership" splits into: (1) Functional: "...so I can share accurate project status" and (2) Social: "...so I can be perceived as organized and in control." |
| All three types present | The statement is a compound job (anti-pattern). Split into three separate statements, one per type. | Flag as compound; decompose. |

---

## Opportunity Scoring Rules

Opportunity scoring follows Ulwick's Outcome-Driven Innovation (ODI) formula. Source: Ulwick (2016) [Tier 2].

### Formula

```
Opportunity Score = Importance + max(Importance - Satisfaction, 0)
```

Source: Ulwick (2016) [Tier 2] -- original ODI formula.

### Input Scales

| Input | Scale | Anchors |
|-------|-------|---------|
| **Importance** | 1-10 (integer) | 1 = Irrelevant to the user's success. 5 = Moderately important; users notice but tolerate gaps. 10 = Critical; failure to address blocks the job entirely. |
| **Satisfaction** | 1-10 (integer) | 1 = Current solutions completely fail to deliver. 5 = Current solutions deliver acceptably. 10 = Current solutions deliver excellently; no room for improvement. |

### Score Range and Thresholds

Source: Ulwick (2016) [Tier 2] -- canonical ODI threshold classification.

| Score Range | Classification | Strategic Implication |
|-------------|---------------|----------------------|
| >= 10 | **Underserved** | High opportunity for innovation. Users care deeply but current solutions fail to deliver. Prioritize for new feature development or redesign. |
| 6 - 9 | **Appropriately served** | Incremental improvement opportunity. Current solutions are adequate but refinement adds value. Candidate for optimization, not reinvention. |
| < 6 | **Overserved** | Potential for cost reduction or simplification. Current solutions exceed user needs. Consider whether investment here has diminishing returns. |

### Canonical Outcome Statement Formats

Ulwick defines three canonical formats for desired outcome statements. These formats help distinguish valid outcome statements from features or solutions. Source: Ulwick (2016) [Tier 2].

| Format | Purpose | Example |
|--------|---------|---------|
| "Minimize the time it takes to [desired outcome]" | Captures speed/efficiency outcomes | "Minimize the time it takes to identify the root cause of a build failure" |
| "Minimize the likelihood of [undesired outcome]" | Captures risk-reduction outcomes | "Minimize the likelihood of deploying a regression to production" |
| "Increase the likelihood of [desired outcome]" | Captures success-rate outcomes | "Increase the likelihood of onboarding a new hire within the first week" |
| "Minimize the variability of [quality measure]" | Captures consistency/reliability outcomes | "Minimize the variability of deployment success rates across environments" |

Ulwick defines multiple canonical formats. The four above cover the most common outcome types: speed, risk reduction, success rate, and consistency. Outcome statements that do not fit any of these formats are likely features, solutions, or tasks rather than true desired outcomes. The agent SHOULD reframe non-conforming outcome statements into one of these canonical formats before scoring.

### Score Validation Rules

| Rule | Enforcement |
|------|-------------|
| Both Importance and Satisfaction MUST be integers on the 1-10 scale | HARD -- reject non-integer or out-of-range values |
| The max() function prevents negative dissatisfaction from reducing the score | HARD -- when Satisfaction >= Importance, the second term is 0 (floor, not penalty) |
| Maximum possible score is 19 (Importance=10, Satisfaction=1: 10 + max(10-1, 0) = 19) | Informational -- scores exceeding 19 indicate a calculation error |
| Minimum possible score is 1 (Importance=1, Satisfaction=10: 1 + max(1-10, 0) = 1) | Informational |
| Scores must show the full calculation, not just the result | HARD -- output must include Importance, Satisfaction, and the computed score |

### Sample Size Guidance (P-022 Disclosure)

In the AI-augmented single-analyst context, opportunity scores are derived from secondary research rather than statistically sampled user data.

| Context | Guidance | Disclosure Requirement |
|---------|----------|----------------------|
| AI-synthesized scores (no primary data) | Importance and Satisfaction ratings are estimates based on secondary evidence (reviews, competitor analysis, domain literature). | MUST disclose: "Opportunity scores are AI-synthesized estimates from secondary research. Treat as directional hypotheses requiring validation, not statistically validated measurements." |
| Partial primary data (1-5 data points) | Scores may reflect limited primary evidence but do not meet statistical significance thresholds. | MUST disclose: "Opportunity scores incorporate limited primary data (N={count}). Sample size is insufficient for statistical confidence; treat as informed estimates." |
| Validated primary data (6+ data points with segment alignment) | Scores have reasonable directional validity for the target segment. | MAY omit the disclosure caveat but SHOULD note the sample size. |

Traditional ODI research recommends N=50-200 respondents per user segment (Source: Ulwick (2016) [Tier 2] -- recommended survey sample sizes for ODI research). The AI-augmented context operates well below this threshold. Per P-022 (no deception), this limitation MUST be transparently communicated in every output containing opportunity scores.

---

## Switch Force Analysis Rules

Switch force analysis follows the Moesta/Spiek four forces model. Source: Moesta (2020) [Tier 2].

### The Four Forces

```
PUSH (current pain)  +  PULL (new solution appeal)
                    vs.
ANXIETY (fear of new)  +  HABIT (comfort with current)

Switch occurs when: PUSH + PULL > ANXIETY + HABIT
```

| Force | Direction | Definition | Evidence Sources |
|-------|-----------|-----------|-----------------|
| **Push** | Drives change | Pain points, frustrations, and limitations of the current solution that push users away | Negative reviews, support tickets, churn data, competitive comparison complaints |
| **Pull** | Drives change | Attractive features, outcomes, and promises that draw users toward a new solution | Positive reviews of alternatives, resonant marketing copy, trial signups, feature requests |
| **Anxiety** | Resists change | Fears and uncertainties about adopting the new solution | FAQ pages (questions reveal fears), onboarding drop-off, trial abandonment, "switching cost" mentions |
| **Habit** | Resists change | Comfort, workflow inertia, and sunk costs that keep users attached to the current solution | Feature usage depth, integration ecosystem, learning curve investment, sunk cost language |

Source: Moesta (2020) [Tier 2] -- four forces of progress model.

### Rating Scale

Each force is rated on a 1-5 integer scale based on evidence volume and intensity.

| Rating | Label | Anchor Definition |
|--------|-------|-------------------|
| 1 | Minimal | Sparse evidence; weak or isolated signal. Fewer than 3 evidence instances. |
| 2 | Low | Some evidence; detectable but not prominent. 3-5 evidence instances, low intensity. |
| 3 | Moderate | Clear evidence from multiple sources; recognizable theme. 6-10 evidence instances or fewer instances with high intensity. |
| 4 | Strong | Substantial evidence; dominant theme across multiple source types. 10+ evidence instances or strong intensity across 3+ source types. |
| 5 | Dominant | Overwhelming evidence; the primary narrative in user feedback. Pervasive across all evidence sources with high intensity. |

### Net Force Calculation

```
Net Force = (Push + Pull) - (Anxiety + Habit)
```

| Net Force | Interpretation | Strategic Implication |
|-----------|---------------|----------------------|
| > 0 (positive) | Driving forces outweigh resisting forces | Switch is likely; focus on reducing remaining anxiety and habit barriers to accelerate adoption. |
| = 0 (balanced) | Forces are in equilibrium | Switch is uncertain; small changes in any force could tip the balance. Identify the weakest resisting force to target. |
| < 0 (negative) | Resisting forces outweigh driving forces | Switch is unlikely without intervention; must either increase push/pull or decrease anxiety/habit before users will adopt. |

### Analysis Rules

| Rule | Enforcement |
|------|-------------|
| All four forces MUST be assessed for each main job | HARD -- incomplete force analysis is rejected |
| Each force rating MUST cite at least one evidence source | HARD -- unsourced ratings are rejected (P-001 compliance) |
| Force ratings MUST use the 1-5 integer scale with anchor definitions | HARD -- reject non-integer or out-of-range values |
| Net force calculation SHOULD be shown explicitly | MEDIUM -- output should include the arithmetic |
| When evidence is insufficient to rate a force, use the midpoint (3) and flag for validation | MEDIUM -- prevents analytical paralysis while maintaining transparency |

---

## Confidence Classification Rules

Every job statement, switch force finding, and opportunity score MUST carry a confidence classification. Confidence levels align with the quality gate framework in `.context/rules/quality-enforcement.md` [H-13, P-022].

### Classification Criteria

| Level | Criteria | Example |
|-------|---------|---------|
| **HIGH** | 3 or more direct, independent data sources corroborate the finding. Sources include primary research data (interviews, observations, analytics), published peer-reviewed studies, or converging evidence from 3+ Tier 1/Tier 2 sources. | Job statement corroborated by 3 user interviews, 2 support ticket themes, and behavioral analytics showing the same pattern. |
| **MEDIUM** | 1-2 direct sources, OR secondary synthesis from credible methodology sources (Tier 2). This is the default classification for all AI-synthesized outputs. | Job statement synthesized from competitor reviews and domain literature without direct user validation. |
| **LOW** | Inference only -- no direct evidence. The finding is derived from analogy, pattern matching across unrelated domains, or logical deduction without supporting data. | Job statement inferred from analogous products in a different industry with no evidence from the target domain. |

### Escalation Rules

| Condition | Action |
|-----------|--------|
| Any finding classified as LOW | MUST be flagged in the Synthesis Judgments Summary with the specific inference basis. MUST appear in the Validation Required section with a named validation method. |
| Majority of findings (> 50%) classified as LOW | MUST add a low-confidence majority banner at the top of the output: "WARNING: The majority of findings in this analysis are classified LOW confidence (inference only). This output should be treated as a hypothesis generation exercise, not a decision basis. Validate all LOW-confidence findings against primary user data before proceeding." |
| Any finding downgraded from MEDIUM to LOW during analysis | MUST document the downgrade reason in the Synthesis Judgments Summary (e.g., "Downgraded from MEDIUM to LOW: contradictory evidence found in competitor review analysis"). |
| Finding upgraded from MEDIUM to HIGH | MUST cite the 3+ corroborating sources explicitly. Upgrade without sufficient corroboration is a P-022 violation. |

### Confidence Propagation

When JTBD output is handed off to downstream sub-skills (per `skills/user-experience/rules/ux-routing-rules.md` [Cross-Sub-Skill Handoff]):

- HIGH confidence findings propagate as HIGH (downstream sub-skill may downgrade based on its own assessment).
- MEDIUM confidence findings propagate as MEDIUM.
- LOW confidence findings propagate as LOW (downstream sub-skill MUST NOT upgrade without additional evidence).

Source: `skills/user-experience/rules/synthesis-validation.md` [Confidence Propagation] (exists, 285 lines -- verified 2026-03-04).

---

## Scope Rules

### Job Count Limits

| Constraint | Value | Rationale |
|-----------|-------|-----------|
| Minimum main functional jobs per engagement | 3 | Fewer than 3 jobs suggests insufficient exploration; the analysis likely missed important job dimensions. |
| Maximum main functional jobs per engagement | 7 | Tiny teams (1-5 people) lack capacity to address more than 7 jobs effectively. Beyond 7, strategic focus is diluted. |
| Social and emotional jobs | No hard limit, but SHOULD be 1-3 per main functional job | Social and emotional jobs are complementary dimensions of functional jobs. Excessive social/emotional jobs without corresponding functional jobs indicates classification errors. |

### Consolidation Rules (When > 7 Jobs Identified)

When initial job identification surfaces more than 7 main functional jobs:

| Step | Action |
|------|--------|
| 1 | **Identify related job clusters.** Group jobs that share the same triggering situation or target the same user segment. |
| 2 | **Merge related jobs into parent jobs.** A parent job encompasses the shared goal; child jobs become job steps or outcome expectations within the parent. |
| 3 | **Prioritize by opportunity score.** If consolidation still leaves more than 7, rank by opportunity score and retain the top 7. Document the deprioritized jobs as "Identified but deprioritized" with their scores. **Tie-breaking:** When two candidate parent jobs have equal scope, consolidate under the one with the higher maximum child opportunity score. Secondary tie-breaker: if maximum child opportunity scores are equal, prefer the parent job with more child jobs (broader coverage). |
| 4 | **Document consolidation decisions.** Each merge or deprioritization MUST appear in the Synthesis Judgments Summary with the rationale. |

### Parent-Child Job Hierarchies

| Concept | Definition | Example |
|---------|-----------|---------|
| **Parent job** | A high-level job that encompasses multiple related child jobs. The parent describes the overarching goal. | "Manage my team's project delivery" |
| **Child job** | A specific sub-task or dimension of the parent job. Each child job is a valid job statement in its own right. | "Track task completion across team members" (child of project delivery) |
| **Job step** (distinct from child job) | A sequential phase within a single job's execution, following the universal 8-step process (Define through Conclude). Job steps are NOT independent jobs. | "Locate the relevant project files" (step 2 of the parent job) |

**Hierarchy rules:**

| Rule | Enforcement |
|------|-------------|
| Parent jobs MUST be decomposable into 2 or more child jobs or job steps | MEDIUM -- a "parent" with only one child is not a meaningful hierarchy |
| Child jobs MUST share the parent's triggering situation or user segment | HARD -- unrelated jobs grouped under a parent indicate a classification error |
| Hierarchy depth MUST NOT exceed 2 levels (parent -> child) | HARD -- deeper hierarchies add complexity without analytical value for tiny teams |
| Job steps belong to job mapping (Phase 4), not job identification (Phase 2) | MEDIUM -- avoid conflating job hierarchy with job process decomposition |

---

## Source Authority Rules

All evidence cited in JTBD outputs MUST be classified by source authority tier. This enables reviewers to assess finding reliability at a glance.

### Source Tiers

| Tier | Name | Definition | Examples | Trust Level |
|------|------|-----------|----------|-------------|
| **Tier 1** | Primary research data | Direct observation of or communication with target users. Data collected specifically for the research question. | User interviews, usability tests, behavioral analytics, support ticket analysis, app store reviews from verified users, survey responses | Highest -- direct user voice |
| **Tier 2** | Published methodology | Peer-reviewed research, published books by recognized JTBD practitioners, established framework documentation. | Christensen (2016), Ulwick (2016), Moesta (2020), peer-reviewed UX journals, NNG research reports | High -- vetted knowledge |
| **Tier 3** | Tertiary sources | Blog posts, conference talks, framework documentation from unofficial sources, opinion pieces, marketing materials, social media discussions. | Medium blog posts, conference slide decks, framework README files, product marketing copy, Twitter/X threads | Lowest -- unvetted, potentially biased |

### Citation Rules

| Rule | Enforcement |
|------|-------------|
| Every job statement MUST cite at least one evidence source with its tier classification | HARD (P-001 compliance) |
| Every switch force rating MUST cite at least one evidence source with its tier classification | HARD (P-001 compliance) |
| Every opportunity score's Importance and Satisfaction ratings MUST reference the evidence basis | HARD -- prevents precise-looking numbers without evidence context (P-022 compliance) |
| Tier 3 sources MUST NOT be the sole evidence for any job statement | HARD -- a finding supported only by blog posts or conference talks is insufficiently grounded |
| Tier 3 sources MAY be used as supplementary evidence when paired with Tier 1 or Tier 2 sources | MEDIUM -- tertiary sources can enrich but not replace primary or published evidence |
| When only Tier 3 evidence is available for a finding, the finding MUST be classified as LOW confidence | HARD -- aligns source quality with confidence classification |
| Citation format MUST include: author/source name, year (if available), tier classification | MEDIUM -- enables rapid source quality assessment |

### Citation Format

```
Source: {author or source name} ({year}) [Tier {N}]
```

Examples:
- `Source: Ulwick (2016) [Tier 2]`
- `Source: App Store reviews, 47 reviews mentioning onboarding friction (2025-2026) [Tier 1]`
- `Source: UX Collective blog, "JTBD in Practice" (2025) [Tier 3]`

---

## References

| Source | Citation | Tier |
|--------|----------|------|
| Christensen, C. M., Hall, T., Dillon, K., & Duncan, D. S. (2016). *Competing Against Luck: The Story of Innovation and Customer Choice.* Harper Business. | Christensen (2016) | Tier 2 |
| Ulwick, A. W. (2016). *Jobs to Be Done: Theory to Practice.* Idea Bite Press. | Ulwick (2016) | Tier 2 |
| Moesta, B. (2020). *Demand-Side Sales 101: Stop Selling and Help Your Customers Make Progress.* Lioncrest Publishing. | Moesta (2020) | Tier 2 |
| Moesta, B. & Spiek, C. (2014). *The Jobs-to-Be-Done Handbook.* Re-Wired Group. | Moesta-Spiek (2014) | Tier 2 |

---

*Rule file: jtbd-methodology-rules.md*
*Version: 1.3.0*
*Parent sub-skill: `/ux-jtbd` (`skills/ux-jtbd/SKILL.md`)*
*Agent: `ux-jtbd-analyst` (`skills/ux-jtbd/agents/ux-jtbd-analyst.md`)*
*Parent skill: `/user-experience` (`skills/user-experience/SKILL.md`)*
*Quality enforcement SSOT: `.context/rules/quality-enforcement.md`*
*Decision Basis: ADR-PROJ022-001, ADR-PROJ022-002, ORCHESTRATION.yaml (projects/PROJ-022-user-experience-skill/orchestration/ux-skill-build-20260303-001/ORCHESTRATION.yaml)*
*Created: 2026-03-04*
*Status: COMPLETE*

<!-- VERSION: 1.3.0 | DATE: 2026-03-04 | SOURCE: skills/ux-jtbd/SKILL.md, skills/ux-jtbd/agents/ux-jtbd-analyst.md | PARENT: /ux-jtbd sub-skill | REVISION: iter4 quality fixes -- inline quality-enforcement.md citation in Confidence Classification, Moesta-Spiek (2014) added to References, Decision Basis footer, Job Statement Rules inline citation, visible metadata block -->
