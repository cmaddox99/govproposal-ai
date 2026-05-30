---
# Stage A — Initialize — Product Discovery Stage A–F
# Governed by: ENG-11.2, PRD-2.1, PRD-2.5, BUS-7.1, ENG-13.1

id: disc-2026-004
spec_id: disc-2026-004
type: discovery
stage: A
stage_label: Initialize
status: APPROVED
created: 2026-04-22
branch: main
workflow: product-discovery-stage-a-f
workflow_version: "2.0.0"
skill: skill-product-discovery-orchestration
title: "Gate Management Platform — Operations Intelligence Discovery"

mode: Exploratory
tier: Tier 2

laws:
  - PRD-2.1
  - PRD-2.5
  - BUS-7.1
  - ENG-11.1
  - ENG-11.2
  - ENG-13.1

laws_applied:
  - PRD-2.1
  - PRD-2.5
  - BUS-7.1
  - ENG-13.1
  - ENG-11.1

stages:
  - id: A
    label: Initialize
    status: active
  - id: B
    label: Field Study
    status: active
  - id: C
    label: Code Evidence
    status: locked
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
      Gate Management product avatar (avatar-product-gate-management) fully validated
      and committed (Phase 6 complete, commit 635f30a, 2026-04-22). RAG recall 5/5 across
      all four sub-domains: DSS Display, Biometric Boarding, Carry-On Compliance, Connect Me.
      Three supporting tech avatars also validated: dss-event-driven, apigee-azure.
      Discovery triggered by absence of a validated problem statement — avatar intelligence
      surfaced four distinct operational failure modes requiring structured discovery before
      any solution design proceeds.
  exit:
    status: pending
    description: >
      Awaiting §Stakeholder Approval from named Director+ approver.
      Self-certification prohibited by PRD-2.5.

mode_selection:
  selected: Exploratory
  rationale: >
    No prior validated problem statement exists for Gate Management. All four sub-domain
    problem hypotheses (display staleness, biometric false non-match, carry-on rule drift,
    Connect Me alert latency) are avatar-sourced hypotheses — not field-validated. Baselines
    for staleness_ms, false non-match rate, gate-check rate, and alert delivery latency are
    explicitly flagged as UNKNOWN in the avatar use cases. Exploratory mode is required.

tier_selection:
  tier: Tier 2
  rationale: >
    Gate Management spans four bounded contexts (DSS, Biometrics, Carry-On, Connect Me),
    each backed by distinct microservice clusters. Three regulatory regimes apply
    (FAA/DOT, TSA/CBP, GDPR/CCPA). Stakeholder groups include gate agents, ramp crews,
    FLCs, station managers, ops controllers, and airline + CBP partner systems.
    Implementation will require cross-team coordination across at least three engineering
    teams and a multi-quarter timeline. All five Tier 2 rubric criteria are met.
  rubric:
    - question: Does the discovery span 3+ services or bounded contexts?
      answer: "Yes"
    - question: Are there 3+ stakeholder groups with distinct needs?
      answer: "Yes"
    - question: Does the domain involve regulatory or compliance constraints?
      answer: "Yes"
    - question: Is the expected implementation timeline > 1 quarter?
      answer: "Yes"
    - question: Does the discovery require cross-team coordination (2+ teams)?
      answer: "Yes"

stakeholder:
  approver: "Ram"
  title: "Director of Product Agility — Leader, Hangar"
  date: "2026-04-22"
  method: "In-session approval — Copilot CLI session"
  self_cert: false

avatars:
  - icon: "🎯"
    name: "avatar-product-gate-management"
    context: "Gate operations product avatar — DSS · Biometrics · Carry-On · Connect Me. RAG validated 2026-04-22. Governs PRD laws: PRD-1.2, PRD-5.1. Business laws: BUS-2.1, BUS-2.2, BUS-2.4. Engineering: ENG-6.7, ENG-6.1."
  - icon: "⚙️"
    name: "avatar-tech-dss-event-driven"
    context: "DSS DisplayHub event-driven microservices — TypeScript/Node, Java, .NET. Azure Service Bus event pipeline. RAG validated 2026-04-22."
  - icon: "🔗"
    name: "avatar-tech-apigee-azure"
    context: "Apigee API gateway + Azure cloud infrastructure — Biometrics boarding API, Carry-On apigee proxy, OAuth 2.0, Azure App Insights. RAG validated 2026-04-22."

