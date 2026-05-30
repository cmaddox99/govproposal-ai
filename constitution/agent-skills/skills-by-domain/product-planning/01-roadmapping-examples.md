> Examples for: skill-01-roadmapping  
> Parent skill: 01-roadmapping.md  
> These are optional pedagogical supplements — not in governance scope.

---

## Good Examples

### Example 1: E-commerce Platform Roadmap

**Vision:** Enable small businesses to sell online as easily as selling in person.

**Strategic Themes:**
1. Frictionless Checkout
2. Merchant Success
3. Multi-Channel Presence

**NOW (Current Quarter)**
```
Theme: Frictionless Checkout

Outcome: Customers complete purchases without creating an account
Why: Cart abandonment data shows 35% drop-off at account creation
Success Metric: Reduce checkout abandonment by 20%
Dependencies: None
Risks: May reduce customer data collection

Outcome: Customers can pay with their preferred method
Why: Support requests show demand for Apple Pay, Google Pay
Success Metric: 15% of transactions use alternative payment
Dependencies: Payment processor integration
Risks: PCI compliance scope increase
```

**NEXT (Next Quarter)**
```
Theme: Merchant Success

Outcome: Merchants understand what drives their sales
Why: Merchant interviews reveal lack of actionable insights
Success Metric: 50% of merchants use analytics weekly
Dependencies: Data pipeline improvements (NOW)
Risks: Data accuracy concerns

Outcome: Merchants can recover abandoned carts
Why: Top requested feature, proven revenue impact
Success Metric: 10% cart recovery rate
Dependencies: Email infrastructure
Risks: Spam concerns, unsubscribe rates
```

**LATER (Future)**
```
Theme: Multi-Channel Presence

Outcome: Merchants can sell on social media platforms
Why: Market trend, competitive pressure
Confidence: Medium - awaiting platform API changes

Outcome: Merchants can manage inventory across channels
Why: Logical extension of multi-channel
Confidence: Low - depends on multi-channel adoption
```

**Why it's good:**
- Outcomes, not features
- Clear rationale for each item
- Explicit dependencies and risks
- Appropriate confidence levels

### Example 2: Internal Tool Roadmap

**Vision:** Engineering teams ship features 50% faster with confidence.

**NOW**
```
Outcome: Developers can run production-like environments locally
Why: Environment inconsistency causes 30% of bug reports
Metric: Time to reproduce bugs < 5 minutes

Outcome: Teams can deploy to staging in under 10 minutes
Why: Current 45-minute deploy blocks iteration
Metric: Staging deploy time
```

**NEXT**
```
Outcome: Teams can see deployment status without leaving their IDE
Why: Context switching reduces productivity
Metric: Developer satisfaction survey

Outcome: Failed deployments automatically roll back
Why: Manual rollbacks cause extended outages
Metric: Mean time to recovery
```

**LATER**
```
Outcome: Teams can preview changes before merging
Why: Reduces review time, catches integration issues
Confidence: Medium - infrastructure complexity

Outcome: Deployments self-heal from common failures
Why: Reduce on-call burden
Confidence: Low - requires ML/pattern detection
```

---

## Bad Examples (Anti-Patterns)

### Anti-Pattern 1: Feature Factory Roadmap

```
# BAD - List of features without strategic context

Q1:
- Dark mode
- Notification preferences
- Export to CSV
- Admin dashboard

Q2:
- Mobile app
- API v2
- Reporting module
- SSO integration

Q3:
- AI features
- Performance improvements
- Bug fixes
- Technical debt
```

**Why it's wrong:**
- No connection to user outcomes
- No prioritization rationale
- Features could be anything
- No success metrics
- "Q3" implies false precision

**Correct approach:** Frame as outcomes with strategic rationale.

### Anti-Pattern 2: Commitment-Heavy Roadmap

```
# BAD - Specific dates and promises

March 15: Launch dark mode
March 22: Complete notification system
April 1: Deploy admin dashboard v1.0
April 15: Mobile app beta release
May 1: API v2 general availability
```

**Why it's wrong:**
- Creates false expectations
- No room for learning/adaptation
- Encourages cutting corners to meet dates
- Treats software development as predictable

**Correct approach:** Use Now/Next/Later without specific dates.

### Anti-Pattern 3: Technology-Driven Roadmap

```
# BAD - Technology focus instead of user focus

Q1: Migrate to microservices
Q2: Implement event sourcing
Q3: Add GraphQL API
Q4: Kubernetes deployment
```

**Why it's wrong:**
- No user value articulated
- Technology for technology's sake
- Stakeholders can't evaluate priority
- No success criteria beyond "done"

**Correct approach:** Frame technical work as enabling outcomes:
```
NOW: Teams can deploy services independently
(Enabled by: microservices architecture)
```

---

## Artifacts & Templates

### Template: Roadmap Document

```markdown
# Product Roadmap: [Product Name]

## Vision
[1-2 sentence vision statement]

## Strategic Themes

### Theme 1: [Name]
**Objective:** [What we're trying to achieve]
**Key Results:**
- [Measurable result 1]
- [Measurable result 2]

### Theme 2: [Name]
[Continue pattern...]

---

## NOW (Current Focus)

### [Outcome 1]
**Theme:** [Theme name]
**Description:** [What users will be able to do]
**Why Now:** [Strategic rationale]
**Success Metric:** [How we'll measure]
**Dependencies:** [Prerequisites]
**Risks:** [What could go wrong]
**Status:** [Not Started | In Progress | Complete]

### [Outcome 2]
[Continue pattern...]

---

## NEXT (Upcoming)

### [Outcome 3]
**Theme:** [Theme name]
**Description:** [What users will be able to do]
**Why Next:** [Strategic rationale]
**Confidence:** [High | Medium | Low]
**Open Questions:**
- [Question 1]
- [Question 2]

---

## LATER (Future Possibilities)

### [Outcome 4]
**Theme:** [Theme name]
**Description:** [What users might be able to do]
**Confidence:** [Low]
**Depends On:** [What needs to happen first]

---

## Changelog

| Date | Change | Rationale |
|------|--------|-----------|
| [Date] | [What changed] | [Why] |

## Review Schedule
[How often this roadmap is reviewed and by whom]
```

### Template: Outcome Statement

```markdown
## Outcome: [User-focused outcome statement]

**Theme:** [Strategic theme this belongs to]

**User Story:**
As a [user type]
I want [capability]
So that [benefit]

**Why This Matters:**
[2-3 sentences on strategic importance]

**Success Metrics:**
| Metric | Current | Target | Timeframe |
|--------|---------|--------|-----------|
| [Metric] | [Now] | [Goal] | [When] |

**Key Assumptions:**
- [Assumption 1]
- [Assumption 2]

**Open Questions:**
- [Question 1]
- [Question 2]

**Dependencies:**
- [Prerequisite 1]
- [Prerequisite 2]

**Risks and Mitigations:**
| Risk | Impact | Likelihood | Mitigation |
|------|--------|------------|------------|
| [Risk] | H/M/L | H/M/L | [Plan] |
```

---

