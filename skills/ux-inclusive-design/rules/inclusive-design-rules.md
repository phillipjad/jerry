<!-- VERSION: 1.1.0 | DATE: 2026-03-04 | SOURCE: skills/ux-inclusive-design/SKILL.md, skills/ux-inclusive-design/agents/ux-inclusive-evaluator.md | PARENT: /ux-inclusive-design sub-skill | REVISION: iter2 -- fix Robust POUR criterion count (A:0→A:1, AA:2→AA:1), add PS-001 through PS-003 to GOVERNANCE ID INDEX, add P-022 limitations disclosure rule (LM-001), add IP-003 scope guidance, add CG-001 non-English text rule -->

# Inclusive Design Methodology Rules

> Operational constraints and methodology rules for the `ux-inclusive-evaluator` agent. Provides WCAG 2.2 POUR evaluation rules, conformance level determination, success criteria evaluation format, Microsoft Inclusive Design Persona Spectrum methodology rules, color contrast thresholds, keyboard navigation test protocol, screen reader compatibility test protocol, cognitive load assessment protocol, severity scale alignment, and quality gate integration. This file is the SSOT for how the ux-inclusive-evaluator agent applies the dual-framework accessibility evaluation methodology.

## Document Sections

| Section | Purpose |
|---------|---------|
| [Workflow Phase Sequencing Rules](#workflow-phase-sequencing-rules) | Explicit phase-order constraints for the 7-step evaluation workflow |
| [WCAG 2.2 POUR Evaluation Rules](#wcag-22-pour-evaluation-rules) | Per-principle evaluation requirements and conformance level determination |
| [Success Criteria Evaluation Format Rules](#success-criteria-evaluation-format-rules) | Per-criterion output format, required fields, severity-decision rules |
| [Severity Scale](#severity-scale) | 0-4 severity scale with Nielsen alignment and cross-framework synthesis support |
| [Microsoft Inclusive Design Rules](#microsoft-inclusive-design-rules) | Three principles, Persona Spectrum methodology, cell population rules |
| [Persona Spectrum Methodology Rules](#persona-spectrum-methodology-rules) | 4x3 matrix rules, interaction pattern identification, mapping discipline |
| [Color Contrast Assessment Rules](#color-contrast-assessment-rules) | Threshold tables, computation requirements, degraded mode constraints |
| [Keyboard Navigation Test Protocol](#keyboard-navigation-test-protocol) | Tab order, focus visibility, keyboard trap, shortcut conflict test rules |
| [Screen Reader Compatibility Test Protocol](#screen-reader-compatibility-test-protocol) | Heading hierarchy, ARIA landmarks, alt text, form labels, live regions |
| [Cognitive Load Assessment Protocol](#cognitive-load-assessment-protocol) | Reading level, navigation consistency, error prevention, input assistance |
| [Conformance Level Determination Rules](#conformance-level-determination-rules) | How to determine achieved conformance level from per-criterion results |
| [Remediation Priority Rules](#remediation-priority-rules) | Priority ranking methodology, WCAG technique referencing |
| [Quality Gate Integration](#quality-gate-integration) | How scores map to S-014 rubric dimensions |
| [Self-Review Checklist](#self-review-checklist) | S-010 verification before output persistence |
| [Limitations Disclosure Rules](#limitations-disclosure-rules) | P-022 minimum disclosure obligations for evaluation reports |
| [References](#references) | Source citations and traceability |

---

## Workflow Phase Sequencing Rules

The inclusive design evaluation follows a 7-step sequential workflow. Steps MUST execute in order -- no step may be skipped or reordered. Each step produces intermediate findings that feed subsequent steps.

> **Source:** Dual-framework evaluation workflow defined in `skills/ux-inclusive-design/agents/ux-inclusive-evaluator.md` `<methodology>` section. WCAG 2.2 POUR evaluation sequence from W3C (2023). Microsoft Inclusive Design methodology from Microsoft (2016).

### Phase Order Constraint

| Rule ID | Rule | Consequence of Violation |
|---------|------|-------------------------|
| EV-001 | Steps MUST execute in the sequence: Step 1 (Context Gathering) then Step 2 (WCAG 2.2 POUR Audit) then Step 3 (Color Contrast) then Step 4 (Keyboard Navigation) then Step 5 (Screen Reader + Cognitive Load) then Step 6 (Persona Spectrum) then Step 7 (Synthesis + Report) | Evaluating Persona Spectrum (Step 6) without WCAG findings (Steps 2-5) produces exclusion analysis disconnected from compliance evidence; synthesizing without complete findings produces incomplete reports |
| EV-002 | Each step MUST complete before the next step begins -- partial step outputs MUST NOT be carried forward as complete | Downstream steps operating on incomplete upstream findings propagate gaps; conformance determination becomes unreliable |
| EV-003 | Step 1 (Context Gathering) MUST determine Figma MCP availability and activate degraded mode (screenshot-input) before Step 2 begins | Late mode detection requires re-evaluation of color contrast findings (Step 3) and component hierarchy assessments |
| EV-004 | Step 2 (WCAG 2.2 POUR Audit) MUST evaluate all four principles (P, O, U, R) sequentially -- principles MUST NOT be skipped unless the entire principle is not applicable to the input artifacts | Skipping a principle without N/A justification creates gaps in conformance determination |
| EV-005 | Steps 3, 4, and 5 MUST reference findings from Step 2 to avoid duplication -- if a success criterion was already evaluated in Step 2 with sufficient evidence, the specialized protocol in Steps 3-5 adds detail, not duplicates | Duplication inflates finding counts and creates inconsistent severity assignments for the same criterion |

### Step Summary

| Step | Name | Input | Output | Rules Governing Content |
|------|------|-------|--------|------------------------|
| 1 | Context Gathering | UX CONTEXT handoff data | Context brief: scope, input inventory, target level, MCP status | Input validation rules in agent definition `<input>` section |
| 2 | WCAG 2.2 POUR Audit | Context brief, input artifacts | Per-criterion findings organized by principle | [WCAG 2.2 POUR Evaluation Rules](#wcag-22-pour-evaluation-rules), [Success Criteria Evaluation Format Rules](#success-criteria-evaluation-format-rules) |
| 3 | Color Contrast Assessment | Input artifacts, Step 2 Perceivable findings | Per-element contrast ratio measurements | [Color Contrast Assessment Rules](#color-contrast-assessment-rules) |
| 4 | Keyboard Navigation Audit | Input artifacts, Step 2 Operable findings | Focus order, visibility, trap, shortcut findings | [Keyboard Navigation Test Protocol](#keyboard-navigation-test-protocol) |
| 5 | Screen Reader + Cognitive Load | Input artifacts, Step 2 findings | Semantic HTML, ARIA, reading level, error prevention findings | [Screen Reader Compatibility Test Protocol](#screen-reader-compatibility-test-protocol), [Cognitive Load Assessment Protocol](#cognitive-load-assessment-protocol) |
| 6 | Persona Spectrum Analysis | All WCAG findings from Steps 2-5 | Per-interaction-pattern persona spectrum profiles | [Microsoft Inclusive Design Rules](#microsoft-inclusive-design-rules), [Persona Spectrum Methodology Rules](#persona-spectrum-methodology-rules) |
| 7 | Synthesis + Report | All findings from Steps 2-6 | Complete evaluation report with remediation priorities | [Remediation Priority Rules](#remediation-priority-rules), [Quality Gate Integration](#quality-gate-integration) |

---

## WCAG 2.2 POUR Evaluation Rules

WCAG 2.2 organizes accessibility requirements into four principles (POUR), each containing guidelines with testable success criteria at three conformance levels (A, AA, AAA).

> **Source:** W3C (2023). Web Content Accessibility Guidelines (WCAG) 2.2. W3C Recommendation, 05 October 2023.

### Principle Evaluation Order

| Rule ID | Rule | Consequence of Violation |
|---------|------|-------------------------|
| PR-001 | Principles MUST be evaluated in POUR order: Perceivable, Operable, Understandable, Robust | Consistent ordering enables cross-engagement comparison and ensures no principle is inadvertently skipped |
| PR-002 | Within each principle, guidelines MUST be evaluated in numerical order (e.g., 1.1 before 1.2 before 1.3 before 1.4 for Perceivable) | Numerical ordering ensures systematic coverage and enables reviewers to verify completeness |
| PR-003 | Within each guideline, success criteria MUST be evaluated up to and including the target conformance level | Evaluating Level A criteria is mandatory for all targets; Level AA criteria are additionally required for AA and AAA targets; Level AAA criteria are additionally required only for AAA targets |

### Principle Scope Rules

| Rule ID | Rule | Consequence of Violation |
|---------|------|-------------------------|
| PS-001 | All four POUR principles MUST be evaluated -- no principle may be omitted without explicit N/A justification | Omitting a principle creates gaps in conformance determination; the achieved level cannot be determined without coverage of all principles |
| PS-002 | A principle is marked N/A only when the input artifacts contain no content addressable by that principle (e.g., Robust is N/A when no markup or code is available for evaluation) | False N/A marks suppress genuine findings; N/A must reflect genuine inapplicability, not evaluation difficulty |
| PS-003 | When a principle is marked N/A, the output MUST include a justification explaining why no content is addressable by that principle | Unjustified N/A marks cannot be distinguished from skipped evaluations |

### Conformance Level Scope Rules

| Rule ID | Rule | Consequence of Violation |
|---------|------|-------------------------|
| CL-001 | When the target is A, evaluate all Level A success criteria | Level A is the minimum accessibility floor |
| CL-002 | When the target is AA, evaluate all Level A AND Level AA success criteria | AA conformance requires meeting all A and AA criteria (W3C, 2023) |
| CL-003 | When the target is AAA, evaluate all Level A, Level AA, AND Level AAA success criteria | AAA conformance requires meeting all criteria at all levels |
| CL-004 | The evaluator MAY note AAA-level findings even when the target is A or AA, but MUST mark them as beyond-scope recommendations, not conformance failures | AAA findings provide improvement opportunities but should not inflate the failure count for a lower target |

### POUR Principle Reference

| Principle | Letter | Key Guidelines | Success Criteria Count (WCAG 2.2) |
|-----------|--------|---------------|-----------------------------------|
| Perceivable | P | 1.1 Text Alternatives, 1.2 Time-Based Media, 1.3 Adaptable, 1.4 Distinguishable | A: 9, AA: 7, AAA: 6 |
| Operable | O | 2.1 Keyboard, 2.2 Enough Time, 2.3 Seizures, 2.4 Navigable, 2.5 Input Modalities | A: 9, AA: 8, AAA: 7 |
| Understandable | U | 3.1 Readable, 3.2 Predictable, 3.3 Input Assistance | A: 5, AA: 4, AAA: 6 |
| Robust | R | 4.1 Compatible | A: 1, AA: 1, AAA: 0 |

**Note:** WCAG 2.2 removed SC 4.1.1 (Parsing) from Level A. The criterion count reflects the current WCAG 2.2 specification. SC 4.1.2 (Name, Role, Value) and 4.1.3 (Status Messages) are Level A and AA respectively.

---

## Success Criteria Evaluation Format Rules

Every WCAG 2.2 success criterion evaluated MUST follow the canonical per-criterion format.

> **Source:** Agent definition `<methodology>` Step 2 [Per-criterion evaluation format]. Nielsen (1994b) severity scale.

### Required Fields

| Rule ID | Rule | Consequence of Violation |
|---------|------|-------------------------|
| SC-001 | Every criterion evaluation MUST include all five fields: Status, Evidence, Affected Elements, Severity, Remediation | Incomplete criterion evaluations cannot be used for conformance determination or remediation planning |
| SC-002 | Status MUST be one of exactly three values: PASS, FAIL, or NOT APPLICABLE | Non-standard status values (e.g., "PARTIAL", "NEEDS REVIEW") create ambiguity; use FAIL with appropriate severity for partial failures |
| SC-003 | Evidence MUST describe specific observations, measurements, or test results -- not restatements of the success criterion itself | "No alt text found on hero image" is evidence; "Non-text content lacks text alternatives" is a criterion restatement, not evidence |
| SC-004 | Affected Elements MUST reference specific UI elements by selector, component name, or screen location | "Multiple elements" is insufficient; "Hero image in the product listing card" or "All form inputs in the checkout step 2 form" is specific |
| SC-005 | Severity MUST use the 0-4 scale defined in [Severity Scale](#severity-scale) | Non-standard severity values prevent cross-framework synthesis with `/ux-heuristic-eval` |
| SC-006 | Remediation MUST reference a specific WCAG technique (e.g., "Apply ARIA-label per Technique ARIA14") when a technique exists | Remediation without technique references is not actionable for engineering teams |

### Severity-Decision Rules

| Rule ID | Rule | Consequence of Violation |
|---------|------|-------------------------|
| SD-001 | PASS criteria MUST always receive severity 0 | Assigning severity > 0 to a PASS finding creates contradictory status/severity pairs |
| SD-002 | Severity 1-4 MUST only be applied to FAIL findings | Severity on non-FAIL findings inflates barrier counts |
| SD-003 | NOT APPLICABLE criteria do not receive a severity rating -- omit the severity field or mark "N/A" | N/A criteria have no user impact to rate |
| SD-004 | Severity assignment for FAIL findings is an AI judgment classified as MEDIUM synthesis confidence | Presenting AI-assigned severity as objective measurement violates P-022 |

### Per-Criterion Output Format

```
### SC {X.Y.Z}: {Success Criterion Name} [{Level}]

- **Status:** PASS | FAIL | NOT APPLICABLE
- **Evidence:** {specific observation, measurement, or test result}
- **Affected Elements:** {UI element references, selectors, or screen locations}
- **Severity:** 0 (not a problem) | 1 (cosmetic) | 2 (minor barrier) | 3 (major barrier) | 4 (critical -- blocks access)
- **Remediation:** {specific fix with WCAG technique reference, e.g., "Apply ARIA-label per Technique ARIA14"}
```

---

## Severity Scale

The severity scale aligns with Nielsen's severity rating scale (Nielsen, 1994b) to enable cross-framework synthesis with `/ux-heuristic-eval` findings.

> **Source:** Nielsen, J. (1994b). Severity ratings for usability problems. In *Usability Inspection Methods*, pp. 413-414. John Wiley & Sons. Scale adapted for accessibility context per `skills/ux-inclusive-design/SKILL.md` [Success Criteria Evaluation Format].

| Severity | Label | Accessibility Interpretation | Nielsen Alignment | Action |
|----------|-------|------------------------------|-------------------|--------|
| 0 | Not a problem | The criterion passes; no accessibility barrier exists | Not a usability problem | No action needed |
| 1 | Cosmetic | Minor accessibility issue that does not impede task completion; fix if time permits | Cosmetic problem only | Low priority; address in future sprints |
| 2 | Minor barrier | Accessibility barrier that causes some difficulty but users can work around it | Minor usability problem | Fix with low priority; users can complete tasks with extra effort |
| 3 | Major barrier | Significant accessibility barrier that causes serious difficulty for affected users | Major usability problem | Important to fix; high priority; significantly impedes affected users |
| 4 | Critical -- blocks access | Accessibility barrier that completely prevents task completion for affected users | Usability catastrophe | Must fix before release; prevents task completion entirely |

### Cross-Framework Severity Correspondence

| Severity | Inclusive Design Interpretation | Heuristic Eval Interpretation | Synthesis Signal |
|----------|-------------------------------|-------------------------------|-----------------|
| 0 | WCAG criterion passes | Nielsen heuristic not violated | No convergence signal |
| 1 | Cosmetic accessibility issue | Cosmetic usability issue | Weak convergence -- low priority |
| 2 | Minor accessibility barrier | Minor usability problem | Moderate convergence -- validate with users |
| 3 | Major accessibility barrier | Major usability problem | Strong convergence -- high priority remediation |
| 4 | Access blocked entirely | Usability catastrophe | Critical convergence -- must fix |

**Handoff threshold:** Only findings with severity >= 2 are included in cross-framework synthesis handoffs. Severity 0 and 1 findings remain in the full audit report but are excluded from synthesis signal extraction.

---

## Microsoft Inclusive Design Rules

Microsoft Inclusive Design methodology (Microsoft, 2016) complements WCAG compliance with a design-thinking approach.

> **Source:** Microsoft (2016). Microsoft Inclusive Design Toolkit. microsoft.com/design/inclusive.

### Three Principles Application Rules

| Rule ID | Rule | Consequence of Violation |
|---------|------|-------------------------|
| ID-001 | **Recognize Exclusion:** For each interaction pattern, the evaluator MUST identify specific design decisions that create barriers for users with permanent, temporary, or situational impairments | Failing to identify exclusion points produces Persona Spectrum profiles without actionable design direction |
| ID-002 | **Solve for One, Extend to Many:** Each Persona Spectrum profile MUST identify how solving for the permanent disability scenario extends benefits to temporary and situational users | Omitting the extension analysis misses the core value proposition of inclusive design -- solutions that benefit the broadest range of users |
| ID-003 | **Learn from Diversity:** When accessible, the evaluator SHOULD note adaptation strategies developed by people with disabilities that inform design improvements | Adaptation strategies provide design insights that complement WCAG technique references |

### Persona Spectrum Application Rules

| Rule ID | Rule | Consequence of Violation |
|---------|------|-------------------------|
| PS-010 | A Persona Spectrum profile MUST be produced for each interaction pattern identified in the evaluated interface | Missing interaction patterns create gaps in exclusion analysis |
| PS-011 | Each Persona Spectrum profile MUST use the 4x3 matrix format: 4 disability types (Visual, Motor, Auditory, Cognitive) x 3 duration categories (Permanent, Temporary, Situational) | Non-standard matrix dimensions prevent cross-engagement comparison |
| PS-012 | Every cell in the 4x3 matrix MUST be populated -- when a scenario is not applicable, explicitly state "Low exclusion risk for this combination" rather than leaving the cell empty | Empty cells create ambiguity between "not evaluated" and "not applicable"; complete population ensures systematic coverage |
| PS-013 | Each Persona Spectrum profile MUST include three summary fields: Exclusion Points, Design Opportunity, and Current Compliance (WCAG success criteria cross-reference) | Summary fields connect the Persona Spectrum analysis back to actionable WCAG findings |
| PS-014 | Persona Spectrum profiles are classified as MEDIUM synthesis confidence -- they are heuristic models (Microsoft, 2016), not empirically grounded user research | Presenting AI-generated persona scenarios as validated user profiles violates P-022 |

---

## Persona Spectrum Methodology Rules

### Interaction Pattern Identification

| Rule ID | Rule | Consequence of Violation |
|---------|------|-------------------------|
| IP-001 | The evaluator MUST identify interaction patterns from the input artifacts during Step 1 (Context Gathering) | Late identification of interaction patterns delays Persona Spectrum analysis and may result in incomplete coverage |
| IP-002 | Each interaction pattern describes a discrete user task or action (e.g., "complete checkout form", "navigate product catalog", "read notification") | Overly broad patterns (e.g., "use the application") produce generic Persona Spectrum profiles with low analytical value |
| IP-003 | The evaluator SHOULD identify at minimum 2 interaction patterns per evaluated interface or flow. For complex flows with many potential interaction patterns, prioritize patterns where WCAG FAIL findings with severity >= 2 were identified in Steps 2-5 | Single-pattern analysis may miss interaction-specific barriers; complex flows typically contain multiple distinct interaction patterns. Scope guidance prevents unbounded pattern proliferation on complex products |

### 4x3 Matrix Format

Each interaction pattern produces one Persona Spectrum profile using the following matrix:

| Disability Type | Permanent | Temporary | Situational |
|----------------|-----------|-----------|-------------|
| **Visual** | {scenario: e.g., blind user} | {scenario: e.g., post-surgery} | {scenario: e.g., bright sunlight} |
| **Motor** | {scenario: e.g., single arm} | {scenario: e.g., arm in cast} | {scenario: e.g., holding child} |
| **Auditory** | {scenario: e.g., deaf user} | {scenario: e.g., ear infection} | {scenario: e.g., loud environment} |
| **Cognitive** | {scenario: e.g., learning disability} | {scenario: e.g., concussion} | {scenario: e.g., distracted by children} |

### Matrix Population Rules

| Rule ID | Rule | Consequence of Violation |
|---------|------|-------------------------|
| MX-001 | Each cell MUST contain a plausible user scenario specific to the interaction pattern -- not a generic disability description | "Blind user" without context of the specific interaction (e.g., "Blind user navigating product filter controls") produces non-actionable analysis |
| MX-002 | Scenarios MUST progress across the Permanent-Temporary-Situational spectrum in decreasing severity of impairment for the same disability type | Scenarios that do not follow the P-T-S progression obscure the "solve for one, extend to many" design insight |
| MX-003 | When a disability type and interaction pattern combination genuinely has low exclusion risk, state "Low exclusion risk for this combination: {brief reason}" | Unjustified low-risk claims mask evaluation gaps |

---

## Color Contrast Assessment Rules

Color contrast ratios are evaluated against WCAG 2.2 success criteria for distinguishable content.

> **Source:** W3C (2023). WCAG 2.2 Success Criteria 1.4.3 (Contrast Minimum, AA), 1.4.6 (Contrast Enhanced, AAA), 1.4.11 (Non-text Contrast, AA), 2.4.11 (Focus Appearance, AA, new in 2.2).

### Contrast Threshold Table

| Test | Element Type | Threshold (AA) | Threshold (AAA) | WCAG Criterion |
|------|-------------|----------------|-----------------|----------------|
| Normal text contrast | Text < 18pt and not bold | >= 4.5:1 | >= 7:1 | 1.4.3 / 1.4.6 |
| Large text contrast | Text >= 18pt OR text >= 14pt bold | >= 3:1 | >= 4.5:1 | 1.4.3 / 1.4.6 |
| UI component contrast | Non-text UI components and graphical objects | >= 3:1 | >= 3:1 | 1.4.11 |
| Focus indicator contrast | Focus visible indicator against adjacent colors | >= 3:1 | >= 3:1 | 2.4.11 (new in 2.2) |

### Contrast Evaluation Rules

| Rule ID | Rule | Consequence of Violation |
|---------|------|-------------------------|
| CC-001 | Every contrast evaluation MUST include foreground color, background color, computed ratio, target threshold, and pass/fail status | Incomplete contrast data prevents verification of the pass/fail determination |
| CC-002 | Color values MUST be specified as hex (#RRGGBB) or RGB (rgb(R, G, B)) format | Non-standard color formats prevent ratio computation verification |
| CC-003 | NEVER claim PASS for a contrast check without a computed ratio from hex/RGB values | Visual estimation from screenshots is not precise enough for compliance determination; unverified PASS claims create false legal compliance confidence |
| CC-004 | In degraded mode (screenshot-input), elements with potentially insufficient contrast MUST be flagged for manual measurement with the note: "Manual verification required -- hex/RGB values not available from screenshot" | Omitting the degraded mode flag conceals measurement limitations |
| CC-005 | Large text determination (>= 18pt or >= 14pt bold) MUST be documented per element -- do not assume text size without evidence | Incorrect large/normal text classification applies the wrong threshold, potentially producing false PASS results |

### Per-Element Output Format

| Element | Foreground | Background | Ratio | Target | Status |
|---------|-----------|-----------|-------|--------|--------|
| {element reference} | {hex/RGB} | {hex/RGB} | {computed ratio}:1 | {threshold for target level} | PASS / FAIL |

---

## Keyboard Navigation Test Protocol

Keyboard navigation is evaluated against WCAG 2.2 Operable principle success criteria.

> **Source:** W3C (2023). WCAG 2.2 Guideline 2.1 (Keyboard Accessible), Guideline 2.4 (Navigable).

### Test Matrix

| Test | Evaluation Criteria | WCAG Criterion | Level |
|------|-------------------|----------------|-------|
| Tab order completeness | All interactive elements reachable via Tab/Shift+Tab | 2.1.1 | A |
| Focus visibility | Focus indicator visible on all focused elements | 2.4.7 (AA), 2.4.11 (AA, new in 2.2) | AA |
| No keyboard traps | Focus can be moved away from all components via standard keyboard keys | 2.1.2 | A |
| Shortcut conflicts | Single character key shortcuts can be turned off or remapped | 2.1.4 (A, added in WCAG 2.1; retained in 2.2) | A |
| Skip navigation | Skip-to-content mechanism available | 2.4.1 | A |
| Focus not obscured | Focused element not fully hidden by other content (e.g., sticky headers, modals) | 2.4.12 (AA, new in 2.2) | AA |

### Keyboard Test Rules

| Rule ID | Rule | Consequence of Violation |
|---------|------|-------------------------|
| KB-001 | Every keyboard navigation issue MUST document: affected element, expected behavior, observed behavior, and WCAG criterion violated | Incomplete keyboard findings cannot be reproduced or remediated by engineering teams |
| KB-002 | Tab order evaluation MUST assess logical reading order, not just reachability -- elements reachable in an illogical order are a finding (severity 2-3) | Tab order that reaches all elements but in a confusing order creates cognitive barriers |
| KB-003 | Focus visibility MUST be evaluated for both default browser focus indicators and custom focus styles | Custom focus styles may be less visible than browser defaults; both must meet the 3:1 contrast requirement (2.4.11) |
| KB-004 | Keyboard trap detection MUST test both Tab and Escape key as exit mechanisms for modal dialogs, dropdown menus, and overlay components | Components that trap focus on Tab but release on Escape (or vice versa) are partial traps that still violate 2.1.2 |
| KB-005 | In degraded mode (screenshot-input), keyboard navigation findings are limited to structural assessment from visual layout -- flag as "Structural assessment only; manual keyboard testing required" | Screenshot analysis cannot verify actual keyboard behavior; limitations must be disclosed |

---

## Screen Reader Compatibility Test Protocol

Screen reader compatibility is evaluated through structural assessment of semantic HTML and ARIA implementation.

> **Source:** W3C (2023). WCAG 2.2 Principles 1 (Perceivable) and 4 (Robust). W3C (2023b). ARIA Authoring Practices Guide (APG) 1.2.

### Test Matrix

| Test | Evaluation Criteria | WCAG Criterion | Level |
|------|-------------------|----------------|-------|
| Heading hierarchy | Logical heading structure (h1-h6) without skipped levels | 1.3.1 | A |
| ARIA landmarks | Main, navigation, banner, contentinfo landmarks present and correct | 1.3.1, 4.1.2 | A |
| Alternative text | All non-decorative images have descriptive alt text; decorative images use empty alt | 1.1.1 | A |
| Form labels | All form controls have programmatically associated labels | 1.3.1, 3.3.2 | A |
| Live regions | Dynamic content updates announced via ARIA live regions | 4.1.3 | AA |
| Error identification | Error messages programmatically associated with the invalid field | 3.3.1 | A |

### Screen Reader Test Rules

| Rule ID | Rule | Consequence of Violation |
|---------|------|-------------------------|
| SR-001 | Heading hierarchy assessment MUST identify skipped levels (e.g., h1 to h3 without h2) and missing top-level headings | Skipped heading levels break screen reader navigation and violate 1.3.1 |
| SR-002 | ARIA landmark evaluation MUST verify both presence and correct usage -- an ARIA landmark with the wrong role is worse than no landmark | Incorrect ARIA roles mislead screen reader users about page structure |
| SR-003 | Alternative text assessment MUST distinguish between decorative images (should have empty alt) and informative images (should have descriptive alt) | Applying alt text rules uniformly without distinguishing purpose creates either verbose screen reader output (alt text on decorative images) or missing information (empty alt on informative images) |
| SR-004 | Screen reader compatibility assessment is structural (semantic HTML, ARIA), not experiential -- this limitation MUST be disclosed per P-022 | The evaluator cannot simulate the actual screen reader experience across different AT combinations (JAWS, NVDA, VoiceOver with different browsers) |
| SR-005 | Every screen reader finding MUST reference the specific WCAG success criterion and cite evidence from the input artifacts | Findings without WCAG criterion references are not actionable for compliance remediation |

---

## Cognitive Load Assessment Protocol

Cognitive load assessment evaluates information density, reading level, consistency, and error prevention mechanisms.

> **Source:** W3C (2023). WCAG 2.2 Principle 3 (Understandable). Nielsen (1994b) severity scale for cognitive barrier assessment.

### Test Matrix

| Test | Evaluation Criteria | WCAG Criterion | Level |
|------|-------------------|----------------|-------|
| Reading level | Content appropriate for target audience's reading level | 3.1.5 | AAA |
| Consistent navigation | Navigation mechanisms consistent across pages/screens | 3.2.3 | AA |
| Error prevention | Reversible submissions; confirmation for consequential actions | 3.3.4 (AA), 3.3.6 (AAA) | AA/AAA |
| Input assistance | Labels, instructions, and suggestions provided for user input | 3.3.2 (A), 3.3.3 (AA) | A/AA |
| Redundant entry | Information previously entered is auto-populated or selectable | 3.3.7 (A, new in 2.2) | A |
| Consistent help | Help mechanisms in consistent relative order across pages | 3.2.6 (A, new in 2.2) | A |

### Cognitive Load Rules

| Rule ID | Rule | Consequence of Violation |
|---------|------|-------------------------|
| CG-001 | Reading level evaluation MUST use the Flesch-Kincaid readability formula when sufficient English text is available for analysis. When text is in a non-English language, use the appropriate language-specific readability formula (e.g., SMOG for Spanish, LIX for Scandinavian languages) or flag as "Language-specific readability assessment required" with MEDIUM confidence | Flesch-Kincaid provides a quantifiable, reproducible reading level assessment. Language-specific formula guidance prevents misapplication of English-calibrated formulas to non-English content |
| CG-002 | When text is insufficient for Flesch-Kincaid computation (e.g., only labels and short UI copy), use AI-assisted reading level assessment and flag as MEDIUM synthesis confidence | AI-assessed reading levels without a formal readability formula are judgment-based and must be disclosed |
| CG-003 | Consistent navigation evaluation MUST compare navigation patterns across at minimum 2 pages or screens when multi-page input is available | Single-page evaluation cannot assess navigation consistency; flag as "Single-page assessment -- cross-page consistency not evaluated" when only one page is provided |
| CG-004 | Error prevention evaluation MUST assess both reversibility of submissions and presence of confirmation dialogs for consequential actions | Missing either reversibility or confirmation assessment produces incomplete error prevention findings |
| CG-005 | Cognitive load assessment findings are classified as MEDIUM synthesis confidence when based on AI judgment about user cognitive burden | Presenting cognitive load assessments as objective measurements without confidence disclosure violates P-022 |

---

## Conformance Level Determination Rules

Conformance level is determined from the aggregate per-criterion results, not from individual findings.

> **Source:** W3C (2023). WCAG 2.2 [Understanding Conformance]. Conformance is assessed at the level (A, AA, AAA), not per criterion.

### Determination Rules

| Rule ID | Rule | Consequence of Violation |
|---------|------|-------------------------|
| CD-001 | Conformance at Level A is achieved only when ALL Level A success criteria receive PASS or NOT APPLICABLE status | A single Level A FAIL prevents Level A conformance |
| CD-002 | Conformance at Level AA is achieved only when ALL Level A AND Level AA success criteria receive PASS or NOT APPLICABLE status | AA conformance requires complete A conformance plus all AA criteria passing |
| CD-003 | Conformance at Level AAA is achieved only when ALL success criteria at all three levels receive PASS or NOT APPLICABLE status | AAA conformance requires complete A + AA + AAA conformance |
| CD-004 | If the achieved conformance level is lower than the target level, the output MUST state: "Target: {target}. Achieved: {achieved}. {N} criteria at {target level} failed." | Ambiguous conformance reporting creates false legal compliance confidence |
| CD-005 | If no conformance level is achieved (one or more Level A criteria fail), the output MUST state: "Conformance level: None achieved. {N} Level A criteria failed." | Even when the target is higher, Level A failures must be highlighted as the most critical gap |

---

## Remediation Priority Rules

Remediation recommendations are prioritized based on severity, conformance level, and user impact.

### Priority Ranking Methodology

| Rule ID | Rule | Consequence of Violation |
|---------|------|-------------------------|
| RP-001 | Remediation items MUST be ranked by: (1) severity descending (4 before 3 before 2), (2) conformance level ascending within severity (Level A before AA before AAA), (3) estimated user impact within same severity and level | Non-systematic priority ranking produces remediation lists that do not address the most critical barriers first |
| RP-002 | Every remediation recommendation MUST reference a specific WCAG technique by ID (e.g., "Technique ARIA14", "Technique G18", "Technique H67") | Technique references enable engineering teams to look up implementation guidance directly from W3C documentation |
| RP-003 | Remediation effort estimates MUST use one of three values: Low (< 1 day), Medium (1-3 days), High (> 3 days) | Standardized effort levels enable resource planning; finer-grained estimates suggest false precision |
| RP-004 | The impact field MUST describe who benefits from the fix, referencing the Persona Spectrum analysis when applicable | Connecting remediation to specific persona scenarios demonstrates the "solve for one, extend to many" principle |
| RP-005 | Remediation priority ranking is classified as MEDIUM synthesis confidence -- priority involves AI judgment about relative impact and effort | Presenting priority rankings as objective measurements violates P-022 |

### Remediation Output Format

| Priority | WCAG Criterion | Severity | Affected Element | Remediation | Effort Estimate | Impact |
|----------|---------------|----------|-----------------|-------------|-----------------|--------|
| {rank} | SC {X.Y.Z} | {0-4} | {element} | {fix with technique reference} | Low / Medium / High | {who benefits, persona reference} |

---

## Quality Gate Integration

How the inclusive design evaluation maps to the S-014 LLM-as-Judge quality dimensions for quality gate scoring (H-13, >= 0.92 for C2+ deliverables).

> **Source:** `.context/rules/quality-enforcement.md` [Quality Gate]. `skills/ux-inclusive-design/SKILL.md` [Synthesis Hypothesis Confidence].

### S-014 Dimension Mapping

| S-014 Dimension | Weight | Inclusive Design Mapping | Verification |
|----------------|--------|-------------------------|--------------|
| Completeness | 0.20 | All four POUR principles evaluated; all success criteria at target level assessed; all interaction patterns have Persona Spectrum profiles | Count of criteria evaluated vs. criteria in scope; count of interaction patterns with complete 4x3 matrices |
| Internal Consistency | 0.20 | Severity assignments consistent across similar findings; conformance determination consistent with per-criterion results; Persona Spectrum scenarios consistent with WCAG findings | No contradictory severity/status pairs (SD-001); conformance level matches aggregate criterion results (CD-001 through CD-005) |
| Methodological Rigor | 0.20 | WCAG evaluation follows POUR order; Persona Spectrum follows Microsoft methodology; severity scale aligns with Nielsen | Evidence of systematic step-by-step evaluation; methodology citations present |
| Evidence Quality | 0.15 | Every finding has specific evidence; every contrast ratio has hex/RGB values (or degraded mode flag); every keyboard finding has affected element and observed behavior | No findings without evidence; no contrast claims without computed ratios |
| Actionability | 0.15 | Every remediation references a WCAG technique; effort estimates are present; impact descriptions connect to persona scenarios | All FAIL findings have actionable remediation; no "fix this" without technique reference |
| Traceability | 0.10 | Every finding references a specific WCAG success criterion; every Persona Spectrum profile cross-references WCAG criteria; engagement ID and target level are documented | All criterion IDs present; all profile-to-criterion cross-references valid |

---

## Self-Review Checklist

Before persisting the evaluation report, verify all items below (S-010):

- [ ] 1. All four POUR principles have been evaluated with per-criterion pass/fail status (PR-001, PS-001)
- [ ] 2. The conformance level result is correctly determined -- all criteria at that level PASS (CD-001 through CD-005)
- [ ] 3. Every color contrast element has foreground/background values and computed ratios, or is flagged for manual measurement in degraded mode (CC-001, CC-003, CC-004)
- [ ] 4. Every keyboard navigation issue has the affected element, expected behavior, observed behavior, and WCAG criterion (KB-001)
- [ ] 5. Every screen reader finding has evidence and WCAG criterion reference (SR-005)
- [ ] 6. Every interaction pattern has a complete Persona Spectrum profile with all 12 cells populated (PS-012)
- [ ] 7. Every FAIL finding has a severity rating of 1-4; every PASS finding has severity 0 (SD-001, SD-002)
- [ ] 8. Every remediation recommendation references a WCAG technique (RP-002)
- [ ] 9. The Synthesis Judgments Summary lists each AI judgment call with confidence classification (SD-004, PS-014, CG-005, RP-005)
- [ ] 10. The navigation table is present and all anchors resolve (H-23)
- [ ] 11. Degraded mode disclosure is present if Figma MCP was unavailable (P-022)
- [ ] 12. Remediation priorities are ranked by severity descending, then conformance level ascending (RP-001)
- [ ] 13. Handoff data includes only findings with severity >= 2 (handoff threshold)
- [ ] 14. The executive summary states the achieved conformance level and critical violation count (CD-004, CD-005)
- [ ] 15. P-022 limitations disclosure requirements are met: single-evaluator disclosure present, residual limitations listed, and input mode limitations documented (LM-001)

---

## Limitations Disclosure Rules

P-022 (no deception about capabilities) requires explicit disclosure of evaluation limitations. These rules codify the minimum disclosure obligations for the evaluation report.

> **Source:** `docs/governance/JERRY_CONSTITUTION.md` (P-022). `skills/ux-inclusive-design/templates/accessibility-report-template.md` [Limitations and Reliability].

| Rule ID | Rule | Consequence of Violation |
|---------|------|-------------------------|
| LM-001 | The evaluation report MUST include a Limitations and Reliability section containing: (a) a single-evaluator disclosure stating that full WCAG 2.2 compliance requires manual AT testing, automated tools, and user testing with people who have disabilities, (b) a residual limitations list (cannot replicate AT testing, persona profiles are heuristic models, severity is MEDIUM confidence), and (c) input mode limitations disclosure when operating in degraded mode | Omitting limitations disclosure presents AI-evaluated findings as comprehensive compliance certification, violating P-022 |

---

## References

| Source | Citation | Used For |
|--------|----------|----------|
| W3C, 2023 (WCAG) | Web Content Accessibility Guidelines (WCAG) 2.2. W3C Recommendation, 05 October 2023. | POUR principles, success criteria, conformance levels, techniques |
| W3C, 2023 (APG) | ARIA Authoring Practices Guide (APG) 1.2. W3C Group Note. | ARIA pattern implementations, landmark roles, widget patterns |
| Microsoft, 2016 | Microsoft Inclusive Design Toolkit. Microsoft Corporation, 2016. | Three principles, Persona Spectrum methodology |
| Nielsen, 1994b | Nielsen, J. (1994b). Severity ratings for usability problems. In *Usability Inspection Methods*, pp. 413-414. John Wiley & Sons. | 0-4 severity scale alignment |
| Agent definition | `skills/ux-inclusive-design/agents/ux-inclusive-evaluator.md` | Evaluation workflow, per-criterion format, Persona Spectrum format |
| SKILL.md | `skills/ux-inclusive-design/SKILL.md` | Methodology, output specification, MCP dependencies, synthesis confidence |
| Quality enforcement | `.context/rules/quality-enforcement.md` | S-014 quality dimensions, H-13 threshold, criticality levels |
| Synthesis validation | `skills/user-experience/rules/synthesis-validation.md` | Confidence classification, convergence thresholds |
| US DOJ, 2024 | "Guidance on Web Accessibility and the ADA." U.S. Department of Justice. | Legal compliance context (ADA) |
| European Parliament, 2019 | Directive (EU) 2019/882 -- European Accessibility Act (EAA). | Legal compliance context (EAA) |
| Section 508 | Section 508 of the Rehabilitation Act (29 U.S.C. 794d). | Legal compliance context (federal) |

---

<!-- GOVERNANCE ID INDEX: EV-001 through EV-005 (workflow sequencing), PR-001 through PR-003 (principle evaluation), PS-001 through PS-003 (principle scope), CL-001 through CL-004 (conformance scope), SC-001 through SC-006 (criterion format), SD-001 through SD-004 (severity-decision), ID-001 through ID-003 (inclusive design principles), PS-010 through PS-014 (persona spectrum), IP-001 through IP-003 (interaction patterns), MX-001 through MX-003 (matrix population), CC-001 through CC-005 (color contrast), KB-001 through KB-005 (keyboard navigation), SR-001 through SR-005 (screen reader), CG-001 through CG-005 (cognitive load), CD-001 through CD-005 (conformance determination), RP-001 through RP-005 (remediation priority), LM-001 (limitations disclosure) -->

*Rules: inclusive-design-rules.md (v1.1.0)*
*Sub-skill: `/ux-inclusive-design`*
*Parent skill: `/user-experience`*
*Agent: `ux-inclusive-evaluator` (T3, Systematic, Sonnet)*
*Project: PROJ-022 User Experience Skill*
*Created: 2026-03-04*
