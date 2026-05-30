# Proposal: Avatar Validation Rules for constitution-lint

**Proposal ID:** avatar-constitution-lint-extension  
**Submitted:** April 5, 2026  
**Status:** DRAFT — Proposal complete; awaiting prioritization  
**Origin:** Identified during C++ avatar enrichment (see [c-plus-plus-avatar-enrichment](../c-plus-plus-avatar-enrichment/PROPOSAL.md), Amendment A)

## Laws Cited (ENG-11.2 Compliance)

Per [ENG-11.2: Proposal Completeness](laws/engineering/eng-11-hangar-sdd.md), every proposal must cite at least one law.

| Law ID | Title | Relevance |
|--------|-------|-----------|
| [ENG-10.1](laws/engineering/eng-10-constitution.md) | Constitution Compliance | Meta-governance: avatar validation rules enforce compliance |
| [ENG-4.1](laws/engineering/eng-4-testing.md) | Atomic TDD Law (Non-Negotiable) | Implementation must follow TDD |
| [ENG-4.2](laws/engineering/eng-4-testing.md) | Test Pyramid Law | New rules need unit tests |
| [ENG-11.1](laws/engineering/eng-11-hangar-sdd.md) | Hangar SDD Law (Non-Negotiable) | Governs this proposal's lifecycle |

---

## Problem Statement

Per [PRD-1.2](laws/product/prd-1-discovery.md) (Problem-First Law):

The `constitution-lint` tool (`tools/constitution-lint/`) currently validates project-level governance (AGENTS.md exists, test pyramid structure, hangar-ai-specs/ directory, law references). However, it has **no rules for validating technology avatar artifacts** themselves.

This means:
1. **Invalid law references in avatar manifests go undetected** until a human reviewer catches them
2. **Missing example files** for declared `specializes_laws` entries are not caught
3. **Token budget violations** in example files (>600 tokens) accumulate silently
4. **Structural parity gaps** between new and reference avatars are not flagged
5. **Citation format violations** (bare law IDs instead of hyperlinks) in guidance files pass lint

During the C++ avatar enrichment, we discovered that all 14 unit tests were text-presence checks (e.g., `assert "unique_ptr" in content`). While these catch regressions, they don't verify governance behavior. We addressed this within the C++ proposal by creating reusable test helpers (`avatar_test_helpers.py`) and a compliance test suite (`test_constitution_compliance.py`). However, these helpers are scoped to the C++ avatar's test directory.

**The structural problem remains:** every future avatar enrichment will need to rebuild or copy these governance checks. The right long-term solution is to embed avatar validation in `constitution-lint` itself, so all avatars are validated automatically during CI and the VERIFY step of every TDD cycle.

---

## Proposed Solution

Extend `constitution-lint` with a new `AvatarValidationRule` (and potentially sub-rules) that validate technology avatar artifacts against constitution governance requirements.

### Architecture

The existing lint architecture provides a clean extension point:

```
tools/constitution-lint/src/aa_constitution_lint/domain/rules/
├── base.py          # Rule abstract base class — evaluate(project_path) → List[LawEvaluation]
├── structure.py     # AgentsFileRule, TestPyramidRule, HangarAiSpecsDirRule
├── references.py    # LawReferenceRule (validates ENG-*/PRD-*/BUS-* refs)
├── testing.py       # AtomicTddRule
└── avatars.py       # ← NEW: AvatarValidationRule
```

Each rule returns `LawEvaluation` results (pass/fail/warning/skip) with structured context, feeding into the existing `LintResult` summary.

### Proposed Rules

