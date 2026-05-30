# PRD-3.1: Roadmap Planning — Check-In & Boarding

> **Law:** PRD-3.1 Roadmap Planning Law  
> **Detail file:** `PRD-3.1-roadmap-detail.md` (Tier 2+3, investment table, scoring methodology)

---

## Prioritisation Framework

**Score = Passenger Impact (40%) + Operational Impact (40%) + Effort (20% inverse)**

---

## Tier 1 — Q1 2026 (Score ≥80)

### 1.1 Mobile Boarding Pass Reliability (Score: 94)
**Problem:** 8% failure rate → 112K daily gate recoveries → 560K-1.1M labour hours/year  
**Solution:** Offline barcode, pre-gate validation 15 min before boarding, instant kiosk backup, scanner QR format upgrade  
**Value:** $11.2M labour savings, +2-3% on-time improvement  
**Effort:** 120 eng days

### 1.2 Real-Time Gate Ops Dashboard (Score: 88)
**Problem:** Kevin operates blind — no check-in status, no oversell prediction, no accessibility pre-awareness  
**Solution:** Mobile tablet at gate: checked-in status, standby queue, accessibility flags, real-time boarding count, exception alerts  
**Value:** Boarding 40→35 min; $1.7M/year; +3-4% on-time  
**Effort:** 90 eng days

### 1.3 Accessibility-First Redesign (Score: 90)
**Problem:** 5% of passengers (85K/day) take 2× processing time; kiosk not usable without sighted assistance  
**Solution:** Kiosk large text + audio, VoiceOver in app, accessibility manifest flags, fast-track boarding process  
**Value:** $31M/year labour savings; accessibility satisfaction 68%→85%  
**Effort:** 100 eng days

---

## Tier 1 Timeline

| Feature | Start | Launch | Dependencies |
|---------|-------|--------|--------------|
| Mobile Reliability | Q1 | Q2 | App framework upgrade, barcode format change |
| Gate Ops Dashboard | Q1 | Q2 | Device procurement, backend APIs |
| Accessibility Redesign | Q1 | Q2-Q3 | UX testing with accessibility community, kiosk firmware |

---

## 2026 Success Targets (all Tier 1)

| Metric | Now | Q4 Target |
|--------|-----|-----------|
| Mobile reliability | 92% | 99.9% |
| Boarding time | 40 min | 35 min |
| On-time performance | 78% | 82% |
| Accessibility processing time | 12 min | 6 min |
| Gate agent satisfaction | 5/10 | 8/10 |

**Total 2026 investment:** $9.1M · **Expected annual return:** $44M+ · **ROI: 4.8×**