spec_artifacts:
  - icon: "📄"
    filename: "stage-a-initialize.md"
    status: "DRAFTED"
  - icon: "🌐"
    filename: "stage-a-initialize.html"
    status: "PENDING"

exit_checklist:
  - title: "Discovery ID assigned in disc-YYYY-NNN format"
    laws: ["ENG-11.1", "PRD-2.5"]
    status: done
  - title: "stage-a-initialize.md created from template"
    laws: ["ENG-11.2", "PRD-2.5"]
    status: done
  - title: "Problem statement complete — all 4 PRD-2.1 dimensions filled"
    laws: ["PRD-2.1"]
    status: done
  - title: "Scope defined (in/out table populated)"
    laws: ["PRD-2.5"]
    status: done
  - title: "Mode declared (Exploratory) in frontmatter"
    laws: ["PRD-2.5"]
    status: done
  - title: "Tier declared (Tier 2) in frontmatter"
    laws: ["PRD-2.5"]
    status: done
  - title: "Product and Technology avatars activated and recorded"
    laws: ["PRD-2.5", "BUS-7.1"]
    status: done
  - title: "Stakeholder approval obtained from named Director+ approver"
    description: "Self-certification prohibited by PRD-2.5."
    laws: ["PRD-2.1", "PRD-2.5"]
    status: done
  - title: "stage-a-initialize.md rendered via aa-artifact-render and APPROVED in browser"
    laws: ["ENG-13.1"]
    status: done
  - title: "BUS-7.1 audit event filed — Stage A → B transition"
    laws: ["BUS-7.1"]
    status: done

audit_log:
  - event: "Stage A — Initialized"
    actor: "Amal (Copilot CLI) + Adeel Ali"
    role: "Product Coach + Discovery Sponsor"
    system: "GitHub Copilot CLI"
    timestamp: "2026-04-22T16:55:00Z"
    outcome: "IN_PROGRESS"
  - event: "Stage A — Avatar activation recorded"
    actor: "Amal (Copilot CLI)"
    role: "Product Coach"
    system: "GitHub Copilot CLI"
    timestamp: "2026-04-22T16:55:00Z"
    outcome: "3 avatars activated (product-gate-management, dss-event-driven, apigee-azure)"
  - event: "Stage A — HTML rendered and reviewed"
    actor: "Bhavita + Derek"
    role: "Product Coaches / Human-in-the-Loop Reviewers"
    system: "GitHub Copilot CLI"
    timestamp: "2026-04-22T18:54:17Z"
    outcome: "APPROVED"
  - event: "Stage A — Stakeholder approval"
    actor: "Ram"
    role: "Director of Product Agility — Leader, Hangar"
    system: "GitHub Copilot CLI"
    timestamp: "2026-04-22T18:54:17Z"
    outcome: "APPROVED"
  - event: "Stage A → B"
    actor: "Willem (Copilot CLI)"
    role: "Constitutional Architect"
    system: "GitHub Copilot CLI"
    timestamp: "2026-04-22T18:54:17Z"
    outcome: "GATE PASSED — Stage B unlocked"

findings:
  - title: "Display staleness baseline is unestablished"
    description: >
      No instrumentation exists for dss.display.staleness_ms across GIDS, FIDS, BIDS, WIDS surfaces.
      The 5,000ms AOC-to-display SLA is an operational target — not a measured baseline.
    laws: ["PRD-2.1"]
    status: pend
  - title: "Biometric false non-match rate is unmeasured"
    description: >
      The 1.5% false non-match target is a design hypothesis. No production measurement exists
      at any AA pilot gate. Boarding throughput (target ≥22 pax/min) is similarly unverified.
    laws: ["PRD-2.1"]
    status: pend
  - title: "Carry-on rule propagation and override rates are unknown"
    description: >
      Gate-check rate, override rate, and policy propagation time (target ≤60s) have no current
      measurement. Rule version compliance across station gates is unverified.
    laws: ["PRD-2.1"]
    status: pend
  - title: "Connect Me alert latency and unread rate are unbaselined"
    description: >
      Alert delivery latency (target ≤30,000ms p95) and unread alert rate (threshold >5% in 5min)
      are operational targets with no production data confirming today's actual performance.
    laws: ["PRD-2.1"]
    status: pend

