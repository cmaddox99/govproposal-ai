# Proposal: Strengthen Constitution Linter and RAG

**Proposal ID:** strengthen-constitution-linter-and-rag
**Submitted:** 2026-04-07
**Last Updated:** 2026-04-07
**Status:** PROPOSED — awaiting implementation go-ahead
**Laws governing this work:** `ENG-10.1`, `ENG-11.1`, `ENG-11.2`, `BUS-7.1`

---

## Problem

Four gaps prevent the `hangar-ai-constitution` from governing itself with the same rigor it demands of adopting codebases:

**1. The linter validates downstream codebases, not the constitution itself.**
`aa-constitution-lint` v0.1.0 contains 5 rules that check for `AGENTS.md`, test pyramid directories, `hangar-ai-specs/`, and test file pairing. These are codebase adoption checks — fully owned by the adoption workflows (`greenfield-development`, `legacy-rescue-*`) and SonarQube gates. The linter has no rules validating that the constitution's own content is complete, consistent, or internally coherent. This is a governance inversion: the constitution has no linter that lints *it*.

**2. The constitution's content has structural gaps that would block RAG quality.**
14 product avatars and 29 technology avatars have inconsistent completeness:
- 5 product avatars missing `guidance.md`
- 4 product avatars missing `examples/` directory
- 8 product avatars with zero examples for non-negotiable PRD laws (PRD-1.2, PRD-1.5, PRD-2.5, PRD-5.1, PRD-6.2)
- 17 technology avatars missing examples for non-negotiable ENG security laws (ENG-6.1, ENG-6.4, ENG-6.7)
- `ADOPTION.md` is a deprecated construct still present in 11 product avatars; `guidance.md` is the correct pattern

**3. The index files that power token-optimized RAG are incomplete and unvalidated.**
`AVATAR-RAG-INDEX.yaml` covers only ~10/14 product avatars and 2/29 technology avatars. `avatars/index.yaml` is missing entries. Skill domain `index.yaml` files list files that are never verified to exist on disk, and files on disk are never verified to be listed in indexes. There is no rule that catches an orphaned file or a broken index reference — meaning RAG retrieval silently degrades as the constitution evolves.

**4. There is no quality gate on the constitution's GitHub repository.**
No `.github/workflows/` directory exists. The only protection is a local pre-commit hook running the linter that checks downstream codebases, not the constitution itself. There is no automated gate on PRs or pushes to `main`.

**5. There is no RAG evaluation harness.**
The constitution is used as the primary knowledge base for AI agents across American Airlines. There is no mechanism to measure whether agents can actually retrieve the right laws, skills, and avatars from it. Score thresholds cannot be enforced, and regressions in retrieval quality are invisible.

---

## Solution

Three changes to the `hangar-ai-constitution` repository, executed in six phases:

**1. Refocus and enhance the linter** (`aa-constitution-lint` v0.1.0 → v0.2.0):
- Remove the 4 codebase adoption rules (owned by adoption workflows) — `structure.agents_file`, `structure.test_pyramid`, `structure.hangar_ai_specs_dir`, `testing.atomic_tdd`
- Keep `references.law_references` — validates internal law citation consistency across constitution files
- Add 9 constitution self-governance rules (avatar completeness, non-negotiable law examples, deprecated construct detection, manifest schema, law frontmatter, skill index consistency)
- Add 7 index integrity rules (validate all index files are complete and in sync with disk)

**2. Add a GitHub Actions CI gate** enforcing the linter on all PRs and pushes to `main`. Add a second workflow for the RAG evaluation harness.

**3. Build a RAG test harness** (`tools/rag-eval/`) with a scored evaluation model (5 dimensions, configurable thresholds) executable standalone and as part of the linter gate.

**4. Strengthen the constitution content** so it passes its own new gates:
- Fill all product and technology avatar gaps identified in Problem 2
- Remove `ADOPTION.md` from product/tech avatars (deprecated; content migrated to `guidance.md`)
- Complete all index files so every file is indexed and every index entry resolves to a real file

