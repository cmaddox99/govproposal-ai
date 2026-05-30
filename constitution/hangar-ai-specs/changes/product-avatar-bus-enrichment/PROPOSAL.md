# Proposal: Product Avatar BUS-* Law Enrichment

**Status:** 🔵 IN PROGRESS — 13 of 14 files unblocked; PRD-3.4 split to `product-avatar-accessibility-governance`
**Spec ID:** `product-avatar-bus-enrichment`
**Triggered by:** Amendment O (V1/V2) — 14 BUS-*/PRD-* example files removed from `avatars/technology/cpp/` as domain boundary violations; content needs to be routed to the correct artifact layer
**Scope:** Product-type avatars in `avatars/product/` — new or enriched BUS-*/PRD-* example files
**Parent PR:** #14 (c-plus-plus-avatar-enrichment)
**Companion to:** `cpp-extended-reference-docs`, `cpp-tier-compliance-rating`

---

## Problem

The C++ technology avatar (PR #14) contained 14 BUS-*/PRD-* example files that violated the technology avatar domain boundary (V1/V2 in Amendment O). These files were deleted to fix the violations:

**BUS-* files (business/operational governance):**
- `BUS-1.1-compliance-audit-trail.md` — Audit trail schema for compliance systems
- `BUS-1.2-data-processing-agreement.md` — Data processing agreements
- `BUS-1.4-pii-anonymization.md` — PII anonymization patterns
- `BUS-2.1-misra-cpp-safety.md` — MISRA C++ safety standard mapping
- `BUS-3.1-cost-allocation-tagging.md` — Cloud cost allocation tagging
- `BUS-5.1-sla-breach-notification.md` — SLA breach notification workflows
- `BUS-5.2-canary-release-gate.md` — Canary release governance gates
- `BUS-7.1-audit-event-schema.md` — Audit event schema
- `BUS-7.2-audit-retention-policy.md` — Audit log retention policies

**PRD-* files (product management):**
- `PRD-1.1-backlog-item.md` — Backlog item templates
- `PRD-2.1-user-story.md` — User story formats
- `PRD-3.1-feature-spec.md` — Feature specification templates
- `PRD-3.4-accessibility.md` — Accessibility requirements
- `PRD-5.1-metrics-dashboard.md` — Product metrics dashboards

### Why This Content Has Value

These files were not wrong to exist — they were wrong to exist **in a technology avatar**. BUS-* laws govern operational compliance, data governance, SLA management, and audit requirements. PRD-* laws govern product discovery, requirements, and delivery. This content has legitimate constitutional value and should be available to AI agents through the correct artifact layer: **product-type avatars**.

The C++ technology context is also relevant for many of these (e.g., MISRA C++ safety is explicitly a C++ engineering concern). Where applicable, the BUS-*/PRD-* examples can reference C++ technology avatar patterns.

---

## Solution

Route the 14 deleted files to product-type avatars where they constitutionally belong:

### Routing Map

| File | Target Avatar | Rationale |
|------|--------------|-----------|
| `BUS-1.1-compliance-audit-trail.md` | `avatars/product-type/travel-docs-compliance/` | Compliance audit trails are core to travel document verification; `travel-docs-compliance` already covers regulatory record-keeping |
| `BUS-1.2-data-processing-agreement.md` | `avatars/product-type/marketing-personalization/` | DPA governance is most relevant where PII processing is core; `marketing-personalization` already has BUS-4.3 (data subject rights) and BUS-9.3 (breach notification) |
| `BUS-1.4-pii-anonymization.md` | `avatars/product-type/marketing-personalization/` | PII anonymization pairs with existing BUS-4.3 (data subject rights) in marketing-personalization |
| `BUS-2.1-misra-cpp-safety.md` | `avatars/product-type/crew-training-scheduling/` | Safety-critical regulatory mapping; `crew-training-scheduling` already has BUS-2.1-regulatory-mapping.md — enrich with MISRA/C++ context |
| `BUS-3.1-cost-allocation-tagging.md` | `avatars/product-type/ground-ops-staffing-analytics/` | FinOps cost tagging is an analytics/ops concern; ground-ops analytics is the closest operational cost-tracking avatar |
| `BUS-5.1-sla-breach-notification.md` | `avatars/product-type/customer-service/` | SLA breach notification is a customer-service operations concern |
| `BUS-5.2-canary-release-gate.md` | `avatars/product-type/schedule-change-self-serve/` | Canary release governance is most relevant to high-traffic self-service products with progressive rollout |
| `BUS-7.1-audit-event-schema.md` | `avatars/product-type/customer-relations-ops/` | Audit event schemas are core to customer relations compliance; extends existing PRD-* examples |
| `BUS-7.2-audit-retention-policy.md` | `avatars/product-type/customer-relations-ops/` | Audit retention pairs with BUS-7.1 audit schema above |
| `PRD-1.1-backlog-item.md` | `avatars/product-type/cargo-freight/` | Backlog templates; cargo-freight already has PRD-1.1-discovery.md — enrich with backlog formatting |
| `PRD-2.1-user-story.md` | `avatars/product-type/check-in-travel/` | User story format; check-in-travel already has PRD-2.1-journey.md — enrich with story structure |
| `PRD-3.1-feature-spec.md` | `avatars/product-type/loyalty-aadvantage/` | Feature spec templates; loyalty-aadvantage is the richest product avatar (10 examples) — good template host |
| `PRD-3.4-accessibility.md` | See [`product-avatar-accessibility-governance`](../product-avatar-accessibility-governance/PROPOSAL.md) | Domain boundary ruling pending — split to dedicated proposal |
| `PRD-5.1-metrics-dashboard.md` | `avatars/product-type/network-planning-optimization/` | Product metrics dashboards; network-planning is data-intensive and metrics-driven |

### Note: PRD-3.4 Accessibility

`PRD-3.4-accessibility.md` has been split into a separate proposal (`product-avatar-accessibility-governance`) pending a governance ruling on its domain boundary. This proposal covers the remaining 13 files only.

---

## Deliverables

| Artifact | Description |
|----------|-------------|
| This PROPOSAL.md | Routing map for deleted BUS-*/PRD-* content |
| `tasks.md` | Atomic TDD tasks for each routing decision |
| Per-avatar additions | New BUS-*/PRD-* example files in correct product avatar directories |
| Preserved content | All 14 deleted files recreated in correct locations with C++ context notes where applicable |

---

## Success Criteria

| Criterion | Verification |
|-----------|--------------|
| All 14 BUS-*/PRD-* files routed to correct product avatars | Manual audit — each file exists in appropriate product avatar |
| No BUS-*/PRD-* files in `avatars/technology/cpp/examples/` | `test_technology_avatar_examples_only_contain_eng_laws()` PASSES |
| Product avatars receiving content have passing tests | Each target avatar's test suite passes |
| PRD-3.4 handled by companion proposal | [`product-avatar-accessibility-governance`](../product-avatar-accessibility-governance/PROPOSAL.md) unblocks remaining 13 files |

---

## Laws Cited

| Law | Relevance |
|-----|-----------|
| [ENG-11.1](laws/engineering/spec-driven-development.md) | Spec-Driven Development — domain boundary enforcement for avatar artifact types |
| [ENG-11.2](laws/engineering/spec-driven-development.md) | Proposal Completeness — formal routing map required for moved content |

---

## Implementation Priority

This proposal is lower priority than `cpp-extended-reference-docs` and `cpp-tier-compliance-rating`. The deleted content was creating governance violations; the product avatars that would receive this content currently function without it. Implementation can be scheduled as part of a future product avatar enrichment sprint.
