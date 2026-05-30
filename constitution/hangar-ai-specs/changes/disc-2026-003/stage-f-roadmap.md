---
# Stage F — Roadmap Lock — Product Discovery v2.0.0
# Governed by: PRD-4.1, PRD-4.2, ENG-11.1, BUS-7.1, ENG-13.1, ENG-13.3

id: disc-2026-003
spec_id: disc-2026-003
type: discovery
stage: F
stage_label: Roadmap Lock
status: IN_PROGRESS
created: 2026-04-18
branch: disc-2026-003-gate-management-modernization
workflow: product-discovery-stage-a-f
workflow_version: "2.0.0"
skill: skill-product-discovery-orchestration
title: "Gate Management Modernization — Roadmap Lock"
template_version: "1.0.0"
template_path: "tools/templates/product-discovery/stage-f-roadmap.md"
avatar_path: "avatars/technology/java-spring/"

mode: Exploratory
tier: Tier 2

laws:
  - PRD-4.1
  - PRD-4.2
  - ENG-11.1
  - BUS-7.1
  - ENG-13.1
  - ENG-13.3

laws_applied:
  - PRD-4.1
  - PRD-4.2
  - ENG-11.1
  - BUS-7.1
  - ENG-13.1
  - ENG-13.3

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
    status: done
  - id: F
    label: Roadmap Lock
    status: active

gates:
  entry:
    status: met
    description: >
      Stage E Metric Rebaseline approved. PMF targets defined and measurability
      confirmed. Stage F roadmap lock initiated 2026-04-18.
  exit:
    status: pending
    description: >
      Awaiting roadmap approved, Slice 1 brief complete, PDF generated (ENG-13.3).
      Human browser review and BUS-7.1 audit event required to close discovery.

stakeholder:
  approver: "Adeel Ali"
  title: "Architect & Co-founder"
  affirm: false
  note: "Pending human-in-loop review — confirm in browser before advancing"

spec_artifacts:
  - icon: "📄"
    filename: "stage-f-roadmap.md"
    status: "DRAFTED"
  - icon: "🌐"
    filename: "stage-f-roadmap.html"
    status: "PENDING"

avatars:
  - avatar-technology-java-spring

roadmap:
  slices:
    - id: slice-1
      title: "Event-Driven Gate-Change Service (Spring Boot + Kafka)"
      description: >
        Greenfield Spring Boot 3 / Java 21 replacement for GateMgr core.
        Publishes gate-change domain events to FLIFO Kafka topic on every
        assignment mutation. Strangler-fig cutover from WebSphere polling API.
        TDD-first; coverage gate ≥ 80%; SonarQube quality gate PASSED.
      status: proposed
    - id: slice-2
      title: "Crew Notification Integration"
      description: >
        CrewNotify Kafka consumer subscribes to gate-change topic.
        Consumer batching tuned for < 90s p95 latency SLA.
        Gate agents receive push notification on crew tablet within 90s.
        CrewNotify consumer UAT with DFW dispatcher team.
      status: proposed
    - id: slice-3
      title: "Passenger App Real-Time Push + Ground Ops Integration"
      description: >
        PassengerPush consumer connects to gate-change Kafka topic.
        Passenger push notification delivered within 60s of gate change.
        GroundOps tablet REST polling replaced with Server-Sent Events
        feed backed by Kafka consumer. All 3 downstream consumers migrated.
      status: proposed

exit_checklist:
  - title: "Outcome framing complete — Now/Next/Later roadmap locked"
    laws: ["PRD-4.1", "PRD-4.2"]
    status: pend
  - title: "Executive approval obtained — named Director+ sign-off"
    laws: ["PRD-2.5"]
    status: pend
  - title: "Implementation proposal complete with team, cost, timeline"
    laws: ["PRD-4.1"]
    status: pend
  - title: "stage-f-roadmap.md rendered via aa-artifact-render and APPROVED in browser"
    laws: ["ENG-13.1"]
    status: pend
  - title: "PDF export generated per ENG-13.3"
    laws: ["ENG-13.3"]
    status: pend
  - title: "BUS-7.1 audit event filed — Stage F → Complete"
    laws: ["BUS-7.1"]
    status: pend

audit_log:
  - event: "Stage F — Roadmap Lock initiated"
    actor: "Adeel Ali"
    role: "Architect & Co-founder"
    system: "GitHub Copilot CLI"
    timestamp: "2026-04-18T10:15:00Z"
    outcome: "IN_PROGRESS"
  - event: "Stage F → Complete"
    actor: "Adeel Ali"
    role: "Architect & Co-founder"
    system: "GitHub Copilot CLI"
    timestamp: "2026-04-18T10:15:00Z"
    outcome: "AWAITING"

