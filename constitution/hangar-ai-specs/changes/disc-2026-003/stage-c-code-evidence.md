---
# Stage C — Code Evidence — Product Discovery v2.0.0
# Governed by: ENG-3.1, ENG-6.7, PRD-3.2, BUS-7.1, ENG-13.1

id: disc-2026-003
spec_id: disc-2026-003
type: discovery
stage: C
stage_label: Code Evidence
status: IN_PROGRESS
created: 2026-04-18
branch: disc-2026-003-gate-management-modernization
workflow: product-discovery-stage-a-f
workflow_version: "2.0.0"
skill: skill-product-discovery-orchestration
title: "Gate Management Modernization — Code Evidence"
template_version: "1.0.0"
template_path: "tools/templates/product-discovery/stage-c-code-evidence.md"
avatar_path: "avatars/technology/java-spring/"

mode: Exploratory
tier: Tier 2

laws:
  - ENG-3.1
  - ENG-6.7
  - PRD-3.2
  - BUS-7.1
  - ENG-13.1

laws_applied:
  - ENG-3.1
  - ENG-6.7
  - PRD-3.2
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
    status: active
  - id: D
    label: Validation
    status: locked
  - id: E
    label: Metrics
    status: locked
  - id: F
    label: Roadmap Lock
    status: locked

gates:
  entry:
    status: met
    description: >
      Stage B Field Study approved. ≥3 validated user insights confirmed.
      Competitive landscape documented. Stage C codebase assessment initiated 2026-04-18.
  exit:
    status: pending
    description: >
      Awaiting codebase assessment complete with no unreviewed critical findings.
      Human browser review and BUS-7.1 audit event required before Stage D.

stakeholder:
  approver: "Adeel Ali"
  title: "Architect & Co-founder"
  affirm: false
  note: "Pending human-in-loop review — confirm in browser before advancing"

spec_artifacts:
  - icon: "📄"
    filename: "stage-c-code-evidence.md"
    status: "DRAFTED"
  - icon: "🌐"
    filename: "stage-c-code-evidence.html"
    status: "PENDING"

avatars:
  - avatar-technology-java-spring

exit_checklist:
  - title: "Repository assessment complete — all active services catalogued"
    laws: ["ENG-11.1"]
    status: pend
  - title: "Architecture overview documented with bounded contexts"
    laws: ["ENG-3.2"]
    status: pend
  - title: "Domain model extracted per ENG-6.7"
    laws: ["ENG-6.7"]
    status: pend
  - title: "Tech debt inventory completed per ENG-3.1"
    laws: ["ENG-3.1"]
    status: pend
  - title: "Compliance and regulatory constraints documented"
    laws: ["BUS-4.1", "BUS-7.1"]
    status: pend
  - title: "Build vs Buy vs Extend recommendation made"
    laws: ["ENG-11.1"]
    status: pend
  - title: "stage-c-code-evidence.md rendered via aa-artifact-render and APPROVED in browser"
    laws: ["ENG-13.1"]
    status: pend
  - title: "BUS-7.1 audit event filed — Stage C → D transition"
    laws: ["BUS-7.1"]
    status: pend

audit_log:
  - event: "Stage C — Code Evidence initiated"
    actor: "Adeel Ali"
    role: "Architect & Co-founder"
    system: "GitHub Copilot CLI"
    timestamp: "2026-04-18T09:30:00Z"
    outcome: "IN_PROGRESS"
  - event: "Stage C → D"
    actor: "Adeel Ali"
    role: "Architect & Co-founder"
    system: "GitHub Copilot CLI"
    timestamp: "2026-04-18T09:30:00Z"
    outcome: "AWAITING"

---

# Stage C Code Evidence: Gate Management Modernization

---

## Repository Assessment

| Attribute | Value |
|-----------|-------|
| Repository | `aa-ops/gate-mgr` (internal GitLab) |
| Primary language(s) | Java 8, Spring MVC 4.3, Hibernate 5 |
| LOC (approx) | ~18,400 lines (excluding generated sources) |
| Last commit | 2025-11-14 (no active development in 5 months) |
| Active contributors (90d) | 1 (maintenance-only; on rotation) |
| Test coverage (branch) | 12% |
| SonarQube quality gate | FAILED — 3 critical violations |

---

## Architecture Overview

GateMgr is a monolithic Spring MVC web application deployed on WebSphere 9. It owns the gate-assignment lifecycle — creation, modification, and status transitions — and exposes a REST polling API consumed by downstream services. There is no event emission; all consumers poll `GET /api/gates/{flightId}` on 5-minute intervals.

