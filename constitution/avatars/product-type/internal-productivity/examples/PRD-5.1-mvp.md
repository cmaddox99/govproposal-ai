---
law: PRD-5.1
avatar: avatar-product-internal-productivity
title: "MVP: Monthly Headcount Report Automation"
---

# PRD-5.1 MVP Law — Internal Productivity

## Law Summary

The smallest experiment that validates the hypothesis is the correct first investment. Automate one workflow completely before building the second.

---

## ✅ COMPLIANT Example — MVP Canvas

### Hypothesis

> Automating the monthly headcount report generation (pulling from Workday HRIS, applying standard formatting, and generating the Excel output) will reduce HR Business Partner preparation time from 4 hours to ≤ 30 minutes per month-end cycle.

### Riskiest Assumption

Workday HRIS data is clean and consistently structured enough for automated extraction. If headcount data has frequent exceptions, manual correction overhead will eliminate the time savings.

### MVP Scope

**In scope:**
- One report: Monthly Headcount Report (current employees, new hires, terminations, by department and cost center)
- One data source: Workday HRIS (read-only API)
- Output: Formatted Excel file matching current template exactly
- Trigger: Manual run by HR Business Partner (not scheduled automation)
- Audience: 3 HR Business Partners who currently generate this report

**Out of scope:**
- Full HR analytics suite
- Real-time dashboards
- Self-service access for line managers
- Additional reports (turnover, compensation, performance)
- Scheduled/automated runs without human trigger
- Integration with Tableau or Power BI

### Acceptance Criteria

```gherkin
Scenario: HR Business Partner generates monthly headcount report
  Given it is the first business day after month-end
  And the Workday HRIS data has been finalized
  When the HR Business Partner runs the headcount report automation
  Then a formatted Excel file is generated in ≤ 5 minutes
  And the file matches the standard template layout exactly
  And headcount figures reconcile with Workday source within 0 variance
  And the HR Business Partner does not need to manually copy or format data
```

### Success Criteria (First 3 Month-End Cycles)

| Metric | Baseline | Target | Fail Gate |
|--------|----------|--------|-----------|
| Report preparation time per analyst | 4 hours | ≤ 30 minutes | > 90 min → investigate data quality |
| Data reconciliation variance | N/A | 0 discrepancies | > 0 → halt, fix data pipeline |
| Analyst satisfaction with output | N/A | ≥ 4.0/5.0 | < 3.5 → investigate template compliance |
| Report generation errors requiring manual correction | N/A | 0 per cycle | > 1 → review Workday API data quality |

### What This Proves

If the headcount report MVP achieves ≤ 30-minute generation: the Workday API integration pattern is reusable for other HRIS-sourced reports, and the automation approach is validated for the team.

Workflow 2 (AP exception coding) begins only after 3 successful month-end cycles with headcount automation.

---

## ❌ VIOLATION Example

> "Let's automate all 12 monthly Finance and HR reports simultaneously, integrate with SAP, Workday, and Tableau, and build a self-service portal for line managers."

**Why this violates PRD-5.1:**
- 12 reports × 3 data sources = too many assumptions bundled.
- If any data source has quality issues, all 12 reports fail simultaneously.
- Self-service portal is a separate product that requires validated automation first.
- Correct approach: one report, one data source, three cycles of proof.
