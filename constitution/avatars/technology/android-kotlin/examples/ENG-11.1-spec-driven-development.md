---
law_id: ENG-11.1
avatar: android-kotlin
---

# ENG-11.1: Spec-Driven Development — Android Projects

> **Law (NON-NEGOTIABLE):** Every project adopting the Hangar AI Constitution MUST have a
> `hangar-ai-specs/` folder. All significant work follows the `PROPOSE → IMPLEMENT → ARCHIVE`
> lifecycle. No external spec tool required or permitted. A PR without a spec reference
> is not ready for review.

---

## Required Directory Structure

```
androidapps/               ← Gradle project root
  hangar-ai-specs/
    changes/               ← active proposals (one folder per work item)
    specs/                 ← current system truth documents
    archive/               ← completed proposals (dated, immutable)
    manifest-ref.yaml      ← governing avatar reference (see ENG-10.1)
  app/
  lintchecks/
  build.gradle
```

> ⚠️ `openspec/` is **prohibited**. `hangar-ai-specs/` is the only permitted name.

---

## PROPOSE → IMPLEMENT → ARCHIVE Lifecycle

### Stage 1 — PROPOSE

Scaffold a new proposal directory before writing any code:

```
hangar-ai-specs/changes/decompose-flight-status-god-class/
  PROPOSAL.md
  tasks.md
```

```yaml
# PROPOSAL.md skeleton — per ENG-11.2 (Proposal Completeness Law)
## Problem
FlightStatusViewModel is 1,247 lines. Cyclomatic complexity exceeds ENG-3.1 limit
(≤10) in 14 functions. Every new feature increases coupling to the Android framework,
making unit tests impossible without Robolectric.

## Solution
Decompose into: FlightStatusViewModel (orchestration only) + FlightStatusUseCase
(pure Kotlin domain logic) + FlightStatusRepository (interface). Domain layer has
zero Android imports per ENG-2.2.

## Deliverables
- FlightStatusUseCase.kt (pure Kotlin, JVM-testable)
- FlightStatusRepository interface + RoomFlightStatusRepository implementation
- FlightStatusViewModelTest.kt (MockK — no Robolectric)
- All ENG-3.1 violations resolved in affected files

## Success Criteria
- `./gradlew lint` reports zero ConstitutionComplexity violations in FlightStatus*
- FlightStatusViewModelTest: ≥90% line coverage, JVM only (no emulator)
- `./gradlew test` passes on CI without instrumented test suite

## References
- ENG-4.1 (Atomic TDD — tests written before each production class)
- ENG-2.2 (Layered Architecture — domain has zero Android imports)
- ENG-3.1 (Complexity Limits — cyclomatic ≤10 per Kotlin function)
- ENG-11.1 (Hangar SDD — this proposal gates implementation)
```

```markdown
# tasks.md
Progress: 0/4 tasks complete

- [ ] Task 1 — Extract FlightStatusUseCase (pure Kotlin)
  Scenario: decompose-flight-status-god-class/1.1 | Law: ENG-4.1, ENG-2.2
- [ ] Task 2 — Extract FlightStatusRepository interface
  Scenario: decompose-flight-status-god-class/1.2 | Law: ENG-2.2
- [ ] Task 3 — Slim FlightStatusViewModel to orchestration only
  Scenario: decompose-flight-status-god-class/1.3 | Law: ENG-3.1
- [ ] Task 4 — Verify ENG-3.1 gate: ./gradlew lint reports zero violations
  Scenario: decompose-flight-status-god-class/1.4 | Law: ENG-10.1
```

---

### Stage 2 — IMPLEMENT

Execute tasks in strict TDD order (ENG-4.1). Each commit references the scenario ID:

```bash
# Conventional commit referencing the spec scenario
git commit -m "feat(flight-status): extract FlightStatusUseCase to domain layer

Scenario: decompose-flight-status-god-class/1.1
Laws: ENG-4.1, ENG-2.2

- FlightStatusUseCase.kt — pure Kotlin, zero Android imports
- FlightStatusUseCaseTest.kt — 12 tests, JVM only (MockK)
- ./gradlew test passes; no Robolectric dependency added"
```

Update `tasks.md` after each completed task:

```markdown
Progress: 1/4 tasks complete

- [x] Task 1 — Extract FlightStatusUseCase (pure Kotlin)
  ✓ Commit: a1b2c3d
```

---

### Stage 3 — ARCHIVE

When all tasks are complete and the PR is merged, move the proposal to `archive/`:

```bash
# Archive: move to dated subdirectory (immutable after this point)
mv hangar-ai-specs/changes/decompose-flight-status-god-class \
   hangar-ai-specs/archive/2026-05-06-decompose-flight-status-god-class

git commit -m "chore(specs): archive decompose-flight-status-god-class

Scenario: decompose-flight-status-god-class — COMPLETE
All 4 tasks done. ENG-3.1 gate green. PR #847 merged."
```

---

## PR Gate

Every PR description MUST include a spec reference:

```
Spec: hangar-ai-specs/changes/decompose-flight-status-god-class/PROPOSAL.md
Laws verified: ENG-4.1 (tests written first), ENG-2.2 (domain has zero Android imports),
               ENG-3.1 (lint gate green — zero ConstitutionComplexity violations)
```

A reviewer MUST confirm the spec reference is present before approving.
This is a hard gate per ENG-11.1 — not a courtesy check.

## What Agents Must NOT Do

- Do not write production code before a `PROPOSAL.md` exists and is committed
- Do not use `openspec/` — the only valid directory name is `hangar-ai-specs/`
- Do not batch multiple spec proposals into one `changes/` folder
- Do not skip the ARCHIVE stage — stale entries in `changes/` are an ENG-11.3 violation
