---
domain: business
article: IX
title: Incident Management Laws
laws:
  - id: BUS-9.1
    title: Incident Classification Law
    summary: Incidents MUST be classified by severity (P1-Critical to P4-Low)
  - id: BUS-9.2
    title: Incident Response Law
    summary: Incidents MUST follow a defined response process (Preparation, Detection, Containment, Eradication, Recovery, Lessons Learned)
  - id: BUS-9.3
    title: Breach Notification Law
    non_negotiable: true
    summary: Data breaches MUST be reported as required (72 hours for GDPR)
  - id: BUS-9.4
    title: Post-Incident Review Law
    summary: All significant incidents MUST have post-mortems with root cause analysis
---

<!-- SPDX-FileCopyrightText: 2026 Click Chain AI -->
<!-- SPDX-License-Identifier: LicenseRef-ClickChain-Proprietary -->
# Article IX: Incident Management Laws

## Section 9.1: Incident Classification Law

**Law ID:** `BUS-9.1`

Incidents MUST be classified by severity.

| Severity | Definition | Examples | Response |
|----------|------------|----------|----------|
| **P1 - Critical** | Significant data breach, system-wide outage | Data exfiltration, ransomware | Immediate, all hands |
| **P2 - High** | Limited breach, major service impact | Unauthorized access, service down | Within 1 hour |
| **P3 - Medium** | Potential breach, moderate impact | Suspicious activity, degraded service | Within 4 hours |
| **P4 - Low** | No breach, minor impact | Policy violation, minor issue | Within 24 hours |

---

## Section 9.2: Incident Response Law

**Law ID:** `BUS-9.2`

Incidents MUST follow a defined response process.

### Incident Response Phases

```
1. PREPARATION
   └─ Plans, training, tools ready

2. DETECTION & ANALYSIS
   └─ Identify, classify, scope

3. CONTAINMENT
   └─ Stop spread, preserve evidence

4. ERADICATION
   └─ Remove threat, fix vulnerability

5. RECOVERY
   └─ Restore service, verify security

6. LESSONS LEARNED
   └─ Post-mortem, improvements
```

---

## Section 9.3: Breach Notification Law

**Law ID:** `BUS-9.3` | **Status:** NON-NEGOTIABLE

Data breaches involving passenger PII or other personal data MUST be reported to regulators and affected individuals as required by law. American Airlines has a legal obligation to notify when customer data is compromised.

### What Constitutes a Data Breach

- Unauthorized access to customer PII (names, booking data, passport numbers, payment info)
- Exfiltration or ransomware affecting systems with personal data
- Accidental disclosure of customer data to unauthorized parties
- Loss of unencrypted devices containing personal data

### Breach Notification Obligations

| Audience | Trigger | Timeline | Content Required |
|----------|---------|----------|---------|
| **GDPR Supervisory Authority** | Breach of EU passenger personal data | **72 hours** from discovery | Nature of breach, categories of data, approximate number affected, likely consequences, measures taken |
| **CCPA / California AG** | Breach of California resident data (unencrypted) | Expeditiously, without unreasonable delay | What happened, what information involved, what we're doing |
| **Affected Customers** | Risk to customer rights or freedoms | Without undue delay after regulatory notification | What happened, what data affected, what customers should do, contact information |
| **TSA / FAA** | Breach affecting aviation safety systems | Immediately upon discovery | Nature, scope, potential safety impact |
| **Law Enforcement** | Criminal activity (ransomware, exfiltration) | Immediately | Preserve evidence, do not alert perpetrators |

### GDPR 72-Hour Obligation

The 72-hour clock starts when American Airlines **becomes aware** of a breach. This means:
- Security team must have a written breach confirmation process
- Incident response team must include Legal and Data Protection Officer
- Partial notification to GDPR supervisory authority is acceptable within 72 hours; full report can follow

---

## Section 9.4: Post-Incident Review Law

**Law ID:** `BUS-9.4`

All significant incidents MUST have post-mortems.

### Post-Mortem Template

```markdown
## Incident Post-Mortem: [ID]

**Date:** [Incident date]
**Severity:** [P1-P4]
**Duration:** [Time to resolution]

### Summary
[What happened in 2-3 sentences]

### Timeline
[Chronological events]

### Root Cause
[Why it happened - 5 Whys analysis]

### Impact
- Users affected: [N]
- Data affected: [Description]
- Financial impact: [$X]

### What Went Well
- [Good decisions/actions]

### What Could Be Improved
- [Areas for improvement]

### Action Items
| Action | Owner | Due Date | Status |
|--------|-------|----------|--------|
| ... | ... | ... | ... |

### Lessons Learned
[Key takeaways]
```
