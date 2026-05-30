> Examples for: skill-02-user-journey-mapping  
> Parent skill: 02-user-journey-mapping.md  
> These are optional pedagogical supplements — not in governance scope.

---

## Good Examples

### Example 1: E-commerce First Purchase Journey

**Scope:**
```
Persona: First-time online shopper (Sarah, 45)
Goal: Purchase a birthday gift for grandson
Scope: From realizing need to receiving confirmation
Touchpoints: Google, Website, Email
```

**Journey Map:**

| Stage | Actions | Touchpoints | Emotions | Pain Points |
|-------|---------|-------------|----------|-------------|
| **Trigger** | Realizes grandson's birthday is in 2 weeks | Calendar reminder | Slightly anxious (time pressure) | - |
| **Search** | Googles "toys for 8 year old boy" | Google, Review sites | Overwhelmed (too many options) | Information overload |
| **Browse** | Visits our site, looks at categories | Website - Home, Category | Curious but uncertain | Categories not intuitive for gift-givers |
| **Evaluate** | Reads reviews, checks shipping time | Product pages | Growing confidence | Reviews don't mention age appropriateness |
| **Add to Cart** | Selects item, chooses options | Product page, Cart | Hopeful | Can't easily see delivery date |
| **Checkout** | Creates account, enters payment | Checkout flow | Anxious (data entry) | Required account creation feels intrusive |
| **Confirm** | Reviews order, submits | Confirmation page | Relieved, satisfied | Confirmation email delayed |

**Pain Points (Prioritized):**
1. **Critical:** Can't see delivery date until checkout (causes abandonment)
2. **High:** Required account creation adds friction
3. **High:** Categories designed for parents, not gift-givers
4. **Medium:** Reviews don't address age appropriateness
5. **Low:** Confirmation email delayed

**Opportunities:**
1. Add "gift finder" with recipient age/interest filters
2. Guest checkout with optional account creation post-purchase
3. Show estimated delivery date on product pages
4. Add "age appropriateness" to review prompts
5. Real-time order confirmation

**JTBD Statements:**
```
When I'm buying a gift for someone else
I want to find age-appropriate items quickly
So I can be confident my gift will be enjoyed

When I'm checking out for the first time
I want to complete my purchase without creating an account
So I can get my gift ordered without extra steps
```

### Example 2: SaaS Onboarding Journey

**Scope:**
```
Persona: Marketing Manager (Mike, 32)
Goal: Start using product to track campaign performance
Scope: From signup to first valuable insight
Touchpoints: Website, App, Email, Help docs
```

**Journey Map:**

| Stage | Actions | Emotions | Pain Points |
|-------|---------|----------|-------------|
| **Signup** | Enters email, creates password | Optimistic | Requested info seems excessive |
| **Verify** | Clicks email link | Slightly annoyed | Verification email slow |
| **Initial Setup** | Names workspace, invites team | Uncertain | Don't know if team should be invited yet |
| **Connect Data** | Attempts to connect Google Analytics | Frustrated | OAuth flow confusing, permissions scary |
| **Explore** | Looks at empty dashboard | Confused | No guidance on what to do next |
| **First Value** | Sees first data appear | Relieved | Took 3 days for data to populate |
| **Aha Moment** | Discovers insight they couldn't see before | Delighted | Almost gave up before this |

**Critical Insight:**
> The journey from signup to "Aha Moment" takes 3+ days. Users who don't reach the Aha Moment in 48 hours have 80% higher churn. The gap between "Connect Data" and "First Value" is where we lose people.

**Opportunities:**
1. Demo data for immediate value (reduce time to Aha)
2. Guided setup wizard with progress indicator
3. Simplified OAuth with clear permission explanations
4. "First insight" notification to pull users back
5. Segment-specific onboarding paths

---

## Bad Examples (Anti-Patterns)

### Anti-Pattern 1: Feature-Centric Journey

```
# BAD - Describes our product, not user experience

Stage 1: User sees our homepage
Stage 2: User clicks signup button
Stage 3: User fills out our form
Stage 4: User activates their account
Stage 5: User uses our dashboard
Stage 6: User upgrades to premium
```

