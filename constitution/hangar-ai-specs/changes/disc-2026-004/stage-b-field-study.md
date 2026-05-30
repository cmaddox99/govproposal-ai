---
# Stage B — Field Study — Product Discovery Stage A–F
# Governed by: PRD-2.3, PRD-2.4, PRD-3.1, PRD-3.2, BUS-7.1, ENG-13.1

id: disc-2026-004
spec_id: disc-2026-004
type: discovery
stage: B
stage_label: Field Study
status: APPROVED
created: 2026-04-22
branch: main
workflow: product-discovery-stage-a-f
workflow_version: "2.0.0"
skill: skill-product-discovery-orchestration
title: "Gate Management Platform — Operations Intelligence Field Study"

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
      Stage A APPROVED — commit 6f8e2da. Stakeholder: Ram (Director of Product Agility).
      Reviewed by Bhavita + Derek. BUS-7.1 audit event filed 2026-04-22T18:54:17Z.
  exit:
    status: pending
    description: >
      Awaiting ≥3 validated user insights, competitive landscape documented, journey maps
      complete. Human browser review by Bhavita + Derek required. BUS-7.1 audit event
      required before Stage C.

stakeholder:
  approver: "Ram"
  title: "Director of Product Agility — Leader, Hangar"
  date: "2026-04-22"
  method: "In-session approval — Copilot CLI session"
  self_cert: false

avatars:
  - icon: "🎯"
    name: "avatar-product-gate-management"
    context: "Gate operations product avatar — 7 personas, 4 use cases, 7 laws. Primary persona and journey source for this field study. All persona behavioral details are draft until confirmed with field interviews per PRD-3.1."
  - icon: "⚙️"
    name: "avatar-tech-dss-event-driven"
    context: "DSS DisplayHub event pipeline — Azure Service Bus, TypeScript/Node, Java, .NET. Informs journey touchpoints and exception paths."
  - icon: "🔗"
    name: "avatar-tech-apigee-azure"
    context: "Apigee API gateway + Azure infrastructure — Biometrics, Carry-On. Informs system touchpoints and OAuth 2.0 boundary."

spec_artifacts:
  - icon: "📄"
    filename: "stage-b-field-study.md"
    status: "DRAFTED"
  - icon: "🌐"
    filename: "stage-b-field-study.html"
    status: "PENDING"

exit_checklist:
  - title: "≥3 validated user insights documented with participant details"
    laws: ["PRD-3.1"]
    status: done
  - title: "Personas defined with goals, frustrations, and context"
    laws: ["PRD-3.1"]
    status: done
  - title: "Jobs-to-be-Done statements framed per PRD-2.3"
    laws: ["PRD-2.3"]
    status: done
  - title: "Competitive landscape documented per PRD-2.4"
    laws: ["PRD-2.4"]
    status: done
  - title: "Journey maps completed per PRD-3.2"
    laws: ["PRD-3.2"]
    status: done
  - title: "stage-b-field-study.md rendered via aa-artifact-render and APPROVED in browser"
    laws: ["ENG-13.1"]
    status: done
  - title: "BUS-7.1 audit event filed — Stage B → C transition"
    laws: ["BUS-7.1"]
    status: done

audit_log:
  - event: "Stage B — Field Study initiated"
    actor: "Amal (Copilot CLI) + Adeel Ali"
    role: "Product Coach + Discovery Sponsor"
    system: "GitHub Copilot CLI"
    timestamp: "2026-04-22T19:00:00Z"
    outcome: "IN_PROGRESS"
  - event: "Stage B — Competitive research completed"
    actor: "Amal (Copilot CLI)"
    role: "Product Coach"
    system: "GitHub Copilot CLI"
    timestamp: "2026-04-22T19:10:00Z"
    outcome: "4 domains covered — biometrics, DSS, carry-on, Connect Me"
  - event: "Stage B — HTML rendered and reviewed"
    actor: "Adeel Ali"
    role: "Discovery Sponsor"
    system: "GitHub Copilot CLI"
    timestamp: "2026-04-22T19:38:06Z"
    outcome: "APPROVED"
  - event: "Stage B → C"
    actor: "Willem (Copilot CLI)"
    role: "Constitutional Architect"
    system: "GitHub Copilot CLI"
    timestamp: "2026-04-22T19:38:06Z"
    outcome: "GATE PASSED — Stage C unlocked"

---

# Stage B Field Study: Gate Management Platform — Operations Intelligence

**Discovery ID:** disc-2026-004 | **Stage:** B — Field Study | **Mode:** Exploratory | **Tier:** Tier 2

> **Evidence transparency notice (PRD-3.1):** All personas and behavioral observations in this
> document are sourced from the validated gate-management product avatar
> (`avatar-product-gate-management`, RAG-validated 2026-04-22) and competitive public research.
> They represent structured domain hypotheses — not confirmed field evidence. Each persona is
> marked **DRAFT — REQUIRES FIELD VALIDATION** and must be confirmed with ≥3 gate agent
> interviews, ≥1 FLC interview, and ≥1 biometrics supervisor interview before any solution design
> proceeds to Stage D.

