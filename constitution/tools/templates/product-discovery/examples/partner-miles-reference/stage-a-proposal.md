---
# Stage A PROPOSAL — Product Discovery v2.0.0
# Governed by: ENG-11.2, PRD-2.1, PRD-2.5, BUS-7.1, ENG-13.1

id: disc-2026-042
spec_id: disc-2026-042
stage: A
stage_label: Initialize
status: IN_PROGRESS
created: 2026-04-17
branch: exploratory-demo
workflow: product-discovery
workflow_version: "2.0.0"
skill: skill-product-discovery-orchestration
title: "AAdvantage Partner-Miles Posting — Trust Gap"

# Header — populates title bar + badges
mode: Exploratory
tier: Tier 2

# All laws referenced anywhere in this artifact
laws:
  - PRD-2.1
  - PRD-2.5
  - BUS-7.1
  - ENG-11.1
  - ENG-11.2
  - ENG-13.1
  - PRD-1.1
  - PRD-5.1
  - BUS-4.1
  - ENG-6.4

# Laws to surface as header ribbon + active-laws sidebar (≤9 recommended)
laws_applied:
  - PRD-2.1
  - PRD-2.5
  - BUS-7.1
  - ENG-13.1
  - ENG-11.1
  - PRD-1.1
  - PRD-5.1
  - BUS-4.1
  - ENG-6.4

# Stage navigation bar + Discovery Progress sidebar
stages:
  - id: A
    label: Initialize
    status: active
  - id: B
    label: Field Study
    status: locked
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

# Stage Gates card (main column)
gates:
  entry:
    status: met
    description: >
      Workshop opportunity surfaced from avatar-product-loyalty (AAdvantage)
      core journey "Points Earning Through Travel". Competitive signal
      corroborated (Delta SkyMiles, United MileagePlus). Exploratory
      discovery initiated on 2026-04-17.
  exit:
    status: pending
    description: >
      Awaiting §Render Gate decision in source PROPOSAL.md from named
      Director+ approver (Adeel Ali). Initiator is Amal (Product Coach) —
      self-certification prohibited by PRD-2.5.

# Mode card
mode_selection:
  selected: Exploratory
  rationale: >
    No prior validated problem statement. Opportunity surfaced from avatar
    pattern + competitive signal. All 4 PRD-2.1 dimensions must be closed
    with fresh evidence in Stage B Field Study.

# Tier card + rubric
tier_selection:
  tier: Tier 2
  rationale: >
    4/5 complexity rubric "Yes". Cross-system member journey, regulatory
    surface (PCI + GDPR), multi-stakeholder, multi-quarter timeline if
    pursued. Full Tier 2 artifact manifest applies.
  rubric:
    - question: Does the discovery span 3+ services or bounded contexts?
      answer: "Yes"
      evidence: Member DB · Points Ledger · Partner Integration APIs · Email/Comms Platform
    - question: Are there 3+ stakeholder groups with distinct needs?
      answer: "Yes"
      evidence: Casual · Frequent traveler · Elite · Program Manager (internal)
    - question: Does the domain involve regulatory or compliance constraints?
      answer: "Yes"
      evidence: PCI-DSS (redemption) · GDPR Art. 6 (EU) · 7-yr retention on financial records
    - question: Is the expected implementation timeline > 1 quarter?
      answer: "Yes"
      evidence: Mainframe partner-feed touchpoints · 180M+ member scale · multi-stack integration
    - question: Does the discovery require cross-team coordination (2+ teams)?
      answer: "TBD"
      evidence: Likely Loyalty + Partner Integrations; confirm in Stage C Assess

# PRD-2.1 four-dimension grid
problem_validation:
  dim1:
    label: "1. Problem Exists"
    status: warn
    text: >
      Avatar + competitor signals suggest yes. AAdvantage partner-mile
      posting window 4–6 weeks vs. Delta ~7 days with status tracker.
      Not yet confirmed by member interviews — Stage B action.
  dim2:
    label: "2. Problem Matters"
    status: warn
    text: >
      Hypothesized cost surfaces — support-call volume and Gold/Platinum
      retention risk. Baseline metrics not yet pulled. Stage B action.
  dim3:
    label: "3. Problem Is Solvable"
    status: ok
    text: >
      Precedent confirmed — Delta and United ship posting-status trackers
      on comparable stack shapes. Feasibility confidence high; integration
      (not capability) is the primary risk.
  dim4:
    label: "4. Users Will Exchange Value"
    status: warn
    text: >
      Hypothesized — members trade 30s of app attention for certainty.
      Low-cost, high-utility *if* hypothesis holds. Needs member validation
      via interviews + concept test in Stage B.