**Why it's wrong:**
- Focused on OUR product, not USER experience
- Misses what happens before/after our touchpoints
- Doesn't capture emotions or pain points
- Assumes linear happy path

**Correct approach:** Start with user goal, include all touchpoints (even competitors).

### Anti-Pattern 2: Solution-Contaminated Journey

```
# BAD - Already has solutions embedded

Pain Point: Users don't have dark mode
Pain Point: Users need more notification options
Pain Point: Users want mobile app
```

**Why it's wrong:**
- These are feature requests, not pain points
- Skips understanding the actual problem
- May be solving wrong problem

**Correct approach:**
```
Pain Point: Users report eye strain during evening use
- Causes: Bright interface, no time-based adjustments
- Severity: High (mentioned by 40% of support tickets)
- Possible solutions: Dark mode, auto-brightness, scheduled themes
```

### Anti-Pattern 3: Assumption-Based Journey

```
# BAD - No evidence, just guesses

"Users probably feel frustrated here"
"We think users want..."
"Users should appreciate this feature"
```

**Why it's wrong:**
- Based on team opinions, not user data
- "Should" indicates wishful thinking
- Can lead to building unwanted features

**Correct approach:** Ground every statement in evidence:
```
"23 of 30 interviewed users mentioned frustration at this step"
"Session recordings show 60% of users pause here for >30 seconds"
"Support tickets about this issue increased 40% this quarter"
```

---

## Artifacts & Templates

### Template: Journey Map Canvas

```markdown
# User Journey Map: [Journey Name]

## Scope Definition

**Persona:** [Name and key characteristics]
**Goal:** [What they're trying to accomplish]
**Trigger:** [What initiates this journey]
**End State:** [What success looks like]
**Timeframe:** [Typical duration]
**Touchpoints:** [All channels/products involved]

---

## Journey Stages

### Stage 1: [Name]

**User Goal:** [What they're trying to do in this stage]

**Actions:**
- [Action 1]
- [Action 2]

**Touchpoints:**
- [Touchpoint 1]
- [Touchpoint 2]

**Questions User Has:**
- [Question 1]
- [Question 2]

**Emotional State:** [Description + emoji indicator]
😊 Positive | 😐 Neutral | 😟 Negative

**Pain Points:**
| Pain Point | Severity | Evidence |
|------------|----------|----------|
| [Pain] | High/Med/Low | [Data source] |

**Opportunities:**
- [Opportunity 1]
- [Opportunity 2]

---

### Stage 2: [Name]
[Continue pattern for each stage...]

---

## Summary

### Top Pain Points (Prioritized)
1. **[Pain Point]** - Severity: [X], Stage: [Y]
2. **[Pain Point]** - Severity: [X], Stage: [Y]
3. **[Pain Point]** - Severity: [X], Stage: [Y]

### Top Opportunities
1. **[Opportunity]** - Impact: [X], Effort: [Y]
2. **[Opportunity]** - Impact: [X], Effort: [Y]
3. **[Opportunity]** - Impact: [X], Effort: [Y]

### Jobs-to-be-Done
```
When [situation]
I want to [action]
So I can [outcome]
```

### Recommended Next Steps
- [ ] [Research/validation needed]
- [ ] [Quick wins to implement]
- [ ] [Strategic initiatives to plan]

---

## Evidence Sources

| Source | Type | Date | Key Findings |
|--------|------|------|--------------|
| [Source] | Interview/Survey/Analytics | [Date] | [Summary] |
```

### Template: Pain Point Card

```markdown
## Pain Point: [Short Description]

**Stage:** [Journey stage where this occurs]
**Severity:** Critical / High / Medium / Low

**Description:**
[2-3 sentences describing the pain point from user perspective]

**Evidence:**
- [Data point 1]
- [Data point 2]
- [Quote from user research]

**Impact:**
- User impact: [How it affects user experience]
- Business impact: [Abandonment, support tickets, etc.]

**Root Cause:**
[Why this pain point exists]

**Potential Solutions:**
1. [Solution option 1]
2. [Solution option 2]

**Related JTBD:**
When [situation]
I want to [action]
So I can [outcome]
```

---

