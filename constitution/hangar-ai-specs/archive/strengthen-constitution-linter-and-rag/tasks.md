# Tasks: strengthen-constitution-linter-and-rag

**Branch:** `feature/strengthen-constitution-linter-and-rag`
**Laws governing this work:** `ENG-10.1`, `ENG-11.1` (NON-NEGOTIABLE), `ENG-11.2`, `BUS-7.1`

## Progress Summary

- Completed: 0 / 46
- In Progress: 0
- Blocked: 0

---

## Phase 1 — GitHub Actions CI Gate

- [ ] 1.1 Create `.github/workflows/` directory
- [ ] 1.2 Create `.github/workflows/constitution-lint.yml` — triggers: `pull_request`→`main`, `push`→`main`; installs `aa-constitution-lint` from source; runs `aa-constitution-lint . --constitution .`; fails on FAIL severity; posts violation summary as PR comment via `actions/github-script`; pip cache keyed on `pyproject.toml` hash
- [ ] 1.3 Create `.github/workflows/rag-eval.yml` — triggers: `pull_request`→`main`, `push`→`main`, `workflow_dispatch`; runs `python tools/rag-eval/evaluate.py --format github-actions --threshold-check`; fails on threshold breach; posts score card as PR comment; uploads `tools/rag-eval/reports/latest.json` as workflow artifact (BUS-7.1)

## Phase 2 — Linter Enhancement (v0.2.0)

### 2a — Remove codebase adoption rules (wrong scope)
- [ ] 2.1 Remove `AgentsFileRule` from `domain/rules/structure.py` and deregister from `linter.py`
- [ ] 2.2 Remove `TestPyramidRule` from `domain/rules/structure.py` and deregister from `linter.py`
- [ ] 2.3 Remove `HangarAiSpecsDirRule` from `domain/rules/structure.py` and deregister from `linter.py`
- [ ] 2.4 Remove `AtomicTddRule` from `domain/rules/testing.py` and deregister from `linter.py`

### 2b — Constitution self-governance rules (`domain/rules/constitution.py`)
- [ ] 2.5 Implement `constitution.product_avatar_completeness` (FAIL) — every product avatar dir must contain `manifest.yaml`, `guidance.md`, `examples/`
- [ ] 2.6 Implement `constitution.tech_avatar_completeness` (FAIL) — every tech avatar dir must contain `manifest.yaml`, `guidance.md`, `examples/`
- [ ] 2.7 Implement `constitution.product_avatar_nonneg_examples` (FAIL) — product avatar `examples/` must contain at least one file referencing each non-neg PRD law: PRD-1.2, PRD-1.5, PRD-2.5, PRD-5.1, PRD-6.2
- [ ] 2.8 Implement `constitution.tech_avatar_nonneg_examples` (FAIL) — tech avatar `examples/` must contain at least one file per non-neg ENG law: ENG-4.1, ENG-6.1, ENG-6.4, ENG-6.7
- [ ] 2.9 Implement `constitution.no_deprecated_adoption` (WARNING initially) — product/tech avatar dirs must not contain `ADOPTION.md`; industry avatars (`avatars/industry/`) exempt
- [ ] 2.10 Implement `constitution.avatar_manifest_schema` (FAIL) — `manifest.yaml` must have required top-level keys: `avatar.id`, `avatar.type`, `avatar.name`, `activates`, `specializes_laws`
- [ ] 2.11 Implement `constitution.avatar_manifest_nonneg_citation` (WARNING) — `specializes_laws` in `manifest.yaml` must cite ≥1 non-negotiable law ID
- [ ] 2.12 Implement `constitution.law_frontmatter_completeness` (FAIL) — all law `.md` files in `laws/` must have valid YAML frontmatter with `domain`, `article`, `title`, and ≥1 entry under `laws:` with `id`, `title`, `non_negotiable`
- [ ] 2.13 Implement `constitution.skill_index_consistency` (FAIL) — bidirectional check: every `file:` in skill domain `index.yaml` must exist on disk; every skill `.md` file on disk must be listed in its domain's `index.yaml`

