---
type: discovery
id: disc-2026-042
spec_id: disc-2026-042
stage: F
stage_label: Roadmap Lock
status: APPROVED
created: 2026-04-17
branch: exploratory-demo
workflow: product-discovery
workflow_version: "2.0.0"
skill: skill-product-discovery-orchestration
title: "AAdvantage Partner-Miles Posting — Roadmap Lock + Implementation Proposal"

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
      All five prior stages approved. Stage E AARRR funnel finalized
      with concrete PMF criteria (M2 ≥ 35% AND M4 ≥ −20% at Day 90).
      Stage D RED finding (retention) properly isolated as hypothesis,
      not roadmap commitment.
  exit:
    status: pending
    description: >
      Awaiting §Render Gate APPROVE + executive-sponsor sign-off.
      Implementation proposal handed off to greenfield-development
      workflow Phase 1 (Capture).

mode_selection:
  selected: Exploratory
  rationale: "Mode locked at Stage A."

tier_selection:
  tier: Tier 2
  rationale: "Tier 2 carried; full slice-1-ready brief + executive briefing."

problem_validation:
  dim1:
    label: "1. Problem Exists"
    status: ok
    text: "Validated. Carried."
  dim2:
    label: "2. Problem Matters"
    status: ok
    text: "Validated. $2.4M annual support cost baseline."
  dim3:
    label: "3. Problem Is Solvable"
    status: ok
    text: "Validated. Extend ledger + member-app, no mainframe changes."
  dim4:
    label: "4. Users Will Exchange Value"
    status: ok
    text: "Validated. 7/8 concept-test adoption signal."

domain_landscape_title: "Roadmap — Now / Next / Later (PRD-4.2)"
domains:
  - name: "NOW (Q2 2026 — 6-week slice)"
    icon: "🚀"
    header_bg: "#f0fdf4"
    header_color: "#166534"
    role: "Read-only partner-miles status tracker, Gold-tier rollout"
    stack: "aa-loyalty-ledger GraphQL + aa-member-app screen + LaunchDarkly flag"
    submodules: "Slice 1"
    tags:
      - {text: "Validated", tone: "green"}
      - {text: "Hand off to Greenfield Phase 1", tone: "green"}
      - {text: "PMF target: Day 90", tone: "green"}
  - name: "NEXT (Q3 2026)"
    icon: "📡"
    header_bg: "#eff6ff"
    header_color: "#1d4ed8"
    role: "Push notifications when partner miles transition to POSTED state"
    stack: "aa-member-comms integration + consent gating per GDPR"
    submodules: "Slice 2"
    tags:
      - {text: "Conditional on Slice-1 PMF", tone: "blue"}
      - {text: "Comms platform reuse", tone: "blue"}
  - name: "NEXT (Q3 2026)"
    icon: "🧪"
    header_bg: "#f5f3ff"
    header_color: "#5b21b6"
    role: "Matched-cohort A/B for retention lift hypothesis (resolves DVFT-A3)"
    stack: "Loyalty Strategy ownership · Q3 design · Q4–Q1 execution"
    submodules: "Experiment"
    tags:
      - {text: "Resolves RED claim", tone: "purple"}
      - {text: "No promise; measurement", tone: "purple"}
  - name: "LATER (Q1 2027+)"
    icon: "⏳"
    header_bg: "#fffbeb"
    header_color: "#92400e"
    role: "Mainframe partner-feed real-time integration (reduces window from 4-6w to <72h)"
    stack: "Mainframe + partner-feed-ingest rewrite · multi-quarter"
    submodules: "Slice 3"
    tags:
      - {text: "Big bet — separate initiative", tone: "yellow"}
      - {text: "Conditional on partner contracts", tone: "yellow"}
      - {text: "Skip if NOW solves enough", tone: "yellow"}

arch_title: "Slice 1 Architecture — What Greenfield Phase 1 Will Build"
arch_flow: |
  Member opens AA app
        ↓
        aa-member-app (React Native)
        ↳ NEW: <PartnerMilesTracker /> screen, behind 'partner-miles-tracker' LaunchDarkly flag
        ↳ Gold-tier cohort first (10% → 50% → 100% over 4 weeks)

  GraphQL query: partnerEarnings(memberId, limit: 10, status: ['PENDING', 'PROCESSING', 'POSTED'])
        ↓
        aa-loyalty-ledger (Java)
        ↳ NEW: partnerEarnings root field on the ledger schema
        ↳ Reads existing PartnerEarningTransaction.status enum (no schema change)

  Returns ordered list of transactions with:
        - flight (carrier, route, date)
        - status (PENDING / PROCESSING / POSTED / REJECTED)
        - estimatedPostBy (computed from posting SLA)
        - lastUpdated (audit timestamp)

  Member sees: "Your Iberia MAD-MIA flight from April 7 — Processing — expected by April 28"

  Observability instrumentation (resolves DVFT-A2):
        - Mixpanel events: tracker_viewed, tracker_opened, tracker_returned
        - CX call-reason 'partner_miles' → linked to most-recent member tracker state at time of call
        - Looker dashboard 'partner-miles-cx' surfaces M1–M4 daily

