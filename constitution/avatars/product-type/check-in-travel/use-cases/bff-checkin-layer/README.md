# Use Case: BFF Check-In Layer Intelligence (mobile-fly-checkin-bff)

**Avatar:** avatar-check-in-travel  
**Laws:** PRD-4.1 (MVP), ENG-11.1 (SDD Gate), ENG-3.1 (Complexity)  
**Source:** mobile-fly-checkin-bff — Quality score 4.6/10 (Yellow tier)  
**Evidence date:** March 2026

## BFF Overview

`mobile-fly-checkin-bff` is the mobile check-in Backend-for-Frontend. It sits between the AA mobile app and the airline's check-in service. Quality score 4.6/10 — Yellow tier. Three confirmed bugs with product impact.

## Confirmed Bugs — Product Risk

### Bug 1 — CRITICAL: Year-Boundary Date Comparison (HIGH)
**File:** `FlifoAdapter.java` (L679–684)  
**Behavior:** Year-boundary check in `isIncomingFlightInfoOutsideTimeLimit()` compares day-of-year without accounting for year rollover. On December 31, a flight departing January 1 is calculated as "364 days ago" — outside the check-in window.  
**Product impact:** Check-in validation breaks for all Dec 31 → Jan 1 flights. Customers cannot complete mobile check-in for New Year's Eve flights.  
**Fix:** Use `ChronoUnit.HOURS.between(departure, now)` — no manual year arithmetic.

### Bug 2 — MEDIUM: God Method (177 lines)
**File:** `FlifoAdapter.mapFlifoResponse()` (177 LOC)  
**Behavior:** Monolithic method maps all FLIFO data into the mobile response. Any change risks regression across all 12+ FLIFO field mappings.  
**Product impact:** Every FLIFO-driven feature (gate display, delay notifications, on-time performance) depends on this method. Test coverage is low by design — method is too complex to test comprehensively.  
**Fix:** Decompose into focused mappers — `mapFlightStatus()`, `mapGateInfo()`, `mapTimingInfo()`. Each ≤ 30 LOC, independently testable.

### Bug 3 — MEDIUM: HTTP Calls Hidden in Getter-Named Methods
**File:** `FlifoAdapter` — multiple methods  
**Behavior:** Methods named `getFlightStatus()` and `getFlifoData()` perform HTTP calls. Callers have no indication of network I/O.  
**Product impact:** Timeout handling and error paths are not treated with appropriate care — callers don't know they need to handle network errors.  
**Fix:** Rename to `fetchFlightStatus()`, `callFlifo()`. Add explicit timeout handling.

## Roadmap Gate

Before any new check-in feature that touches `FlifoAdapter`:
1. Fix the year-boundary bug — it will affect every New Year's Eve deployment
2. File PROPOSAL.md per ENG-11.1 before modifying FlifoAdapter contracts
3. Add regression test for Dec 31 / Jan 1 boundary before the bug fix — test must fail first (ENG-4.1)