### 2c — Index integrity rules (`domain/rules/index_integrity.py`)
- [ ] 2.14 Implement `index.laws_registry_files_exist` (FAIL) — all filenames listed per domain in `laws/index.yaml` must exist as files in the corresponding `laws/{domain}/` directory
- [ ] 2.15 Implement `index.laws_registry_complete` (FAIL) — all `.md` files present in `laws/{domain}/` must be listed in `laws/index.yaml`; no orphaned law files
- [ ] 2.16 Implement `index.avatar_rag_complete` (FAIL) — every directory under `avatars/product-type/` and `avatars/technology/` must have a corresponding top-level entry in `AVATAR-RAG-INDEX.yaml`
- [ ] 2.17 Implement `index.avatar_rag_files_exist` (FAIL) — every file path referenced under `files:` blocks in `AVATAR-RAG-INDEX.yaml` must exist on disk relative to `avatars/`
- [ ] 2.18 Implement `index.avatar_rag_laws_valid` (FAIL) — all law IDs cited under `specializes_laws:` in `AVATAR-RAG-INDEX.yaml` must be registered law IDs
- [ ] 2.19 Implement `index.avatar_index_complete` (FAIL) — all dirs under `avatars/technology/` listed in `avatars/index.yaml`; all dirs under `avatars/product-type/` listed in `avatars/product-type/index.yaml`
- [ ] 2.20 Implement `index.nonneg_laws_consistent` (FAIL) — law IDs listed under `non_negotiable:` in `laws/index.yaml` must exactly match law IDs flagged `non_negotiable: true` in their respective law `.md` frontmatter

### 2d — Register + version bump
- [ ] 2.21 Register all 16 new rules in `application/linter.py`; deregister the 4 removed adoption rules
- [ ] 2.22 Bump version to `0.2.0` in `tools/constitution-lint/pyproject.toml`; update `tools/constitution-lint/README.md` with new rule table and removal notice

## Phase 3 — Constitution Content: Product Avatars

### 3a — Add missing `guidance.md` files
- [ ] 3.1 Create `avatars/product-type/airport-operations/guidance.md` — gate management, crew coordination, IROP response; cites BUS-2.1, BUS-2.2, PRD-1.2, PRD-5.1
- [ ] 3.2 Create `avatars/product-type/crew-training-scheduling/guidance.md` — FAR Part 117 compliance, crew licensing, scheduling constraints; cites BUS-2.1, ENG-6.7
- [ ] 3.3 Create `avatars/product-type/customer-service/guidance.md` — DOT refund timelines, rebooking policies, complaint handling; cites BUS-2.3, PRD-1.2, PRD-6.2
- [ ] 3.4 Create `avatars/product-type/internal-productivity/guidance.md` — internal tooling patterns, workflow automation, employee experience; cites PRD-1.2, ENG-6.4
- [ ] 3.5 Create `avatars/product-type/passenger-booking/guidance.md` — DOT fare transparency, PCI compliance, booking flows; cites BUS-2.3, BUS-4.3, PRD-1.2

### 3b — Add `examples/` with non-neg PRD law coverage to avatars with no examples dir
- [ ] 3.6 Create `avatars/product-type/airport-operations/examples/` with PRD-1.2, PRD-1.5, PRD-2.5, PRD-5.1, PRD-6.2 example files
- [ ] 3.7 Create `avatars/product-type/customer-service/examples/` with PRD-1.2, PRD-1.5, PRD-2.5, PRD-5.1, PRD-6.2 example files
- [ ] 3.8 Create `avatars/product-type/internal-productivity/examples/` with PRD-1.2, PRD-1.5, PRD-2.5, PRD-5.1, PRD-6.2 example files
- [ ] 3.9 Create `avatars/product-type/passenger-booking/examples/` with PRD-1.2, PRD-1.5, PRD-2.5, PRD-5.1, PRD-6.2 example files

### 3c — Add non-neg PRD examples to avatars with existing `examples/` but zero non-neg coverage
- [ ] 3.10 Add PRD-1.2 + PRD-5.1 examples to `avatars/product-type/customer-relations-ops/examples/`
- [ ] 3.11 Add PRD-1.2 + PRD-5.1 examples to `avatars/product-type/ground-ops-staffing-analytics/examples/`
- [ ] 3.12 Add PRD-1.2 + PRD-5.1 examples to `avatars/product-type/network-planning-optimization/examples/`
- [ ] 3.13 Add PRD-1.2 + PRD-5.1 examples to `avatars/product-type/travel-docs-compliance/examples/`

### 3d — Remove deprecated `ADOPTION.md` from product avatars
- [ ] 3.14 Migrate unique content from `ADOPTION.md` into `guidance.md` for each avatar that has ADOPTION.md; delete `ADOPTION.md`
  - airport-operations, cargo-freight, check-in-travel, crew-training-scheduling, customer-relations-ops, customer-service, ground-ops-staffing-analytics, internal-productivity, loyalty-aadvantage, network-planning-optimization, passenger-booking

## Phase 4 — Constitution Content: Tech Avatars + Index Files

