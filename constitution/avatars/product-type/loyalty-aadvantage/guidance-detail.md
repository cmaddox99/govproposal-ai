# AADvantage Loyalty Product Guidance

## What We Do

AADvantage is American Airlines' global loyalty program rewarding members for flying American Airlines and our partners. With 180M+ enrolled members, we drive incremental revenue, improve customer lifetime value, and create emotional connection through:

- **Points Earning:** Every flight earns points; elite members earn faster
- **Elite Status:** Gold/Platinum progression with exclusive benefits (upgrades, lounge, perks)
- **Redemption:** Use points for free flights, upgrades, hotel stays, experiences
- **Partnerships:** Earn/redeem with 15+ hotel partners, credit card, shopping, dining
- **Recognition:** Personalized benefits and concierge service for top members

**Business Model:** We make money through:
1. Member lifetime value growth (fly more, earn more lifetime value)
2. Upselling premium redemptions (business class, suite hotels)
3. Partner revenue sharing (credit card, shopping portal, hotel partnerships)
4. Incremental revenue per member from better retention

---

## Product Laws & How They Apply

> **Full PRD law definitions** are in the [PRD Laws Reference](../../../docs/guides/avatars/prd-laws-reference.md). This section shows loyalty-specific applications.

### PRD-1.1: Continuous Discovery

