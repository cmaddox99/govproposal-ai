# Example: AADvantage MVP & Product-Market Fit (PRD-4.1 MVP & PMF)

**Law Reference:** PRD-4.1: MVP & Product-Market Fit

**What This Example Shows:**
- How to define minimum viable loyalty features to test market fit
- What features go IN MVP and what stays OUT
- How to interpret feedback and decide on next phase

---

## Context: Why This Matters for Loyalty

AADvantage serves 100M+ members across casual, frequent, and elite tiers. Building full features for all tiers is expensive and slow. PRD-4.1 ensures we test hypotheses with small, targeted MVPs before committing to full rollout. Every major loyalty feature—progress tracker, personalized offers, gifting—starts as a scoped experiment with clear go/no-go criteria.

**Key Principles from PRD-4.1:**
- Define MVP scope (in/out features)
- Identify must-validate assumptions
- Choose early-adopter member segment
- Measure market fit signals before scaling

---

## MVP 1: Elite Progress Tracker

### MVP Scope: What's IN

1. **Live MQM Dashboard** — Real-time miles qualifying toward elite; updates within 24 hours of flight completion
2. **Monthly Forecast** — "At this pace, you'll reach Gold by September" based on trailing 90-day earning velocity
3. **Push Notifications** — Alert at 50%, 75%, and 90% milestones (one notification per milestone, not spammy)
4. **In-App Widget** — Dashboard tile: current tier, next tier, distance remaining; tap to expand for monthly breakdown

### MVP Scope: What's OUT (Phase 2+)
- Gamification (badges, streaks, challenges)
- Companion/family progress tracking
- Earning recommendations ("Fly DFW→LAX for 2x points")
- Partner earning integration (hotel, rental car)
- Social sharing or custom goal setting

**Core test:** Does visibility into progress change earning behavior? Each excluded item adds 3+ engineering weeks without validating the fundamental hypothesis.

---

### Success Metrics Table

| Criterion | Target | Actual (Beta) | Go? |
|-----------|--------|---------------|-----|
| Weekly active users | 40%+ | 48% | ✅ |
| Earning velocity change | +10%+ | +8% | ⚠️ |
| User satisfaction | 8/10+ | 8.4/10 | ✅ |
| "Would you miss this?" | 70%+ | 82% | ✅ |
| Support tickets | < 50 | 23 | ✅ |
| Elite achievement (projected) | +5% | +10% | ✅ |

**Decision: GO** → 5 of 6 criteria met. Earning velocity slightly below target but elite achievement projection exceeds goal. Launch broadly with refined messaging.

---

## When to Apply PRD-4.1 for Loyalty

✅ **Use this law when:**
- Launching any new member benefit (test with a segment before all 100M members)
- Changing tier structure or earning rules (validate with frequent travelers first)
- Adding a partner integration (test with a small partner set)
- Redesigning member experience (A/B test before full rollout)

❌ **Don't skip even if:**
- "Competitors already have this" — validate it works for AA members specifically
- "Executive wants it by Q2" — MVP is faster than full build + rework
- "We have 100M members" — a targeted segment produces cleaner signal

---

**Last Updated:** February 23, 2026
**Domain:** AADvantage Loyalty | **Law:** PRD-4.1: MVP & Product-Market Fit
