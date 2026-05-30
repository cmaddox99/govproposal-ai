## Product Avatar BUS-* Law Enrichment — Tasks

**Spec:** `product-avatar-bus-enrichment`
**Parent PR:** #14 (c-plus-plus-avatar-enrichment) — companion proposal

---

### Phase 1 — Governance Panel Ruling on PRD-3.4 (Blocking)

- [ ] 1.1 Await governance panel ruling on `PRD-3.4-accessibility.md` in `mobile-react-native` (PR #14 comment, 2026-04-11)
- [ ] 1.2 Document ruling in PROGRESS.md
- [ ] 1.3 Update routing map in PROPOSAL.md based on ruling

---

### Phase 2 — Route BUS-1.x Compliance Files

- [ ] 2.1 Create `BUS-1.1-compliance-audit-trail.md` in `avatars/product-type/travel-docs-compliance/examples/`
- [ ] 2.2 Create `BUS-1.2-data-processing-agreement.md` in `avatars/product-type/marketing-personalization/examples/`
- [ ] 2.3 Create `BUS-1.4-pii-anonymization.md` in `avatars/product-type/marketing-personalization/examples/`
- [ ] 2.4 Write RED tests for each BUS-1.x example in target avatar
- [ ] 2.5 Confirm GREEN — commit

---

### Phase 3 — Route BUS-2.1 Safety-Critical

- [ ] 3.1 Enrich `avatars/product-type/crew-training-scheduling/examples/` with `BUS-2.1-misra-cpp-safety.md` (extends existing BUS-2.1-regulatory-mapping.md with MISRA/C++ context)
- [ ] 3.2 Write RED test for BUS-2.1 MISRA content in crew-training-scheduling
- [ ] 3.3 Confirm GREEN — commit

---

### Phase 4 — Route BUS-3.x and BUS-5.x Operational Files

- [ ] 4.1 Create `BUS-3.1-cost-allocation-tagging.md` in `avatars/product-type/ground-ops-staffing-analytics/examples/`
- [ ] 4.2 Create `BUS-5.1-sla-breach-notification.md` in `avatars/product-type/customer-service/examples/`
- [ ] 4.3 Create `BUS-5.2-canary-release-gate.md` in `avatars/product-type/schedule-change-self-serve/examples/`
- [ ] 4.4 Write RED tests for each file in target avatar
- [ ] 4.5 Confirm GREEN — commit

---

### Phase 5 — Route BUS-7.x Audit Files

- [ ] 5.1 Create `BUS-7.1-audit-event-schema.md` in `avatars/product-type/customer-relations-ops/examples/`
- [ ] 5.2 Create `BUS-7.2-audit-retention-policy.md` in `avatars/product-type/customer-relations-ops/examples/`
- [ ] 5.3 Write RED tests for BUS-7.x in customer-relations-ops
- [ ] 5.4 Confirm GREEN — commit

---

### Phase 6 — Route PRD-* Product Management Files

- [ ] 6.1 Create `PRD-1.1-backlog-item.md` in `avatars/product-type/cargo-freight/examples/` (enriches existing PRD-1.1-discovery.md)
- [ ] 6.2 Create `PRD-2.1-user-story.md` in `avatars/product-type/check-in-travel/examples/` (enriches existing PRD-2.1-journey.md)
- [ ] 6.3 Create `PRD-3.1-feature-spec.md` in `avatars/product-type/loyalty-aadvantage/examples/`
- [ ] 6.4 Route `PRD-3.4-accessibility.md` to `avatars/product-type/passenger-booking/examples/` per governance panel ruling (Phase 1)
- [ ] 6.5 Create `PRD-5.1-metrics-dashboard.md` in `avatars/product-type/network-planning-optimization/examples/`
- [ ] 6.6 Write RED tests for each PRD-* file in target avatar
- [ ] 6.7 Confirm GREEN — commit

---

### Phase 7 — PR and Close

- [ ] 7.1 Run full test suite — confirm 0 failures across all modified product avatars
- [ ] 7.2 Open PR targeting main
- [ ] 7.3 Request governance review
