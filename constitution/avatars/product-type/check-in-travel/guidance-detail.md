# Check-In & Boarding Guidance: Product Application of PRD Laws

## What We Do

American Airlines' Check-In & Boarding product streamlines how 1.7M passengers daily transition from booking to aircraft departure. Our mission:

- **Speed:** Get passengers boarded in 35 minutes (industry: 40-45 min)
- **Accessibility:** Enable every passenger to check in their way (digital, kiosk, counter)
- **Reliability:** 99.9% system uptime; zero passengers missing flights due to check-in failures
- **Efficiency:** Reduce gate-level manual work and operational delays
- **Delight:** Transform check-in from stressful to seamless

We serve four distinct personas with precision:

1. **Alex (Digital Traveler):** Frictionless mobile check-in; never touches an agent
2. **Maria (Supported Traveler):** Airport counter with human reassurance; special services
3. **Kevin (Gate Agent):** Real-time visibility; proactive workflow tools
4. **Patricia (Operations Manager):** Strategic oversight; predictive decision-making

---

## How to Apply Each PRD Law

> **Full PRD law definitions** are in the [PRD Laws Reference](../../../docs/guides/avatars/prd-laws-reference.md). This section shows check-in-specific applications.

### PRD-1.1: Continuous Discovery

**Reference:** [PRD-1.1 Full Definition](../../../docs/guides/avatars/prd-laws-reference.md#prd-11-continuous-discovery)

**Check-In Application:**

Every quarter, we discover new insights by:

1. **Passenger Research** (Quarterly)
   - Mobile: Why do 28% still not use it? What barriers remain?
   - Counter: What makes Maria choose human over self-serve?
   - Gate: What failures cause cascading boarding delays?

2. **Operational Observation** (Quarterly)
   - Shadow gate agents (Kevin): What manual tasks are still happening?
   - Observe operations center (Patricia): What alerts cause most reaction?
   - Monitor peak hours: 6-8am and 5-7pm reveal capacity constraints

3. **Competitive Benchmarking** (Biannual)
   - Southwest: 78% mobile adoption, 2% failure rate (Why ahead?)
   - United: Oversell alerts 30 min pre-departure (How implemented?)
   - Delta: Baggage integration with boarding (How reduces delays?)

4. **Data Analysis** (Continuous)
   - Which passengers don't complete mobile check-in? (Intent: retention)
   - Which flights have gate-level bottlenecks? (Intent: operational improvement)
   - Where do special services take extra time? (Intent: accessibility)

**Real Check-In Examples (2026):**

- **Discovery Insight:** "8% mobile failure rate is our #1 gate-level issue"
  - Method: Analyzed 1M boarding passes; 112K daily failures
  - Action: Built offline barcode support (MVP Q2 2026)
  - Result: 99.9% reliability achieved by Q4

- **Discovery Insight:** "Maria (25% of passengers) prefers counter but dreads long lines"
  - Method: Interviewed 100 Maria-type passengers at 5 hubs
  - Action: Implemented queue management + gate check-in options
  - Result: Peak wait reduced from 35 min → 14 min

- **Discovery Insight:** "Patricia reacts to oversell chaos; could she predict it?"
  - Method: Analyzed 500 flights; oversell occurs 2.5% of flights
  - Action: Built predictive oversell alerts 30 min pre-departure
  - Result: 74% volunteer rate; smooth boarding

---

### PRD-2.1: Journey Mapping

**Reference:** [PRD-2.1 Full Definition](../../../docs/guides/avatars/prd-laws-reference.md#prd-21-user-journey-mapping)

**Check-In Application:**

We map four distinct journeys:

**Journey 1: Alex (Digital Frictionless)**
- Intention: Get boarding pass, zero human contact
- Ideal Flow: Open app → Select flight (1 sec) → Confirm → Done (90 sec total)
- Friction Points: Mobile fails (app crash, offline barcode invalid, Wi-Fi fails)
- Emotional Journey: Confident → frustrated (if fails) → relieved (once done)
- Moments of Truth: Does app open on first try? Does barcode work at gate?

**Journey 2: Maria (Supported Traveler)**
- Intention: Check in with human help; feel reassured
- Ideal Flow: Arrives at counter → Wait (30 min) → Agent greets → Agent helps (8 min) → Boarding pass printed → Relieved
- Friction Points: Long wait, agent doesn't explain, bag weight surprises, special services scrambled
- Emotional Journey: Hopeful → impatient (waiting) → confused (check-in process) → reassured (agent helps) → proud (finished)
- Moments of Truth: Is there a long line? Is the agent nice? Does agent solve my problem?

**Journey 3: Kevin (Gate Agent Operational)**
- Intention: Board 180 passengers in 35 minutes; zero failures
- Ideal Flow: Receive passenger manifest → Validate passes → Scan at gate → Board → Move to next flight
- Friction Points: Invalid boarding passes (manual lookup 5-10 min each), oversell surprises, special services not flagged, seat chaos
- Emotional Journey: Prepared → stressed (invalid pass) → scattered (oversell discovered at gate) → relieved (all boarded)
- Moments of Truth: Do I have visibility 15 min before boarding? Does my dashboard work? Are there oversold passengers?

**Journey 4: Patricia (Operations Manager Strategic)**
- Intention: Maintain on-time performance (82% target), prevent cascading delays
- Ideal Flow: Monitor flights → Identify at-risk flights → Take preventative action → Flight departs on-time
- Friction Points: No early alerts, reactive learning from gate agents via radio, no data on delay causes
- Emotional Journey: Confident → anxious (if alert-less) → strategic (with predictive data) → satisfied (on-time achieved)
- Moments of Truth: Do I know oversell 30 min early? Can I pre-volunteer passengers? Are boarding delays reducing?

**Real Check-In Journey Mapping (2026 Q2):**

When designing mobile reliability improvements:
- Alex's current journey: Opens app (1s) → Sees boarding pass (2s) → Worried ("Is it offline safe?") → Screenshots as backup → Arrives gate (concerned) → Scans (2s) → Relieved
- Friction: Lack of trust in offline mode; no visibility into barcode validity
- Improvement: Added offline validation notice + 15-min pre-gate validation → Alex's journey becomes: Opens app → Sees "Valid offline" → Confident → No screenshot needed → Arrives gate → Scans → Relieved

**When to Use PRD-2.1:**

- You're redesigning a feature: Map current journey first, then show how redesign removes friction
- You're adding a new feature: Will it help the journey or add complexity?
- You're optimizing operations: Journey mapping reveals bottlenecks (Kevin's "invalid pass lookup" is #1 friction)
- Quarterly reviews: Has passenger journey improved? (Time, confidence, emotions)

**Pitfalls to Avoid:**

- Mapping only happy path: Oversell journey, mobile failure journey, accessibility journey = real friction
- Ignoring emotions: Alex doesn't care about tech; cares about "Do I feel confident my pass works?"
- Missing operational personas: Kevin and Patricia's journeys are as important as passengers'

---

### PRD-3.1: Roadmap Planning

**Reference:** [PRD-3.1 Full Definition](../../../docs/guides/avatars/prd-laws-reference.md#prd-31-roadmap-planning)

**Check-In Application:**

We apply the prioritization framework to Check-In roadmap decisions:

**Real Check-In Roadmap (2026):**

**Tier 1 (Start Q1, Deploy Q2):**

1. **Mobile Offline Barcode Support**
   - Member Impact: 85/100 (solves #1 reliability concern)
   - Business Value: 92/100 ($11M labor savings)
   - Effort: 35/100 (moderate engineering)
   - Score: 85×0.4 + 92×0.4 + 65×0.2 = 84 ✅ **TOP PRIORITY**

2. **Real-Time Gate Dashboard (Kevin)**
   - Member Impact: 78/100 (proactive vs. reactive)
   - Business Value: 88/100 (operational efficiency)
   - Effort: 42/100 (system integration required)
   - Score: 78×0.4 + 88×0.4 + 58×0.2 = 81 ✅ **HIGH PRIORITY**

3. **Kiosk UX Simplification (Maria)**
   - Member Impact: 82/100 (lowers "too complicated" barrier)
   - Business Value: 75/100 (diverts 20% to self-serve)
   - Effort: 38/100 (UX + frontend, not backend)
   - Score: 82×0.4 + 75×0.4 + 62×0.2 = 77 ✅ **MEDIUM-HIGH PRIORITY**

**Tier 2 (Start Q2, Deploy Q3):**

1. **Predictive Oversell Alerts (Patricia)**
   - Member Impact: 68/100 (improves passenger experience if needed)
   - Business Value: 72/100 ($1M+ volunteer cost savings)
   - Effort: 52/100 (ML model required)
   - Score: 68×0.4 + 72×0.4 + 48×0.2 = 67 ✅ **MEDIUM PRIORITY**

---

### PRD-4.1: MVP & Product-Market Fit

**Reference:** [PRD-4.1 Full Definition](../../../docs/guides/avatars/prd-laws-reference.md#prd-41-mvp--product-market-fit)

**Check-In Application:**

For every significant feature:

1. **Define MVP Scope** (1-2 weeks)
   - What's the core hypothesis? (e.g., "Offline barcode support drives adoption")
   - What's the minimum to test? (e.g., Offline barcode generation + validation at 3 gates)
   - Who are beta users? (e.g., Early adopter passengers at DEN hub)

2. **Build & Deploy to Beta** (2-4 weeks)
   - Scope small: 3 gates, 1000 passengers, 30 days
   - Instrument for measurement: Track success metrics in real-time
   - Ready to iterate: If doesn't work, learn why fast

3. **Validate with Real Data** (2-4 weeks)
   - Adoption rate: Do passengers use offline mode? (Target: 60%)
   - Success rate: Does offline barcode work at gate? (Target: 99%)
   - Satisfaction: Would passengers recommend? (Target: 8/10)
   - Go/no-go decision: Launch broad or iterate?

**Real Check-In MVP Examples (2026):**

**Mobile Offline Barcode MVP (Q2 2026):**
- Beta: 100K passengers, 30 days, 3 major hubs
- Validation: 60% adoption of offline mode, 99.1% success rate at gate ✅
- Go/no-go: **GO** → Broad launch with refinements

**Gate Operations Dashboard MVP (Q2 2026):**
- Beta: Kevin (gate agent) uses new dashboard for 50 flights
- Validation: <5 sec to find passenger info, 94% vs. 100% accuracy ✅
- Go/no-go: **GO** → System replaced paper manifest

**Kiosk UX Simplification MVP (Q2 2026):**
- Beta: 200 kiosks, new UX vs. old UX A/B tested
- Validation: Completion 60% → 76%, time 5.5 → 3.2 min ✅
- Go/no-go: **GO** → Kiosk rollout Q3

---

### PRD-5.1: Metrics & Success Definition

**Reference:** [PRD-5.1 Full Definition](../../../docs/guides/avatars/prd-laws-reference.md#prd-51-metrics--success-definition)

**Check-In Application:**

We track three tiers of metrics:

**Tier 1: Passenger Experience (Member Satisfaction)**

- Mobile adoption: Track % using app to check in (52% baseline → 72% target)
- Check-in completion rate: % who complete check-in without human help (65% baseline → 78% target)
- Boarding satisfaction: "Was boarding smooth?" (6/10 baseline → 8/10 target)
- Accessibility experience: Passengers with special needs satisfaction (68% baseline → 85% target)
- Check-in time (digital): Minutes from start to boarding pass (2 min target)
- Check-in time (counter): Minutes including wait + service (8 min target by Q4)

**Tier 2: Operational Efficiency**

- Boarding time: Minutes from first passenger to last (40 min baseline → 35 min target)
- On-time performance: % flights departing ≤15 min late (78% baseline → 82% target)
- Gate-level manual interventions: Manual lookups per flight (40 baseline → 8 target)
- Operational uptime: System availability (99.8% baseline → 99.9% target)
- Peak-hour capacity: Passengers checked in per hour during 6-8am (1400 baseline → 1700 target)

**Tier 3: Business Impact (Revenue & Cost)**

- Labor savings: Reduced manual gate work ($11M+ annual potential)
- On-time revenue: Reduced rebooking costs + satisfaction premium ($8M+ annual potential)
- Scalability cost: Cost per passenger check-in (tracking for efficiency)
- Operational resilience: Reduction in cascade delays from check-in issues ($2-5M annual)

**Real Check-In Metrics (2026 Q4 Results):**

| Metric | Q1 Baseline | Q4 Target | Q4 Actual | Status | Impact |
|--------|------------|-----------|-----------|--------|--------|
| Mobile adoption | 52% | 72% | 72% | ✅ Hit | +20% passengers self-serving |
| Boarding time | 40 min | 35 min | 35.2 min | ✅ Hit | $8M+ on-time improvement |
| On-time | 78% | 82% | 82.1% | ✅ Hit | Competitive parity with United/Delta |
| Gate manual work | 40/flight | 8/flight | 6/flight | ✅ Exceeded | $3.7M labor savings |
| Accessibility satisfaction | 68% | 85% | 85% | ✅ Hit | Inclusive design working |

**When to Use PRD-5.1:**

- Q1 planning: Define success metrics for the year
- Monthly reviews: Are we on track? Course-correct
- Feature MVPs: What metrics validate success?
- Quarterly reviews: Did we hit targets? Why/why not?

**Pitfalls to Avoid:**

- Too many metrics: Focus on 5-7 core metrics, not 50
- Vanity metrics: "Sessions" are nice, but "Mobile adoption 72% +" is more actionable
- Ignoring leading indicators: If gate-level work is high, on-time will suffer; act early

---

## Persona-Specific Guidance

### For Alex (Digital Traveler)

**Your World:**
- Seamless technology expected; any friction → frustration
- Reliable system > fancy features (offline barcode works > animation)
- Speed matters; you're always on-the-go
- Trust system first time; no screenshots needed

**How to Serve Alex:**

1. **Reliability > Features:** Invest in offline support, stress testing, crash reduction before new features
2. **Simplicity > Options:** 5-step flow > 15-step flow with every option
3. **Speed:** Mobile check-in <2 min; gate scan <5 sec
4. **Transparency:** Show boarding pass validity ("Valid offline" indicator) upfront

**Apply These Laws:**
- **PRD-1.1:** Research why 28% don't use digital; remove barriers
- **PRD-2.1:** Alex's journey = frictionless flow; identify every pause point
- **PRD-3.1:** Prioritize reliability features (offline support #1) over feature-rich options
- **PRD-4.1:** MVP with real users; validate offline barcode works before broad launch
- **PRD-5.1:** Track mobile adoption (52% → 72%), reliability (92% → 99.9%), satisfaction (7 → 9/10)

---

### For Maria (Supported Traveler)

**Your World:**
- Technology can be confusing; prefer human help
- Don't understand baggage rules, fees, special instructions
- Long lines cause anxiety; need clear expectations
- Feel respected, not rushed; agent's tone matters

**How to Serve Maria:**

1. **Accessibility Over Efficiency:** Plain English > jargon; large buttons > complex flows
2. **Transparency:** Show wait time estimate; explain baggage fees upfront
3. **Proactivity:** Alert counter agent to special services so they're ready
4. **Human Touch:** Agent greeting sets tone; "Let's make sure everything is right" vs. "Next!"

**Apply These Laws:**
- **PRD-1.1:** Interview Maria-type passengers; why prefer counter? What makes them anxious?
- **PRD-2.1:** Maria's counter journey includes 30-min wait; how to make it less stressful?
- **PRD-3.1:** Kiosk UX simplification (60% → 75% completion) and special services integration prioritized
- **PRD-4.1:** MVP kiosk redesign; test with real Maria-type users
- **PRD-5.1:** Counter check-in time 12 → 8 min, peak wait 35 → 14 min, satisfaction 6 → 8.5/10

---

### For Kevin (Gate Agent)

**Your World:**
- Responsible for on-time departures; stress when things go wrong
- Manual work (lookup, oversell management) detracts from leadership role
- Special services (wheelchair, medical) require extra care; want to be proactive
- Need real-time visibility; paper manifests are outdated

**How to Serve Kevin:**

1. **Proactivity:** Pre-gate validation eliminates manual lookups; 40 → 8 per flight
2. **Real-Time Visibility:** Dashboard shows passenger status, special services, oversell alerts
3. **Autonomy:** Kevin makes decisions (boarding sequence, special services timing) with good data
4. **Respect:** System removes busywork; Kevin becomes operational leader

**Apply These Laws:**
- **PRD-1.1:** Shadow Kevin during peak; observe every manual task; research pain points
- **PRD-2.1:** Kevin's journey = React to chaos → Proactive with visibility → Smooth boarding
- **PRD-3.1:** Gate dashboard (prioritized) + oversell alerts + pre-validation features
- **PRD-4.1:** MVP dashboard with 50 flights; validate Kevin can find info in <5 sec
- **PRD-5.1:** Track manual lookups (40 → 6/flight), satisfaction (5 → 8.5/10), stress reduction (8 → 4.5/10)

---

### For Patricia (Operations Manager)

**Your World:**
- Responsible for on-time performance (82% target)
- Reactive crisis management (oversell, delays) pulls you from strategic work
- Control room lacks real-time data; always 5-10 min behind
- Need predictive alerts to be proactive; need visibility to optimize

**How to Serve Patricia:**

1. **Predictive Data:** Oversell alerts 30 min early; on-time risk flagging
2. **Real-Time Visibility:** <5 min data lag; see which flights are at-risk
3. **Automation:** System handles routine decisions; Patricia focuses on exceptions
4. **ROI Tracking:** Measure impact of changes (oversell volunteer rate, on-time improvement, labor savings)

**Apply These Laws:**
- **PRD-1.1:** Analyze 500 flights; when do delays happen? What predictive signals exist?
- **PRD-2.1:** Patricia's journey = Reactive fire-fighting → Strategic decision-making
- **PRD-3.1:** Oversell alerts (30-min early), gate dashboard (real-time visibility), metrics tracking
- **PRD-4.1:** MVP oversell alerts with 600 flights; validate 98% accuracy
- **PRD-5.1:** Track on-time (78% → 82%), oversell volunteer rate (0% → 74%), decision time (5 → 1.5 min)

---

## Common Q&A

**Q: How do we balance speed (Alex) with accessibility (Maria)?**
A: Dual-track design. For digital: <2 min, minimal flow. For counter: Patient, clear, reassuring. Don't make kiosk as complex as mobile; instead, design both for their personas, not force both to same standard.

**Q: Offline barcode failed in our system; now what?**
A: PRD-1.1 in action: Research why it failed. User research: Did passengers trust it? Operational research: Did scanners read it reliably? Fix root cause, then MVP with small population again. Failure = learning opportunity.

**Q: Our on-time metric isn't improving; how do we find the bottleneck?**
A: PRD-1.1 + PRD-5.1. Analyze gate-level delays: Which flights? Which gates? Which times? Trace back: Is it check-in delays? Boarding delays? Oversell chaos? Once you find the #1 bottleneck, apply roadmap (PRD-3.1) to prioritize fixes.

**Q: How do we measure if a feature was worth building?**
A: PRD-5.1. Did offline barcode improve adoption? YES (52% → 72%). Did it improve reliability? YES (92% → 99.9%). Did it reduce gate-level work? YES (40 → 6 lookups/flight). If all three YES, feature was worth it.

**Q: Our agents don't like the new dashboard; what went wrong?**
A: PRD-4.1. MVP validation didn't include real agents in real conditions (peak time, stress). Next time: MVP includes Kevin for full shift during peak hour, not lab conditions.

**Q: Should we build biometric boarding in 2026 or wait for 2027?**
A: PRD-3.1 roadmap. Biometric scores 68/100 (lower than other Tier 1 features). Current Tier 1 hits higher ROI, lower effort. Biometric is strategic for 2027; right call to defer. Re-evaluate quarterly.

---

## Success Stories

**Story 1: Alex's Trust (2026 Q4)**

Alex hadn't used mobile check-in before (28% of passengers). Heard about "offline barcode support." Downloaded app in DEN terminal (curious, not trusting). Saw "Valid offline ✓" indicator on boarding pass. Felt confident. Didn't take screenshot. Gate agent scanned phone; worked immediately. Texted friend, "This is the way." Likely to use digital next trip. **Result:** Adoption up from 52% to 72%; reliability trust restored.

**Story 2: Maria's Counter Joy (2026 Q4)**

Maria arrived at DEN counter at 6:50am for 7:00am flight. Saw digital sign: "Counter wait 8 min; check in on kiosk in 2 min." Unsure of kiosk, but 8 min wait << online check-in confidence. Tried new simplified kiosk: Flight → Bags → Seat → Done (3 min). Surprised it worked. Next trip? Might try kiosk first. Counter agent had time to help Maria with baggage question (wasn't rushed). **Result:** Kiosk completion up; counter lines shorter; Maria satisfaction up.

**Story 3: Kevin's Transformation (2026 Q4)**

Kevin started shift stressed: "Hope no mobile failures today." New dashboard showed all 180 passengers pre-boarding; 2 flagged as "special services." Kevin alerted, prepared wheelchair space, ensured quiet boarding environment nearby. Mobile failure rate down 96% (no manual lookups). Oversell alert 30 min early; Patricia volunteered 4 passengers without drama. Boarding finished in 34 min (usually 40). Kevin went home feeling accomplished, not exhausted. **Result:** Kevin satisfaction up from 5 to 8.5/10; stress down from 8 to 4.5/10.

**Story 4: Patricia's Strategic Day (2026 Q4)**

Patricia started monitoring at 5:30am with new predictive alerts. By 6:00am, system flagged 3 flights at-risk of oversell. Patricia approved early volunteer offers; by 7:30am, all 3 flights solved without bumping passengers. Real-time visibility showed gate delays down 40%. Patricia spent afternoon analyzing why on-time improved (instead of firefighting). Recommended more of same. **Result:** On-time up from 78% to 82%; Patricia's role shifted from tactical to strategic.

---

## Next Steps for Check-In Teams

1. **Quarterly Research (PRD-1.1):** What's the #1 pain point passengers still face? What's changed in operations? What are competitors doing?

2. **Roadmap Planning (PRD-3.1):** Evaluate features using impact/value/effort framework. Align stakeholders (Alex, Maria, Kevin, Patricia perspectives).

3. **MVP Validation (PRD-4.1):** Before broad launch, test with 100-1000 real users. Measure adoption, success, satisfaction.

4. **Metrics Tracking (PRD-5.1):** Measure quarterly progress. Course-correct. Focus on 5-7 core KPIs, not vanity metrics.

5. **Journey Optimization (PRD-2.1):** Re-map journeys quarterly. Are passengers calmer? Is Kevin less stressed? Is Patricia more strategic? Optimize friction points.

---

## Summary

Check-In & Boarding is where passengers begin their journey with American Airlines. First impression matters. By applying PRD laws—discovery (understand pain), journey mapping (optimize flow), roadmap planning (prioritize high-impact features), MVP validation (test before broad launch), and metrics tracking (measure success)—we transform check-in from stressful to seamless.

**2026 Results:**
- Mobile adoption 52% → 72% (+38%)
- Boarding time 40 → 35.2 min (-4.8 min, 12% faster)
- On-time 78% → 82.1% (+4% strategic advantage)
- Gate operations: Manual work down 85% (40 → 6 lookups/flight)
- $13M+ annual operational savings

**2027 Vision:**
- Mobile adoption 72% → 85%+ (with biometric)
- Boarding time 35.2 → 32 min
- On-time 82% → 85%+
- Integration: Baggage + crew + loyalty in check-in workflow
- Total operational savings $20M+

The key: Listen to passengers. Understand operations. Prioritize ruthlessly. Test with real users. Measure obsessively. Repeat quarterly. That's how you build world-class check-in & boarding.
