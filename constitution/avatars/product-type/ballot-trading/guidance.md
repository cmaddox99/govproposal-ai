# Pilot Ballot & Trip Trading Guidance

> **Purpose:** Govern CBA-compliant pilot trip-pairing trades across CCA (rules engine), DOTC Portal (reserve visibility), and PTTS/BTS (matching).

---

## Overview

Pilots trade flight trip pairings through a digital platform enforcing every CBA rule programmatically. No trade is awarded without a CBA eligibility check and an immutable audit record.

## Non-Negotiable Laws

### PRD-1.1 — Continuous Discovery
- **Requires:** Pilot interviews and ballot-period observation every cycle to surface CBA interpretation gaps. See `examples/PRD-1.1-discovery.md`.
- **Violates:** Shipping features without observed pilot pain points from at least one ballot period.

### PRD-1.2 — Problem-First Law (NON-NEGOTIABLE)
- **Requires:** Validate the specific pilot friction point with interview evidence and behavioral telemetry before any solution work begins. See `examples/PRD-1.2-problem-first.md`.
- **Violates:** Proposing trade submission or eligibility UI changes without a filed, evidence-backed problem statement.

### PRD-1.5 — Evidence-Based Decision Law (NON-NEGOTIABLE)
- **Requires:** Award rankings and eligibility decisions surface their CBA evidence to pilots and schedulers. Deviations from evidence-ranked order require logged justification. See `examples/PRD-1.5-evidence-based.md`.
- **Violates:** Award ordering by submission timestamp or any factor not grounded in CBA article evidence.

### PRD-2.1 — User Journey Mapping
- **Requires:** Journey maps for all paths: real-time trade, batch ballot, reserve check, and dispute. See `examples/PRD-2.1-journey.md`.
- **Violates:** Designing only the happy-path real-time trade; batch and escalation paths omitted.

### PRD-2.5 — Discovery Stage-Gate Law (NON-NEGOTIABLE)
- **Requires:** Discovery stages progress sequentially with evidence gates filed in `hangar-ai-specs/`. CBA domain model must be reviewed by Labor Relations before spec work begins. See `examples/PRD-2.5-stage-gate.md`.
- **Violates:** Writing feature specs before CBA article review is complete (Stage C exit not met).

### PRD-5.1 — MVP & Experimentation
- **Requires:** Validate real-time eligible-trade slice before batch or AI investment. See `examples/PRD-5.1-metrics.md`.
- **Violates:** Building batch engine before validating real-time trade confirmation with pilots.

### PRD-6.2 — Retention Over Acquisition (NON-NEGOTIABLE)
- **Requires:** Prioritize pilot trust and retention over new feature acquisition. Opaque rejection messages or reliability issues must be resolved before new trade scenarios ship. See `examples/PRD-6.2-retention.md`.
- **Violates:** Shipping new trade features while pilots are reverting to scheduler calls due to unclear system behavior.

### BUS-7.1 — Audit Trail (NON-NEGOTIABLE)
- **Requires:** Every eligibility decision and trade outcome logged immutably with masked pilot ID, CBA article, and timestamp. See `examples/BUS-7.1-audit-trail.md`.
- **Violates:** Any trade decision without a persisted, tamper-evident audit record.

### BUS-2.2 — Control Framework
- **Requires:** Every eligibility check traces bidirectionally to a CBA article and produces an audit record. See `examples/BUS-2.2-control-framework.md`.
- **Violates:** Eligibility logic without a named CBA article reference.

### BUS-3.1 — Data Classification
- **Requires:** Pilot IDs, schedules, seniority, and trade records classified as Confidential with retention and access controls. See `examples/BUS-3.1-data-classification.md`.
- **Violates:** Raw pilot PII in logs or observability dashboards.

## Core Journeys

| Journey | Persona | Laws |
|---|---|---|
| Real-time trip trade | Line Pilot | PRD-2.1, BUS-7.1 |
| Batch ballot award | Line Pilot | BUS-2.2, BUS-7.1 |
| Reserve availability | Reserve Pilot | PRD-2.1 |
| CBA dispute review | CBA Analyst | BUS-7.1, BUS-2.2 |

## Anti-Patterns

- **Soft-coded CBA rules** — every constraint must cite a CBA article (BUS-2.2).
- **Best-effort audit logs** — records must persist before response returns; dropped records = BUS-7.1 hard block.
