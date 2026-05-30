---
# Stage A — Initialize — Product Discovery Stage A–F
# Governed by: ENG-11.2, PRD-2.1, PRD-2.5, BUS-7.1, ENG-13.1
# Usage: Copy this file to hangar-ai-specs/changes/disc-YYYY-NNN/stage-a-initialize.md
#        Replace all <PLACEHOLDER> values before advancing to Stage B.
# Example (rendered): tools/templates/product-discovery/examples/partner-miles-reference/stage-a-proposal.html

id: disc-YYYY-NNN
spec_id: disc-YYYY-NNN
type: discovery
stage: A
stage_label: Initialize
status: IN_PROGRESS
created: YYYY-MM-DD
branch: <git-branch-name>
workflow: product-discovery-stage-a-f
workflow_version: "2.1.0"
skill: skill-product-discovery-orchestration
title: "<Short Title — e.g. AADvantage Loyalty Platform — Member Experience Modernization>"

mode: Exploratory                        # Exploratory | Accelerated — see §Mode Selection
tier: Tier 2                             # Tier 1 | Tier 2 — see §Tier Complexity Rubric

laws:
  - PRD-2.1
  - PRD-2.5
  - BUS-7.1
  - ENG-11.1
  - ENG-11.2
  - ENG-13.1

laws_applied:                            # ≤9 laws to surface in header ribbon + sidebar
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
      <Describe what surfaced the opportunity — avatar signal, stakeholder request, competitive trigger, etc.>
  exit:
    status: pending
    description: >
      Awaiting §Stakeholder Approval from named Director+ approver.
      Self-certification prohibited by PRD-2.5.

mode_selection:
  selected: Exploratory                  # Exploratory | Accelerated
  rationale: >
    <Why this mode — e.g. no prior validated problem statement, or cite prior discovery ID if Accelerated>

tier_selection:
  tier: Tier 2                           # Tier 1 | Tier 2
  rationale: >
    <Summarise the rubric outcome and why Tier 2 applies>
  rubric:
    - question: Does the discovery span 3+ services or bounded contexts?
      answer: "Yes"                      # Yes | No
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
  title: "<Role — e.g. Director, Product | Discovery Sponsor>"
  date: "<YYYY-MM-DD>"
  method: "<In-person | Async written | PR review | Email>"
  self_cert: false
# ---------------------------------------------------------------------------
# PROBLEM EVIDENCE REGISTRY (PRD-2.1 · BUS-7.1)
# Every PRD-2.1 dimension MUST cite at least one source using the inline
# syntax [SRC-A-NNN] in the problem statement prose.
#
# source_type values:
#   stakeholder_statement | market_report | prior_discovery | complaint_data |
#   analytics | compliance_mandate | field_study | other
#
# confidence values: High | Medium | Low
#   High   — verbatim stakeholder statement, signed document, or audit finding
#   Medium — market report, analytics extract, or prior discovery reference
#   Low    — inferred from indirect signals or secondary sources
# ---------------------------------------------------------------------------
problem_evidence:
  - id: SRC-A-001
    dimension: "1. Problem Exists"   # one of the 4 PRD-2.1 dimension labels
    claim: "<The specific assertion being supported — e.g. 'Loyalty members report earning confusion as top pain point'>"
    source_type: stakeholder_statement   # see values above
    source_ref: "<doc path, URL, or prior disc-YYYY-NNN>"
    system_of_record: "<system name, 'stakeholder', or 'artifact'>"
    date: "<YYYY-MM-DD>"
    quote: "<Verbatim excerpt from the source>"
    confidence: High                     # High | Medium | Low
    confidence_rationale: "<Why this confidence level>"

  - id: SRC-A-002
    dimension: "2. Problem Matters"
    claim: "<assertion>"
    source_type: market_report
    source_ref: "<path or URL>"
    system_of_record: "<system>"
    date: "<YYYY-MM-DD>"
    quote: "<verbatim excerpt>"
    confidence: Medium
    confidence_rationale: "<rationale>"

  - id: SRC-A-003
    dimension: "3. Problem Is Solvable"
    claim: "<assertion>"
    source_type: analytics
    source_ref: "<path or URL>"
    system_of_record: "<system>"
    date: "<YYYY-MM-DD>"
    quote: "<verbatim excerpt>"
    confidence: Medium
    confidence_rationale: "<rationale>"

  - id: SRC-A-004
    dimension: "4. Users Will Exchange Value"
    claim: "<assertion>"
    source_type: field_study
    source_ref: "<path or URL>"
    system_of_record: "<system>"
    date: "<YYYY-MM-DD>"
    quote: "<verbatim excerpt>"
    confidence: Medium
    confidence_rationale: "<rationale>"

  # Add more entries as needed: SRC-A-005, SRC-A-006 …