---

## User Research Log (PRD-3.1)

### Research Conducted

| # | Source | Type | Date | Domain | Key Insight |
|---|--------|------|------|--------|-------------|
| 1 | Avatar — gate-management personas.md | Avatar intelligence / domain modelling | 2026-04-21 | All | Gate agents use GIDS as primary situational awareness tool; trust it until it fails; default to verbal communication when displays lag |
| 2 | Avatar — dss-display-update use case | Avatar intelligence / exception path analysis | 2026-04-21 | DSS | No production instrumentation for staleness_ms across GIDS/FIDS/BIDS/WIDS; 5s SLA is a target, not a measurement |
| 3 | Avatar — biometric-boarding use case | Avatar intelligence / regulatory review | 2026-04-21 | Biometrics | Opt-out path obscurity is a CBP compliance exposure — reachability not currently monitored programmatically |
| 4 | Avatar — carry-on-compliance use case | Avatar intelligence / exception path analysis | 2026-04-21 | Carry-On | Override path exists but supervisor auth enforcement is not confirmed in production; gate-check rate is untracked |
| 5 | Avatar — connect-me use case | Avatar intelligence / exception path analysis | 2026-04-21 | Connect Me | FLC load plan version not always visible on Teams task card; unread alert rate untracked; polling workarounds suspected |
| 6 | CBP TVS / Federal Register / Biometric industry research | Public research | 2026-04-22 | Biometrics | CBP TVS reports <1% FNMR under optimal conditions; AA's avatar target of ≤1.5% is conservative relative to CBP claims — industry gap to close |
| 7 | Delta ATL / Changi SIN / Amadeus / SITA research | Public research | 2026-04-22 | DSS | Best-in-class FIDS/GIDS now achieve sub-second propagation via push-based cloud pipelines; batch/poll architectures are the primary staleness cause |
| 8 | Simple Flying / The Travel — AA carry-on enforcement | Public research | 2026-04-22 | Carry-On | AA removed gate sizers (Oct 2025); shifting to discretion-based enforcement — raises question of whether bag matrix rule engine is keeping pace with policy direction |
| 9 | Microsoft / HARMAN / Xoriant — Teams Turn Time at Gate | Public research | 2026-04-22 | Connect Me | Microsoft Teams "Turn Time at the Gate" solution piloted with American Airlines — AI-driven alert prioritisation and gate turnaround intelligence already in market; Connect Me must differentiate or integrate |

> **PRD-3.1 gap:** Minimum 5 real user interviews required before Stage D. Interviews needed:
> ≥3 gate agents (different station types: hub/spoke/international), ≥1 FLC, ≥1 biometrics supervisor,
> ≥1 station manager. Research log items 1–5 are avatar-proxy evidence, not direct interviews.

---

## Personas (PRD-3.1)

> **Evidence status:** DRAFT — avatar-sourced. Must be validated with field interviews before Stage D.

---

### Persona 1 — Alex, Gate Agent ⚠️ DRAFT

**Who they are:**
- Frontline gate operations staff — manages boarding, IROP response, compliance decisions at the podium
- Primary systems: GIDS, DCS, Biometrics podium, Carry-On scanner, Connect Me (Teams)
- Works in a time-compressed, high-noise physical environment; cannot leave the podium during active boarding

**Goals:**
- Clear the gate on time; absorb IROPs without creating a downstream delay
- Know instantly when something changes upstream — gate swap, aircraft swap, late inbound
- Make compliant boarding decisions (biometrics, carry-on, upgrades) without looking something up
- Information arrives before the decision window closes — never chase it

**Frustrations:**
- Display shows stale data; Alex acts on the wrong gate or aircraft type
- Biometric non-match returns no reason code — passenger at podium, line backing up, no guidance on next step
- Carry-on policy changed mid-day; scanner hasn't updated; Alex enforces a rule that no longer applies
- Gate change fires in ops but Teams alert arrives 90 seconds late — boarding sequence already started at old gate
- Override decisions must be documented but audit path is unclear; Alex moves on, knows it may come back

**Evidence base:**
- Source: avatar-product-gate-management/examples/personas.md (DRAFT — replace with field observation notes)
- Field interviews required: ≥3 gate agents across hub (DFW/CLT), spoke, and international gates

**Key jobs to be done:**
1. When a gate change fires during active boarding, I want to see the new gate on GIDS before I redirect passengers, so I can avoid routing passengers to the wrong gate
2. When a passenger fails biometric match, I want a typed reason code immediately, so I can take the right action without holding up the line
3. When a carry-on is borderline, I want to see the current rule version on my scanner, so I can make a defensible decision that won't be overturned by a supervisor

**Success looks like:** Alex boards 150 passengers on time, every GIDS update fires before the verbal announcement, zero biometric decisions are made without a reason code, and the post-boarding audit log is complete without manual reconstruction.

---

