# Tasks: Avatar Token Budget Overflow Pattern

**Proposal:** [PROPOSAL.md](PROPOSAL.md)
**Spec ID:** `avatar-full-reference-pattern`
**Status:** 📋 PROPOSED

---

## Prerequisites

- [ ] Amendment P (PR #14) merged to `main` before Phase 3 (linter revert) executes

---

## Phase 1: Constitutional Guide (D1)

> **Goal:** Produce `docs/guides/constitution/avatar-reference-doc-architecture.md` — the
> canonical human reference for the complete avatar token budget overflow pattern.

- [ ] 1.1 Write `docs/guides/constitution/avatar-reference-doc-architecture.md` with all required sections:
  - Section 1: Four-layer architecture table (all budgets, load strategies, overflow indicators)
  - Section 2: RAG hybrid architecture explanation (embedding model + routing pointer model; why search_queries entries are required; the unreachable-file failure mode)
  - Section 3: Overflow vs. shrink decision table (per file type, with trigger conditions and acceptable-shrink criteria)
  - Section 4: Overflow file conventions — establish naming and location for all four file types (guidance.md → `full-reference.md` is the established precedent; determine the conventions for examples/, use-cases/, manifest.yaml overflow files)
  - Section 5: Required location rule — all overflow files inside the avatar directory; why this is governance not convention
  - Section 6: Two-step RAG registration procedure (`files:` block entry + `search_queries:` routing entries; minimum one routing entry per major section)
  - Section 7: C++ avatar as reference implementation (links to `avatars/technology/cpp/full-reference.md` and the `cpp` block in `AVATAR-RAG-INDEX.yaml`)
- [ ] 1.2 Write ONE failing test asserting guide exists and required sections are present (RED)
- [ ] 1.3 Write content to make test pass (GREEN)
- [ ] 1.4 Review and refine prose quality (REFACTOR)
- [ ] 1.5 Run full test suite + `aa-constitution-lint .` (VERIFY)

## Phase 2: Agent Skill (D2 + D3)

> **Goal:** Produce `skill-avatar-token-overflow.md` so AI agents apply the overflow strategy
> proactively instead of silently shrinking content below the point of usefulness.

- [ ] 2.1 Write `agent-skills/skills-by-domain/platform-engineering/skill-avatar-token-overflow.md` with:
  - YAML frontmatter: id, name, domain, laws, triggers, version
  - Core principle quote (verbatim from guide Section 3): "Shrinking content below the point of usefulness is always worse than exceeding a token budget…"
  - Decision tree: identify file type → apply overflow/shrink rule → create overflow file → register in RAG index (two steps) → link from source file → verify with linter
  - Per-file-type procedure table (guidance.md, examples/*.md, use-cases/*.md, manifest.yaml) using conventions from D1 Section 4
  - Explicit warning: omitting `search_queries:` entries is the failure mode — the overflow file becomes unreachable
  - Reference to the guide (D1) and C++ reference implementation
- [ ] 2.2 Register skill in `agent-skills/skills-by-domain/platform-engineering/index.yaml`:
  - Add entry with file, name, triggers, and laws
  - Triggers must include: "guidance.md exceeds token budget", "example file too large", "token budget exceeded", "content too large for avatar file", "where does overflow content go", "how do I handle overflow"
- [ ] 2.3 Write ONE failing test asserting skill exists and required sections are present (RED)
- [ ] 2.4 Write content to make test pass (GREEN)
- [ ] 2.5 Run full test suite + `aa-constitution-lint .` (VERIFY)

## Phase 3: Linter Patch Revert (D4 + D5)

> **Goal:** Revert `f2e1552` to restore `AvatarRagFilesExistRule` avatar-relative enforcement.
> **⛔ Prerequisite: Amendment P (PR #14) must be merged to `main` before this phase executes.**

- [ ] 3.1 Revert commit `f2e1552` — restores avatar-directory-relative path resolution in `AvatarRagFilesExistRule`
- [ ] 3.2 Run `aa-constitution-lint .` on `main` — must PASS
- [ ] 3.3 Add or update linter unit test confirming that `docs/`-prefixed paths in avatar `files:` blocks are rejected (not silently accepted)
- [ ] 3.4 Run full linter test suite — all tests must pass

## Phase 4: Commit and PR

- [ ] 4.1 Commit Phase 1: `docs(constitution): avatar-reference-doc-architecture guide (avatar-full-reference-pattern/D1)`
- [ ] 4.2 Commit Phase 2: `feat(skill): skill-avatar-token-overflow — overflow-vs-shrink decision procedure (avatar-full-reference-pattern/D2-D3)`
- [ ] 4.3 Commit Phase 3: `fix(lint): revert f2e1552 — restore avatar-relative path enforcement (avatar-full-reference-pattern/D4-D5)`
- [ ] 4.4 Open new PR targeting `main` (independent of PR #14)
- [ ] 4.5 Reference this proposal, Amendment O, and Amendment P in PR description

---

## Progress Summary

| Phase | Tasks | Done |
|-------|-------|------|
| Phase 1: Constitutional Guide | 5 | 0 |
| Phase 2: Agent Skill | 5 | 0 |
| Phase 3: Linter Patch Revert | 4 | 0 |
| Phase 4: Commit and PR | 5 | 0 |
| **Total** | **19** | **0** |
