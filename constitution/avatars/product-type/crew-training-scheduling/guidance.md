---
avatar: avatar-crew-training-scheduling
domain: FAR Part 117 Crew Rest/Duty Limits, Crew Licensing, Training Compliance, Pairing/Bidding
laws:
  - BUS-2.1
  - BUS-7.1
  - PRD-1.2
  - PRD-5.1
  - ENG-6.7
skills:
  - 06-atomic-tdd
  - 07-vertical-slice-dev
  - 21-prompt-engineering
---

# Crew Training Scheduling — Implementation Guidance

## Overview

Crew Training Scheduling tools optimize pilot OE (Operating Experience) training sequences. The reference implementation is **JOSE — Journey Optimization & Spoilage Elimination**. The core problem: Flight Standards blocks OE sequences weeks in advance; by training time, student/CKP availability has shifted, leaving sequences unassigned ("open blocked") and at risk of spoilage — forcing costly buy-sequence recovery. A MIP solver generates the globally optimal assignment in minutes.

---

## Core Journeys

| Journey | Persona | Success Metric |
|---------|---------|----------------|
| Open blocked sequence recovery | Mid-Range Scheduler | Open Blkd Seq Saved ↑ |
| Buy-sequence elimination | Scheduling Coordinator | Buy Sequences Dropped ↑ |
| OE training completion | Training Manager | Students Completed ↑ |
| Solution quality review | OR Scientist | Solution Acceptance Rate ≥ 80% |
| Scoring weight tuning | OR Developer | Infeasibility Rate < 5% |

**Key personas:** Mid-Range Scheduler, Scheduling Coordinator, OR Scientist, OR Developer, Training Manager, Compliance Officer.

---

## Non-Negotiable Laws

### BUS-2.1 — FAA Compliance (FAR Part 117)

All scheduling constraints encoding FAR rules **must** cite the specific FAR section in code comments and have a corresponding characterization test traceable FAR rule → constraint method → test → commit.

| Constraint | FAR Citation | Required Implementation |
|------------|--------------|------------------------|
| Min 10-hour rest between duties | FAR Part 117.25(b) | Hard reject in `NetworkGenerator` feasibility filter |
| Max 5 consecutive working days | FAR Part 117.23 | Rolling 7-day window check; cannot be overridden by UI |
| Total hours cap ≤ 30 | OE policy (FAA-backed) | Option generation hour cap; alert if approaching limit |

Any change to completion-reward logic must be reviewed against FAA requirements from `api/oeinputs/trainings/`.

### BUS-7.1 — Audit Trail
- Every optimizer run must log: UserID, Fleet, ContractMonth, solver status, objective value, solve time, snapshot ID.
- `SolutionRecommendation.xlsx` and `SelectedStudentOptions.xlsx` are artifacts of record — retained per audit policy.

### PRD-1.2 — Problem-First
- Validate spoilage rate and buy-sequence cost baseline before any feature extension.
- Research: `spoilage_rate_by_fleet_and_base`, `buy_sequence_cost_per_month`, `solution_acceptance_rate_per_run`.

### PRD-5.1 — MVP
- MVP = feasible solution + freeze window enforcement + sequence exclusivity + scheduler-readable Excel output + run audit trail.
- Email notifications, K-best pruning, and real-time run status are enhancements — not MVP.

---

## Key Patterns

- **Freeze window is inviolable:** Never recommend changes within N days of sequence start; surface freeze reason in Excluded/Unchanged sheet.
- **Scheduler-readable output:** `SolutionRecommendation.xlsx` is the primary interface — Metrics, Student Actions, CKP Actions sheets required on every run.
- **Operational alerts:** Solve Time > 10 min → alert OR team. Infeasibility Rate > 5% → escalate for constraint review.
- **Experimental profiles:** Scoring weight changes go through `test.json` with `enableExperimental: true`; standard profile is never modified in production without OR Scientist sign-off.

---

## Anti-Patterns

- ❌ Deploying scoring weight changes without an experimental profile run and characterization tests.
- ❌ Suppressing the freeze window check to "recover" more sequences — FAA compliance is not negotiable.
- ❌ Presenting solution metrics without the Warnings and Excluded Students sheets (schedulers need full context to trust recommendations).
- ❌ Reporting Solution Acceptance Rate without tracking override reasons — low acceptance without root-cause data cannot drive improvement.
- ❌ Building real-time run status UI before acceptance rate ≥ 80% is achieved (solve the quality problem first).
