# Tasks — iOS Build Infrastructure Avatar Corrections

**Proposal:** avatar-ios-build-infrastructure
**Scenario:** avatar-ios-build-infra/1.1 (post-RAG-validation corrections)
**Total Tasks:** 7
**Completed:** 7/7

## Progress Summary

- [x] IBI-01 — Trim manifest.yaml to ≤150 tokens: remove `ios_build_notes` custom sub-fields from `specializes_laws` entries ✓ 2f7c338
- [x] IBI-BS-01 — Add ENG-6.7 example file (boy scout) ✓ (next commit)
- [x] IBI-BS-02 — Add ENG-6.1 example file (boy scout) ✓ (next commit)
- [x] IBI-BS-03 — Add ENG-6.4 example file (boy scout) ✓ (next commit)
- [x] IBI-BS-04 — Add AVATAR-RAG-INDEX.yaml entry (boy scout) ✓ (next commit)
- [x] IBI-02 — Add `## Non-Negotiable Laws` section to guidance.md (schema §5 required structure) ✓ (next commit)
- [x] IBI-03 — Remove hardcoded simulator UDID from guidance.md (project-specific, not domain-general) ✓ (next commit)

## Task Detail

### IBI-01 — manifest.yaml token trim
**File:** `avatars/technology/ios-build-infrastructure/manifest.yaml`
Current tokens: 353 (limit: 150). Cause: `ios_build_notes` is a custom sub-field
not in the manifest allowlist. Content is already captured in `examples/` files.
Remove `ios_build_notes` from all three `specializes_laws` entries.

### IBI-02 — guidance.md NNL section
**File:** `avatars/technology/ios-build-infrastructure/guidance.md`
Schema §5 requires `## Non-Negotiable Laws` with one `###` per law.
Laws: ENG-6.7 (audit trail integrity), ENG-4.1 (test host crash safety), ENG-4.2
(profraw alignment + 4-layer bootstrap). Statements must be grounded in Stage C
evidence (F-C-iOS-08 through F-C-iOS-11, KI-001, KI-005, KI-006, KI-007).
Must stay within 450-token total budget after addition.

### IBI-03 — Remove hardcoded UDID
**File:** `avatars/technology/ios-build-infrastructure/guidance.md`
`FD0B7FB8-3B45-44F4-8FD7-9BC7026C3181` is a machine-specific simulator UDID.
Avatars must be domain-general, not project-specific. Remove or replace with
`$(xcrun simctl list devices booted -j | jq -r '...')` pattern reference.
