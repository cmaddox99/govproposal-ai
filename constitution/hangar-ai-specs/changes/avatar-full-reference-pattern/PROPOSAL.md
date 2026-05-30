# Proposal: Avatar Token Budget Overflow Pattern

**Status:** 📋 PROPOSED
**Spec ID:** `avatar-full-reference-pattern`
**Triggered by:** Amendment O (PR #14) + Amendment P investigation (April 12, 2026) —
`full-reference.md` was created for the C++ avatar without constitutional documentation of the
pattern, without correct placement, and without a generalized strategy for other budget-constrained
files. This proposal formalizes the overflow pattern for **all four token-budget file types**,
corrects the linter patch that masked the placement violation, and produces a new agent skill
so AI agents stop silently shrinking content and instead apply the correct overflow strategy.
**Scope:**
1. Human guide — `docs/guides/constitution/avatar-reference-doc-architecture.md`
2. Agent skill — `agent-skills/skills-by-domain/platform-engineering/skill-avatar-token-overflow.md`
3. Linter revert — `f2e1552` reverted on `main`

**Independent of:** PR #14 (`c-plus-plus-avatar-enrichment`) — this is its own PR

---

## Problem Statement

### P1 — The Overflow Pattern is Undocumented for All File Types

The constitutional documentation on `main` describes only a 3-layer avatar architecture with hard
token budgets and no documented overflow strategy:

| Layer | File | Budget | Load Strategy |
|-------|------|--------|---------------|
| 1 | `guidance.md` | 200–450 tokens | Always loaded |
| 2 | `examples/*.md` | 750–850 tokens each | On-demand by law |
| 3 | `use-cases/*.md` | 1,200–1,500 tokens | On-demand by scenario |
| 4 | `manifest.yaml` | ~100 tokens | Always loaded |

When any of these limits is exceeded, the current documented behavior is: **make it fit**.
There is no documented path that says "when fitting degrades quality below usefulness, create an
overflow file." The `full-reference.md` pattern introduced by Amendment O (PR #14) for `guidance.md`
is not documented on `main` and has no generalisation to the other three file types.

### P2 — AI Agents Default to Shrink-to-Fit, Degrading Quality

Without explicit overflow guidance, AI agents follow the token budget as a hard constraint. The
current strategy is to reduce detail until the content fits. In practice this means:

- `guidance.md` trimmed until it contains no actionable patterns — just law names
- `examples/*.md` compressed until the code snippet is a skeleton with no explanation
- `use-cases/*.md` cut until the scenario has no decision rationale
- `manifest.yaml` blocks removed rather than extracted to a companion file

The C++ avatar demonstrated the damage: `guidance.md` was trimmed from 5,693 lines of actionable
guidance to a 29-line stub with no engineering detail. The AI could respond to C++ questions but
with no constitutional backing — it was effectively unguided. Amendment O recovered the content via
`full-reference.md`, but only because a human noticed and intervened. The next avatar will face the
same failure silently unless the AI has a skill that prevents it.

**The core principle missing from agent instructions:**
> Shrinking content below the point of usefulness is always worse than exceeding a token budget.
> Token budgets protect RAG performance, not content quality. When a budget would force a quality
> degradation, the correct response is to overflow — not to fit.

### P3 — The Two-Step Requirement is Undocumented

Creating an overflow file is only half the work. The file must also be registered in
`AVATAR-RAG-INDEX.yaml` with explicit `search_queries:` routing entries. Without these entries,
the overflow file is unreachable in practice:

- The AI agent will not know to load it for relevant queries
- The content is embedded by `text-embedding-3-large` at index-build time, but without routing
  hints the AI has no signal to retrieve the right section for the right question
- The `search_queries:` entries are lightweight (~10 tokens each) and do not bloat the index —
  they are pointers, not content

**The failure mode:** overflow file exists, `files:` block in AVATAR-RAG-INDEX.yaml references it,
but no `search_queries:` entries map topic questions to its sections. The file is there but dark.

### P4 — Linter Patch `f2e1552` Weakens a Correct Governance Rule

Commit `f2e1552` (April 11 17:35 CST) patched `AvatarRagFilesExistRule` to accept
repo-root-relative paths in avatar `files:` blocks. The original rule enforced that all files
declared in an avatar's RAG index must reside inside that avatar's directory. This is intentional
governance — avatars are self-contained units. The patch was written to silence a linter error
caused by `full-reference.md` being placed incorrectly at `docs/guides/avatars/cpp/`.
Amendment P (PR #14) corrects the C++ placement. This proposal reverts the patch.

---

## Solution

### S1 — Human Guide: `docs/guides/constitution/avatar-reference-doc-architecture.md`

A canonical constitutional guide covering the complete avatar reference-doc architecture:

**Section 1 — The Four-Layer Architecture**
Full table of all four layers with budgets, load strategies, and overflow indicators.

**Section 2 — RAG Architecture: How Retrieval Actually Works**
Explain the hybrid model so authors understand *why* the rules are what they are:
- `text-embedding-3-large` embeds file content into the vector index at build time
- `AVATAR-RAG-INDEX.yaml` `search_queries:` entries are explicit routing pointers (~10 tokens each)
  that tell the AI agent which file/section to load for specific question types
- On-demand files are **not** loaded into context unless a query routes to them — the pointer
  is what makes them reachable, not just their presence on disk
- Adding overflow file entries to `search_queries:` is lightweight and does **not** degrade
  RAG performance; omitting them leaves the file unreachable

**Section 3 — When to Overflow vs. Shrink**
Decision criteria for each file type:

| File Type | Overflow Trigger | Shrink Acceptable When |
|-----------|-----------------|------------------------|
| `guidance.md` | Actionable engineering patterns no longer fit in ≤450 tokens | Content is genuinely redundant or covered by example files |
| `examples/*.md` | Code + explanation cannot convey the law's intent within ≤850 tokens | Example is illustrative only, not a full implementation reference |
| `use-cases/*.md` | Scenario decision rationale is lost within ≤1,500 tokens | Use case is simple enough that a summary is sufficient |
| `manifest.yaml` | A configuration block is too large to inline but is authoritative | Block is optional/illustrative and can be documented in an example |

**Core principle — "Never Silently Shrink" (ENG-1.2 Non-Negotiable):**
> Shrinking content below the point of usefulness is always worse than exceeding a token budget.
> Token budgets exist to protect RAG context performance, not to justify degrading guidance quality.
> When a budget would force a quality degradation, the correct response is to overflow and register.

This principle is **non-negotiable** under ENG-1.2 (Human Oversight). An AI agent that silently
discards actionable guidance to make content fit has made a unilateral quality decision without
human knowledge — exactly the class of silent action ENG-1.2 forbids. The agent skill (S2) must
surface this decision explicitly so a human can confirm or override it.

**Section 4 — Overflow File Conventions**
All overflow file names and locations must follow these established conventions (C++ avatar
sets the canonical precedent; all future avatars must use the same patterns):

| Source File | Budget | Overflow File | Location |
|-------------|--------|---------------|----------|
| `guidance.md` | ≤450 tokens | `full-reference.md` | `avatars/{category}/{name}/full-reference.md` |
| `examples/{law-id}.md` | ≤850 tokens | `examples/extended/{law-id}.md` | `avatars/{category}/{name}/examples/extended/` |
| `use-cases/{scenario}.md` | ≤1,500 tokens | `use-cases/{scenario}/extended.md` | `avatars/{category}/{name}/use-cases/{scenario}/` |
| `manifest.yaml` | ~100 tokens inline | `manifest-extended.yaml` | `avatars/{category}/{name}/manifest-extended.yaml` |

**Design rationale for naming conventions:**
- `full-reference.md` — mirrors the established C++ precedent exactly; all avatars use the same name
- `examples/extended/{law-id}.md` — mirrors the source file's law-id; keeps extended examples co-located
  with their source in a dedicated `extended/` subdirectory to prevent mixing with budget-compliant examples
- `use-cases/{scenario}/extended.md` — promotes scenario to a directory; `extended.md` is the overflow companion
- `manifest-extended.yaml` — symmetric naming with source; YAML format preserved for parsability

**Implementation note:** These conventions are first-pass proposals. The human guide (D1) and
agent skill (D2) will be the authoritative source once ratified. Any avatar that diverges from
these conventions must include a `# Convention note:` comment justifying the deviation and
must update the guide.

**Section 5 — Required Location**
All overflow files must reside inside the avatar directory (`avatars/{category}/{avatar-name}/`),
not in `docs/`. Avatar directories are self-contained governance units. The linter enforces this.

**Section 6 — AVATAR-RAG-INDEX.yaml Registration: Two Required Steps**
1. Add an entry to the `files:` block (relative filename, no repo-root path)
2. Add `search_queries:` entries mapping topic questions to overflow file sections with token estimates
Omitting step 2 is the failure mode — the file is unreachable even if step 1 is complete.

**Section 7 — C++ as Reference Implementation**
Point to `avatars/technology/cpp/full-reference.md` + the `cpp` block in `AVATAR-RAG-INDEX.yaml`
as the canonical working example of the full pattern.

---

### S2 — Agent Skill: `skill-avatar-token-overflow.md`

A new skill in `agent-skills/skills-by-domain/platform-engineering/` that gives AI agents an
explicit decision procedure whenever a token budget is encountered during avatar construction or
enrichment.

**Triggers (to be registered in `index.yaml`):**
- "guidance.md is too long", "guidance.md exceeds token budget"
- "example file is too large", "example exceeds 850 tokens"
- "use case is too long", "manifest is too large"
- "token budget exceeded", "how do I handle overflow"
- "content too large for avatar file", "where does overflow content go"

**Skill content:**

1. **Stop and classify** — identify which file type is over budget
2. **Apply the decision rule** — overflow if quality degradation would result; shrink only if content is genuinely redundant
3. **Create the overflow file** — follow the naming/location convention from the guide (Section 4)
4. **Register in `AVATAR-RAG-INDEX.yaml`** — two required steps: `files:` entry + `search_queries:` routing entries (minimum one entry per major section of the overflow file)
5. **Link from the source file** — the original file (guidance.md, example, etc.) must contain an explicit reference to the overflow file so a human reader can follow the chain
6. **Verify with linter** — `aa-constitution-lint .` must pass; overflow file must be inside avatar directory

**Laws implemented:** ENG-10.1 (Constitution Compliance), ENG-11.1 (Hangar SDD)

---

### S3 — Revert Linter Patch `f2e1552`

Revert commit `f2e1552` to restore the original `AvatarRagFilesExistRule` avatar-relative path
enforcement. After Amendment P (PR #14) moves `full-reference.md` into the avatar directory, the
reverted rule will pass correctly.

**Sequencing constraint:** S3 must not merge until Amendment P (PR #14) is merged to `main`.

---

## Background: How the C++ Pattern Was Established (Amendment O / P)

**Amendment O** (`9d6c8af`, April 11 2026) split `guidance.md` (5,693 lines, ~66,500 tokens,
147× over budget) into a 348-token index at `guidance.md` and extended content at
`docs/guides/avatars/cpp/full-reference.md` — incorrect placement.

**Linter patch `f2e1552`** (April 11 17:35 CST) silenced the resulting linter error by weakening
the governance rule instead of correcting the file location.

**Amendment P** (PR #14, April 12 2026) corrects the placement: moves `full-reference.md` to
`avatars/technology/cpp/full-reference.md`, updates `AVATAR-RAG-INDEX.yaml` to use a relative
path, and fixes `guidance.md` link and `conftest.py` fixture.

**This proposal** generalizes the lesson: documents the pattern for all four file types, produces
a skill so AI agents apply it proactively, and reverts the weakened linter rule.

---

## Deliverables

| # | Deliverable | Path | Notes |
|---|-------------|------|-------|
| D1 | Avatar reference-doc architecture guide | `docs/guides/constitution/avatar-reference-doc-architecture.md` | New file |
| D2 | Avatar token overflow agent skill | `agent-skills/skills-by-domain/platform-engineering/skill-avatar-token-overflow.md` | New file |
| D3 | Skill registered in platform-engineering index | `agent-skills/skills-by-domain/platform-engineering/index.yaml` | Add entry |
| D4 | Linter patch reverted | `tools/constitution-lint/src/aa_constitution_lint/domain/rules/index_integrity.py` | Revert `f2e1552` |
| D5 | Linter unit test confirming avatar-relative enforcement | `tools/constitution-lint/tests/` | New or updated test |

---

## Acceptance Criteria

| Criterion | Measure |
|-----------|---------|
| Guide exists at correct path | `docs/guides/constitution/avatar-reference-doc-architecture.md` present |
| Guide covers all 4 file types with overflow triggers, naming, location, and RAG registration | Section presence tests |
| Guide documents the two-step RAG registration requirement | Section presence test |
| Guide documents the RAG hybrid architecture (embedding + routing pointer) | Section presence test |
| Skill exists at correct path | `skill-avatar-token-overflow.md` present |
| Skill registered in `index.yaml` | Entry present with triggers and laws |
| Linter patch reverted | `f2e1552` reverted in `main` history |
| `AvatarRagFilesExistRule` resolves paths relative to avatar directory only | Linter unit test PASS |
| Linter PASS on `main` post Amendment-P merge | `aa-constitution-lint .` output |

---

## Laws Cited

| Law | Relevance |
|-----|-----------|
| [ENG-10.1](laws/engineering/eng-10-constitution.md) | Constitution Compliance — linter enforces avatar file placement; skill produces compliant artifacts |
| [ENG-11.1](laws/engineering/spec-driven-development.md) | Hangar SDD — governance patterns require spec proposals |
| [ENG-11.2](laws/engineering/spec-driven-development.md) | Proposal Completeness — this proposal satisfies required sections |
| [ENG-1.2](laws/engineering/eng-1-principles.md) | Human Oversight — AI agents must not silently degrade guidance quality |

---

## Related Proposals

### PR #26: `cpp-external-references` — Orthogonal, Not Incorporated

PR #26 introduces a three-layer *external references* architecture for the C++ avatar: where the
AI goes for **authoritative sources outside the constitution** (cppreference, GTest docs, FAA eCFR,
MSVC docs, Compiler Explorer) when it reaches the edge of what the avatar documents.

| | This proposal (`avatar-full-reference-pattern`) | PR #26 (`cpp-external-references`) |
|--|--|--|
| **Problem** | Where does *overflow content* go when a file exceeds its token budget? | Where does the AI go for *external authoritative sources* beyond the avatar? |
| **Solution** | Overflow files inside avatar dir + RAG `search_queries:` routing | `further_reading` blocks in manifest + `external_references` in RAG index + inline callouts |
| **Scope** | All avatars, all 4 file types; constitutional governance + agent skill | C++ avatar; Layer 3 adds callouts inside `full-reference.md` |

**These are orthogonal.** Neither supersedes the other. They do not need to be merged.

The constitutional guide (D1) produced by this proposal should include a brief note distinguishing
the two patterns, so future avatar authors do not confuse *token budget overflow* (internal content
placement) with *external reference navigation* (outside sources). The agent skill (D2) should
similarly note that external references belong in `further_reading` / `external_references` blocks,
not in overflow files.

---

## References

- [hangar-ai-specs/changes/c-plus-plus-avatar-enrichment/PROPOSAL.md](../c-plus-plus-avatar-enrichment/PROPOSAL.md) — Amendment O and Amendment P
- [hangar-ai-specs/evidence/avatar-scan-cpp.md](../../evidence/avatar-scan-cpp.md) — V7 violation scan evidence
- [avatars/AVATAR-RAG-INDEX.yaml](../../../avatars/AVATAR-RAG-INDEX.yaml) — RAG index (token budgets at lines 17–20; C++ block at ~line 990)
- [docs/guides/avatar-model-schema.md](../../../docs/guides/avatar-model-schema.md) — existing 3-layer architecture doc (to be superseded by D1)
- [agent-skills/skills-by-domain/platform-engineering/skill-avatar-workflow.md](../../../agent-skills/skills-by-domain/platform-engineering/skill-avatar-workflow.md) — related avatar construction skill
- [tools/constitution-lint/src/aa_constitution_lint/domain/rules/index_integrity.py](../../../tools/constitution-lint/src/aa_constitution_lint/domain/rules/index_integrity.py) — `AvatarRagFilesExistRule`
