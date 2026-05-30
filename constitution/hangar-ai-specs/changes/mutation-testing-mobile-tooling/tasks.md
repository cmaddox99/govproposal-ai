# Tasks — Add iOS/Swift and Android to Mutation Testing Tool Tables

**Spec ID:** `mutation-testing-mobile-tooling`
**Status:** Complete

## Task List

- [x] MMT-01 — Add iOS/Swift (Muter) and Android/Kotlin (pl.droidsonroids.pitest) to ENG-4.11 Tool Selection table in `laws/engineering/testing.md` ✓
- [x] MMT-02 — Add iOS/Swift and Android/Kotlin rows to tool selection table in `skill-11-mutation-testing.md` ✓
- [x] MMT-03 — Add Muter + droidsonroids docs references to `skill-11-mutation-testing.md` ✓
- [x] MMT-04 — Replace incorrect `Kotlin/Android → PIT (pitest-maven) → same as Java` row in `legacy-rescue-refactor.md` stack table; add iOS/Swift (Muter) row ✓
- [x] MMT-05 — Add iOS/Swift (Muter) and Android/Kotlin (pl.droidsonroids.pitest) run blocks to "Running Mutation Testing (Phase 7)" section in `legacy-rescue-refactor.md` ✓
- [x] MMT-06 — Correct runbook `disc-2026-004-impediment-resolution.md`: replace non-existent ArcMutate Android plugin with pl.droidsonroids.pitest; replace /tmp Muter binary path with Homebrew install + HTML format ✓
- [ ] MMT-07 — Run constitution lint; verify no regressions
- [ ] MMT-08 — Commit with spec ID reference

## Jury Findings (pre-implementation)

Key findings that shaped the implementation:
- **juror-technical:** ArcMutate has no Android product; `com.arcmutate.pitest-android` does not exist; correct tool is `pl.droidsonroids.pitest` v0.2.27 (OSS, updated March 2026)
- **juror-completeness:** `laws/engineering/testing.md` (ENG-4.11 itself) has its own tool table — missed in original scope
- **juror-impact:** Muter supports `--format html`; use system command not `/tmp` path; Android run block needed for parity
- **juror-constitutional:** ArcMutate licence + ENG-4.12 hard block = unrecoverable compliance gap (resolved by using OSS tool)

## Follow-on: Single Source of Truth

The mutation testing tool table is now duplicated across 3 files. A separate proposal should evaluate
collapsing to a single canonical source (e.g., in the law file) with other files referencing it.