problem_validation:
  dim1:
    label: "1. Problem Exists"
    text: >
      Gate operations staff — agents, ramp crews, FLCs, station managers, ops controllers —
      are making time-critical decisions (gate changes, IROPs, boarding clearances, load approvals)
      using information that may be stale, inconsistently displayed, or undelivered. Four
      documented failure patterns: (1) GIDS/FIDS not updated before agent decision window closes,
      (2) biometric non-match causing boarding line backup or undetected false positives,
      (3) carry-on decisions made against an outdated or unpropagated rule version,
      (4) Teams alerts arriving after the actionable window or remaining unread.
      Evidence source: avatar use-case READMEs, exception-path documentation, non-negotiables.
    status: warn
  dim2:
    label: "2. Problem Matters"
    text: >
      Operational risk is high across all four domains. DSS staleness carries DOT 14 CFR Part 259
      tarmac timer compliance exposure — a tarmac timer displayed incorrectly or late is a
      regulatory violation. Biometric false non-match causes boarding throughput degradation
      and potential CBP audit findings. Carry-on rule drift creates DOT consumer protection
      liability (inconsistent enforcement, denied boarding disputes). Connect Me delivery
      failure leaves ramp crews and FLCs operating on stale information during IROPs — the
      highest-consequence operational windows. Cost of inaction: regulatory findings,
      operational inefficiency, and passenger-facing disruption compounding across all four domains.
    status: warn
  dim3:
    label: "3. Problem Is Solvable"
    text: >
      Three validated tech avatars confirm the infrastructure exists. Azure Service Bus,
      Azure App Insights, Apigee OAuth 2.0, DisplayHub event consumers, and Teams bot
      integration are all operational. The engineering surface is understood. What is missing
      is instrumentation, baseline measurement, and product-defined SLAs tied to measured
      behaviour — not missing capability. This is a product intelligence and engineering
      instrumentation problem, not a greenfield build.
    status: ok
  dim4:
    label: "4. Users Will Exchange Value"
    text: >
      Gate agents, FLCs, and ramp crews are captive users — adoption is mandated, not optional.
      Station managers have direct administrative pain (rule propagation visibility gap).
      Ops controllers are motivated by compliance exposure. CBP and TSA mandate biometric
      exit programs — external adoption pressure is regulatory, not commercial.
      Willingness to change behaviour is high where the alternative is regulatory non-compliance
      or operational failure. However, usability debt (opt-out path, agent scanner UI, Teams
      card design) may create adoption friction that field study must surface.
    status: warn

---

# Discovery Proposal: Gate Management Platform — Operations Intelligence Discovery

**ID:** disc-2026-004 | **Mode:** Exploratory | **Tier:** Tier 2
**Created:** 2026-04-22 | **Discovery Sponsor:** Adeel Ali

---

## Problem Statement

> **PRD-2.1 — Problem Validation Law:** All problems MUST be validated before solution design.
> All four dimensions are required before Stage B begins.

### 1. Problem Exists

Gate operations at American Airlines relies on four interconnected systems — DSS Display, Biometric Boarding, Carry-On Compliance, and Connect Me alerts — to move information from operational sources (AOC, CBP TIS, load systems) to frontline staff in time for decisions to be made.

**The problem is decision latency and information integrity failure.** In each domain:

- **DSS Display:** Gate Information Display Systems (GIDS) and Flight Information Display Systems (FIDS) may not reflect AOC gate or flight changes within the 5-second operational SLA. Tarmac timer display compliance is at risk if the rendering pipeline lags.
- **Biometric Boarding:** False non-matches create boarding line backups. Opt-out path obscurity creates CBP compliance exposure. Biometric PII boundaries in operational logs are unverified in production.
- **Carry-On Compliance:** Gate agents may be enforcing carry-on rules against stale or unpropagated rule versions. Override paths lack consistent supervisor authentication enforcement evidence. Gate-check rate and override rate are untracked.
- **Connect Me:** Teams alerts for gate changes and FLC load approvals may arrive after the actionable decision window or go unread. No production alert latency or unread rate measurement exists.

