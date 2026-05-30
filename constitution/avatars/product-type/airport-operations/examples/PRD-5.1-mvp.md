---
law: PRD-5.1
avatar: avatar-product-airport-operations
title: "MVP: Gate Change Push Notifications Pilot"
---

# PRD-5.1 MVP Law — Airport Operations

## Law Summary

The smallest possible experiment that validates the core hypothesis is the correct first investment. Do not automate the full IROP workflow before testing whether push notification delivery reduces departure delays.

---

## ✅ COMPLIANT Example — MVP Canvas

### Hypothesis

> Gate agents at DFW who receive push notifications for gate changes and ramp readiness will have 10% fewer departure delays attributable to information latency, compared to agents using the current GMS polling workflow.

### Riskiest Assumption

Agents will act on push notifications faster than they currently act on GMS screens or verbal radio updates. If agents ignore notifications or find them disruptive, the hypothesis fails.

### MVP Scope

**In scope:**
- 5 gate agents, DFW Terminal B, 4-week pilot
- Push notifications for: gate reassignment, bag count confirmed, crew arrival at gate, tarmac timer T−30 min alert
- Android/iOS app notification only (no new hardware)
- Manual dispatch from OCC workstation (no automated triggers)

**Out of scope:**
- Full IROP automation
- Crew reassignment workflows
- Network-wide rollout
- Integration with GMS, SABRE, or crew systems
- Automated trigger logic

### Success Criteria

| Metric | Baseline | Target | Measurement |
|--------|----------|--------|-------------|
| Departure delays (info-latency cause) per gate per week | 3.2 | ≤ 2.9 (10% reduction) | Delay log coded by cause |
| Agent notification acknowledgment time | N/A | < 90 seconds | App telemetry |
| Agent satisfaction with notifications | N/A | ≥ 4.0/5.0 | Weekly survey (5 agents) |

### Fail Criteria (Stop and Pivot)

- Delay reduction < 5% after 4 weeks: notification delivery is not the right intervention — investigate rebooking tools or OCC workflow instead.
- Agent satisfaction < 3.0/5.0: notification format or frequency is causing friction — redesign before expanding.

### What This Proves

If successful, this MVP proves that push notification delivery (not a new dashboard) is the correct mechanism for reducing gate decision latency at DFW. Network rollout proceeds only after 4-week pilot results are reviewed.

---

## ❌ VIOLATION Example

> "Build full IROP automation: automated gate reassignment, automated crew swap recommendations, automated passenger rebooking, and push notifications for all 350 stations."

**Why this violates PRD-5.1:**
- Hypothesis not tested at minimum scale before network investment.
- Multiple assumptions bundled: notification delivery + automated crew logic + rebooking integration.
- If any one assumption is wrong, the entire system fails and the root cause is unclear.
- Correct approach: test notification delivery alone at 5 gates before automating anything.
