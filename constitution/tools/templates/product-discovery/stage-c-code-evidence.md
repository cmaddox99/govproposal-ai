---
# Stage C — Code Evidence — Product Discovery Stage A–F
# Governed by: ENG-3.1, ENG-6.7, PRD-3.2, BUS-7.1, ENG-13.1
# Usage: Copy to hangar-ai-specs/changes/[discovery-id]/stage-c-code-evidence.md
#        Replace all <PLACEHOLDER> values before advancing to Stage D.
# Example (rendered): tools/templates/product-discovery/examples/partner-miles-reference/stage-c-code-evidence.html

id: disc-YYYY-NNN
spec_id: disc-YYYY-NNN
type: discovery
stage: C
stage_label: Code Evidence
status: IN_PROGRESS
created: YYYY-MM-DD
branch: <git-branch-name>
workflow: product-discovery-stage-a-f
workflow_version: "2.1.0"
skill: skill-product-discovery-orchestration
title: "<Short Title — e.g. AADvantage Loyalty Platform — Code Evidence>"

mode: Exploratory                        # Exploratory | Accelerated
tier: Tier 2                             # Tier 1 | Tier 2

laws:
  - ENG-3.1
  - ENG-6.7
  - PRD-3.2
  - BUS-7.1
  - ENG-13.1

laws_applied:
  - ENG-3.1
  - ENG-6.7
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
      Stage B Field Study approved. ≥3 validated user insights confirmed.
      Competitive landscape documented. Stage C codebase assessment initiated.
  exit:
    status: pending
    description: >
      Awaiting codebase assessment complete with no unreviewed critical findings.
      Human browser review and BUS-7.1 audit event required before Stage D.
stakeholder:
  approver: "<Full name>"
  title: "<Role — e.g. Director, Product | Discovery Sponsor>"
  date: "<YYYY-MM-DD>"
  method: "<In-person | Async written | PR review | Email>"
  self_cert: false
avatars:
  - icon: "🎯"
    name: "product"
    context: "constitutional context"
  - icon: "💼"
    name: "business"
    context: "constitutional context"
spec_artifacts:
  - icon: "📄"
    filename: "stage-c-code-evidence.md"
    status: "DRAFTED"
  - icon: "🌐"
    filename: "stage-c-code-evidence.html"
    status: "PENDING"

exit_checklist:
  - title: "Repository assessment complete — all active services catalogued"
    laws: ["ENG-11.1"]
    status: pend
  - title: "Architecture overview documented with bounded contexts"
    laws: ["ENG-3.2"]
    status: pend
  - title: "Domain model extracted per ENG-6.7"
    laws: ["ENG-6.7"]
    status: pend
  - title: "Tech debt inventory completed per ENG-3.1 — all HIGH/MEDIUM items carry evidence_ids"
    laws: ["ENG-3.1"]
    status: pend
  - title: "Evidence glossary populated — all critical findings and HIGH/MEDIUM severity items have EVI-C-NNN entry with source_file, quote, verification_method, and confidence"
    laws: ["ENG-3.1", "BUS-7.1"]
    status: pend
  - title: "Compliance and regulatory constraints documented"
    laws: ["BUS-4.1", "BUS-7.1"]
    status: pend
  - title: "Build vs Buy vs Extend recommendation made"
    laws: ["ENG-11.1"]
    status: pend
  - title: "stage-c-code-evidence.md rendered via aa-artifact-render and APPROVED in browser"
    laws: ["ENG-13.1"]
    status: pend
  - title: "BUS-7.1 audit event filed — Stage C → D transition"
    laws: ["BUS-7.1"]
    status: pend

