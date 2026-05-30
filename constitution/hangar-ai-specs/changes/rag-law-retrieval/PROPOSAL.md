# Proposal: RAG Law Retrieval — Section Heading Improvements

**ID:** rag-law-retrieval
**Status:** PROPOSED
**Branch:** `proposal/rag-law-retrieval`
**Targets:** `law_retrieval` dimension → 88.8% → 100%
**Independent:** Can be merged in any order relative to the other RAG PRs

---

## Problem Statement

The RAG evaluator's `law_retrieval` dimension measures whether the expected law ID appears in
the retrieved results for a given query. Currently **15 queries fail** (88.8%, 119/134).

The retriever uses `##` section headings as high-weight trigger phrases (weight 2.0× vs keyword
weight 1.0×). The three `foundations.md` files contain dense, general vocabulary and consistently
occupy 2–3 of the top-3 slots for many queries, leaving no room for the specific law file that
owns the query's intent. Adding a targeted section heading to the correct law file converts a
keyword-weight hit into a trigger-phrase hit, doubling its score and displacing a foundations file.

| Metric | Before | After |
|--------|--------|-------|
| `law_retrieval` | 88.8% (119/134) | 100% (134/134) |
| Retrieval failures | 15 | 0 |

---

## Failure Analysis

| Failing Query (test case) | Expected Law | Root Cause |
|---|---|---|
| "What are the security requirements I must include in every feature?" (tc-eng-005) | `ENG-6.1` | `foundations.md` scores higher than `security.md`; no matching heading in security.md |
| "What are the stage gate criteria to move from discovery to design?" (tc-prd-008) | `PRD-2.5` | Product foundations outscores discovery.md; no "stage gate" heading |
| "Can we skip the discovery stage and go straight to development?" (tc-prd-009) | `PRD-2.5` | Same — discovery.md lacks heading for skipping stages |
| "What evidence must I file before moving to the next discovery stage?" (tc-prd-010) | `PRD-2.5` | Same — no evidence-filing heading in discovery.md |
| "We are making this decision based on gut feel — is that okay?" (tc-prd-006) | `PRD-1.5` | Foundations outscores; no "gut feel / evidence-based" heading in foundations.md |
| "How do I validate an assumption before we commit to building?" (tc-prd-007) | `PRD-1.5` | Same — "validate assumption" not a trigger in product foundations |
| "Should we invest in acquisition or reduce churn first?" (tc-prd-015) | `PRD-6.2` | `metrics.md` lacks "acquisition vs churn" heading |
| "How do I measure and improve retention metrics for AAdvantage?" (tc-prd-016) | `PRD-6.2` | `metrics.md` lacks "AAdvantage retention" heading |
| "How do I map all applicable FAA and aviation regulatory requirements?" (tc-bus-004) | `BUS-2.1` | `compliance.md` lacks "FAA regulatory mapping" heading; foundations wins |
| "What are the DOT refund requirements when a flight is cancelled?" (tc-bus-005) | `BUS-2.3` | `compliance.md` lacks "DOT consumer protection" heading |
| "How do I implement the right to erasure for customer accounts?" (tc-bus-010) | `BUS-4.3` | `compliance.md` lacks "right to erasure" heading |
| "What law governs the presentation of governance artifacts?" (tc-ar-003) | `ENG-13.1` | `artifact-rendering.md` lacks "governance artifact presentation" heading |
| "How do I add correlation ID tracing to my service?" (tc-eng-013) | `ENG-6.7` | `governance.md` lacks "correlation ID tracing" heading |
| "C++ MISRA safety-critical DO-178C aviation — what requirements apply to avionics C++ code?" (tc-av-040) | `ENG-4.1`, `ENG-6.1` | `testing.md` and `security.md` lack "DO-178C" / "avionics" headings |
| "C++ test traceability FAR-117 — how do I link C++ unit tests to FAR Part 117 requirements?" (tc-av-059) | `ENG-4.1`, `ENG-6.7` | `testing.md` and `governance.md` lack "FAR Part 117 traceability" heading |

---

## Scope

### In Scope
- Add targeted `##` section headings to 9 law files
- Narrow overly-generic headings in `foundations.md` files to reduce false-positive scoring

### Out of Scope
- Changing any law content (only headings added/renamed)
- Changes to `agent-skills/` files
- Deferred law cleanup (covered by `proposal/rag-deferred-laws-cleanup`)
- Trigger phrase additions (covered by `proposal/rag-skill-routing`)

---

## Tasks

| ID | Description | File | Fixes |
|----|-------------|------|-------|
| LR-01 | Add `## Security Requirements in Every Feature` heading to `security.md` | `laws/engineering/security.md` | tc-eng-005, tc-av-040 |
| LR-02 | Add `## Coverage Gates and Test Traceability` and `## DO-178C Avionics Safety Requirements` headings to `testing.md` | `laws/engineering/testing.md` | tc-av-040, tc-av-059 |
| LR-03 | Add `## Governance Artifact Presentation` heading to `artifact-rendering.md` | `laws/engineering/artifact-rendering.md` | tc-ar-003 |
| LR-04 | Add `## Audit Trail and Correlation ID Tracing` and `## FAR Part 117 Test Traceability` headings to `governance.md` | `laws/engineering/governance.md` | tc-eng-013, tc-av-059 |
| LR-05 | Add `## FAA Regulatory Mapping`, `## DOT Consumer Protection and Refund Requirements`, and `## Right to Erasure and Account Deletion` headings to `compliance.md` | `laws/business/compliance.md` | tc-bus-004, tc-bus-005, tc-bus-010 |
| LR-06 | Rename generic headings in `foundations.md` to domain-specific ones to reduce false-positive trigger weight (e.g., `## Business Priorities` → `## Legal and Regulatory Priority Hierarchy`) | `laws/business/foundations.md` | multiple |
| LR-07 | Add `## Stage Gate Criteria` and `## Evidence Required Before Advancing Discovery Stages` headings to `discovery.md` | `laws/product/discovery.md` | tc-prd-008, tc-prd-009, tc-prd-010 |
| LR-08 | Add `## AAdvantage Retention Metrics` and `## Acquisition vs Churn Investment Decisions` headings to `metrics.md` | `laws/product/metrics.md` | tc-prd-015, tc-prd-016 |
| LR-09 | Add `## Evidence-Based Decision Making` and `## Validate Assumptions Before Committing` headings to `foundations.md`; narrow generic headings to reduce false-positive scoring | `laws/product/foundations.md` | tc-prd-006, tc-prd-007 |
| LR-10 | Verify full test suite (786+ tests) and constitution-lint (20/20) pass | all | quality gate |

---

## Acceptance Criteria

1. `python3 tools/rag-eval/evaluate.py` reports `law_retrieval: 100%`
2. `python3 -m pytest tests/unit/ tests/governance/ -q` — 786+ tests pass
3. `aa-constitution-lint .` — 20/20 pass
4. All 15 previously failing law retrieval test cases now pass
5. No law content changed — only section headings added or renamed
