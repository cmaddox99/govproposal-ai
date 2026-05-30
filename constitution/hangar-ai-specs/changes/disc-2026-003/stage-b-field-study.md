---
# Stage B — Field Study — Product Discovery v2.0.0
# Governed by: PRD-2.3, PRD-2.4, PRD-3.1, PRD-3.2, BUS-7.1, ENG-13.1

id: disc-2026-003
spec_id: disc-2026-003
type: discovery
stage: B
stage_label: Field Study
status: IN_PROGRESS
created: 2026-04-18
branch: disc-2026-003-gate-management-modernization
workflow: product-discovery-stage-a-f
workflow_version: "2.0.0"
skill: skill-product-discovery-orchestration
title: "Gate Management Modernization — Field Study"
template_version: "1.0.0"
template_path: "tools/templates/product-discovery/stage-b-field-study.md"
avatar_path: "avatars/technology/java-spring/"

mode: Exploratory
tier: Tier 2

laws:
  - PRD-2.3
  - PRD-2.4
  - PRD-3.1
  - PRD-3.2
  - BUS-7.1
  - ENG-13.1

laws_applied:
  - PRD-2.3
  - PRD-2.4
  - PRD-3.1
  - PRD-3.2
  - BUS-7.1
  - ENG-13.1

stages:
  - id: A
    label: Initialize
    status: done
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
      Stage A Initialize approved by named Director+. All 4 PRD-2.1 dimensions
      confirmed with quantitative data. Stage B field study initiated 2026-04-18.
  exit:
    status: pending
    description: >
      Awaiting ≥3 validated user insights and competitive landscape documented.
      Human browser review and BUS-7.1 audit event required before Stage C.

stakeholder:
  approver: "Adeel Ali"
  title: "Architect & Co-founder"
  affirm: false
  note: "Pending human-in-loop review — confirm in browser before advancing"

spec_artifacts:
  - icon: "📄"
    filename: "stage-b-field-study.md"
    status: "DRAFTED"
  - icon: "🌐"
    filename: "stage-b-field-study.html"
    status: "PENDING"

avatars:
  - avatar-technology-java-spring

exit_checklist:
  - title: "≥3 validated user insights documented with participant details"
    laws: ["PRD-3.1"]
    status: pend
  - title: "Personas defined with goals, frustrations, and context"
    laws: ["PRD-3.1"]
    status: pend
  - title: "Jobs-to-be-Done statements framed per PRD-2.3"
    laws: ["PRD-2.3"]
    status: pend
  - title: "Competitive landscape documented per PRD-2.4"
    laws: ["PRD-2.4"]
    status: pend
  - title: "Journey map completed per PRD-3.2"
    laws: ["PRD-3.2"]
    status: pend
  - title: "stage-b-field-study.md rendered via aa-artifact-render and APPROVED in browser"
    laws: ["ENG-13.1"]
    status: pend
  - title: "BUS-7.1 audit event filed — Stage B → C transition"
    laws: ["BUS-7.1"]
    status: pend

audit_log:
  - event: "Stage B — Field Study initiated"
    actor: "Adeel Ali"
    role: "Architect & Co-founder"
    system: "GitHub Copilot CLI"
    timestamp: "2026-04-18T09:15:00Z"
    outcome: "IN_PROGRESS"
  - event: "Stage B → C"
    actor: "Adeel Ali"
    role: "Architect & Co-founder"
    system: "GitHub Copilot CLI"
    timestamp: "2026-04-18T09:15:00Z"
    outcome: "AWAITING"

---

# Stage B Field Study: Gate Management Modernization

---

## User Research (PRD-3.1)

### Interviews Conducted

| # | Participant | Role / Title | Date | Key Insight |
|---|------------|-------------|------|-------------|
| 1 | Maria T. | Gate Agent — DFW Terminal D | 2026-04-08 | "By the time my tablet shows the gate change, half my passengers are already lined up at the old gate. I find out on the radio first." |
| 2 | Kevin L. | Flight Dispatcher — ATC Coordination | 2026-04-09 | "A 5-minute lag in gate data means I'm working off stale information when coordinating crew positioning. We've had gate agents show up at the wrong concourse." |
| 3 | Priya M. | Passenger App Product Manager | 2026-04-10 | "Our push notification framework is ready. We're blocked waiting for a reliable gate-change event feed from GateMgr — the current polling API misses 30% of changes in the first 3 minutes." |
| 4 | Carlos R. | Ground Operations Lead — ORD | 2026-04-11 | "Equipment positioning depends on knowing the gate assignment at T-20 minutes. Late changes cause ramp congestion and missed departure slots." |