---

# Stage F Roadmap Lock: Gate Management Modernization

---

## Outcome Framing (PRD-4.1)

| Outcome | Metric | Target | Timeline |
|---------|--------|--------|----------|
| Eliminate gate-change propagation delay | p95 latency FLIFO event → consumer receipt | < 60s passenger; < 90s crew | Q3 2026 (end of Slice 2) |
| Reduce gate-change departure delay attribution | % gate-change delays coded to notification lag | < 5% (from 23% baseline) | Q4 2026 (2 months post-Slice 3) |
| Improve ops team satisfaction with gate tooling | Ops NPS (gate agents + dispatchers) | ≥ 55 (from 22 baseline) | Q4 2026 post-launch survey |
| Eliminate Java 8 / WebSphere security exposure | SonarQube critical violations | 0 (from 3 baseline) | Q2 2026 (end of Slice 1) |

---

## Roadmap — Now / Next / Later (PRD-4.2)

### Now (0–8 weeks) — Slice 1: Event-Driven Gate-Change Service

| Initiative | Vertical Slice | Effort Estimate | Owner |
|-----------|---------------|:---------------:|-------|
| Greenfield Spring Boot 3 / Java 21 GateMgr replacement | Publish gate-change domain events to FLIFO Kafka topic on every gate assignment mutation; strangler-fig cutover from WebSphere; ≥ 80% branch coverage; SonarQube gate PASSED | L | Platform Engineering |
| Kafka topic schema design | Define and publish `gate.change.v1` Avro schema; reviewed by FLIFO, CrewNotify, and PassengerPush teams | S | Platform Engineering + FLIFO Team |
| FAA audit log integration | Persist immutable gate-change event log to meet FAA 7-year retention requirement | S | Platform Engineering |

### Next (8–16 weeks) — Slice 2: Crew Notification Integration

| Initiative | Vertical Slice | Effort Estimate | Dependencies |
|-----------|---------------|:---------------:|-------------|
| CrewNotify Kafka consumer for gate changes | Subscribe to `gate.change.v1`; tune batching for < 90s p95 latency; push to crew tablet | M | Slice 1 Kafka topic live |
| Crew notification UAT at DFW | Gate agent and dispatcher UAT with real gate-change events; latency instrumented | S | CrewNotify consumer deployed to staging |
| Consumer SLA monitoring | OpenTelemetry dashboard for p95 latency; PagerDuty alert on SLA breach | S | Kafka consumer deployed |

### Later (16–24 weeks) — Slice 3: Passenger Push + Ground Ops

| Initiative | Why Later | Prerequisite |
|-----------|----------|-------------|
| PassengerPush Kafka consumer + < 60s passenger notification | Depends on stable Slice 1 schema and Slice 2 consumer patterns proven in production | Slice 2 in production for ≥ 4 weeks |
| GroundOps tablet Server-Sent Events integration | Ground ops integration has wider stakeholder coordination (ramp, equipment scheduling); scoped after crew integration proven | Slice 2 UAT complete; GroundOps team sprint capacity confirmed |
| Full polling API decommission | WebSphere polling API retired only after all 3 consumers migrated and monitored for 30 days | Slice 3 deployed and all consumers on Kafka |

---

## Implementation Proposal

> The implementation proposal scaffolds the next workflow phase (legacy-rescue-rewrite).

| Field | Value |
|-------|-------|
| Implementation ID | `impl-2026-gate-mgr-001` |
| Workflow | legacy-rescue-rewrite |
| First vertical slice | Slice 1 — Greenfield Spring Boot 3 / Java 21 gate-change service publishing `gate.change.v1` Kafka events; strangler-fig cutover from WebSphere GateMgr |
| Estimated effort | L (~8 weeks, 2 engineers) |
| Success criteria | p95 FLIFO → Kafka publish latency < 5s; SonarQube quality gate PASSED; ≥ 80% branch coverage; FAA audit log operational; zero polling API regressions during cutover |
| Implementation spec | `hangar-ai-specs/changes/impl-2026-gate-mgr-001/PROPOSAL.md` |

---

## Executive Approval

> **Required reviewer:** Executive Sponsor + Product Owner

| Field | Value |
|-------|-------|
| **Approver Name** | Adeel Ali |
| **Role / Title** | Architect & Co-founder |
| **Approval Date** | Pending |
| **Approval Form** | Browser review (human-in-loop) |
| **Conditions** | Kafka topic schema reviewed by FLIFO platform team before Slice 1 sprint start |
| **Status** | ⬜ Pending |
