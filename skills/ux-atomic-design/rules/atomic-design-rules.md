<!-- VERSION: 1.1.0 | DATE: 2026-03-04 | SOURCE: skills/ux-atomic-design/SKILL.md (v1.2.0), skills/ux-atomic-design/agents/ux-atomic-architect.md (v1.0.1), Frost (2016) "Atomic Design" | PARENT: /ux-atomic-design sub-skill | REVISION: iter2 — add Handoff Threshold Rules (HAND-001–003), version-pin synthesis-validation.md citation, clarify TAX-005, cross-ref drift thresholds to maturity, define effort criteria, version-annotate Related Files -->

# Atomic Design Methodology Rules

> Operational constraints and methodology rules for the `ux-atomic-architect` agent. Provides Brad Frost's 5-level taxonomy enforcement, composition rules, molecule/organism boundary adjudication, design token architecture governance, Storybook coverage model targets, consolidation opportunity identification, confidence classification rules, and quality gate integration that complement the agent definition.

## Document Sections

| Section | Purpose |
|---------|---------|
| [5-Level Taxonomy Rules](#5-level-taxonomy-rules) | Brad Frost's hierarchy with identification criteria and classification discipline |
| [Composition Rules](#composition-rules) | What can contain what; forbidden and optional compositions |
| [Molecule/Organism Boundary Adjudication](#moleculeorganism-boundary-adjudication) | Tie-breaker rules for ambiguous classification |
| [Design Token Architecture Rules](#design-token-architecture-rules) | 7 token categories, drift ratio formula, threshold enforcement |
| [Storybook Coverage Model](#storybook-coverage-model) | Per-level coverage targets and gap prioritization |
| [Consolidation Opportunity Rules](#consolidation-opportunity-rules) | Duplicate detection, similarity assessment, design debt quantification |
| [Design System Maturity Assessment](#design-system-maturity-assessment) | 4-level maturity classification with threshold criteria |
| [Confidence Classification Rules](#confidence-classification-rules) | HIGH/MEDIUM/LOW mapping criteria, synthesis judgment requirements |
| [Quality Gate Integration](#quality-gate-integration) | Score mapping to S-014 rubric dimensions |
| [Handoff Threshold Rules](#handoff-threshold-rules) | Minimum data requirements for component handoff eligibility |
| [Related Files](#related-files) | Dependency matrix: upstream, downstream, and sibling references |
| [Self-Review Checklist](#self-review-checklist) | S-010 verification before output persistence |

---

## 5-Level Taxonomy Rules

Brad Frost's Atomic Design methodology (2016) structures interface components into five distinct levels, each building on the level below. These rules enforce consistent classification discipline across all component inventories.

> **Source:** Frost, B. (2016). "Atomic Design." Self-published. atomicdesign.bradfrost.com. Chemistry metaphor: atoms combine into molecules, molecules combine into organisms.

### Level Definitions and Identification Criteria

| Level | Name | Identification Criteria | Examples |
|-------|------|------------------------|----------|
| 1 | **Atoms** | (a) Single specific function, (b) cannot be decomposed further, (c) maps to single HTML element or tightly-coupled group | Buttons, inputs, labels, headings, icons, form elements, design tokens |
| 2 | **Molecules** | (a) Combines 2-5 atoms, (b) serves single describable purpose, (c) removing any atom degrades function | Search form, form field, media object, nav item, card header |
| 3 | **Organisms** | (a) Combines molecules and atoms, (b) recognizable section, (c) reusable across templates, (d) has internal layout logic | Header, product card grid, comment thread, sidebar navigation, footer |
| 4 | **Templates** | (a) Arranges organisms into complete page structure, (b) uses placeholder content, (c) defines spatial relationships, (d) multiple pages can instantiate | Product listing template, dashboard template, article template |
| 5 | **Pages** | Template instances populated with real, representative content for validation | Product listing page, dashboard page, article page |

### Classification Discipline

| ID | Rule | Tier | Consequence of Violation |
|----|------|------|--------------------------|
| TAX-001 | Every component MUST be classified into exactly one of the 5 levels. No component may remain unclassified in the final inventory. | HARD | Unclassified components cannot be assessed for coverage, composition, or handoff eligibility |
| TAX-002 | Every classification MUST include a rationale when the classification is ambiguous (component could plausibly be assigned to an adjacent level). Clear classifications (e.g., a standalone button is an atom) do not require explicit rationale. | HARD | Unreasoned classification violates P-001 (evidence required) and prevents downstream validation |
| TAX-003 | The inventory MUST be constructed bottom-up: atoms first, then molecules, then organisms, then templates, then pages. Each level depends on the level below being complete. | HARD | Top-down classification skips foundational components; molecules reference unknown atoms |
| TAX-004 | When a component cannot be classified after applying the identification criteria and the boundary adjudication rules, classify as the HIGHER level and document the rationale. Over-classifying is safer than under-classifying because higher levels carry more explicit documentation requirements (layout logic, composition rules). | HARD | Under-classification omits required documentation; organisms misclassified as molecules lose layout logic records |
| TAX-005 | Design tokens are classified as Level 1 (Atoms). Tokens define a single visual property value (e.g., `color-primary-500`, `spacing-4`) and are the sub-atomic foundation that atoms consume. Level 1 encompasses both HTML-element atoms and design tokens; the "sub-atomic" description is conceptual (tokens underpin atoms), not a separate hierarchy level. | MEDIUM | Token misclassification creates circular references in the hierarchy |
| TAX-006 | Pages MUST reference exactly one template. A page that combines elements from multiple templates indicates a missing template definition. | MEDIUM | Multi-template pages suggest the template layer is incomplete |
| TAX-007 | Orphaned components (referenced by no parent) and dangling references (parent references a non-existent child) MUST be flagged in the inventory and listed separately. | HARD | Orphans and dangling references indicate inventory incompleteness |

---

## Composition Rules

Composition rules document valid assembly patterns between hierarchy levels. These rules prevent inconsistent component usage and serve as the structural backbone of the design system.

> **Source:** Frost (2016), Chapters 2-3. Composition hierarchy is directional: lower levels compose into higher levels.

### Valid Composition Patterns

| Composition Type | What Contains What | Constraint |
|-----------------|-------------------|------------|
| **Atom-to-Molecule** | Molecules contain 2-5 atoms | Every atom in a molecule MUST serve the molecule's single purpose |
| **Molecule-to-Organism** | Organisms contain molecules and/or atoms | Every organism MUST have internal layout logic separating it from a large molecule |
| **Organism-to-Template** | Templates arrange organisms into page-level structure | Templates MUST use placeholder content, not real data |
| **Template-to-Page** | Pages instantiate exactly one template with real content | Each page tests content variation (length, empty states, error states) |

### Composition Discipline

| ID | Rule | Tier | Consequence of Violation |
|----|------|------|--------------------------|
| CMP-001 | Every molecule MUST reference at least one atom. A molecule with zero atom references is either misclassified or incompletely inventoried. | HARD | Composition chain broken; molecule floats without foundational components |
| CMP-002 | Every organism MUST reference at least one molecule. Organisms composed entirely of raw atoms without any molecule grouping are likely misclassified molecules. | HARD | Organism-molecule boundary blurred; layout logic documentation omitted |
| CMP-003 | Every template MUST reference at least one organism. A template without organism references indicates the organism layer is missing. | HARD | Template-organism chain broken; page structure lacks recognizable sections |
| CMP-004 | Every page MUST reference exactly one template. | MEDIUM | Multi-template pages indicate incomplete template layer (TAX-006) |
| CMP-005 | Organisms MUST NOT be nested inside other organisms at the same hierarchy level. If an organism appears inside another organism, the outer structure is likely a template or the inner structure should be reclassified as a molecule. | HARD | Nesting violation creates ambiguous hierarchy; composition rules become circular |
| CMP-006 | Forbidden compositions MUST be documented alongside valid compositions. Common forbidden patterns: atom-inside-atom nesting, template-inside-organism embedding, page-inside-template recursion. | MEDIUM | Undocumented forbidden patterns lead to inconsistent component assembly |
| CMP-007 | Optional compositions (components that may or may not appear in a parent) MUST be documented with the optionality explicitly noted. Example: error message atom is optional within form field molecule. | MEDIUM | Undocumented optionality leads to inconsistent parent rendering across instances |

---

## Molecule/Organism Boundary Adjudication

The boundary between molecules and organisms is the most common classification ambiguity. These rules provide a deterministic adjudication procedure.

> **Source:** Frost (2016), Chapter 2: "Molecules" and Chapter 2: "Organisms." The boundary is acknowledged as subjective in Frost's original text; these tie-breaker rules operationalize a consistent classification approach.

### Adjudication Procedure

Apply the following checks in order. The first matching check determines the classification:

| Priority | Check | Result | Rationale |
|----------|-------|--------|-----------|
| 1 | Does the component contain other molecules as children? | **Organism** | By definition, organisms combine molecules; a group of molecules cannot itself be a molecule |
| 2 | Are all children atoms AND can the group be described with a single verb-noun phrase? | **Molecule** | Single-purpose atom groups are molecules (e.g., "captures search query", "displays user avatar") |
| 3 | Does the component have its own internal layout logic (grid, flex, positioning)? | **Organism** | Internal layout logic distinguishes organisms from simple atom groupings |
| 4 | Could the component be reused in different template contexts without modification? | **Organism** | Cross-template reusability suggests section-level independence characteristic of organisms |
| 5 | None of the above checks produce a clear result | **Organism** (default) | Over-classifying as organism is safer; organisms carry layout logic documentation that molecules do not |

### Adjudication Discipline

| ID | Rule | Tier | Consequence of Violation |
|----|------|------|--------------------------|
| ADJ-001 | When a component is ambiguous between molecule and organism, the adjudication procedure MUST be applied in priority order (1 through 5). NEVER skip checks. | HARD | Inconsistent classification across the inventory; same pattern classified differently in different contexts |
| ADJ-002 | Every adjudication decision for ambiguous components MUST be documented in the Synthesis Judgments Summary with the check number that determined the classification. | HARD | Undocumented adjudication prevents downstream review and consistency validation |
| ADJ-003 | When the default (Priority 5) is applied, the rationale MUST explain why checks 1-4 were inconclusive. | MEDIUM | Default classification without rationale provides no audit trail for the decision |
| ADJ-004 | The same component pattern MUST be classified consistently across the inventory. If "search form" is classified as a molecule in one context, it MUST be a molecule everywhere unless the composition differs. | HARD | Inconsistent classification of identical patterns undermines the taxonomy's value as a shared vocabulary |

---

## Design Token Architecture Rules

Design tokens are the sub-atomic foundation of the component hierarchy. Token auditing ensures consistency across the entire design system.

> **Source:** Frost (2016), Chapter 2. Token categories aligned with W3C Design Token Community Group draft categories. Drift ratio formula and threshold are framework-internal heuristics.

### Token Categories

The architect audits all 7 token categories. Each category represents a distinct visual property domain.

| # | Token Category | Examples | Consistency Check |
|---|---------------|---------|-------------------|
| 1 | **Color** | Primary, secondary, surface, error, text, border | No unnamed hex/rgb values in components; all colors reference token names |
| 2 | **Typography** | Font family, font size scale, line height, font weight | No magic number font sizes; all text styles reference token scale |
| 3 | **Spacing** | Margin scale, padding scale, gap scale | No arbitrary pixel values; all spacing references token scale |
| 4 | **Breakpoints** | Mobile, tablet, desktop, wide | Consistent breakpoint values across all responsive components |
| 5 | **Elevation** | Shadow levels (none, low, medium, high) | Shadow values match defined elevation tokens |
| 6 | **Border** | Border width, border radius, border style | Consistent radius and width across similar component types |
| 7 | **Motion** | Duration, easing, transition types | Animation timing consistent with motion token definitions |

### Drift Ratio Formula

```
drift_ratio = hardcoded_values / total_style_values
```

Where:
- `hardcoded_values` = count of style values that use literal values (hex codes, pixel values, magic numbers) instead of token references
- `total_style_values` = total count of all style values inspected in that token category

### Drift Ratio Threshold

| Drift Ratio | Status | Interpretation |
|-------------|--------|----------------|
| < 0.05 | PASS (Optimized) | Full token governance; incidental overrides only |
| 0.05 - 0.10 | PASS (Mature) | Systematic tokens with minor drift; acceptable for mature systems |
| 0.10 - 0.20 | PASS (Developing) | Partial token governance; improvement recommended but not critical |
| > 0.20 | **FAIL** | Significant design system inconsistency; more than 1-in-5 style values bypass the token system |

*(Heuristic threshold: the 0.20 FAIL boundary is a framework-internal heuristic derived from the reasoning that a design system where more than 1 in 5 style values bypass the token system has lost meaningful token governance. Adjust based on team design system maturity: nascent systems may tolerate 0.30; mature systems should target < 0.10. The > 0.20 FAIL boundary aligns with the Nascent maturity level ([Design System Maturity Assessment](#design-system-maturity-assessment)), where drift ratio > 0.30 is a defining characteristic; systems between 0.20 and 0.30 fall in the Developing range.)*

### Token Audit Discipline

| ID | Rule | Tier | Consequence of Violation |
|----|------|------|--------------------------|
| TKN-001 | All 7 token categories MUST be audited. If a category has no defined tokens in the design system, document it as "No tokens defined" with drift ratio N/A. | HARD | Incomplete audit creates false confidence in token governance |
| TKN-002 | Drift ratio MUST be calculated per category, not as a single aggregate number. The overall drift ratio is the weighted average across categories. | HARD | Aggregate-only drift ratio hides category-specific problems |
| TKN-003 | Every drift instance (hardcoded value) MUST list: component name, hardcoded value, and suggested token replacement. | MEDIUM | Drift instances without remediation guidance are not actionable |
| TKN-004 | Token naming convention MUST be assessed as "systematic" (e.g., `color-primary-500`) or "ad hoc" (e.g., `blue3`, `mainColor`). Document which convention the design system uses. | MEDIUM | Naming convention affects maintainability and onboarding |
| TKN-005 | Cross-component token inconsistencies MUST be identified: cases where two components use different tokens for the same visual purpose (e.g., two different spacing tokens for card padding). | MEDIUM | Cross-component inconsistency indicates token governance gaps beyond simple drift |
| TKN-006 | When operating in Manual Component Inventory Mode (Storybook MCP unavailable), token audit accuracy MUST be disclosed as reduced per P-022. Token analysis from text descriptions is sampling-based, not comprehensive. | HARD | Undisclosed accuracy limitations violate P-022 (no deception) |

---

## Storybook Coverage Model

Storybook coverage measures how well the component library is documented with interactive stories. Coverage assessment operates at three granularity levels with per-hierarchy-level targets.

> **Source:** Storybook "Component-Driven Development" guide (storybook.js.org/tutorials/intro-to-storybook/, 2024). Coverage targets are framework-internal heuristics; see rationale below.

### Coverage Targets (Heuristic Thresholds)

| Coverage Level | Atoms Target | Molecules/Organisms Target | Rationale |
|---------------|-------------|---------------------------|-----------|
| **Component coverage** | >= 80% | >= 60% | Atoms have outsized reuse impact as foundational components; molecules/organisms have higher documentation cost per component |
| **State coverage** | >= 70% | >= 50% | States (default, hover, active, disabled, error, loading) are critical for atoms; molecules/organisms have fewer universal states |
| **Variant coverage** | >= 60% | >= 40% | Variants (size, color, style) document the design system's flexibility; lower targets for molecules/organisms due to higher per-variant cost |

*(Heuristic thresholds: these percentage targets are framework-internal, not industry-standard benchmarks. Component coverage: a single undocumented atom affects every molecule and organism that consumes it, justifying the higher 80% atom target vs. 60% for molecules/organisms which have higher per-component documentation cost. State coverage: atoms have 6 universal interactive states (default, hover, active, disabled, error, loading) that propagate to all consuming molecules; the 70% atom target ensures most interactive behaviors are documented, while the 50% molecule/organism target reflects that higher-level components inherit atom states and have fewer unique states of their own. Variant coverage: the 60%/40% split reflects that atom variants (size, color, style) define the design system's flexibility vocabulary, while molecule/organism variants are typically compositions of atom variants and thus have higher per-variant documentation cost with lower marginal documentation value. Calibrate per design system maturity and team context.)*

### Coverage Gap Prioritization

When identifying undocumented components, prioritize by:

| Priority | Criterion | Rationale |
|----------|-----------|-----------|
| 1 | **Reuse frequency** | High-reuse undocumented components have the highest documentation ROI |
| 2 | **Hierarchy level** | Atoms before molecules before organisms; foundational components first |
| 3 | **Complexity** | Components with multiple states/variants need documentation more urgently than simple single-state components |

### Coverage Discipline

| ID | Rule | Tier | Consequence of Violation |
|----|------|------|--------------------------|
| COV-001 | Coverage MUST be calculated per hierarchy level (atoms, molecules, organisms). Templates and pages are assessed for existence but do not have percentage targets. | HARD | Per-level calculation reveals which hierarchy layer has the biggest documentation gap |
| COV-002 | Coverage percentages MUST be compared against the heuristic targets with explicit PASS/FAIL status per level. | HARD | Targets without PASS/FAIL status are not actionable |
| COV-003 | Undocumented components MUST be listed and prioritized using the coverage gap prioritization criteria (reuse frequency, hierarchy level, complexity). | MEDIUM | Unprioritized gaps leave teams without a clear documentation roadmap |
| COV-004 | When operating in Manual Component Inventory Mode, coverage percentages MUST carry a disclaimer that accuracy depends on the completeness of user-provided inventory data. | HARD | Coverage percentages from incomplete inventories are artificially inflated; disclosure required per P-022 |
| COV-005 | State coverage and variant coverage MUST be assessed at the atom and molecule levels only. Organism-level state/variant coverage is optional. | MEDIUM | Organism states are composition-dependent and less amenable to systematic coverage measurement |

---

## Consolidation Opportunity Rules

Consolidation identifies duplicate or near-duplicate components that can be merged to reduce design system complexity and maintenance burden.

> **Source:** Frost (2016), Chapter 5: "Maintaining Design Systems." Design debt quantification criteria are framework-internal.

### Consolidation Identification Criteria

A component pair is a consolidation candidate when any of the following conditions are met:

| Condition | Detection Method | Similarity Level |
|-----------|-----------------|-----------------|
| Same name with different suffixes | Name comparison (e.g., `Button`, `ButtonPrimary`, `ButtonNew`) | HIGH |
| Overlapping purpose with different names | Purpose comparison from component descriptions | MEDIUM |
| Shared composition (same atoms/molecules in different arrangement) | Composition parent comparison | MEDIUM |
| Identical visual appearance with different implementations | Visual comparison (when screenshots available) | HIGH |

### Consolidation Discipline

| ID | Rule | Tier | Consequence of Violation |
|----|------|------|--------------------------|
| CSL-001 | Every consolidation candidate pair MUST include: component A name, component B name, similarity level (HIGH/MEDIUM), recommendation (Merge/Deduplicate/Keep both), and estimated effort (Low/Medium/High). | HARD | Incomplete consolidation entries are not actionable |
| CSL-002 | The recommendation MUST be one of: **Merge** (combine into a single component with variants), **Deduplicate** (remove one and redirect references), or **Keep both** (document why both are needed despite similarity). | MEDIUM | Open-ended recommendations without a clear action path delay resolution |
| CSL-003 | "Keep both" recommendations MUST include a one-line rationale explaining why the components serve distinct purposes despite similarity. | MEDIUM | Undocumented "keep both" decisions appear as missed consolidation opportunities in future audits |
| CSL-004 | Consolidation candidates MUST be prioritized by: (a) reuse frequency of the affected components, (b) estimated effort (low effort first), (c) downstream impact (components consumed by many parents first). | MEDIUM | Unprioritized consolidation lists do not guide team effort allocation |

**Effort criteria:** Low = single-file change or rename affecting 1 component; Medium = cross-file refactor affecting 2-5 components (e.g., merging two atom variants into one with updated references); High = cross-team coordination or design system version bump affecting 6+ components (e.g., deduplicating organisms used across multiple templates requiring layout re-verification).

### Design Debt Quantification

Design debt is quantified as a composite count of system inconsistencies:

| Debt Factor | Measurement | Weight |
|-------------|-------------|--------|
| Token drift violations | Count of categories with drift ratio > 0.20 | HIGH |
| Undocumented Storybook stories | Count of components without any story | MEDIUM |
| Orphaned components | Count of components referenced by no parent | MEDIUM |
| Dangling references | Count of parent references to non-existent children | HIGH |
| Naming inconsistencies | Count of components violating naming conventions | LOW |
| Consolidation candidates | Count of HIGH-similarity pairs | MEDIUM |

**Debt factor severity criteria:** HIGH = structural integrity risk that can cause cascading failures across the component hierarchy (broken references, token governance loss); MEDIUM = quality and maintainability degradation that does not break the hierarchy but increases rework cost; LOW = cosmetic or convention violations that affect readability and onboarding but not functionality.

---

## Design System Maturity Assessment

Maturity assessment classifies the design system into one of four levels based on component coverage and token governance.

> **Source:** SKILL.md Phase 5 Activity 3. Maturity levels are framework-internal heuristics.

### Maturity Levels

| Level | Component Coverage | Token Governance (Drift Ratio) | Characteristics |
|-------|-------------------|-------------------------------|-----------------|
| **Nascent** | < 30% | > 0.30 | Ad-hoc components; no systematic token usage; no documented composition rules |
| **Developing** | 30-60% | 0.15-0.30 | Partial component library; some token governance; composition patterns emerging |
| **Mature** | 60-80% | 0.05-0.15 | Systematic component library; consistent token usage; documented composition rules |
| **Optimized** | > 80% | < 0.05 | Near-comprehensive coverage; full token governance; composition rules enforced |

*(Heuristic thresholds: component coverage refers to component coverage from the Storybook Coverage Model. A design system with < 30% documented components lacks critical mass for systematic reuse; > 80% reflects near-comprehensive coverage. Token governance levels operationalized via drift ratio ranges. Adjust based on team context.)*

### Maturity Discipline

| ID | Rule | Tier | Consequence of Violation |
|----|------|------|--------------------------|
| MAT-001 | Maturity assessment MUST use both component coverage AND token governance dimensions. A system with 90% coverage but > 0.30 drift is NOT "Optimized." | HARD | Single-dimension assessment creates misleading maturity classification |
| MAT-002 | Maturity classification MUST cite the specific component coverage percentage and average drift ratio that support the classification. | HARD | Unsupported classification violates P-001 (evidence required) |
| MAT-003 | When component coverage and token governance point to different maturity levels, classify at the LOWER level. | MEDIUM | Conservative classification prevents over-representing design system health |

---

## Confidence Classification Rules

Every AI-generated judgment in the architect's output requires a confidence classification. These rules govern classification criteria and synthesis gate compliance.

> **Source:** `skills/user-experience/rules/synthesis-validation.md` (v1.1.0) Section "Confidence Classification" and Section "Sub-Skill Synthesis Output Map."

### Classification Criteria

| Classification | Criteria | Action | Example |
|---------------|----------|--------|---------|
| **HIGH** | Multiple data sources converge; validated by prior component audit OR direct Storybook inspection data | Proceed with recommendation | Component classification confirmed by both Storybook story inspection and design file structure |
| **MEDIUM** | Single-framework reasoning; assessment based on user-provided inventory without live Storybook verification | Include "Validation Required" note; withhold definitive recommendation | Taxonomy completeness assessment from manual inventory mode without Storybook verification |
| **LOW** | Insufficient data; AI inference from text descriptions without visual or programmatic component inspection | Flag for human review before acting | Design token consistency analysis from text descriptions only; no CSS/style inspection |

### Judgment Types Requiring Classification

| Judgment Type | Description | Typical Confidence |
|---------------|-------------|-------------------|
| Component classification | Assigning a component to atom/molecule/organism/template/page | MEDIUM (classification involves subjective boundary judgment) |
| Boundary adjudication | Molecule vs. organism determination using tie-breaker rules | MEDIUM (systematic procedure applied, but boundary is inherently subjective) |
| Drift ratio assessment | Calculating token drift from available documentation | LOW (comprehensive token audit requires programmatic CSS inspection) |
| Consolidation recommendation | Identifying duplicate/near-duplicate component pairs | MEDIUM (name and purpose similarity detectable; visual similarity requires inspection) |
| Maturity classification | Assigning nascent/developing/mature/optimized level | MEDIUM (based on quantified coverage and drift, but thresholds are heuristic) |
| Storybook coverage assessment | Calculating coverage percentages from inventory data | MEDIUM in connected mode; LOW in manual inventory mode |

### Atomic Design Confidence Dynamics

Atomic Design outputs are typically MEDIUM confidence because component classification involves subjective boundary judgment. Confidence increases when:

1. A component inventory is verified against a live Storybook instance with programmatic inspection (classification -> HIGH for verified components)
2. A taxonomy assessment converges with `/ux-heuristic-eval` findings on component inconsistency (taxonomy completeness -> HIGH)

This means:
- **Manual inventory mode outputs** are MEDIUM for taxonomy, LOW for token analysis
- **Storybook-connected outputs** (future) may reach HIGH for taxonomy, MEDIUM for token analysis
- **Design token consistency** remains LOW because comprehensive token auditing requires programmatic CSS/style inspection that exceeds AI text-analysis capabilities

### Classification Discipline

| ID | Rule | Tier |
|----|------|------|
| CLS-001 | Every AI judgment call in the Synthesis Judgments Summary MUST include a confidence classification (HIGH, MEDIUM, or LOW) and a one-line rationale. | HARD |
| CLS-002 | NEVER classify a manual-inventory-mode judgment as HIGH unless multiple independent data sources converge (e.g., Storybook data + heuristic evaluation findings). | HARD |
| CLS-003 | Design token consistency analysis MUST be classified as LOW when based on text descriptions only. Classification may be MEDIUM when based on programmatic Storybook/CSS inspection. | HARD |
| CLS-004 | The minimum-confidence rule applies: when a single finding draws from multiple judgment types with different confidence levels, the finding's confidence is the LOWEST among all contributing judgments. | HARD |

---

## Quality Gate Integration

Atomic Design facilitation output maps to the S-014 LLM-as-Judge rubric dimensions (`.context/rules/quality-enforcement.md` Section "Quality Gate") as follows:

### Dimension Mapping

| S-014 Dimension | Weight | Atomic Design Evaluation Criteria |
|-----------------|--------|-----------------------------------|
| **Completeness** | 0.20 | All 5 hierarchy levels represented in inventory (or explicitly empty with rationale); all 7 token categories audited; Storybook coverage calculated per level; consolidation candidates identified; maturity level assigned |
| **Internal Consistency** | 0.20 | Component classifications consistent across inventory (same pattern = same level); composition references resolve correctly (no dangling references); drift ratios align with maturity classification; coverage percentages consistent with inventory counts |
| **Methodological Rigor** | 0.20 | 5-phase execution procedure followed sequentially; boundary adjudication applied for ambiguous components; drift ratio formula applied correctly; coverage targets compared against heuristic thresholds; bottom-up inventory construction order enforced |
| **Evidence Quality** | 0.15 | Component classifications cite identification criteria; drift ratios show formula and data source; consolidation recommendations cite specific similarity evidence; degraded mode disclosed when operating in manual inventory mode |
| **Actionability** | 0.15 | Consolidation candidates include recommendation and estimated effort; undocumented components prioritized with clear ordering criteria; maturity assessment includes specific improvement targets; design debt quantified with remediation priorities |
| **Traceability** | 0.10 | Every component traces to a hierarchy level with rationale for ambiguous cases; every drift instance traces to a specific component; coverage gaps trace to specific undocumented components; upstream heuristic findings cited where used; Frost (2016) methodology referenced |

### Scoring Discipline for Atomic Design

| ID | Rule | Tier |
|----|------|------|
| QG-001 | The quality gate threshold applies to the overall architect report, not to individual components or token categories. Baseline threshold: >= 0.92 (H-13, C2+). At C4 criticality, the threshold is >= 0.95. | HARD |
| QG-002 | Completeness scoring MUST assess all 5 hierarchy levels. If a level has zero components (e.g., no templates identified), completeness is not penalized IF the absence is explicitly documented with rationale. | MEDIUM |
| QG-003 | Evidence Quality scoring MUST penalize undisclosed degraded mode operation. If the agent operated in Manual Component Inventory Mode without the P-022 degraded mode banner, Evidence Quality receives a 0 score. | HARD |
| QG-004 | Internal Consistency scoring MUST verify that composition references are bidirectionally consistent: if molecule M references atom A as a child, atom A should list molecule M as a composition parent. | HARD |

---

## Handoff Threshold Rules

Handoff threshold rules define the minimum data a component must carry to qualify for inclusion in the Handoff Data section of the output template and for downstream consumption by `/ux-inclusive-design`.

> **Source:** SKILL.md (v1.2.0) handoff specification, `component-inventory-template.md` Handoff Data section.

| ID | Rule | Tier | Consequence of Violation |
|----|------|------|--------------------------|
| HAND-001 | A component qualifies for handoff when it has: (a) an assigned classification level (atom through page), (b) a component name, and (c) a variant count (estimated or exact). All three fields are required; a component missing any field is excluded from the handoff table. | HARD | Downstream sub-skills receive incomplete data; `/ux-inclusive-design` cannot assess component accessibility without level and variant information |
| HAND-002 | Components identified during inventory but not yet classified (TAX-001 pending) MUST NOT be included in the handoff data. Unclassified components are listed in the Orphaned Components section but excluded from the Handoff Data table and YAML. | HARD | Unclassified components pollute downstream data; consuming agents cannot determine applicable accessibility criteria without a hierarchy level |
| HAND-003 | The `handoff_components_count` field in the Handoff YAML MUST equal the number of rows in the Components for Downstream Consumption table. A mismatch indicates either a table row was added without updating the count or vice versa. | MEDIUM | Count mismatch between YAML and table creates data integrity doubt for consuming orchestrator or downstream sub-skill |

---

## Related Files

> Dependency matrix for operational traceability. Upstream files provide inputs or prerequisites; downstream files consume this rules file's outputs; sibling files share the same parent sub-skill.

| Relationship | File | Version | Purpose |
|-------------|------|---------|---------|
| **Parent SKILL.md** | `skills/ux-atomic-design/SKILL.md` | v1.2.0 | Sub-skill definition; methodology overview; agent routing |
| **Agent definition** | `skills/ux-atomic-design/agents/ux-atomic-architect.md` | v1.0.1 | Agent frontmatter, system prompt, output section (handoff threshold) |
| **Governance YAML** | `skills/ux-atomic-design/agents/ux-atomic-architect.governance.yaml` | v1.0.1 | Enforcement metadata: quality_threshold, quality_gate (S-014) |
| **MCP runbook** | `skills/ux-atomic-design/rules/mcp-runbook.md` | v1.0.0 | Context7 integration; Storybook degraded mode protocol |
| **Output template** | `skills/ux-atomic-design/templates/component-inventory-template.md` | v1.0.0 | Report template consumed by architect agent |
| **Wave progression** | `skills/user-experience/rules/wave-progression.md` | unversioned (no VERSION header) | Wave 3 (Design System) entry conditions; Wave 2 completion is a prerequisite |
| **Synthesis validation** | `skills/user-experience/rules/synthesis-validation.md` | v1.1.0 | Confidence classification shared taxonomy; Sub-Skill Synthesis Output Map |
| **MCP coordination** | `skills/user-experience/rules/mcp-coordination.md` | v1.2.0 | Storybook REQ dependency; degraded-mode disclosure requirements |
| **Quality enforcement** | `.context/rules/quality-enforcement.md` | SSOT -- version tracked externally (v1.6.0 at time of writing) | S-014 dimension rubric; H-13 quality gate threshold (>= 0.92 baseline, >= 0.95 at C4) |

> **Wave 2 prerequisite:** This rules file governs agent behavior in Wave 3 (Design System). Per `wave-progression.md`, Wave 2 (Data-Ready) completion is required before Atomic Design executes, unless the bypass condition is met (Storybook already in use).

---

## Self-Review Checklist

Before persisting the report, the architect MUST verify (S-010, H-15):

| # | Check | Rule Reference |
|---|-------|---------------|
| 1 | All 5 hierarchy levels are represented in the inventory (or explicitly empty with rationale) | TAX-001 |
| 2 | Every ambiguous classification includes a rationale with the adjudication check number | TAX-002, ADJ-002 |
| 3 | Inventory was constructed bottom-up (atoms first through pages last) | TAX-003 |
| 4 | Every molecule references at least one atom; every organism references at least one molecule | CMP-001, CMP-002 |
| 5 | Every template references at least one organism; every page references exactly one template | CMP-003, CMP-004 |
| 6 | Orphaned components and dangling references are flagged and listed | TAX-007 |
| 7 | All 7 token categories audited with drift ratio per category | TKN-001, TKN-002 |
| 8 | Every drift instance lists component name, hardcoded value, and suggested replacement | TKN-003 |
| 9 | Storybook coverage calculated per level with PASS/FAIL against targets | COV-001, COV-002 |
| 10 | Undocumented components prioritized by reuse frequency, hierarchy level, complexity | COV-003 |
| 11 | Consolidation candidates include similarity, recommendation, and estimated effort | CSL-001 |
| 12 | Design system maturity classified with supporting coverage and drift ratio evidence | MAT-001, MAT-002 |
| 13 | Synthesis Judgments Summary lists every AI judgment call with confidence classification | CLS-001 |
| 14 | Navigation table present with correct anchor links (H-23) | H-23 |
| 15 | Degraded mode disclosure present if operating in Manual Component Inventory Mode | P-022, TKN-006, COV-004 |
| 16 | Handoff Data section populated for `/ux-inclusive-design` downstream consumption | SKILL.md handoff threshold |
| 17 | Same component pattern classified consistently across the entire inventory | ADJ-004 |
| 18 | Handoff table includes only components with assigned level, name, and variant count | HAND-001 |
| 19 | Unclassified components excluded from Handoff Data table and YAML | HAND-002 |
| 20 | `handoff_components_count` YAML field matches Handoff Data table row count | HAND-003 |

---

*Rule file: atomic-design-rules.md*
*Version: 1.1.0*
*Parent sub-skill: /ux-atomic-design*
*Parent skill: /user-experience*
*Agent: ux-atomic-architect*
*SSOT: `skills/ux-atomic-design/SKILL.md` (v1.2.0)*
*Created: 2026-03-04*

<!-- Traceability: PROJ-022 EPIC-003. Standards: H-23 (navigation), H-34 (agent-dev), SR-002 (input validation), SR-003 (output filtering). Methodology: Frost, B. (2016) "Atomic Design." Synthesis validation: skills/user-experience/rules/synthesis-validation.md. Quality gate: .context/rules/quality-enforcement.md. ORCHESTRATION: projects/PROJ-022-user-experience-skill/orchestration/ux-skill-build-20260303-001/ORCHESTRATION.yaml -->
<!-- VERSION: 1.1.0 | DATE: 2026-03-04 | SOURCE: skills/ux-atomic-design/SKILL.md (v1.2.0), skills/ux-atomic-design/agents/ux-atomic-architect.md (v1.0.1), Frost (2016) "Atomic Design" | REVISION: iter2 — Handoff Threshold Rules, synthesis-validation.md version pin, TAX-005 clarification, drift-maturity cross-ref, effort criteria, Related Files annotations -->