**Reference:** [PRD-1.1 Full Definition](../../../docs/guides/avatars/prd-laws-reference.md#prd-11-continuous-discovery)

**How AADvantage Uses It:**

- **Research Methods:**
  - Annual member surveys (satisfaction, needs, competitive comparison)
  - Quarterly interviews with churned members ("Why did you leave?")
  - Behavioral analysis (who redeems? when? what's popular?)
  - Competitive benchmarking (United, Delta, Southwest, JetBlue features & benefits)

- **Example Questions:**
  - "Why do casual members abandon redemption 62% of the time?"
  - "What would make elite members feel more valued?"
  - "How do we compare to United MileagePlus on award availability?"

**Real AADvantage Example:**
> Research found casual members don't redeem because they can't find their routes (12 options shown, no recommendations). We built "Recommended for You" matching member preferences with available awards. Redemption completion rate increased 45% → 62%.

---

### PRD-2.1: User Journey Mapping

**Reference:** [PRD-2.1 Full Definition](../../../docs/guides/avatars/prd-laws-reference.md#prd-21-user-journey-mapping)

**How AADvantage Uses It:**

- **Core Journeys Mapped:**
  1. Casual Member: Enroll → Earn passively → Annual redemption → Churn risk
  2. Frequent Traveler: Join → Strategic earning → Track elite progress → Achievement → Maintain → Retention decision
  3. Elite Member: Achieve platinum → Use exclusive benefits → Renewal decision → Advocacy or switch

- **Friction Points Identified:**
  - Sarah (Casual): "Points expire but I don't remember them" → Solution: Expiry warning 90 days out
  - Marcus (Frequent): "I don't know how close I am to elite" → Solution: Real-time progress tracker
  - Jennifer (Elite): "Lounge quality has declined" → Solution: Reserve favorite seat in app pre-flight

**Real AADvantage Example:**
> Journey mapping revealed frequent travelers abandon elite pursuit at Month 7 (don't realize they're 30% toward goal). Adding a progress tracker at Month 7 increased elite achievement from 25% to 35%.

---

### PRD-3.1: Roadmap Planning

**Reference:** [PRD-3.1 Full Definition](../../../docs/guides/avatars/prd-laws-reference.md#prd-31-roadmap-planning)

**How AADvantage Uses It:**

- **Prioritization Framework:** Impact (40%) + Business Value (40%) + Effort (20%)

- **Tier 1 Features (Start Immediately):**
  - Mobile app redesign (score 88): Improve redemption conversion 45% → 65%
  - Award seat expansion (score 88): 2 seats/flight → 10 seats; membership attraction
  - Real-time elite tracking (score 93): Live progress toward gold/platinum

- **Tier 2 Features (Start Q2-Q3):**
  - Points gifting (score 83): Give points to family; increase member LTV
  - Elite concierge (score 86): Dedicated support for platinum; retention
  - Partner expansion (score 82): 12 partners → 25; diversify earning

- **Tier 3 Features (Start Q4+):**
  - Points never expire (score 75): Competitive parity
  - Exclusive experiences (score 68): Events, partnerships, emotional connection

**Real AADvantage Example:**
> Roadmap scoring showed elite progress tracker (score 93) delivers more ROI than gamification (score 62) despite gamification being "cool." We chose progress tracker; 35% of frequent travelers achieved elite status (vs. 25% baseline).

---

### PRD-4.1: MVP & Product-Market Fit

**Reference:** [PRD-4.1 Full Definition](../../../docs/guides/avatars/prd-laws-reference.md#prd-41-mvp--product-market-fit)

**How AADvantage Uses It:**

- **MVP Examples:**
  1. Elite Progress Tracker MVP: Live MQM dashboard for 50K beta users
     - Measure: Weekly active users (target 40%, actual 48%)
     - Measure: Earning velocity (target +10%, actual +8%)
     - Decision: Launch broadly; messaging refinement needed
  
  2. In-Flight Signup MVP: Offer enrollment on 50 flights
     - Measure: Signup rate (target 5%, actual 6.2%)
     - Measure: Post-flight engagement (60% active within 30 days)
     - Decision: Expand to 500 flights; simplify password step
  
  3. Personalized Offers MVP: 200K frequent travelers get travel-based offers
     - Measure: Redemption rate (target 25%, actual 28%)
     - Measure: Incremental spend (target $45/member, actual $45)
     - Decision: Launch broadly; travel-based > seasonal > upgrade-based

- **Success Criteria:** Member satisfaction, engagement rate, incremental business value

**Real AADvantage Example:**
> We MVP'd "points gifting" with 5K elite members. Found 64% wanted to gift, 35% actually did after launch. Real adoption was 35% not 64%; we scaled conservatively, adjusting messaging and incentives.

---

### PRD-5.1: Metrics & Success Definition

**What:** Define what success looks like (KPIs), measure monthly, review quarterly, make decisions based on data

**Why:** Without metrics, you can't tell if features work or if you're moving toward goals. Metrics drive accountability and continuous improvement.

**How AADvantage Uses It:**

- **Tier 1: Member Satisfaction** (How happy are our members?)
  - NPS: 6.2/10 target 7.5/10 (50% weighting)
  - Redemption rate: 45% target 65% (20% weighting)
  - Elite advancement: 25% target 35% (20% weighting)
  - Activation rate: 55% target 70% (10% weighting)

- **Tier 2: Program Health** (Is it operating well?)
  - Award seat availability: 2.1 seats/flight target 10/flight
  - Churn rate: 8-15% target 6-10%
  - Customer service cost: $8.50/inquiry target $6.50
  - Points earning rate: 1.2 points/$ target 1.5 points/$

- **Tier 3: Business Impact** (Are we making money?)
  - Member LTV: $650 target $750
  - Acquisition cost: $22 target $10
  - Contribution margin: 45% target 50%
  - Incremental revenue: $0 baseline target $60M+ annually

- **Who Needs This:** Everyone; PMs track features, executives track KPIs, customer insight tracks satisfaction
- **When to Use:** Monthly check-ins, quarterly reviews, feature ROI calculations, strategic planning
- **Example Questions:**
  - "Is our NPS improving? Which segment moved?"
  - "Did the elite concierge feature hit its ROI target?"
  - "Are we on track for $750 member LTV this year?"
  - "Which feature drives most member satisfaction improvement?"

**Real AADvantage Example:**
> Metrics showed points gifting driving +7K new members/month (acquired at $2/member vs. $22 elsewhere). We prioritized gifting; now 40% of new members come via referral from existing elite members gifting points.

---

## When to Apply Each Law

### For Sarah (Casual Member)

| Goal | Which Law | Example |
|------|-----------|---------|
| Why doesn't she redeem? | PRD-1.1 Discovery | Survey: "I can't find my routes" → Build recommendation engine |
| What's her experience? | PRD-2.1 Journey | Map: Enroll → Earn → Forget → Annual redemption | Friction: Doesn't know balance |
| How do we increase her redemption? | PRD-3.1 Roadmap | Score features: Quick-redeem buttons (80+), gamification (62) → Choose quick-redeem |
| Will quick-redeem work? | PRD-4.1 MVP | MVP: 50K users get feature; measure 28% vs. baseline 22% → Yes, scale |
| Is it working at scale? | PRD-5.1 Metrics | Monitor: Redemption rate 45% → 62%; Cost per redemption: $0.50 → $0.30 |

### For Marcus (Frequent Traveler)

| Goal | Which Law | Example |
|------|-----------|---------|
| Why doesn't he reach elite? | PRD-1.1 Discovery | Interview: "I don't know how close I am" → Build progress tracker |
| What does his path look like? | PRD-2.1 Journey | Map: Earn → Month-7 (30% toward gold) → Wonders if worth it → Maybe abandon |
| How do we get more to elite? | PRD-3.1 Roadmap | Score: Elite tracker (93), partner earning (82), gamification (62) → Choose tracker |
| Will tracker work? | PRD-4.1 MVP | MVP: 50K frequent travelers; measure 48% weekly engagement vs. target 40% → Yes, launch |
| How many reach elite? | PRD-5.1 Metrics | Elite achievement: 25% → 32%; +7% = +210K elite members × $500 LTV = $105M value |

### For Jennifer (Elite Member)

| Goal | Which Law | Example |
|------|-----------|---------|
| Why might she churn? | PRD-1.1 Discovery | Interview: "I don't feel valued; lounge experience declining" |
| What's her retention risk? | PRD-2.1 Journey | Map: Year-4 renewal → Evaluates investment → Considers United → Possible switch |
| How do we keep her? | PRD-3.1 Roadmap | Score: Concierge (86), value recognition (82), exclusive experiences (78) → Prioritize all 3 |
| Will concierge work? | PRD-4.1 MVP | Pilot: 50 platinum; measure 100% retention + 9.2/10 NPS vs. 82% retention baseline → Yes |
| Is she more satisfied? | PRD-5.1 Metrics | NPS: Elite 8.2 → 8.9; Retention: 82% → 92%; LTV: $2,200 → $2,800 |

### For Diana (Program Manager)

| Goal | Which Law | Example |
|------|-----------|---------|
| What should we build this year? | PRD-1.1 Discovery | Research: Churn causes, competitive analysis, member surveys |
| What are the opportunities? | PRD-2.1 Journey | Map all 3 journeys; identify biggest friction points |
| What's the priority order? | PRD-3.1 Roadmap | Score 20 ideas; select top 6 by ROI; build roadmap |
| Which features actually work? | PRD-4.1 MVP | MVP top 3 priorities; measure real member response; iterate |
| Are we hitting targets? | PRD-5.1 Metrics | Monthly dashboard: NPS, LTV, churn, acquisition, margin |

---

## Common Questions

**Q: Should I skip discovery and go straight to building features?**
A: No. Discovery prevents building features nobody wants. 2-week discovery saves 3-month feature that doesn't drive impact.

**Q: Can I build all features at once?**
A: Not if you want to succeed. Roadmap scoring forces prioritization. Build Tier-1 features; measure impact; then build Tier-2.

**Q: Do metrics ever show a feature should be killed?**
A: Yes. Elite concierge pilot had great NPS (9.2) but negative ROI initially (-$520/member). We scaled model (500 → 2,000 members) to achieve profitability. If metrics showed it still doesn't work, we'd pause.

**Q: What if member feedback contradicts metrics?**
A: Investigate. Qualitative (member feedback) + quantitative (metrics) both needed. If members love feature but metrics show no behavior change, dig deeper on why they don't use it.

**Q: How often should we research/reevaluate?**
A: Continuously. Quarterly deep research cycles + monthly metric reviews. Markets change; stay current.

**Q: Are all 5 laws required for every feature?**
A: No. Quick features (e.g., notification copy) need PRD-4.1 (MVP) + PRD-5.1 (metrics). Major features need all 5.

**Q: What if we disagree on prioritization?**
A: Use PRD-3.1 scoring framework. Forces objective decision-making. If scores are close, default to member impact.

---

## AADvantage Success Stories

### Story 1: The Casual Member Redemption Crisis → Solved

**Problem:** 62% of casual members abandoned redemption mid-flow. Lost $40M/year in unredeemed points.

**Law Application:**
- PRD-1.1: Researched; found 12 search options overwhelming ("Don't know which flight is best")
- PRD-2.1: Mapped friction: Search → Indecision → Abandon
- PRD-3.1: Built "Recommended for You" search (scored 82; high impact, medium effort)
- PRD-4.1: MVP'd with 50K users; 62% vs. baseline 45% redemption ✓
- PRD-5.1: Launched; metric tracked: 45% → 62% redemption (+17%); 400K additional redemptions/year

**Impact:** +$85M annual redemption value; improved casual member NPS from 5.8 to 6.5

---

### Story 2: The Elite Retention Cliff → Fixed

**Problem:** Platinum members' 1-year renewal rate was 82% (vs. 95% target). Losing $2M/year in churn.

**Law Application:**
- PRD-1.1: Interviewed churned elite; found "don't feel valued" and "lounge experience declined"
- PRD-2.1: Mapped elite year-end renewal moment; identified uncertainty and undervaluation
- PRD-3.1: Scored features; chose concierge (86), value recognition (82), exclusive experiences (78)
- PRD-4.1: Pilot concierge with 50 platinum; 100% retention + 9.2/10 NPS ✓
- PRD-5.1: Scaled to 500 platinum; retention 82% → 92%; NPS 8.2 → 8.9

**Impact:** +60K platinum members retained; +$132M annual value; elite advocacy increased 35% → 58%

---

### Story 3: The Elite Advancement Plateau → Unlocked

**Problem:** Only 25% of frequent travelers reached elite status; wanted 35%. Losing $100M annual opportunity.

**Law Application:**
- PRD-1.1: Surveyed frequent travelers; 30% didn't know how close they were to elite
- PRD-2.1: Mapped journey; identified Month-7 as dropout point ("Am I ever getting there?")
- PRD-3.1: Scored real-time tracker (93); highest ROI feature
- PRD-4.1: Beta tested tracker with 50K users; 48% weekly engagement vs. target 40% ✓
- PRD-5.1: Launched; elite achievement 25% → 32%; +210K elite members × $500 LTV = $105M

**Impact:** +$105M annual member value; elite tier strengthened; acquisition improved (elite members worth 10x more)

---

## Using This Guidance

- **You're a PM:** Pick your goal (increase casual redemption? reduce churn? grow elite?) → Find corresponding laws → Apply sequentially
- **You're an engineer:** Understand *why* features matter (discovery/journey) → Build MVPs (validate) → Measure (iterate)
- **You're in marketing:** Use PRD-2.1 journey mapping to create persona-specific campaigns; use PRD-5.1 metrics to prove marketing ROI
- **You're an executive:** Use PRD-3.1 roadmap scores to approve/deny features; use PRD-5.1 KPIs to track program health quarterly

**Next:** Start with your biggest member pain point. Run discovery (PRD-1.1). What will you find?

---

*Last Updated: February 2026*  
*Questions?* Contact Diana (Program Manager) or refer back to the product law examples in [../../../laws/product/_domain.yaml](../../../laws/product/_domain.yaml)
