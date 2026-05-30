---
avatar: avatar-internal-productivity
domain: Internal Tooling, Workflow Automation, Employee Experience (Non-Customer-Facing)
laws:
  - PRD-1.2
  - PRD-5.1
  - BUS-4.3
  - BUS-7.1
  - ENG-4.1
  - ENG-2.3
  - ENG-3.1
  - ENG-1.5
skills:
  - 28-content-transformation
  - 25-ux-design
  - 21-prompt-engineering
  - 06-atomic-tdd
  - 07-vertical-slice-dev
---

# Internal Productivity — Implementation Guidance

## Overview

Internal Productivity tools automate repetitive employee workflows, transform content to brand standards, and enable self-service for non-technical users in Finance, HR, and Operations. No customer PII is exposed; employee data is subject to BUS-4.3. The primary failure mode is **over-engineering**: teams request "AI-powered" suites before validating which specific workflow bottleneck drives the most lost hours.

---

## Core Journeys

| Journey | Persona | Success Metric |
|---------|---------|----------------|
| Content Transformation | Finance/Ops Analyst | Manual formatting time → 0 |
| Workflow Automation | Finance Analyst | Hours saved on target workflow |
| Self-Service Portal | HR Business Partner | Specialist call volume reduced |
| Brand Compliance Check | Any employee | Compliance pass rate on first submission |
| Template Generation | Operations Analyst | Report generation time ≤ 30 min |

**Key personas:** Operations Analyst, Finance Analyst, HR Business Partner, Brand Manager, IT Productivity Team.

---

## Non-Negotiable Laws

### BUS-4.3 — Employee Data Privacy
- No employee PII (salary, performance ratings, health data, HR case details) in application logs, training data, or audit exports.
- Transformation tools processing HR documents must redact PII before any AI processing step.
- Employee data retention in tool databases must follow AA HR data retention policy — not general app retention defaults.

### PRD-1.2 — Problem-First
- Validate hours-lost on the specific workflow **before** proposing automation.
- Research: time audits, error rate analysis, user interviews with ≥ 8 analysts across target workflows.
- "AI-powered expense categorization" is a solution. "Finance Analysts spend 40% of month-end close on 8,000+ uncategorized transactions" is a validated problem.

### PRD-5.1 — MVP: One Workflow First
- Start with the single highest-impact transformation or workflow.
- MVP = one workflow automated and measurably improved before building the second.
- Full self-service portals and real-time dashboards are roadmap items, not MVP scope.

### ENG-4.1 — Atomic TDD
- All transformation rules must have tests written before implementation.
- Brand compliance rules (color, font, layout) must be individually testable and passing before pipeline assembly.

### ENG-2.3 — Vertical Slice
- Deliver one transformation type at a time: colors → fonts → layouts. Never attempt all in a single slice.

### ENG-1.5 — API-First
- Expose transformation logic as API endpoints; this enables downstream automation and integration with Power Automate, SharePoint, etc.

---

## Key Patterns

- **Time audit before build:** Quantify hours-lost per workflow with a 2–6 week observation before any engineering sprint.
- **One workflow, one metric:** MVP succeeds or fails on a single time-reduction metric (e.g., 4 hours → 30 minutes for headcount report).
- **Employee data redaction before AI:** PII redaction is an input gate, not an output filter.
- **Transformation rules are tests first:** Every brand rule (e.g., "AA Red = #C8102E") has a passing unit test before the transformer is written.

---

## Anti-Patterns

- ❌ Building a general "AI productivity suite" without identifying which specific workflow consumes the most analyst time.
- ❌ Logging employee names, salaries, or HR case IDs in application debug logs.
- ❌ Treating brand compliance rules as implicit ("the AI will figure it out") — rules must be explicit, testable, and auditable.
- ❌ Multi-workflow rollout before the first workflow proves time savings at the stated target.
- ❌ Self-service portal with real-time dashboards as the MVP — validate the core transformation first.
