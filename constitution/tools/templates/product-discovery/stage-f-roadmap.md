---
# Stage F — Roadmap Lock — Product Discovery Stage A–F
# Governed by: PRD-4.1, PRD-4.2, ENG-11.1, BUS-7.1, ENG-13.1, ENG-13.3
# Usage: Copy to hangar-ai-specs/changes/[discovery-id]/stage-f-roadmap.md
#        Replace all <PLACEHOLDER> values. PDF required (ENG-13.3).
# Example (rendered): tools/templates/product-discovery/examples/partner-miles-reference/stage-f-roadmap.html

id: disc-YYYY-NNN
spec_id: disc-YYYY-NNN
type: discovery
stage: F
stage_label: Roadmap Lock
status: IN_PROGRESS
created: YYYY-MM-DD
branch: <git-branch-name>
workflow: product-discovery-stage-a-f
workflow_version: "2.1.0"
skill: skill-product-discovery-orchestration
title: "<Short Title — e.g. AADvantage Loyalty Platform — Roadmap Lock>"

mode: Exploratory                        # Exploratory | Accelerated
tier: Tier 2                             # Tier 1 | Tier 2

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
      Stage E Metric Rebaseline approved. Success metrics and PMF targets
      confirmed measurable. Stage F roadmap lock and implementation proposal initiated.
  exit:
    status: pending
    description: >
      Awaiting roadmap approved, Slice 1 brief complete, PDF generated (ENG-13.3).
      Human browser review and BUS-7.1 audit event required to close discovery.
stakeholder:
  approver: "<Full name>"
  title: "<Role — e.g. Director, Product | Discovery Sponsor>"
  date: "<YYYY-MM-DD>"
  method: "<In-person | Async written | PR review | Email>"
  self_cert: false
# ---------------------------------------------------------------------------
# DECISION TRACEABILITY — ROADMAP RATIONALE (PRD-4.1 · PRD-4.2 · BUS-7.1)
# Every Now, Next, AND Later horizon initiative MUST have ≥1 driven_by entry
# linking it to upstream discovery evidence.
#
# Allowed ref formats:
#   SRC-A-NNN — Stage A problem evidence
#   SRC-B-NNN — Stage B field study source
#   EVI-C-NNN — Stage C code evidence glossary entry
#   BSL-E-NNN — Stage E baseline source
#   A1/A2/…   — Stage D validated/invalidated assumption ID
#
# driven_by.type values:
#   user_insight | tech_debt | market_signal | compliance | metric_gap | assumption
#
# rationale_confidence:
#   High   — direct evidence from ≥2 prior stages (Now/Next expected to be High/Medium)
#   Medium — single-stage evidence, reasonable extrapolation
#   Low    — hypothesis or bet; acceptable for Later horizon items
# ---------------------------------------------------------------------------
roadmap_rationale:
  - initiative_id: "NOW-1"          # stable ID matching Initiative column in roadmap table
    initiative: "<initiative label>"
    horizon: "Now"                  # Now | Next | Later
    driven_by:
      - ref: "SRC-B-001"            # Any upstream ref is valid
        type: user_insight
        reason: "<Why this insight motivates this initiative>"
      - ref: "EVI-C-002"
        type: tech_debt
        reason: "<Why this tech debt requires this initiative>"
    addresses_assumption: "A1"      # optional — Stage D assumption_id
    moves_metric: "M1"              # optional — Stage E metric_id
    rationale_confidence: High      # High | Medium | Low

  - initiative_id: "NEXT-1"
    initiative: "<initiative label>"
    horizon: "Next"
    driven_by:
      - ref: "SRC-B-002"
        type: user_insight
        reason: "<reason>"
    addresses_assumption: "A2"
    moves_metric: "M2"
    rationale_confidence: Medium

  - initiative_id: "LATER-1"
    initiative: "<initiative label>"
    horizon: "Later"
    driven_by:
      - ref: "SRC-A-001"
        type: market_signal
        reason: "<reason — Low confidence is acceptable for Later>"
    rationale_confidence: Low

  # Add more: NOW-2, NEXT-2, LATER-2 …
avatars:
  - icon: "🎯"
    name: "product"
    context: "constitutional context"
  - icon: "💼"
    name: "business"
    context: "constitutional context"
