# Use Case: Airport Check-In — Counter & Kiosk for Supported Passengers
# Avatar: avatar-check-in-travel | Laws: PRD-1.1, PRD-2.1, PRD-3.1, PRD-4.1, PRD-5.1, BUS-2.2, ENG-6.4
# Detail: mvp-results.md · outcomes.md

use_case:
  id: uc-cit-airport-checkin
  name: Airport Check-In — Counter & Kiosk Optimisation
  jtbd: "When I check in at the airport, I want a clear, supported process that doesn't make me feel rushed or confused — with or without technology."
  actor: Maria (airport-preferred traveller) + Kevin (counter agent) + Patricia (ops)
  laws: [PRD-1.1, PRD-2.1, PRD-3.1, PRD-4.1, BUS-2.2, ENG-6.4]
  targets: "Counter time 12→8 min; kiosk completion 60%→75%; special services 12→8 min; peak wait 30→15 min"

---

## Why This Use Case Exists

48% of passengers still prefer airport check-in. Current counter average: 12 min (8 min service + 4 min wait). Kiosk completion: 60% — 40% fail and go to the counter anyway. Special services (wheelchair, unaccompanied minor, language barrier) take 12 min vs. 6 min standard: 2× time for passengers who most need support.

## Phase 1: Discovery (Q1)

**Research:** 800 passengers at DEN/ATL/DFW + counter agent shift observations

**Why passengers still use the counter:**
- Never used digital before (35%)
- Prefer human help (25%)
- Complex booking/worried about something (30%)
- Luggage concerns (10%)

**Kiosk abandonment reasons:**
- Too complicated — 7-step flow, confusing language (40%)
- Touchscreen unresponsive — double-booking risk (20%)
- Unclear baggage fees — passenger exits to ask at counter (20%)
- Language barrier (10%)
- Hardware issues (10%)

**Special services pain:** Wheelchair 12 min, unaccompanied minor 8 min, language barrier 15 min. Root cause: none of it is integrated — agent discovers needs at the counter and scrambles for forms from a separate system.

**Competitive gap:** United 70% kiosk completion / Delta 72% / American 60%

## Phase 2: Roadmap (Q1-Q2)

**Tier 1 features:**
1. **Kiosk UX simplification** — 7 steps → 4 steps, large text, baggage fee preview, plain language
2. **Pre-luggage weight alerts** — ML model flags likely-overweight passengers 24h before → agent pre-warns; eliminates 5-10 min of surprise
3. **Special services integration** — Wheelchair/minor/medical/language flags from booking → agent sees upfront; system prints forms
4. **Counter queue management** — Real-time wait display at terminal entrance + "Check in at gate" diversion option

## Pre-conditions (Special Services — BUS-2.2)

- For IFCI (international): Passport scan or manual entry must be completed before boarding pass is issued
- For unaccompanied minors: Release waiver signed and printed before boarding
- For medical devices (oxygen, mobility aid): Baggage rules validated against DOT regulations

## Main Flow — Maria at Kiosk (New UX)

1. Maria approaches kiosk, sees "Check in in 2 minutes"
2. Scans confirmation barcode from email (or types confirmation code)
3. Flight confirmed → bag count question ("How many checked bags?") with fee shown upfront
4. Seat confirmed (pre-assigned shown; option to change)
5. Boarding pass printed + email copy sent
6. Maria proceeds to baggage drop; receives tracking number verbally from agent

## Main Flow — Maria at Counter

1. Agent greeted Maria; ID + confirmation scanned
2. Dashboard shows: seat, baggage plan, accessibility flag (large text preferred)
3. Luggage weighed → if overweight, agent pre-warned by alert → conversation prepared
4. Boarding pass printed; agent explains baggage tracking number
5. Maria leaves with printed pass + verbal confirmation of gate and zone

## Alternate Flows

| Branch | Trigger | Resolution |
|--------|---------|------------|
| Kiosk abandoned mid-flow | Touchscreen unresponsive | Kiosk locks state for 60 sec; same session resumes on tap |
| Overweight baggage discovered | Weight exceeds limit | Fee shown on screen; option to pay or remove items |
| Special services not in system | Booked via phone without flag | Agent adds flag manually; system prints appropriate form |
| Peak-hour queue >25 min | Queue management alert | Agent offers: "Would you prefer to check in at the gate?" |

> See `mvp-results.md` for all 4 MVP validation results. See `outcomes.md` for Q3-Q4 business impact ($17M+ annually).