# ---------------------------------------------------------------------------
# EVIDENCE GLOSSARY (ENG-3.1 · BUS-7.1)
# Every critical finding and HIGH/MEDIUM severity tech debt item MUST have
# at least one EVI-C-NNN entry below.
#
# verification_method values:
#   direct-file-inspection       — wc -l, grep, manual file read
#   automated-metrics            — metrics-snapshot.csv, quality-scores.csv
#   report-cross-reference       — reference to a reports/ analysis document
#   manual-code-review           — human engineer reviewed the code
#   agent-extracted-human-verified — agent authored from corpus; human certified
#
# confidence values: High | Medium | Low
#   High   — direct measurement (file path + wc -l, test assertion count)
#   Medium — AI-assisted scoring, aggregate report data
#   Low    — inferred from indirect signals or extrapolation
# ---------------------------------------------------------------------------
evidence_glossary:
  - id: EVI-C-001
    claim: "<The specific assertion being supported — e.g. 'BookingViewModel.kt is 2,286 LOC'>"
    source_file: "<relative path — e.g. reports/android/androidapps/code-quality-analysis.md>"
    section: "<section heading or §label — e.g. §3.1 SOLID Principles>"
    quote: "<Verbatim extract from the source document>"
    verified_by: "<Full name · YYYY-MM-DD or 'GitHub Copilot CLI · YYYY-MM-DD (pending human review)'>"
    verification_method: direct-file-inspection   # see values above
    confidence: High                              # High | Medium | Low
    confidence_rationale: "<Why this confidence level — e.g. 'Measured directly via wc -l'>"

  - id: EVI-C-002
    claim: "<Second claim>"
    source_file: "<path>"
    section: "<section>"
    quote: "<verbatim quote>"
    verified_by: "<name · date>"
    verification_method: report-cross-reference
    confidence: Medium
    confidence_rationale: "<Rationale>"

  # Add more entries: EVI-C-003, EVI-C-004 …

audit_log:
  - event: "Stage C — Code Evidence initiated"
    actor: "<name>"
    role: "<role>"
    system: "GitHub Copilot CLI"
    timestamp: "<YYYY-MM-DDTHH:MM:SSZ>"
    outcome: "IN_PROGRESS"
  - event: "Stage C → D"
    actor: "<name>"
    role: "<role>"
    system: "<…>"
    timestamp: "<YYYY-MM-DDTHH:MM:SSZ>"
    outcome: "AWAITING"

---

# Stage C Code Evidence: <Short Title>

---

## Repository Assessment

| Attribute | Value |
|-----------|-------|
| Repository | <repo name / URL> |
| Primary language(s) | <languages> |
| LOC (approx) | <lines of code> |
| Last commit | <date> |
| Active contributors (90d) | <count> |

---

## Architecture Overview

<DESCRIBE CURRENT ARCHITECTURE — bounded contexts, services, integrations, data flows>

---

## Domain Model Extraction (ENG-6.7)

| Entity | Bounded Context | Relationships | Notes |
|--------|----------------|--------------|-------|
| <entity> | <context> | <relationships> | <notes> |

---

## Tech Debt Inventory (ENG-3.1)

> Each HIGH and MEDIUM severity item **must** reference at least one `EVI-C-NNN` ID from the evidence glossary.
> The rendered HTML links each ID to the glossary entry showing source file, verbatim quote, and confidence level.

| Item | Severity (H/M/L) | Impact | Remediation Path | Evidence |
|------|:-:|---|---|---|
| <tech debt item> | <H/M/L> | <impact description> | <remediation> | EVI-C-NNN |

---

## Compliance / Regulatory Constraints

| Constraint | Source | Impact on Discovery |
|-----------|--------|-------------------|
| <constraint> | <regulation/policy> | <how it affects what we can build> |

---

## Build vs. Buy vs. Extend

| Option | Pros | Cons | Recommendation |
|--------|------|------|---------------|
| Build | <pros> | <cons> | |
| Buy | <pros> | <cons> | |
| Extend | <pros> | <cons> | |

**Recommended approach:** <BUILD / BUY / EXTEND> — <rationale>

---

## Critical Findings

| # | Finding | Severity | Evidence | Reviewed? |
|---|---------|:--------:|----------|:---------:|
| 1 | <finding> | <H/M/L> | EVI-C-NNN | ✅ / ⬜ |

> **Exit gate requirement:** No unreviewed critical findings. All HIGH/MEDIUM items carry at least one EVI-C-NNN reference.

---

## Evidence Glossary (ENG-3.1 · BUS-7.1)

> Auto-populated from `evidence_glossary` frontmatter. Agent drafts entries from the code analysis corpus;
> **human reviewer certifies each entry** by updating the `verified_by` field before Stage C exit gate.
> Confidence: 🟢 High = direct measurement · 🟡 Medium = AI-assisted/aggregate · 🔴 Low = inferred

| ID | Claim | Source File | Section | Quote (excerpt) | Method | Confidence |
|----|-------|-------------|---------|-----------------|--------|:----------:|
| EVI-C-001 | <claim> | `<source_file>` | <section> | *"<quote excerpt>"* | <verification_method> | 🟢 High |
| EVI-C-002 | <claim> | `<source_file>` | <section> | *"<quote excerpt>"* | <verification_method> | 🟡 Medium |

> Verified by: `<name · date>` — update `verified_by` in frontmatter to certify.

> **Exit gate requirement:** No unreviewed critical findings.