# Domain Landscape cards + arch flow
domain_landscape_title: "Candidate Domain Landscape — From Avatar Dependencies"
domains:
  - name: "Points Ledger"
    icon: "💳"
    header_bg: "#fff1f2"
    header_color: "#9f1239"
    role: "System of record"
    stack: "Mainframe + Ledger API"
    submodules: "—"
    tags:
      - {text: "Earnings", tone: "green"}
      - {text: "Redemptions", tone: "green"}
      - {text: "7-yr retention", tone: "yellow"}
  - name: "Partner Integration APIs"
    icon: "🤝"
    header_bg: "#fffbeb"
    header_color: "#92400e"
    role: "Partner flight feed"
    stack: "Batch ETL · Kafka (proposed)"
    submodules: "—"
    tags:
      - {text: "Nightly batch", tone: "red"}
      - {text: "No real-time hook", tone: "red"}
      - {text: "oneworld", tone: "yellow"}
  - name: "Comms Platform"
    icon: "📧"
    header_bg: "#f5f3ff"
    header_color: "#5b21b6"
    role: "Member notification"
    stack: "Email · Push · SMS"
    submodules: "—"
    tags:
      - {text: "Email", tone: "green"}
      - {text: "Push", tone: "green"}
      - {text: "Consent-gated", tone: "blue"}
arch_title: "Candidate Member Journey — Partner Flight → Mile Post"
arch_flow: |
  Step 1  Member books partner-airline flight
          ↓
          Partner airline processes ticket & flight
          ↳ AA has no real-time signal

  Step 2  Member flies partner segment
          ↓
          Partner → nightly batch feed → AAdvantage Points Ledger
          ↳ Processing window: 4–6 weeks

  Step 3  Member checks AA app daily
          ↓
          AA App → Points Ledger query
          ↳ No "in-flight" status — just absence

  Step 4  Trust erodes → Support call or silent churn
          ↓
          Support: "Please wait 4–6 weeks"
          ↳ No member-facing feedback loop

# Findings
findings_title: "Initial Findings — Stage A Pre-Research Observations"
findings:
  - title: "Competitive benchmark confirms category pattern"
    description: "Delta + United both ship posting-status trackers with ~7-day targets. AA at 4–6 weeks with no visibility."
    status: done
  - title: "Compliance surface is non-trivial"
    description: "Any new member-facing service inherits PCI-DSS, GDPR Art. 6, and 7-yr retention obligations from the ledger."
    status: done
    laws: [BUS-2.2, BUS-4.1, ENG-6.4]
  - title: "Narrowest defensible slice — read-only tracker"
    description: "No mainframe changes, no new PII collection. Surfaces what the ledger already holds."
    status: done
  - title: "Blocker — no member-research data"
    description: "Stage B must originate field study — ≥12 Gold/Platinum interviews + ≥6 casual."
    status: wait

# Ensemble verdict — Amal + Amaya + Willem + Sentinel
ensemble_verdict:
  verdicts:
    - persona: Amal (Product Coach)
      law: PRD-2.1
      note: "Hypothesis documented with 4 PRD-2.1 dimensions partially addressed (#3 confident, #1/#2/#4 hypothesized pending Stage B)."
      verdict: WARN
    - persona: Amaya (Technical Coach)
      law: ENG-6.4
      note: "PII / GDPR surface flagged early (180M+ members, EU data). No architectural commitment yet — appropriate for Stage A."
      verdict: PASS
    - persona: Willem (Constitutional Architect)
      law: PRD-2.5
      note: "Stage-gate non-negotiable: Director+ approver required. No self-certification. Approval pending in §Render Gate."
      verdict: WARN
    - persona: Sentinel
      law: BUS-7.1
      note: "Audit log rows present for initialize, draft, render. Stage A→B transition row queued pending approver decision."
      verdict: PASS

# Exit gate checklist
exit_checklist:
  - title: "Discovery ID assigned in disc-YYYY-NNN format"
    description: "disc-2026-042"
    status: done
    laws: [ENG-11.1, PRD-2.5]
  - title: "PROPOSAL.md created from v2.0.0 template"
    description: "All structural sections populated."
    status: done
    laws: [ENG-11.2, PRD-2.5]
  - title: "Problem statement drafted — 4 PRD-2.1 dimensions"
    description: "3 hypothesized (Stage B to validate), 1 confident."
    status: done
    laws: [PRD-2.1]
  - title: "Scope defined (in/out)"
    description: "Surfaced in body §Scope."
    status: done
    laws: [PRD-2.5]
  - title: "Product + Business + Loyalty avatars activated"
    description: "avatar-product-loyalty v1.0.0 loaded by Amal."
    status: done
    laws: [PRD-2.5, BUS-7.1]
  - title: "Mode declared — Exploratory"
    description: "No prior validated problem; all 4 dimensions from fresh evidence."
    status: done
    laws: [PRD-2.5]
  - title: "Tier declared — Tier 2"
    description: "4/5 rubric Yes."
    status: done
    laws: [PRD-2.5]
  - title: "Stakeholder approval — named Director+ approver"
    description: "Pending: Adeel Ali (Inventor). Self-cert prohibited."
    status: wait
    laws: [PRD-2.1, PRD-2.5, BUS-7.1]
  - title: "HTML render gate — APPROVED in browser"
    description: "Awaiting ticked APPROVE in §Render Gate of source PROPOSAL.md."
    status: wait
    laws: [ENG-13.1]
  - title: "BUS-7.1 audit event filed — Stage A → B transition"
    description: "Will append automatically on APPROVE."
    status: wait
    laws: [BUS-7.1]

