---
title: "{Avatar ID} — RAG Validation Report"
spec_id: "{spec-id}"
type: avatar
workflow: "avatar-workflow"
phase: "phase-5-rag-validate"
confidence: "{low|medium|high}"
rag_summary:
  recall: "{n}/5"
  recall_pct: {0-100}
  max_tokens: {n}
  precision_pct: {0-100}
  confidence: "{low|medium|high}"
  verdict: "{PASS|FAIL}"
laws_applied:
  - ENG-13.1
  - ENG-11.1
exit_checklist:
  - item: "Q1 — Law coverage: ≥ 3 law IDs with titles returned"
    status: "pend"
  - item: "Q2 — Example retrieval: non-negotiable law example found"
    status: "pend"
  - item: "Q3 — Setup guidance: guidance.md accessible"
    status: "pend"
  - item: "Q4 — Use case retrieval: use-case file content returned"
    status: "pend"
  - item: "Q5 — Skill activation: activates.skills list returned"
    status: "pend"
  - item: "Recall ≥ 95% (5/5 queries answered)"
    status: "pend"
  - item: "Max tokens per query response ≤ 3,500"
    status: "pend"
  - item: "Precision ≥ 90% (no hallucinated laws)"
    status: "pend"
  - item: "Rendered HTML reviewed in browser (ENG-13.1)"
    status: "pend"
stakeholder:
  name: "{Reviewer Name}"
  role: "{Role}"
  affirm: false
  note: "Pending review"
audit_log:
  - date: "{YYYY-MM-DD}"
    actor: "{Agent or Human}"
    action: "RAG validation run completed"
    outcome: "DRAFTED"
spec_artifacts:
  - path: "avatars/{type}/{domain}/manifest.yaml"
    type: "manifest"
    status: "IN_PROGRESS"
  - path: "avatars/{type}/{domain}/guidance.md"
    type: "guidance"
    status: "IN_PROGRESS"
  - path: "avatars/{type}/{domain}/examples/"
    type: "examples"
    status: "IN_PROGRESS"
template_version: "1.0.0"
template_path: "docs/templates/avatars/rag-validation-template.md"
---

# {Avatar ID} — RAG Validation Report

**Mode:** {Generate | Assess & Correct | Enrich}
**Avatar type:** {technology | product | industry}
**Date:** {YYYY-MM-DD}
**Validator:** {agent-id or human reviewer}

---

## Query Results

| # | Query | Result | Laws/Content Returned | Token Count |
|---|-------|--------|----------------------|-------------|
| Q1 | What laws govern {stack/domain} development at AA? | PASS / FAIL | {law IDs returned} | {n} |
| Q2 | Show me a {stack/domain} example for {non-negotiable law} | PASS / FAIL | {example file found} | {n} |
| Q3 | How do I set up a {stack/domain} project at AA? | PASS / FAIL | {guidance.md sections} | {n} |
| Q4 | What is the use case for {stack/domain} in {context}? | PASS / FAIL | {use-case file found} | {n} |
| Q5 | What skills are activated by the {stack/domain} avatar? | PASS / FAIL | {skills list} | {n} |

---

## Threshold Summary

| Metric | Target | Actual | Result |
|--------|--------|--------|--------|
| Recall | ≥ 95% (5/5) | {n}/5 ({pct}%) | PASS / FAIL |
| Max tokens per query | ≤ 3,500 | {n} | PASS / FAIL |
| Precision (no hallucinated laws) | ≥ 90% | {pct}% | PASS / FAIL |

---

## Verdict

**{PASS — proceed to Phase 6 render gate | BLOCKED — resolve failures before re-running}**

### Failures to resolve (if BLOCKED)

| Query | Root cause | Fix required |
|-------|-----------|-------------|
| {Q#} | {Root cause} | {What to add/change in Phase 4} |

---

## Notes

{Any observations about token budgets, missing use cases, or law coverage gaps that do not block but should be addressed in the next enrich cycle.}
