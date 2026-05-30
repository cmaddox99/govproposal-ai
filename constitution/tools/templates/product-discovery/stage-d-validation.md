---
# Stage D — Internal Validation — Product Discovery Stage A–F
# Governed by: PRD-2.1, PRD-2.2, BUS-7.1, ENG-13.1
# Usage: Copy to hangar-ai-specs/changes/[discovery-id]/stage-d-validation.md
#        Replace all <PLACEHOLDER> values before advancing to Stage E.
# Example (rendered): tools/templates/product-discovery/examples/partner-miles-reference/stage-d-validation.html

id: disc-YYYY-NNN
spec_id: disc-YYYY-NNN
type: discovery
stage: D
stage_label: Internal Validation
status: IN_PROGRESS
created: YYYY-MM-DD
branch: <git-branch-name>
workflow: product-discovery-stage-a-f
workflow_version: "2.1.0"
skill: skill-product-discovery-orchestration
title: "<Short Title — e.g. AADvantage Loyalty Platform — Internal Validation>"

mode: Exploratory                        # Exploratory | Accelerated
tier: Tier 2                             # Tier 1 | Tier 2

laws:
  - PRD-2.1
  - PRD-2.2
  - BUS-7.1
  - ENG-13.1

laws_applied:
  - PRD-2.1
  - PRD-2.2
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
    status: active
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
      Stage C Code Evidence approved. No unreviewed critical findings.
      Technical feasibility confirmed. Stage D validation initiated.
  exit:
    status: pending
    description: >
      Awaiting all blockers resolved and DVFT matrix complete.
      Human browser review and BUS-7.1 audit event required before Stage E.
stakeholder:
  approver: "<Full name>"
  title: "<Role — e.g. Director, Product | Discovery Sponsor>"
  date: "<YYYY-MM-DD>"
  method: "<In-person | Async written | PR review | Email>"
  self_cert: false
# ---------------------------------------------------------------------------
# CROSS-STAGE EVIDENCE MAP (PRD-2.1 · PRD-2.2 · BUS-7.1)
# Every assumption marked Validated or Invalidated MUST have ≥1 entry in
# assumption_citations referencing upstream evidence from Stages A, B, or C.
#
# Allowed ref formats: SRC-A-NNN · SRC-B-NNN · EVI-C-NNN
#   SRC-A-NNN — problem evidence from Stage A
#   SRC-B-NNN — field study source from Stage B
#   EVI-C-NNN — code evidence glossary entry from Stage C
#
# evaluated_by / evaluated_at: BUS-7.1 attribution for the validation decision
# ---------------------------------------------------------------------------
assumption_citations:
  - assumption_id: "A1"             # stable ID matching DVFT matrix # column
    assumption: "<Short label — e.g. 'Users want real-time earning visibility'>"
    status: Validated               # Validated | Invalidated | Untested
    evaluated_by: "<Full name · YYYY-MM-DD or 'GitHub Copilot CLI · YYYY-MM-DD (pending human review)'>"
    supporting_evidence:
      - ref: "SRC-B-001"            # SRC-A-*, SRC-B-*, or EVI-C-* all valid
        how: "<How this source validates/refutes this assumption>"
      - ref: "EVI-C-002"
        how: "<How this code evidence validates/refutes>"
    confidence: High               # High | Medium | Low

  - assumption_id: "A2"
    assumption: "<label>"
    status: Untested
    evaluated_by: "<GitHub Copilot CLI · YYYY-MM-DD (pending human review)>"
    supporting_evidence: []         # empty for Untested
    confidence: Low

  # Add more: A3, A4, … matching all rows in DVFT matrix
avatars:
  - icon: "🎯"
    name: "product"
    context: "constitutional context"
  - icon: "💼"
    name: "business"
    context: "constitutional context"
spec_artifacts:
  - icon: "📄"
    filename: "stage-d-validation.md"
    status: "DRAFTED"
  - icon: "🌐"
    filename: "stage-d-validation.html"
    status: "PENDING"