**Bounded contexts affected:**
- **GateMgr** — gate assignment CRUD and status engine (this service)
- **FLIFO** — flight information object bus (Kafka-based; does not currently receive gate events)
- **CrewNotify** — crew scheduling push notification platform (Kafka consumer; ready for gate-change topic)
- **PassengerPush** — AA mobile app notification service (Kafka consumer; pending gate-change feed)
- **GroundOps** — ramp and equipment coordination tablet app (REST polling; candidate for event upgrade)

---

## Domain Model Extraction (ENG-6.7)

| Entity | Bounded Context | Relationships | Notes |
|--------|----------------|--------------|-------|
| GateAssignment | GateMgr | Has one Flight, has one Gate, has one Status | Core aggregate — immutable after departure |
| GateChangeEvent | GateMgr (proposed) | Produced by GateAssignment on modification | Does not exist today; must be introduced |
| Flight | FLIFO | Referenced by GateAssignment | FLIFO is source of truth for flight identity |
| Gate | GateMgr | Has one Terminal, has one Airport | Static master data; updated via ops admin UI |
| CrewNotification | CrewNotify | Triggered by GateChangeEvent | Kafka consumer; topic subscription needed |
| PushNotification | PassengerPush | Triggered by GateChangeEvent | Kafka consumer; topic subscription needed |

---

## Tech Debt Inventory (ENG-3.1)

| Item | Severity (H/M/L) | Impact | Remediation Path |
|------|:-:|---|---|
| Java 8 (EOL) — no security patches since Sep 2023 | H | CVE exposure; blocks JVM-level security updates | Migrate to Java 21 LTS in Spring Boot 3.x rewrite |
| Zero integration tests; 12% branch coverage | H | Regression risk is unquantified; any change is high-risk | TDD-first implementation in new service; coverage gate ≥80% |
| Synchronous polling API as sole event mechanism | H | Structural cause of 4–7 min propagation delay | Replace with Kafka event publication on gate-change |
| WebSphere 9 deployment (EoS 2025) | M | Platform lifecycle risk; blocking cloud migration | New service targets Kubernetes / EKS |
| No domain event log — no audit trail for gate changes | M | Cannot replay or trace gate-change history | Event sourcing on new service; FLIFO event log |
| Hard-coded airport configuration in properties files | L | Configuration drift across environments | Externalise to config service |

---

## Compliance / Regulatory Constraints

| Constraint | Source | Impact on Discovery |
|-----------|--------|-------------------|
| FAA departure integrity — gate assignments must be auditable for 7 years | FAA Order 7110.65 | New service must retain immutable gate-change event log |
| TSA gate-access logging — gate changes must not bypass security zone validation | TSA Security Directive | Gate-change events must carry security-zone metadata; cannot bypass access controls |
| DOT on-time reporting — gate changes within 15 min of departure must be flagged | 14 CFR Part 234 | Event stream must include departure-proximity flag for DOT reporting pipeline |

---

## Build vs. Buy vs. Extend

| Option | Pros | Cons | Recommendation |
|--------|------|------|---------------|
| Build | Full control over event model and domain; clean Java 21 / Spring Boot 3 implementation; Kafka-native | Highest initial effort (~12 weeks for Slice 1) | ✅ Recommended |
| Buy | Vendor gate-management platforms exist (SITA AMS, Amadeus) | Vendor lock-in; integration cost; loss of AA-specific event model; multi-year contract | Not recommended |
| Extend | Faster than full rewrite; preserves existing data model | Java 8 / WebSphere constraints cannot be resolved incrementally; polling model deeply embedded; test coverage too low to safely extend | Not recommended |

**Recommended approach:** BUILD — greenfield Spring Boot 3 / Java 21 service with Kafka event publication, replacing GateMgr incrementally via strangler-fig pattern over 3 implementation slices.

---

## Critical Findings

| # | Finding | Severity | Reviewed? |
|---|---------|:--------:|:---------:|
| 1 | Java 8 EOL — active CVEs unpatched since Sep 2023 (SonarQube CVE-2023-21968, CVE-2023-21954) | H | ✅ |
| 2 | Zero integration tests — 12% branch coverage; regression risk unquantified for any change | H | ✅ |
| 3 | No gate-change event emission — polling model is the structural root cause of the propagation delay | H | ✅ |

> **Exit gate requirement:** All critical findings reviewed. No unreviewed critical findings remain.