findings_title: "Implementation Proposal — Handoff to Greenfield Phase 1"
findings:
  - title: "Slice 1 estimate: 4–6 engineer-weeks (Now bucket)"
    description: "aa-loyalty-ledger: 2ew (GraphQL field + tests). aa-member-app: 2-3ew (screen + flag + a11y). Observability: 1ew. Phased rollout: 1-2 calendar weeks."
    status: done
    laws: [PRD-4.2]
  - title: "Outcome framing (PRD-4.1): 'Members can see their partner miles processing'"
    description: "Single-sentence outcome. Replaces feature framing ('build a tracker'). Connects directly to Stage B JTBD ('know my earning is safe')."
    status: done
    laws: [PRD-4.1]
  - title: "Slice-1-ready brief filed for Greenfield Phase 1 ingestion"
    description: "tools/templates/product-discovery/slice-1-ready-brief.md filled. Includes: outcome, primary user, slice scope, success metric (M2 + M4), out-of-scope, dependencies."
    status: done
    laws: [PRD-4.2, ENG-11.1]
  - title: "Out-of-scope for Slice 1 (defended explicitly)"
    description: "Push notifications (Q3 Next), reducing posting window (Later), redemption-side UX (out of program scope), partner-side push integration (architecturally avoided)."
    status: done
    laws: [PRD-4.2]
  - title: "Stage F PDF generated for executive sign-off (ENG-13.3)"
    description: "PDF rendered via aa-artifact-render --pdf. PDF is the formal review surface for the executive sponsor and CFO delegate."
    status: done
    laws: [ENG-13.3]
  - title: "Implementation handoff target: greenfield-development workflow Phase 1 (Capture)"
    description: "implementation-proposal.md becomes the Capture-phase input. Workflow continuity preserved."
    status: done
    laws: [ENG-11.1]

ensemble_verdict:
  verdicts:
    - persona: Amal (Product Coach)
      law: PRD-4.1
      note: "Outcome-framed, not feature-framed. Slice-1 scope is the smallest defensible thing that tests the core hypothesis (visibility > speed) and produces measurable PMF signal."
      verdict: PASS
    - persona: Amal (Product Coach)
      law: PRD-4.2
      note: "Now/Next/Later structure honest. RED-tagged retention claim sits in Next as an experiment, not in Now as a promise. Later bucket explicitly conditional on Now performance."
      verdict: PASS
    - persona: Amaya (Technical Coach)
      law: ENG-11.1
      note: "Implementation proposal hands cleanly to greenfield-development Phase 1. Architecture diagram + observability instrumentation gate are concrete. Estimate is bottom-up from Stage C codebase assessment."
      verdict: PASS
    - persona: Sentinel
      law: BUS-7.1
      note: "Audit trail intact across all 6 stages. Compliance sign-offs (PCI, GDPR, retention) carried into roadmap as constraints. Phased rollout plan is auditable per cohort."
      verdict: PASS
    - persona: Willem (Constitutional Architect)
      law: PRD-2.5
      note: "All 6 stages executed in order with appropriate gate evidence at each. PRD-2.5 satisfied. No skipping. No self-certification. Workflow is clean."
      verdict: PASS

exit_checklist:
  - title: "Now/Next/Later roadmap defined (PRD-4.2)"
    description: "1 Now slice + 2 Next slices + 1 Later bet. RED finding properly isolated."
    status: done
    laws: [PRD-4.2]
  - title: "Outcome framing applied (PRD-4.1)"
    description: "'Members can see their partner miles processing' — single sentence, replaces feature framing."
    status: done
    laws: [PRD-4.1]
  - title: "Vertical slices defined for Slice 1"
    description: "End-to-end member app screen + GraphQL field + observability + phased rollout plan."
    status: done
    laws: [PRD-4.2]
  - title: "Implementation proposal scaffolded for Greenfield Phase 1"
    description: "implementation-proposal.md ready for handoff. Outcome, scope, success metric (M2 + M4), out-of-scope, dependencies all filled."
    status: done
    laws: [ENG-11.1]
  - title: "Stage F PDF generated (ENG-13.3)"
    description: "PDF rendered alongside HTML for executive sign-off. Cross-platform reproducible."
    status: done
    laws: [ENG-13.3]
  - title: "Stakeholder approval — Executive Sponsor + Product Owner"
    description: "Pending: Adeel Ali (Discovery Sponsor) + executive sponsor delegate."
    status: wait
    laws: [PRD-2.5]
  - title: "HTML render gate — APPROVED in browser (PDF preferred for sponsor review)"
    description: "Awaiting ticked APPROVE."
    status: wait
    laws: [ENG-13.1, ENG-13.3]
  - title: "BUS-7.1 audit event filed for Stage F → workflow-complete + greenfield-development entry"
    description: "Will append on APPROVE."
    status: wait
    laws: [BUS-7.1]

