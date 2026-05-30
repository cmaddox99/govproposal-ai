---
laws: [PRD-6.2]
avatar: [gate-management]
title: Retention Over Acquisition — Gate Management Platform
---

# PRD-6.2: Retention Over Acquisition

**Law Reference:** PRD-6.2: Retention Over Acquisition
**Avatar:** gate-management

Gate management serves **internal airline operations users** — gate agents, ramp crew, flight load controllers, and station managers — not consumers. PRD-6.2 applied to this context means: prioritize making existing gate agent workflows faster, more reliable, and less error-prone over adding new touchpoints or expanding to new user groups. Agent workflow adoption and satisfaction are the retention metrics, not consumer churn.

---

## Interpreting PRD-6.2 for Internal Ops Products

In consumer products, "retention" means returning users and reduced churn. For gate management:

| Consumer Context | Gate Management Equivalent |
|-----------------|---------------------------|
| DAU / MAU retention | Gate agent daily active usage (all agents use the tool = 100% is the floor, not the goal) |
| Churn rate | Agent workaround rate — how often do agents bypass the system to use paper, phone calls, or manual DCS entries? |
| Re-engagement | Agents voluntarily recommending the platform to peers at other stations |
| Feature adoption | Adoption of new digital signage or Connect Me features by station ops managers |
| NPS | Gate Agent Satisfaction Score (quarterly survey, target ≥ 65) |

---

## Retention Signals for Gate Management

```
High retention signals (positive):
  ✅ Gate agents complete boarding close without calling OCC (ops control center)
  ✅ IROP gate change handled end-to-end in Connect Me — no parallel phone coordination
  ✅ Biometric boarding replaces manual document check without agent assistance
  ✅ Carry-on override rate declining (agents trust system policy decisions)
  ✅ Zero DCS manual entry workarounds for display-related gate assignments

Low retention signals (risk indicators):
  ❌ Agents printing backup boarding lists "just in case" DSS goes down
  ❌ Station manager maintains separate spreadsheet for gate assignments
  ❌ Agents calling OCC for status that Connect Me should deliver
  ❌ Biometric kiosk lines causing agents to wave passengers through manually
```

---

## PRD-6.2 Compliant Prioritization

**Prioritize (retention):**
- Reduce DSS display refresh latency from 340 ms → < 200 ms (agents distrust slow displays)
- Improve Connect Me IROP delivery reliability from 94% → 99.5% (agents fall back to phone when unreliable)
- Reduce biometric false rejection rate (agents intervene manually, creating lines and frustration)
- Simplify gate agent carry-on override workflow (currently 7 taps → target 3 taps)

**Deprioritize (acquisition over retention — requires strong evidence):**
- Extend Connect Me to lounge staff before gate agent reliability is solved
- Add passenger-facing gate change notifications before agent notification is reliable
- Expand to new airport stations before DFW/CLT/MIA agents are fully satisfied

---

## PRD-6.2 Decision Gate

Before adding a new gate management capability or expanding to a new user group, answer:

1. **Current agent satisfaction:** Is Gate Agent Satisfaction Score ≥ 65 for existing workflows?
2. **Workaround rate:** Is agent workaround rate for existing features < 5%?
3. **Reliability floor:** Is the relevant service (DSS / Connect Me / Biometrics) at ≥ 99.5% uptime?

If any answer is NO → fix the existing experience before expanding scope (PRD-6.2).

---

## Example: Rejecting a New-Acquisition Feature (PRD-6.2 Applied)

**Proposal:** Add passenger-facing mobile push notifications for gate changes (new user group: passengers)

**PRD-6.2 Analysis:**
- Gate agent Connect Me delivery reliability: 94% (below 99.5% floor)
- Gate agent workaround rate for IROP coordination: 18% (above 5% threshold)
- Gate Agent Satisfaction Score: 58 (below 65 target)

**Decision:** PRD-6.2 requires resolving agent reliability and satisfaction gaps before expanding to passenger-facing notifications. Roadmap item deferred until agent retention metrics meet thresholds.
