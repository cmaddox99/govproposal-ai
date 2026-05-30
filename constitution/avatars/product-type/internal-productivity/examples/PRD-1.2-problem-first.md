---
law: PRD-1.2
avatar: avatar-product-internal-productivity
title: "Problem-First: Finance Expense Categorization Bottleneck"
---

# PRD-1.2 Problem-First — Internal Productivity

## Law Summary

Validate the specific workflow bottleneck before proposing a solution. "AI-powered" is a solution label, not a problem statement.

---

## ✅ COMPLIANT Example

### Stated Request

> "Finance wants an AI-powered expense categorization tool to automate month-end close."

### Research Conducted

6-week time audit across 5 Finance Analysts (Q4 month-end close, Jan 2026). Structured workflow observation + time-tracking spreadsheet completed by analysts.

| Activity | Avg Hours/Analyst/Month-End | % of Close Time |
|---------- |----------------------------|-----------------|
| Manual expense categorization (uncategorized transactions) | 18.4 hours | 40% |
| Reconciliation review | 8.2 hours | 18% |
| Report compilation (manual copy-paste from legacy systems) | 9.6 hours | 21% |
| Stakeholder communication | 5.8 hours | 13% |
| Other (meetings, approvals) | 3.7 hours | 8% |

**Volume:** 8,000–11,000 uncategorized transactions per month-end close. Analysts manually assign each to one of 42 GL account codes.

**Error rate:** 3.2% miscategorization rate on manual entries; requires correction in subsequent close cycle.

**Analyst verbatim:** "The categorization is the worst part. Most transactions follow obvious patterns — vendor name matches category 90% of the time. But I still have to touch every one of them."

### Validated Problem Statement

> Finance Analysts spend 40% of month-end close (avg 18.4 hours/analyst) manually categorizing 8,000–11,000 transactions into GL codes. 90% of these transactions follow vendor-name patterns that are automatable. The problem is **manual repetition of pattern-matching work**, not complex financial judgment. An AI-powered general assistant will not fix this — a rule-based or ML categorization engine targeting the 90% predictable transactions will.

### Correct Solution Direction

Automated GL categorization for high-confidence vendor-name patterns (≥ 90% historical accuracy), with analyst review queue for low-confidence and novel vendor transactions. Target: reduce manual categorization time by 70%.

---

## ❌ VIOLATION Example

> "Finance needs an AI productivity suite: expense categorization, budget variance analysis, FP&A report generation, and natural-language querying of financial data."

**Why this violates PRD-1.2:**
- Four solutions bundled before any single problem is validated.
- No time audit: what % of analyst time does each activity consume?
- "AI productivity suite" addresses everything and therefore prioritizes nothing.
- Correct first step: 6-week time audit to identify the single highest-impact bottleneck.
