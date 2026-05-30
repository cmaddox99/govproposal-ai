# Proposal: C++ Extended Reference Documentation

**Status:** ✅ COMPLETE
**Amendment P Correction (April 12, 2026):** This proposal was marked COMPLETE with
`full-reference.md` placed at `docs/guides/avatars/cpp/full-reference.md`. Amendment P
(PR #14) corrects this location to `avatars/technology/cpp/full-reference.md` per the
constitutional rule that all avatar artifacts must reside inside the avatar directory
(`AvatarRagFilesExistRule`, ENG-10.1). All path references to `docs/guides/avatars/cpp/`
in this proposal should be read as `avatars/technology/cpp/`. The content, purpose, and
RAG registration strategy documented here remain valid; only the destination path changes.

**Spec ID:** `cpp-extended-reference-docs`
**Triggered by:** Amendment O (V7) — `guidance.md` exceeded the 450-token RAG token budget; extended content moved out of the technology avatar's guidance file per constitutional scope constraints
**Scope:** `docs/guides/avatars/cpp/` — new extended reference file; no changes to `avatars/technology/cpp/`
**Parent PR:** #14 (c-plus-plus-avatar-enrichment)
**Companion to:** `cpp-tier-compliance-rating`, `product-avatar-bus-enrichment`

---

## Problem

The C++ avatar's `guidance.md` was 5,693 lines (~66,500 tokens) — 147× over the 200–450 token RAG budget for guidance files (defined in `avatars/AVATAR-RAG-INDEX.yaml`).

The constitution requires `guidance.md` to be a concise index (purpose statement + non-negotiable law table + pointer to extended docs). The full engineering guidance content — C++ version policy, testing framework deep-dives, package management, domain modeling, concurrency, CI toolchain policy, coroutine governance, logging, brownfield migration playbooks, legacy code navigation, per-tier configurations, and 25+ other topics — cannot fit in the guidance index.

This content is **not out-of-scope** — it is constitutionally valid C++ engineering guidance that should remain accessible to AI agents. It only needs to move to the correct artifact layer: the `docs/` reference layer, which has no token limit and is loaded on-demand via RAG retrieval.

### Impact Without This Proposal

- AI agents cannot access the full C++ engineering detail (no guidance.md means no deep retrieval)
- 25+ engineering topics become unreachable
- The `AVATAR-RAG-INDEX.yaml` queries that reference `guidance.md` sections (e.g., "C++ migrate standard version? → guidance.md brownfield migration") become dead links

---

## Solution

Create `docs/guides/avatars/cpp/full-reference.md` as the canonical C++ extended reference. This file:
1. Contains all C++ engineering content previously in `guidance.md`
2. Has no token limit (it is a docs layer artifact, not an avatar artifact)
3. Is loaded on-demand by RAG — not loaded automatically with every C++ query
4. Is linked from the slim `guidance.md` index

Update `AVATAR-RAG-INDEX.yaml` to reference `docs/guides/avatars/cpp/full-reference.md` for queries previously pointing to `guidance.md` sections.

---

## Deliverables

| Artifact | Description | Status |
|----------|-------------|--------|
| `docs/guides/avatars/cpp/full-reference.md` | Full C++ engineering reference (all content previously in guidance.md) | Delivered (Amendment O Step 16.6) |
| `avatars/AVATAR-RAG-INDEX.yaml` — cpp section | Updated `guidance` query targets to reference `full-reference.md` | Pending |
| Tests: section coverage | Verify all 25+ engineering sections present in `full-reference.md` | Delivered (guidance section tests redirected to full-reference.md) |

---

## Success Criteria

| Criterion | Test |
|-----------|------|
| `guidance.md` ≤450 tokens | `test_guidance_md_within_token_budget()` — word_count × 1.3 ≤450 |
| `full-reference.md` contains all original sections | `test_guidance_*` suite reads from full-reference.md and passes |
| All 25+ original guidance sections present | Section-heading tests pass |
| `AVATAR-RAG-INDEX.yaml` cpp queries updated | Manual review — no dead section references |
| BUS-* law citations removed from full-reference.md | `test_law_reference_coverage.py` — no BUS-* in section citation requirements |

---

## Laws Cited

| Law | Relevance |
|-----|-----------|
| [ENG-11.1](laws/engineering/spec-driven-development.md) | Spec-Driven Development — artifacts belong at the correct constitutional layer |
| [ENG-10.3](laws/engineering/quality.md) | Compliance Reporting — avatar artifacts must stay within token budgets |

---

## Notes

- `full-reference.md` replaces `guidance.md` as the load target for all section-level C++ queries
- The slim `guidance.md` remains the entry point — AI agents always load it first (200–450 tokens)
- This proposal is non-blocking for PR #14 — the `full-reference.md` file was delivered as part of Amendment O Step 16.6
- The `AVATAR-RAG-INDEX.yaml` update is the only remaining work item
