---
laws: [PRD-1.2]
avatar: [gate-management]
title: Problem-First Validation — Gate Management Platform
---

# PRD-1.2: Problem-First Validation

**Law Reference:** [PRD-1.2: Problem-First](../../../../laws/product/foundations.md)
**Status:** Experimental — all baselines are hypotheses until measured from production telemetry

> Every feature proposal must answer: *"What is the current measured latency, and is that the actual failure mode?"*
> Do not propose a solution until you have a measured baseline for the domain below.

---

## DSS — Digital Signage

**Problem candidate:** Gate displays show stale flight status during irregular operations.

- What is the current measured staleness (ms) from AOC event to display update — and at which layer (hand-off, consumer, render pipeline)?
- Do gate agents trust the GIDS display, or have they developed verbal workarounds that bypass it?

**Do not build until:** Baseline staleness per display type, plus one confirmed incident where staleness caused a wrong agent decision.

---

## Biometrics — Touchless Boarding

**Problem candidate:** False non-matches delay passengers and erode agent trust.

- What is the current false non-match rate (%)? Is it uniform across gates or concentrated at specific hardware/lighting conditions?
- What is boarding throughput (pax/min) biometric vs. manual scan? Is biometric actually faster?

**Do not build until:** False non-match rate baseline, confirmed agent understanding of reason codes, opt-out path usability confirmed by observation.

---

## Carry-On Baggage

**Problem candidate:** Inconsistent enforcement due to rule version lag across gates.

- What is the current gate-check rate, and does it vary across gates in ways that suggest different rule versions?
- What is the override rate? Are overrides concentrated at specific agents or policy rules?

**Do not build until:** Gate-check rate baseline, confirmed rule version visibility (or confirmed absence), propagation time measurement.

---

## Connect Me

**Problem candidate:** Flight event alerts arrive after the agent decision window closes.

- What is the current time from AOC event fire to agent-aware-and-acting (Teams read + task acknowledged)? Where is the latency — pipeline, Teams delivery, or notification visibility?
- What % of operational alerts go unread? Which alert types have the highest unread rate?

**Do not build until:** Measured alert latency baseline, unread rate by alert type, confirmed FLC load data version visibility gap.