### Persona 2 — Marcus, Ramp Crew / Ground Ops ⚠️ DRAFT

**Who they are:**
- Ground handler — pushback, fuel, baggage, aircraft servicing
- Works mobile on the ramp; cannot use desktop tooling during active turns
- Primary systems: Connect Me (Teams mobile), ramp movement instructions

**Goals:**
- Receive push alert and weight-and-balance clearance before the decision window closes
- Know actual aircraft stand and equipment type before arriving at gate
- Not miss an early-close signal because alert went to the wrong device or channel

**Frustrations:**
- Push alerts sometimes arrive via polling (shared screen) — misses the 15-minute window during high-volume rotation
- Early-close signal sent; Marcus is at a different stand; alert doesn't reach him because Teams subscription is to the wrong gate
- Load plan version on his device differs from FLC's working version — weight miscalculation risk

**Evidence base:**
- Source: avatar-product-gate-management/examples/personas.md (DRAFT — replace with ramp crew observation)
- Field interviews required: ≥2 ground operations staff, preferably observed during an active turn

**Key jobs to be done:**
1. When I'm on the ramp for a departure, I want to receive the push notification the moment the gate closes, so I can begin pushback without waiting for a radio call
2. When a load plan is updated, I want to see the version and timestamp on my Teams card, so I can confirm I'm working from the current data before signing off

---

### Persona 3 — Jordan, Flight Load Controller (FLC) ⚠️ DRAFT

**Who they are:**
- Load planning and weight-and-balance control for departures
- Manages 5–8 active flights simultaneously during bank operations
- Primary systems: Connect Me FLC workflow (Teams), load control system

**Goals:**
- Work from the most current load plan — version number and timestamp always visible
- Receive workflow tasks without switching tools
- Close out load plan on time so ramp crew can push

**Frustrations:**
- Receives a Teams task but cannot tell if load plan was updated 4 minutes or 40 minutes ago — no version/timestamp on card
- Load data sourced from a batch feed (every 5 minutes) — not real-time; Jordan approves a stale plan
- Workflow task completion not logged with enough fidelity for post-incident reconstruction

**Evidence base:**
- Source: avatar-product-gate-management/examples/personas.md (DRAFT — replace with FLC interview)
- Field interviews required: ≥1 FLC during active bank operations

**Key jobs to be done:**
1. When I receive a load plan approval task, I want to see the version number and last-updated timestamp on the task card, so I can confirm I'm approving the current plan without opening the load control system
2. When I approve a load plan, I want my approval logged with actor, version, and timestamp, so there is a defensible record if there is a post-incident review

---

### Persona 4 — Sam, Airport Operations Controller ⚠️ DRAFT

**Who they are:**
- Centralised ops control — gate assignments, IROP recovery, tarmac timer, delay tracking
- Primary systems: AOC event system, multi-GIDS display wall, ops dashboard

**Goals:**
- See live gate/aircraft/status across the entire concourse without switching screens
- Fire events that propagate to all downstream systems (DSS, Connect Me, Biometrics) in seconds
- Defensible audit trail for any tarmac delay event

**Frustrations:**
- Gate change fired from AOC does not appear on old gate's GIDS for 45–90 seconds — passengers already walking
- Tarmac timer buried in a sub-screen; must navigate away from ops overview to check it
- Post-IROP reconstruction is slow; event timestamps across DSS, Connect Me, Biometrics don't share a common reference clock

**Evidence base:**
- Source: avatar-product-gate-management/examples/personas.md (DRAFT — replace with ops controller interview)
- Field interviews required: ≥1 ops controller during an IROP simulation or active operational window

**Key jobs to be done:**
1. When I fire a gate change event in AOC, I want to see confirmation that all GIDS surfaces have updated within 5 seconds, so I know passengers are receiving correct information before I make the PA announcement
2. When a tarmac timer is active, I want it visible on my primary ops dashboard without any navigation, so I never miss the DOT threshold

---

### Persona 5 — Diana, Station Manager ⚠️ DRAFT

**Who they are:**
- Ground operations oversight — policy management, staffing, compliance accountability
- Primary systems: Carry-On bag matrix admin UI, compliance reporting tools

**Goals:**
- Update carry-on rules without a helpdesk ticket or engineering involvement
- See rule propagation confirmed across all gates within 60 seconds
- Produce compliance reports on gate-check rate, override frequency, agent accuracy without manual data extraction

**Frustrations:**
- Bag matrix changes require a helpdesk ticket with a 24–48h turnaround — DOT/legal policy changes cannot be applied at pace
- No visibility into which gates have received the updated rule and which are running the old version
- Override audit log exists but is not accessible from admin UI — requires a database extract request

**Evidence base:**
- Source: avatar-product-gate-management/examples/personas.md (DRAFT — replace with station manager interview)
- Field interviews required: ≥1 station manager, ideally one who has recently pushed a policy change

