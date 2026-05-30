# PRD Laws Reference

> **Single Source of Truth for Product Laws (PRD-1.1 through PRD-5.1)**
> 
> This document is the canonical reference. Product-type avatars link to this file rather than duplicating.

---

## PRD-1.1: Continuous Discovery

### Definition
Continuously research customer needs, pain points, and unmet desires through interviews, observation, behavioral analysis, and competitive benchmarking.

### Why It Matters
Products succeed when they solve real problems, not guesses. Continuous discovery ensures you stay aligned with what customers actually need, not what you assume they need.

### When to Use
- **Quarterly Planning:** What changed? What new needs emerged? What are competitors doing?
- **Feature Conception:** Before building anything, validate the problem exists
- **Churn Analysis:** Why are customers leaving? What unmet needs caused it?
- **Roadmap Decisions:** Invest discovery first; let findings guide priorities

### How to Apply
1. **Interviews:** Talk to 20-50 customers. Ask open questions: "What's hard about X?" not "Do you want feature Y?"
2. **Observation:** Shadow customers in their environment. See what they struggle with.
3. **Behavioral Analysis:** Mine data. Who uses what features? When do they abandon? What's popular?
4. **Competitive Benchmarking:** What do competitors offer? Why might customers choose them?
5. **Exception Analysis:** Where do things go wrong? What patterns emerge?

### Success Signals
- Clear problem statement: "25% of customers abandon at step X because Y"
- Validated root cause: Interviewed 15+ customers; they all mentioned the same barrier
- Actionable insights: "If we remove friction at Y, we could reduce abandonment by Z%"

### Pitfalls to Avoid
- Building without research: "I think customers want..." ≠ "Customers told us..."
- One-time research: Discovery is continuous, not annual
- Ignoring operational perspectives: Frontline staff (gate agents, customer service) see patterns customers don't mention
- Confusing opinions with facts: "We think this feature is important" requires validation

### Real Examples
- **Loyalty:** Discovered casual members abandon redemption (62%) because too many options (12+ award flights shown). Solution: "Recommended for You" filtering. Result: redemption increased 45% → 62%
- **Check-In:** Discovered mobile check-in adoption stuck at 52% because passengers don't trust offline barcode. Solution: Added "Valid offline ✓" indicator + reliability improvements. Result: adoption 52% → 72%
- **Cargo:** Discovered freight forwarders need <15 second quotes because customers call with cargo ready to ship. If quote >30 sec, they call competitor. Solution: Quote engine optimization.

---

## PRD-2.1: User Journey Mapping

### Definition
End-to-end map of how customers interact with your product, from initial awareness through value realization, identifying friction points and emotional peaks/valleys.

### Why It Matters
Journey mapping reveals where customers drop off, get frustrated, or lose value. Small fixes at the right point unlock disproportionate improvements. It also reveals emotional journey, not just functional flow.

### When to Use
- **Feature Design:** Before building, map current journey; show how feature removes friction
- **Churn Analysis:** Where in journey do customers exit? Why?
- **Persona Validation:** Does journey differ for different personas? (Yes, usually)
- **Accessibility Design:** Which journey steps are hard for elderly, non-tech users, wheelchair users?

### How to Apply
1. **Define Journey Stages:** Typically: Awareness → Decision → First Use → Ongoing Use → Renewal Decision
2. **Map Functional Steps:** What does customer actually do at each stage?
3. **Identify Friction Points:** Where does customer slow down, abandon, or need help?
4. **Map Emotional Journey:** When do they feel confident? Frustrated? Delighted?
5. **Highlight Moments of Truth:** Which 2-3 decision points matter most?

### Success Signals
- Journey map shows both happy path and exception paths (errors, edge cases)
- Friction points are concrete: "At step 3, customer confused because X field unclear" (not "UX is bad")
- Emotional journey is specific: "At airport check-in, passenger anxious because worried about luggage" (not "customer stressed")
- Multiple journeys per product: Different personas have different paths

### Pitfalls to Avoid
- Mapping only happy path: Real customers face errors, exceptions, accessibility challenges
- Ignoring emotions: Technical flow is necessary but not sufficient
- Missing operational personas: For B2B or operational products, include frontline staff journeys (gate agents, customer service, managers)
- Assuming one journey fits all: Casual users journey differently than power users

### Real Examples
- **Loyalty (Sarah—Casual Member):** Enroll → Earn passively → Forget about points → Points expire → Frustrated, churn. Friction: Expiry notification missing. Solution: 90-day reminder. Emotional: Hopeful at enroll, forgotten during earning, frustrated at expiry.
- **Check-In (Alex—Digital Traveler):** Open app → Download boarding pass → Gate scan → Board. Friction: 8% mobile failures require gate recovery. Solution: Offline barcode support. Emotional: Confident (if works) or frustrated (if fails).
- **Check-In (Maria—Airport Prefer):** Arrive 3 hours early → Wait 30-45 min in line → Agent interaction (8 min) → Boarding pass → Relief. Friction: Long wait (anxiety), complex UX (confusion), surprise fees (frustration). Solution: Queue management, simplified counter process, pre-alerts.

