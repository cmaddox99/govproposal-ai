---
# Stage E — Metric Rebaseline — Product Discovery Stage A–F
# Governed by: PRD-6.1, ENG-10.1, BUS-7.1, ENG-13.1
# Usage: Copy to hangar-ai-specs/changes/[discovery-id]/stage-e-metrics.md
#        Replace all <PLACEHOLDER> values before advancing to Stage F.
# Example (rendered): tools/templates/product-discovery/examples/partner-miles-reference/stage-e-metrics.html

id: disc-YYYY-NNN
spec_id: disc-YYYY-NNN
type: discovery
stage: E
stage_label: Metric Rebaseline
status: IN_PROGRESS
created: YYYY-MM-DD
branch: <git-branch-name>
workflow: product-discovery-stage-a-f
workflow_version: "2.1.0"
skill: skill-product-discovery-orchestration
title: "<Short Title — e.g. AADvantage Loyalty Platform — Metric Rebaseline>"

mode: Exploratory                        # Exploratory | Accelerated
tier: Tier 2                             # Tier 1 | Tier 2

laws:
  - PRD-6.1
  - ENG-10.1
  - BUS-7.1
  - ENG-13.1

laws_applied:
  - PRD-6.1
  - ENG-10.1
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
    status: done
  - id: E
    label: Metrics
    status: active
  - id: F
    label: Roadmap Lock
    status: locked

gates:
  entry:
    status: met
    description: >
      Stage D Validation approved. All blockers resolved. DVFT matrix complete.
      Stage E metric rebaseline and PMF target definition initiated.
  exit:
    status: pending
    description: >
      Awaiting metrics spec complete with measurability confirmed.
      Human browser review and BUS-7.1 audit event required before Stage F.
stakeholder:
  approver: "<Full name>"
  title: "<Role — e.g. Director, Product | Discovery Sponsor>"
  date: "<YYYY-MM-DD>"
  method: "<In-person | Async written | PR review | Email>"
  self_cert: false
# ---------------------------------------------------------------------------
# BASELINE SOURCE REGISTRY (PRD-6.1 · ENG-10.1 · BUS-7.1)
# Every metric baseline in the AARRR table MUST cite at least one BSL-E-NNN
# entry using inline syntax [BSL-E-NNN] in the Baseline cell.
#
# metric_id: stable short ID for cross-referencing from Stage F (M1, M2, …)
# query_or_method: REQUIRED — SQL snippet, dashboard filter, or export method
#                  for reproducibility
# snapshot_at: ISO-8601 timestamp of when the data was captured
# ---------------------------------------------------------------------------
baseline_sources:
  - id: BSL-E-001
    metric_id: "M1"                  # stable ID used in Stage F roadmap_rationale
    metric: "<metric display name — must match AARRR table>"
    baseline_value: "<current measured value with unit>"
    tool: "<Amplitude | Adobe Analytics | Tableau | internal dashboard | etc.>"
    dashboard_url: "<URL or 'internal' for proprietary sources>"
    query_or_method: "<Required — SQL snippet, dashboard filter description, or export method>"
    snapshot_at: "<YYYY-MM-DDTHH:MM:SSZ>"   # ISO-8601 timestamp
    owner: "<Full name>"
    notes: "<caveats, seasonality, known gaps — or 'None'>"

  - id: BSL-E-002
    metric_id: "M2"
    metric: "<metric name>"
    baseline_value: "<value>"
    tool: "<tool>"
    dashboard_url: "<URL or 'internal'>"
    query_or_method: "<required>"
    snapshot_at: "<YYYY-MM-DDTHH:MM:SSZ>"
    owner: "<name>"
    notes: "<caveats>"

  # Add more: BSL-E-003, BSL-E-004, … one per AARRR metric
avatars:
  - icon: "🎯"
    name: "product"
    context: "constitutional context"
  - icon: "💼"
    name: "business"
    context: "constitutional context"
spec_artifacts:
  - icon: "📄"
    filename: "stage-e-metrics.md"
    status: "DRAFTED"
  - icon: "🌐"
    filename: "stage-e-metrics.html"
    status: "PENDING"

