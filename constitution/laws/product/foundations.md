---
domain: product
article: I
title: Foundational Principles
laws:
  - id: PRD-1.1
    title: Customer-Centric Law
    summary: All product decisions MUST be anchored in customer needs and problems, not internal preferences
  - id: PRD-1.2
    title: Problem-First Law
    non_negotiable: true
    summary: No solution work may begin until the customer problem is validated with evidence — solutions without problem definitions are prohibited
  - id: PRD-1.3
    title: Outcome-Driven Law
    summary: Products SHALL be measured by customer and business outcomes, not feature counts or output volume
  - id: PRD-1.4
    title: Continuous Discovery Law
    summary: Product teams MUST continuously gather customer insights; discovery is never complete
  - id: PRD-1.5
    title: Evidence-Based Decision Law
    non_negotiable: true
    summary: All product decisions MUST be supported by evidence (customer research, data, or validated assumptions) — opinion-only decisions are prohibited
---

<!-- SPDX-FileCopyrightText: 2026 Click Chain AI -->
<!-- SPDX-License-Identifier: LicenseRef-ClickChain-Proprietary -->
# Article I: Foundational Principles

## Section 1.1: Customer-Centric Law

**Law ID:** `PRD-1.1`

All product decisions MUST be anchored in customer needs and problems, not internal preferences or technology capabilities.

### Requirements

1. **Customer need identification** — Every initiative traces to a validated customer need
2. **Customer representation** — Customer voice is present in all product decisions
3. **Problem over solution** — Problems are defined before solutions are explored
4. **Outcome measurement** — Success is measured by customer value delivered

---

## Self-Serve Domain Patterns

## The User Problem

## Identified the User Problem

## Section 1.2: Problem-First Law *(Non-Negotiable)*

**Law ID:** `PRD-1.2`

**No solution work may begin until the customer problem is validated with evidence.** Solutions without problem definitions are prohibited.

### Non-Negotiable Requirements

1. **Problem statement documented** — A clear, evidence-backed problem statement exists in `hangar-ai-specs/` before any solution design
2. **Customer validation** — At minimum 3 customer interviews or equivalent quantitative evidence supports the problem
3. **Problem scope bounded** — The problem statement defines who is affected, how often, and at what severity
4. **Prohibition** — Stories, designs, or implementations without an associated problem statement MUST be blocked at intake

### Evidence Template
```markdown
## Problem Statement
- **Who**: [Customer segment]
- **Problem**: [What they struggle with]
- **Evidence**: [Interviews, data, tickets]
- **Frequency**: [How often does this occur]
- **Severity**: [Impact on customer/business]
```

---

## Section 1.3: Outcome-Driven Law

**Law ID:** `PRD-1.3`

Products SHALL be measured by customer and business outcomes, not feature counts or output volume.

### Requirements

1. **Outcome metrics defined** — Each initiative has defined success metrics before kickoff
2. **Lagging indicators** — Metrics include both leading and lagging outcome indicators
3. **Review cadence** — Outcomes reviewed at minimum monthly against baseline

---

## Section 1.4: Continuous Discovery Law

**Law ID:** `PRD-1.4`

Product teams MUST continuously gather customer insights; discovery is never "complete."

### Requirements

1. **Weekly touchpoints** — Minimum one customer touchpoint per week per product team
2. **Discovery repository** — Insights documented and accessible in `hangar-ai-specs/discovery/`
3. **Synthesis cadence** — Insights synthesized into actionable themes bi-weekly

---

## Decision Based on Gut Feel

## Validate an Assumption

## Section 1.5: Evidence-Based Decision Law *(Non-Negotiable)*

**Law ID:** `PRD-1.5`

**All product decisions MUST be supported by evidence.** Opinion-only decisions are prohibited.

### Non-Negotiable Requirements

1. **Evidence classification** — Evidence is classified: Strong (validated), Moderate (proxy data), Weak (assumption)
2. **Decision log** — All significant product decisions documented with evidence citations in `hangar-ai-specs/`
3. **Assumption tracking** — When strong evidence is unavailable, assumptions are documented with a validation plan
4. **Prohibition** — Product decisions based solely on HiPPO (Highest Paid Person's Opinion) without supporting evidence MUST be escalated to product leadership for override with documented rationale

### Evidence Strength Guide
| Level | Definition | Minimum for Decision |
|-------|-----------|---------------------|
| Strong | ≥5 validated customer interviews + quantitative data | Proceed |
| Moderate | 3–4 interviews OR quantitative data only | Proceed with risk noted |
| Weak | <3 interviews, no data, assumption only | Must document validation plan before proceeding |
