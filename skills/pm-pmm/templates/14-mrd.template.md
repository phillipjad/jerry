---
title: "{{TITLE}}"
id: "PM-MS-{{NNN}}"
type: "mrd"
agent: "pm-market-strategist"
status: "draft"
mode: "{{discovery|delivery}}"
risk_domain: "business-viability-risk"
created: "{{YYYY-MM-DD}}"
last_validated: "{{YYYY-MM-DD}}"
frameworks_applied:
  - "Positioning Framework"
  - "Product-Market Fit Survey"
cross_refs:
  - "{{related_artifact_id}}"
---

# Market Requirements Document: {{Product/Market Name}}

## Document Sections

| Section | Purpose |
|---------|---------|
| [Market Overview](#market-overview) | Market opportunity and context |
| [Market Problems](#market-problems) | Problems the market needs solved |
| [Market Requirements](#market-requirements) | What the market demands |
| [Competitive Context](#competitive-context) | How competitors address these requirements |
| [Segment Prioritization](#segment-prioritization) | Which segments to target first |
| [Product-Market Fit Assessment](#product-market-fit-assessment) | PMF measurement and gaps |
| [Success Criteria](#success-criteria) | How to measure market success |
| [Assumptions and Risks](#assumptions-and-risks) | What must hold true |

---

## Market Overview

### Discovery Mode

**Market hypothesis:** {{One sentence describing the market opportunity}}

**Target market:** {{Market name and scope}}
**Market size:** {{TAM reference from PM-BA-NNN if available}}
**Growth rate:** {{N% CAGR}}
**Key trend:** {{Single most important market trend}}

**Confidence:** {{High/Medium/Low}}

### Delivery Mode

| Dimension | Detail |
|-----------|--------|
| **Market defined as** | {{Precise market definition}} |
| **Geographic scope** | {{Regions}} |
| **Market size** | {{$N TAM, $N SAM}} (reference: {{PM-BA-NNN}}) |
| **Growth rate** | {{N% CAGR over N years}} |
| **Maturity** | {{Emerging / Growing / Mature / Declining}} |
| **Key trends** | {{List 3-5 market trends}} |

---

## Market Problems

### Discovery Mode

| # | Problem | Who Has It | Severity | Alternatives Today |
|---|---------|-----------|----------|-------------------|
| 1 | {{problem}} | {{segment}} | {{Critical/High/Medium}} | {{current solution}} |
| 2 | {{problem}} | {{segment}} | {{severity}} | {{alternative}} |

### Delivery Mode

#### Problem 1: {{Problem Name}}

**Description:** {{2-3 sentences describing the market problem}}

**Who experiences this:** {{Segments, roles, company types}}

**Current solutions:** {{How the market currently addresses this}}

**Gaps in current solutions:** {{What is missing or inadequate}}

**Evidence:**
- {{Data point 1 with source}}
- {{Data point 2 with source}}

**Severity:** {{Critical / High / Medium / Low}}

---

## Market Requirements

### Delivery Mode

| MR-ID | Requirement | Problem Ref | Priority | Segment | Competitive Gap |
|-------|-------------|-------------|----------|---------|----------------|
| MR-001 | {{market requirement}} | {{Problem N}} | {{Must/Should/Could}} | {{segment}} | {{how competitors fall short}} |
| MR-002 | {{requirement}} | {{problem}} | {{priority}} | {{segment}} | {{gap}} |

### Requirement Categories

| Category | Requirements | Market Pressure |
|----------|-------------|----------------|
| **Table stakes** | {{What every solution must have}} | {{High -- buyers will not consider without these}} |
| **Differentiators** | {{What separates winners from losers}} | {{Medium -- buyers prefer but do not require}} |
| **Future bets** | {{What the market will demand in 12-24 months}} | {{Low now, high later}} |

---

## Competitive Context

| Requirement | Us | Competitor 1 | Competitor 2 | Market Gap |
|------------|-----|-------------|-------------|-----------|
| {{MR-001}} | {{Strong/Partial/Absent}} | {{rating}} | {{rating}} | {{unmet need}} |
| {{MR-002}} | {{rating}} | {{rating}} | {{rating}} | {{gap}} |

**Competitive reference:** See {{PM-CA-NNN}} for detailed competitive analysis.

---

## Segment Prioritization

| Segment | Market Size | Fit with MRs | Competitive Intensity | Priority |
|---------|-----------|-------------|----------------------|----------|
| {{segment 1}} | {{$N}} | {{Strong/Moderate/Weak}} | {{High/Medium/Low}} | Primary |
| {{segment 2}} | {{$N}} | {{fit}} | {{intensity}} | Secondary |

### Beachhead Segment (Delivery Mode)

*Framework: Crossing the Chasm (Moore)*

**Selected beachhead:** {{Segment name}}
**Why this segment first:** {{Evidence-based rationale}}
**Whole product requirements for this segment:** {{What is needed beyond core product}}
**Reference customer target:** {{N referenceable customers by date}}

---

## Product-Market Fit Assessment

*Framework: Product-Market Fit Survey (Ellis, Hacking Growth)*

### PMF Survey Design

**Core question:** "How would you feel if you could no longer use {{product}}?"
- Very disappointed
- Somewhat disappointed
- Not disappointed

**PMF threshold:** >= 40% "Very disappointed"

### Current PMF Status (if measurable)

| Metric | Current | Target | Status |
|--------|---------|--------|--------|
| "Very disappointed" % | {{N%}} | >= 40% | {{Above/Below}} |
| Sample size | {{N}} | >= 40 | {{Adequate/Insufficient}} |

### PMF Gap Analysis (Delivery Mode)

| Gap | Description | Required Action | Priority |
|-----|------------|----------------|----------|
| {{gap 1}} | {{what is missing for PMF}} | {{action}} | {{H/M/L}} |
| {{gap 2}} | {{description}} | {{action}} | {{priority}} |

---

## Success Criteria

| Metric | Target | Timeline | Measurement Method |
|--------|--------|----------|-------------------|
| {{Market share}} | {{N%}} | {{by date}} | {{how measured}} |
| {{Revenue from segment}} | {{$N}} | {{by date}} | {{how measured}} |
| {{PMF score}} | {{>= 40%}} | {{by date}} | {{survey}} |
| {{Customer count}} | {{N}} | {{by date}} | {{CRM}} |

---

## Assumptions and Risks

| # | Assumption | If Wrong | Likelihood | Mitigation |
|---|-----------|----------|-----------|------------|
| 1 | {{assumption}} | {{consequence}} | {{H/M/L}} | {{what we do}} |
| 2 | {{assumption}} | {{consequence}} | {{likelihood}} | {{mitigation}} |

---

*Template Version: 1.0.0 | Frameworks: Positioning, Product-Market Fit Survey, Crossing the Chasm | Agent: pm-market-strategist*