**Who experiences it:** Gate agents, ramp crews, Flight Load Controllers (FLCs), station managers, and ops controllers — across all AA domestic and international stations with gate display infrastructure and biometric pilot programs.

### 2. Problem Matters

The cost of inaction is regulatory and operational:

- **DOT 14 CFR Part 259** tarmac timer regulations require accurate, timely display — a rendering pipeline that doesn't meet the 5s SLA is a compliance exposure, not just a UX issue.
- **TSA 49 CFR Part 1542 / CBP Biometric Exit mandate** require that opt-out is always accessible and that biometric PII retention complies with a ≤12h post-departure deletion mandate. Non-compliance is an audit finding with federal consequences.
- **DOT consumer protection regulations (14 CFR Part 259)** govern carry-on baggage disclosure and denied boarding. Inconsistent rule enforcement across gates — caused by rule version drift — creates direct liability.
- **Operational disruption compounds:** Stale displays, boarding throughput degradation, and unread alerts all cascade during IROP events — the highest-consequence operational windows where errors multiply.

Failure to address these four failure patterns means operating with unquantified compliance exposure and unmeasured operational degradation across the gate estate.

### 3. Problem Is Solvable

The technology infrastructure exists and is validated:

- Azure Service Bus event pipelines are operational for DSS and Connect Me.
- Apigee OAuth 2.0 gateway is live for Biometrics and Carry-On.
- DisplayHub consumer services are deployed and processing events.
- Teams bot integration (Connect Me) is running in production.
- Azure App Insights is available for custom metric instrumentation.

Three tech avatars (product-gate-management, dss-event-driven, apigee-azure) confirm the stack is understood and operable. The gap is **measurement and product intelligence** — not greenfield capability. SLAs exist as targets; production baselines do not.

This is a **product instrumentation and validation problem** — the engineering surface is known; what is missing is field evidence, measured baselines, and product-defined acceptance criteria tied to real data.

### 4. Users Will Exchange Value

