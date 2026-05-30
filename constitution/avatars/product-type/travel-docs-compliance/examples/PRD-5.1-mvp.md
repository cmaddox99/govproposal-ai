---
law: PRD-5.1
avatar: avatar-product-travel-docs-compliance
title: "MVP: Pre-Departure Check for Top-3 Document Error Types"
---

# PRD-5.1 MVP Law — Travel Docs Compliance

## Law Summary

Address the highest-impact, most-automatable document error types first. Do not attempt full document suite automation before proving the top-3 error type hypothesis.

---

## ✅ COMPLIANT Example — MVP Canvas

### Hypothesis

> Implementing automated pre-departure readiness checks for the top-3 false-block document error types (future-dated passport expiry, visa-on-arrival eligibility, minor name mismatch) will reduce the overall false-block rate from 1.8% to ≤ 0.9%, saving ~170 gate agent interventions per day.

### Riskiest Assumption

The top-3 error types are automatable with deterministic rules (no edge-case judgment required). Specifically: that "minor name mismatch" can be defined by a consistent rule (e.g., nickname/middle name presence/absence) rather than requiring gate agent judgment on every case.

### Why Top-3 Error Types First

Root cause analysis of 90-day false-block data identified concentration:

| Error Type | % of False Blocks | Automatable? |
|-----------|------------------|--------------|
| Expired passport (but valid for all trip dates) | 41% | Yes — rule: passport expiry > return date |
| Missing visa (but destination is visa-on-arrival eligible) | 33% | Yes — rule: match destination to TIMATIC VOA list |
| Name mismatch (nickname vs. legal name per TSA PreCheck) | 18% | Yes — rule: name in TSA PreCheck record = legal name |
| Other (document type, condition, etc.) | 8% | Requires judgment — deferred |

Top-3 cover 92% of false blocks and are rule-based. The remaining 8% require case-by-case judgment and are deferred.

### MVP Scope

**In scope:**
- Automated pre-departure document readiness check for 3 error types listed above
- Check runs at T−24 hours and T−4 hours before departure
- Scope: all AA-operated domestic and international flights
- Alert if check fails: notify passenger via email/push (not gate agent) with specific document requirement
- Gate agent receives resolved/unresolved status at check-in, not raw document data

**Out of scope:**
- All other document types (military IDs, refugee travel documents, complex visa types)
- Real-time APIS (Advance Passenger Information System) integration
- Mobile app document upload or verification
- Automated boarding denial (gate agent retains final authority)
- Codeshare partners (TIMATIC data may differ)

### Acceptance Criteria

```gherkin
Scenario: Passport valid for all trip dates is pre-cleared
  Given a passenger's passport expires on 2026-12-15
  And the passenger's return date is 2026-11-30
  When the pre-departure document check runs at T−24 hours
  Then the passenger is flagged as "passport valid for trip dates"
  And the gate agent sees "Passport: Pre-Cleared" status at check-in
  And no gate agent intervention is required for this check type

Scenario: Visa-on-arrival eligible destination is pre-cleared
  Given the passenger is traveling to Japan
  And the passenger holds a valid US passport
  And Japan is on the TIMATIC visa-on-arrival eligible list for US passport holders
  When the pre-departure document check runs
  Then the passenger is flagged as "visa-on-arrival eligible: Japan"
  And no "missing visa" block is generated
```

### Success Criteria (60-Day Pilot)

| Metric | Baseline | Target | Fail Gate |
|--------|----------|--------|-----------|
| Overall false-block rate | 1.8% | ≤ 0.9% | > 1.4% → investigate rule accuracy |
| False blocks from top-3 error types | ~331/day | ≤ 50/day | > 150/day → review TIMATIC data freshness |
| Gate agent interventions caused by false blocks | ~340/day | ≤ 170/day | > 280/day → investigate check coverage |
| Genuine non-compliance block rate | 0.3% | ≥ 0.3% (must not decrease) | < 0.2% → review false negative risk |
| Passenger false-block complaint rate | ~12/day | ≤ 6/day | > 10/day → investigate passenger notification clarity |

### Expansion Gate

Additional document types and APIS integration considered only after: 60-day pilot shows false-block rate ≤ 0.9% AND genuine non-compliance block rate unchanged.

---

## ❌ VIOLATION Example

> "Build full automated document verification for all document types, all destinations, with real-time APIS integration and mobile document upload."

**Why this violates PRD-5.1:**
- Full document type coverage before proving top-3 error types are automatable.
- Real-time APIS integration adds regulatory compliance scope (DHS, CBP requirements) — separate project.
- Mobile document upload introduces identity verification and fraud risk — separate product track.
- If the name-mismatch rule is wrong, full suite deployment would increase false blocks network-wide simultaneously.
- Correct approach: top-3 error types, 60-day pilot, prove false-block rate halved. Then extend.