| Rule | Law | What it checks |
|------|-----|---------------|
| `AvatarManifestSchemaRule` | ENG-10.1 | Required sections exist (avatar, stack, activates, specializes_laws, conventions, commands) |
| `AvatarLawReferenceRule` | ENG-10.1 | All law IDs in `specializes_laws` are valid per `LawRegistry` |
| `AvatarExampleFileRule` | ENG-10.1 | Every `specializes_laws` entry with `example_file` has a matching file on disk |
| `AvatarTokenBudgetRule` | ENG-10.1 | Example files stay under 600-token budget (word count × 1.3) |
| `AvatarCitationFormatRule` | ENG-10.1 | Guidance.md uses `[LAW-ID](path)` hyperlink format, not bare IDs |
| `AvatarParityRule` | ENG-10.1 | New avatar has structural parity with reference avatars (configurable baseline) |
| `AvatarNonNegotiableCoverageRule` | ENG-10.1 | All 18 non-negotiable laws have example files (or explicit documented exemptions) |

### Key Design Decisions to Make

1. **Discovery mechanism:** Should the rule auto-discover avatars from `avatars/index.yaml`, or scan `avatars/technology/*/manifest.yaml` directly?
2. **Parity baseline:** Which avatar(s) define the reference schema? java-spring? python-fastapi? A configurable list?
3. **Severity levels:** Which checks are CRITICAL (fail the build) vs. WARNING (report but pass)?
4. **Brownfield tolerance:** Should there be a mechanism for avatars to declare exemptions (e.g., brownfield avatars that intentionally skip non-negotiable coverage)?

---

## Implementation Context

### Existing Infrastructure to Leverage

The following components already exist and should be reused:

**`LawRegistry` (`infrastructure/law_registry.py`):**
- Loads all valid law IDs from `laws/` directory (markdown frontmatter + YAML domain files)
- Provides `law_exists(law_id)` and `get_law(law_id)` methods
- Already used by `LawReferenceRule` — the avatar rules should use the same instance

**`Rule` base class (`domain/rules/base.py`):**
- Abstract `evaluate(project_path: Path) → List[LawEvaluation]` method
- All rules registered in the lint engine and executed during `aa-constitution-lint` runs
- Returns `LawEvaluation` objects with structured context (law_id, result, timestamp, context dict)

**`LintResult` model (`domain/models.py`):**
- Aggregates `LawEvaluation` + `Violation` + `Summary`
- Supports JSON output for CI/CD integration
- New avatar rules automatically participate in summary counts

**`avatar_test_helpers.py` (created during C++ proposal):**
- Contains reusable validation functions that can inform the lint rule implementation
- Functions: `validate_law_references()`, `check_example_file_exists()`, `check_token_budget()`, `check_parity_sections()`, `check_citation_format()`
- These are test-time helpers; the lint rules would be their production equivalent

### Reference Avatars for Parity Comparison

| Avatar | Path | Maturity |
|--------|------|----------|
| Java/Spring Boot | `avatars/technology/java-spring/` | Mature reference — full manifest, guidance, examples |
| Python/FastAPI | `avatars/technology/python-fastapi/` | Mature reference — full manifest, guidance, examples |
| C++ | `avatars/technology/cpp/` | New — created by c-plus-plus-avatar-enrichment proposal |

### Schema Expectations (derived from existing avatars)

A valid technology avatar `manifest.yaml` must contain:

```yaml
# Required top-level keys
avatar:          # id, type, name, version
stack:           # language, testing, tools
activates:       # skills (list), workflows (list)
specializes_laws: # list of {id, title, example_file}
conventions:     # naming, patterns, testing_layout
commands:        # build, test, lint, format (minimum)
```

A valid `guidance.md` must contain:
- Section headings matching the technology's governance topics
- Law citations in `[LAW-ID](path)` hyperlink format
- Code examples demonstrating governance patterns

---

## Deliverables

1. `tools/constitution-lint/src/aa_constitution_lint/domain/rules/avatars.py` — Avatar validation rules
2. `tools/constitution-lint/tests/test_avatar_rules.py` — Unit tests for avatar rules
3. Updated `tools/constitution-lint/src/aa_constitution_lint/application/lint_engine.py` — Register new rules
4. Updated `tools/constitution-lint/README.md` — Document new checks
5. Updated `AGENTS.md` — Reference new lint checks in VERIFY step guidance

