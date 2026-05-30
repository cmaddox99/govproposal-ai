---
law: PRD-1.2
avatar: avatar-product-customer-relations-ops
title: "Problem-First: AI Draft Assistance vs. Auto-Send"
---

# PRD-1.2 Problem-First — Customer Relations Operations

## Law Summary

Validate the actual bottleneck before committing to a solution. Stakeholder requests often describe a solution, not the problem.

---

## ✅ COMPLIANT Example

### Stated Request

> "Auto-send all complaint responses to reduce backlog and meet SLA targets."

### Research Conducted

Time-in-motion study with 8 CR Reps (4 weeks), audit of 90 days of complaint response data, and SLA compliance analysis.

| Finding | Value | Source |
|---------|-------|--------|
| Average time per complaint from intake to response | 45 minutes | Time-in-motion study |
| % of cases missing 3-day SLA | 32% | SLA compliance audit |
| Time breakdown: draft writing | 28 min (62%) | Time-in-motion study |
| Time breakdown: policy research | 11 min (24%) | Time-in-motion study |
| Time breakdown: review and send | 6 min (13%) | Time-in-motion study |
| Draft acceptance rate for existing templates | 74% | Template audit |
| % of responses that required compliance correction post-send | 2.1% | Compliance audit (90 days) |

**Root cause:** 62% of the 45-minute handle time is spent writing drafts from scratch. Policy research (11 min) is the second driver — reps frequently look up the same policies repeatedly. Auto-send without human review is not a viable solution: the 2.1% compliance violation rate means auto-send would produce DOT violations at scale.

### Validated Problem Statement

> CR Reps spend 28 minutes per complaint writing drafts from scratch. Policy and compensation calculation is a secondary bottleneck (11 min). The 3-day SLA violation (32% of cases) is caused by drafting time, not send-step delays. **AI draft assistance** (not auto-send) that reduces drafting from 28 to ≤ 10 minutes addresses the root cause. Auto-send removes the human review that prevents compliance violations.

### Correct Solution Direction

AI-generated draft that the CR Rep reviews and approves before sending. Not auto-send. Target: reduce draft time from 28 to ≤ 10 minutes. Expected SLA compliance improvement: 32% violation rate to ≤ 15%.

---

## ❌ VIOLATION Example

> "We're missing SLA targets. Auto-send AI responses for all complaint categories to clear the backlog."

**Why this violates PRD-1.2:**
- No root cause analysis: is the bottleneck drafting, research, or send-step approvals?
- Auto-send removes the review that prevents compliance violations.
- 2.1% violation rate × scale = hundreds of DOT violations per month at auto-send volume.
- Correct first step: time-in-motion study to identify the specific time-consuming step.
