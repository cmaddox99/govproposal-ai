---
law: PRD-6.2
avatar: avatar-product-internal-productivity
title: "Retention: Internal Tool Quality and Analyst Attrition"
---

# PRD-6.2 Retention Law — Internal Productivity

## Law Summary

Employee experience is a product outcome. Internal tool quality correlates with staff retention. Measure tool NPS before assuming attrition is a compensation or headcount problem.

---

## ✅ COMPLIANT Example

### Context

Finance and Operations teams have 15% annual analyst attrition — above the 9% AA corporate average. HR is proposing a compensation adjustment. The Internal Productivity product team challenges this assumption.

### Evidence

**Exit interview analysis (n=28 analyst departures, last 12 months):**

| Exit Reason Cited | % of Departures |
|------------------|-----------------|
| Frustration with manual, repetitive work / poor tools | 43% |
| Compensation | 29% |
| Career growth / advancement | 18% |
| Other | 10% |

**Internal Tools NPS Survey (current staff, n=89 analysts, Q1 2026):**

| Tool Category | NPS Score | % Promoters | % Detractors |
|--------------|-----------|-------------|--------------|
| Report generation tools | −18 | 12% | 30% |
| Data entry workflows | −34 | 8% | 42% |
| Self-service portals | +12 | 31% | 19% |

**Attrition correlation finding:**
- Analysts who score internal tools ≤ 5/10 have 22% attrition rate (12-month trailing)
- Analysts who score internal tools ≥ 8/10 have 8% attrition rate (12-month trailing)
- Correlation coefficient: −0.61 (tool satisfaction vs. 12-month attrition probability)

### Retention Metric (North Star)

**Internal Tools NPS — quarterly survey across all analyst roles.**

### Investment Gate

Goal: reduce analyst attrition from 15% to ≤ 10% within 12 months of tool improvements.

**Gating logic:**
1. Q2 2026: Deploy headcount report automation + expense categorization automation (PRD-5.1 MVPs).
2. Q3 2026: Run internal tools NPS survey. Target: improve report generation NPS from −18 to ≥ 0.
3. Q4 2026: Measure 12-month rolling attrition. If ≤ 10%: tool quality was a primary driver; continue roadmap.
4. If attrition persists at > 12% after NPS improvement: re-evaluate compensation hypothesis.

### What This Prevents

Spending $450K on compensation adjustments for a problem that is 43% attributable to tool frustration, when tool automation can be delivered for $95–150K.

---

## ❌ VIOLATION Example

> "15% attrition is above benchmark. Approve Q3 compensation survey and adjustment budget."

**Why this violates PRD-6.2:**
- Compensation adjustment addresses 29% of the problem while ignoring the 43% tool frustration driver.
- No correlation analysis between tool satisfaction and attrition.
- Treating retention as an HR problem before investigating whether it is a product problem.
- Correct approach: run internal tools NPS, measure attrition-by-tool-satisfaction correlation, then decide on compensation vs. tool investment.
