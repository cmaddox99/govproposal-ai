---
# Stage B — Field Study — Product Discovery Stage A–F
# Governed by: PRD-2.3, PRD-2.4, PRD-3.1, PRD-3.2, BUS-7.1, ENG-13.1
# Usage: Copy to hangar-ai-specs/changes/[discovery-id]/stage-b-field-study.md
#        Replace all <PLACEHOLDER> values before advancing to Stage C.
# Example (rendered): tools/templates/product-discovery/examples/partner-miles-reference/stage-b-field-study.html

id: disc-YYYY-NNN
spec_id: disc-YYYY-NNN
type: discovery
stage: B
stage_label: Field Study
status: IN_PROGRESS
created: YYYY-MM-DD
branch: <git-branch-name>
workflow: product-discovery-stage-a-f
workflow_version: "2.1.0"
skill: skill-product-discovery-orchestration
title: "<Short Title — e.g. AADvantage Loyalty Platform — Field Study>"

mode: Exploratory                        # Exploratory | Accelerated
tier: Tier 2                             # Tier 1 | Tier 2

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
      Stage A Initialize approved by named Director+. Problem statement
      validated across all 4 PRD-2.1 dimensions. Stage B field study initiated.
  exit:
    status: pending
    description: >
      Awaiting ≥3 validated user insights and competitive landscape documented.
      Human browser review and BUS-7.1 audit event required before Stage C.
stakeholder:
  approver: "<Full name>"
  title: "<Role — e.g. Director, Product | Discovery Sponsor>"
  date: "<YYYY-MM-DD>"
  method: "<In-person | Async written | PR review | Email>"
  self_cert: false

# ---------------------------------------------------------------------------
# SOURCE REGISTRY (PRD-3.1 · BUS-7.1)
# Every insight in this document MUST cite at least one source ID using the
# inline syntax [SRC-B-NNN] in the prose body.
#
# Tier 1 — required minimum per source:
#   id, label, platform, url, retrieved
# Tier 2 — also required:
#   record_count, description, sample_quotes (≥1 quote per insight category)
#
# Platform values: app_store_ios | google_play | reddit | trustpilot |
#                  user_interview | survey | analytics | internal_report | other
# ---------------------------------------------------------------------------
methodology_note: >
  <Describe how evidence was collected — e.g. "372 complaints filtered from
  1,009 voice records via three-gate keyword, sentiment, and digital-context
  filter; sources: App Store iOS, Google Play, Reddit, Trustpilot (Apr 2026).">

source_registry:
  - id: SRC-B-001
    label: "<Short descriptive name — e.g. App Store iOS Reviews>"
    platform: app_store_ios           # app_store_ios | google_play | reddit | trustpilot | user_interview | survey | analytics | internal_report | other
    url: "<https://... or 'internal' for proprietary sources>"
    retrieved: "<YYYY-MM-DD>"
    record_count: <N>                  # number of records / reviews / responses
    description: >
      <What this source is and why it was selected.>
    sample_quotes:
      - text: "<Verbatim quote from a real user or participant>"
        date: "<YYYY-MM-DD>"
        rating: <1-5 or null>
        category: "<complaint/feedback category>"
      - text: "<Second verbatim quote>"
        date: "<YYYY-MM-DD>"
        rating: <1-5 or null>
        category: "<category>"

  - id: SRC-B-002
    label: "<e.g. Google Play Reviews>"
    platform: google_play
    url: "<https://...>"
    retrieved: "<YYYY-MM-DD>"
    record_count: <N>
    description: >
      <What this source is and why it was selected.>
    sample_quotes:
      - text: "<Verbatim quote>"
        date: "<YYYY-MM-DD>"
        rating: <1-5 or null>
        category: "<category>"

  # Add more sources as needed: SRC-B-003, SRC-B-004 …
avatars:
  - icon: "🎯"
    name: "product"
    context: "constitutional context"
  - icon: "💼"
    name: "business"
    context: "constitutional context"
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
  - title: "source_registry populated — all cited sources have minimum fields (id, label, platform, url, retrieved); ≥1 verbatim quote per insight category"
    laws: ["PRD-3.1", "BUS-7.1"]
    status: pend
  - title: "All insights carry inline [SRC-B-NNN] citations traceable to source_registry entries"
    laws: ["PRD-3.1", "BUS-7.1"]
    status: pend
  - title: "stage-b-field-study.md rendered via aa-artifact-render and APPROVED in browser"
    laws: ["ENG-13.1"]
    status: pend
  - title: "BUS-7.1 audit event filed — Stage B → C transition"
    laws: ["BUS-7.1"]
    status: pend