audit_log:
  - event: "Stage E → F"
    actor: "Adeel Ali"
    role: "Inventor / Approver"
    system: "manual"
    timestamp: "2026-04-17"
    outcome: "APPROVED"
  - event: "Now/Next/Later roadmap drafted"
    actor: "Amal"
    role: "Product Coach"
    system: "Hangar AI Constitution"
    timestamp: "2026-04-17"
    outcome: "OK"
  - event: "Implementation proposal scaffolded"
    actor: "Amal + Amaya"
    role: "Product + Technical"
    system: "Hangar AI Constitution"
    timestamp: "2026-04-17"
    outcome: "OK"
  - event: "Stage F PDF generated for executive sign-off"
    actor: "aa-artifact-render"
    role: "Renderer (ENG-13.3)"
    system: "Hangar AI Constitution"
    timestamp: "2026-04-17"
    outcome: "RENDERED"
  - event: "Ensemble verdict computed"
    actor: "VerdictEngine"
    role: "Constitutional Ensemble"
    system: "Hangar AI Constitution"
    timestamp: "2026-04-17"
    outcome: "APPROVED"
  - event: "Workflow complete — handoff to greenfield-development"
    actor: "Adeel Ali + Executive Sponsor"
    role: "Approvers"
    system: "manual"
    timestamp: "TBD"
    outcome: "AWAITING"

render_gate:
  status: pending

spec_artifacts:
  - filename: "stage-f-roadmap.md"
    icon: "📄"
    status: "DRAFTED"
  - filename: "implementation-proposal.md"
    icon: "📄"
    status: "OK"
  - filename: "slice-1-ready-brief.md"
    icon: "📄"
    status: "OK"
  - filename: "executive-briefing-deck.html"
    icon: "🌐"
    status: "RENDERED"
  - filename: "stage-f-roadmap.html"
    icon: "🌐"
    status: "RENDERED"
  - filename: "stage-f-roadmap.pdf"
    icon: "📕"
    status: "RENDERED"

avatars:
  - name: "product"
    icon: "🎯"
    context: "lead at Stage F"
  - name: "engineering"
    icon: "🔴"
    context: "Amaya — handoff lead to Greenfield"
  - name: "business"
    icon: "💼"
    context: "Executive sponsor + CFO delegate"
  - name: "avatar-product-loyalty"
    icon: "✈️"
    context: "AAdvantage"

stakeholder:
  approver: "Adeel Ali + Executive Sponsor"
  title: "Inventor / Discovery Sponsor + Executive"
  date: "Pending"
  method: "PDF review + workshop session"
  self_cert: false

footer_id: disc-2026-042
footer_project: "AAdvantage Partner-Miles Posting · Stage F (workflow complete)"
---

# Stage F Evidence: Roadmap Lock — AAdvantage Partner-Miles Posting

> **Reference example.** Synthesized data; demonstrates a complete Stage F under the rich-card discovery template — including the handoff to greenfield-development.

---

## The single-sentence outcome (PRD-4.1)

> **"Members can see their partner miles processing."**

That replaces "build a tracker." Outcome framing forces us to measure the right thing (members seeing it) instead of the wrong thing (the tracker existing).

---

## Handoff to Greenfield Phase 1

`implementation-proposal.md` is ready as the Capture-phase input for the **greenfield-development workflow**. Slice 1 estimate: 4–6 engineer-weeks. Phased rollout: Gold-tier cohort first (10% → 50% → 100% over 4 weeks). PMF declaration target: Day 90 post-launch.

🔴 **Amaya** picks up from here when greenfield-development Phase 1 begins.

---

## Render Gate (ENG-13.1 + ENG-13.3)

> **NON-NEGOTIABLE:** Reviewer ticks exactly one decision below. Stage F additionally requires PDF for executive sign-off (ENG-13.3).

- [ ] ✅ **APPROVE** — Roadmap is ready; greenfield-development Phase 1 may begin
- [ ] 🔄 **ENHANCE** — Specific roadmap item needs sharpening
- [ ] ❌ **REJECT** — Roadmap not ready; do NOT hand off to engineering

| Field | Value |
|-------|-------|
| **Reviewer name** | _pending_ |
| **Reviewer role** | Discovery Sponsor + Executive Sponsor |
| **Decision timestamp** | _pending_ |
| **Review method** | PDF review (executive) + in-browser HTML (sponsor) |
| **Self-cert?** | No — initiator (Amal) ≠ reviewers (Adeel + executive) |