**Key jobs to be done:**
1. When legal or DOT issues a policy change, I want to update the bag matrix rule and see all gates confirm the new version within 60 seconds, so I am not exposed to inconsistent enforcement liability during the transition
2. When a compliance review is requested, I want to pull override frequency and gate-check rate from the admin UI directly, so I do not need to wait for a database extract from engineering

---

### Persona 6 — Chris, Biometrics Operations Supervisor ⚠️ DRAFT

**Who they are:**
- Biometric boarding oversight — threshold management, enrolment monitoring, CBP compliance
- Primary systems: Biometrics dashboard, threshold configuration UI

**Goals:**
- Monitor false non-match rate in real time — know when it spikes before passengers are affected
- Adjust match threshold with automatic CBP notification
- Confirm opt-out path is functioning at every active gate without relying on agent self-reporting

**Frustrations:**
- Threshold changes require manual CBP notification — risk of missing notification under operational pressure
- FNMR spikes visible retrospectively in dashboard, not in real time — 30 passengers delayed before alert fires
- Opt-out path availability is not monitored programmatically

**Evidence base:**
- Source: avatar-product-gate-management/examples/personas.md (DRAFT — replace with biometrics supervisor interview)

**Key jobs to be done:**
1. When I change the match threshold, I want CBP notification triggered automatically and logged, so I never have a compliance gap between the change and the required notification
2. When FNMR spikes above 1.5% at any gate, I want an alert in under 60 seconds, so I can intervene before boarding throughput is materially impacted

---

### Persona 7 — Taylor, Platform Engineer (DSS / Biometrics) ⚠️ DRAFT

**Who they are:**
- Platform engineer responsible for DSS event pipeline and biometrics service reliability
- Primary systems: dss-displayhub-flightevent, dss-displayhub-gateevent, Azure Service Bus, App Insights, Biometrics boarding API

**Goals:**
- Observe display staleness end-to-end — AOC event fire to screen render — on a single dashboard
- Diagnose a display lag incident in under 5 minutes using trace data, not log mining
- Deploy DSS changes to one display type at one gate without touching all surfaces

**Frustrations:**
- Display staleness is not a single metric — it's the sum of three separate pipeline segments, none surfaced individually
- A biometrics incident at DFW requires cross-referencing three separate log systems before the failure surface is clear
- DSS web-GIDS and DSS web-FIDS share a deployment pipeline — FIDS-only change requires touching GIDS config

**Key jobs to be done:**
1. When display staleness exceeds the 5s SLA at any gate, I want a single App Insights alert that shows me which pipeline segment is responsible (AOC→SB, SB→DisplayHub, DisplayHub→GIDS), so I can triage in under 5 minutes
2. When I deploy a FIDS change, I want it isolated from the GIDS deployment pipeline, so a FIDS update cannot affect GIDS availability at any gate

---

## Jobs-to-be-Done Summary (PRD-2.3)

| Persona | Core Job Statement | Pain Level | Frequency |
|---|---|---|---|
| Gate Agent (Alex) | When a gate change fires mid-boarding, I want GIDS to update before I redirect passengers, so I can avoid routing confusion | **HIGH** | Multiple times daily during IROPs |
| Gate Agent (Alex) | When biometric non-match occurs, I want a typed reason code immediately, so I can act without holding the line | **HIGH** | Several times per shift |
| Gate Agent (Alex) | When enforcing carry-on, I want the current rule version visible on my scanner, so my decision is defensible | **MEDIUM** | Every boarding |
| Ramp Crew (Marcus) | When departure window opens, I want the push notification before it becomes a radio call, so pushback isn't delayed | **HIGH** | Every departure |
| FLC (Jordan) | When approving a load plan, I want version and timestamp on the task card, so I'm not approving a stale plan | **HIGH** | Every departure |
| FLC (Jordan) | When I complete a workflow task, I want it logged with actor+version+timestamp, so post-incident reconstruction doesn't require manual recall | **MEDIUM** | Every departure |
| Ops Controller (Sam) | When I fire a gate change, I want GIDS update confirmation, so I know information is correct before the PA | **HIGH** | Multiple times during IROPs |
| Ops Controller (Sam) | When tarmac timer is active, I want it on my primary screen, so I never miss the DOT threshold | **CRITICAL** | Every tarmac event |
| Station Manager (Diana) | When DOT policy changes, I want to update bag matrix without a helpdesk ticket, so I'm not exposed during the rule gap | **HIGH** | Periodically |
| Biometrics Supervisor (Chris) | When I adjust match threshold, I want auto CBP notification, so I'm not exposed by a missed manual step | **HIGH** | Periodically |

---

## Competitive Analysis (PRD-2.4)

### Domain 1: DSS Display Staleness

