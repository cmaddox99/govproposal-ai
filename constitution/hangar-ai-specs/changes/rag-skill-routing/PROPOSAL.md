# Proposal: RAG Skill Routing — Trigger Phrase Improvements

**ID:** rag-skill-routing
**Status:** PROPOSED
**Branch:** `proposal/rag-skill-routing`
**Targets:** `skill_routing` dimension → 81.4% → 100%
**Stacked On:** `proposal/rag-deferred-laws-cleanup` — **must merge that PR first**

---

## Problem Statement

The RAG evaluator's `skill_routing` dimension measures whether the correct skill file is returned
in the top-3 results for a given query. Currently **16 queries fail** (81.4%, 70/86).

The retriever routes skill queries exclusively via trigger phrases defined in each domain's
`index.yaml`. When a query's wording doesn't appear as a substring of any trigger phrase,
the wrong skill wins — typically a C++ skill with high token overlap scores higher than the
correct intent-matched skill.

**Note — stacking dependency:** This proposal modifies the same `index.yaml` files that
`proposal/rag-deferred-laws-cleanup` also modifies (removing deferred law ID references).
Specifically, `ml-ai/index.yaml` lines 44–45 have adjacent `triggers:`/`laws:` edits between
the two proposals. **This PR must be based on `proposal/rag-deferred-laws-cleanup` and merged
after it to avoid a merge conflict.**

| Metric | Before | After |
|--------|--------|-------|
| `skill_routing` | 81.4% (70/86) | 100% (86/86) |
| Routing failures | 16 | 0 |

---

## Failure Analysis

| Failing Query (test case) | Expected Skill | Why It Fails |
|---|---|---|
| "How do I justify this feature to leadership?" (tc-prd-001) | `product-discovery-orchestration.md` | "justify feature" not in triggers |
| "What problem does this feature actually solve for users?" (tc-prd-002) | `product-discovery-orchestration.md` | "what problem does this solve" not in triggers |
| "We want to build a feature but haven't identified the user problem yet" (tc-prd-003) | `product-discovery-orchestration.md` | "haven't identified the user problem" not in triggers |
| "How do I validate that the problem we are solving is real?" (tc-prd-004) | `product-discovery-orchestration.md` | "validate the problem" not in triggers |
| "What evidence do I need before making a product decision?" (tc-prd-005) | `product-discovery-orchestration.md` | "evidence before product decision" not in triggers |
| "What are the stage gate criteria to move from discovery to design?" (tc-prd-008) | `product-discovery-orchestration.md` | "stage gate criteria" not in discovery triggers |
| "How do I define an MVP for this new booking feature?" (tc-prd-011) | `01-roadmapping.md` | "define an MVP" not in roadmapping triggers |
| "What is the smallest thing we can build to test our riskiest assumption?" (tc-prd-012) | `01-roadmapping.md` | "riskiest assumption" not in triggers |
| "What is the minimum viable feature we need to ship?" (tc-prd-013) | `01-roadmapping.md` | "minimum viable feature" not in triggers |
| "Should we invest in acquisition or reduce churn first?" (tc-prd-015) | `01-roadmapping.md` | "reduce churn", "acquisition" not in triggers |
| "I am building an AI agent with LangChain" (tc-av-013) | `23-ai-agents.md` | "LangChain" only in prompt-engineering triggers; ai-agents entry lacks it |
| "What law governs the presentation of governance artifacts?" (tc-ar-003) | `skill-artifact-html-rendering.md` | C++ skills dominate "governance" tokens; artifact rendering trigger absent |
| "What is our obligation when a data breach occurs involving passenger PII?" (tc-bus-014) | `11-incident-response.md` | "data breach occurs", "passenger PII" not in incident-response triggers |
| "What is the data classification policy for passenger data?" (tc-eng-009) | `10-security-review.md` | "data classification policy" not in security-review triggers |
| "How do I write a characterization test to pin legacy C++ behavior?" (tc-av-060) | `skill-cpp-legacy-survival-patterns` | "golden-master", "characterization test to pin legacy" not in index triggers |
| "How do I write unit tests for an Android Kotlin app using JUnit 5 and MockK?" (tc-av-020) | `skill-06-atomic-tdd` | "junit 5 mockk", "android kotlin" not in atomic-tdd triggers |

