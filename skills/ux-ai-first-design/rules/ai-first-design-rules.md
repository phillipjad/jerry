<!-- VERSION: 1.1.0 | DATE: 2026-03-04 | REVISION: iter2 — added AI Transparency Assessment Rules section (AID-013 through AID-013c), PAIR inline citation, template version fix, nav table update, cognitive mode note | SOURCE: skills/ux-ai-first-design/SKILL.md (v1.1.0), skills/ux-ai-first-design/agents/ux-ai-design-guide.md (v1.0.0), Yang et al. (2020) DOI:10.1145/3313831.3376301, Amershi et al. (2019) DOI:10.1145/3290605.3300233, Shneiderman (2020) DOI:10.1080/10447318.2020.1741118, Google PAIR (2019) | PARENT: /ux-ai-first-design sub-skill -->

# AI-First Interaction Design Rules

> Operational constraints and methodology rules for the `ux-ai-design-guide` agent. Provides conditional activation enforcement, trust-risk classification rules, error-risk classification rules, interaction pattern selection rules (3x3 matrix), Amershi guidelines integration rules, progressive disclosure rules (Shneiderman 5-stage), AI transparency assessment rules (PAIR patterns), AI staleness risk disclosure enforcement, confidence classification, output format requirements, and quality gate integration that complement the agent definition.
>
> **Cognitive mode note:** The agent definition declares `cognitive_mode: divergent` per AD-M-005, reflecting the agent's design-space exploration role (generating alternative interaction patterns, exploring trust-risk scenarios, considering multiple progressive disclosure strategies). The rules below enforce systematic execution discipline within that divergent exploration — classification algorithms, matrix lookups, and threshold criteria are convergent mechanisms that structure the agent's divergent output into consistent, comparable results. The divergent mode governs *how the agent reasons*; these rules govern *how it structures its conclusions*.

## Document Sections

