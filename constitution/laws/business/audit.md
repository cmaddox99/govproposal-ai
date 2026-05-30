---
domain: business
article: VII
title: Audit & Evidence Laws
laws:
  - id: BUS-7.1
    title: Audit Trail Law
    non_negotiable: true
    summary: All significant actions MUST be logged with immutable, tamper-evident records
  - id: BUS-7.2
    title: Evidence Integrity Law
    summary: Audit evidence MUST be trustworthy with cryptographic hashing
  - id: BUS-7.3
    title: Audit Readiness Law
    summary: Organizations MUST be ready for audits with current documentation
  - id: BUS-7.4
    title: Internal Audit Law
    summary: Regular internal audits SHALL be conducted with findings tracked to remediation
---

<!-- SPDX-FileCopyrightText: 2026 Click Chain AI -->
<!-- SPDX-License-Identifier: LicenseRef-ClickChain-Proprietary -->
# Article VII: Audit & Evidence Laws

## Section 7.1: Audit Trail Law

**Law ID:** `BUS-7.1` | **Status:** NON-NEGOTIABLE

All significant actions MUST be logged.

### Audit Log Requirements

- **Who** (authenticated user/service)
- **What** (action performed)
- **When** (timestamp with timezone)
- **Where** (system, IP address)
- **Why** (business context if available)
- **Outcome** (success/failure)

### Log Retention

- Minimum 1 year online
- Minimum 7 years archived
- Immutable (append-only)
- Tamper-evident

---

## Section 7.2: Evidence Integrity Law

**Law ID:** `BUS-7.2`

Audit evidence MUST be trustworthy.

### Integrity Requirements

- Cryptographic hashing of log entries
- Secure log transmission (TLS)
- Restricted access to log systems
- Segregation of log administrators
- Regular integrity verification

---

## Section 7.3: Audit Readiness Law

**Law ID:** `BUS-7.3`

Organizations MUST be ready for audits.

### Audit Readiness Checklist

- [ ] Control documentation current
- [ ] Evidence collection automated
- [ ] Previous findings remediated
- [ ] Key personnel identified and available
- [ ] Access for auditors prepared
- [ ] Timeline and scope understood

---

## Section 7.4: Internal Audit Law

**Law ID:** `BUS-7.4`

Regular internal audits SHALL be conducted.

### Internal Audit Program

- Annual audit plan approved by leadership
- Risk-based prioritization
- Independent audit function
- Findings tracked to remediation
- Results reported to audit committee/board
