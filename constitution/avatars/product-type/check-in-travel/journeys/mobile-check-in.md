# Journey: Mobile Check-In
# Avatar: avatar-check-in-travel | Law: PRD-3.2 Journey Mapping Law
# Grounded in: checkin-ios analysis (2025-07-17) — 178 source files, 280 test methods
# Source modules: CheckInManager/, CheckInReservationViewController/, IFCI/, TravelerContactInfo/

journey:
  id: journey-mobile-check-in
  name: Mobile Check-In (Non-BE Flow)
  persona: Passenger checking in via AA iOS app 24h–1h before departure
  laws: [PRD-3.2, PRD-1.2, BUS-2.1, BUS-2.2, BUS-4.1, ENG-6.4]
  source_evidence: checkin-ios code-quality-analysis.md (2025-07-17)

---

## Journey Map

| Step | What the passenger does | iOS module | Key law |
|------|------------------------|------------|---------|
| 1. Eligibility check | App determines if check-in is available for segment | `CheckInManager.isCheckInAvailable()` | BUS-2.1 |
| 2. Hazmat declaration | Confirms no prohibited items | `Hazmat/` module | BUS-2.2 (TSA) |
| 3. IFCI (international) | Scans passport via NFC or manual entry | `IFCI/ScanPassportViewController` | BUS-2.2, ENG-6.4 |
| 4. Traveller contact info | Confirms / updates contact details | `TravelerContactInfoViewController` (918 lines) | BUS-4.1 |
| 5. Offers (optional) | Upgrade offer presented if eligible | `CheckInOffersManager` | PRD-3.2 |
| 6. Check-in confirmation | `CheckInManager` submits to server; state machine advances | `AACheckInStateMachine` | BUS-2.1, ENG-6.7 |
| 7. Boarding pass | Boarding pass rendered; wallet add offered | `aa-ct-mobile-boardingpass-bff` | ENG-6.4 |

## Architecture Evidence

`CheckInManager.swift` (1,186 lines) is the God Controller for this journey — it owns state machine coordination, server calls, UI presentation, analytics, and notifications simultaneously. Per ENG-3.1, this is the highest-priority refactoring target in the check-in flow.

The codebase has already begun the right pattern with extension-based decomposition (`CheckInManager_Analytics.swift`, `CheckInManager_Notifications.swift`) — this should continue toward full coordinator extraction.

## TSA Compliance (BUS-2.2)

Hazmat declaration and IFCI passport validation are TSA-mandated gates. The `CheckInManagerProvider` strategy pattern (`CheckInManager` vs `CheckInOffersManager`) must not bypass either gate regardless of feature toggle state.

## IFCI International Passport Scanning Flow

The International Flight Check-In (IFCI) sub-flow is triggered when a passenger's segment requires travel document verification. Real module names:

| Step | Module | Description |
|------|--------|-------------|
| 1. Passport scan entry | `IFCI/ScanPassport/ScanPassportViewController.swift` | Presents camera scan UI for machine-readable zone (MRZ) |
| 2. NFC fallback | `IFCI/NFCScanning/MRZEntryViewController.swift` | Manual MRZ entry if NFC chip read fails |
| 3. Document validation | `IFCI/VerifyTravelDocuments/` | Cross-checks passport data against PNR |
| 4. Infant check | `IFCI/InfantCheck/` | Flags infants-in-arms and lap-infant records |
| 5. Passenger validation | `IFCI/ValidatePassenger/IFCIValidatePassengerViewController.swift` | Final validate-passenger call; submits to `mobile-fly-checkin-bff` |

Travel document status is built in `mobile-fly-checkin-bff` at `checkin/performer/model/traveldocs/TravelDocsStatusRequestBuilder.java` — the iOS IFCI flow calls this BFF endpoint. Passport data (PII) must not be retained beyond the session per ENG-6.4.

## Privacy at the Gate (BUS-4.1)

`TravelerContactInfoViewController` collects contact details. Location data is not captured at this step — if added in future, a Privacy Impact Assessment is required under BUS-4.5.
