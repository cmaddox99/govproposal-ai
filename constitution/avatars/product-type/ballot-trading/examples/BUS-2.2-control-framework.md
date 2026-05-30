---
avatar: avatar-product-ballot-trading
law: BUS-2.2
title: "Control Framework"
---

# BUS-2.2 — Control Framework: Ballot Trading Application

## What This Law Requires

The Collective Bargaining Agreement (CBA) is the documented control framework. Every eligibility determination must trace bidirectionally to a specific CBA article and produce an audit record.

## Compliant Example

**CBA Control Mapping Table (excerpt)**

| Control ID | CBA Article | Rule Description | System Enforcing | Evidence |
|---|---|---|---|---|
| CTL-001 | Art. 12.3 | Max monthly flight hours: 80 | CCA rules engine | BUS-7.1 audit record |
| CTL-002 | Art. 14.1 | Minimum rest between pairings: 10h | CCA rules engine | BUS-7.1 audit record |
| CTL-003 | Art. 20.2 | Seniority-ordered trade award priority | PTTS/BTS matching | BUS-7.1 audit record |
| CTL-004 | Art. 22.4 | Overtime limit before trade disqualification | pilottts_otlimitservice | BUS-7.1 audit record |
| CTL-005 | Art. 8.5 | Reserve pilot availability window constraints | DOTC/RAS | BUS-7.1 audit record |

**Traceability Chain**
```
CBA Article (Art. 12.3)
  → CCA Rule (RULE-DT-001: monthly_flight_hours ≤ 80)
    → CCA API eligibility check
      → Trade decision (REJECTED / APPROVED)
        → BUS-7.1 audit record (cba_article: "Art. 12.3")
```

**Control Validation Cadence**
- CBA updates: re-map all affected controls within 30 days of new CBA ratification
- CCA rules engine: every deployed rule must have a corresponding CTL entry
- Annual control review: CBA Compliance Analyst reviews CTL table against current CBA

## Violation Example

```
❌ VIOLATION: Hardcoded threshold without CBA citation
   // In CCA rules engine:
   if (monthlyFlightHours > 80) return INELIGIBLE;
   // No CBA article reference, no control mapping entry

   When CBA is renegotiated and limit changes to 85 hours:
   - No traceability to find and update this rule
   - Pilot wrongly rejected; CBA dispute cannot be defended
   - BUS-2.2: control not mapped to requirement = audit failure
```

## Edge Cases & Warnings

- **CBA amendments require immediate control table updates** — a stale CTL entry that cites a superseded article is a compliance violation.
- **Compound rules need separate control entries** — if trade eligibility depends on both duty-time AND overtime limit, create one CTL entry per CBA article, not a single combined entry.
- **Override controls are controls too** — scheduler override capability must have its own CTL entry citing the CBA provision that permits manual overrides.