# Audit log
audit_log:
  - event: "Stage A — Initialized"
    actor: "Amal"
    role: "Product Coach"
    system: "Claude Code / Constitution MCP"
    timestamp: "2026-04-17"
    outcome: "IN_PROGRESS"
  - event: "proposal.md drafted"
    actor: "Amal"
    role: "Product Coach"
    system: "Hangar AI Constitution"
    timestamp: "2026-04-17"
    outcome: "DRAFTED"
  - event: "HTML artifact rendered"
    actor: "aa-artifact-render"
    role: "Renderer (ENG-13.1)"
    system: "Hangar AI Constitution"
    timestamp: "2026-04-17"
    outcome: "RENDERED"
  - event: "Stage A → B"
    actor: "Adeel Ali"
    role: "Inventor / Approver"
    system: "manual"
    timestamp: "TBD"
    outcome: "AWAITING"

# Render gate state — reads from §Render Gate checkbox in body
render_gate:
  status: pending
  reviewer: ""
  timestamp: ""

# Spec artifacts (file list, sidebar)
spec_artifacts:
  - filename: "proposal.md"
    icon: "📄"
    status: "DRAFTED"
  - filename: "workflow-state.md"
    icon: "📄"
    status: "OK"
  - filename: "stage-a-discovery-rendered.html"
    icon: "🌐"
    status: "RENDERED"
  - filename: "audit.yaml"
    icon: "📋"
    status: "WAIT"

# Avatars (sidebar)
avatars:
  - name: "product"
    icon: "🎯"
    context: "constitutional context"
  - name: "business"
    icon: "💼"
    context: "constitutional context"
  - name: "avatar-product-loyalty"
    icon: "✈️"
    context: "AAdvantage · 180M members · 5 journeys"

# Stakeholder approval (sidebar)
stakeholder:
  approver: "Adeel Ali"
  title: "Inventor, Hangar AI Constitution"
  date: "Pending"
  method: "In-session workshop review"
  self_cert: false

footer_id: disc-2026-042
footer_project: "AAdvantage Partner-Miles Posting"
---

# Discovery Proposal: AAdvantage Partner-Miles Posting — Trust Gap

> ⚠️ **Honest framing — workshop demo.** This Stage A proposal was drafted by **Amal (Product Coach)** from the AAdvantage loyalty avatar and competitive pattern knowledge — **not from member research.** Stage A output is a *hypothesis*. Its job is to be contestable. If Stage B research contradicts it, the hypothesis dies — and that is a good outcome.

---

## Hypothesis Statement

> We believe that **providing a real-time posting-status tracker for partner-airline miles**
> will result in **higher retention among Gold and Platinum members and lower "where are my miles" support-call volume**
> for **frequent travelers who fly at least one partner segment per quarter.**

---

## Open Questions — Stage B Marching Orders

1. Is the pain the **delay** itself, or the **silence** during the delay? Would members accept a 4-week window if they had in-flight visibility?
2. Which **partner segments** are most affected — leisure partners (e.g., British Airways) or business partners (e.g., Japan Airlines)?
3. What **specific moment** causes members to lose trust — day 7? day 14? first support call?
4. How often do members **call support** specifically about partner miles, and what fraction of total support volume is that?
5. What do **Delta / United members** say about their trackers? Do trackers actually reduce complaints, or just change their shape?

---

## Scope

| In Scope | Out of Scope |
|----------|-------------|
| Partner-airline mile posting experience (oneworld + codeshare) | AA-metal flight earning (already real-time) |
| Member-facing visibility of posting state | Actually reducing the posting window (mainframe work — separate initiative) |
| Gold / Platinum / Elite member retention impact | Redemption-side UX |
| Support-call cost reduction | Acquisition funnel changes |
| Compliance surface (PCI / GDPR / retention) | Partner-contract renegotiation |

---

## Render Gate (ENG-13.1)

> **NON-NEGOTIABLE:** The reviewer ticks **exactly one** decision below and fills in the metadata. Source-of-truth for the gate decision is **this file**, not the rendered HTML.

- [ ] ✅ **APPROVE** — artifact is complete, accurate, law-compliant; Stage B may begin
- [ ] 🔄 **ENHANCE** — artifact needs targeted improvement; agent re-renders (max 3 rounds)
- [ ] ❌ **REJECT** — artifact has a blocker; document below and do NOT advance

| Field | Value |
|-------|-------|
| **Reviewer name** | _pending_ |
| **Reviewer role** | Inventor, Hangar AI Constitution (Director+) |
| **Decision timestamp** | _pending_ |
| **Review method** | In-browser render, workshop session |
| **Self-cert?** | No — initiator (Amal) ≠ reviewer (Adeel) |
| **Blocker (if REJECT)** | N/A |
| **Enhancement request (if ENHANCE)** | N/A |
