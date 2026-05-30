---
type: discovery
spec_id: golden-fixture-stage-a
stage: A
stage_label: Initialize
title: "Golden Fixture — Stage A Discovery"
workflow: product-discovery
mode: Exploratory
tier: Tier 1
laws_applied:
  - PRD-2.1
  - PRD-2.5
  - BUS-7.1
  - ENG-13.1
stages:
  - id: A
    label: Initialize
    status: active
  - id: B
    label: Field Study
    status: locked
gates:
  entry:
    status: met
    description: "Golden fixture entry — stable across releases."
  exit:
    status: pending
    description: "Awaiting reviewer in §Render Gate."
problem_validation:
  dim1:
    label: "1. Problem Exists"
    status: warn
    text: "Hypothesized — not yet validated."
ensemble_verdict:
  verdicts:
    - persona: Amaya
      law: ENG-13.1
      note: "Golden fixture verdict."
      verdict: PASS
problem_evidence:
  - id: SRC-A-001
    dimension: "1. Problem Exists"
    claim: "Golden fixture problem exists claim"
    source_type: stakeholder_statement
    source_ref: "golden-fixture/stakeholder-statement.md"
    system_of_record: "stakeholder"
    date: "2026-01-15"
    quote: "Golden fixture verbatim quote for dimension 1."
    confidence: High
    confidence_rationale: "Signed stakeholder statement — golden fixture."
  - id: SRC-A-002
    dimension: "2. Problem Matters"
    claim: "Golden fixture problem matters claim"
    source_type: analytics
    source_ref: "golden-fixture/analytics-report.md"
    system_of_record: "Amplitude"
    date: "2026-01-10"
    quote: "Golden fixture verbatim quote for dimension 2."
    confidence: Medium
    confidence_rationale: "Analytics extract — golden fixture."
---

# Golden Fixture — Stage A Discovery

This file is used by `test_determinism.py` to assert byte-stable rendering.

If this file changes, the golden HTML must also be regenerated via
`tools/artifact-renderer/regen-golden.sh`.
