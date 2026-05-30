---
domain: business
article: I
title: Foundational Principles
laws:
  - id: BUS-1.1
    title: Priority Hierarchy Law
    non_negotiable: true
    summary: All business and technical decisions MUST follow the priority hierarchy — Legal > Safety > Privacy > Security > Business Continuity > Efficiency
  - id: BUS-1.2
    title: Risk-Based Approach Law
    summary: All compliance and governance decisions SHALL be risk-based, proportionate to the likelihood and impact of harm
  - id: BUS-1.3
    title: Accountability Law
    summary: Every compliance obligation MUST have a named accountable owner with documented responsibilities
  - id: BUS-1.4
    title: Transparency Law
    summary: Compliance posture, known gaps, and risk decisions MUST be transparently documented and accessible to authorized stakeholders
  - id: BUS-1.5
    title: Continuous Improvement Law
    summary: Compliance and governance programs MUST be continuously improved based on audit findings, incidents, and regulatory changes
---

<!-- SPDX-FileCopyrightText: 2026 Click Chain AI -->
<!-- SPDX-License-Identifier: LicenseRef-ClickChain-Proprietary -->
# Article I: Foundational Principles

## Section 1.1: Legal and Regulatory Priority Hierarchy *(Non-Negotiable)*

**Law ID:** `BUS-1.1`

**All business and technical decisions MUST follow the priority hierarchy.** This hierarchy is non-negotiable and cannot be overridden by schedule, budget, or business pressure.

### Priority Order

| Priority | Domain | Description |
|----------|--------|---------|
| 1 | **Legal Compliance** | All applicable regulations and legal requirements |
| 2 | **Safety** | Passenger safety, operational safety, crew safety |
| 3 | **Privacy** | Customer data protection, data subject rights |
| 4 | **Security** | System security, data security, access control |
| 5 | **Business Continuity** | System availability, disaster recovery, resilience |
| 6 | **Efficiency** | Performance optimization, cost reduction, productivity |

### Non-Negotiable Requirements

1. **Conflict resolution** — When requirements conflict, higher-priority concerns always win; no exception without VP-level written approval documented in `hangar-ai-specs/`
2. **Legal review gate** — Any initiative touching regulated domains MUST receive legal review before production deployment
3. **Safety impact assessment** — Any change to systems in the safety-critical path MUST complete a safety impact assessment
4. **Prohibition** — Deploying features that violate legal compliance requirements to meet a schedule deadline is prohibited; schedule slips before compliance

### Decision Escalation Template
```markdown
## Business Obligation Priority Conflict Escalation
- **Conflict**: [describe the conflict between priorities]
- **Impacted priorities**: [e.g., Efficiency vs. Privacy]
- **Recommendation**: [Prioritize X because...]
- **Approver**: [VP or above for P1/P2 conflicts]
- **Date**: [YYYY-MM-DD]
```

---

## Section 1.2: Risk-Based Approach Law

**Law ID:** `BUS-1.2`

All compliance and governance decisions SHALL be risk-based, proportionate to the likelihood and impact of harm.

### Requirements

1. **Risk assessment** — All governance decisions are preceded by a risk assessment
2. **Proportionality** — Controls are proportionate to risk; over-control is waste, under-control is liability
3. **Risk register** — Material risks are tracked in a risk register (see BUS-6.1)

---

## Section 1.3: Accountability Law

**Law ID:** `BUS-1.3`

Every compliance obligation MUST have a named accountable owner with documented responsibilities.

### Requirements

1. **Named owner** — Every law in this domain has a designated accountable owner in the org
2. **RACI documented** — RACI matrix for compliance obligations maintained in `hangar-ai-specs/compliance/`
3. **Succession planning** — Backup owner identified for each critical compliance obligation

---

## Section 1.4: Transparency Law

**Law ID:** `BUS-1.4`

Compliance posture, known gaps, and risk decisions MUST be transparently documented and accessible to authorized stakeholders.

### Requirements

1. **Compliance dashboard** — Current compliance status visible to authorized stakeholders
2. **Gap documentation** — Known compliance gaps documented with remediation timelines
3. **Risk acceptance** — Accepted risks formally documented with owner, rationale, and review date

---

## Section 1.5: Continuous Improvement Law

**Law ID:** `BUS-1.5`

Compliance and governance programs MUST be continuously improved based on audit findings, incidents, and regulatory changes.

### Requirements

1. **Post-incident review** — Every compliance incident triggers a review of contributing controls
2. **Regulatory watch** — Regulatory changes monitored and assessed for impact within 30 days of publication
3. **Annual review** — Full compliance program review conducted annually with findings documented