### 4a — Add ENG-6.x security examples to 17 tech avatars
- [ ] 4.1 Add `examples/ENG-6-security.md` to `angular` — covering ENG-6.1, ENG-6.4, ENG-6.7 in Angular context
- [ ] 4.2 Add `examples/ENG-6-security.md` to `azure-openai` — covering ENG-6.1, ENG-6.4, ENG-6.7 in Azure OpenAI context
- [ ] 4.3 Add `examples/ENG-6-security.md` to `dotnet-core` — covering ENG-6.1, ENG-6.4, ENG-6.7 in .NET context
- [ ] 4.4 Add `examples/ENG-6-security.md` to `java-spring` — covering ENG-6.1, ENG-6.4, ENG-6.7 in Spring Boot context
- [ ] 4.5 Add `examples/ENG-6-security.md` to `legacy-ml-interop`
- [ ] 4.6 Add `examples/ENG-6-security.md` to `ml-analytics`
- [ ] 4.7 Add `examples/ENG-6-security.md` to `mlflow-kubeflow`
- [ ] 4.8 Add `examples/ENG-6-security.md` to `mobile-native`
- [ ] 4.9 Add `examples/ENG-6-security.md` to `mobile-react-native`
- [ ] 4.10 Add `examples/ENG-6-security.md` to `postgresql-sqlalchemy`
- [ ] 4.11 Add `examples/ENG-6-security.md` to `python-streamlit`
- [ ] 4.12 Add `examples/ENG-6-security.md` to `pytorch`
- [ ] 4.13 Add `examples/ENG-6-security.md` to `react-typescript`
- [ ] 4.14 Add `examples/ENG-6-security.md` to `sagemaker`
- [ ] 4.15 Add `examples/ENG-6-security.md` to `tensorflow`
- [ ] 4.16 Add `examples/ENG-6-security.md` to `vector-databases`
- [ ] 4.17 Create `avatars/technology/opentelemetry-python/examples/` and add `ENG-4.1-atomic-tdd.md` + `ENG-6-security.md`

### 4b — Complete index files
- [ ] 4.18 Complete `avatars/AVATAR-RAG-INDEX.yaml` — add entries for 6 missing product avatars: airport-operations, crew-training-scheduling, customer-service, internal-productivity, passenger-booking, customer-relations-ops
- [ ] 4.19 Complete `avatars/AVATAR-RAG-INDEX.yaml` — add entries for all 27 missing technology avatars
- [ ] 4.20 Complete `avatars/index.yaml` — add all missing technology avatar entries with `stack`, `activates`, `specializes_laws` blocks
- [ ] 4.21 Extend `laws/index.yaml` — add `law_ids:` enumeration per domain enabling `index.nonneg_laws_consistent` cross-validation
- [ ] 4.22 Audit and fix all 5 skill domain `index.yaml` files — verify each `file:` reference exists on disk; add any missing skill entries

## Phase 5 — RAG Test Harness

- [ ] 5.1 Create `tools/rag-eval/` directory structure with `README.md`
- [ ] 5.2 Implement `tools/rag-eval/retriever.py` — keyword + law ID matching against constitution files; returns ranked results
- [ ] 5.3 Implement `tools/rag-eval/scorer.py` — 5-dimension scoring: law retrieval (35%), skill routing (25%), avatar selection (20%), index integrity (10%), cross-reference consistency (10%)
- [ ] 5.4 Write `tools/rag-eval/test-cases/engineering.yaml` — ~20 test cases for ENG law retrieval
- [ ] 5.5 Write `tools/rag-eval/test-cases/product.yaml` — ~20 test cases for PRD law retrieval
- [ ] 5.6 Write `tools/rag-eval/test-cases/business.yaml` — ~15 test cases for BUS law retrieval
- [ ] 5.7 Write `tools/rag-eval/test-cases/skills.yaml` — ~15 test cases for skill routing via trigger phrases
- [ ] 5.8 Write `tools/rag-eval/test-cases/avatars.yaml` — ~15 test cases for avatar selection
- [ ] 5.9 Create `tools/rag-eval/config.yaml` — thresholds: law_retrieval: 0.85, skill_routing: 0.80, avatar_selection: 0.80, index_integrity: 0.95, cross_reference_consistency: 0.95, overall: 0.85
- [ ] 5.10 Implement `tools/rag-eval/evaluate.py` — Click CLI with `--format [console|json|github-actions]` and `--threshold-check`; writes report to `tools/rag-eval/reports/latest.json`
- [ ] 5.11 Add `tools/rag-eval/reports/` to `.gitignore`

## Phase 6 — Linter–RAG Integration + Final Gate

- [ ] 6.1 Add `--with-rag-eval` flag to `tools/constitution-lint/src/aa_constitution_lint/cli.py` — runs linter then invokes `evaluate.py`; threshold breaches surfaced as CRITICAL in linter output
- [ ] 6.2 Promote `constitution.no_deprecated_adoption` from WARNING to FAIL in `constitution.py` (after Phase 3 content complete — all `ADOPTION.md` files removed)
- [ ] 6.3 Run `aa-constitution-lint . --constitution . --with-rag-eval` against the constitution; verify 0 FAILs, 0 WARNINGs, overall RAG score ≥ 0.85
- [ ] 6.4 Update `PROGRESS.md` to COMPLETE and prepare for archive
