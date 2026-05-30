## C++ Tier System and Compliance Evaluation Framework — Tasks

**Spec:** `cpp-tier-compliance-rating`
**Parent PR:** #14 (c-plus-plus-avatar-enrichment)

---

### Phase 1 — Formalize Tier Taxonomy (RED → GREEN)

- [ ] 1.1 Write RED test: `test_manifest_standard_tiers_has_spec_reference()` — asserts `standard_tiers` block in manifest.yaml contains a `spec_ref` field pointing to this proposal
- [ ] 1.2 Add `spec_ref: hangar-ai-specs/changes/cpp-tier-compliance-rating/PROPOSAL.md` to the `standard_tiers:` block in `manifest.yaml`
- [ ] 1.3 Confirm GREEN — commit

---

### Phase 2 — Formalize Evaluation Formula in Skill (RED → GREEN)

- [ ] 2.1 Write RED test: `test_compliance_rating_skill_has_spec_reference()` — asserts skill file references this proposal
- [ ] 2.2 Update `skill-cpp-compliance-rating.md` — add reference to this PROPOSAL.md as governing spec
- [ ] 2.3 Write RED test: `test_compliance_rating_skill_10_dimensions_present()` — asserts all 10 dimension names present in skill
- [ ] 2.4 Verify all 10 dimensions are in skill file; add any missing ones
- [ ] 2.5 Confirm GREEN — commit

---

### Phase 3 — Governance Registration

- [ ] 3.1 Add `cpp-tier-compliance-rating` to `hangar-ai-specs/README.md` spec index (pending proposals section)
- [ ] 3.2 Run full test suite — confirm 0 failures
- [ ] 3.3 Open PR targeting main
- [ ] 3.4 Request governance review
