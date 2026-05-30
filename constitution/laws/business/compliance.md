---
domain: business
article: II
title: Compliance Framework Laws
laws:
  - id: BUS-2.1
    title: FAA Compliance Law
    non_negotiable: true
    summary: All software systems must comply with applicable FAA regulations including FAR Part 25, FAR Part 117 (crew duty limits), and DO-178C for avionics-adjacent software
  - id: BUS-2.2
    title: Control Framework Law
    non_negotiable: true
    summary: Controls MUST be documented and mapped to requirements
  - id: BUS-2.3
    title: DOT Consumer Protection Law
    non_negotiable: true
    summary: All customer-facing products must comply with DOT consumer protection regulations including refund obligations, fare transparency, denied boarding compensation, and accessibility requirements
  - id: BUS-2.4
    title: Evidence Collection Law
    summary: Compliance evidence MUST be collected and retained
---

<!-- SPDX-FileCopyrightText: 2026 Click Chain AI -->
<!-- SPDX-License-Identifier: LicenseRef-ClickChain-Proprietary -->
# Article II: Compliance Framework Laws

## FAA and Aviation Regulatory Requirements

## Applicable FAA and Aviation Regulatory Requirements

## All Applicable FAA and Aviation Regulatory Requirements

## Section 2.1: FAA Compliance Law

**Law ID:** `BUS-2.1`

All software systems MUST comply with applicable FAA regulations. Aviation-adjacent systems must be developed per FAA requirements.

### Key FAA Regulatory Requirements

- **FAR Part 117** — Crew duty limits and rest requirements; scheduling systems must enforce these limits
- **DO-178C** — Software development assurance for avionics software; safety-critical systems require design assurance level review
- **FAR Part 25** — Airworthiness standards; passenger-facing systems affecting safety must comply
- **FAR Part 121** — Air carrier operations; systems supporting operations must be FAA-compliant
- **FAR Part 139** — Airport certification; airport-facing systems must support FAA audit requirements

### Compliance Requirements

All regulatory mappings must be maintained in `hangar-ai-specs/compliance/`.

### Regulatory Mapping Template

| Regulation | Jurisdiction | Applicability | Key Requirements | Owner | Status |
|------------|--------------|---------------|------------------|-------|--------|
| GDPR | EU/EEA | Customer data | Consent, rights, DPA | Legal | Active |
| CCPA | California | CA residents | Disclosure, opt-out | Legal | Active |
| HIPAA | USA | PHI handling | Privacy, security rules | Security | Active |
| SOC 2 | N/A | Customer trust | Trust principles | Security | Active |
| PCI-DSS | Global | Card data | 12 requirements | Security | Active |

---

## Section 2.2: Control Framework Law

**Law ID:** `BUS-2.2`

Controls MUST be documented and mapped to requirements.

### Control Categories

| Type | Description | Examples |
|------|-------------|----------|
| **Preventive** | Stop violations before they occur | Access controls, validation |
| **Detective** | Identify violations that occurred | Monitoring, audits, alerts |
| **Corrective** | Fix issues after detection | Incident response, patches |
| **Deterrent** | Discourage violations | Policies, training, consequences |

### Control Documentation Template

```markdown
## Control: [ID] - [Name]

**Type:** [ ] Preventive [ ] Detective [ ] Corrective [ ] Deterrent

**Description:** [What the control does]

**Implementation:** [How it's implemented]

**Regulations Addressed:**
- [Regulation 1] - [Specific requirement]
- [Regulation 2] - [Specific requirement]

**Testing:**
- Frequency: [How often tested]
- Method: [How tested]
- Last Test: [Date]
- Result: [Pass/Fail]

**Owner:** [Team/Person]
```

---

## DOT Refund Requirements

## DOT Refund Requirements When a Flight Is Cancelled

## Refund Requirements When a Flight Is Cancelled

## When a Flight Is Cancelled

## Section 2.3: DOT Consumer Protection Law

**Law ID:** `BUS-2.3`

All customer-facing products MUST comply with DOT consumer protection regulations.

### Key DOT Requirements

- **Refund obligations** — Full refund required within 7 business days (credit card) or 20 days (other) when AA cancels or significantly changes a flight
- **Fare transparency** — Total price including all taxes and fees MUST be displayed before purchase; drip pricing prohibited
- **Denied boarding compensation** — IDB (Involuntary Denied Boarding) compensation rates per 14 CFR Part 250
- **VDB (Voluntary Denied Boarding)** — Gate agents must solicit volunteers before IDB; compensation limits per regulation
- **Accessibility** — 14 CFR Part 382 disability accommodation requirements apply to all booking flows
- **Tarmac delay rule** — Maximum tarmac delays and passenger rights per 14 CFR Part 244

### Monitoring Requirements

- Automated refund SLA monitoring; alert at 5 days for credit card, 15 days for other payment
- Fare transparency validation in all booking flows before launch
- DOT complaint tracking and 30-day response window compliance

### Compliance Status Levels

| Status | Definition | Action Required |
|--------|------------|-----------------|
| 🟢 Compliant | All controls operating effectively | Maintain |
| 🟡 At Risk | Minor gaps, remediation in progress | Track closely |
| 🔴 Non-Compliant | Significant gaps or failures | Immediate remediation |
| ⚪ Not Assessed | Not yet evaluated | Schedule assessment |

---

## Section 2.4: Evidence Collection Law

**Law ID:** `BUS-2.4`

Compliance evidence MUST be collected and retained.

### Evidence Types

- Policy documents (versioned)
- Procedure documentation
- Training records
- Access reviews
- Audit logs
- Test results
- Exception approvals
- Incident reports

### Retention Requirements

- Minimum 3 years for most compliance evidence
- 7 years for financial/SOX-related
- Industry-specific requirements may extend