avatars:
  - icon: "🎯"
    name: "product"
    context: "constitutional context"
  - icon: "💼"
    name: "business"
    context: "constitutional context"
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
    status: pend
  - title: "stage-a-initialize.md created from this template"
    laws: ["ENG-11.2", "PRD-2.5"]
    status: pend
  - title: "Problem statement complete — all 4 PRD-2.1 dimensions filled"
    laws: ["PRD-2.1"]
    status: pend
  - title: "Scope defined (in/out table populated)"
    laws: ["PRD-2.5"]
    status: pend
  - title: "Mode declared (Exploratory or Accelerated) in frontmatter"
    laws: ["PRD-2.5"]
    status: pend
  - title: "Tier declared (Tier 1 or Tier 2) in frontmatter"
    laws: ["PRD-2.5"]
    status: pend
  - title: "Product and Business avatars activated and recorded"
    laws: ["PRD-2.5", "BUS-7.1"]
    status: pend
  - title: "Stakeholder approval obtained from named Director+ approver"
    description: "Self-certification prohibited by PRD-2.5."
    laws: ["PRD-2.1", "PRD-2.5"]
    status: pend
  - title: "problem_evidence populated — all 4 PRD-2.1 dimensions cite ≥1 SRC-A-NNN entry with source_ref, date, and quote"
    laws: ["PRD-2.1", "BUS-7.1"]
    status: pend
  - title: "All SRC-A-NNN inline citations in problem statement prose are traceable to problem_evidence entries"
    laws: ["PRD-2.1", "BUS-7.1"]
    status: pend
  - title: "stage-a-initialize.md rendered via aa-artifact-render and APPROVED in browser"
    laws: ["ENG-13.1"]
    status: pend
  - title: "BUS-7.1 audit event filed — Stage A → B transition"
    laws: ["BUS-7.1"]
    status: pend

audit_log:
  - event: "Stage A — Initialized"
    actor: "<name>"
    role: "<role>"
    system: "GitHub Copilot CLI"
    timestamp: "<YYYY-MM-DDTHH:MM:SSZ>"
    outcome: "IN_PROGRESS"
  - event: "Stage A → B"
    actor: "<name>"
    role: "<role>"
    system: "<…>"
    timestamp: "<YYYY-MM-DDTHH:MM:SSZ>"
    outcome: "AWAITING"

findings:
  - title: "<Key finding title>"
    description: "<1-2 sentence description>"
    laws: ["PRD-2.5"]
    status: pend

problem_validation:
  dim1:
    label: "1. Problem Exists"
    text: "<What pain/gap exists and who experiences it>"
    status: warn
  dim2:
    label: "2. Problem Matters"
    text: "<Business impact or cost of inaction>"
    status: warn
  dim3:
    label: "3. Problem Is Solvable"
    text: "<Why this is addressable>"
    status: ok
  dim4:
    label: "4. Users Will Exchange Value"
    text: "<Evidence of willingness to adopt>"
    status: warn

---

# Discovery Proposal: <Short Title>

---

## Problem Statement

> **PRD-2.1 — Problem Validation Law:** All problems MUST be validated before solution design.
> Complete all four dimensions below before proceeding.
> **Citation syntax:** reference problem evidence inline as `[SRC-A-NNN]` — e.g. *"Members report X [SRC-A-001]."*
> The rendered HTML resolves each ID to a card showing dimension, source, and verbatim quote.

### 1. Problem Exists
_What is the pain or gap? Who experiences it? Where is the evidence it exists today?_

<DESCRIBE THE PROBLEM. Be specific. Do not frame as a solution or a feature.>

### 2. Problem Matters
_Why is this significant enough to act on? What is the cost of inaction?_

<DESCRIBE BUSINESS IMPACT, OPERATIONAL RISK, OR USER HARM IF UNADDRESSED.>

### 3. Problem Is Solvable
_Is a solution technically and organisationally feasible? What gives you confidence?_

<DESCRIBE WHY THIS IS ADDRESSABLE — EXISTING CAPABILITIES, ANALOGOUS SOLUTIONS, ETC.>

### 4. Users Will Exchange Value
_Will users invest time, money, or behaviour change to solve this? What's the evidence?_

<DESCRIBE WILLINGNESS TO ADOPT — EARLY SIGNALS, STAKEHOLDER DEMAND, COMPLIANCE MANDATE, ETC.>

---

## Scope

| In Scope | Out of Scope |
|----------|-------------|
| <What this discovery covers> | <What is explicitly excluded> |
| <…> | <…> |

---

## Problem Evidence Registry (PRD-2.1 · BUS-7.1)

> All sources listed in the `problem_evidence` frontmatter block. Each `[SRC-A-NNN]` citation in the Problem Statement resolves to the entry below.
> The rendered HTML displays each source as a card with dimension, confidence indicator, source reference, and verbatim quote.

| ID | Dimension | Source Type | Date | Confidence |
|----|-----------|-------------|------|:----------:|
| SRC-A-001 | 1. Problem Exists | <source_type> | <YYYY-MM-DD> | 🟢 High |
| SRC-A-002 | 2. Problem Matters | <source_type> | <YYYY-MM-DD> | 🟡 Medium |
| SRC-A-003 | 3. Problem Is Solvable | <source_type> | <YYYY-MM-DD> | 🟡 Medium |
| SRC-A-004 | 4. Users Will Exchange Value | <source_type> | <YYYY-MM-DD> | 🟡 Medium |

> **Exit gate requirement (PRD-2.1 · BUS-7.1):** Every PRD-2.1 dimension must carry at least one cited SRC-A-NNN entry. All entries must have source_ref, date, and verbatim quote. Attribution is provided by the Stage A stakeholder approval block (approver name + date satisfies BUS-7.1 for problem statement decisions).
