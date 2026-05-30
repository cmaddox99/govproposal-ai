---
laws: [PRD-1.5]
avatar: [gate-management]
title: Evidence-Based Decisions — Gate Management Platform
---

# PRD-1.5: Evidence-Based Decisions

**Law Reference:** PRD-1.5: Evidence-Based Decisions
**Avatar:** gate-management

No gate management feature decision may be based solely on opinion, stakeholder request, or assumption. Every product decision must be supported by telemetry, direct observation, or validated data from gate operations. PRD-1.5 prohibits opinion-only feature decisions.

---

## What PRD-1.5 Requires

1. **Telemetry-first decisions** — All feature prioritization cites measurable data (latency, match rate, error rate, agent action time)
2. **Baseline before building** — Establish current-state metrics before committing to a solution
3. **Decision log** — Every significant product decision records the evidence that justified it
4. **No HIPPO-driven features** — "Highest Paid Person's Opinion" is not evidence; gate agent observed behavior is

---

## Gate Management Evidence Sources

| Signal Type | Source | Metric Example |
|-------------|--------|----------------|
| Digital Signage performance | DSS telemetry (Azure Monitor) | P95 display refresh latency: 340 ms → target < 200 ms |
| Biometric boarding accuracy | CBP/TSA match API response logs | False rejection rate: 0.8% → target < 0.3% |
| Carry-on decision quality | Gate agent override rate in DCS | Agent override rate: 12% → target < 5% (overrides = policy errors) |
| Gate agent action time | Connect Me delivery receipts + DCS event timestamps | IROP response time: 4.2 min → target < 2 min |
| Boarding close speed | Boarding sequence completion logs | Door-close-ready time: 8 min post-final-scan → target < 5 min |

---

## PRD-1.5 Compliant Decision Example

**Decision:** Add predictive gate-change banner to digital signage boards

**Evidence:**
- Telemetry: 23% of gate changes occur < 45 min before departure (AOC event logs, 90 days)
- Observation: Gate agents report passengers miss gate change notifications 34% of the time (structured interview, 12 agents, 3 stations)
- Cost: Average irregular ops cost per missed gate change: $1,840 in re-accommodation (Finance data, FY25)

**Hypothesis:** A persistent "GATE CHANGE" banner displayed ≥ 30 min before departure will reduce passenger miss rate from 34% to < 10%.

**Decision gate:** Instrument the feature to measure passenger miss rate via biometric scan arrival time vs. new gate departure time. Gate after 30-day pilot at DFW.

---

## PRD-1.5 Violation Examples (Prohibited)

```
❌ "Let's add a countdown timer to the boarding display — passengers seem to like it."
   (No telemetry, no observation — opinion only)

❌ "The VP of Airport Operations wants a dashboard showing live gate utilization."
   (HIPPO request without evidence of agent need or measurable outcome)

❌ "Competitors have biometric boarding — we should too."
   (Benchmarking without problem evidence for AA's specific gate operations context)
```

---

## Evidence Collection Checklist (Pre-Feature)

Before any gate management feature enters the roadmap:

- [ ] Metric baseline established (current state measured, not estimated)
- [ ] Data source identified (DSS telemetry / DCS logs / AOC events / agent interviews)
- [ ] Hypothesis stated in measurable form: "If X, then Y will change from A to B"
- [ ] Decision gate defined: What metric change confirms the hypothesis?
- [ ] Negative evidence considered: What data would prove the feature is NOT needed?