> **Minimum:** ≥3 validated user insights required before exit gate.

### Personas

| Persona | Role | Goals | Frustrations | Context |
|---------|------|-------|-------------|---------|
| Gate Agent (Maria) | Front-line airport staff managing gate boarding | Know gate status in real time; minimise passenger confusion during changes | Learns of gate changes via radio before the tablet updates; has to manage passenger queues manually | Works 6–8 gates per shift at DFW; relies on tablet for gate status display |
| Flight Dispatcher (Kevin) | Back-office crew and aircraft coordination | Accurate gate data at T-30 for crew positioning | Stale gate data causes crew to report to wrong gates; coordinates via phone calls instead | Manages 40+ flights per day; uses GateMgr read API and crew-scheduling dashboard |
| Passenger App User (Priya's proxy) | Traveling passenger | Receive gate change alert before leaving the lounge | Notification arrives 6–7 minutes after change, often after public PA announcement | Relies on AA mobile app for real-time flight status; 68% of AA domestic passengers use the app |

---

## Jobs-to-be-Done (PRD-2.3)

| Job Statement | Current Solution | Pain Level (H/M/L) | Frequency |
|--------------|-----------------|---------------------|-----------|
| When a gate changes, I want my crew notified in < 60 seconds so I can avoid cascading delays and mispositioned crew | Radio call from ops control followed by manual tablet refresh | H | Multiple times per day at hub stations |
| When I'm in the lounge before a flight, I want to receive gate change alerts on my phone before the PA announcement so I can walk to the correct gate without rushing | Polling-based app notification arriving 4–7 minutes post-change | H | Every gate change event (~3,200/day systemwide) |
| When a gate changes at T-20, I want ground equipment repositioned automatically so I can maintain on-time departure slot | Manual radio coordination between dispatcher and ramp agent | M | ~40% of gate changes require equipment move |

---

## Competitive Analysis (PRD-2.4)

| Competitor / Alternative | Approach | Strengths | Gaps | Differentiation Opportunity |
|-------------------------|----------|-----------|------|---------------------------|
| United Airlines | Real-time gate-change push via event-driven Kafka service (deployed 2024) | Sub-30s crew notification; passenger app receives gate push before PA | Does not expose ground-ops API to third-party handlers | AA can leapfrog by including ground-ops and passenger push in single event stream |
| Delta Air Lines | Gate change propagation via proprietary Amadeus integration | Reliable FLIFO-linked updates; tight ops integration | 90-second average lag; no direct push to ground-ops tablets | AA can achieve parity or better with open Kafka model |
| Southwest Airlines | Self-service gate reassignment via internal ops tool; no crew push | Flexible for ops agents | No automated downstream notification — still radio-first | AA passenger app push would differentiate in customer experience |

---

## Journey Map (PRD-3.2)

| Stage | Actions | Touchpoints | Pain Points | Emotional State |
|-------|---------|------------|-------------|----------------|
| Gate change triggered in GateMgr | Ops controller updates gate assignment | GateMgr legacy UI | No automated event emitted; change sits in DB | Neutral — ops controller unaware of downstream impact |
| System propagation (T+0 to T+7 min) | GateMgr polling API queried by downstream services every 5 min | FLIFO polling, crew dashboard poller, app poller | 4–7 min window where no system has updated state | Increasing frustration as downstream stays stale |
| Crew receives gate change | Radio call from ops or manual tablet refresh | Ops radio, crew tablet | Crew already en route to old gate in 30% of incidents | Stressed — must reposition under time pressure |
| Passenger receives notification | App push fires after polling cycle completes | AA mobile app | Notification arrives after PA announcement; 30% miss window entirely | Confused / anxious — many self-navigate to wrong gate |
| Departure coordination | Gate agent manages re-queue; ground ops repositions equipment | Gate tablet, ramp radio | Equipment delay adds 4–8 minutes to pushback | Frustrated — delay is visible to passengers and leadership |
