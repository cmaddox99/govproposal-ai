# Use Case: Digital Check-In — Mobile-First Experience Optimisation
# Avatar: avatar-check-in-travel | Laws: PRD-1.1, PRD-2.1, PRD-3.1, PRD-4.1, PRD-5.1
# Detail: implementation-results.md (Phase 3-4 MVP results + business impact)

use_case:
  id: uc-cit-digital-check-in
  name: Digital Check-In — Mobile Adoption & Reliability
  jtbd: "When I check in for my flight, I want to do it from my phone and trust it will work at the gate — no backup plan needed."
  actor: Alex (digital traveller) + Patricia (ops)
  laws: [PRD-1.1, PRD-3.1, PRD-4.1, PRD-5.1]
  duration: 12 months (Q1-Q4 2026)
  targets: "Mobile adoption 52%→72%; reliability 92%→99.9%; gate-level failures 8%→2%"

---

## Why This Use Case Exists

52% of passengers use mobile check-in. Competitors: 68-78%. The 8% failure rate (112K daily gate recoveries) is the #1 cause of preventable boarding delays. Alex takes a screenshot of his boarding pass because he doesn't trust the app — that's the design problem this use case solves.

## Phase 1: Discovery (Q1)

**Research:** 450 participants (200 digital travellers, 150 airport pax, 100 accessibility pax, 25 gate agents, 30 days operational data)

**Barriers to mobile adoption:**
- App too complicated (35% of non-users)
- Don't trust phone at gate (25%)
- WiFi concerns (15%)
- Prefer printed backup (15%)

**Mobile failure root causes:**
- App crash (3%) — outdated framework
- Offline barcode invalid (2%) — barcode generated online only
- Scanner incompatibility (2%) — older QR format
- Auth timeout (1%) — session expires at airport

**Competitive gap:** Southwest 78% adoption / 2% failure · United 72% / 3% · American 52% / 8%

## Phase 2: Roadmap (Q1-Q2)

**Tier 1 features:**
1. **Offline barcode** — Generate + cache locally; works without network → eliminates 2% offline failures
2. **App redesign** — 5-step flow, large buttons, estimated "90 seconds" framing → removes complexity barrier
3. **Pre-gate validation** — Alert 15 min before boarding; instant kiosk backup if invalid → gate never sees failures
4. **App stability** — Framework upgrade; optimised for peak load → crashes 3%→0.2%

**Q2 interim targets:** Mobile adoption 52%→58%, reliability 92%→95%, gate-level recovery 8%→5%

## Pre-conditions

- Passenger is authenticated (AAdvantage or guest)
- Check-in window is open (24h–1h before departure)
- Feature toggles for offline barcode and pre-gate validation are enabled

## Main Flow (Happy Path)

1. Push notification arrives 24h before flight
2. Passenger opens app → Face ID → selects flight → seat confirmed
3. Boarding pass generated and cached locally (offline mode)
4. 15 min before boarding: pre-gate validation runs → green indicator shown
5. Passenger scans phone at gate → first-try success → boards

## Alternate Flows

| Branch | Trigger | Resolution |
|--------|---------|------------|
| Offline barcode invalid | Validation fails 15 min before boarding | Redirect to nearest kiosk for instant printed backup |
| App crash during validation | Runtime error | Deep-link to kiosk QR code shown on lock screen |
| Auth expired at airport | Session timeout | 1-tap Face ID re-auth without re-entering credentials |
| Flight gate changed | API push during validation | New gate shown on boarding pass before passenger leaves security |

> See `implementation-results.md` for Phase 3 MVP validation results and Phase 4 launch outcomes.

---

## Implementation Grounding (checkin-ios)

The main flow maps directly to these `checkin-ios` modules:

| Flow step | iOS class | Role |
|-----------|-----------|------|
| Check-in window open | `Relevance/AAFeatureCheckInEligible.swift` | Feature flag controlling eligibility |
| Modernised flow toggle | `Relevance/AAFeatureFlyCheckinModernization.swift` | A/B gates new step sequencing |
| Entry point | `CheckInReservationViewController/CheckInReservationViewController.swift` | Primary check-in entry VC |
| Orchestration | `CheckInManager/CheckInManager.swift` | State machine; server calls; analytics |
| Hazmat gate | `Hazmat/HazmatViewController.swift` + `HazmatProcessor.swift` | TSA-mandated prohibited-items declaration |
| IFCI passport scan | `IFCI/ScanPassport/ScanPassportViewController.swift` | Camera MRZ capture |
| NFC passport fallback | `IFCI/NFCScanning/MRZEntryViewController.swift` | Manual MRZ entry |
| Passenger validation | `IFCI/ValidatePassenger/IFCIValidatePassengerViewController.swift` | Final CBP/TSA document check |
| Contact info | `TravelerContactInfo/TravelerContactInfoViewController.swift` | PNR contact update |

Tests follow `*Tests.swift` / `*UnitTests.swift` convention in `Tests/Sources/`; mocks via `MockURLProtocol` in `Tests/SharedSources/MockData/`.