---

## PRD-3.1: Roadmap Planning

### Definition
Prioritize features by impact (customer value + business value) and effort, creating quarterly deliverables aligned with strategic objectives.

### Why It Matters
Not all features are equal. Some delight customers but cost $5M; others solve critical problems cheaply. Roadmap planning forces trade-off decisions and ensures you build high-ROI features first.

### When to Use
- **Quarterly Planning:** Which features should we build this quarter?
- **Feature Requests:** New request comes in? Score it. Is it higher priority than current roadmap?
- **Resource Allocation:** "If we have 3 engineers, what 3 features deliver most value?"
- **Board/Executive Reviews:** "Why are we building X instead of Y?"

### How to Apply
**Prioritization Framework:**
- **Customer Impact** (40% weight): How much does this help the customer? Satisfaction gain, time saved, problem solved?
- **Business Value** (40% weight): Revenue growth, cost savings, retention improvement, acquisition lift?
- **Implementation Effort** (20% weight): Engineering hours, complexity, dependencies, risk?

**Scoring:** Rate each 0-100; calculate combined score = (Impact × 0.4) + (Business × 0.4) + ((100 - Effort) × 0.2)

**Typical Result:** Score 80+ = Tier 1 (prioritize now), 60-80 = Tier 2 (plan for Q2-Q3), <60 = Tier 3 (exploratory, strategic)

