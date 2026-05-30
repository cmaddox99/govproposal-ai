# Proposal: Add iOS/Swift (Muter) and Android (ArcMutate) to Mutation Testing Tool Tables

**Status:** In Progress
**Spec ID:** `mutation-testing-mobile-tooling`
**Law reference:** ENG-4.11 (Mutation Testing Law), ENG-11.1 (Hangar SDD)

---

## Problem Statement

The mutation testing skill (`skill-11-mutation-testing.md`) and the legacy rescue
refactor workflow (`legacy-rescue-refactor.md`) both contain tool tables listing
supported stacks. Both tables are missing mobile stack entries:

| Missing Entry | Tool | Source of truth |
|---|---|---|
| iOS / Swift | Muter v16 | `runbooks/disc-2026-004-impediment-resolution.md` |
| Android / Kotlin | ArcMutate (Pitest-Android) | `runbooks/disc-2026-004-impediment-resolution.md` |

The refactoring workflow already has a row for `Kotlin / Android → PIT
(pitest-maven)` but it is incomplete — it points to Java's pitest-maven
rather than the Android-specific ArcMutate plugin, and it omits Muter for iOS
entirely.

The runbook `disc-2026-004-impediment-resolution.md` contains the correct
setup for both tools from a live run but this knowledge is not surfaced in the
canonical skill or workflow reference tables.

**Impact:** An agent or engineer following ENG-4.11 for an iOS or Android
codebase has no constitution-authoritative tool reference. They must either
guess or find the runbook themselves.

---

## Solution

### File 1: `agent-skills/skills-by-domain/development-practices/11-mutation-testing.md`

Add two rows to the "Step 1: Select Tool by Language" table:

| Language | Tool | Command | Notes |
|---|---|---|---|
| iOS / Swift | Muter | `muter run --format json --output muter-report.json` | Requires `muter init` first |
| Android / Kotlin | ArcMutate (Pitest-Android) | `./gradlew :<module>:pitestDebug` | Requires `com.arcmutate.pitest-android` licence |

Add Muter docs reference to the References section.

### File 2: `workflows/legacy-rescue-refactor.md`

**Tool table (line ~479):** Replace the incomplete `Kotlin / Android` row and
add the iOS row:

| Stack | Tool | Run Command | Report Location |
|---|---|---|---|
| **iOS / Swift** | Muter v16 | `muter run --format json --output muter-report.json` | `muter-report.json` |
| **Android / Kotlin** | ArcMutate (Pitest-Android) | `./gradlew :<module>:pitestDebug` | `build/reports/pitest/` |

**Running Mutation Testing section (line ~617):** Add an iOS/Swift block
(parallel to the existing Java, Python, TypeScript, .NET blocks).

---

## Open Design Question: Single Source of Truth for Tool Tables

The mutation testing tool table currently exists (in full or partial form) in multiple files:
- `agent-skills/skills-by-domain/development-practices/11-mutation-testing.md`
- `workflows/legacy-rescue-refactor.md`
- Potentially others (workflows, avatar guidance files)

Every time a new technology avatar is added to the constitution, all of these tables must be updated in sync — a maintenance burden that grows with the avatar count.

**Options:**
1. **Status quo (multiple copies)** — simplest now, drift risk long-term
2. **Single canonical source in the skill** — workflow references the skill table (no duplication); requires cross-file linking convention
3. **Dedicated reference file** — e.g., `docs/guides/testing/mutation-testing-tool-registry.md` that all files cite

This proposal does not resolve the design question but flags it for a follow-on proposal. This change proceeds with option 1 (status quo), with the tool tables kept in sync as part of this change.

---

## Changes

| File | Change |
|---|---|
| `laws/engineering/testing.md` | Add iOS/Swift (Muter) and Android/Kotlin (pl.droidsonroids.pitest) to ENG-4.11 Tool Selection table |
| `agent-skills/skills-by-domain/development-practices/11-mutation-testing.md` | Add iOS/Swift and Android/Kotlin rows to tool selection table; add Muter + droidsonroids docs refs |
| `workflows/legacy-rescue-refactor.md` | Replace incorrect `Kotlin/Android → PIT (pitest-maven) → same as Java` row; add iOS/Swift (Muter) row; add iOS/Swift and Android/Kotlin run blocks to Phase 7 section; remove phantom law citations `ENG-3.9`/`ENG-3.10`/`ENG-3.11` (OCP/LSP/ISP — never authored or registered) from frontmatter and Phase 8 section; replace with plain SOLID principle names |
| `runbooks/disc-2026-004-impediment-resolution.md` | Correct iOS Muter entry (Homebrew install, HTML format, drop /tmp path); correct Android entry (replace non-existent ArcMutate plugin with pl.droidsonroids.pitest) |

---

## Additional Changes (2026-05-26 — CI Fix)

**Phantom citation removal:** `workflows/legacy-rescue-refactor.md` referenced `ENG-3.9` (OCP), `ENG-3.10` (LSP), and `ENG-3.11` (ISP) in six locations (frontmatter `laws:` list, Phase 8 table, Phase 9 table, Phase 8 constitutional basis note, SOLID audit table, Phase 8.3 gate). These IDs were never authored or registered in `laws/index.yaml`; the registry ends at ENG-3.8. The phantom citations caused Citation Audit CI failures on this PR.

**Decision:** Do not author stub laws. Bad references are bad references. The phantom IDs were replaced with plain SOLID principle names (OCP, LSP, ISP) where the meaning needed to be retained. ENG-3.4 (SRP) and ENG-2.5 (DIP) — which are registered — were preserved as law citations.

**Follow-on work:** Authoring `ENG-3.9` (OCP), `ENG-3.10` (LSP), `ENG-3.11` (ISP) as full governed laws with enforceable criteria is deferred to a future proposal. Until then, Phase 8 SOLID Rescue enforces OCP/LSP/ISP as engineering principles without constitutional law backing.
