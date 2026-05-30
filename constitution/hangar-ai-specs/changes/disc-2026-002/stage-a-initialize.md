---
# Stage A — Initialize — Product Discovery v2.0.0
# Governed by: ENG-11.2, PRD-2.1, PRD-2.5, BUS-7.1, ENG-13.1

id: disc-2026-002
spec_id: disc-2026-002
type: discovery
stage: A
stage_label: Initialize
status: IN_PROGRESS
created: 2026-04-18
branch: disc-2026-002-loyalty-platform-discovery
workflow: product-discovery-stage-a-f
workflow_version: "2.0.0"
skill: skill-product-discovery-orchestration
title: "AADvantage Loyalty Platform — Member Experience Modernization"
template_version: "1.0.0"
template_path: "tools/templates/product-discovery/stage-a-proposal.md"
example_path: "tools/templates/product-discovery/examples/partner-miles-reference/stage-a-proposal.html"
avatar_path: "avatars/product-type/loyalty-aadvantage/"

mode: Exploratory
tier: Tier 2

laws:
  - PRD-2.1
  - PRD-2.5
  - BUS-7.1
  - ENG-11.1
  - ENG-11.2
  - ENG-13.1
  - PRD-1.1
  - PRD-3.1
  - PRD-4.1
  - PRD-6.1

laws_applied:
  - PRD-2.1
  - PRD-2.5
  - BUS-7.1
  - ENG-13.1
  - ENG-11.1
  - PRD-1.1
  - PRD-3.1
  - PRD-6.1

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

gates:
  entry:
    status: met
    description: >
      Loyalty platform member experience modernisation opportunity surfaced
      from loyalty-aadvantage avatar. Three measurable failure modes confirmed
      via internal analytics and member research (Q3–Q4 2025, Feb 2026).
      Exploratory discovery initiated 2026-04-18.
  exit:
    status: pending
    description: >
      Awaiting stakeholder approval in §Stakeholder Approval from named
      Director+ approver. Initiator is Amal (Product Coach) —
      self-certification prohibited by PRD-2.5.

mode_selection:
  selected: Exploratory
  rationale: >
    No prior validated problem statement exists across all four PRD-2.1
    dimensions. Known metrics surface pain points but fresh evidence is
    required. All 4 PRD-2.1 dimensions closed with avatar-grounded content.

tier_selection:
  tier: Tier 2
  rationale: >
    5/5 complexity rubric Yes. Spans points engine, redemption surface,
    partner integration layer, elite status service, and member data
    platform across 2+ teams. Multi-quarter timeline. Financial loyalty
    regulatory surface (PCI, data retention).
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
  approver: "<Full name>"
  title: "<Role / Title>"
  date: "<YYYY-MM-DD>"
  method: "<pending>"
  self_cert: false

spec_artifacts:
  - icon: "📄"
    filename: "stage-a-initialize.md"
    status: "DRAFTED"
  - icon: "🌐"
    filename: "stage-a-initialize.html"
    status: "RENDERED"
  - icon: "📋"
    filename: "package-index.md"
    status: "PENDING"

avatars:
  - icon: "✈️"
    name: "loyalty-aadvantage"
    context: "avatars/product-type/loyalty-aadvantage/ · AAdvantage · 180M members"
  - icon: "🎯"
    name: "product"
    context: "constitutional context"
  - icon: "💼"
    name: "business"
    context: "constitutional context"

findings:
  - title: "Three failure modes confirmed with quantitative data"
    description: "Redemption abandonment (62%), elite advancement gap (25%→35% opportunity), elite churn (82% vs 95% target) — all measured Q3-Q4 2025."
    laws: ["PRD-2.1"]
    status: done
  - title: "Internal prototypes confirm solvability"
    description: "Recommended-for-You moved casual completion 45%→62%; progress tracker hit 48% weekly engagement vs 40% target."
    laws: ["PRD-2.5"]
    status: done
  - title: "Avatar roadmap scores validated — Stage B prioritisation ready"
    description: "loyalty-aadvantage scores: elite tracker (93), mobile redesign (88), award seat expansion (88), elite concierge (86), points gifting (83)."
    status: done
  - title: "Blocker — stakeholder approval not yet obtained"
    description: "Director+ approval required before Stage B. Schedule Stage A review."
    laws: ["PRD-2.5", "BUS-7.1"]
    status: wait

problem_validation:
  dim1:
    label: "1. Problem Exists"
    text: "180M+ member base failing to convert enrollment to engagement. Three measurable failure modes: 62% redemption abandonment, 25% elite achievement rate, 82% Platinum renewal vs 95% target."
    status: ok
  dim2:
    label: "2. Problem Matters"
    text: "$40M/year unredeemed points trust erosion, $100M/year elite advancement opportunity, $2M/year elite churn to competitors. AA is now a digital experience laggard vs United/Delta."
    status: ok
  dim3:
    label: "3. Problem Is Solvable"
    text: "All 5 bounded contexts in production. Internal prototypes hit targets. loyalty-aadvantage avatar provides validated law library, persona set, and roadmap scoring framework."
    status: ok
  dim4:
    label: "4. Users Will Exchange Value"
    text: "62% completion with recommendations vs 45% baseline. 48% weekly engagement on progress tracker. Elite concierge pilot: 100% 1-year retention, 9.2/10 NPS."
    status: ok

