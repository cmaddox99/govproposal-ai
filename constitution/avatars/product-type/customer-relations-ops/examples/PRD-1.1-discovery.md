---
law: PRD-1.1
avatar: avatar-customer-relations-ops
title: "Continuous Discovery — CR Draft Quality and Pipeline Efficiency"
---

# PRD-1.1 Continuous Discovery — Customer Relations Ops

## Context

CR Operations uses AI-assisted drafting for complaint responses. Discovery focuses on
draft acceptance rates, compliance violation patterns, and CR Rep efficiency signals.

---

## ✅ COMPLIANT Example

### Weekly Draft Quality Analysis (FastAPI audit traces)

| Metric | Current | Target | Signal |
|--------|---------|--------|--------|
| Draft acceptance rate | 76% | >80% | 24% major-edit rate — primary improvement area |
| Compliance violations | 0% | 0% | No violations delivered (pipeline enforcing) |
| PII in LLM payload | 0% | 0% | pii_redact.py blocking all PII from LLM |
| Avg review time | 142s | <120s | 22s over target — classification delay primary cause |
| Category accuracy | 87% | >95% | Lost-baggage and delay categories confused 13% |

**Discovery finding:** Draft acceptance 76% → root cause: compensation estimate in draft
misaligns with agent's manual calculation for delay categories. Not a language quality issue.

### CR Rep Interviews (N=12, 3 hubs)

| Issue | Frequency | Implication |
|-------|-----------|-------------|
| "Draft compensation is wrong" | 10/12 | CompensationValidator not using latest tier table |
| "Draft too formal for informal complaints" | 8/12 | Tone template needs calibration for complaint severity |
| "Takes too long to appear" | 7/12 | Classification stage latency p95 = 4.8s (target <2s) |

### Discovery Output → Problem Statement

> **Validated problem:** CompensationValidator using stale tier table drives 10/12 draft rejections.
> **Evidence:** Audit traces + interviews confirm compensation mismatch pattern.
> **Next step:** Update CompensationValidator to pull tier table from live config.