---

## Success Criteria

| Criteria | Measurement |
|----------|-------------|
| All 7 proposed rules implemented and tested | Unit test coverage per rule |
| `aa-constitution-lint .` reports avatar compliance | Run against repo with C++, java-spring, python-fastapi avatars |
| No false positives on existing mature avatars | java-spring and python-fastapi pass all new rules |
| C++ avatar passes all new rules | Validates the C++ enrichment is governance-complete |
| Rules integrate with CI/CD JSON output | `--format json` includes avatar evaluations |

---

## Estimated Scope

- **New files:** 2–3 (rules module, tests, possibly a config/schema file)
- **Modified files:** 2–3 (lint engine registration, README, AGENTS.md)
- **Tasks:** ~15–20 (one per rule + integration + documentation)
- **Risk:** Low — extends existing architecture with no breaking changes

---

## Dependencies

| Dependency | Status | Impact |
|-----------|--------|--------|
| C++ avatar enrichment complete | 🟡 In progress | Provides the newest avatar to validate; not blocking — can develop rules against java-spring/python-fastapi first |
| `avatar_test_helpers.py` created | 🟡 In progress (task 2.7a) | Informs rule design; not blocking — rules are independent implementations |
| Existing lint infrastructure stable | ✅ Stable | `Rule`, `LawEvaluation`, `LawRegistry` APIs are established |

---

## Context from Origin Session (2026-04-05)

> **Why this proposal exists:** During C++ avatar enrichment, we evaluated the testing strategy and identified four levels of improvement. The first three (test helpers, upgraded tests, compliance suite) were incorporated into the C++ proposal as Amendment A. The fourth — extending `constitution-lint` with reusable avatar validation rules — was too large for an in-flight amendment and was separated into this standalone proposal.
>
> **Key insight:** Every avatar enrichment (C++, and future Rust, Go, etc.) will need the same governance validation. Building it once in `constitution-lint` eliminates redundant `avatar_test_helpers.py` modules in each avatar's test directory and ensures consistent enforcement.
>
> **What already exists to build on:**
> - The `Rule` → `LawEvaluation` pattern in constitution-lint is clean and extensible
> - `LawRegistry` already validates law IDs — avatar rules just need to call it for manifest entries
> - The `avatar_test_helpers.py` module (created in C++ proposal task 2.7a) contains prototype validation logic that maps directly to lint rules
> - Two mature reference avatars (java-spring, python-fastapi) provide the parity baseline
>
> **Design direction established:** Seven specific rules were identified (see Proposed Rules table above). The severity model and discovery mechanism are open design decisions for this proposal to resolve.

---

## References

- [hangar-ai-specs/changes/c-plus-plus-avatar-enrichment/PROPOSAL.md](../c-plus-plus-avatar-enrichment/PROPOSAL.md)
- [tools/constitution-lint/src/aa_constitution_lint/domain/rules/base.py](tools/constitution-lint/src/aa_constitution_lint/domain/rules/base.py)
- [tools/constitution-lint/src/aa_constitution_lint/domain/models.py](tools/constitution-lint/src/aa_constitution_lint/domain/models.py)
- [tools/constitution-lint/src/aa_constitution_lint/infrastructure/law_registry.py](tools/constitution-lint/src/aa_constitution_lint/infrastructure/law_registry.py)
- [avatars/index.yaml](avatars/index.yaml)
- [avatars/AVATAR-RAG-INDEX.yaml](avatars/AVATAR-RAG-INDEX.yaml)
- [avatars/technology/java-spring/manifest.yaml](avatars/technology/java-spring/manifest.yaml)
- [avatars/technology/python-fastapi/manifest.yaml](avatars/technology/python-fastapi/manifest.yaml)
- [laws/index.yaml](laws/index.yaml)
- [AGENTS.md](AGENTS.md)
