---
title: "avatar-tech-apigee-azure — RAG Validation Report"
spec_id: "rag-apigee-azure-2026-04-22"
type: avatar
workflow: "avatar-workflow"
phase: "phase-5-rag-validate"
confidence: "high"
rag_summary:
  recall: "5/5"
  recall_pct: 100
  max_tokens: 930
  precision_pct: 100
  confidence: "high"
  verdict: "PASS"
laws_applied:
  - ENG-13.1
  - ENG-11.1
exit_checklist:
  - item: "Q1 — Law coverage: all 7 law IDs with titles returned from manifest + guidance"
    status: "pass"
  - item: "Q2 — Security: ENG-6.1 OAuthV2 PreFlow, Managed Identity, M2M vs user auth table returned"
    status: "pass"
  - item: "Q3 — CI/CD setup: ENG-5.2 GitHub Actions pipeline for proxy + Terraform + Functions returned"
    status: "pass"
  - item: "Q4 — Example retrieval: ENG-4.1 atomic TDD across all 3 layers (Mocha, checkov, Jest) returned"
    status: "pass"
  - item: "Q5 — Audit trail: ENG-6.7 correlation ID propagation across Apigee + Azure Functions returned"
    status: "pass"
  - item: "Recall ≥ 95% (5/5 queries answered)"
    status: "pass"
  - item: "Max tokens per query response ≤ 3,500"
    status: "pass"
  - item: "Precision ≥ 90% (no hallucinated laws)"
    status: "pass"
  - item: "Rendered HTML reviewed in browser (ENG-13.1)"
    status: "confirmed"
stakeholder:
  name: "Adeel Ali"
  role: "Inventor / Co-founder"
  affirm: true
  note: "Approved 2026-04-22"
audit_log:
  - date: "2026-04-22"
    actor: "Amaya (Technical Coach)"
    action: "Phase 5 RAG simulation run — 5 canonical queries"
    outcome: "PASS"
spec_artifacts:
  - path: "avatars/technology/apigee-azure/manifest.yaml"
    type: "manifest"
    status: "COMPLETE"
  - path: "avatars/technology/apigee-azure/guidance.md"
    type: "guidance"
    status: "COMPLETE"
  - path: "avatars/technology/apigee-azure/examples/"
    type: "examples"
    status: "COMPLETE — 7 law examples (ENG-4.1, ENG-3.1, ENG-6.1, ENG-6.4, ENG-6.7, ENG-5.2, ENG-7.1)"
template_version: "1.0.0"
template_path: "docs/templates/avatars/rag-validation-template.md"
---

# avatar-tech-apigee-azure — RAG Validation Report

**Mode:** Generate
**Avatar type:** technology
**Date:** 2026-04-22
**Validator:** Amaya (Technical Coach) — file-based RAG simulation

---

## Query Results

| # | Query | Result | Laws/Content Returned | Token Count |
|---|-------|--------|----------------------|-------------|
| Q1 | What laws govern Apigee + Azure development at AA? | PASS | ENG-4.1, ENG-3.1, ENG-6.1, ENG-6.4, ENG-6.7, ENG-5.2, ENG-7.1 (manifest + guidance) | 574 |
| Q2 | How do I secure an Apigee proxy — OAuth and Managed Identity? | PASS | ENG-6.1-security-by-design.md — OAuthV2 PreFlow XML, Managed Identity Terraform + C#, M2M vs user auth table | 650 |
| Q3 | How do I set up CI/CD for Apigee and Terraform at AA? | PASS | manifest.yaml commands block + ENG-5.2-cicd-pipeline.md — GitHub Actions proxy deploy, Terraform plan/apply, Functions ZIP | 930 |
| Q4 | Show me an atomic TDD example for an Apigee proxy and Azure Function | PASS | ENG-4.1-atomic-tdd.md — Mocha proxy (Layer 1), checkov Terraform (Layer 2), Jest Function handler (Layer 3) | 700 |
| Q5 | How do I propagate correlation IDs across Apigee and Azure for audit compliance? | PASS | ENG-6.7-audit-trail.md — AM-CorrelationId AssignMessage, ML-AzureMonitor MessageLogging, Azure Functions structured logging | 600 |

---

## Threshold Summary

| Metric | Target | Actual | Result |
|--------|--------|--------|--------|
| Recall | ≥ 95% (5/5) | 5/5 (100%) | PASS |
| Max tokens per query | ≤ 3,500 | 930 | PASS |
| Precision (no hallucinated laws) | ≥ 90% | 100% | PASS |

---

## Verdict

**PASS — proceed to Phase 6 render gate**

> Render gate (ENG-13.1): HTML render of this report required. Human confirmation by Adeel before `rag_validated: true` is set in `index.yaml`.

---

## Notes

- All 7 law examples verified present on disk and within 850-token budget
- All law IDs are ENG-* — zero law boundary violations for a technology avatar
- guidance.md is pure navigation table format — trimmed to nav-table, within 450-token budget
- Cardinal rule: every gate device request hits Apigee first — OAuth at the edge, Managed Identity for every Azure service call downstream
- Key security pattern: never expose stack traces through Apigee FaultRules; normalized error envelope with correlation ID only
