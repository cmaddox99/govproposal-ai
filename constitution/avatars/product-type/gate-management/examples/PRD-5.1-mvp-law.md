---
avatar: avatar-product-gate-management
law: PRD-5.1
title: "MVP Law"
---

# PRD-5.1 — MVP Law: Gate Management Application

**What this law requires:** MVPs shall be the smallest experiment to validate the core hypothesis — not a crappy first version, but a deliberate learning vehicle. Single gate before hub; one hub before network.

---

## Gate Management MVP Scope Ladder

### DSS — Digital Signage

| Stage | Scope | Hypothesis | Stop Signal |
|---|---|---|---|
| Gate pilot | 1 display type (GIDS) at 1 gate — DFW A15 | Staleness drops to ≤5s from baseline | Staleness still >5s after 2-week run |
| Hub pilot | All GIDS at DFW Concourse A (20 gates) | p99 staleness ≤5s under real event volume | DLQ events >1% of total events |
| Network rollout | Full GIDS network → FIDS → BIDS | Ops controller decision speed improves | Blocked until GIDS NPS >4.0 |

**MVP Rule:** GIDS only in Stage 1. No FIDS, BIDS, WIDS until GIDS hypothesis validated.

### Biometrics — Touchless Boarding

| Stage | Scope | Hypothesis | Stop Signal |
|---|---|---|---|
| Gate pilot | 1 departure gate — DFW A15, domestic only | Throughput ≥ manual scan (≥10 pax/min) | Throughput <9 pax/min after 2-week run |
| Concourse pilot | Full Concourse A — DFW | Match rate ≥98%; opt-out rate stable | Opt-out rate >20% |
| Hub rollout | Full DFW → ORD → MIA | CBP compliance maintained | Any TSA/CBP compliance finding |

**MVP Rule:** One domestic gate only in Stage 1. No international until CBP notification process confirmed.

### Carry-On Baggage

| Stage | Scope | Hypothesis | Stop Signal |
|---|---|---|---|
| Gate pilot | 1 gate agent, 1 gate — DFW A15 | Decision time ≤45s; consistent application | Disputes >10% of decisions |
| Station pilot | All gate agents at DFW | Rule version consistency (0 stale-rule incidents) | Any stale-rule incident post-SLA validation |
| Hub rollout | Full DFW | Gate-check rate aligns with policy intent | Override rate >15% |

### Connect Me

| Stage | Scope | Hypothesis | Stop Signal |
|---|---|---|---|
| FLC pilot | FLC workflow at 1 hub — DFW | Time-from-event to FLC-aware ≤90s | Time >120s after 2-week run |
| Gate agent pilot | Gate agent alerts at DFW | Agent acts on alert within 2min, 90% of the time | Action rate <80% |
| Hub rollout | All airport teams at DFW → ORD | Teams adoption ≥80% | Adoption <60% after 4 weeks |

---

## Gate Decision Before Each Stage Advance

All of these must be true before advancing from pilot to hub:
1. Hypothesis validated (measured, not assumed) — evidence filed in `hangar-ai-specs/`
2. Stop signal NOT triggered
3. Stakeholder sign-off: Product Owner + Ops Lead
4. No open P1/P2 compliance issues from current pilot stage
