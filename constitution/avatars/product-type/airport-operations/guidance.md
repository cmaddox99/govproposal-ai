---
avatar: avatar-airport-operations
domain: Gate Management, Crew Coordination, IROP Response
laws:
  - BUS-2.1
  - BUS-2.2
  - BUS-2.3
  - PRD-1.2
  - PRD-5.1
  - ENG-6.7
skills:
  - 14-real-time-data-integration
  - 22-decision-support
  - 06-atomic-tdd
---

# Airport Operations — Implementation Guidance

## Overview

Airport Operations tools serve gate agents, operations controllers, and station managers managing flight turns, crew coordination, and irregular operations (IROP) recovery. The primary failure mode in this domain is **decision latency** — agents acting on stale data cause downstream delays. Every feature must be evaluated against this root cause.

---

## Core Journeys

| Journey | Persona | Success Metric |
|---------|---------|----------------|
| Gate Assignment | Operations Controller | Zero gate conflicts at push |
| Crew Management | Crew Scheduler | 100% legal crew at departure |
| Ground Handling | Ramp Supervisor | Turn ≤ 45 min domestic |
| IROP Recovery | Operations Controller | Recovery stabilized within 90 min |
| Flight Dispatch | Operations Controller | D0 rate > 60% |

**Key personas:** Gate Agent, Crew Scheduler, Ramp Supervisor, Operations Controller, Station Manager.

---

## Non-Negotiable Laws

### BUS-2.3 — DOT Tarmac Delay Rule
- **Domestic:** Return to gate or deplane at 3-hour mark. System must surface tarmac timer when aircraft door closes on the ground.
- **International:** 4-hour hard limit. Timer triggers at door-close, not pushback.
- **Implementation:** Any operations dashboard must display tarmac elapsed time prominently; alert at T−30 min. Never suppress or hide this timer.

### BUS-2.1 — FAA Compliance (Crew Scheduling)
- FAR Part 117 rest/duty limits are hard constraints, not soft recommendations.
- Crew reassignment tools must reject illegally-short rest periods at data entry, not post-save.
- Any proposed crew swap must show the legal status (rest hours remaining, duty period length) before the scheduler confirms.

### BUS-2.2 — TSA Security Protocols
- IROP recovery plans must never route passengers through sterile-area breaches to save time.
- Gate reassignments that cross concourse security boundaries require TSA coordination flag; tool must surface this automatically.

### PRD-1.2 — Problem-First
- Validate the specific decision latency gap (seconds of delay per affected departure) before building dashboards.
- Research: `turn_time_analysis`, `delay_causation_studies`, `gate_conflict_patterns`, `crew_utilization_metrics`.

### PRD-5.1 — MVP
- Single-station pilot before network rollout. Gate notification push for one hub (e.g., DFW) is the correct MVP; full IROP automation is not.

---

## Key Patterns

- **Push over pull:** Gate agents must not poll for status; systems must push alerts (gate change, bag count, crew arrival) proactively.
- **Tarmac timer always visible:** Never hide in a tab or sub-screen. Pin to top of operations view.
- **Crew legality pre-check:** Run FAR 117 legality check before presenting swap option to scheduler — not after selection.
- **Cross-system integration:** Gate, crew, and baggage systems must share a common flight context; siloed data is the #1 source of turn-time failures.

---

## Anti-Patterns

- ❌ Building a "gate status dashboard" without validating that **decision latency** (not data absence) is the root cause of delays.
- ❌ Tarmac timer displayed only in an admin view; it belongs on every gate agent screen.
- ❌ Suggesting a crew swap that would violate FAR 117 and requiring the scheduler to check legality manually.
- ❌ IROP recovery tools that route passengers through unsecured areas — TSA compliance is non-negotiable even under operational pressure.
- ❌ Network-wide rollout before single-station pilot proves the D0/turn-time hypothesis.