### Success Signals
- Roadmap reflects data, not HiPPO (Highest Paid Person's Opinion)
- Team understands why features are prioritized (transparent scoring)
- High-impact, low-effort features done first (quick wins)
- Tier 1 features are genuinely high-impact (not just novel or cool)

### Pitfalls to Avoid
- Scoring without data: Validate assumptions, don't guess
- Too much consensus: Some features are genuinely lower priority; own the trade-off decisions
- Ignoring strategic shifts: Roadmap should flex quarterly as market changes
- Missing operational requirements: Exclude bug fixes, technical debt, compliance requirements at peril

### Real Examples
- **Loyalty Tier 1 (Score 88-93):** Mobile redesign (adoption +20%), elite progress tracker (retention +10%), award seat expansion (acquisition lift)
- **Loyalty Tier 2 (Score 82-86):** Points gifting, concierge service, partner expansion
- **Loyalty Tier 3 (Score 62-75):** Points never expire (parity), gamification (nice-to-have), exclusive experiences
- **Check-In Tier 1 (Score 90+):** Mobile reliability (core blocker), gate dashboard (operational efficiency), accessibility redesign (legal + ethical)

---

## PRD-4.1: MVP & Product-Market Fit

### Definition
Build minimum viable product; test with real users; measure adoption, satisfaction, and business impact before broad deployment.

### Why It Matters
Big launches often miss the mark. MVPs validate assumptions quickly and cheaply. If MVP fails, you learn why before investing $1M+ on full release.

### When to Use
- **Before Broad Feature Launch:** Always MVP first (unless it's a small UI tweak)
- **Uncertain Adoption:** "Will customers actually use this?"
- **High Investment Required:** "Is this worth $2M engineering investment?"
- **New Market:** "Can we compete in this segment?"

### How to Apply
1. **Define MVP Scope** (1-2 weeks): Minimum to test core hypothesis. In: core feature. Out: nice-to-haves, polish, scale.
2. **Choose Beta Users** (Carefully): Early adopters, not mainstream users. High engagement, willingness to feedback.
3. **Set Success Criteria** (Clear): What metrics prove market fit? (Typical: 40%+ adoption, 8+/10 satisfaction, repeat usage 60%+)
4. **Build & Deploy** (2-4 weeks): Scope small; iterate fast.
5. **Measure Real Data** (2-4 weeks): Real users, real conditions, real feedback.
6. **Go/No-Go Decision** (Clear): Launch broad, iterate further, or pivot?

### Success Signals
- MVP completed in 2-4 weeks (not months)
- Beta includes 100-1000 real users
- Clear metrics defined upfront (not retroactively)
- Success criteria exceeded (or if not, you understand why and what to fix)

### Pitfalls to Avoid
- MVP too large: If you're building for 4 months, it's not MVP
- Not measuring: No data means gut-feel decisions; avoid this
- Ignoring negative signals: If adoption is 5% (target 40%), learn why before launch
- Wrong beta audience: Beta users are often different than mainstream; choose wisely

### Real Examples
- **Check-In Mobile MVP:** 100K passengers, 30 days, beta offline barcode support. Target: 60% adoption, 99% success rate. Actual: 60% adoption, 99.1% success. Decision: **LAUNCH BROADLY** with refinements.
- **Loyalty Elite Progress MVP:** 50K members beta dashboard. Target: 40% weekly active users. Actual: 48%. Decision: **LAUNCH** with messaging refinement.
- **Cargo Quote/Book MVP:** 3 forwarders, Feb 2026. Target: <15s quote, 80% completion. Actual: 13.8s, 83%. Decision: **EXPAND** to 10 customers; start API parallel.

---

## PRD-5.1: Metrics & Success Definition

### Definition
Define success metrics (KPIs) tied to business outcomes; measure continuously; course-correct quarterly.

### Why It Matters
Without metrics, you don't know if you're winning. Metrics force clarity on "success" and create accountability. Bad metrics optimize for the wrong thing (e.g., "sessions" vs. "member satisfaction").

### When to Use
- **Feature Planning:** What metrics prove this feature worked?
- **Quarterly Reviews:** Are we on track? Where should we invest next?
- **MVP Validation:** Did MVP hit targets?
- **Executive Reporting:** "How are we doing?" (Needs clear metrics, not opinions)

### How to Apply
**Three Tiers of Metrics:**

1. **Tier 1 (Member Satisfaction):** Most important; direct impact on customer
   - Examples: NPS, satisfaction rating, adoption rate, completion rate, time to complete, accessibility experience, recommendation intent
   - Frequency: Monthly or quarterly measurement
   - Target: Typically 8+ out of 10 or 70%+ adoption

2. **Tier 2 (Operational Efficiency):** How well does system run?
   - Examples: Uptime, latency, error rate, throughput, on-time performance, processing time
   - Frequency: Continuous or daily measurement
   - Target: Typically 99.9%+ uptime, <2s latency, <1% error

3. **Tier 3 (Business Impact):** Revenue, cost, ROI
   - Examples: Incremental revenue, labor savings, churn reduction, LTV, CAC, ROI
   - Frequency: Monthly, quarterly, annual measurement
   - Target: ROI 3x+ is considered successful

### Success Signals
- Metrics are leading indicators: You measure before it's too late to course-correct
- Metrics focus on outcomes (member satisfaction) not just activity (sessions)
- Ownership is clear: "Who owns this metric? Who's accountable?"
- Targets are achievable but ambitious: Not sandbagging, but realistic

### Pitfalls to Avoid
- Too many metrics: Focus on 5-7 core metrics, not 50
- Vanity metrics: "1M sessions" sounds great but doesn't tell you if members are happy
- No targets: Measuring without targets is just data; targets create accountability
- Ignoring Tier 2 (operational): Can't have happy members if system is down
- Ignoring Tier 3 (business): Can have happy members but still lose money (not sustainable)

### Real Examples
- **Loyalty Metrics (2026):**
  - Tier 1: NPS 6.2 → 7.5, redemption 45% → 65%, elite achievement 25% → 35%, LTV $650 → $750
  - Tier 2: System uptime 99.8% → 99.95%, booking error <1%
  - Tier 3: Incremental revenue $260M, LTV gain $250M, ROI 28.9x

- **Check-In Metrics (2026):**
  - Tier 1: Mobile adoption 52% → 72%, boarding satisfaction 6 → 8/10, accessibility experience 68% → 85%
  - Tier 2: Boarding time 40 → 35.2 min, on-time 78% → 82%, uptime 99.8% → 99.9%
  - Tier 3: Labor savings $11M, on-time revenue $8M, operational resilience $2-5M

---

## How to Use This Reference

### For Avatar Guidance Files
Link to this document instead of repeating law explanations:

```markdown
### PRD-1.1: Continuous Discovery
For detailed explanation, see [PRD-1.1 Reference](prd-laws-reference.md#prd-11-continuous-discovery)

For {{ product }} specifically:
- {{ Product-specific example }}
- {{ Product-specific when-to-use }}
```

### For Use-Case Files
Reference specific law sections and examples:

```markdown
## Phase 1: Discovery (PRD-1.1)
[See PRD-1.1 in reference](prd-laws-reference.md#prd-11-continuous-discovery)

For {{ use-case }} specifically:
- Research question: {{ What are we investigating? }}
- Findings: {{ What did we learn? }}
```

### For Templates
Templates link to this reference, then show pattern:

```markdown
# Use Case Template
Each use case follows PRD-1.1 through PRD-5.1 pattern. See [PRD-LAWS-REFERENCE](PRD-LAWS-REFERENCE.md)

## Phase 1: Discovery (PRD-1.1)
[ Follow pattern from reference ]
```

---

## Version History

| Date | Changes |
|------|---------|
| Feb 20, 2026 | Created canonical PRD laws reference to eliminate duplication across guidance files |

