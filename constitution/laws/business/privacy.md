---
domain: business
article: IV
title: Privacy Laws
laws:
  - id: BUS-4.1
    title: Privacy by Design Law
    summary: Privacy MUST be embedded in all processing using the 7 PbD principles
  - id: BUS-4.2
    title: Consent Management Law
    summary: Consent MUST be freely given, specific, informed, and unambiguous
  - id: BUS-4.3
    title: Data Subject Rights Law
    non_negotiable: true
    summary: Individual rights MUST be respected (access, rectification, erasure, portability)
  - id: BUS-4.4
    title: Privacy Notice Law
    summary: Clear privacy notices MUST be provided explaining data collection and use
  - id: BUS-4.5
    title: Privacy Impact Assessment Law
    summary: PIAs MUST be conducted for high-risk processing
---

<!-- SPDX-FileCopyrightText: 2026 Click Chain AI -->
<!-- SPDX-License-Identifier: LicenseRef-ClickChain-Proprietary -->
# Article IV: Privacy Laws

## Section 4.1: Privacy by Design Law

**Law ID:** `BUS-4.1`

Privacy MUST be embedded in all processing.

### Seven Privacy by Design Principles

1. **Proactive not Reactive** - Prevent privacy issues
2. **Privacy as Default** - No action required for protection
3. **Privacy Embedded** - Built into design
4. **Full Functionality** - No privacy vs. function tradeoff
5. **End-to-End Security** - Lifecycle protection
6. **Visibility and Transparency** - Open practices
7. **Respect for Users** - User-centric design

---

## Section 4.2: Consent Management Law

**Law ID:** `BUS-4.2`

Consent MUST be freely given, specific, informed, and unambiguous.

### Consent Requirements

- Clear explanation of what user is consenting to
- Separate consent for different purposes
- Easy withdrawal mechanism
- Record of consent (what, when, how)
- No pre-checked boxes
- No bundling with terms of service

### Consent Record

```
Consent ID: [UUID]
User: [Identifier]
Purpose: [Specific purpose]
Collected: [Timestamp]
Method: [How collected - checkbox, signed, verbal]
Version: [Policy version at time of consent]
Withdrawn: [Timestamp if withdrawn, null otherwise]
```

---

## Right to Erasure for Customer Accounts

## Section 4.3: Data Subject Rights Law

**Law ID:** `BUS-4.3` | **Status:** NON-NEGOTIABLE

Individual rights over their personal data MUST be respected. All requests to access, delete, correct, or export personal data must be processed within regulatory timeframes.

### GDPR and CCPA Data Subject Rights

The following rights apply to all customers under GDPR (EU residents) and CCPA (California residents):

| Right | GDPR Article | Description | Response Time |
|-------|-------------|-------------|---------------|
| **Right to Access** | Art. 15 | Passenger right to know what personal data we hold | 30 days |
| **Right to Erasure / Right to be Forgotten** | Art. 17 | Delete passenger personal data upon request (unless legal retention applies) | 30 days |
| **Right to Rectification** | Art. 16 | Correct inaccurate personal data | 30 days |
| **Right to Portability** | Art. 20 | Export personal data in machine-readable format | 30 days |
| **Right to Restriction** | Art. 18 | Limit processing of personal data | 72 hours |
| **Right to Object** | Art. 21 | Stop certain processing of personal data | 72 hours |
| **No Automated Decisions** | Art. 22 | Human review of automated decisions affecting passengers | On request |

### CCPA-Specific Rights (California Residents)
- **Right to Know** — What personal information AA collects, uses, discloses, and sells
- **Right to Delete** — Request deletion of personal information AA has collected
- **Right to Opt-Out** — Opt out of sale or sharing of personal information
- **Right to Non-Discrimination** — Not be discriminated against for exercising privacy rights

### Deletion and Erasure Handling

When a customer requests deletion of their personal data:
1. **Verify identity** — Confirm the requestor's identity before processing
2. **Scope determination** — Identify all systems holding the customer's personal data (PNR, loyalty, CRM, email preferences)
3. **Legal retention check** — Apply retention exceptions: financial records (7 years per BUS-3.4), DOT complaint records (legal hold), safety records
4. **Execute deletion** — Delete all non-exempt data within 30 days
5. **Confirm to customer** — Written confirmation of deletion scope and exemptions applied

### Request Handling Process

1. Receive request (any channel — web form, email, contact center)
2. Verify identity
3. Log request in privacy request tracking system
4. Process within timeline
5. Respond to requestor
6. Document completion and legal basis for any exemptions

---

## Section 4.4: Privacy Notice Law

**Law ID:** `BUS-4.4`

Clear privacy notices MUST be provided.

### Notice Requirements

- Who we are (identity and contact)
- What data we collect
- Why we collect it (legal basis)
- How long we keep it
- Who we share it with
- User rights and how to exercise them
- How to complain
- Updates and notification process

---

## Section 4.5: Privacy Impact Assessment Law

**Law ID:** `BUS-4.5`

PIAs MUST be conducted for high-risk processing.

### PIA Triggers

- New processing of sensitive data
- Large-scale profiling
- Systematic monitoring
- New technology with privacy implications
- Cross-border data transfers

### PIA Template

```markdown
## Privacy Impact Assessment

**Project:** [Name]
**Date:** [YYYY-MM-DD]
**Assessor:** [Name]

### Processing Description
[What data, why, how]

### Necessity and Proportionality
[Why this processing is necessary and proportionate]

### Risk Assessment
| Risk | Likelihood | Impact | Mitigation | Residual Risk |
|------|------------|--------|------------|---------------|
| ... | ... | ... | ... | ... |

### Conclusion
[ ] Processing may proceed
[ ] Processing may proceed with mitigations
[ ] Processing should not proceed
[ ] Consult with supervisory authority

### Approval
[Signatures]
```
