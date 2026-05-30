# Proposal: Android Kotlin Avatar — Assess & Correct (Mode 2)

**Proposal ID:** android-kotlin-avatar-assess-correct  
**Spec Scenario ID:** android-kotlin-avatar-assess-correct/1.0  
**Date:** 2026-05-05  
**Workflow:** Avatar Workflow — Mode 2 (Assess & Correct)  
**Laws:** ENG-11.1 (NON-NEGOTIABLE), ENG-1.2 (NON-NEGOTIABLE), ENG-10.1, ENG-4.1

---

## 1. Problem Statement

Avatar Workflow Mode 3 (Validate) run on `avatars/technology/android-kotlin` on 2026-05-05
identified **2 BLOCKING violations** that prevent any dependent workflow (Product Discovery,
Legacy Rescue Decision Track) from starting:

| # | Violation | Severity | Phase |
|---|-----------|----------|-------|
| 1 | `guidance.md` missing required `## Non-Negotiable Laws` section (schema §5) | 🔴 BLOCKING | Phase 2, Phase 5/Q3 |
| 2 | `manifest.yaml` ≈ 2,936 tokens — 19.6× over the 150-token budget | 🔴 BLOCKING | Phase 2, Phase 5/Q4 |

Plus 5 non-blocking findings:

| # | Finding | Severity |
|---|---------|----------|
| 3 | `guidance.md` states "JUnit 5 + fastlane CI" — contradicts manifest (JUnit 4, no fastlane) | 🟡 SHADOW GOVERNANCE |
| 4 | `guidance.md` frontmatter `version: "1.1.0"` conflicts with manifest `version: "1.3.0"` | 🟡 WARN |
| 5 | `manifest.yaml` ENG-11.1 android_note says "GAP: hangar-ai-specs/ does NOT yet exist" — stale (created 2026-05-05) | 🟡 WARN |
| 6 | `activates.workflows` missing `legacy-rescue-decision-track` (androidapps is a legacy codebase) | 🟡 WARN |
| 7 | `manifest.yaml` `android_note` fields on every law entry (main source of token bloat beyond cross-avatar norm) | 🟡 WARN |

## 2. Solution

Apply Mode 2 (Assess & Correct) per the Avatar Workflow:

1. **Fix guidance.md** — rewrite to schema §5 required structure (Overview + Non-Negotiable Laws + Key Patterns + Anti-Patterns), fix stale JUnit 5 / fastlane data, fix version to 1.3.0
2. **Reduce manifest token bloat** — remove `android_note` fields from all `specializes_laws` entries; these belong in `guidance-detail.md` or `examples/` files. Move `conventions.test_idioms` and `conventions.patterns` detail to `guidance-detail.md`
3. **File ENG-10.3 Exception Request** — per the cpp-manifest-token-exception precedent, even after removing android_notes the remaining schema-permitted content will exceed 150 tokens; an ENG-10.3 exception is required
4. **Add `legacy-rescue-decision-track`** to `activates.workflows`
5. **Update ENG-11.1 android_note** to reflect current state (hangar-ai-specs/ created)

## 3. Deliverables

- [ ] `avatars/technology/android-kotlin/guidance.md` — rewritten to schema §5 structure (≤450 tokens; Non-Negotiable Laws section present)
- [ ] `avatars/technology/android-kotlin/manifest.yaml` — android_notes removed; activates.workflows updated; ENG-11.1 note updated
- [ ] `hangar-ai-specs/changes/android-kotlin-manifest-token-exception/PROPOSAL.md` — ENG-10.3 exception request
- [ ] `tests/unit/test_android_kotlin_avatar/` — test suite validating all fixes
- [ ] `avatars/technology/android-kotlin/examples/ENG-10.1-constitution-governance.md` — new example file (schema §1 required)
- [ ] `avatars/technology/android-kotlin/examples/ENG-11.1-spec-driven-development.md` — new example file (NON-NEGOTIABLE law, schema §1 required)
- [ ] RAG Validate 5/5 passing after corrections

## 4. Success Criteria

- `guidance.md` has `## Non-Negotiable Laws` section — per schema §5
- `guidance.md` mentions JUnit 4 (not JUnit 5), no fastlane
- `guidance.md` frontmatter version = `1.3.0`
- `manifest.yaml` has no `android_note` fields
- `manifest.yaml` `activates.workflows` includes `legacy-rescue-decision-track`
- RAG Q3 ("non-negotiable rules") answered from guidance.md ✅
- Constitution lint passes
- All tests green

## 5. Law References

- ENG-4.1: Atomic TDD Law — all corrections written test-first
- ENG-10.1: Constitution Metrics Collection Law — avatar compliance tracked
- ENG-11.1: Hangar SDD Law — this proposal is the spec before correction begins
- ENG-10.3: Compliance Reporting Law — ENG-10.3 Exception Request required for manifest token budget