spec_artifacts:
  - icon: "📄"
    filename: "stage-f-roadmap.md"
    status: "DRAFTED"
  - icon: "🌐"
    filename: "stage-f-roadmap.html"
    status: "PENDING"

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
  - title: "roadmap_rationale populated — all Now, Next, AND Later initiatives carry ≥1 driven_by evidence reference"
    laws: ["PRD-4.1", "PRD-4.2", "BUS-7.1"]
    status: pend
  - title: "All driven_by refs are traceable to upstream evidence (SRC-A-NNN, SRC-B-NNN, EVI-C-NNN, BSL-E-NNN, or validated assumption ID)"
    laws: ["PRD-4.2", "BUS-7.1"]
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
    actor: "<name>"
    role: "<role>"
    system: "GitHub Copilot CLI"
    timestamp: "<YYYY-MM-DDTHH:MM:SSZ>"
    outcome: "IN_PROGRESS"
  - event: "Stage F → Complete"
    actor: "<name>"
    role: "<role>"
    system: "<…>"
    timestamp: "<YYYY-MM-DDTHH:MM:SSZ>"
    outcome: "AWAITING"

---

# Stage F Roadmap Lock: <Short Title>

---

## Outcome Framing (PRD-4.1)

| Outcome | Metric | Target | Timeline |
|---------|--------|--------|----------|
| <desired outcome> | <how measured> | <quantitative target> | <timeframe> |

---

## Decision Traceability (PRD-4.1 · PRD-4.2 · BUS-7.1)

> Every roadmap initiative is grounded in upstream discovery evidence.
> `[SRC-A-NNN]` · `[SRC-B-NNN]` · `[EVI-C-NNN]` · `[BSL-E-NNN]` · Assumption `A#` can all be cited.

| Initiative (ID) | Horizon | Driven By | Type | Rationale |
|----------------|:-------:|-----------|------|-----------|
| <initiative> (NOW-1) | Now | SRC-B-001 | User Insight | <reason> |
| <initiative> (NEXT-1) | Next | EVI-C-002 | Tech Debt | <reason> |
| <initiative> (LATER-1) | Later | SRC-A-001 | Market Signal | <reason> |

> **Exit gate requirement (PRD-4.2 · BUS-7.1):** ALL horizon initiatives (Now, Next, and Later) must have ≥1 evidence reference. Later items may carry Low confidence. Roadmap decisions not backed by discovery evidence CANNOT be advanced.

---

## Roadmap — Now / Next / Later (PRD-4.2)

### Now (0–4 weeks)

| ID | Initiative | Vertical Slice | Effort Estimate | Owner |
|----|-----------|---------------|:---------------:|-------|
| NOW-1 | <initiative> | <slice description> | <S/M/L> | <team/person> |

### Next (4–12 weeks)

| ID | Initiative | Vertical Slice | Effort Estimate | Dependencies |
|----|-----------|---------------|:---------------:|-------------|
| NEXT-1 | <initiative> | <slice description> | <S/M/L> | <dependencies> |

### Later (12+ weeks)

| ID | Initiative | Why Later | Prerequisite |
|----|-----------|----------|-------------|
| LATER-1 | <initiative> | <rationale for deferral> | <what must happen first> |

---

## Implementation Proposal

> The implementation proposal scaffolds the next workflow phase (greenfield-development or legacy-rescue).

| Field | Value |
|-------|-------|
| Implementation ID | <impl-id> |
| Workflow | <greenfield-development / legacy-rescue-refactor / legacy-rescue-rewrite> |
| First vertical slice | <slice description> |
| Estimated effort | <S/M/L or time estimate> |
| Success criteria | <how we know slice 1 is done> |
| Implementation spec | `hangar-ai-specs/changes/[impl-id]/PROPOSAL.md` |

---

## Executive Approval

> **Required reviewer:** Executive Sponsor + Product Owner

| Field | Value |
|-------|-------|
| **Approver Name** | <full name> |
| **Role / Title** | <Executive Sponsor / VP / Director> |
| **Approval Date** | <YYYY-MM-DD> |
| **Approval Form** | <In-person / Async / PR review> |
| **Conditions** | <conditions or "None"> |
| **Status** | ⬜ Pending / ✅ Approved / ❌ Rejected |