| Section | Purpose |
|---------|---------|
| [Conditional Activation Rules](#conditional-activation-rules) | WSM >= 7.80 AND FEAT-020 DONE check; fallback to /ux-heuristic-eval with PAIR protocol |
| [Trust-Risk Classification Rules](#trust-risk-classification-rules) | Yang et al. (2020) 4 assessment criteria, classification algorithm, HIGH/MEDIUM/LOW |
| [Error-Risk Classification Rules](#error-risk-classification-rules) | Yang et al. (2020) 4 assessment criteria, classification algorithm, HIGH/MEDIUM/LOW |
| [Interaction Pattern Selection Rules](#interaction-pattern-selection-rules) | 3x3 matrix (trust-risk x error-risk), provenance note, "never lower oversight" safety rule |
| [Amershi Guidelines Integration Rules](#amershi-guidelines-integration-rules) | 18 guidelines across 4 phases (Initially G1-G2, During G3-G8, When wrong G9-G13, Over time G14-G18) |
| [Progressive Disclosure Rules](#progressive-disclosure-rules) | Shneiderman (2020) 5-stage framework with stage advancement criteria |
| [AI Transparency Assessment Rules](#ai-transparency-assessment-rules) | PAIR pattern categories: explainability, user control, feedback design, mental model calibration |
| [AI Staleness Risk Disclosure Rules](#ai-staleness-risk-disclosure-rules) | Mandatory disclosure of training data staleness and rapidly evolving AI interaction patterns |
| [Confidence Classification Rules](#confidence-classification-rules) | ALL recommendations LOW confidence; shared taxonomy from synthesis-validation.md |
| [Output Format Rules](#output-format-rules) | Required sections matching ai-first-design-template.md |
| [Quality Gate Integration](#quality-gate-integration) | S-014 dimension mapping for AI-first design output |
| [Related Files](#related-files) | Dependency matrix: upstream, downstream, and sibling references |
| [Self-Review Checklist](#self-review-checklist) | S-010 verification before output persistence |

---

## Conditional Activation Rules

The `/ux-ai-first-design` sub-skill is CONDITIONAL. It operates in Wave 5 (Process Intensives) and requires two activation criteria to be met before the agent proceeds with AI-first interaction design work.

> **Source:** `skills/user-experience/rules/wave-progression.md` (v1.2.0) Wave 5 entry conditions; `skills/ux-ai-first-design/SKILL.md` (v1.1.0) [When to Use This Sub-Skill].

### Activation Criteria

| Criterion | Verification Method | Pass Condition |
|-----------|-------------------|----------------|
| **WSM (Wave Scorecard Metric)** | Check most recent wave signoff at `skills/user-experience/rules/wave-progression.md` | WSM >= 7.80 |
| **Enabler FEAT-020** | Check FEAT-020 status in WORKTRACKER.md | Status = DONE |

### Activation Discipline

| ID | Rule | Tier | Consequence of Violation |
|----|------|------|--------------------------|
| AID-001 | CONDITIONAL activation MUST verify WSM >= 7.80 AND enabler FEAT-020 DONE before proceeding with any design work. Both criteria are required; partial satisfaction is insufficient. Verification MUST be documented in the Engagement Context section of the output. | HARD | Proceeding without activation verification produces AI interaction design guidance for teams that lack the UX maturity to apply it; the guidance may be misapplied and create dangerous trust calibration or inappropriate autonomy levels |
| AID-001a | When CONDITIONAL activation fails (either criterion unmet), the agent MUST halt and inform the orchestrator to route to `/ux-heuristic-eval` with PAIR protocol (AI-specific heuristic supplement) as an interim alternative. The agent MUST NOT produce AI-first design output when the activation condition fails. | HARD | Producing output without activation creates trust in an analysis the team cannot act on; interim PAIR protocol provides appropriate AI coverage at the team's current maturity |
| AID-001b | The activation verification result (WSM score, FEAT-020 status, PASS/FAIL) MUST appear in the output's Engagement Context section. | HARD | Omitting activation verification violates P-022; downstream consumers cannot assess whether the output was produced under valid conditions |

---

## Trust-Risk Classification Rules

Trust-risk classification assesses how much users should trust AI outputs, determining the appropriate trust calibration target. Yang et al. (2020) identify trust miscalibration as a primary failure mode: users who over-trust AI make dangerous errors of omission, while users who under-trust AI abandon valuable features.

> **Source:** Yang, Q., Steinfeld, A., Rose, C., & Zimmerman, J. (2020). "Re-examining Whether, Why, and How Human-AI Interaction Is Uniquely Difficult to Design." CHI '20. DOI: [10.1145/3313831.3376301](https://doi.org/10.1145/3313831.3376301).

### Trust-Risk Level Definitions

| Level | Definition | User-AI Relationship | Examples |
|-------|-----------|---------------------|----------|
| **HIGH** | AI makes decisions autonomously; user delegates control | User trusts AI to act without review | Autonomous trading, self-driving, automated content moderation |
| **MEDIUM** | AI recommends; human reviews and decides | User evaluates AI recommendation before acting | Medical diagnosis suggestions, hiring shortlist, content recommendations |
| **LOW** | AI assists; human maintains full control | User uses AI as a tool but makes all decisions | Search autocomplete, grammar suggestions, code completion |

### Assessment Criteria

| Criterion | Rating Scale | Assessment Question |
|-----------|-------------|---------------------|
| **Consequence of over-trust** | Catastrophic / Significant / Minor | What happens if a user accepts an incorrect AI output without review? |
| **Consequence of under-trust** | Significant loss / Minor loss / Negligible | What happens if a user ignores a correct AI output? |
| **User expertise level** | Expert / Intermediate / Novice | Can the user independently evaluate AI output quality? |
| **AI output verifiability** | Easily verifiable / Partially verifiable / Unverifiable | Can the user verify AI correctness before acting? |

### Classification Algorithm

- Consequence of over-trust = catastrophic OR output unverifiable -> **HIGH** trust-risk
- Consequence of over-trust = significant AND user = novice -> **HIGH** trust-risk
- Consequence of over-trust = significant AND user = intermediate -> **MEDIUM** trust-risk
- Consequence of over-trust = minor AND output easily verifiable -> **LOW** trust-risk
- If no above criteria are met, apply the conservative default: **MEDIUM** trust-risk (per Yang et al., 2020)
- **Tie-breaker:** When multiple rules fire for conflicting levels, apply the higher-risk classification

### Trust-Risk Discipline

| ID | Rule | Tier | Consequence of Violation |
|----|------|------|--------------------------|
| AID-002 | Trust-risk classification MUST use all 4 Yang et al. assessment criteria (consequence of over-trust, consequence of under-trust, user expertise level, AI output verifiability) with explicit evidence for each criterion. No criterion may remain unassessed. | HARD | Incomplete criteria coverage may miss critical trust miscalibration risk factors; the classification algorithm requires all 4 criteria for reliable risk assessment |
| AID-002a | The trust-risk classification MUST include the full classification algorithm trace: which rules were evaluated, which rule matched, whether the tie-breaker was applied, and the resulting trust-risk level. | HARD | Algorithm trace omission prevents downstream review of the classification decision; violates P-001 traceability requirement |
| AID-002b | Every assessment criterion rating MUST cite specific evidence or be explicitly marked as inferred. Ratings without evidence or inference marking are REJECTED. | HARD | Unsupported ratings violate P-001 (truth and accuracy) and prevent downstream validation |
| AID-002c | When uncertain between two adjacent trust-risk levels, MUST choose the HIGHER risk level. Under-protecting against trust miscalibration is more costly than over-protecting (Yang et al., 2020). | HARD | Optimistic classification masks trust miscalibration risk; may result in insufficient human oversight for AI-powered features |
| AID-011a | When multiple classification rules fire for conflicting trust-risk levels, MUST apply the higher-risk classification. NEVER select the lower-risk level when conflicting rules fire. | HARD | Selecting the lower-risk level when rules conflict under-protects against trust miscalibration; Yang et al. (2020) establish that the cost of under-protection exceeds the cost of over-protection |

---

## Error-Risk Classification Rules

Error-risk classification evaluates the cost of AI errors, determining the appropriate error mitigation design. Yang et al. (2020) identify error cost mismanagement as the second primary failure mode: underestimating error costs creates brittle AI interfaces that fail catastrophically, while overestimating error costs creates excessively cautious interfaces that reduce AI utility.

> **Source:** Yang, Q., Steinfeld, A., Rose, C., & Zimmerman, J. (2020). DOI: [10.1145/3313831.3376301](https://doi.org/10.1145/3313831.3376301).

### Error-Risk Level Definitions

| Level | Definition | Error Characteristics | Examples |
|-------|-----------|----------------------|----------|
| **HIGH** | Irreversible or safety-critical errors | Errors cannot be undone; may cause physical, financial, or legal harm | Medical treatment decisions, financial transactions, safety system overrides |
| **MEDIUM** | Costly but recoverable errors | Errors require significant effort to correct but are not permanent | Content publishing, email scheduling, resource allocation |
| **LOW** | Negligible-impact errors | Errors are easily corrected or have minimal consequence | Search suggestions, content formatting, UI customization |

### Assessment Criteria

| Criterion | Rating Scale | Assessment Question |
|-----------|-------------|---------------------|
| **Reversibility** | Irreversible / Reversible with significant cost / Easily reversible | Can the AI error be undone? |
| **Blast radius** | Organization-wide / Team-group / Individual only | How many users/systems are affected by a single error? |
| **Error detection latency** | Immediate / Delayed / Hidden | How quickly can an error be detected? |
| **Recovery cost** | High / Moderate / Low | What does it take to recover from an error? |

### Classification Algorithm

- Irreversible AND blast radius = organization-wide -> **HIGH** error-risk
- Irreversible AND detection = hidden -> **HIGH** error-risk
- Reversible with significant cost AND blast radius = team/group -> **MEDIUM** error-risk
- Easily reversible AND blast radius = individual -> **LOW** error-risk
- If no above criteria are met, apply the conservative default: **MEDIUM** error-risk
- **Tie-breaker:** When multiple rules fire for conflicting levels, apply the higher-risk classification

### Error-Risk Discipline

| ID | Rule | Tier | Consequence of Violation |
|----|------|------|--------------------------|
| AID-003 | Error-risk classification MUST use all 4 Yang et al. assessment criteria (reversibility, blast radius, error detection latency, recovery cost) with explicit evidence for each criterion. No criterion may remain unassessed. | HARD | Incomplete criteria coverage may miss critical error cost factors; the classification algorithm requires all 4 criteria for reliable risk assessment |
| AID-003a | The error-risk classification MUST include the full classification algorithm trace: which rules were evaluated, which rule matched, whether the tie-breaker was applied, and the resulting error-risk level. | HARD | Algorithm trace omission prevents downstream review of the classification decision; violates P-001 traceability requirement |
| AID-003b | Every assessment criterion rating MUST cite specific evidence or be explicitly marked as inferred. Ratings without evidence or inference marking are REJECTED. | HARD | Unsupported ratings violate P-001 (truth and accuracy) and prevent downstream validation |
| AID-003c | When uncertain between two adjacent error-risk levels, MUST choose the HIGHER risk level. Underestimating error cost creates brittle interfaces that fail catastrophically (Yang et al., 2020). | HARD | Optimistic classification masks error cost risk; may result in insufficient error mitigation for AI-powered features |
| AID-011b | When multiple classification rules fire for conflicting error-risk levels, MUST apply the higher-risk classification. NEVER select the lower-risk level when conflicting rules fire. | HARD | Selecting the lower-risk level when rules conflict underestimates error cost; Yang et al. (2020) establish that brittle interfaces from underestimated error cost fail catastrophically |

---

## Interaction Pattern Selection Rules

The trust-risk x error-risk matrix produces nine cells, each mapping to a specific human-AI collaboration pattern. The matrix operationalizes Yang et al.'s (2020) conceptual framework into actionable design patterns.

> **Provenance note (AID-012):** The 3x3 trust-risk x error-risk interaction pattern matrix is the authors' operationalization synthesizing Yang et al.'s (2020) conceptual framework into actionable design patterns. Yang et al. identify trust miscalibration and error cost mismanagement as the two primary failure modes; this matrix maps those failure modes to specific human-AI collaboration patterns. The cell labels and pattern descriptions are derived, not verbatim Yang et al. constructs.

### 3x3 Interaction Pattern Matrix

| | LOW Error-Risk | MEDIUM Error-Risk | HIGH Error-Risk |
|---|---|---|---|
| **HIGH Trust-Risk** | AI autonomous with periodic review | AI advisor with mandatory review | Full human oversight, AI as information provider only |
| **MEDIUM Trust-Risk** | AI autonomous with user correction | Human-in-the-loop with AI assistance | Human-controlled with AI safety checks |
| **LOW Trust-Risk** | AI fully autonomous (low stakes) | AI suggests with easy override | AI assists with mandatory human verification |

### Pattern Selection Procedure

1. Map the trust-risk level (Phase 2) and error-risk level (Phase 3) to the matrix cell
2. Identify the primary interaction pattern for that cell
3. Evaluate whether the pattern matches the product's technical constraints (does the AI system support the required human oversight mechanism?)
4. If technical constraints prevent the ideal pattern, select the adjacent cell with **higher human oversight** (never lower -- AID-005)
5. Document the selected pattern, the rationale, and any deviation from the matrix recommendation

### Pattern Selection Discipline

| ID | Rule | Tier | Consequence of Violation |
|----|------|------|--------------------------|
| AID-004 | The interaction pattern MUST be selected from the 3x3 trust-risk x error-risk matrix. The selected matrix cell (trust-risk level x error-risk level) MUST be documented with rationale for the selection. Free-form pattern selection outside the matrix is REJECTED. | HARD | Free-form pattern selection bypasses the structured risk classification; patterns not grounded in the matrix may misalign human oversight with actual trust-risk and error-risk levels |
| AID-005 | When deviating from the matrix recommendation due to technical constraints, the agent MUST select the adjacent cell with HIGHER human oversight. NEVER lower human oversight when deviating from the matrix. This is a safety invariant. | HARD | Lowering human oversight in response to technical constraints exposes users to trust miscalibration or error cost that the original classification identified; safety violations may result |
| AID-005a | The "never lower oversight" rule applies to ALL deviations, including user-requested overrides. If a user requests a lower-oversight pattern than the matrix recommends, the agent MUST document the risk and note that the user has explicitly accepted the higher risk per P-020 (user authority). | HARD | Silently lowering oversight without documenting the risk violates P-022; user authority (P-020) permits the override but the risk must be disclosed |
| AID-012 | The 3x3 matrix provenance note MUST appear in the output. The note MUST state that the matrix is the authors' operationalization of Yang et al.'s (2020) conceptual framework, not a verbatim Yang et al. construct. | HARD | Omitting provenance misattributes derived work to Yang et al.; violates P-001 (truth and accuracy) and may mislead teams about the evidentiary basis of the matrix |

---

## Amershi Guidelines Integration Rules

Feedback loop design addresses four interaction phases per Amershi et al.'s (2019) 18 guidelines for human-AI interaction. Every AI interaction design output MUST include feedback loop specifications covering all four phases.

> **Source:** Amershi, S., Weld, D., Vorvoreanu, M., et al. (2019). "Guidelines for Human-AI Interaction." CHI '19. DOI: [10.1145/3290605.3300233](https://doi.org/10.1145/3290605.3300233). Complemented by Google PAIR (2019). "People + AI Guidebook." Available at [pair.withgoogle.com/guidebook](https://pair.withgoogle.com/guidebook) — practitioner resource (not peer-reviewed) providing implementation-oriented patterns for AI transparency, explainability, user control, and feedback design.

### Guideline Phase Mapping

| Phase | Amershi Guidelines | Design Scope |
|-------|-------------------|--------------|
| **Initially** (G1-G2) | G1: Make clear what the system can do; G2: Make clear how well the system can do it | Onboarding: capability disclosure, accuracy expectations, limitation statements |
| **During interaction** (G3-G8) | G3: Time services based on context; G4: Show contextually relevant information; G5: Match relevant social norms; G6: Mitigate social biases; G7: Support efficient invocation/dismissal; G8: Make clear why the system did what it did | Real-time: contextual explanations, confidence indicators, dismissal controls |
| **When wrong** (G9-G13) | G9: Support efficient correction; G10: Scope services when in doubt; G11: Make clear how to invoke; G12: Make clear how to provide feedback; G13: Learn from user behavior | Error recovery: correction mechanisms, feedback channels, graceful degradation |
| **Over time** (G14-G18) | G14: Learn from user behavior; G15: Update and adapt cautiously; G16: Encourage granular feedback; G17: Convey consequences of user actions; G18: Provide global controls | Evolution: adaptation transparency, control settings, usage analytics |

### Feedback Loop Discipline

| ID | Rule | Tier | Consequence of Violation |
|----|------|------|--------------------------|
| AID-006 | The feedback loop design MUST cover all 4 Amershi interaction phases (Initially G1-G2, During interaction G3-G8, When wrong G9-G13, Over time G14-G18). No phase may be omitted. | HARD | Omitting any phase leaves a gap in the AI communication design; users encounter AI behavior without appropriate feedback mechanisms for that interaction stage |
| AID-006a | Each guideline applied MUST cite the specific Amershi et al. guideline ID (G1-G18) and describe the design element that implements it in the context of the selected interaction pattern. | HARD | Uncited guideline application prevents traceability; reviewers cannot verify which guidelines were considered and how they were operationalized |
| AID-006b | The feedback loop design MUST be consistent with the selected interaction pattern. A feedback loop designed for autonomous AI is inconsistent with a pattern requiring full human oversight. | MEDIUM | Inconsistent feedback loop design creates misaligned user expectations; the feedback mechanisms must match the human-AI collaboration level specified by the interaction pattern |
| AID-006c | For the "When wrong" phase (G9-G13), the feedback loop MUST include at least one explicit error correction mechanism and one feedback channel. Error recovery without correction mechanisms leaves users unable to recover from AI errors. | HARD | Missing correction mechanisms violate the core purpose of the "When wrong" phase; users encountering AI errors without correction paths experience trust erosion and helplessness |

---

## Progressive Disclosure Rules

Progressive disclosure builds user trust through graduated exposure to AI capabilities. The Shneiderman (2020) 5-stage framework governs how AI features transition from fully human-controlled to progressively autonomous.

> **Source:** Shneiderman, B. (2020). "Human-Centered Artificial Intelligence: Reliable, Safe & Trustworthy." International Journal of Human-Computer Interaction, 36(6), pp. 495-504. DOI: [10.1080/10447318.2020.1741118](https://doi.org/10.1080/10447318.2020.1741118).

### Five-Stage Framework

| Stage | Trust Level | AI Autonomy | User Control | Duration |
|-------|-------------|-------------|-------------|----------|
| **1: Introduction** | Minimal trust | AI explains only; no actions | Full user control | First 1-2 weeks |
| **2: Suggestion** | Growing trust | AI suggests; user decides | Accept/reject controls | Weeks 2-4 |
| **3: Collaboration** | Established trust | AI drafts; user edits and approves | Edit + approve workflow | Months 1-2 |
| **4: Delegation** | High trust | AI acts; user monitors and corrects | Monitoring dashboard + undo | Months 2+ |
| **5: Autonomy** | Full trust | AI operates independently within bounds | Exception-only intervention | After 30+ days at Stage 4 with error rate below threshold AND explicit user opt-in |

### Stage Advancement Criteria

Each stage advancement requires ALL of the following:

1. **Minimum time at current stage** -- no instant escalation to higher autonomy
2. **Explicit user opt-in** -- user must actively choose higher autonomy (never automatic advancement)
3. **Error rate at current stage below threshold** -- suggested: < 5% LOW error-risk, < 2% MEDIUM error-risk, < 0.5% HIGH error-risk (team-defined)
4. **User demonstrates correction capability** -- user has successfully corrected at least one AI error at the current stage

> **Calibration note:** Duration estimates are heuristic starting points. Teams SHOULD adjust based on domain risk profile, user sophistication, and observed trust-building velocity.

### Progressive Disclosure Discipline

| ID | Rule | Tier | Consequence of Violation |
|----|------|------|--------------------------|
| AID-007 | The progressive disclosure plan MUST include all 5 stages (Introduction, Suggestion, Collaboration, Delegation, Autonomy) with stage-specific advancement criteria and rollback conditions. No stage may be omitted. | HARD | Omitting stages breaks the graduated trust-building sequence; users may be exposed to inappropriate AI autonomy levels without the trust foundation established by earlier stages |
| AID-007a | Stage 5 (Autonomy) MUST require explicit user opt-in AND 30+ days at Stage 4 with error rate below threshold. Stage 5 MUST NOT be presented as automatic or inevitable. | HARD | Automatic progression to full AI autonomy bypasses the user's informed consent; users who have not demonstrated sustained trust at Stage 4 are not ready for autonomous AI operation |
| AID-007b | Duration estimates for each stage MUST be included. Estimates MUST be disclosed as heuristic starting points requiring empirical calibration, not prescriptive timelines. | MEDIUM | Undisclosed estimation basis violates P-022; teams may treat heuristic durations as validated benchmarks |
| AID-007c | Each stage MUST include rollback conditions: criteria under which the user is returned to a lower autonomy stage (e.g., error rate exceeds threshold, user requests reduced autonomy). | HARD | Progressive disclosure without rollback is unidirectional; users who experience increased AI errors at higher stages have no defined path to reduce autonomy |

---

## AI Transparency Assessment Rules

AI transparency assessment evaluates the product's current AI transparency implementation against Google PAIR (2019) patterns. This section operationalizes the PAIR Guidebook's transparency, explainability, and user control patterns into assessable criteria.

> **Source:** Google. (2019). "People + AI Guidebook." Available at [pair.withgoogle.com/guidebook](https://pair.withgoogle.com/guidebook). Practitioner resource (not peer-reviewed); complements the peer-reviewed Amershi et al. (2019) guidelines with implementation-oriented patterns.

### PAIR Pattern Categories

| Category | PAIR Patterns | Assessment Focus |
|----------|--------------|------------------|
| **Transparency** | Explain AI capabilities, disclose limitations, show data sources | Does the AI system clearly communicate what it can and cannot do? |
| **Explainability** | Show reasoning, provide confidence, explain factors | Can users understand why the AI produced a specific output? |
| **User Control** | Provide override mechanisms, allow customization, enable opt-out | Can users adjust, override, or disable AI behavior? |
| **Feedback** | Enable correction, collect implicit signals, support explicit feedback | Can users tell the AI when it is wrong and influence its future behavior? |
| **Confidence Communication** | Display uncertainty, calibrate expectations, handle low-confidence gracefully | Does the AI communicate its certainty level to users? |

### Transparency Assessment Discipline

| ID | Rule | Tier | Consequence of Violation |
|----|------|------|--------------------------|
| AID-013 | The AI Transparency Assessment MUST evaluate the product against all 5 PAIR pattern categories (transparency, explainability, user control, feedback, confidence communication). No category may be omitted. | HARD | Omitting a transparency category leaves blind spots in the AI interaction design; users may encounter AI behavior without appropriate transparency mechanisms |
| AID-013a | Each identified transparency gap MUST be classified by severity (Critical: user cannot understand AI actions; Major: user understanding is partial; Minor: user understanding is adequate but could be improved). | MEDIUM | Unclassified transparency gaps prevent prioritization of design improvements |
| AID-013b | Explainability recommendations MUST be calibrated to the selected interaction pattern. Autonomous patterns (low trust-risk, low error-risk) require less explanation than human-oversight patterns (high trust-risk, high error-risk). | HARD | Mismatched explainability depth wastes design effort on low-stakes interactions while under-explaining high-stakes ones |
| AID-013c | Confidence communication design MUST be consistent with the trust-risk classification. HIGH trust-risk products MUST display AI confidence levels prominently; LOW trust-risk products MAY use subtle confidence indicators. | MEDIUM | Inconsistent confidence communication between trust-risk level and UI design creates user confusion about when to trust AI output |

---

## AI Staleness Risk Disclosure Rules

The field of human-AI interaction design is rapidly evolving. Training data for the `ux-ai-design-guide` agent may not reflect the latest AI interaction paradigms, platform-specific guidelines, or emerging best practices for agentic AI, multi-modal AI, or autonomous agent interfaces.

> **Source:** P-022 (No Deception); `skills/ux-ai-first-design/agents/ux-ai-design-guide.md` [methodology] Single-Agent Reliability Note and Acknowledged Limitation.

### Staleness Risk Discipline

| ID | Rule | Tier | Consequence of Violation |
|----|------|------|--------------------------|
| AID-009 | AI pattern staleness risk disclosure MUST appear in every output. The disclosure MUST state that: (a) the AI interaction design field evolves rapidly, (b) training data may not reflect the latest AI interaction paradigms, platform-specific guidelines (e.g., Apple Intelligence HIG, Google Gemini UX), or emerging best practices for agentic/multi-modal/autonomous AI, (c) the Yang et al. (2020) and Amershi et al. (2019) frameworks are the most rigorous available but new paradigms may require pattern extensions not covered by these frameworks. | HARD | Omitting staleness disclosure violates P-022; teams may treat AI design recommendations as current best practices without understanding the training data limitations |
| AID-009a | The REFERENCE-ONLY banner MUST appear in the Feedback Loop Design section: "AI-First Design recommendations are based on the trust-risk/error-risk framework (Yang et al., 2020) and established guidelines (Amershi et al., 2019; Google PAIR, 2019). The AI interaction design field evolves rapidly; validate recommendations against current platform-specific guidelines and user testing before implementation." | HARD | Missing banner understates the speculative nature of AI interaction design recommendations; P-022 requires explicit disclosure of limitations |
| AID-009b | When operating in degraded mode (WebSearch, WebFetch, or Context7 unavailable), the degraded mode banner MUST appear immediately after the document header, disclosing which tools were unavailable and the resulting limitations. | HARD | Undisclosed degraded mode violates P-022; Evidence Quality dimension receives a 0 score per quality gate rules |

---

## Confidence Classification Rules

Every AI-generated judgment in the design output requires a confidence classification. AI-first interaction design outputs follow a predictable confidence pattern because the frameworks provide structured analysis but cannot replace empirical validation of AI interaction patterns.

> **Source:** `skills/user-experience/rules/synthesis-validation.md` (v1.1.0) Section "Confidence Classification" and Section "Sub-Skill Synthesis Output Map."

### Classification Criteria

| Classification | Criteria | Action | Example |
|---------------|----------|--------|---------|
| **HIGH** | Multiple data sources converge; validated by quantitative AI system performance data AND qualitative evidence | Proceed with recommendation | Trust-risk classification supported by AI error rate data + user trust survey + usage analytics |
| **MEDIUM** | Single-framework reasoning; assessment based on available evidence without full empirical validation | Include "Validation Required" note | Trust-risk classification from AI capability characterization and team-provided domain context |
| **LOW** | Insufficient data; AI inference without empirical grounding; speculative assessment | Flag for human review before acting | Interaction pattern recommendation; progressive disclosure timeline; feedback loop design choices |

### Judgment Types Requiring Classification

| Judgment Type | Description | Typical Confidence |
|---------------|-------------|-------------------|
| Conditional activation verification | Confirming WSM and FEAT-020 status | HIGH (deterministic check) |
| AI capability characterization | Assessing determinism, confidence availability, failure modes, learning behavior | MEDIUM (depends on evidence quality) |
| Trust-risk criterion rating | Assessing consequence of over-trust, under-trust, user expertise, output verifiability | MEDIUM (framework-structured but involves interpretive judgment) |
| Trust-risk classification | Applying classification algorithm to produce HIGH/MEDIUM/LOW | MEDIUM (algorithm constrains variance; evidence-dependent) |
| Error-risk criterion rating | Assessing reversibility, blast radius, detection latency, recovery cost | MEDIUM (framework-structured but involves interpretive judgment) |
| Error-risk classification | Applying classification algorithm to produce HIGH/MEDIUM/LOW | MEDIUM (algorithm constrains variance; evidence-dependent) |
| Interaction pattern selection | Selecting pattern from 3x3 matrix based on classified risk levels | LOW (matrix lookup is deterministic but pattern applicability requires judgment) |
| Feedback loop design | Designing 4-phase Amershi guideline implementation | LOW (design choices are speculative without user testing) |
| Progressive disclosure plan | Defining 5-stage rollout with timing estimates | LOW (timeline and advancement criteria require empirical calibration) |
| AI transparency assessment | Evaluating against PAIR patterns | LOW (pattern applicability is context-dependent) |

### AI-First Design Confidence Dynamics

AI-First Design outputs follow a predictable confidence pattern:

- **Classification outputs** (trust-risk, error-risk) are inherently MEDIUM -- the Yang et al. (2020) framework provides structured assessment but criterion ratings involve interpretive judgment about AI system behavior and user populations
- **Design outputs** (interaction pattern selection, feedback loop, progressive disclosure, transparency assessment) are inherently LOW -- design effectiveness depends on implementation context, user behavior, and AI system specifics that analysis cannot capture
- **Post-validation outputs** (if follow-up data is provided) may reach HIGH when the design converges with `/ux-heart-metrics` quantitative measurement

### Classification Discipline

| ID | Rule | Tier | Consequence of Violation |
|----|------|------|--------------------------|
| AID-008 | ALL interaction pattern recommendations, feedback loop designs, progressive disclosure plans, and AI transparency assessments MUST carry LOW confidence classification. These are design recommendations requiring empirical validation. | HARD | Presenting design recommendations without LOW confidence violates P-022; users may over-commit to untested AI interaction patterns |
| AID-008a | Trust-risk and error-risk classifications MUST carry MEDIUM confidence (not HIGH) when based on framework analysis without quantitative AI system performance data. HIGH requires convergence of quantitative data (error rates, confidence distributions, user correction rates) with qualitative evidence. | HARD | MEDIUM-without-quantitative inflated to HIGH misleads teams about classification certainty; P-022 violation |
| AID-008b | NEVER classify a design recommendation (interaction pattern, feedback loop, progressive disclosure) as MEDIUM or HIGH. All design recommendations are LOW because effectiveness requires empirical validation through user testing or A/B experimentation. | HARD | Design recommendations classified MEDIUM/HIGH mislead teams into false confidence; design effectiveness requires empirical validation |
| AID-010 | The Synthesis Judgments Summary MUST list every AI judgment call with classification type, confidence level (HIGH/MEDIUM/LOW), and a one-line rationale. | HARD | Judgment calls without confidence classification cannot be validated by the downstream synthesis pipeline; P-022 violation |
| AID-010a | The minimum-confidence rule applies: when a single finding draws from multiple judgment types with different confidence levels, the finding's confidence is the LOWEST among all contributing judgments. | HARD | Selecting a higher-than-minimum confidence for a composite finding overstates certainty; downstream synthesis inherits inflated confidence |

---

## Output Format Rules

The design guide's output MUST follow the structure defined in `skills/ux-ai-first-design/templates/ai-first-design-template.md`. These rules enforce section completeness and format compliance.

> **Source:** `skills/ux-ai-first-design/templates/ai-first-design-template.md`, SKILL.md [Output Specification].

### Required Sections

| Section | Level | Completeness Criteria |
|---------|-------|-----------------------|
| **Executive Summary** | L0 | Trust-risk classification stated; error-risk classification stated; selected interaction pattern stated; human oversight level stated; top 3-5 design recommendations listed; key findings for stakeholders |
| **Engagement Context** | L1 | Product name, target users, AI capability characterization, AI technology type, determinism level, confidence availability, failure modes, upstream inputs table, evidence inventory, CONDITIONAL activation verification result |
| **Trust-Risk Assessment** | L1 | All 4 criteria assessed with evidence; classification algorithm trace; trust-risk level stated |
| **Error-Risk Assessment** | L1 | All 4 criteria assessed with evidence; classification algorithm trace; error-risk level stated |
| **Interaction Pattern Specification** | L1 | Selected matrix cell; pattern name and description; design elements; technical constraints assessment; deviation rationale (if any) respecting "never lower oversight" |
| **Feedback Loop Design** | L1 | REFERENCE-ONLY banner; all 4 Amershi phases covered with guideline IDs; design elements per phase |
| **Progressive Disclosure Plan** | L1 | REFERENCE-ONLY banner for duration estimates; all 5 stages with trust level, AI autonomy, user control, duration estimate, advancement criteria, rollback conditions |
| **AI Transparency Assessment** | L1 | PAIR pattern evaluation; transparency gaps with severity; explainability recommendations; confidence communication design |
| **Strategic Implications** | L2 | AI interaction maturity assessment; trust calibration roadmap; AI capability progression strategy; organizational readiness analysis |
| **Synthesis Judgments Summary** | L1 | Every AI judgment call listed with classification type, confidence level, and rationale |
| **Handoff Data** | L1 | YAML blocks for `/ux-inclusive-design` and `/ux-heuristic-eval` conforming to `docs/schemas/handoff-v2.schema.json` with `ux_ext` extension fields |

### Output Format Discipline

| ID | Rule | Tier | Consequence of Violation |
|----|------|------|--------------------------|
| OUT-001 | All 11 required sections MUST be present in the output. Missing sections trigger self-review rejection. | HARD | Incomplete output fails the Completeness dimension of the quality gate |
| OUT-002 | The navigation table (H-23) MUST be present with anchor links to all 11 sections. | HARD | Missing navigation violates H-23; document rejected |
| OUT-003 | The Executive Summary MUST contain exactly 3-5 key findings bullets. Fewer than 3 is insufficient for cross-framework synthesis; more than 5 dilutes the summary. | MEDIUM | Cross-framework synthesis receives insufficient orientation data |
| OUT-004 | The Trust-Risk Assessment MUST include the 4-criterion table with ratings and evidence AND the classification algorithm trace. The Error-Risk Assessment MUST include the 4-criterion table with ratings and evidence AND the classification algorithm trace. | HARD | Missing assessment tables or algorithm traces leave the risk classification incomplete; downstream pattern selection cannot execute without full criteria data |
| OUT-005 | The Interaction Pattern Specification MUST state the selected matrix cell coordinates (trust-risk level x error-risk level) and include the provenance note (AID-012). | HARD | Missing cell coordinates prevent verification of matrix lookup; missing provenance misattributes the matrix |
| OUT-006 | The Handoff Data YAML MUST conform to `docs/schemas/handoff-v2.schema.json` and include the `ux_ext` extension fields for downstream `/ux-inclusive-design` and `/ux-heuristic-eval` consumption. | HARD | Non-conforming handoff data rejected by downstream agents |
| OUT-007 | When operating in degraded mode (external tools unavailable), the degraded mode disclosure banner MUST appear immediately after the document header. | HARD | Undisclosed degraded mode violates P-022; Evidence Quality dimension receives a 0 score |

---

## Quality Gate Integration

AI-First Interaction Design output maps to the S-014 LLM-as-Judge rubric dimensions (`.context/rules/quality-enforcement.md` Section "Quality Gate") as follows:

### Dimension Mapping

| S-014 Dimension | Weight | AI-First Design Evaluation Criteria |
|-----------------|--------|-------------------------------------|
| **Completeness** | 0.20 | All 6 phases addressed; all 4 trust-risk criteria assessed; all 4 error-risk criteria assessed; interaction pattern selected from matrix with provenance note; feedback loop covers 4 Amershi phases with guideline IDs; progressive disclosure includes 5 stages with advancement criteria; AI transparency assessed against PAIR; handoff data populated for both downstream consumers |
| **Internal Consistency** | 0.20 | Trust-risk classification consistent with algorithm trace; error-risk classification consistent with algorithm trace; interaction pattern matches matrix cell for classified trust-risk x error-risk levels; feedback loop design matches selected interaction pattern's collaboration level; progressive disclosure stages align with trust-risk level (high trust-risk = slower progression) |
| **Methodological Rigor** | 0.20 | Yang et al. (2020) framework applied for both classifications; 4 criteria per classification with algorithm trace; 3x3 matrix provenance note present; Amershi et al. (2019) guidelines cited by ID; Shneiderman (2020) 5-stage framework applied; "never lower oversight" rule respected; conservative defaults applied when criteria ambiguous |
| **Evidence Quality** | 0.15 | Every criterion rating cites specific evidence or marks inference explicitly; evidence quality classification applied; no fabricated evidence; degraded mode disclosed when operating without external tools; AI staleness risk disclosure present |
| **Actionability** | 0.15 | Interaction pattern includes design elements (UI components, oversight mechanisms); feedback loop includes specific design elements per phase; progressive disclosure includes duration estimates and advancement criteria; recommendations prioritized; REFERENCE-ONLY banners present |
| **Traceability** | 0.10 | Trust-risk classification traces to 4 criteria with algorithm trace; error-risk classification traces to 4 criteria with algorithm trace; interaction pattern traces to matrix cell; feedback loop design elements trace to Amershi guideline IDs; progressive disclosure traces to Shneiderman (2020); methodology claims cite Yang et al. (2020), Amershi et al. (2019), PAIR (2019), Shneiderman (2020) |

### Scoring Discipline for AI-First Design

| ID | Rule | Tier | Consequence of Violation |
|----|------|------|--------------------------|
| QG-001 | The quality gate threshold applies to the overall design report, not to individual classifications or design elements. Baseline threshold: >= 0.92 (H-13 per `.context/rules/quality-enforcement.md` Section "Quality Gate", C2+). At C4 criticality (e.g., user-specified or auto-escalated per AE-002/AE-004), the threshold is >= 0.95 (governance source: PROJ-022 ORCHESTRATION.yaml C4 scoring specification). | HARD | Deliverable rejected per H-13; revision required |
| QG-002 | Completeness scoring MUST verify both trust-risk and error-risk classifications are present with full criteria and algorithm traces. An output missing either classification receives a 0 on the Completeness dimension. | HARD | Completeness dimension zeroed; composite score drops below threshold |
| QG-003 | Evidence Quality scoring MUST penalize undisclosed degraded mode operation. If the agent operated without external tools without the P-022 degraded mode banner, Evidence Quality receives a 0 score. | HARD | Evidence Quality dimension zeroed; P-022 violation |
| QG-004 | Internal Consistency scoring MUST verify that the interaction pattern selection is logically consistent with the trust-risk and error-risk classification algorithm traces. A pattern from the LOW-Trust-Risk x LOW-Error-Risk cell with HIGH trust-risk classification is a consistency failure. | HARD | Internal Consistency dimension penalized; logically inconsistent designs cannot be trusted for downstream implementation |

---

## Related Files

> Dependency matrix for operational traceability. Upstream files provide inputs or prerequisites; downstream files consume this rules file's outputs; sibling files share the same parent sub-skill.

| Relationship | File | Version | Purpose |
|-------------|------|---------|---------|
| **Parent SKILL.md** | `skills/ux-ai-first-design/SKILL.md` | v1.1.0 | Sub-skill definition; methodology overview; agent routing |
| **Agent definition** | `skills/ux-ai-first-design/agents/ux-ai-design-guide.md` | v1.0.0 | Agent frontmatter, system prompt, output section (handoff threshold) |
| **Governance YAML** | `skills/ux-ai-first-design/agents/ux-ai-design-guide.governance.yaml` | v1.0.0 | Enforcement metadata: quality_threshold (0.95), quality_gate (S-014) |
| **Output template** | `skills/ux-ai-first-design/templates/ai-first-design-template.md` | v1.0.0 | Report template consumed by design guide agent |
| **Wave progression** | `skills/user-experience/rules/wave-progression.md` | v1.2.0 | Wave 5 (Process Intensives) entry conditions; WSM >= 7.80 threshold |
| **Synthesis validation** | `skills/user-experience/rules/synthesis-validation.md` | v1.1.0 | Confidence classification shared taxonomy; Sub-Skill Synthesis Output Map |
| **MCP coordination** | `skills/user-experience/rules/mcp-coordination.md` | unversioned -- tracked via git history | MCP integration; degraded-mode disclosure requirements |
| **Quality enforcement** | `.context/rules/quality-enforcement.md` | SSOT -- version tracked externally (v1.6.0 at time of writing) | S-014 dimension rubric; H-13 quality gate threshold (>= 0.92 baseline, >= 0.95 at C4) |

> **Wave 5 prerequisite:** This rules file governs agent behavior in Wave 5 (Process Intensives). Per `wave-progression.md`, Wave 5 is CONDITIONAL on WSM >= 7.80 AND FEAT-020 DONE. The CONDITIONAL activation rules (AID-001) enforce this prerequisite at runtime.

---

## Self-Review Checklist

Before persisting the report, the design guide MUST verify (S-010, H-15):

| # | Check | Rule Reference |
|---|-------|---------------|
| 1 | CONDITIONAL activation verified (WSM >= 7.80, FEAT-020 DONE) and documented in Engagement Context | AID-001 |
| 2 | AI capability is characterized with determinism level, confidence availability, failure modes, and learning behavior | Phase 1 methodology |
| 3 | Trust-risk classification includes all 4 assessment criteria with evidence and the classification algorithm trace | AID-002 |
| 4 | Error-risk classification includes all 4 assessment criteria with evidence and the classification algorithm trace | AID-003 |
| 5 | Interaction pattern is selected from the 3x3 trust-risk x error-risk matrix with rationale documented | AID-004 |
| 6 | "Never lower oversight" rule is respected -- any deviation from the matrix goes toward higher human oversight, not lower | AID-005 |
| 7 | 3x3 matrix provenance note is present (authors' operationalization, not verbatim Yang et al.) | AID-012 |
| 8 | Feedback loop design covers all 4 Amershi interaction phases (Initially G1-G2, During G3-G8, When wrong G9-G13, Over time G14-G18) with specific guideline IDs cited | AID-006 |
| 9 | Progressive disclosure plan includes 5 stages with advancement criteria and rollback conditions | AID-007 |
| 10 | Stage 5 (Autonomy) requires explicit user opt-in and 30+ days at Stage 4 with error rate below threshold | AID-007a |
| 11 | ALL design recommendations (interaction pattern, feedback loop, progressive disclosure) are marked LOW confidence | AID-008 |
| 12 | Trust-risk and error-risk classifications are marked MEDIUM confidence (not HIGH) unless quantitative data supports | AID-008a |
| 13 | AI pattern staleness risk disclosure is present | AID-009 |
| 14 | REFERENCE-ONLY banner present in Feedback Loop Design section | AID-009a |
| 15 | Synthesis Judgments Summary lists every AI judgment call with confidence classification | AID-010 |
| 16 | Navigation table present with correct anchor links (H-23) | H-23 |
| 17 | Degraded mode disclosure present if operating without external tools | AID-009b |
| 18 | Handoff data sections populated for `/ux-inclusive-design` and `/ux-heuristic-eval` downstream consumption | OUT-006 |
| 19 | Trust-risk tie-breaker applied correctly (higher-risk classification when multiple rules fire) | AID-011a |
| 20 | Error-risk tie-breaker applied correctly (higher-risk classification when multiple rules fire) | AID-011b |
| 21 | AI Transparency Assessment covers all 5 PAIR pattern categories | AID-013 |

---

*Rule file: ai-first-design-rules.md*
*Version: 1.1.0*
*Parent sub-skill: /ux-ai-first-design*
*Parent skill: /user-experience*
*Agent: ux-ai-design-guide*
*SSOT: `skills/ux-ai-first-design/SKILL.md` (v1.1.0)*
*Created: 2026-03-04*

<!-- Traceability: PROJ-022 EPIC-005. Standards: H-23 (navigation), H-34 (agent-dev), H-13 (quality gate), SR-002 (input validation), SR-003 (output filtering). Methodology: Yang et al. (2020) DOI:10.1145/3313831.3376301, Amershi et al. (2019) DOI:10.1145/3290605.3300233, Shneiderman (2020) DOI:10.1080/10447318.2020.1741118, Google PAIR (2019) pair.withgoogle.com/guidebook. Synthesis validation: skills/user-experience/rules/synthesis-validation.md. Quality gate: .context/rules/quality-enforcement.md. ORCHESTRATION: projects/PROJ-022-user-experience-skill/orchestration/ux-skill-build-20260303-001/ORCHESTRATION.yaml -->
<!-- VERSION: 1.1.0 | DATE: 2026-03-04 | REVISION: iter2 — added AI Transparency Assessment Rules section (AID-013 through AID-013c), PAIR inline citation, template version fix, nav table update, cognitive mode note | SOURCE: skills/ux-ai-first-design/SKILL.md (v1.1.0), skills/ux-ai-first-design/agents/ux-ai-design-guide.md (v1.0.0), Yang et al. (2020) DOI:10.1145/3313831.3376301, Amershi et al. (2019) DOI:10.1145/3290605.3300233, Shneiderman (2020) DOI:10.1080/10447318.2020.1741118, Google PAIR (2019) -->
