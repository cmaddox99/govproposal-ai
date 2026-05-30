# Use Case: Gate Operations — Real-Time Visibility & Boarding Optimisation
# Avatar: avatar-check-in-travel | Laws: PRD-1.1, PRD-2.1, PRD-3.1, PRD-4.1, PRD-5.1
# Detail: mvp-results.md (MVP 1-4 validation) · outcomes.md (Phase 4 launch + business impact)

use_case:
  id: uc-cit-gate-operations
  name: Gate Operations — Real-Time Visibility & Predictive Boarding
  jtbd: "When I'm managing a gate, I want to know about problems before boarding starts so I can solve them calmly instead of firefighting."
  actor: Kevin (gate agent) + Patricia (ops manager)
  laws: [PRD-1.1, PRD-2.1, PRD-3.1, PRD-5.1]
  targets: "Boarding 40→35 min; on-time 78%→82%; manual lookups 40→6/flight"

---

## Why This Use Case Exists

Kevin does 40 manual passenger lookups per flight, each taking 7.5 min = 300 min of manual work per gate per day. Patricia learns about gate problems from radio calls, not dashboards — always reactive, never proactive. This use case converts both from firefighters to conductors.

## Phase 1: Discovery (Q1)

**Gate agent observations:** 50 gates, morning + evening peak, 3 hubs (ATL/DFW/LAX)

**Bottlenecks ranked:**
| Problem | Root cause | Time cost per flight |
|---------|-----------|---------------------|
| Manual lookups (40/flight) | No pre-scan barcode validation | 300 min |
| Oversell at gate | No predictive alert | 20 min scramble |
| Seat assignment mismatch | 10-min system sync lag | 3 min per conflict (2% of pax) |
| Accessibility surprise | Not flagged in gate system | 10-15 min per incident |

**Competitive gap:** United has 30-min oversell alerts, 82% on-time. Delta has real-time baggage integration. American: reactive, 78% on-time.

## Phase 2: Roadmap (Q1-Q2)

**Tier 1 features (4 features, all validated as MVPs):**
1. **Pre-gate boarding pass validation** — Flags invalid passes 15 min before boarding → 80% of manual lookups eliminated
2. **Real-time gate dashboard** — Mobile tablet for Kevin: pax list, check-in status, accessibility flags, live boarding count
3. **Predictive oversell alerts** — 30 min pre-departure alert → automated volunteer SMS → no gate-level scramble
4. **Real-time seat sync** — Assignment pushed to printer in <1 sec (vs. current 10-min lag)

## Pre-conditions

- Kevin has a gate tablet configured with dashboard access
- Flight is T-60 min or less
- Check-in data feed is live (≥99.2% uptime required)

## Main Flow — Boarding with Dashboard

1. Kevin arrives at gate T-60 min; opens dashboard
2. Manifest visible: 148 checked in / 6 not checked in / 3 accessibility flags / 2 standbys
3. T-30 min: Oversell prediction runs → no oversell on this flight → green status
4. T-15 min: Pre-gate validation scans all 154 passes → 2 flagged invalid → Kevin notified → passengers redirect to kiosk
5. Boarding opens: Kevin scans passengers — first-try success rate 98% (vs 92% baseline)
6. Dashboard count ticks up in real time → confirms all 154 boarded → gate closed → pushback

## Alternate Flows

| Branch | Trigger | Resolution |
|--------|---------|------------|
| Oversell detected T-30 min | More confirmed pax than seats | Automated SMS to standbys: volunteer offer + same-day rebooking |
| Accessibility pax arrives | Flag on dashboard | Kevin pre-positioned assistance; no delay |
| Scanner failure (hardware) | Gate scanner offline | Dashboard shows passenger confirmation fallback — Kevin approves by name |
| Late pax not in system | Connecting flight delay | Kevin can look up by confirmation code in <3 sec |

> See `mvp-results.md` for validated metrics from 600-flight beta. See `outcomes.md` for Q4 launch results and $13M+ business impact.
