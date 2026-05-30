---
law: PRD-2.5
avatar: avatar-product-internal-productivity
title: "Stage-Gate: Workflow Automation Tool Discovery"
---

# PRD-2.5 Stage-Gate — Internal Productivity

## Law Summary

Each discovery stage has defined evidence requirements. Stage B does not begin until Stage A evidence is accepted by the product and engineering leads.

---

## ✅ COMPLIANT Example

### Initiative

Workflow Automation Tool for Operations and Finance teams — automate repetitive manual reporting and data entry workflows.

---

### Stage A — Opportunity Quantification Gate

**Question to answer:** What is the total hours-saved opportunity across the 3 target workflows, and which has the highest ROI for MVP?

**Target workflows under evaluation:**
1. Monthly headcount report generation (HRIS → Excel)
2. Accounts payable exception coding (SAP → GL)
3. Budget variance commentary drafting (Finance data → PowerPoint)

**Required evidence before Stage B:**

| Evidence Required | Method | Owner | Deadline |
|------------------|--------|-------|----------|
| Time-per-workflow audit (hours/analyst/month) | Structured time tracking, 4 weeks, 8 analysts | UX Researcher | Week 4 |
| Error rate per workflow | QA audit of 3 months of output per workflow | Finance QA Lead | Week 4 |
| Automatable % per workflow (rule-based vs. judgment) | Workflow decomposition with 3 senior analysts | Product Manager | Week 4 |
| System integration feasibility (HRIS, SAP API availability) | Technical spike — read-only API test | Platform Engineer | Week 3 |
| Analyst willingness to change workflow | 8 structured interviews | UX Researcher | Week 3 |

**Stage A Evidence Targets:**

| Workflow | Required to Proceed |
|----------|-------------------|
| Monthly headcount report | ≥ 3 hours/analyst/month, ≥ 70% automatable |
| AP exception coding | ≥ 3 hours/analyst/month, ≥ 70% automatable |
| Budget variance commentary | ≥ 3 hours/analyst/month, ≥ 60% automatable |

**Stage A Gate Decision (Week 5):**
- ✅ Proceed: rank the 3 workflows by (hours saved × automatable %) / build complexity. Top-ranked workflow becomes MVP.
- ❌ Pivot: if no workflow meets thresholds, the automation opportunity is smaller than assumed — investigate different team or workflow set.

---

### Stage B — MVP Design Gate (If Stage A Passes)

**Question to answer:** What is the minimum automation that proves the top-ranked workflow can be automated with measurable time savings?

**Required evidence before build:**
- Wizard-of-Oz prototype tested with 3 analysts (simulated automation, human-operated backend)
- HRIS/SAP API read access confirmed (technical prerequisite)
- Target time reduction agreed: from X hours to Y hours per analyst per month

---

## ❌ VIOLATION Example

> "Let's build an automation platform that connects all of our Finance and HR systems, generates reports on demand, and uses AI to draft commentary. We'll find the use cases as we build."

**Why this violates PRD-2.5:**
- No Stage A: hours-saved opportunity is unquantified.
- "Find use cases as we build" = building without a validated problem.
- Platform investment before any single workflow is proven automatable.
- Correct first step: 4-week time audit across 3 workflows to identify which one to start with.