exit_checklist:
  - title: "Discovery ID assigned: disc-2026-002"
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
  - title: "Tier 2 declared — all 5 rubric questions Yes"
    laws: ["PRD-2.5"]
    status: done
  - title: "Mode (Exploratory) declared in frontmatter and narrative"
    laws: ["PRD-2.5"]
    status: done
  - title: "Loyalty-AADvantage, Product, and Business avatars activated"
    laws: ["PRD-2.5", "BUS-7.1"]
    status: done
  - title: "Stakeholder approval obtained from named Director+"
    description: "Self-certification prohibited by PRD-2.5."
    laws: ["PRD-2.1", "PRD-2.5"]
    status: wait
  - title: "Stakeholder approval recorded in §Stakeholder Approval"
    laws: ["PRD-2.5"]
    status: wait
  - title: "All open blockers from Initial Findings resolved"
    laws: ["PRD-2.5"]
    status: wait
  - title: "package-index.md created with Tier 2 manifest"
    laws: ["ENG-11.1"]
    status: wait
  - title: "stage-a-initialize.md rendered via aa-artifact-render and APPROVED in browser"
    laws: ["ENG-13.1"]
    status: wait
  - title: "BUS-7.1 audit event filed — Stage A → B transition"
    laws: ["BUS-7.1"]
    status: wait

audit_log:
  - event: "Stage A — Initialized"
    actor: "Adeel Ali"
    role: "Discovery Sponsor"
    system: "GitHub Copilot CLI"
    timestamp: "2026-04-18T04:15:00Z"
    outcome: "IN_PROGRESS"
  - event: "Stage A → B"
    actor: "<name>"
    role: "<role>"
    system: "<…>"
    timestamp: "<YYYY-MM-DDTHH:MM:SSZ>"
    outcome: "AWAITING"

---

# Discovery Proposal: AADvantage Loyalty Platform — Member Experience Modernization

---

## Problem Statement

> **PRD-2.1 — Problem Validation Law:** All problems MUST be validated before solution design.
> Complete all four dimensions below before proceeding.

### 1. Problem Exists

AADvantage has 180M+ enrolled members but is failing to convert enrollment into sustained engagement and redemption. Three measurable failure modes exist today:

- **Redemption abandonment:** 62% of casual members abandon award redemption mid-flow — unable to identify a relevant option across 12 undifferentiated search results (internal analytics, Q4 2025).
- **Elite advancement gap:** Only 25% of frequent travelers achieve elite status; 30% drop out at Month 7 unaware they are within reach (member survey, Feb 2026).
- **Elite churn:** Platinum 1-year renewal rate is 82% vs. 95% target — churned elites cite declining perceived value and lounge experience quality (churn interviews, Q3 2025).

### 2. Problem Matters

- Redemption abandonment costs **$40M/year** in unredeemed points that erode program trust.
- The elite advancement gap represents a **$100M/year opportunity** — closing 25% → 35% adds ~210K elite members × $500 LTV.
- Elite churn at current rate costs an estimated **$2M/year** in high-LTV members switching to United MileagePlus or Delta SkyMiles.
- AA is now a digital experience laggard: United and Delta modernised award search and redemption UX in 2024–2025. Inaction deepens the gap.

### 3. Problem Is Solvable

All five bounded contexts already exist in production — no net-new infrastructure required. Internal prototypes confirm feasibility: a "Recommended for You" redemption feature moved casual completion from 45% → 62% in a constrained test (Q2 2025); the elite progress tracker beta hit 48% weekly engagement vs. 40% target. The loyalty-aadvantage avatar provides a validated PRD law application library, persona set, and roadmap scoring framework specific to this domain.

### 4. Users Will Exchange Value

- Casual members complete redemption at 62% when shown relevant recommendations vs. 45% baseline — they will invest attention for relevant awards.
- Frequent travelers engaged with the progress tracker at 48% weekly active rate — they will invest regular check-ins to track elite advancement.
- Elite concierge pilot with 50 platinum members delivered 100% 1-year retention and 9.2/10 NPS — they will exchange loyalty for restored perceived value.

---

## Scope

| In Scope | Out of Scope |
|----------|-------------|
| Redemption search and award discovery experience (casual member) | New partner contract negotiation |
| Elite progress tracking and advancement communications (frequent traveler) | Points earn-rate or pricing changes (commercial decision) |
| Elite retention and perceived-value experience (elite member) | Credit card co-brand product terms |
| Member-facing mobile and web surfaces across all three journey types | Back-office partner settlement systems |
| Points engine read APIs powering the redemption surface | Infrastructure re-platforming |
| Real-time elite status data flows to member-facing surfaces | Non-loyalty AA products (cargo, check-in, etc.) |
| Metric rebaseline: NPS, redemption rate, elite achievement, retention | International regulatory compliance outside US |
