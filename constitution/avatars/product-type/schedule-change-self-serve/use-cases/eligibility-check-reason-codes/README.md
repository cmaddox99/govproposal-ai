# Use Case: Eligibility Check and Reason Code Display

**Avatar:** schedule-change-self-serve  
**Law:** PRD-2.1 User Journey Mapping, PRD-4.1 MVP, BUS-2.1 Regulatory Mapping  
**Slice:** 1 — Eligibility Transparency  
**Grounded in:** `bff/mobile-change-bff` — `ChangeTripController.java`, `ReshopEligibilityBuilder.java`, `ReshopEligibilityResponse.java`, `RuleResult.java`

---

## Overview

A passenger attempts to change a domestic same-day flight on AA.com or the mobile
app. The eligibility service determines the change is blocked. Instead of a generic
"ineligible" message, the platform returns a structured reason code with a plain-
language explanation and a suggested next step.

---

## Actors

- **Passenger** — self-serve channel (mobile app via `changetrip-ios`)  
- **ChangeTripController** — REST entry point (`api/controller/changetrip/ChangeTripController.java`)  
- **ChangeTripService / ChangeTripServiceImplementation** — orchestration (`api/service/`)  
- **ReshopEligibilityBuilder** — request construction (`api/builder/changetrip/ReshopEligibilityBuilder.java`)  
- **Downstream reshop/eligibility** — rule evaluation returning `ReshopEligibilityResponse` with `RuleResult` list  
- **SelectFlightViewModel** — iOS reason code display (`Sources/ViewModels/SelectFlightViewModel.swift`)

---

## Happy Path

1. Passenger taps "Change Flight" in `changetrip-ios`; `ChangeTripHostingViewController.swift` initiates flow.
2. `ChangeTripController` receives `ChangeTripEligibilityRequest` (PNR = `recordLocator`, flight details).
3. `ReshopEligibilityBuilder.buildReshopEligibilityRequest()` constructs the downstream `ReshopEligibilityRequest` with `HeaderRequest` (clientId, transactionId) and `SearchCriteria`.
4. Downstream reshop/eligibility returns `ReshopEligibilityResponse` containing a list of `RuleResult` objects.
5. `ChangeTripServiceImplementation` maps `RuleResult.reasonCode` + `RuleResult.regulatoryRef` into `ChangeTripEligibilityResponse`.
6. `SelectFlightViewModel.swift` receives `INELIGIBLE` response and renders plain-language explanation with suggested next action.
7. Interaction is logged to audit trail (BUS-7.1).

---

## Key Classes

| Class | Package | Role |
|-------|---------|------|
| `ChangeTripController` | `api/controller/changetrip/` | POST /change-trip/eligibility endpoint |
| `ChangeTripService` | `api/service/` | Service interface |
| `ChangeTripServiceImplementation` | `api/service/implementation/` | Orchestration logic |
| `ReshopEligibilityBuilder` | `api/builder/changetrip/` | Builds ReshopEligibilityRequest |
| `ReshopEligibilityRequest` | `domain/changetrip/infrastructure/reshop/eligibility/` | Downstream request model |
| `ReshopEligibilityResponse` | `domain/changetrip/infrastructure/reshop/eligibility/` | Downstream response model |
| `RuleResult` | `domain/changetrip/infrastructure/reshop/eligibility/` | Per-rule result with reason code |
| `ChangeabilityBuilder` | `api/builder/changetrip/` | Builds changeability assessment |

---

## Exception Paths

| Scenario | Handling |
|----------|---------|
| Eligibility service timeout | `ChangeTripServiceImplementation` returns degraded `ChangeTripEligibilityResponse`; BFF logs via `@Timed` / `@TransactionId` interceptors |
| Unknown `RuleResult.reasonCode` | `ChangeTripServiceImplementation` logs unknown code, returns generic fallback explanation |
| Passenger authenticated but PNR not found | Controller returns 404 before calling `ReshopEligibilityBuilder` |

---

## Acceptance Criteria (Slice 1)

- 100% of INELIGIBLE `RuleResult` objects include a non-null `reasonCode`
- `RuleResult.regulatoryRef` present for all airline-initiated IROP ineligible cases (BUS-2.1)
- 0% of reason codes result in a UI error state in `SelectFlightViewModel`
- Reason code accuracy ≥90% (validated by agent audit of 100 ineligible samples)
- Passenger clarity score ≥3.5/5 in post-result survey
- `EligibilityEndpointTest.java` covers: eligible, ineligible with reason code, IROP with `regulatoryRef`, timeout degraded response

---

## Test Coverage

**BFF tests:** `src/test/java/com/aa/change/bff/api/controller/changetrip/EligibilityEndpointTest.java`  
**iOS tests:** `Tests/Sources/ChangeTripInfoFetcherTests_Flights.swift` — ineligibility reason propagation to ViewModel
