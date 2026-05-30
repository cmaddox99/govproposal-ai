# Tasks: android-kotlin-avatar-assess-correct

Spec Scenario ID: android-kotlin-avatar-assess-correct

Progress: 9/9 tasks complete ✅

---

## Tasks

- [x] Task 1 — `guidance.md`: Add `## Non-Negotiable Laws` section (schema §5 required structure)
  - Scenario: android-kotlin-avatar-assess-correct/1.1
  - Law: ENG-11.1, ENG-10.1
  - Test: `test_guidance_has_non_negotiable_laws_section`
  - ✓ Commit: b676dca

- [x] Task 2 — `guidance.md`: Fix stale stack line (JUnit 4 not JUnit 5; no fastlane)
  - Scenario: android-kotlin-avatar-assess-correct/1.2
  - Law: ENG-10.1
  - Test: `test_guidance_stack_reflects_junit4_not_junit5`
  - ✓ Covered by Task 1 rewrite (b676dca)

- [x] Task 3 — `guidance.md`: Fix frontmatter version to match manifest (1.3.0)
  - Scenario: android-kotlin-avatar-assess-correct/1.3
  - Law: ENG-10.1
  - Test: `test_guidance_version_matches_manifest`
  - ✓ Covered by Task 1 rewrite (b676dca)

- [x] Task 4 — `manifest.yaml`: Remove `android_note` fields from all specializes_laws entries
  - Scenario: android-kotlin-avatar-assess-correct/1.4
  - Law: ENG-10.1
  - Test: `test_manifest_has_no_android_notes`

- [x] Task 5 — `manifest.yaml`: Add `legacy-rescue-decision-track` to activates.workflows
  - Scenario: android-kotlin-avatar-assess-correct/1.5
  - Law: ENG-11.1
  - Test: `test_manifest_activates_legacy_rescue_workflow`

- [x] Task 6 — `manifest.yaml`: Update ENG-11.1 android_note (stale gap warning — hangar-ai-specs/ now exists)
  - Scenario: android-kotlin-avatar-assess-correct/1.6
  - Law: ENG-11.1
  - Note: Covered as part of Task 4 (android_notes removed entirely)
  - ✓ Covered by Task 4

- [x] Task 7 — `examples/ENG-10.1-constitution-governance.md`: Create missing example file
  - Scenario: android-kotlin-avatar-assess-correct/1.7
  - Law: ENG-10.1
  - Test: `test_eng_10_1_example_exists_and_valid`
  - Note: Schema §1 requires one example per specializes_law; ENG-10.1 is declared in manifest but has no example file

- [x] Task 8 — `examples/ENG-11.1-spec-driven-development.md`: Create missing example file
  - Scenario: android-kotlin-avatar-assess-correct/1.8
  - Law: ENG-11.1
  - Test: `test_eng_11_1_example_exists_and_valid`
  - Note: ENG-11.1 is NON-NEGOTIABLE; missing example is a schema violation

- [x] Task 9 — `AVATAR-RAG-INDEX.yaml`: Correct stale android-kotlin entry
  - Scenario: android-kotlin-avatar-assess-correct/1.9
  - Law: ENG-10.1, ENG-11.1
  - Test: `test_rag_index_android_kotlin_entry`
  - Issues: JUnit 5 → JUnit 4 (×3); fastlane → Gradle+Jenkins (×3); add eng_10_1 + eng_11_1 to files block; add ENG-10.1 + ENG-11.1 to specializes_laws; fix search_queries and use_cases