Frontline adoption is mandated (gate agents, FLCs, ramp crews operate within AA's systems by role requirement), which removes commercial adoption friction but introduces usability adoption risk. Field study must probe:

- Whether the opt-out path on biometric podiums is actually accessible without agent involvement in practice.
- Whether gate agents consult the rule version on the scanner UI — or whether they have workarounds.
- Whether FLCs read Teams task cards before acting — or whether they have offline habits that bypass the system.
- Whether ops controllers trust GIDS staleness indicators when they are displayed.

External adoption pressure from CBP and TSA (regulatory mandate for biometric exit programs) and DOT (consumer protection) creates a compliance floor. The discovery must determine whether operational users are aligned with that floor — or working around it.

---

## Scope

| In Scope | Out of Scope |
|----------|-------------|
| DSS DisplayHub pipeline: GIDS, FIDS, BIDS, WIDS display staleness measurement | Upstream AOC systems — fire-and-forget is the DSS contract |
| Tarmac timer compliance display chain (door-close → GIDS render) | Gate agent scheduling or rostering systems |
| Biometric boarding: CBP TIS match flow, opt-out path, false non-match rate | Biometric enrolment (pre-gate; separate product domain) |
| Biometric PII log boundary verification | Passport / document scanning (separate flow) |
| Carry-On: bag matrix rule engine, Apigee proxy, admin propagation UI | Checked baggage systems (separate domain) |
| Carry-On: override audit completeness and supervisor auth enforcement | Revenue management pricing for gate-checked bags |
| Connect Me: Teams alert delivery latency, FLC load plan sign-off flow | Non-gate Teams bots or notification systems |
| Connect Me: unread alert rate measurement and escalation workflow | Connect Me integrations outside flight ops events |
| Azure App Insights custom metric instrumentation (all four domains) | Infrastructure SRE/capacity planning |
| Baseline measurement for all four domains (Sprint 0 instrumentation) | Post-discovery solution design and build |
| Regulatory compliance evidence collection (FAA, TSA, CBP, DOT) | Legal proceedings or audit response (owned by Legal/Compliance teams) |

---

## Discovery Questions

These are the questions this discovery must answer before any solution design begins. Each maps to a PRD-2.1 dimension gap or a known open baseline.

### DSS Display
1. What is the current p95 latency from AOC event publish to GIDS render across the estate — not the target, the measurement?
2. Under what conditions does the 5s SLA break — Service Bus lag, DisplayHub render contention, or network?
3. Has the tarmac timer ever been in a sub-screen or behind a tab in any station? Is there audit evidence?

### Biometric Boarding
4. What is the measured false non-match rate at the current pilot gate(s)?
5. What is the boarding throughput with biometrics vs. manual scan — does biometrics slow or accelerate boarding today?
6. Can a passenger reach the opt-out path at the gate podium without agent involvement in under 2 taps? Field-test evidence?
7. Are biometric deletion jobs confirmed running and purging within 12h post-departure in production?

### Carry-On Compliance
8. What is today's gate-check rate by station and flight type?
9. What is the override rate — how often do agents successfully override without supervisor auth?
10. What is today's measured rule propagation time from admin submit to all-gates confirmed?

### Connect Me
11. What is today's p95 Teams alert delivery latency from AOC publish to device delivery?
12. What percentage of gate change alerts go unread within 5 minutes in production?
13. Do FLCs confirm load plan task cards before departures, or do they have offline workarounds?

---

## Avatars Activated

| Avatar | Type | Context |
|--------|------|---------|
| `avatar-product-gate-management` | Product | Gate operations domain intelligence — 4 use cases, 7 personas, 7 laws. RAG validated 2026-04-22. |
| `avatar-tech-dss-event-driven` | Technology | DSS DisplayHub event-driven microservices — Azure Service Bus, TypeScript/Node, Java, .NET. RAG validated 2026-04-22. |
| `avatar-tech-apigee-azure` | Technology | Apigee API gateway + Azure infrastructure — Biometrics, Carry-On OAuth proxy. RAG validated 2026-04-22. |

---

## Open Questions for Bhavita and Derek

Before we lock Stage A and open Stage B, the following questions need your product expertise:

1. **Approval authority:** Adeel is listed as Discovery Sponsor. PRD-2.5 requires a named Director+ approver who is not self-certifying. Is Adeel the formal approver for this discovery, or is there another stakeholder who should co-sign?

2. **Scope boundary — biometric enrolment:** We've scoped out biometric enrolment (pre-gate). Is the enrolment funnel actually a discovery question for this run — e.g., if opt-out rates are driven by enrolment friction — or does it stay out of scope?

3. **Priority ordering:** All four domains have open baselines. If Stage B field study resources are constrained, which domain is highest-priority for depth? Our recommendation based on regulatory risk is: **Biometrics (CBP exposure) → DSS (DOT tarmac timer) → Carry-On (DOT consumer protection) → Connect Me (operational).**

4. **Trio peer-check confirmation:** Adeel referenced trio laws as session-established principles. We are treating this as: Amal frames problem/product, Amaya frames technical feasibility, Willem calls governance gates. Bhavita and Derek, does this working protocol match your expectations for the session, or should we formalise it differently?

---

## Stage A Exit Checklist

| # | Gate | Law | Status |
|---|------|-----|--------|
| 1 | Discovery ID assigned (disc-2026-004) | ENG-11.1 | ✅ Done |
| 2 | stage-a-initialize.md created from template | ENG-11.2 | ✅ Done |
| 3 | Problem statement — all 4 PRD-2.1 dimensions filled | PRD-2.1 | ✅ Done |
| 4 | Scope defined (in/out table populated) | PRD-2.5 | ✅ Done |
| 5 | Mode declared (Exploratory) | PRD-2.5 | ✅ Done |
| 6 | Tier declared (Tier 2) | PRD-2.5 | ✅ Done |
| 7 | Product + Technology avatars activated and recorded | PRD-2.5, BUS-7.1 | ✅ Done |
| 8 | Stakeholder approval — named Director+ (PRD-2.5, no self-cert) | PRD-2.5 | ⏳ Pending your approval |
| 9 | HTML rendered and APPROVED in browser | ENG-13.1 | ⏳ Pending render |
| 10 | BUS-7.1 audit event filed — Stage A → B | BUS-7.1 | ⏳ After render approval |
