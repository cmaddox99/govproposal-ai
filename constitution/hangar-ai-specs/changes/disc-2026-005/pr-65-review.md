---
title: "PR #65 Code Review — skill-02 Amendments 22–27"
type: evidence
date: 2026-05-14
author: Adeel Ali
reviewer: GitHub Copilot
pr: "https://github.com/AAInternal/hangar-ai-constitution/pull/65"
verdict: merge-with-fix
laws: [ENG-4.1, ENG-6.7, ENG-11.1]
---

# PR #65 Code Review — `skill-02` Amendments 22–27

**Branch:** `proposal/constitutional-companion-updates`  
**Skill:** `02-constitutional-companion` v2.24.0 → v2.27.0  
**Reviewed:** 2026-05-14  
**Verdict:** ✅ Recommend merge — one minor fix required

---

## Problem This PR Solves

The Constitutional Companion skill (`skill-02`) is the primary AI guide for engineers adopting the constitution. After live adoption sessions — including iOS/Swift coaching — several usability and maintenance problems were identified:

- The skill file was **2,306 lines** — too large for reliable partial reads, causing AI agents to miss steps mid-session
- **Adoption setup content was mixed** into the recurring companion flow — one-time governance tasks cluttered per-feature workflow
- **14 law citations were missing hyperlinks** — agents couldn't navigate directly to law definitions
- **8 iOS/Swift-specific adoption failures** from session logs had no remediation guidance
- **No CHARACTERIZE-ONLY path** for teams needing to understand code before committing to refactoring
- **Type 1 duplications** (identical content in multiple places) created drift risk

---

## How It Solves It — Amendments 22–27

### Amendment 22 — Session Log Analysis: 8 iOS/Swift Fixes (CCU-38) ✅ Complete

Analysed live iOS adoption session logs and identified 8 recurring failure patterns — wrong scheme selection, missing simulator setup, AmericanTestCore link phase issues, and others. Each pattern now has explicit guidance baked into the companion flow.

### Amendment 23 — AI Correction Prompts + Dedicated Guide (CCU-39) ✅ Complete

Created `docs/guides/adoption/ai-correction-prompts.md` — 14 failure pattern prompts engineers can paste directly into a Copilot session to recover from common AI mistakes (over-splitting methods, skipping RED step, wrong test pyramid, etc.).

### Amendment 24 — Skill File Split: Main + Setup Supplement (CCU-40) ✅ Complete

The monolithic 2,306-line skill was split into two focused files:

- **`02-constitutional-companion.md`** — the recurring per-feature workflow (1,800 lines, ~22% smaller)
- **`02-adoption-setup.md`** — one-time governance setup, Phase 3b decision tree, Phase 3d SonarQube (531 lines)

The supplement is only loaded when setting up a project for the first time, significantly reducing partial-read risk for ongoing sessions.

### Amendment 25 — CHARACTERIZE-ONLY Path + EXTEND Verdict Removal (CCU-41) ✅ Complete

Added a clean **CHARACTERIZE-ONLY** path for teams needing to understand and test existing code without immediately committing to architectural changes. The EXTEND verdict was removed — it was being used as an escape hatch to avoid proper refactoring decisions.

### Amendment 26 — Type 1 Duplication Removals (CCU-42) ⚠️ 5 of 9 Complete

5 of 9 duplicate content blocks removed. The 4 remaining (CCU-42F, 42G-GRASP, 42H, 42I) are blocked on prerequisite Type 2/3 refactoring work — clearly documented in the proposal with explicit blocker references.

### Amendment 27 — 14 Missing Law Citations Added (CCU-43) ✅ Complete

All 14 missing law citations (CCU-43A through CCU-43N) now have proper GitHub anchor hyperlinks using relative paths. All links verified to resolve correctly against current law file structure.

---

## Files Changed

| File | Change | Notes |
|---|---|---|
| `02-constitutional-companion.md` | Modified | 2,306 → 1,800 lines; iOS fixes, law citations, CHARACTERIZE-ONLY |
| `02-adoption-setup.md` | New | 531 lines; one-time governance setup |
| `docs/guides/adoption/ai-correction-prompts.md` | New | 243 lines; 14 paste-ready recovery prompts |
| `PROPOSAL.md` | Modified | Amendments 22–27 documented; ⚠️ version header stale |
| `constitutional-cross-reference-audit.md` | New | 9 duplication findings catalogued |

---

## Issue Found

### ⚠️ Version mismatch — PROPOSAL.md header (Minor)

`PROPOSAL.md` line 5 still reads `v2.24.0` but the actual skill frontmatter is `v2.27.0`. The header was not updated after Amendments 25–27 incremented the version.

**Fix:** Update `PROPOSAL.md` line 5:
```
(v2.24.0 — amended 2026-05-13)   ← current (stale)
(v2.27.0 — amended 2026-05-13)   ← correct
```

---

## Verification Checks

| Check | Result |
|---|---|
| YAML frontmatter valid (both skill files) | ✅ Pass |
| All 14 law citation hyperlinks resolve | ✅ Pass |
| File split cross-references wired correctly | ✅ Pass |
| Amendment 26 blocked tasks documented | ✅ Pass |
| Task count accurate (74/78) | ✅ Pass |
| Cross-reference audit thorough | ✅ Pass |
| No trigger phrase collisions introduced | ✅ Pass |
| PROPOSAL.md version header | ⚠️ Stale — fix before merge |

---

## Remaining / Follow-on Work

- **CCU-42F, 42G, 42H, 42I** — 4 Type 1 duplication removals blocked on prerequisite Type 2/3 changes. Tracked in proposal.
- **Type 2/3 duplications** — identified in cross-reference audit, out of scope for this PR. Future proposal.
- **PROPOSAL.md version** — one-line fix: `v2.24.0` → `v2.27.0`.

---

## Verdict

**✅ Recommended: Merge after one-line fix**

This is a high-quality, well-documented improvement to a critical skill. The file split alone significantly reduces AI partial-read risk. All law citations, YAML, and cross-references verified clean. Fix the version header and merge.