---

## Deliverables

### Phase 1 — GitHub Actions CI Gate
- `.github/workflows/constitution-lint.yml` — blocks PRs and push to `main` on FAIL violations; posts violation summary as PR comment
- `.github/workflows/rag-eval.yml` — blocks on score threshold breach; posts score card as PR comment; uploads score JSON as workflow artifact (BUS-7.1 audit trail); supports `workflow_dispatch` for on-demand runs

### Phase 2 — Linter Enhancement (v0.2.0)
- `tools/constitution-lint/src/aa_constitution_lint/domain/rules/constitution.py` — 9 new constitution self-governance rules
- `tools/constitution-lint/src/aa_constitution_lint/domain/rules/index_integrity.py` — 7 new index validation rules
- `tools/constitution-lint/src/aa_constitution_lint/application/linter.py` — register new rules; deregister 4 adoption rules
- Version bump to `0.2.0` in `pyproject.toml`

New rules (linter goes from 5 → 17 total; all 17 scoped to constitution self-governance):

| Rule ID | Sev | Enforces |
|---------|-----|---------|
| `constitution.product_avatar_completeness` | FAIL | Every product avatar: `manifest.yaml` + `guidance.md` + `examples/` |
| `constitution.tech_avatar_completeness` | FAIL | Every tech avatar: `manifest.yaml` + `guidance.md` + `examples/` |
| `constitution.product_avatar_nonneg_examples` | FAIL | Product avatar `examples/` covers each non-neg PRD law |
| `constitution.tech_avatar_nonneg_examples` | FAIL | Tech avatar `examples/` covers each non-neg ENG law (ENG-4.1, ENG-6.1, ENG-6.4, ENG-6.7) |
| `constitution.no_deprecated_adoption` | WARN→FAIL | No `ADOPTION.md` in product/tech avatars (industry exempt); phases to FAIL after content migration |
| `constitution.avatar_manifest_schema` | FAIL | `manifest.yaml` has `avatar.id`, `avatar.type`, `avatar.name`, `activates`, `specializes_laws` |
| `constitution.avatar_manifest_nonneg_citation` | WARN | `specializes_laws` cites ≥1 non-negotiable law |
| `constitution.law_frontmatter_completeness` | FAIL | All law `.md` files have valid YAML frontmatter with `domain`, `article`, `title`, ≥1 law entry |
| `constitution.skill_index_consistency` | FAIL | Bidirectional: skill files ↔ domain `index.yaml` (no orphans, no broken refs) |
| `index.laws_registry_files_exist` | FAIL | Files listed in `laws/index.yaml` exist on disk |
| `index.laws_registry_complete` | FAIL | All `.md` files in `laws/{domain}/` listed in `laws/index.yaml` |
| `index.avatar_rag_complete` | FAIL | Every avatar dir has entry in `AVATAR-RAG-INDEX.yaml` |
| `index.avatar_rag_files_exist` | FAIL | All `files:` paths in `AVATAR-RAG-INDEX.yaml` exist on disk |
| `index.avatar_rag_laws_valid` | FAIL | All law IDs in `AVATAR-RAG-INDEX.yaml` `specializes_laws` are registered |
| `index.avatar_index_complete` | FAIL | All avatar dirs listed in `avatars/index.yaml` + `product-type/index.yaml` |
| `index.nonneg_laws_consistent` | FAIL | Non-neg IDs in `laws/index.yaml` match `non_negotiable: true` in law file frontmatter |

### Phase 3 — Constitution Content Strengthening (Product Avatars)
- Add `guidance.md` to 5 product avatars: `airport-operations`, `crew-training-scheduling`, `customer-service`, `internal-productivity`, `passenger-booking`
- Add `examples/` with full non-neg PRD law coverage (PRD-1.2, PRD-1.5, PRD-2.5, PRD-5.1, PRD-6.2) to 4 avatars with no examples dir
- Add non-neg PRD law examples to 4 avatars with existing `examples/` but no non-neg coverage
- Remove `ADOPTION.md` from all 11 product avatars that have it (deprecated; content migrated to `guidance.md`)

