# Proposal: Consolidate Mutation Testing Tool Table to Single Source of Truth

**Status:** Implemented — commit `17b2c40` on `feat/mutation-tool-table-ssot`
**Spec ID:** `mutation-tool-table-ssot`
**Triggered by:** Multi-LLM jury finding during `mutation-testing-mobile-tooling` implementation (PR #78) — Go tool `cosmic-ray` appearing in two files (law + skill) while workflow correctly uses `gremlins`, confirming active drift across three unsynchronised copies.
**Law reference:** ENG-4.11 (Mutation Testing Law), ENG-11.1 (Hangar SDD)

---

## Problem Statement

The mutation testing tool selection table exists in three files:

| File | Columns | Stacks | Purpose |
|---|---|---|---|
| `laws/engineering/testing.md` | 2 (Language, Tool) | 5 | Normative tool mandate in ENG-4.11 |
| `agent-skills/.../11-mutation-testing.md` | 4 (Language, Tool, Command, Notes) | 6 | Operational reference agents load via RAG |
| `workflows/legacy-rescue-refactor.md` | 4 (Stack, Tool, Command, Report Path) | 7 | Procedural run blocks for Legacy Rescue Phase 7 |

Three-way duplication creates a synchronisation obligation on every avatar addition or tool update. This obligation is not enforced automatically — drift is already present:

| Location | Go tool listed | Correct? |
|---|---|---|
| `laws/engineering/testing.md` | `cosmic-ray` | ❌ `cosmic-ray` is a Python mutation framework |
| `agent-skills/.../11-mutation-testing.md` | `cosmic-ray` | ❌ same error |
| `workflows/legacy-rescue-refactor.md` | `gremlins` | ✅ correct Go mutation testing tool |

The law and skill files both carry the wrong tool for Go while the workflow is correct — a live drift case discovered during the preceding mobile tooling jury.

**Impact:**
1. An agent following ENG-4.11 for a Go project will be directed to the wrong tool.
2. Every new technology avatar addition requires three synchronised edits with no lint guard.
3. A law file containing operational tool details (install commands, binary names) creates a category mismatch: laws mandate *what*, skills mandate *how*.

---

## Jury Findings (Multi-LLM Review, 2026-05-26)

Three jurors were convened to evaluate the SSOT design options:

### ssot-architecture (Claude Opus 4.5)

- **Option 2 (law as SSOT) is not viable.** Agents follow the RAG protocol: `index.yaml` → matched skill `.md`. They do not chain-load law files for operational commands. Cross-file references in the law would not be reliably followed by the agent RAG loop.
- Recommends: skill file as operational SSOT; workflow keeps self-contained procedural blocks (serves a different audience/context).
- Also confirmed the Go tool inconsistency independently.

### ssot-governance (GPT-5.2)

- Tool tables inside law files are a **category error** — laws should specify thresholds and outputs (`≥70% mutation score`), not binary names or install commands.
- "Lowest overhead" path: **remove the table from the law**; replace with one delegation sentence pointing to skill-11; skill becomes de facto SSOT without introducing a new registry file.
- If a registry is ever warranted (>8 stacks), it should be Markdown + YAML frontmatter, require a named owner, and include an explicit delegation reference from the law.

### ssot-inventory (Claude Haiku 4.5)

- Confirmed exactly **3 files** contain mutation tool tables — no hidden copies in `docs/guides/testing/`, avatar guidance files, or governance archives.
- Confirmed Go inconsistency: `cosmic-ray` in law + skill, `gremlins` in workflow.
- Flagged naming variation: "Pitest" vs "PIT (pitest-maven)" across files.

### Jury consensus

| Option | Verdict |
|---|---|
| Status quo (3 copies) | Rejected — drift already occurring |
| Law as SSOT | Rejected — breaks agent RAG protocol |
| New dedicated registry | Viable but premature at current stack count |
| **Drop law table, skill as SSOT** | **Accepted — lowest overhead, correct architecture** |

---

## Solution

### Principle

- **`laws/engineering/testing.md`** — mandates thresholds, outputs, and requirements only. No tool names or commands. Delegates to skill-11 for tool selection.
- **`skill-11-mutation-testing.md`** — canonical SSOT for tool selection. Agents load this via the RAG protocol. This is where the full table lives.
- **`workflows/legacy-rescue-refactor.md`** — keeps its self-contained run blocks. They serve a different purpose (step-by-step procedure for a specific workflow context) and are intentionally more verbose than a reference table. The workflow adds a one-line citation pointing to skill-11 as the canonical source.

This reduces synchronisation obligation from 3 files to 1 (skill). Law and workflow are no longer competing sources.

### Change 1: Fix Go tool in `laws/engineering/testing.md` and `skill-11-mutation-testing.md`

Replace `cosmic-ray` (Python tool, wrong) with `gremlins` (correct Go mutation testing tool) in both files.

### Change 2: Remove tool table from `laws/engineering/testing.md`

Replace the ENG-4.11 "Tool Selection" table with a delegation paragraph:

> **Tool Selection:** Use the tool designated for your language/platform in the Mutation Testing Skill (`agent-skills/skills-by-domain/development-practices/11-mutation-testing.md`, Step 1). The skill is the canonical source of approved mutation tools and commands.

The threshold requirements, output format requirements, and enforcement rules remain in the law — only the tool enumeration is removed.

### Change 3: Add citation to `workflows/legacy-rescue-refactor.md`

Add a one-line note above the Tech Stack Translation table pointing to skill-11 as the canonical reference, so engineers know where to find the authoritative source if the workflow table and skill table ever differ.

---

## Changes

| File | Change |
|---|---|
| `laws/engineering/testing.md` | Replace ENG-4.11 tool table with delegation sentence; fix `cosmic-ray` → `gremlins` (moot after table removal, but fix the body text if referenced anywhere) |
| `agent-skills/skills-by-domain/development-practices/11-mutation-testing.md` | Fix `cosmic-ray` → `gremlins` for Go row |
| `workflows/legacy-rescue-refactor.md` | Add one-line skill-11 citation above Tech Stack Translation table; fix `cosmic-ray` → `gremlins` if present |

---

## Out of Scope

- Coverage tool tables (Jacoco, Istanbul, etc.) appearing in the same workflow section — a separate proposal if warranted.
- Automated lint guard for table synchronisation — out of scope; addressed by removing the duplication rather than enforcing sync.
- Creating a dedicated registry file — deferred; revisit if stack count exceeds 8 entries.