---

## Scope

### In Scope
- Add trigger phrases to 4 domain `index.yaml` files:
  - `agent-skills/skills-by-domain/discovery-research/index.yaml`
  - `agent-skills/skills-by-domain/product-planning/index.yaml`
  - `agent-skills/skills-by-domain/ml-ai/index.yaml`
  - `agent-skills/skills-by-domain/development-practices/index.yaml`
  - `agent-skills/skills-by-domain/platform-engineering/index.yaml`

### Out of Scope
- Changes to skill `.md` body files (only trigger phrases in index files)
- Changes to `laws/` files (covered by `proposal/rag-law-retrieval`)
- Deferred law ID cleanup (covered by `proposal/rag-deferred-laws-cleanup`)

---

## Tasks

| ID | Description | File | Fixes |
|----|-------------|------|-------|
| SR-01 | Add triggers to `product-discovery-orchestration.md` entry in `discovery-research/index.yaml`: "justify this feature", "what problem does this feature solve", "haven't identified the user problem", "validate the problem is real", "evidence before making a product decision" | `discovery-research/index.yaml` | tc-prd-001/002/003/004/005 |
| SR-02 | Add triggers to `product-discovery-orchestration.md` entry for stage-gate: "stage gate criteria" | `discovery-research/index.yaml` | tc-prd-008 |
| SR-03 | Add triggers to `01-roadmapping.md` entry in `product-planning/index.yaml`: "define an MVP", "minimum viable feature", "riskiest assumption", "reduce churn", "invest in acquisition" | `product-planning/index.yaml` | tc-prd-011/012/013/015 |
| SR-04 | Add "building an AI agent with LangChain", "AI agent with LangChain" to `23-ai-agents.md` triggers in `ml-ai/index.yaml` | `ml-ai/index.yaml` | tc-av-013 |
| SR-05 | Add "governance artifact", "presentation of governance artifacts" to `skill-artifact-html-rendering.md` triggers in `development-practices/index.yaml` | `development-practices/index.yaml` | tc-ar-003 |
| SR-06 | Add "data breach occurs", "passenger PII obligation" to `11-incident-response.md` triggers in `platform-engineering/index.yaml` | `platform-engineering/index.yaml` | tc-bus-014 |
| SR-07 | Add "data classification policy" to `10-security-review.md` triggers in `platform-engineering/index.yaml` | `platform-engineering/index.yaml` | tc-eng-009 |
| SR-08 | Add "characterization test to pin legacy", "golden-master" to `skill-cpp-legacy-survival-patterns` triggers in `platform-engineering/index.yaml` | `platform-engineering/index.yaml` | tc-av-060 |
| SR-09 | Add "android kotlin unit tests", "junit 5 mockk" to `skill-06-atomic-tdd` triggers in `development-practices/index.yaml` | `development-practices/index.yaml` | tc-av-020 |
| SR-10 | Verify full test suite (786+ tests) and constitution-lint (20/20) pass | all | quality gate |

---

## Acceptance Criteria

1. `python3 tools/rag-eval/evaluate.py` reports `skill_routing: 100%`
2. `python3 -m pytest tests/unit/ tests/governance/ -q` — 786+ tests pass
3. `aa-constitution-lint .` — 20/20 pass
4. All 16 previously failing test cases (tc-prd-001 through tc-prd-005, tc-prd-008, tc-prd-011/012/013/015, tc-av-013, tc-ar-003, tc-bus-014, tc-eng-009, tc-av-060, tc-av-020) now pass
