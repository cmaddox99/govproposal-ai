---
avatar: avatar-product-gate-management
law: BUS-2.2
title: "Control Framework Law"
---

# BUS-2.2 — Control Framework Law: Gate Management Application

**What this law requires:** Controls must be documented, mapped to requirements, and enforced in code — not just in policy documents. Every control has a test that proves it works.

---

## Control Register — Gate Management

### Control GM-C1: Tarmac Timer Visibility
- **Requirement:** DOT 14 CFR Part 259 — 3hr/4hr tarmac hard limits
- **Control:** Timer always rendered in primary gate agent UI viewport; never in a tab, modal, or settings screen
- **Test:** UI automation — resize viewport to minimum supported size, assert timer is still visible without scroll
- **Override:** None — timer cannot be hidden by any agent action or system state

### Control GM-C2: Biometric Match Threshold
- **Requirement:** CBP Biometric Exit — operator-configurable, CBP notification on change
- **Control:** Threshold in config (not code); change requires supervisor role; triggers audit event + CBP notification
- **Test:** Attempt threshold change with agent role → assert 403; supervisor role → assert audit event logged + notification queued
- **Override:** Supervisor-only; every change logged with previous value, new value, actor, timestamp

### Control GM-C3: Carry-On Agent Override Authorization
- **Requirement:** DOT Consumer Protection — carry-on policy enforced consistently
- **Control:** Agent override of bag matrix decision requires supervisor authorization token before it can be saved
- **Test:** Attempt override without supervisor token → assert blocked; override with token → assert audit log entry with supervisor ID
- **Override:** Supervisor must provide time-limited authorization token (≤15 min TTL)

### Control GM-C4: Biometric Opt-Out Availability
- **Requirement:** CBP Biometric Exit — opt-out available to all passengers
- **Control:** Opt-out button rendered at same visual weight as boarding confirmation
- **Test:** Accessibility audit — opt-out reachable within 2 taps from boarding screen at all times
- **Override:** None — opt-out must never be suppressed

### Control GM-C5: Bag Matrix Rule Propagation
- **Requirement:** Policy consistency — all gates enforce current rules
- **Control:** Rule version stamped on every compliance decision; propagation SLA ≤60 seconds
- **Test:** Update rule in admin UI → measure propagation time across 3 test gate endpoints → assert ≤60s
- **Override:** None — stale rules flagged to agent (staleness banner) until propagation confirmed
