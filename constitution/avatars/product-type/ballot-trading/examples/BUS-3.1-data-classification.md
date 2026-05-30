---
avatar: avatar-product-ballot-trading
law: BUS-3.1
title: "Data Classification"
---

# BUS-3.1 — Data Classification: Ballot Trading Application

## What This Law Requires

All pilot scheduling, trade, and contract data must be classified according to sensitivity level, with access controls, retention policies, and handling procedures defined before any system stores or transmits that data.

## Compliant Example

**Data Classification Register (Ballot Trading)**

| Data Element | Classification | Storage | Access Control | Retention |
|---|---|---|---|---|
| Pilot employee ID | Confidential | CCA DB (encrypted at rest) | CBA Compliance Analyst, CCA system only | 7 years |
| Flight pairing assignment | Confidential | CCA DB | Pilot (own record), Crew Scheduler | Active + 2 years |
| Trade request history | Confidential | PTTS audit store | Pilot (own), CBA Analyst, Scheduler | 7 years |
| CBA eligibility decision + reason | Confidential | BUS-7.1 audit log | CBA Analyst, read-only | 7 years |
| Seniority ranking | Restricted | CCA DB (encrypted) | CCA system, Crew Scheduler | Duration of employment + 2 years |
| Reserve availability window | Confidential | dotc_ras_cache (TTL-bounded) | Pilot (own), Dispatcher | Active window only |
| Aggregate match statistics | Internal | Analytics store | Product team, no PII | 3 years |

**Handling Rules**
```
Confidential data:
  - Encrypted at rest (AES-256) and in transit (TLS 1.2+)
  - Access logged in observability layer
  - Pilot ID masked in logs, metrics, and observability (last-4 only)
  - No Confidential data in exception messages or stack traces

Restricted data (seniority):
  - Read access: CCA system service account only
  - No direct query access from application code outside CCA
  - Separate encryption key from general Confidential data
```

## Violation Example

```
❌ VIOLATION: Pilot ID logged in plain text in observability
   logger.info("Processing trade for pilot: " + pilot.getEmployeeId()
               + ", pairing: " + pairingId);

   Employee ID (Confidential) in log stream.
   Log stream accessible to broader engineering team.
   BUS-3.1 violation: Confidential data handled without access control.
   Potential CCPA / privacy obligation breach depending on jurisdiction.
```

## Edge Cases & Warnings

- **Cache data classification** — `dotc_ras_cache` holds reserve availability; classify as Confidential even though it is Redis-backed. TTL does not substitute for a retention policy.
- **Analytics pipelines must strip PII before storage** — `ptts_purge_adf` post-processing must anonymize pilot IDs before writing to analytics store. No pilot-identifiable data in aggregate dashboards.
- **Cross-region data transfer** — if east/west Apigee routing moves pilot data across regions, evaluate BUS-3.5 (Cross-Border Data Transfer) for applicable jurisdictions.