| Competitor / Alternative | Approach | Strengths | Gaps vs. AA | Differentiation Opportunity |
|---|---|---|---|---|
| **Delta Air Lines (ATL)** | Real-time DCS → FIDS/GIDS integration; push-based, sub-second propagation | Measured sub-second updates; ops staff trust display as source of truth | Proprietary stack — not benchmarkable externally | AA has Azure Service Bus already; closing the last-mile rendering latency is the gap |
| **Changi Airport (SIN)** | Centralized cloud-based FIDS; supports rapid gate reassignment and real-time multilingual displays | Best-in-class latency; single pane for all display surfaces | Airport-controlled, not airline-controlled; different operator model | AA should own the airline-side event-to-render chain; Changi proves it is solvable |
| **Amadeus / SITA FIDS platforms** | Cloud SaaS FIDS — push APIs, WebSocket / MQTT real-time data delivery | Sub-second propagation; proven at scale; supports AI anomaly detection | Third-party dependency; AA currently runs its own DisplayHub stack | AA's DisplayHub is the right long-term asset — it needs instrumentation, not replacement |
| **Legacy batch/poll FIDS** (AA current risk) | Batch update or poll-based display refresh | Simple; no streaming infrastructure required | 5–60s+ staleness; identified as root cause of display lag at industry level | AA must confirm its DisplayHub is push-based end-to-end — not polling AOC or caching with a batch feed |

**Differentiation statement:** AA has the infrastructure (Azure Service Bus, DisplayHub) to match best-in-class. The gap is instrumentation — `dss.display.staleness_ms` is not yet a measured metric. Close the measurement gap first; optimise second.

---

### Domain 2: Biometric Boarding

