---
law: PRD-2.5
avatar: avatar-product-customer-service
title: "Stage-Gate: AI Complaint Resolution Discovery"
---

# PRD-2.5 Stage-Gate — Customer Service

## Law Summary

Each discovery stage has a required evidence output. Stage B does not begin until Stage A evidence meets the acceptance threshold.

---

## ✅ COMPLIANT Example

### Initiative

AI-Assisted Complaint Resolution — reduce average complaint response time from 3 days to < 24 hours using AI-drafted responses.

---

### Stage A — Problem Validation Gate

**Question to answer:** What % of complaints have a data-available resolution (policy lookup, compensation calculation) vs. a judgment call (goodwill, service recovery discretion)?

**This matters because:** AI can assist with data-available resolutions. Judgment-call complaints require human decision authority. If 80%+ of complaints are judgment calls, AI drafting will produce low-acceptance-rate output that agents reject — wasting investment.

**Required evidence before Stage B:**

| Evidence Required | Method | Sample | Owner | Deadline |
|------------------|--------|--------|-------|----------|
| Complaint coding by resolution type | Code 200 recent complaints: data-available vs. judgment call vs. mixed | 200 samples | UX Researcher + CR Lead | Week 3 |
| Draft acceptance rate baseline | Measure current template acceptance rate (existing templates) | 4-week audit | Analytics | Week 3 |
| Agent time breakdown | Time-in-motion study: how much of 45 min is research vs. writing vs. review? | 8 agents, 2 weeks | UX Researcher | Week 3 |
| Compliance violation rate baseline | Audit last 90 days: prohibited language, incorrect compensation amounts | 90-day audit | Compliance | Week 3 |

**Stage A Acceptance Threshold:**
- ✅ Proceed to Stage B if: ≥ 40% of complaints are data-available resolution type. AI drafting is viable.
- ❌ Pivot if: < 40% data-available. AI drafting investment will produce low-quality output; focus on research/lookup tooling instead.

---

### Stage B — Solution Design Gate (If Stage A Passes)

**Question to answer:** What is the minimum AI drafting capability that reduces research time (not writing time)?

**Required evidence before build:**
- Paper prototype of AI-assisted draft flow tested with 6 CR Reps
- Compliance review of draft output quality on 50 sample complaints
- Agreement on draft acceptance rate target: ≥ 80% of AI drafts accepted without rewrite

---

## ❌ VIOLATION Example

> "AI is getting good at writing. Let's build an end-to-end AI complaint resolution system that automatically sends responses for all complaint categories."

**Why this violates PRD-2.5:**
- No Stage A: what % of complaints can actually be auto-resolved vs. require judgment?
- Auto-send without CR Rep review violates BUS-7.1 (audit trail) and is a regulatory risk.
- "AI is getting good at writing" is not evidence about complaint resolution quality.
- Skips the discovery stage entirely and jumps to build.
