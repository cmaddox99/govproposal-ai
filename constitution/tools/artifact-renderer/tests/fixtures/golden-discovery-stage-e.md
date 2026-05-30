---
type: discovery
spec_id: golden-fixture-stage-e
stage: E
stage_label: Metric Rebaseline
title: "Golden Fixture — Stage E Discovery"
workflow: product-discovery
mode: Exploratory
tier: Tier 1
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
gates:
  entry:
    status: met
    description: "Golden fixture entry — Stage E."
  exit:
    status: pending
    description: "Awaiting reviewer."
baseline_sources:
  - id: BSL-E-001
    metric_id: "M1"
    metric: "Daily Active Users"
    baseline_value: "42,300 DAU"
    tool: "Amplitude"
    dashboard_url: "internal"
    query_or_method: "SELECT count(distinct user_id) FROM events WHERE event_date = CURRENT_DATE - 7 ORDER BY event_date"
    snapshot_at: "2026-01-15T09:00:00Z"
    owner: "Analytics Lead"
    notes: "7-day rolling average. Excludes bots."
  - id: BSL-E-002
    metric_id: "M2"
    metric: "Points Redemption Rate"
    baseline_value: "23% of earned points redeemed within 90 days"
    tool: "Adobe Analytics"
    dashboard_url: "internal"
    query_or_method: "Redemption events / Earning events within 90-day rolling window"
    snapshot_at: "2026-01-15T09:00:00Z"
    owner: "Loyalty Analytics"
    notes: "None"
---

Golden fixture Stage E prose body.