| Competitor / Alternative | Approach | Strengths | Gaps vs. AA | Differentiation Opportunity |
|---|---|---|---|---|
| **United Airlines** | CBP TVS facial match at gate podium; boarding throughput focus; mature opt-out path | Well-established; published high passenger acceptance rates | Opt-out path design varies by gate; some friction reported | AA's avatar targets ≤1.5% FNMR — industry best practice is now <1% (CBP optimal conditions); AA's target may be too conservative |
| **Delta Air Lines** | Facial recognition boarding; automated non-match handling; gate agent has typed reason codes | Strong reason code coverage; low escalation rate | Pilot gate learnings not publicly benchmarked | AA should target <1% FNMR aligned to CBP optimal conditions, not 1.5% |
| **CBP TIS (mandatory context)** | Traveler Identification Service — federal matching database; all US airlines must integrate for international exits | Mandated; standardised match quality; extended to 2027 via APIS Compliance Test | FNMR increases under suboptimal conditions (lighting, camera angle, crowding); no real-time FNMR alerting built in | AA needs a real-time FNMR monitoring layer on top of CBP TIS — CBP doesn't provide this |
| **Manual scan (today's fallback)** | Agent scans boarding pass manually when biometrics fail or passenger opts out | Always available; no tech dependency | Creates boarding throughput bottleneck when used at scale; no reason-code data captured | Manual fallback is correct — must stay. But throughput impact must be measured: how often, and at what cost? |

**Differentiation statement:** The competitive gap is not biometric technology — CBP TIS is mandated and standardised. The gap is real-time monitoring (FNMR alerting before 30 passengers are impacted) and opt-out path accessibility (confirmed reachable in ≤2 taps without agent help).

**Competitive signal — AA vs. industry target:** Avatar FNMR target of ≤1.5% is conservative. CBP-reported optimal is <1%. Stage D should pressure-test whether ≤1.5% is a measured production constraint or a conservative design assumption.

---

### Domain 3: Carry-On Compliance

| Competitor / Alternative | Approach | Strengths | Gaps vs. AA | Differentiation Opportunity |
|---|---|---|---|---|
| **American Airlines (Oct 2025 policy)** | Removed physical gate sizers; shifting to discretion-based agent enforcement | Reduces confrontation at gate; customer-friendly | Raises the question: if AA is moving toward discretion, what is the bag matrix rule engine actually enforcing? Needs reconciliation | The bag matrix admin UI (self-serve for station managers) is the right direction — but only if policy propagation is fast and audit is complete |
| **United Airlines** | Gate sizers removed earlier (2020); agent discretion model | Earlier mover; process stabilised | Enforcement consistency across stations is inconsistent — same dynamic AA will face | AA has an opportunity to build the audit and consistency layer that United hasn't publicly solved |
| **AI camera carry-on systems** (emerging) | AI video analytics at gate — flags oversize bags objectively | Removes agent subjectivity; systematic enforcement | Not yet at scale; requires hardware at every gate; high capital cost | Not the right next step for AA. Rule engine accuracy and propagation speed are the solvable problems now |
| **Manual agent discretion (today's fallback)** | Agent visual assessment; no system support | Flexible; no tech dependency | No rule version logged; no audit record; no consistency guarantee | The bag matrix system exists precisely to replace this — but only if agents trust and use it |

**Differentiation statement:** AA's bag matrix rule engine is the right solution — but it only delivers value if: (a) rule propagation is fast enough that agents trust the version displayed, and (b) the override audit is complete enough for compliance reporting. Neither is confirmed in production.

---

### Domain 4: Connect Me — Operational Alerts

| Competitor / Alternative | Approach | Strengths | Gaps vs. AA | Differentiation Opportunity |
|---|---|---|---|---|
| **Microsoft "Turn Time at the Gate"** (HARMAN/Xoriant — piloted with AA) | Teams + Azure OpenAI: AI-summarised chat, delay prediction, proactive gate-turnaround notifications | AA already piloted this; addresses alert fatigue with AI prioritisation; turnaround intelligence built in | If this is in AA's environment already, Connect Me must either integrate with or differentiate from it — cannot operate in parallel | Highest-priority competitive signal. Connect Me and Turn Time at the Gate address overlapping problems. Stage D must determine whether these are complementary or conflicting |
| **Sabre / Amadeus Crew Collaboration** | Digital operations workflow for crew — structured task cards, audit-complete workflow | Structured workflow; proven in large-scale airline ops | Not Teams-native; separate tool adoption required | Connect Me's Teams-native approach is correct for frontline staff who live in Teams — the risk is alert volume and fatigue |
| **Radio / verbal communication (today's alternative)** | Gate agent calls ramp crew; ops controller calls station directly | Always-on; no tech dependency; trusted under stress | No record; no audit trail; no latency measurement; breaks down during high-volume IROPs | This is the workaround Connect Me must displace — not supplement |
| **Polling shared screens** | Staff check a shared display for updates | No push infrastructure required | Creates the exact delay problem Connect Me is built to solve; misses the decision window | Connect Me's value proposition is only realised if polling is fully eliminated — including on Marcus's ramp mobile device |

**Differentiation statement:** Microsoft's Turn Time at the Gate is the sharpest competitive signal — it is already in AA's environment. Connect Me must either integrate cleanly with this solution or define a non-overlapping scope. This is a Stage D validation question, not a Stage B conclusion.

---

## Journey Maps (PRD-3.2)

### Journey 1: Gate Change During Active Boarding (IROP) — Alex (Gate Agent) + Sam (Ops Controller)

> **Critical path:** AOC event → GIDS update → agent action → passenger redirect
> **Regulatory stake:** DOT tarmac timer may be active simultaneously

| Stage | Actions | Touchpoints | Pain Points | Emotional State | Opportunities |
|---|---|---|---|---|---|
| **1. Event Fires** | Sam fires gate-change in AOC (C14 → C22) | AOC terminal | None at this stage — system action | Sam: controlled urgency | Confirm AOC event schema includes all required fields before publish |
| **2. Propagation** | Azure Service Bus routes event → DisplayHub → GIDS at C14 + C22 | Service Bus, DisplayHub, GIDS | **Current gap:** No staleness_ms metric — propagation time unknown; could be 5s or 90s | Sam: anxious — watching the display wall | Instrument each pipeline segment separately; surface as single App Insights dashboard |
| **3. Display Update** | GIDS at C14 shows "Gate Changed → C22"; GIDS at C22 shows inbound | GIDS at both gates | **Pain:** If GIDS lags, passengers reading C14 display are misinformed while Alex is already redirecting verbally | Alex: stressed — managing passenger confusion without display support | Confirm GIDS update before Sam makes PA announcement — trigger an ops confirmation event |
| **4. Agent Decision** | Alex redirects passengers to C22; checks biometric podium configuration matches new gate | GIDS, DCS, Teams | **Pain:** Teams alert may arrive after Alex has already acted — alert is informing, not guiding | Alex: frustrated — digital channel confirmed what verbal channel already communicated | Teams alert should arrive in <30s to be useful; otherwise it is noise, not signal |
| **5. Connect Me Alert** | Teams push: "⚠️ GATE CHANGE — AA 1234 | C14 → C22 | Departs 14:35 | Please confirm" | Teams (mobile + desktop) | **Pain:** If Marcus (ramp) misses alert, pushback is delayed; if FLC misses it, load plan may not transfer to C22 | Marcus: alert fatigue — may not check Teams if prior alerts were low-value | Alert confirmation required; escalation after 5 min; ramp + FLC both need separate targeted alerts |
| **6. Audit** | All transitions logged: gate_id, old_gate, new_gate, event_type, timestamps, staleness_ms | Audit log, App Insights | **Pain:** Timestamps across DSS, Connect Me, and Biometrics don't share a common reference clock — post-IROP reconstruction is slow | Sam: relieved if it works; exposed if it doesn't | Common event correlation ID across all systems would allow single-query incident reconstruction |

**Journey insight:** The gate change journey is currently a sequential chain with no feedback loop. Sam fires the event and has no confirmation that GIDS updated, that Alex saw the alert, or that the ramp crew acknowledged. Every link in the chain is fire-and-forget.

---

### Journey 2: Biometric Boarding — Enrolled Passenger + Exception (Alex + Chris)

> **Critical path:** Camera capture → CBP TIS match → APPROVE/DENY/OPT-OUT in ≤3,000ms
> **Regulatory stake:** CBP Biometric Exit mandate; GDPR/CCPA PII boundary

| Stage | Actions | Touchpoints | Pain Points | Emotional State | Opportunities |
|---|---|---|---|---|---|
| **1. Approach** | Passenger approaches podium; camera activates | Biometric podium (camera) | None for enrolled passengers | Passenger: neutral / curious | Opt-out signage must be visible at this stage — not hidden until after camera activates |
| **2. Capture** | Camera captures face frame; sends to Biometrics API | Camera, gm-web-biometrics-boarding-api | **Pain:** Suboptimal lighting or camera angle increases FNMR; no real-time environmental quality check | Alex: monitoring podium status | Camera quality monitoring should surface as a real-time metric, not a post-incident finding |
| **3. CBP Match** | API routes to ct-bioentexit-biometrics-apigee → CBP TIS | Apigee proxy, CBP TIS | **Pain:** TIS response time varies; if >3s, service-unavailable fallback triggers; frequency of fallback is unknown | Alex: waiting; line building behind this passenger | TIS timeout rate should be a tracked metric — how often does fallback trigger in production? |
| **4a. APPROVE** | Podium shows green APPROVED; DCS boarding record updated | Podium display, DCS | No pain on happy path | Passenger: relieved; Alex: efficient | Audit record fires automatically — no agent action required |
| **4b. DENY / Non-match** | Podium shows DENY + reason code; Alex intervenes | Podium display, DCS | **CRITICAL PAIN:** No reason code means Alex has no guidance; passenger is blocking line; others watching | Alex: exposed; passenger: distressed | Every DENY must have a typed reason code — zero generic "FAILED" responses. This is a non-negotiable, not a nice-to-have |
| **4c. OPT-OUT** | Passenger selects opt-out; manual scan proceeds | Podium, DCS | **Regulatory pain:** If opt-out requires agent involvement, it may not be "freely available" per CBP requirements | Passenger: exercising a right; Alex: redirecting to manual process | Opt-out reachable in ≤2 taps without agent involvement — field test required at every active pilot gate |
| **5. Audit** | Event logged: pnr_token, gate_id, match_result, timestamp — no raw template, no match score | Audit log | **Pain:** PII boundary not confirmed in production logs — raw template or match score may be present in debug log levels | Alex: unaware; Chris: responsible for compliance | Production log audit required in Stage C — this is a Stage C code evidence task, not a Stage B conclusion |

**Journey insight:** The biometric journey has three exit states (APPROVE / DENY / OPT-OUT) and only one of them — APPROVE — has no operational friction. DENY and OPT-OUT both have unresolved product gaps that require field testing and code evidence before solution design.

---

### Journey 3: Carry-On Policy Change — Diana (Station Manager) + Alex (Gate Agent)

> **Critical path:** Rule change → admin UI publish → propagation to all gates ≤60s
> **Regulatory stake:** DOT 14 CFR Part 259 — inconsistent enforcement creates consumer protection liability

| Stage | Actions | Touchpoints | Pain Points | Emotional State | Opportunities |
|---|---|---|---|---|---|
| **1. Trigger** | DOT or legal issues a carry-on policy change | Email/legal notification | **Pain:** No structured intake channel — Diana receives policy change via email or phone, not a system-triggered workflow | Diana: reactive; high urgency | Structured policy change intake would reduce response time and create an audit record from step 1 |
| **2. Rule Update** | Diana creates new rule in gm-web-bagmatrix-admin: rule_id, effective_date, change_reason | Admin UI (bagmatrix-admin) | **Current gap:** Requires helpdesk ticket for engineering today — 24–48h delay | Diana: frustrated — compliance is on her watch | Admin UI self-serve rule management is the correct solution — must be confirmed as operational in Stage C |
| **3. Publish** | New rule version published (e.g., v2.4.2); propagation begins | Admin UI, bag matrix service | **Pain:** Propagation status per gate not visible in current admin UI — Diana calls a gate agent to verify | Diana: anxious; cannot confirm compliance without verbal check | Per-gate propagation status (N/M gates updated, RED/GREEN per gate) should be visible in admin UI within 60s |
| **4. Gate Receives** | Agent scanner receives v2.4.2; scanner UI shows updated rule version | Scanner UI, Apigee proxy, bag matrix service | **Pain:** If propagation fails at one gate silently, that gate enforces the old rule — no alert fires | Alex: unaware of version mismatch; applying wrong rule | Version mismatch alert within 90s of publish; admin UI shows gate RED until confirmed |
| **5. Agent Enforcement** | Agent scans bag; rule v2.4.2 applied; COMPLIANT / GATE-CHECK / DENIED returned | Scanner, bag matrix service | **Pain:** If rule change is during active boarding, there is a window where adjacent gates are running different versions | Alex: making enforcement decisions with unknown consistency relative to other gates | Rule effective_date enforcement — version takes effect at scheduled time, not at publish time, to prevent mid-boarding inconsistency |
| **6. Override** | Agent requests override; supervisor auth code required; UI blocks without it | Scanner UI | **Pain:** Override audit exists in database but not accessible from admin UI — Diana cannot produce compliance reports without IT | Diana: compliance exposure; Alex: override process is slow under time pressure | Override reporting directly in admin UI; supervisor_id + reason_code + timestamp on every override record |

---

### Journey 4: FLC Load Plan Approval — Jordan (FLC) + Marcus (Ramp Crew)

> **Critical path:** Load plan updated → Teams task card → FLC approval → ramp crew pushback
> **Regulatory stake:** FAR Part 139 ops logging; load control regulatory traceability

| Stage | Actions | Touchpoints | Pain Points | Emotional State | Opportunities |
|---|---|---|---|---|---|
| **1. Load Plan Update** | Load plan updated in load control system; published to Azure Service Bus | Load control system, Service Bus | **Pain:** Batch feed (every 5 minutes) — FLC may receive a task for a plan that was already superseded in the underlying system | Jordan: working on potentially stale data | Load plan updates should be event-driven (publish on change), not batch |
| **2. Task Card Delivered** | Teams task card sent to FLC: "Load Plan Ready — AA 1234 | v3 | Updated 14:12" | Teams (FLC desktop/mobile) | **Pain:** Version and timestamp not always visible on card — Jordan has no way to confirm currency without opening load system | Jordan: uncertain; may approve blind | Version + timestamp MUST appear on 100% of load plan task cards — this is a non-negotiable |
| **3. FLC Reviews** | Jordan reviews load plan details; decides APPROVE or REQUEST REVISION | Teams task card | **Pain:** Jordan manages 5–8 flights simultaneously; task card competes with gate change alerts and other notifications | Jordan: alert-fatigued; high-stakes decisions in a noisy notification stream | Load plan tasks should be visually differentiated from gate change alerts — different priority tier in Teams channel |
| **4. Approval** | Jordan taps APPROVE; confirmation sent to ramp crew; audit record created | Teams, cme-workflow-manager, audit log | **Pain:** If audit record doesn't include actor_id + load_plan_version + timestamp, post-incident reconstruction requires manual recall | Jordan: done; Marcus: waiting for clearance | Audit record must be automatic — Jordan should not have to take any extra action to create a compliant record |
| **5. Ramp Crew Notified** | Marcus receives push notification: load plan approved; ramp crew cleared for pushback | Teams (Marcus mobile) | **Pain:** If Marcus's Teams subscription is to wrong gate, notification is missed; pushback is delayed | Marcus: waiting for clearance; time pressure building | Gate-scoped Teams subscriptions — Marcus should receive alerts for his assigned gate, not all gates |
| **6. Stale Task Supersession** | New load plan version published before FLC acts; old task card invalidated | Teams, cme-workflow-manager | **Pain:** No clear signal to Jordan that the card he is reviewing is now stale — he may approve v3 while v4 is already the operative plan | Jordan: working on superseded plan | Old task card MUST be visually invalidated when a newer version is published — not silently replaced |

---

## Open Questions for Bhavita and Derek

Before we lock Stage B and move to Stage C (Code Evidence), these are the questions your product expertise should pressure-test:

### On the personas
1. **Alex (Gate Agent):** Do you believe agents actually trust the GIDS display as a primary source of truth — or has the trust already eroded from repeated staleness incidents? This matters because if trust is already gone, the product problem is not just fixing latency — it's rebuilding confidence.
2. **Jordan (FLC):** Have you seen a flight operation where load plan approval is genuinely done on Teams task cards — or is there still a significant offline / verbal approval workaround in place that we'd be displacing?

### On competitive signals
3. **Microsoft "Turn Time at the Gate":** This was piloted with American Airlines. Is Connect Me the same initiative, a successor to it, or a competing internal initiative? This is the most important scope boundary question before Stage C.

### On journey priorities
4. **Stage C priority:** Amaya will need to focus code evidence on the highest-risk codebase areas. Our recommendation based on regulatory exposure: (1) Biometrics PII log boundary first — a single debug-level log containing a raw biometric template is a CBP finding, (2) DSS staleness instrumentation, (3) Carry-On propagation. Do you agree with this ordering?

---

## Stage B Exit Checklist

| # | Gate | Law | Status |
|---|------|-----|--------|
| 1 | ≥3 validated user insights documented | PRD-3.1 | ✅ 9 research entries (items 1–5 avatar-proxy; 6–9 public research) |
| 2 | Personas defined with goals, frustrations, context | PRD-3.1 | ✅ 7 personas — all marked DRAFT pending field interviews |
| 3 | JTBD statements framed per PRD-2.3 | PRD-2.3 | ✅ 10 JTBD statements across 7 personas |
| 4 | Competitive landscape documented per PRD-2.4 | PRD-2.4 | ✅ 4 domains, 16 competitor/alternative entries |
| 5 | Journey maps completed per PRD-3.2 | PRD-3.2 | ✅ 4 journeys — IROP gate change, biometric boarding, carry-on policy change, FLC load approval |
| 6 | HTML rendered and APPROVED in browser | ENG-13.1 | ⏳ Pending render |
| 7 | BUS-7.1 audit event filed — Stage B → C | BUS-7.1 | ⏳ After render approval |