### Phase 4 — Constitution Content Strengthening (Tech Avatars + Indexes)
- Add `ENG-6-security.md` (covering ENG-6.1, ENG-6.4, ENG-6.7) to `examples/` in 17 tech avatars missing security law coverage
- Add `examples/` dir to `opentelemetry-python`
- Complete `AVATAR-RAG-INDEX.yaml` with 33 missing entries (6 product + 27 tech avatars)
- Complete `avatars/index.yaml` with all 29 tech avatar entries
- Extend `laws/index.yaml` with individual law ID enumeration per domain
- Verify all 5 skill domain `index.yaml` files match disk

### Phase 5 — RAG Test Harness
- `tools/rag-eval/evaluate.py` — Click CLI: `evaluate.py [--format console|json|github-actions] [--threshold-check]`
- `tools/rag-eval/scorer.py` — 5-dimension scoring model
- `tools/rag-eval/retriever.py` — keyword + law ID content retrieval simulation
- `tools/rag-eval/config.yaml` — configurable score thresholds
- `tools/rag-eval/test-cases/*.yaml` — 85+ test cases across 5 domains
- `tools/rag-eval/README.md` — scoring model documentation, usage, threshold configuration

### Phase 6 — Linter–RAG Integration
- `cli.py` updated with `--with-rag-eval` flag — runs linter then RAG eval; threshold breaches reported as CRITICAL
- `constitution.no_deprecated_adoption` promoted from WARNING to FAIL (after Phase 3 content migration complete)

---

## Success Criteria

| # | Criterion | Measurable Target |
|---|-----------|------------------|
| 1 | Constitution lints itself clean | `aa-constitution-lint . --constitution .` returns 0 FAILs, 0 WARNINGs |
| 2 | RAG overall score | ≥ 0.85 weighted across all 5 dimensions |
| 3 | Law retrieval | ≥ 0.85 — test questions retrieve expected law(s) in top-3 |
| 4 | Skill routing | ≥ 0.80 — questions route to correct skill via trigger matching |
| 5 | Avatar selection | ≥ 0.80 — avatar queries resolve to correct avatar |
| 6 | Index integrity | ≥ 0.95 — all index entries resolve; no orphans |
| 7 | Cross-reference consistency | ≥ 0.95 — law citations in skills/avatars/workflows valid |
| 8 | PR gate active | Every PR to `main` blocked by `constitution-lint` + `rag-eval` workflows |
| 9 | Product avatar completeness | All 14 product avatars: `guidance.md` + `examples/` + non-neg PRD coverage |
| 10 | Tech avatar completeness | All 29 tech avatars: `examples/` + ENG-4.1 + ENG-6.1/6.4/6.7 coverage |
| 11 | Index coverage | 100% of avatar dirs in `AVATAR-RAG-INDEX.yaml`; 0 orphaned files |
| 12 | No deprecated constructs | 0 `ADOPTION.md` files in product/tech avatars |

---

## References

- `ENG-10.1` — Constitution Metrics Collection Law: compliance monitoring and amendment process
- `ENG-11.1` — Hangar SDD Law (NON-NEGOTIABLE): this proposal follows `PROPOSE → IMPLEMENT → ARCHIVE`
- `ENG-11.2` — Proposal Completeness Law: this document satisfies all required sections
- `BUS-7.1` — Audit Trail Law (NON-NEGOTIABLE): CI artifacts, score reports, and PR comments provide traceability
- `ENG-6.1` — Security by Design: CI gate prevents insecure law citations from merging
- `PRD-5.1` — MVP Law: phases are sequenced so each delivers independent value; Phase 1 alone improves governance