exit_checklist:
  - title: "DVFT Assumption Matrix completed — all assumptions logged"
    laws: ["PRD-2.2"]
    status: pend
  - title: "All 4 PRD-2.1 problem validation dimensions confirmed with evidence"
    laws: ["PRD-2.1"]
    status: pend
  - title: "Stakeholder review conducted with named Product Owner"
    laws: ["PRD-2.5"]
    status: pend
  - title: "All critical blockers resolved or have explicit owner and path"
    laws: ["PRD-2.5"]
    status: pend
  - title: "assumption_citations populated — all Validated/Invalidated assumptions carry ≥1 cross-stage evidence ref (SRC-A-NNN, SRC-B-NNN, or EVI-C-NNN) with evaluated_by"
    laws: ["PRD-2.2", "BUS-7.1"]
    status: pend
  - title: "No assumption marked Validated or Invalidated has an empty supporting_evidence list"
    laws: ["PRD-2.1", "BUS-7.1"]
    status: pend
  - title: "stage-d-validation.md rendered via aa-artifact-render and APPROVED in browser"
    laws: ["ENG-13.1"]
    status: pend
  - title: "BUS-7.1 audit event filed — Stage D → E transition"
    laws: ["BUS-7.1"]
    status: pend

audit_log:
  - event: "Stage D — Internal Validation initiated"
    actor: "<name>"
    role: "<role>"
    system: "GitHub Copilot CLI"
    timestamp: "<YYYY-MM-DDTHH:MM:SSZ>"
    outcome: "IN_PROGRESS"
  - event: "Stage D → E"
    actor: "<name>"
    role: "<role>"
    system: "<…>"
    timestamp: "<YYYY-MM-DDTHH:MM:SSZ>"
    outcome: "AWAITING"

---

# Stage D Internal Validation: <Short Title>

---

## DVFT Assumption Matrix (PRD-2.2)

| ID | Assumption | Desirability | Viability | Feasibility | Testability | Status |
|----|-----------|:-----------:|:---------:|:-----------:|:-----------:|--------|
| A1 | <assumption> | H/M/L | H/M/L | H/M/L | H/M/L | Validated / Invalidated / Untested |
| A2 | <assumption> | H/M/L | H/M/L | H/M/L | H/M/L | Validated / Invalidated / Untested |

---

## Problem Validation Summary (PRD-2.1)

| Dimension | Evidence | Confidence |
|-----------|----------|:----------:|
| Problem exists | <evidence> | H/M/L |
| Problem matters | <evidence> | H/M/L |
| Problem is solvable | <evidence> | H/M/L |
| Users will exchange value | <evidence> | H/M/L |

---

## Cross-Stage Evidence Map (PRD-2.2 · BUS-7.1)

> Each Validated or Invalidated assumption below is backed by traceable upstream evidence.
> Use assumption IDs (A1, A2, …) to reference rows in the DVFT matrix above.

| ID | Assumption | Status | Supporting Evidence | Confidence | Evaluated By |
|----|-----------|:------:|---------------------|:----------:|-------------|
| A1 | <label> | Validated | SRC-B-001 — <how> | 🟢 High | <name · date> |
| A2 | <label> | Untested | — | 🔴 Low | — |

> **Exit gate requirement (PRD-2.2 · BUS-7.1):** Every Validated or Invalidated assumption must have ≥1 upstream evidence reference. All `evaluated_by` fields must name the decision-maker and date (BUS-7.1).

---

## Stakeholder Review

| Stakeholder | Role | Feedback | Blockers Raised |
|------------|------|----------|----------------|
| <name> | <role> | <feedback summary> | <blockers or "None"> |

---

## Blocker Resolution

| Blocker | Owner | Resolution | Status |
|---------|-------|-----------|:------:|
| <blocker> | <name> | <how resolved> | ✅ Resolved / ⬜ Open |

> **Exit gate requirement:** All blockers resolved before advancing.