audit_log:
  - event: "Stage B — Field Study initiated"
    actor: "<name>"
    role: "<role>"
    system: "GitHub Copilot CLI"
    timestamp: "<YYYY-MM-DDTHH:MM:SSZ>"
    outcome: "IN_PROGRESS"
  - event: "Stage B → C"
    actor: "<name>"
    role: "<role>"
    system: "<…>"
    timestamp: "<YYYY-MM-DDTHH:MM:SSZ>"
    outcome: "AWAITING"

---

# Stage B Field Study: <Short Title>

---

## User Research (PRD-3.1)

> **Research Methodology:** `<methodology_note from frontmatter — how evidence was gathered>`
>
> **Citation syntax:** reference sources inline as `[SRC-B-NNN]` — e.g. *"Users report frequent login failures [SRC-B-001]."*
> The rendered HTML resolves each ID to a clickable source chip showing platform, URL, retrieval date, and record count.

### Interviews / Research Sessions Conducted

| # | Participant | Role / Title | Date | Key Insight | Source |
|---|------------|-------------|------|-------------|--------|
| 1 | <name or derived source> | <role> | <date> | <insight> | [SRC-B-NNN] |
| 2 | <name or derived source> | <role> | <date> | <insight> | [SRC-B-NNN] |
| 3 | <name or derived source> | <role> | <date> | <insight> | [SRC-B-NNN] |

> **Minimum:** ≥3 validated user insights required before exit gate.

### Validated User Insights

**Insight 1 — <Theme>** `[SRC-B-NNN]`
> <Describe the insight with specific evidence. Cite source ID inline.>
> *Evidence: `<source file or URL>` — verbatim: "<quote from source>"*

**Insight 2 — <Theme>** `[SRC-B-NNN]`
> <Insight description with evidence citation.>
> *Evidence: `<source>` — verbatim: "<quote>"*

**Insight 3 — <Theme>** `[SRC-B-NNN]`
> <Insight description with evidence citation.>
> *Evidence: `<source>` — verbatim: "<quote>"*

### Personas

| Persona | Role | Goals | Frustrations | Context |
|---------|------|-------|-------------|---------|
| <name> | <role> | <goals> | <frustrations> | <context> |

---

## Jobs-to-be-Done (PRD-2.3)

| Job Statement | Current Solution | Pain Level (H/M/L) | Frequency | Source |
|--------------|-----------------|---------------------|-----------|--------|
| When I <situation>, I want to <motivation>, so I can <outcome> | <current approach> | <H/M/L> | <daily/weekly/monthly> | [SRC-B-NNN] |

---

## Competitive Analysis (PRD-2.4)

| Competitor / Alternative | Approach | Strengths | Gaps | Differentiation Opportunity |
|-------------------------|----------|-----------|------|---------------------------|
| <competitor> | <approach> | <strengths> | <gaps> | <opportunity> |

---

## Journey Map (PRD-3.2)

| Stage | Actions | Touchpoints | Pain Points | Emotional State | Source |
|-------|---------|------------|-------------|----------------|--------|
| <stage> | <actions> | <touchpoints> | <pain points> | <emotional state> | [SRC-B-NNN] |

---

## Source Registry (PRD-3.1 · BUS-7.1)

> All sources listed in the `source_registry` frontmatter block. Each `[SRC-B-NNN]` citation in this document resolves to the entry below.
> The rendered HTML displays each source as a clickable chip with platform icon, URL, retrieval date, and record count.

| ID | Label | Platform | Retrieved | Records | Description |
|----|-------|----------|-----------|---------|-------------|
| SRC-B-001 | <label> | <platform> | <YYYY-MM-DD> | <N> | <description> |
| SRC-B-002 | <label> | <platform> | <YYYY-MM-DD> | <N> | <description> |

> **Exit gate requirement (PRD-3.1 · BUS-7.1):** Every source cited inline must appear in this registry with minimum fields populated. At least one verbatim `sample_quote` required per insight category at Tier 2.
