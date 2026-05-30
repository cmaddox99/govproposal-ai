---
domain: engineering
article: VI
title: Security & Privacy Laws
laws:
  - id: ENG-6.1
    title: Security by Design Law
    non_negotiable: true
    summary: Security SHALL be built in, not bolted on
  - id: ENG-6.2
    title: Authentication Law
    summary: All systems SHALL implement proper authentication with MFA for privileged access
  - id: ENG-6.3
    title: Authorization Law
    summary: All access SHALL be controlled using principle of least privilege
  - id: ENG-6.4
    title: Data Protection Law
    non_negotiable: true
    summary: All sensitive data SHALL be protected at rest and in transit using industry-standard encryption
  - id: ENG-6.5
    title: Input Validation Law
    summary: ALL input SHALL be validated on the server using whitelist validation
  - id: ENG-6.6
    title: Vulnerability Management Law
    summary: Dependencies SHALL be managed with critical vulnerabilities fixed within 24 hours
  - id: ENG-6.7
    title: Audit Trail Law
    non_negotiable: true
    summary: All sensitive operations SHALL be logged with immutable audit records
  - id: ENG-6.8
    title: Privacy Law
    summary: Personal data SHALL be handled according to regulations with data minimization
---

<!-- SPDX-FileCopyrightText: 2026 Click Chain AI -->
<!-- SPDX-License-Identifier: LicenseRef-ClickChain-Proprietary -->
# Article VI: Security & Privacy Laws

## Security Requirements

## Security Requirements I Must Include in Every Feature

## Security Requirements for a Passenger

## MISRA Safety Critical

## Safety Critical Do 178C

## MISRA Safety Critical Do 178C

## Safety Critical

## Section 6.1: Security by Design Law

**Law ID:** `ENG-6.1` | **Status:** NON-NEGOTIABLE

Security SHALL be built in, not bolted on. Every feature MUST include security requirements as part of its acceptance criteria.

### Security Requirements for Every Feature

Every feature implementation must address these security requirements:
- **Input validation** — All inputs from untrusted sources must be validated and sanitized
- **Authentication and authorization** — All endpoints enforce appropriate auth; no anonymous access to sensitive data
- **Encryption** — Sensitive data encrypted at rest and in transit (TLS 1.2+, AES-256)
- **Injection prevention** — SQL injection, XSS, CSRF protections required
- **Error handling** — Errors must not expose sensitive information or stack traces
- **Dependency security** — No known critical CVEs in dependencies at deployment
- **Secrets management** — No credentials in code; vault/environment-based secrets required

### Implementation Checklist

## Threat Modeling

- [ ] Threat model documented before implementation
- [ ] Security requirements defined for each feature
- [ ] SAST tools integrated in CI pipeline
- [ ] DAST testing scheduled regularly
- [ ] Dependency scanning enabled

---

## Section 6.2: Authentication Law

**Law ID:** `ENG-6.2`

All systems SHALL implement proper authentication:

- Strong password policies (min 12 chars, complexity)
- Multi-factor authentication for privileged access
- Token-based authentication using industry-standard protocols
- Session management with proper expiration

### Avatar Guidance

See technology avatar for protocol selection guidance (e.g., OAuth2, OIDC, SAML).
- Account lockout after failed attempts

### Password Requirements

| Requirement | Minimum |
|-------------|---------|
| Length | 12 characters |
| Complexity | Upper, lower, number, special |
| History | Cannot reuse last 10 passwords |
| Expiration | 90 days for privileged, 180 days for standard |

---

## Section 6.3: Authorization Law

**Law ID:** `ENG-6.3`

All access SHALL be controlled:

- Principle of least privilege
- Role-based access control (RBAC) or Attribute-based (ABAC)
- Authorization checks on every request
- No security through obscurity
- Audit log of access decisions

---

## Section 6.4: Data Protection Law

**Law ID:** `ENG-6.4` | **Status:** NON-NEGOTIABLE

All sensitive data SHALL be protected.

### At Rest

- Encryption using current industry-standard symmetric ciphers (minimum 256-bit key length)
- Key management via HSM/KMS
- Keys rotated regularly

### In Transit

- Transport encryption using current industry-standard protocols at their latest stable versions
- Certificate pinning for mobile apps
- No HTTP in production (HTTPS only)

### Data Classification

| Level | Examples | Handling |
|-------|----------|----------|
| Public | Marketing content | Standard |
| Internal | Internal docs | Access control |
| Confidential | Customer data, PII | Encrypted + audit |
| Restricted | Credentials, keys | Encrypted + vault + MFA |

---

## Section 6.5: Input Validation Law

**Law ID:** `ENG-6.5`

ALL input SHALL be validated:

- Validate on the server (client validation is UX only)
- Whitelist validation (define what's allowed)
- Parameterized queries (no SQL injection)
- Output encoding (no XSS)
- Content-Type validation for uploads

### Validation Checklist

- [ ] Server-side validation for all inputs
- [ ] Parameterized queries for database access
- [ ] Output encoding for all dynamic content
- [ ] File upload validation (type, size, content)
- [ ] API rate limiting implemented

---

## Section 6.6: Vulnerability Management Law

**Law ID:** `ENG-6.6`

Dependencies SHALL be managed:

- Automated dependency scanning in CI
- Critical vulnerabilities fixed within 24 hours
- High vulnerabilities fixed within 7 days
- Regular updates to dependencies
- No dependencies with known critical CVEs

### Remediation SLAs

| Severity | SLA |
|----------|-----|
| Critical | 24 hours |
| High | 7 days |
| Medium | 30 days |
| Low | 90 days |

---

## FAR Part 117 Requirements

## FAR Part 117

## Link C++ Unit Tests to FAR Part 117

## C++ Unit Tests to FAR Part 117 Requirements

## Section 6.7: Audit Trail Law

## Correlation ID Tracing

**Law ID:** `ENG-6.7` | **Status:** NON-NEGOTIABLE

All sensitive operations SHALL be logged. Audit trails must be tamper-evident, immutable, and retained as required.

### Audit Record Structure

Every audit log entry MUST include these fields:
```
Audit Record:
├── Who (user ID, service account, IP address)
├── What (action type, resource type, resource ID)
├── When (timestamp with timezone, correlation ID, request ID)
├── Where (IP address, user agent, service name)
├── Result (success/failure, HTTP status, error code)
└── Context (before/after state for mutation operations)
```

### Correlation ID and Distributed Tracing

All services MUST:
- Propagate a **correlation ID** across service boundaries (X-Correlation-ID header)
- Include correlation ID in every audit log entry for end-to-end request tracing
- Implement OpenTelemetry trace ID as the standard correlation identifier
- Log both `trace_id` and `span_id` in structured log output

### Requirements

- Audit logs are IMMUTABLE — no UPDATE or DELETE operations allowed on audit records
- Minimum retention: 1 year online, 7 years archived (per BUS-7.1)
- Tamper-evident with cryptographic hashing (append-only storage, hash chain)
- Centralized log aggregation in SIEM

---

## Section 6.8: Privacy Law

**Law ID:** `ENG-6.8`

Personal data SHALL be handled according to regulations:

- Data minimization (collect only what's needed)
- Purpose limitation (use only for stated purpose)
- Consent management where required
- Right to access, rectification, deletion
- Data retention policies enforced
- Privacy by design and default

### Privacy Checklist

- [ ] Data inventory maintained
- [ ] Consent mechanism implemented
- [ ] Data subject request process defined
- [ ] Retention policies automated
- [ ] Privacy impact assessment for new features
