# PRD-1.1: Continuous Discovery — Check-In & Boarding

> **Law:** PRD-1.1 Continuous Discovery Law  
> **Findings detail:** `PRD-1.1-discovery-findings.md`

---

## Research Summary (450 participants — passengers, gate agents, ops managers)

| Method | Sample | Key output |
|--------|--------|-----------|
| Digital traveller interviews | N=200 | Trust gap: 8% mobile failure rate driving screenshot backups |
| Airport traveller observation | N=150 | Maria arrives 3h early to compensate for UX confusion |
| Accessibility passenger interviews | N=100 | 2× processing time vs. standard (12 min vs. 6 min) |
| Gate agent shift observation | N=25 (3 hubs) | 40 manual lookups/flight × 5-10 min each = 300 min/flight |
| Operations data | 1.7M passengers, 30 days | Boarding 40 min; on-time 78%; mobile failure 8% |

---

## Five Strategic Findings

1. **Mobile reliability is broken** — 8% failure rate (industry peers: 2-3%). Root causes: app crashes, offline barcode invalid, scanner incompatibility, auth timeout.
2. **Accessibility takes 2× time** — 5% of passengers (85K/day) face 12 min processing vs. 6 min standard. Not a volume problem — a design problem.
3. **Gate agents operate blind** — No real-time check-in status. Kevin discovers oversells and accessibility needs at the gate, not 30 minutes before.
4. **Systems are siloed** — Baggage, loyalty, special services, boarding pass: four separate systems. Passengers see fragmentation; agents waste time bridging them.
5. **Peak hours break everything** — 6–8am and 5–7pm = 65% of daily passengers. System throughput drops 25% in these windows.

---

## Strategic Recommendations

**Quick wins (≤60 days):** Mobile barcode pre-validation, accessibility flags on gate manifest, peak-hour staffing +25%, boarding push notifications.  
**Medium term (6 months):** Offline barcode resilience, real-time gate ops dashboard, kiosk accessibility redesign.  
**Long term (12 months):** Predictive oversell, biometric boarding pilot, peak-hour architecture scaling.

---

## 2026 Targets (from this discovery)

| Metric | Baseline | Target |
|--------|----------|--------|
| Mobile reliability | 92% | 99.5% |
| Accessibility processing time | 12 min | 6 min |
| Boarding time | 40 min | 35 min |
| On-time performance | 78% | 82% |

---

## Discovery-Driven Feature Flags (checkin-ios)

Two feature toggles in `checkin-ios/Sources/Relevance/` reflect discoveries from this research cycle:

- **`AAFeatureTSATouchlessID`** — gates the TSA Touchless ID / biometric boarding programme. Activated after discovery confirmed passenger willingness and TSA pilot feasibility; toggle allows route-level rollout without full release.
- **`AAFeatureFlyCheckinModernization`** — gates the modernised check-in flow (new step sequencing, offline barcode, pre-gate validation). Discovery finding: 35% complexity barrier → redesign justified; toggle enables A/B comparison against legacy flow.

Both flags live in `FeatureToggles.swift` alongside `AAFeatureCheckInEligible`, which controls check-in window availability. These flags are the direct implementation signal that PRD-1.1 discovery outputs are shaping live product decisions.

