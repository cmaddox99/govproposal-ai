# Proposal: RAG Cross-Reference Cleanup — Remove Deferred Law References

**ID:** rag-deferred-laws-cleanup
**Status:** PROPOSED
**Branch:** `proposal/rag-deferred-laws-cleanup`
**Targets:** `cross_ref_consistency` dimension → 98.1% → 100%
**Stacked By:** `proposal/rag-skill-routing` (PR B — must merge this first)

---

## Problem Statement

The RAG evaluator's `cross_ref_consistency` check scans all `agent-skills/` files for law ID
patterns (`[A-Z]{2,5}-\d+\.\d+`) and flags any ID not present in the live law registry.
Currently **20 references** across 13 skill files and index files are flagged as unknown.

All 20 are forward references to laws listed in `DEFERRED_LAWS.md` — laws that were planned
but never authored. One additional false positive (`BSL-1.0`, Business Source License) matches
the law ID regex but is a software license identifier, not a law.

**Decision:** Remove `DEFERRED_LAWS.md` and eliminate all deferred law ID references from
`agent-skills/` files. Deferred law IDs add noise and should not be cited in skills until
the laws are actually authored and registered.

| Metric | Before | After |
|--------|--------|-------|
| `cross_ref_consistency` | 98.1% (1471/1500) | 100% (1500/1500) |
| Unknown law ID failures | 20 | 0 |

---

## Deferred IDs to Remove

| ID | Skill Files Referencing It |
|----|---------------------------|
| `ENG-8.1` | `platform-engineering/12-api-design.md` |
| `ENG-9.1` | `ml-ai/23-ai-agents.md`, `ml-ai/21-prompt-engineering.md`, `ml-ai/index.yaml` |
| `ENG-9.4` | `ml-ai/23-ai-agents.md`, `ml-ai/24-ai-safety.md`, `ml-ai/index.yaml` |
| `BUS-5.1` | `platform-engineering/10-security-review.md` |
| `BUS-8.5` | `platform-engineering/skill-cpp-dependency-governance.md` |
| `BUS-10.3` | `platform-engineering/11-incident-response.md` |
| `PRD-7.1` | `platform-engineering/14-technical-debt.md`, `product-planning/01-roadmapping.md`, `platform-engineering/index.yaml` |
| `PRD-7.2` | `platform-engineering/14-technical-debt.md`, `platform-engineering/index.yaml` |
| `PRD-8.2` | `ml-ai/20-ml-monitoring.md` |
| `PRD-8.3` | `platform-engineering/13-observability.md`, `platform-engineering/27-constitution-compliance.md` |
| `PRD-9.3` | `product-planning/16-documentation.md`, `product-planning/index.yaml` |
| `BSL-1.0` *(false positive)* | `platform-engineering/skill-cpp-dependency-governance.md` — reformat as inline code |

---

## Scope

### In Scope
- Delete `DEFERRED_LAWS.md` from repository root
- Remove deferred law ID references from 10 skill `.md` files
- Remove deferred law ID references from 3 domain `index.yaml` files
- Reformat `BSL-1.0` in `skill-cpp-dependency-governance.md` as inline code (`` `BSL-1.0` ``)
  so the law ID regex does not false-positive match it

### Out of Scope
- Authoring any of the removed law IDs (separate domain-owner effort)
- Changes to `tools/rag-eval/` — the evaluator requires no modification
- Changes to `laws/` files
- Trigger phrase improvements (covered by `proposal/rag-skill-routing`)

---

## Tasks

| ID | Description | Files |
|----|-------------|-------|
| DLC-01 | Delete `DEFERRED_LAWS.md` from repository root | `DEFERRED_LAWS.md` |
| DLC-02 | Remove `ENG-8.1` from `12-api-design.md` | `platform-engineering/12-api-design.md` |
| DLC-03 | Remove `ENG-9.1`, `ENG-9.4` from `23-ai-agents.md` | `ml-ai/23-ai-agents.md` |
| DLC-04 | Remove `ENG-9.1` from `21-prompt-engineering.md` | `ml-ai/21-prompt-engineering.md` |
| DLC-05 | Remove `ENG-9.4` from `24-ai-safety.md` | `ml-ai/24-ai-safety.md` |
| DLC-06 | Remove `BUS-5.1` from `10-security-review.md` | `platform-engineering/10-security-review.md` |
| DLC-07 | Remove `BUS-8.5` from `skill-cpp-dependency-governance.md`; reformat `BSL-1.0` as inline code | `platform-engineering/skill-cpp-dependency-governance.md` |
| DLC-08 | Remove `BUS-10.3` from `11-incident-response.md` | `platform-engineering/11-incident-response.md` |
| DLC-09 | Remove `PRD-7.1`, `PRD-7.2` from `14-technical-debt.md` | `platform-engineering/14-technical-debt.md` |
| DLC-10 | Remove `PRD-7.1` from `01-roadmapping.md` | `product-planning/01-roadmapping.md` |
| DLC-11 | Remove `PRD-8.2` from `20-ml-monitoring.md` | `ml-ai/20-ml-monitoring.md` |
| DLC-12 | Remove `PRD-8.3` from `13-observability.md` and `27-constitution-compliance.md` | `platform-engineering/13-observability.md`, `platform-engineering/27-constitution-compliance.md` |
| DLC-13 | Remove `PRD-9.3` from `16-documentation.md` | `product-planning/16-documentation.md` |
| DLC-14 | Remove `ENG-9.1`, `ENG-9.4` from `ml-ai/index.yaml`; remove `PRD-7.2` from `platform-engineering/index.yaml`; remove `PRD-9.3` from `product-planning/index.yaml` | 3 index.yaml files |
| DLC-15 | Verify full test suite (786+ tests) and constitution-lint (20/20) pass | all |

---

## Acceptance Criteria

1. `python3 tools/rag-eval/evaluate.py` reports `cross_ref_consistency: 100%`
2. Zero unknown law ID failures in the evaluator output
3. `python3 -m pytest tests/unit/ tests/governance/ -q` — 786+ tests pass
4. `aa-constitution-lint .` — 20/20 pass
5. `DEFERRED_LAWS.md` does not exist in the repository
6. `grep -r "ENG-8.1\|ENG-9.1\|ENG-9.4\|BUS-5.1\|BUS-8.5\|BUS-10.3\|PRD-7.1\|PRD-7.2\|PRD-8.2\|PRD-8.3\|PRD-9.3" agent-skills/` returns no matches
