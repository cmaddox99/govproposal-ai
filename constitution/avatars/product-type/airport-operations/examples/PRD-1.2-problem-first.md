---
law: PRD-1.2
avatar: avatar-product-airport-operations
title: "Problem-First: Gate Status During IROP"
---

# PRD-1.2 Problem-First — Airport Operations

## Law Summary

Validate the real problem before proposing a solution. The stated request and the validated problem are often different things.

---

## ✅ COMPLIANT Example

### Stated Request

> "Build a gate status dashboard so gate agents can see what's happening during IROP."

### Validated Problem (After Research)

A 3-week analysis of departure delay logs at DFW identified the root cause: **decision latency** — gate agents acting on status information that is 4–8 minutes old.

| Finding | Data Source | Value |
|---------|------------|-------|
| % of IROP delays attributable to gate agent receiving stale status | Delay log analysis (3 weeks) | 41% |
| Average age of gate status data at time of agent decision | Workflow observation | 6.2 minutes |
| Gap between OCC broadcast and agent acknowledgment | Call log analysis | 4–8 minutes |
| Agent-reported #1 frustration | Workflow interviews (12 agents) | "I find out about gate changes from passengers" |

**Root cause:** Gate agents lack push notifications. They poll the GMS screen or hear changes secondhand. A passive dashboard does not fix this — the dashboard is already available and ignored.

### Correct Problem Statement

> Gate agents at DFW are making boarding and departure decisions based on gate-status data that is 4–8 minutes stale. This causes 41% of IROP-related departure delays at the station. The problem is **information push latency**, not information absence. A static dashboard will not reduce decision latency.

### Validated Solution Direction

Push notifications to gate agent mobile devices (or workstation alerts) when: gate reassignment occurs, bag count is ready, crew arrival is confirmed, or tarmac timer crosses T−30 min.

---

## ❌ VIOLATION Example

> "Gate agents don't have visibility into what's happening. Build a gate status dashboard that shows all flights, gate assignments, bag counts, crew status, and IROP flags in real time."

**Why this violates PRD-1.2:**
- No root cause identified: is the problem data absence, or data delivery mechanism?
- No quantification: how many delays does this cause? What is the dollar impact?
- Solution (dashboard) assumed before problem is validated.
- A dashboard already exists in GMS — agents don't use it. No investigation into why.

**Correct first step:** 3-week delay log analysis + 12 agent workflow observations to identify whether the problem is data absence or push latency. Then propose the minimum intervention.
