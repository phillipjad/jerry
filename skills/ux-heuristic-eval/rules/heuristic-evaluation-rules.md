<!-- VERSION: 1.2.0 | DATE: 2026-03-04 | SOURCE: skills/ux-heuristic-eval/SKILL.md, skills/ux-heuristic-eval/agents/ux-heuristic-evaluator.md | PARENT: /ux-heuristic-eval sub-skill | REVISION: Iter3 quality fixes -- Google PAIR access date, HEART attribution, ORCHESTRATION.yaml traceability, effort tech note, synthesis-validation clarification, unmapped HEART guidance -->

# Heuristic Evaluation Rules

> Operational constraints and methodology rules for the `ux-heuristic-evaluator` agent. Provides detailed evaluation criteria, severity classification guidance, finding documentation requirements, and report structure that complement the agent definition.

## Document Sections

| Section | Purpose |
|---------|---------|
| [Nielsen's 10 Heuristics](#nielsens-10-heuristics) | Evaluation criteria, checkpoints, common violations, severity guidance per heuristic |
| [AI-Interaction Supplement Heuristics](#ai-interaction-supplement-heuristics) | AI-1, AI-2, AI-3 supplementary heuristics for AI product interfaces |
| [Severity Scale](#severity-scale) | 0-4 Nielsen severity taxonomy with decision criteria |
| [Finding Documentation Rules](#finding-documentation-rules) | Required fields, evidence requirements, F-{NNN} format |
| [Deduplication Rules](#deduplication-rules) | When findings count as one pattern vs. separate findings |
| [Single-Evaluator Reliability](#single-evaluator-reliability) | P-022 disclosure on coverage limitations and mitigation |
| [Report Structure](#report-structure) | Required sections in the evaluation output report |

---

## Nielsen's 10 Heuristics

Each heuristic below includes Nielsen's definition, specific evaluation checkpoints, common violation examples, and severity classification guidance. The evaluator applies all 10 heuristics sequentially (H1 through H10) to every screen or flow under review. No heuristic may be skipped.

> **Source:** Jakob Nielsen, "10 Usability Heuristics for User Interface Design" (1994, revised 2020). Nielsen Norman Group.

### H1: Visibility of System Status

**Definition:** The design should always keep users informed about what is going on, through appropriate feedback within a reasonable amount of time.

**Evaluation Checkpoints:**
1. Does every user action produce visible feedback within 1 second?
2. Are loading states, progress indicators, and processing states clearly communicated?
3. Does the system confirm successful completion of actions (saves, submissions, deletions)?
4. Are state changes (active/inactive, selected/unselected, enabled/disabled) visually distinguishable?
5. Does the system indicate the user's current location within the application (breadcrumbs, active nav)?

**Common Violations:**
- Form submission with no loading indicator or success confirmation
- Background saves with no visual acknowledgment
- Navigation state not reflected in the UI (no active menu highlighting)
- Multi-step processes with no progress indicator

**Severity Guidance:** Violations that leave users uncertain whether an action completed are typically severity 3. Missing feedback on non-critical status changes is typically severity 1-2.

---

### H2: Match Between System and Real World

**Definition:** The design should speak the users' language. Use words, phrases, and concepts familiar to the user, rather than internal jargon. Follow real-world conventions, making information appear in a natural and logical order.

**Evaluation Checkpoints:**
1. Does the interface use terminology that the target users would recognize and understand?
2. Are icons and metaphors consistent with real-world conventions?
3. Is information presented in a logical order that matches users' mental models?
4. Are date formats, units, and conventions appropriate for the target audience?

**Common Violations:**
- Technical jargon or internal codenames exposed to end users
- Counterintuitive information ordering (e.g., alphabetical when chronological expected)
- Icons that do not map to recognizable real-world objects or conventions
- Developer-facing identifiers visible in the UI (UUIDs, internal status codes)

**Severity Guidance:** Jargon that blocks task comprehension is severity 3. Minor labeling inconsistencies that do not impede understanding are severity 1-2.

---

### H3: User Control and Freedom

**Definition:** Users often perform actions by mistake. They need a clearly marked "emergency exit" to leave the unwanted state without having to go through an extended process.

**Evaluation Checkpoints:**
1. Can users undo or redo recent actions?
2. Is there a clear way to cancel in-progress operations (form fills, uploads, wizards)?
3. Can users navigate back to previous states without losing work?
4. Are destructive actions (delete, overwrite) reversible or preceded by confirmation?

**Common Violations:**
- No undo after accidental deletion
- Wizard flows with no back button or escape route
- Modal dialogs that cannot be dismissed except by completing the action
- Irreversible bulk actions without confirmation

**Severity Guidance:** Irreversible destructive actions without confirmation are severity 3-4. Missing undo on low-stakes actions is severity 1-2.

---

### H4: Consistency and Standards

**Definition:** Users should not have to wonder whether different words, situations, or actions mean the same thing. Follow platform and industry conventions.

**Evaluation Checkpoints:**
1. Are similar UI elements styled and positioned consistently across screens?
2. Does the interface follow platform conventions (OS, web, mobile)?
3. Are the same terms used consistently for the same concepts throughout the application?
4. Do interactive elements (buttons, links, form controls) behave consistently?
5. Does the visual hierarchy follow established design patterns?

**Common Violations:**
- Same action labeled differently on different screens ("Save" vs. "Submit" vs. "Apply")
- Inconsistent button placement (primary action left on one screen, right on another)
- Non-standard control behavior (checkboxes that behave like radio buttons)
- Mixed visual styles for equivalent components across different sections

**Severity Guidance:** Inconsistencies that cause users to misinterpret actions are severity 3. Visual inconsistencies that do not affect task completion are severity 1.

---

### H5: Error Prevention

**Definition:** Good error messages are important, but the best designs carefully prevent problems from occurring in the first place. Either eliminate error-prone conditions, or check for them and present users with a confirmation option before they commit to the action.

**Evaluation Checkpoints:**
1. Does the interface use input constraints to prevent invalid data entry (date pickers, dropdowns)?
2. Are confirmation dialogs shown before irreversible or high-impact actions?
3. Are sensible defaults provided to reduce input errors?
4. Does real-time validation catch errors before form submission?
5. Are dangerous actions visually distinct from routine actions?

**Common Violations:**
- Free-text input where structured input (dropdown, date picker) would prevent errors
- No confirmation before permanent deletion
- Missing input format hints or masks (phone numbers, dates)
- Destructive buttons styled identically to safe buttons

**Severity Guidance:** Missing confirmation on destructive actions is severity 3-4. Absent input hints on non-critical fields are severity 1-2.

---

### H6: Recognition Rather Than Recall

**Definition:** Minimize the user's memory load by making elements, actions, and options visible. The user should not have to remember information from one part of the interface to another.

**Evaluation Checkpoints:**
1. Are options visible rather than requiring users to remember them?
2. Is contextual help available where users might need it?
3. Are recently used items, search suggestions, or autocomplete available?
4. Can users complete tasks without needing to recall codes, IDs, or values from other screens?

**Common Violations:**
- Requiring users to memorize an ID from one screen and type it into another
- Hidden menus or actions that require prior knowledge to discover
- No search suggestions or recent items in search fields
- Forms that reference information not visible on the current screen

**Severity Guidance:** Requiring recall of critical information across screens is severity 3. Missing convenience features (autocomplete, recent items) is severity 1-2.

---

### H7: Flexibility and Efficiency of Use

**Definition:** Shortcuts -- hidden from novice users -- can speed up the interaction for the expert user so that the design can cater to both inexperienced and experienced users. Allow users to tailor frequent actions.

**Evaluation Checkpoints:**
1. Are keyboard shortcuts available for frequent actions?
2. Can expert users bypass introductory steps or tutorials?
3. Does the interface support customization or personalization of frequent workflows?
4. Are there accelerators for repetitive tasks (bulk actions, templates, defaults)?

**Common Violations:**
- No keyboard shortcuts for primary actions
- Mandatory tutorials or onboarding that cannot be skipped
- No bulk action support for repetitive tasks
- No way to set personal defaults or preferences

**Severity Guidance:** Absent accelerators rarely exceed severity 2 unless the task is performed hundreds of times daily. Missing keyboard accessibility for primary navigation can be severity 3.

---

### H8: Aesthetic and Minimalist Design

**Definition:** Interfaces should not contain information which is irrelevant or rarely needed. Every extra unit of information in an interface competes with the relevant units of information and diminishes their relative visibility.

**Evaluation Checkpoints:**
1. Does the interface prioritize essential information over secondary content?
2. Is visual clutter minimized (unnecessary borders, decorations, dense layouts)?
3. Are rarely needed options appropriately hidden or collapsed?
4. Does the signal-to-noise ratio favor the user's primary task?

**Common Violations:**
- Dashboards showing all possible data with no hierarchy or filtering
- Excessive decorative elements that compete with functional content
- Settings pages showing advanced options at the same prominence as common ones
- Dense text blocks where progressive disclosure would improve scanning

**Severity Guidance:** Clutter that obscures primary task actions is severity 2-3. Purely aesthetic issues that do not impede task completion are severity 1.

---

### H9: Help Users Recognize, Diagnose, and Recover from Errors

**Definition:** Error messages should be expressed in plain language (no error codes), precisely indicate the problem, and constructively suggest a solution.

**Evaluation Checkpoints:**
1. Are error messages written in plain language (no technical codes or stack traces)?
2. Do error messages precisely identify what went wrong?
3. Do error messages suggest concrete steps to recover?
4. Are errors displayed near the relevant input or action?
5. Are error states visually distinct (color, icon, positioning)?

**Common Violations:**
- Generic error messages ("Something went wrong", "Error 500")
- Error messages that identify the problem but offer no recovery path
- Errors displayed only at the top of the page, far from the offending field
- Technical error codes or stack traces shown to end users

**Severity Guidance:** Generic errors with no recovery guidance on critical flows are severity 3-4. Poorly positioned but informative error messages are severity 2.

---

### H10: Help and Documentation

**Definition:** It is best if the system can be used without documentation. However, it may be necessary to provide help and documentation. Such information should be easy to search, focused on the user's task, list concrete steps, and not be too large.

**Evaluation Checkpoints:**
1. Is contextual help available at points where users commonly need guidance?
2. Is documentation searchable and task-oriented?
3. Are help resources easy to find without leaving the current workflow?
4. Do onboarding flows or tooltips guide new users through key features?

**Common Violations:**
- No contextual help or tooltips on complex features
- Documentation that is only accessible by leaving the application
- Help content organized by product architecture rather than user tasks
- Empty or placeholder help sections

**Severity Guidance:** Missing help on complex features that users cannot discover independently is severity 2-3. Missing help on self-explanatory features is severity 0-1.

---

## AI-Interaction Supplement Heuristics

**P-022 Disclosure:** AI-1 through AI-3 are **framework-defined evaluation supplements** for AI-driven interfaces. They are NOT published extensions of Nielsen's original 10 heuristics. They synthesize principles from:
- Amershi, S. et al. (2019). "Guidelines for Human-AI Interaction." ACM CHI 2019.
- Google PAIR (2019). "People + AI Guidebook." pair.withgoogle.com/guidebook (accessed 2026-03-04).

These supplementary heuristics are applied only when the AI Product Flag is set to true in the evaluation context. Findings from these heuristics are marked with `[AI-SUPPLEMENT]` in the report to distinguish them from Nielsen's core 10.

### AI-1: Transparency

**Definition:** The AI system should make its decision-making process, confidence levels, and data sources visible to the user in a manner appropriate to the context.

**Evaluation Checkpoints:**
1. Does the interface communicate when AI is making or influencing a decision?
2. Are confidence levels or uncertainty indicators visible to the user?
3. Can the user understand why the AI produced a specific output or recommendation?
4. Is the boundary between AI-generated and human-authored content clearly marked?

**Common Violations:**
- AI recommendations presented without any indication of confidence or certainty
- No disclosure that content was AI-generated
- Black-box decisions with no explanation or rationale accessible to the user
- AI-driven sorting or filtering with no indication of the ranking logic

**Severity Guidance:** Hidden AI decision-making on high-stakes actions (financial, medical) is severity 4. Absent confidence indicators on low-stakes suggestions are severity 1-2.

---

### AI-2: Controllability

**Definition:** Users should be able to override, correct, adjust, or disable AI behavior to maintain agency over the system's actions.

**Evaluation Checkpoints:**
1. Can the user override or dismiss AI-generated suggestions?
2. Can the user correct AI mistakes and provide feedback that improves future behavior?
3. Can the user adjust AI sensitivity, frequency, or scope of intervention?
4. Can the user disable AI features entirely if preferred?

**Common Violations:**
- AI auto-actions with no way to undo or override
- No mechanism to correct AI misclassifications or wrong suggestions
- AI features that cannot be turned off or adjusted
- Forced AI assistance with no opt-out path

**Severity Guidance:** Inability to override AI on consequential actions is severity 3-4. Missing fine-tuning controls on non-critical suggestions is severity 1-2.

---

### AI-3: Error Recovery

**Definition:** Users should be able to recover effectively when AI produces incorrect, inappropriate, or unexpected output.

**Evaluation Checkpoints:**
1. Can the user undo AI-initiated actions?
2. Is there a clear path to report or flag AI errors?
3. Does the system gracefully degrade when AI confidence is low rather than proceeding silently?
4. Can the user revert to a non-AI workflow when AI output is unsatisfactory?

**Common Violations:**
- AI-generated content that cannot be reverted to a prior state
- No mechanism to flag incorrect AI output
- AI proceeding with low-confidence actions without user confirmation
- No fallback workflow when AI features fail or produce poor results

**Severity Guidance:** Inability to revert AI-initiated destructive actions is severity 4. Missing error-flagging mechanisms on advisory AI features are severity 1-2.

> **Disambiguation: AI-3 vs. H3/H9.** AI-3 focuses specifically on AI-generated errors (model confidence failures, hallucination recovery, explanation quality for incorrect AI output). H3 (User Control and Freedom) and H9 (Help Users Recognize, Diagnose, and Recover from Errors) cover traditional interface errors and user-initiated mistakes. When an error involves AI output (wrong recommendation, low-confidence prediction, AI-generated content error), classify under AI-3. When it involves standard UI interaction (form validation, navigation mistakes, system errors unrelated to AI), classify under H3 or H9. If both AI and traditional error dimensions are present in a single finding, classify under AI-3 and note the H3/H9 overlap in the evidence field.

---

## Severity Scale

Each finding receives a severity rating on the 0-4 scale per Nielsen's severity taxonomy. Severity determines remediation priority, cross-framework handoff inclusion, and resource allocation.

> **Source:** Jakob Nielsen, "Severity Ratings for Usability Problems" (1994). Nielsen Norman Group.

| Severity | Name | Definition | Decision Criteria | Remediation Priority |
|----------|------|------------|-------------------|---------------------|
| **0** | Not a usability problem | Evaluator examined the heuristic and found no violation | Heuristic was evaluated; interface meets the standard. No user impact identified. | No action required |
| **1** | Cosmetic problem only | Issue is noticeable but does not affect task completion or user satisfaction significantly | User can complete the task without difficulty. Issue is aesthetic or involves minor label imprecision. Fix only adds polish. | Fix if extra time available |
| **2** | Minor usability problem | Issue causes minor friction or confusion but users can work around it | User experiences momentary hesitation or takes an extra step. Workaround exists and is discoverable. Low frequency of occurrence or affects non-critical flows. | Low priority; fix in future release |
| **3** | Major usability problem | Issue causes significant difficulty, task failure for some users, or repeated frustration | Users frequently struggle, abandon tasks, or require external help. No obvious workaround. Affects primary user flows or occurs with high frequency. | High priority; important to fix |
| **4** | Usability catastrophe | Issue prevents task completion entirely or causes critical data loss | Users cannot complete the task at all. The issue blocks a core workflow. May cause data loss, security exposure, or complete abandonment. | Must fix before release |

### Rating Discipline

- **Default to the lower rating** when uncertain between adjacent severities. Severity inflation without evidence violates P-022.
- A severity 3 or 4 rating **requires clear evidence** that the issue significantly impedes or prevents task completion.
- Severity 1 findings are real findings. Do not omit them, but do not conflate them with functional usability problems.
- **Frequency and impact are multipliers:** A minor violation on a high-frequency primary flow may warrant a higher severity than a major violation on a rarely used secondary feature.

### Cross-Framework Handoff Threshold

- Findings with **severity >= 2** are included in handoffs to downstream sub-skills (Behavior Design, HEART Metrics).
- Findings with **severity 0-1** remain in the full report but are not propagated to cross-framework handoffs unless specifically requested.

---

## Finding Documentation Rules

Every finding must follow the `F-{NNN}` format and include all required fields. Incomplete findings are rejected during self-review (S-010, Step 5).

### Required Fields Per Finding

```markdown
### Finding F-{NNN}: {brief description}

- **Heuristic:** H{N} -- {heuristic name}  (or AI-{N} -- {name} for supplements)
- **Severity:** {0-4} ({Nielsen severity name})
- **Screen/Flow:** {affected screen or user flow identifier}
- **Evidence:** {specific interface observation demonstrating the violation}
- **Remediation:** {actionable fix recommendation}
- **Effort:** {Low | Medium | High}
```

### Field Requirements

| Field | Requirement | Rejection Criterion |
|-------|-------------|---------------------|
| Finding ID | Sequential `F-{NNN}` in ranked order (assigned in Step 4) | Non-sequential, duplicate, or missing ID |
| Heuristic | Must reference a valid heuristic (H1-H10 or AI-1 through AI-3) | Invalid heuristic reference |
| Severity | Integer 0-4 with the corresponding Nielsen severity name in parentheses | Missing severity, out of range, or missing name |
| Screen/Flow | Specific screen name, flow step, or page identifier | Vague references ("some page", "the app") |
| Evidence | Observable interface artifact: what the evaluator saw that constitutes the violation | Absent evidence, generic assertions ("this is bad"), or claims without interface reference |
| Remediation | Actionable recommendation: what to change and how | Vague advice ("make it better"), or recommendations that merely restate the problem |
| Effort | One of: Low, Medium, High | Missing or non-standard effort classification |

### Evidence Quality Standard

Evidence must reference specific, observable interface artifacts. Acceptable evidence includes:
- "The 'Save' button produces no visual feedback after click -- no spinner, no confirmation toast, no state change"
- "The error message reads 'Error 422' with no plain-language explanation or recovery suggestion"
- "The settings page uses 'Provisioning Cadence' while the dashboard uses 'Update Schedule' for the same feature"

Unacceptable evidence includes:
- "The form feels confusing" (subjective, no specific observation)
- "Users probably struggle here" (speculative, no interface artifact)
- "This violates H1" (circular, restates the heuristic without evidence)

### Effort Classification Criteria

Each finding must include an Effort estimate of Low, Medium, or High. Use the following criteria:

| Effort | Scope | Logic Impact | Estimated Time |
|--------|-------|-------------|----------------|
| **Low** | CSS or content change, single component affected, no logic changes | None | < 1 hour |
| **Medium** | Component restructuring, minor logic changes, may affect 2-3 related components | Minor | 1-4 hours |
| **High** | Architecture change, new component creation, API modifications, cross-system dependencies | Significant | > 4 hours |

When uncertain between adjacent effort levels, default to the higher estimate. Effort estimates are independent of severity -- a severity 4 finding may have Low effort (e.g., a missing confirmation dialog is critical but simple to add), and a severity 1 finding may have High effort (e.g., a cosmetic inconsistency requiring design system refactoring).

**Note:** Time estimates assume a typical React/web application stack. Adjust proportionally for unfamiliar or complex technology stacks.

---

## Deduplication Rules

When the same heuristic violation appears across multiple screens, the evaluator must decide whether findings count as one pattern or separate findings. Deduplication occurs in Step 4 of the evaluation workflow.

### Same Finding (Consolidate)

Consolidate into a single finding when ALL of the following are true:
1. The **same heuristic** is violated (e.g., H4 on both screens)
2. The **same root cause** produces the violation (e.g., inconsistent button placement from a shared layout template)
3. The **same remediation** would fix all instances (e.g., updating the shared component)

When consolidated, list ALL affected screens in the `Screen/Flow` field. Severity reflects the worst-case impact across all affected screens.

### Separate Findings (Do Not Consolidate)

Record as separate findings when ANY of the following are true:
1. **Different heuristics** are violated, even if the same screen element is involved
2. The **root causes differ**, even if the same heuristic is violated (e.g., H9 violated by generic error messages on the login page and by missing error positioning on the checkout page)
3. **Different remediations** are needed to fix each instance

### Edge Cases

| Scenario | Decision | Rationale |
|----------|----------|-----------|
| Same component, different heuristics | Separate findings | Each heuristic violation is independently documented |
| Same heuristic, shared component across screens | One finding, list all screens | Single root cause, single remediation |
| Same heuristic, similar but independent violations | Separate findings | Different root causes require different remediations |
| Cross-screen consistency issue (H4) | One finding if systemic | Systemic inconsistency is a single pattern |

---

## Single-Evaluator Reliability

### P-022 Disclosure

Nielsen's heuristic evaluation methodology recommends **3-5 independent evaluators** for reliable usability problem detection. Research shows that individual evaluators typically find only **35% of usability problems**, with the aggregate across 3-5 evaluators reaching **75-80% coverage** (Nielsen, 1994c: "How to Conduct a Heuristic Evaluation").

This sub-skill operates with a **single AI evaluator**. Users should understand both the compensating strengths and the residual limitations of this approach.

### How AI-Augmented Single Evaluation Compensates

| Human Single-Evaluator Weakness | AI Compensation |
|--------------------------------|-----------------|
| Heuristic omission bias (unconsciously focusing on a subset of heuristics) | Systematic sequential application of all 10 heuristics to every screen -- no heuristic is skipped |
| Fatigue-driven coverage gaps on later screens | Consistent evaluation depth across all screens regardless of count |
| Expertise-biased severity calibration | Consistent application of the 0-4 severity scale with the same criteria across all findings |

### Residual Limitations Not Mitigated

| Limitation | Impact | Recommendation |
|------------|--------|----------------|
| No perspective diversity | Context-specific issues requiring domain expertise, cultural familiarity, or embodied interaction experience may be missed | Supplement with at least one human evaluator for severity 3-4 findings |
| No hands-on interaction | Issues discoverable only through live interaction (gesture feel, animation timing, haptic feedback) cannot be evaluated from screenshots | Note as a coverage gap when operating in screenshot-input mode |
| Systematic AI blind spots | AI may overweight visual design heuristics and underweight interaction flow heuristics | Cross-reference findings distribution across heuristics; flag if 3+ heuristics have zero findings |
| Training data recency | AI evaluation reflects patterns from training data, not current design conventions | Use Context7 or web search for current platform guidelines when evaluating H4 |

### High-Stakes Evaluation Recommendation

For findings rated **severity 3 or 4**, supplement the AI evaluation with at least one human evaluator review before making major design decisions. This is especially important when:
- The product serves specialized user populations (medical, legal, accessibility-dependent)
- Findings will drive significant engineering investment (> 1 sprint of effort)
- The evaluation was conducted in screenshot-input degraded mode without interactive observation

---

## Report Structure

The evaluation output report must include all sections listed below. The structure follows the L0/L1/L2 output level pattern per AD-M-004.

### Required Sections

| # | Section | Level | Content Requirements |
|---|---------|-------|---------------------|
| 1 | **Document Sections** (navigation table) | -- | H-23 navigation table with Section and Purpose columns; all major sections listed with anchor links |
| 2 | **Executive Summary** | L0 | Top 3-5 findings by severity with one-line descriptions; severity distribution (count per level 0-4); overall usability assessment (one paragraph); heuristic coverage confirmation ("All 10 heuristics evaluated across N screens") |
| 3 | **Evaluation Context** | L1 | Product name and domain; target users; screens or flows evaluated (list); input modality (Figma / screenshot / text); MCP status; evaluation scope (screen-level or flow-level); degraded mode disclosure if applicable |
| 4 | **Findings by Heuristic** | L1 | Organized by heuristic (H1 through H10, then AI-1 through AI-3 if applicable); each finding in the F-{NNN} format defined in [Finding Documentation Rules](#finding-documentation-rules); heuristics with no findings noted as "No violations identified" |
| 5 | **Ranked Findings Summary** | L1 | Single table with all findings ranked by severity descending; columns: Finding ID, Heuristic, Severity, Screen/Flow, Brief Description, Effort |
| 6 | **Remediation Roadmap** | L1 | Findings grouped by effort (Low, Medium, High); within each group, ordered by severity descending; suggested implementation order |
| 7 | **Strategic Implications** | L2 | Cross-product usability patterns; organizational UX maturity observations; design evolution recommendations; areas where the evaluation suggests systemic issues beyond individual findings |
| 8 | **Synthesis Judgments Summary** | L1 | Each AI judgment call listed with rationale. Exhaustive judgment call types for this sub-skill: (a) severity calibration judgments (choosing between adjacent severity levels), (b) deduplication decisions (consolidate vs. separate per [Deduplication Rules](#deduplication-rules)), (c) effort estimates (Low/Medium/High assignment per [Effort Classification Criteria](#effort-classification-criteria)), (d) AI-supplement applicability decisions (classifying under AI-1/AI-2/AI-3 vs. Nielsen H1-H10), (e) cross-heuristic pattern grouping (identifying systemic patterns across multiple heuristics). The full confidence classification protocol (HIGH/MEDIUM/LOW) is defined in `skills/user-experience/rules/synthesis-validation.md` and applies across all sub-skills. |
| 9 | **Handoff Data** | L1 | Structured table for downstream sub-skill consumption; columns: Finding ID, Heuristic, Severity, Affected Screen, Candidate HEART Category; only findings with severity >= 2 included |

### Section Ordering

Sections must appear in the order listed above (1-9). The navigation table (section 1) appears immediately after the document title. This ordering ensures L0 readers can stop after the Executive Summary, L1 readers can navigate to specific heuristics or the ranked summary, and L2 readers can find strategic implications at the end.

### Heuristic-to-HEART Category Mapping

The following table provides candidate mappings from Nielsen heuristics to HEART metric categories for populating the "Candidate HEART Category" column in section 9 (Handoff Data). This mapping is a starting heuristic for the evaluator -- downstream `/ux-heart-metrics` confirms final categorization.

| Heuristic | Candidate HEART Category | Rationale |
|-----------|-------------------------|-----------|
| H1 (Visibility of System Status) | Engagement | Feedback quality drives continued interaction |
| H2 (Match Between System and Real World) | Task Success | Terminology comprehension directly affects task completion |
| H3 (User Control and Freedom) | Task Success | Undo/escape paths affect whether users complete or abandon tasks |
| H4 (Consistency and Standards) | Happiness | Consistent interfaces produce satisfaction and reduce frustration |
| H5 (Error Prevention) | Task Success | Preventing errors directly affects task completion rates |
| H7 (Flexibility and Efficiency) | Engagement | Accelerators drive expert engagement and repeated use |
| H10 (Help and Documentation) | Happiness | Accessible help contributes to overall satisfaction |

> **Note:** HEART framework: Rodden, Hutchinson, and Fu (2010), "Measuring the User Experience on a Large Scale." H6 (Recognition), H8 (Aesthetic Design), and H9 (Error Recovery) do not have a single dominant HEART mapping -- assign based on the specific finding context. H6 (Recognition): Map to Happiness when the finding relates to user satisfaction, or Task Success when it relates to error handling. H8 (Aesthetic): Map to Happiness when the finding relates to user satisfaction, or Task Success when it relates to error handling. H9 (Error Recovery): Map to Happiness when the finding relates to user satisfaction, or Task Success when it relates to error handling. AI-1 through AI-3: Map to Task Success for functional AI failures, Happiness for trust/satisfaction impacts.

### Self-Review Checklist (S-010)

Before persisting the report, the evaluator must verify:

1. All 10 heuristics were evaluated for every screen (no heuristic skipped)
2. Every finding has all required fields per [Finding Documentation Rules](#finding-documentation-rules)
3. Every finding has specific interface evidence (not generic assertions)
4. Findings are deduplicated per [Deduplication Rules](#deduplication-rules)
5. Findings are ranked by severity descending in the Ranked Findings Summary
6. The navigation table is present with correct anchor links (H-23)
7. Degraded mode disclosure is present if operating without Figma MCP
8. The Synthesis Judgments Summary lists each AI judgment call
9. Handoff Data includes only severity >= 2 findings
10. Finding IDs are sequential (`F-001`, `F-002`, ...) with no gaps

---

*Rule file: heuristic-evaluation-rules.md*
*Version: 1.2.0*
*Parent sub-skill: /ux-heuristic-eval*
*Parent skill: /user-experience*
*Agent: ux-heuristic-evaluator*
*SSOT: `skills/ux-heuristic-eval/SKILL.md`*
*Created: 2026-03-04*

<!-- Traceability: PROJ-022 EPIC-002, FEAT-005. Standards: H-23 (navigation), H-34 (agent-dev), SR-002 (input validation), SR-003 (output filtering). Methodology: Nielsen (1994), Amershi et al. (2019), Google PAIR (2019). ORCHESTRATION: projects/PROJ-022-user-experience-skill/orchestration/ux-skill-build-20260303-001/ORCHESTRATION.yaml -->
<!-- VERSION: 1.2.0 | DATE: 2026-03-04 | SOURCE: skills/ux-heuristic-eval/SKILL.md, skills/ux-heuristic-eval/agents/ux-heuristic-evaluator.md, Nielsen (1994a, 1994b, 1994c, 2020), Amershi et al. (2019), Google PAIR (2019) | REVISION: Iter3 quality fixes -- Google PAIR access date, HEART attribution, ORCHESTRATION.yaml traceability, effort tech note, synthesis-validation clarification, unmapped HEART guidance -->
