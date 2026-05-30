---
law: BUS-2.1
avatar: avatar-product-travel-docs-compliance
title: "Regulatory Mapping — TIMATIC, APIS, and Health Documentation"
---

# BUS-2.1 Regulatory Mapping — Travel Docs Compliance

## Context

International travel document compliance is governed by multiple overlapping regulatory
frameworks. IATA TIMATIC provides the authoritative rule set for passport, visa, and
entry requirements per origin-destination pair. APIS is a pre-departure legal obligation
for international flights. Health documentation rules are route-specific and change frequently.

---

## ✅ COMPLIANT Example

### TIMATIC Integration Pattern

```
TravelDocsRequirement (BFF orchestrator)
  └── TravelDocsStatusRequestBuilder.buildRequest(pnr, segments)
        └── TIMATIC4 API call → parse rules per segment
              └── DocsStatusEnum: SUFFICIENT / INSUFFICIENT / NOT_APPLICABLE
```

**Key file:** `bff/mobile-fly-checkin-bff/src/.../traveldocs/traveldocsorchestrator/TravelDocsRequirement.java`

**Rule:** TIMATIC check is mandatory for every international itinerary before check-in is allowed.
Cache TTL must be ≤30 minutes; ≤5 minutes during active departure windows (D-2 hours).

### APIS Submission Pattern

| Step | Actor | Obligation |
|------|-------|-----------|
| Passenger data verified | PassportFlowManager (iOS) | MRZ + NFC scan → name, nationality, passport number/expiry |
| APIS record assembled | BFF traveldocs orchestrator | Formatted per CBP schema via TravelDocsStatusRequest |
| APIS transmitted | Sabre Web Services | Pre-departure; transmission timestamp recorded in audit trail |
| Rejection handled | BFF + agent console | Reason code returned; agent notified before gate close |

**Non-negotiable:** APIS submission must never be skipped for performance or latency reasons.
A missing APIS record is a regulatory violation, not a feature trade-off.

### Health Documentation Rules

Health documentation requirements are sourced from Sherpa and are **route-specific**:
- `HealthDocsStatusRequestBuilder.java` builds the health check request per itinerary segment
- `HealthDocsStatusResponse.java` / `SliceHealthDocsResponse.java` carry per-slice verdicts
- `WellnessRequest.java` handles wellness attestation flow

**Update cadence:** Health rules must propagate within 24 hours of upstream Sherpa/CDC update.

---

## ❌ NON-COMPLIANT

> "Skip TIMATIC check for domestic-to-international connections to save latency."

**Violation:** TIMATIC is mandatory for all international segments regardless of connection type.
Skipping TIMATIC exposes AA to regulatory penalties and denied-boarding liability.

> "Cache APIS record and re-use for 24 hours to reduce Sabre calls."

**Violation:** APIS must reflect verified, current passenger document data.
Stale APIS records result in CBP submission errors and potential denied departure.
