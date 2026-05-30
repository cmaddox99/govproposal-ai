---
laws: [PRD-2.5]
avatar: [gate-management]
title: Stage-Gate Review — Gate Management Platform
---

# PRD-2.5: Stage-Gate Review

**Law Reference:** [PRD-2.5: Stage-Gate Review](../../../../laws/product/discovery.md)
**Avatar:** gate-management
**Status:** Active — stage gates are non-negotiable for all four Gate Management domains

Each product increment passes through: **Problem Gate → Solution Gate → Build Gate →
Launch Gate**. No gate may be skipped. See
[PRD Article II](../../../../laws/product/discovery.md) for full law text.

---

## Application to Gate Management Platform

The four-gate model applies uniformly across all Gate Management sub-domains (DSS,
Biometrics, Carry-On, Connect Me). The regulatory stakes of this domain — FAA,
TSA, CBP, DOT — mean that a skipped gate is not a process shortcut; it is a compliance
exposure. A feature that reaches production without a Build Gate review is a feature
that may not have been validated against the biometric opt-out requirement, the tarmac
timer visibility rule, or the bag matrix audit log mandate.

---

## Gate Definitions for This Domain

### Problem Gate
Exit criteria specific to Gate Management:

- [ ] Root failure mode identified and measured (decision latency quantified per domain)
- [ ] Impacted persona(s) confirmed (gate agent, FLC, biometrics supervisor — not assumed)
- [ ] Regulatory constraint mapped: which FAR/TSA/CBP/DOT rule governs this feature space?
- [ ] Baseline metric captured: staleness / throughput / override rate / alert latency
- [ ] Problem statement approved by product owner before any solution work begins

### Solution Gate
Exit criteria specific to Gate Management:

- [ ] Solution framed against measured baseline — not against intuition or competitor feature
- [ ] Non-negotiable patterns honored: opt-out visible, tarmac timer non-suppressible,
  rule version logged, push not poll
- [ ] Regulatory compliance confirmed: which standard (CBP, TSA, DOT) applies and how
  is the solution compliant?
- [ ] Anti-patterns reviewed and ruled out (see `manifest.yaml → anti_patterns`)
- [ ] Rollout plan specifies: single gate pilot → hub pilot → network rollout (no skipping)
- [ ] Solution approved by product owner and compliance stakeholder before Build Gate

### Build Gate
Exit criteria specific to Gate Management:

- [ ] Executable spec written: domain context (flight_id, gate_id, agent_id, timestamp)
  present in all audit log entries
- [ ] TDD cycle begun: test written and failing before implementation
- [ ] Coverage target ≥ 90% for domain logic; mutation score ≥ 70%
- [ ] Security review: PII (biometric templates, PNR data) confirmed not in operational logs
- [ ] Event-driven integration pattern confirmed: no polling of upstream AOC/DCS systems
- [ ] Single-gate pilot deployment plan reviewed and approved before Build Gate exit

### Launch Gate
Exit criteria specific to Gate Management:

- [ ] Single-gate pilot results reviewed against Problem Gate baseline metric
- [ ] No new safety or compliance incidents attributable to the feature during pilot
- [ ] Biometric opt-out path (if applicable) confirmed operational in pilot
- [ ] Tarmac timer visibility (if applicable) confirmed non-suppressible in pilot
- [ ] Rollback plan documented and tested: reverting feature must not leave audit gaps
- [ ] Hub rollout approved by product owner with pilot evidence in hand
- [ ] Network rollout approval is a separate gate — hub pilot results required first