exit_checklist:
  - title: "AARRR success metrics defined for all 5 framework dimensions"
    laws: ["PRD-6.1"]
    status: pend
  - title: "PMF definition documented with quantified threshold"
    laws: ["PRD-6.1"]
    status: pend
  - title: "Leading vs lagging indicators distinguished"
    laws: ["PRD-6.1"]
    status: pend
  - title: "Measurement plan documented — instrumentation, owner, cadence"
    laws: ["PRD-6.1"]
    status: pend
  - title: "All metrics confirmed measurable before Stage F"
    laws: ["PRD-6.1"]
    status: pend
  - title: "baseline_sources populated — all AARRR metric baselines carry ≥1 [BSL-E-NNN] citation with snapshot_at, tool, and query_or_method"
    laws: ["PRD-6.1", "ENG-10.1", "BUS-7.1"]
    status: pend
  - title: "All BSL-E-NNN entries have dashboard_url or query_or_method populated — baselines are reproducible"
    laws: ["PRD-6.1", "BUS-7.1"]
    status: pend
  - title: "stage-e-metrics.md rendered via aa-artifact-render and APPROVED in browser"
    laws: ["ENG-13.1"]
    status: pend
  - title: "BUS-7.1 audit event filed — Stage E → F transition"
    laws: ["BUS-7.1"]
    status: pend

audit_log:
  - event: "Stage E — Metric Rebaseline initiated"
    actor: "<name>"
    role: "<role>"
    system: "GitHub Copilot CLI"
    timestamp: "<YYYY-MM-DDTHH:MM:SSZ>"
    outcome: "IN_PROGRESS"
  - event: "Stage E → F"
    actor: "<name>"
    role: "<role>"
    system: "<…>"
    timestamp: "<YYYY-MM-DDTHH:MM:SSZ>"
    outcome: "AWAITING"

---

# Stage E Metric Rebaseline: <Short Title>

---

## Success Metrics (AARRR Framework)

| ID | Stage | Metric | Baseline | Target | PMF Signal |
|----|-------|--------|----------|--------|------------|
| M1 | Acquisition | <metric> | <current> `[BSL-E-001]` | <target> | <threshold> |
| M2 | Activation | <metric> | <current> `[BSL-E-002]` | <target> | <threshold> |
| M3 | Retention | <metric> | <current> `[BSL-E-003]` | <target> | <threshold> |
| M4 | Revenue | <metric> | <current> `[BSL-E-004]` | <target> | <threshold> |
| M5 | Referral | <metric> | <current> `[BSL-E-005]` | <target> | <threshold> |

---

## PMF Definition

<DESCRIBE WHAT PRODUCT-MARKET FIT LOOKS LIKE FOR THIS DISCOVERY — quantitative thresholds and qualitative signals>

---

## Leading vs. Lagging Indicators

| Type | Indicator | Measurement Frequency | Owner |
|------|-----------|:---------------------:|-------|
| Leading | <indicator> | <daily/weekly/monthly> | <team/person> |
| Lagging | <indicator> | <daily/weekly/monthly> | <team/person> |

---

## Measurement Plan

| Metric | Tool / Source | Collection Method | Frequency | Owner |
|--------|-------------|-------------------|:---------:|-------|
| <metric> | <tool> | <method> | <frequency> | <owner> |

---

## Baseline Source Registry (PRD-6.1 · ENG-10.1 · BUS-7.1)

> All metric baselines listed in the `baseline_sources` frontmatter block. Each `[BSL-E-NNN]` citation in the AARRR table resolves to the entry below.
> The rendered HTML displays each source with tool, snapshot timestamp, query method, and owner.

| ID | Metric (ID) | Baseline | Tool | Snapshot | Owner |
|----|-------------|----------|------|----------|-------|
| BSL-E-001 | <metric> (M1) | <value> | <tool> | <YYYY-MM-DDTHH:MM:SSZ> | <owner> |
| BSL-E-002 | <metric> (M2) | <value> | <tool> | <YYYY-MM-DDTHH:MM:SSZ> | <owner> |

> **Exit gate requirement (PRD-6.1 · BUS-7.1):** All metric baselines must cite a registered BSL-E-NNN source with snapshot_at timestamp and reproducible query_or_method. Baselines without sources CANNOT satisfy Stage E exit gate.

---

## Measurability Confirmation

- [ ] All metrics have a defined baseline (even if baseline = 0)
- [ ] All metrics have a defined target
- [ ] All metrics have a named owner
- [ ] Collection tools/sources are identified and accessible
- [ ] PMF definition is quantitative and testable
