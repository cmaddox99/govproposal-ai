# PRD-1.1: Continuous Discovery — Schedule Change Self-Serve

**Law Reference:** [PRD-1.1: Continuous Discovery](../../../../laws/product/discovery.md)  
**Avatar:** schedule-change-self-serve  
**Status:** Experimental — baselines require validation with real team and passenger data

---

## Applying PRD-1.1 to Schedule Change

Continuous discovery for Schedule Change focuses on three signal sources:

1. **Passenger abandonment signals** — why do eligible passengers still fail to complete a change?
2. **Agent override patterns** — what ineligible scenarios do agents override most, and why?
3. **Competitor UX benchmarks** — how does AA self-serve change compare to United, Delta, Southwest?

---

## Discovery Method Mix

| Method | Signal | Frequency | Owner |
|--------|--------|-----------|-------|
| BFF log analysis | Abandonment rate, error code frequency, latency outliers | Weekly | Engineering |
| Passenger intercept interview (5+) | Reason code clarity, intent at abandonment | Per sprint | UX Research |
| Agent observational session (1-2) | Override frequency, root cause, console friction | Per quarter | Product |
| Competitor UX audit | Change flow benchmark, time-to-confirm, reason clarity | Quarterly | Product |
| Support ticket tagging | Repeat ineligibility complaints, most cited confusion topics | Bi-weekly | Support + Product |

---

## Key Discovery Questions

**For passengers:**
1. Why did you abandon the change flow? What would have helped you complete it?
2. When blocked, did you understand the reason? What did you do next?
3. How does AA's change experience compare to other airlines you use?

**For agents:**
1. What are the top 5 scenarios where passengers ask you to override an ineligibility?
2. Do you have context on why the change was blocked? Or do you investigate from scratch?
3. What information in the console would reduce your investigation time?

**For compliance review:**
1. Are current audit logs sufficient to reconstruct a change decision chain?
2. What override fields are missing that regulators have asked about?

---

## Evidence Template (PRD-2.1)

```
Discovery Sprint: [Sprint ID]

Passenger signal:
- Interviews: [N] conducted, key themes: [...]
- BFF abandonment rate this period: [X]%
- Top 3 error codes by frequency: [...]

Agent signal:
- Override requests observed: [N per shift]
- Most common override reason: [...]
- Console friction point observed: [...]

Competitive signal:
- United change flow: [time to confirm, steps, reason clarity]
- Delta change flow: [time to confirm, steps, reason clarity]
- Southwest change flow: [time to confirm, steps, reason clarity]

Validation status: [ ] Not started  [ ] In progress  [✓] Validated  [ ] Invalidated
```

---

## Experimental Baselines (Replace with Measured Data)

| Signal | Experimental Estimate | Source |
|--------|-----------------------|--------|
| Passenger abandonment rate on ineligible change | 65% (est.) | Architecture constraint + peer benchmark |
| Agent override requests per 1k change attempts | 18 (est.) | BFF error log extrapolation |
| Avg. time to abandon (ineligible flow) | 90 sec (est.) | Peer benchmark |
| Reason code clarity score (passenger self-report) | 2.8/5 (est.) | Team intuition |
