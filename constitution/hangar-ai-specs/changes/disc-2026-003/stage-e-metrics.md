---
# Stage E — Metric Rebaseline — Product Discovery v2.0.0
# Governed by: PRD-6.1, ENG-10.1, BUS-7.1, ENG-13.1

id: disc-2026-003
spec_id: disc-2026-003
type: discovery
stage: E
stage_label: Metric Rebaseline
status: IN_PROGRESS
created: 2026-04-18
branch: disc-2026-003-gate-management-modernization
workflow: product-discovery-stage-a-f
workflow_version: "2.0.0"
skill: skill-product-discovery-orchestration
title: "Gate Management Modernization — Metric Rebaseline"
template_version: "1.0.0"
template_path: "tools/templates/product-discovery/stage-e-metrics.md"
avatar_path: "avatars/technology/java-spring/"

mode: Exploratory
tier: Tier 2

laws:
  - PRD-6.1
  - ENG-10.1
  - BUS-7.1
  - ENG-13.1

laws_applied:
  - PRD-6.1
  - ENG-10.1
  - BUS-7.1
  - ENG-13.1

stages:
  - id: A
    label: Initialize
    status: done
  - id: B
    label: Field Study
    status: done
  - id: C
    label: Code Evidence
    status: done
  - id: D
    label: Validation
    status: done
  - id: E
    label: Metrics
    status: active
  - id: F
    label: Roadmap Lock
    status: locked

gates:
  entry:
    status: met
    description: >
      Stage D Validation approved. All blockers have explicit owners and paths.
      DVFT matrix complete. Stage E metric rebaseline initiated 2026-04-18.
  exit:
    status: pending
    description: >
      Awaiting metrics spec complete with measurability confirmed.
      Human browser review and BUS-7.1 audit event required before Stage F.

stakeholder:
  approver: "Adeel Ali"
  title: "Architect & Co-founder"
  affirm: false
  note: "Pending human-in-loop review — confirm in browser before advancing"

spec_artifacts:
  - icon: "📄"
    filename: "stage-e-metrics.md"
    status: "DRAFTED"
  - icon: "🌐"
    filename: "stage-e-metrics.html"
    status: "PENDING"

avatars:
  - avatar-technology-java-spring

exit_checklist:
  - title: "AARRR success metrics defined for all 5 framework dimensions"
    laws: ["PRD-6.1"]
    status: pend
  - title: "PMF definition documented with quantified threshold"
    laws: ["PRD-6.1"]
    status: pend
  - title: "Leading vs lagging indicators distinguished"
    laws: ["PRD-6.1"]
    status: pend
  - title: "Measurement plan documented — instrumentation, owner, cadence"
    laws: ["PRD-6.1"]
    status: pend
  - title: "All metrics confirmed measurable before Stage F"
    laws: ["PRD-6.1"]
    status: pend
  - title: "stage-e-metrics.md rendered via aa-artifact-render and APPROVED in browser"
    laws: ["ENG-13.1"]
    status: pend
  - title: "BUS-7.1 audit event filed — Stage E → F transition"
    laws: ["BUS-7.1"]
    status: pend

audit_log:
  - event: "Stage E — Metric Rebaseline initiated"
    actor: "Adeel Ali"
    role: "Architect & Co-founder"
    system: "GitHub Copilot CLI"
    timestamp: "2026-04-18T10:00:00Z"
    outcome: "IN_PROGRESS"
  - event: "Stage E → F"
    actor: "Adeel Ali"
    role: "Architect & Co-founder"
    system: "GitHub Copilot CLI"
    timestamp: "2026-04-18T10:00:00Z"
    outcome: "AWAITING"

---

# Stage E Metric Rebaseline: Gate Management Modernization

---

## Success Metrics (AARRR Framework)

| Stage | Metric | Baseline | Target | PMF Signal |
|-------|--------|----------|--------|------------|
| Acquisition | Services migrated from polling to event-driven gate-change feed | 0 of 3 downstream consumers | 3 of 3 (CrewNotify, PassengerPush, GroundOps) | All 3 consumers on Kafka topic — Slice 3 complete |
| Activation | p95 gate-change propagation latency (FLIFO event → downstream consumer receipt) | 4.7 min avg (280s) | < 60s passenger push; < 90s crew notification | p95 latency < 60s for PassengerPush sustained 30 days |
| Retention | Gate-change delay attribution rate (% of gate-change delays coded to notification lag) | 23% | < 5% | < 5% for 2 consecutive months post-Slice 3 |
| Revenue | Cost savings from reduced gate-change delays (crew overtime + compensation) | $4.2M/year annualised | $3.2M/year reduction (> 75% of delay cost eliminated) | $800K+ savings in first full quarter post-launch |
| Referral | Ops team NPS for gate-change communication tooling (gate agents + dispatchers) | 22 (Q1 2026 ops survey) | ≥ 55 | NPS ≥ 55 sustained in 2 consecutive quarterly surveys |

---

## PMF Definition

Product-market fit for Gate Management Modernization is defined as:

1. **Propagation latency** p95 < 60 seconds for passenger push and < 90 seconds for crew notification, sustained for 30 consecutive days post-Slice 2 completion.
2. **Delay attribution rate** < 5% of gate-change departure delays coded to notification lag, measured over 2 consecutive months post-Slice 3.
3. **Ops NPS ≥ 55** from gate agents and dispatchers in the first post-launch quarterly survey.

All three signals must be met simultaneously. Partial achievement does not constitute PMF.

---

## Leading vs. Lagging Indicators

| Type | Indicator | Measurement Frequency | Owner |
|------|-----------|:---------------------:|-------|
| Leading | p95 FLIFO event → Kafka topic publish latency (new service) | Real-time dashboard; daily review | Platform Engineering |
| Leading | p95 Kafka topic → CrewNotify consumer receipt latency | Real-time dashboard; daily review | CrewNotify Team |
| Leading | p95 Kafka topic → PassengerPush receipt latency | Real-time dashboard; daily review | Passenger App Team |
| Lagging | Gate-change delay attribution rate (DOT delay code analysis) | Monthly (aligned to DOT reporting cycle) | Airport Operations |
| Lagging | Ops NPS for gate-change communication | Quarterly (ops survey) | Product / Ops Excellence |
| Lagging | Cost savings from gate-change delay reduction | Quarterly (finance review) | Finance / Ops Excellence |

---

## Measurement Plan

| Metric | Tool / Source | Collection Method | Frequency | Owner |
|--------|-------------|-------------------|:---------:|-------|
| Propagation latency (FLIFO → consumer) | Kafka consumer lag metrics + OpenTelemetry traces | Automated instrumentation in new gate-change service and consumers | Real-time | Platform Engineering |
| Gate-change delay attribution rate | DOT delay code dataset + ops-control incident log | Automated ETL pipeline from ops DB to data warehouse | Monthly | Airport Operations Analytics |
| Ops NPS | Qualtrics ops survey | Quarterly survey distributed to gate agents and dispatchers | Quarterly | Product / Ops Excellence |
| Cost savings | Finance reporting system | Derived from delay-minutes × average cost; validated by finance quarterly | Quarterly | Finance |
| Service test coverage | SonarQube (CI gate) | Automated on every PR merge | Per commit | Engineering |

---

## Measurability Confirmation

- [x] All metrics have a defined baseline (even if baseline = 0)
- [x] All metrics have a defined target
- [x] All metrics have a named owner
- [x] Collection tools/sources are identified and accessible
- [x] PMF definition is quantitative and testable
