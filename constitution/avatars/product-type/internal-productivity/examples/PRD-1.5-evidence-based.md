---
law: PRD-1.5
avatar: avatar-product-internal-productivity
title: "Evidence-Based: Finance Analyst Data Entry Automation"
---

# PRD-1.5 Evidence-Based — Internal Productivity

## Law Summary

Investment decisions require quantified evidence gathered before the decision, not after.

---

## ✅ COMPLIANT Example

### Decision

> Invest in automating manual data entry for Finance Analysts generating monthly legacy reports.

### Hypothesis

> Finance Analysts spend ≥ 3 hours/day on manual data entry into legacy report templates. If we automate data extraction and formatting from HRIS and GL systems, we can reduce that to ≤ 30 minutes/day per analyst, saving ≥ 10 hours/week across the 5-analyst team.

### Evidence Package

**Source:** 6-week structured time observation across 5 Finance Analysts (Jan–Feb 2026). Each analyst tracked time by activity in 30-minute increments using a shared spreadsheet. Observed by UX Researcher for 2 days per analyst.

| Metric | Value | Source |
|--------|-------|--------|
| Avg hours/analyst/day on manual data entry | 3.2 hours | Time audit (6 weeks, 5 analysts) |
| % of data entry that is copy-paste from HRIS/GL | 78% | Workflow observation |
| % requiring analyst judgment | 22% | Workflow observation |
| Data entry error rate (requiring rework) | 4.8% | QA review of 12 months of reports |
| Rework hours per analyst per month (from errors) | 3.4 hours | Calculated from error rate × report count |
| Current tool: Excel + manual export from SAP | — | System audit |
| Hours available for value-added analysis | 1.8 hours/day | Calculated: 8 − 3.2 − other tasks |

**Analyst verbatim (n=5):** "I spend more time formatting spreadsheets than actually analyzing the numbers."

### Investment Calculation

| Item | Value |
|------|-------|
| Hours/week lost to manual entry (5 analysts) | 80 hours/week |
| Fully-loaded analyst cost/hour | $68 |
| Weekly cost of manual entry | $5,440 |
| Annualized cost | $283K/year |
| Estimated automation build cost | $95K |
| Estimated time-to-break-even | 4.2 months |

### Decision Gate

Proceed if: 6-week automation pilot reduces data entry time from 3.2 to ≤ 0.5 hours/day per analyst (≥ 84% reduction). Fail gate: < 60% reduction triggers investigation (data source quality, template complexity, or HRIS API limitations).

---

## ❌ VIOLATION Example

> "Manual data entry wastes time. Let's automate everything: all reports, real-time dashboards, self-service analytics, and natural-language queries."

**Why this violates PRD-1.5:**
- No evidence: 3.2 hours/day is the validated figure. "Wastes time" is not quantified.
- Full automation suite bundles multiple hypotheses — if it fails, root cause is unclear.
- Real-time dashboards and self-service analytics are different products with different value propositions.
- Correct approach: prove the 78% copy-paste automation hypothesis first.
