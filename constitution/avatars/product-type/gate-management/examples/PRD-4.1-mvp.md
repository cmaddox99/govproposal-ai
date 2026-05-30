---
laws: [PRD-4.1]
avatar: [gate-management]
title: MVP Scope Discipline — Gate Management Platform
---

# PRD-4.1: MVP Scope Discipline

**Law Reference:** [PRD-4.1: MVP & Product-Market Fit](../../../../laws/product/roadmap.md)
**Avatar:** gate-management
**Status:** Experimental — pilot scope and cohort criteria require validation with
product owner and station operations lead before Sprint 1

---

## MVP Principle for Gate Management

The Gate Management Platform serves a safety-adjacent, FAA/TSA/CBP-regulated
operational environment. A failure at one gate during a pilot is recoverable.
A failure that has silently propagated across 300 gates is not.

**The non-negotiable rollout law for this domain:**
> Single gate → hub pilot → network. Every time. No skipping.

The smallest useful slice is the one that gives a gate agent — or an ops controller,
or an FLC — a clear, actionable signal in the decision window. Not a dashboard.
Not a summary report. An actionable signal that arrives before the window closes.

---

## Pilot Patterns by Domain

### 🖥️ DSS — Display Staleness Reduction

**Hypothesis:** Reducing the AOC → DisplayHub → GIDS render latency from [baseline]
to ≤5 seconds eliminates the class of boarding errors where gate agents act on stale
flight status.

**Pilot scope (Phase 1):**
- One display type: GIDS (gate information display) only — not FIDS, BIDS, or WIDS
- One gate: a single high-volume departure gate at DFW Concourse C
- Duration: 2 departure banks (≈14 days)

**Risk controls:**
- GIDS change is display-only — no changes to AOC event pipeline or DCS in Phase 1
- Fallback: if staleness regression is detected, rollback to previous DisplayHub build
  within one deployment cycle
- Agent debrief after each bank: "Did the display give you information you trusted?"

**Hub pilot gate (Phase 2):**
Requires Phase 1 result: measured staleness ≤5 seconds at pilot gate AND zero agent
incidents attributable to stale display during pilot period.

**Network rollout gate (Phase 3):**
Requires Phase 2 result across full DFW Concourse C with no new safety/compliance
incidents.

---

### 🛂 Biometrics — Boarding Throughput and Non-Match Rate

**Hypothesis:** Surfacing structured reason codes on every non-match event reduces
gate agent manual-check dwell time and increases biometric boarding throughput by
≥10% within 30 days.

**Pilot scope (Phase 1):**
- One departure gate at DFW (existing biometric-enabled gate)
- Duration: 30 days of departure operations

**Risk controls:**
- Reason code is additive — no change to match threshold or enrollment logic in Phase 1
- Opt-out path audit: confirm opt-out is visible and accessible at pilot gate before
  Phase 1 begins (this is a pre-condition, not a Phase 1 deliverable)
- CBP notification: confirm threshold unchanged (no CBP notification required for
  reason code surfacing)

**Decision gate before Phase 2 (hub):**
1. Reason code coverage ≥ 99% of non-match events
2. Agent dwell time on non-match events: measurably shorter (threshold set at Sprint 0)
3. No increase in false-positive board events during pilot
4. Opt-out rate stable or improved (not suppressed by UI change)

---

### 🧳 Carry-On Compliance — Policy Propagation

**Hypothesis:** Automated rule version propagation with agent-visible version number
reduces policy inconsistency across gates and eliminates the class of incidents where
an agent enforces an outdated carry-on rule.

**Pilot scope (Phase 1):**
- Admin UI rule change → automated propagation to gates — pilot at one station
- Version number and timestamp visible to gate agent on scanner UI
- Duration: 30 days, covering at least one live policy change event

**Risk controls:**
- Propagation is additive (adds version visibility, does not change bag matrix logic)
- Rollback: if propagation failure is detected, gate falls back to last confirmed version
  (never to an undefined state)
- Override audit: confirm override requires supervisor auth at pilot station before Phase 1

**Decision gate before Phase 2 (hub):**
1. Policy propagation time: ≤60 seconds from admin change to all pilot-station gates
2. Gate-check rate stable or improved (no unintended policy tightening from rule versioning)
3. Override rate and supervisor auth rate both measurable from audit log

---

### 💬 Connect Me — Alert Latency and FLC Load Data

**Hypothesis:** Push-only flight event alerts reduce the time from AOC event to
agent-aware-and-acting to ≤30 seconds; surfacing load plan version and timestamp
on every FLC task card eliminates the class of incidents where an FLC approves a
stale plan.

**Pilot scope (Phase 1):**
- Gate change alert (push) and FLC load plan task card (version + timestamp) only
- One hub (DFW) — gate agents and FLC team at that hub
- Duration: 2 departure banks

**Risk controls:**
- FLC version surfacing is read-only — no changes to load control system
- Push alert change: validate Teams delivery receipt rate ≥ 99% before expanding
- Fallback: radio communication protocol documented and available throughout pilot

**Decision gate before Phase 2:**
1. Alert latency: AOC event → Teams agent-read ≤30 seconds at 95th percentile
2. FLC task card: version and timestamp visible on 100% of load plan tasks
3. Unread alert rate: measurably lower than pre-pilot baseline
4. Zero incidents where gate agent missed a gate change during pilot period
