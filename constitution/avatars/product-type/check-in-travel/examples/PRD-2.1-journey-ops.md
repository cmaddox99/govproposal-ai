# PRD-2.1: Journey Detail — Maria + Operations Staff
# Companion to PRD-2.1-journey.md | Laws: PRD-2.1, PRD-1.1, BUS-2.2, ENG-6.4

---

## Journey 2: Maria — Supported Counter/Kiosk Journey

**Pre-departure (often skipped):**  
Receives reminder → Tries website → Interface confusing → Decides *"I'll do it at the airport"* → Doesn't check in online

**Airport arrival:**  
Arrives 3h early → Goes to counter (sees kiosk but unsure) → Hands ID + confirmation to agent → Agent checks her in → Issues printed boarding pass

**Security & gate:**  
TSA screening (no PreCheck, 20 min) → Walks to gate → Asks agent "Is this the right gate?" → Waits → Hears PA (confused about zones) → Boards when agent points to her

| Step | Pain | Design opportunity |
|------|------|-------------------|
| Online check-in | Too complex; app requires Face ID she hasn't set up | Simplified online flow; phone support option |
| Counter orientation | Confusing signage; doesn't want to hold up line | Greeter staff; clear directional signage |
| Baggage handoff | *"Will my bag make it? Where do I pick it up?"* | Verbal explanation + baggage tracking number |
| Boarding zone | PA announces zone; Maria doesn't know which is hers | Personalised SMS "You're in Group 3, boards at 8:15am" |

**Maria's targets:** Counter satisfaction 78%→85%, accessibility perception (felt supported) 72%→90%, boarding confusion incidents 12%→<5%.

---

## Journey 3: Kevin — Gate Operations

**Pre-boarding setup (60 min before):**  
Arrives at gate → Reviews manifest (manual, 10 min) → Notes standby/accessibility/unaccompanied minors → Calls standbys (30 min before pushback) → Opens gate → Calibrates scanner

**Boarding (35-45 min):**  
Scans each passenger → Mobile failures (8%): manually looks up each one (5-10 min) → Manages oversell if discovered → Handles accessibility at gate (discovers needs real-time) → Confirms all boarded → Closes gate → Coordinates pushback

| Failure mode | Frequency | Time cost | Fix |
|---|---|---|---|
| Mobile barcode fails | 8% of passes | 7.5 min each | Pre-gate validation |
| Oversell discovered at gate | ~2.5 per 100 flights | 20 min scramble | Predictive alert 30 min before |
| Accessibility discovered at gate | Routine | 5-10 min | Manifest flag from booking |
| Seat assignment mismatch | 2% of passengers | 3 min per conflict | Real-time sync (<1 sec lag) |

---

## Journey 4: Patricia — Monitoring & Decision

**Start of day (5am):**  
Reviews overnight incidents (manual log, 20 min) → Checks system health → Forecasts peak staffing → Monitors 6-8am departures → Adjusts in real time

**Issue response:**  
Radio call arrives ("Gate 15 boarding time 42 min") → Patricia checks dashboard (10 min lag) → Root cause analysis (10-15 min) → Allocates staff from elsewhere → Manual recovery → Documents learning

**Patricia's targets:** On-time 78%→82%, boarding 40→35 min, incident response time 20 min→<10 min, lab hours per 1K pax 6.8→5.2.

**What transforms Patricia from reactive to proactive:** Real-time gate dashboard + predictive oversell alerts + automated incident root-cause. She needs a system that calls her before Kevin calls her on the radio.
