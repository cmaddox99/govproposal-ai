# PRD-5.1: Metrics Detail — Operations + Business Impact KPIs
# Companion to PRD-5.1-metrics.md | Laws: PRD-5.1, BUS-7.1

---

## Measurement Ownership Model

Every KPI has one named team. No shared ownership.

| KPI owner | Metrics they own |
|-----------|-----------------|
| Mobile product team | Mobile adoption, mobile reliability, kiosk completion |
| Gate operations | Boarding time, manual lookups/flight, gate agent satisfaction |
| Accessibility team | Accessibility processing time, accessibility NPS |
| Operations (Patricia's team) | On-time performance, system availability, labour hours/1K pax |
| Finance | Gate recovery labour cost, missed flight rebooking cost, ROI |

---

## Dashboard Architecture

**Real-time (refreshes every 60 sec):**
- Active boarding times per gate vs. 35-min target
- Mobile pass failures in last 60 min
- Active oversell situations with volunteer count

**Daily (end-of-day report):**
- All Tier 1 + Tier 2 KPIs with delta vs. prior week
- Gate agent satisfaction pulse (sampled 10% of shifts)
- System availability by component

**Weekly executive review:**
- On-time trend vs. 82% target
- Tier 3 business impact (labour costs, rebooking costs, ROI)
- Top 3 incident root causes with fix ETA

---

## 2026 Full-Year Targets

| Metric | Q1 | Q2 | Q3 | Q4 |
|--------|----|----|----|----|
| Mobile reliability | 94% | 97% | 99% | 99.9% |
| Boarding time | 39 min | 37 min | 36 min | 35 min |
| On-time performance | 79% | 80% | 81% | 82% |
| Mobile adoption | 56% | 62% | 68% | 72% |
| Accessibility processing | 10 min | 8 min | 7 min | 6 min |
| Gate agent satisfaction | 6/10 | 7/10 | 8/10 | 8/10 |

---

## Cascade Alert Rules (BUS-7.1 Audit Trail)

Every metric alert must be logged with: timestamp, metric name, value at trigger, threshold breached, notified owner, resolution time, and root cause. No alert closes without a root-cause entry.

**Alert thresholds:**
- Boarding time >40 min on any gate → immediate SMS to Patricia
- Mobile failure rate >2% in any 1-hour window → mobile team paged
- On-time <76% for any 2-hour window → ops director notified
- Accessibility processing time >15 min → accessibility team + ops manager

---

## Counter-Metrics (What Not to Celebrate)

| Metric that looks good | Why it can mislead |
|-----------------------|-------------------|
| "Kiosk usage up 20%" | Only valid if completion rate also rose — raw usage can rise while more passengers fail |
| "Counter volume down 15%" | Could mean passengers gave up and didn't check in at all |
| "Mobile adoption up to 70%" | Means nothing if mobile reliability is still 8% failure — more adoption + same failure = more absolute failures |

Measure outcomes (did the passenger board successfully?) not activities (did the passenger touch the app?).
