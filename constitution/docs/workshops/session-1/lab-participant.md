---
workflow: greenfield-development
avatar: engineering
laws: [ENG-4.1, ENG-11.1, ENG-11.2, PRD-2.1, ENG-6.1]
skills: [skill-spec-governance, skill-04-business-domain-modeling, skill-06-atomic-tdd, skill-07-vertical-slice-dev]
session: 1
type: participant-lab-guide
---

# Session 1: Agentic SDLC Self-Service Track — Participant Lab Guide

> **Laws cited in this document:** ENG-4.1, ENG-11.1, ENG-11.2, PRD-2.1, BUS-7.1

---

## Welcome

This lab walks you through the **AA Hangar AI Constitution Greenfield Workflow** (Phases 1–6) using an AI assistant as your pair. You will build a constitutionally-governed vertical slice of a real domain from first principles — validated problem statement through passing tests.

**Total time:** 3 hours  
**Domain used in examples:** Loyalty Miles Calculation  
**Your domain:** _______________________________________________

**The non-negotiable laws you will be held to today:**

| Law ID | Title | Why It Matters |
|---|---|---|
| `ENG-4.1` | Atomic TDD | No implementation before a failing test — ever |
| `ENG-6.1` | Security Threat Model | Every design must address threats |
| `ENG-11.1` | Hangar SDD | Decisions must be documented in `hangar-ai-specs/` |
| `PRD-2.1` | Problem Validation | Build the right thing before building it right |

Keep your **Learner Prompt Guide** open beside this document. Every phase has a corresponding prompt.

---

## Phase 1: Capture — 20 Minutes

> **Workflow Phase:** 1 — Capture

### Law Citations

> **`PRD-2.1`:** Problem Validation — The problem domain must be validated against real personas before any design begins. Output must include a documented problem statement and at least two user personas.

### Skill Active

`skill-spec-governance`

### You Will

1. Open your AI assistant.
2. Use the **Session Bootstrap Prompt** from your prompt guide to set context. Fill in `[MY DOMAIN]` and `[MY STACK]`.
3. Paste the **Phase 1 Capture prompt** from your prompt guide with your domain problem described.
4. Engage in dialogue with the AI — answer its questions about who has the problem, what success looks like, and what failure looks like.
5. Produce and save two outputs:
   - A **validated problem statement** (2–4 sentences, specific and measurable)
   - **2–3 user personas** (name, role, specific pain point, success criterion)

**Tips:**
- Be specific about personas. "Maria, a Gold-tier member who manually files partner miles each month" is a real persona. "A frequent flyer" is not.
- Your problem statement should answer: Who? What pain? What would success look like? What does failure cost?
- Do not start designing a solution yet. Phase 1 is discovery only.

### Expected Outputs

- Problem statement (write it down — do not leave it in the AI chat only)
- 2–3 personas with name, role, and concrete pain point

### Constitutional Gate

**✅ Gate: Problem Validated (PRD-2.1) + Personas Documented**

Before moving to Phase 2, confirm:
- [ ] Problem statement is written and saved
- [ ] At least 2 personas documented with concrete pain points
- [ ] No code or API designs have been started

---

### Your Turn — Phase 1 Workspace

**Problem Statement:**

```
[Write your validated problem statement here]


```

**Persona 1:**

```
Name:
Role:
Pain point:
Success criterion:
```

**Persona 2:**

```
Name:
Role:
Pain point:
Success criterion:
```

**Persona 3 (optional):**

```
Name:
Role:
Pain point (edge case):
```

---

## Phase 2: Discover — 15 Minutes

> **Workflow Phase:** 2 — Discover

### Law Citations

> **`ENG-1.1`:** Priority Hierarchy — Constitution laws are applied in priority order. Non-negotiable laws (`ENG-4.1`, `ENG-6.1`, `ENG-6.4`, `ENG-11.1`) override all other considerations.
>
> **`PRD-2.1`:** Problem Validation (carry-forward)

### Skill Active

`skill-04-business-domain-modeling`

### You Will

1. Paste the **Phase 2 Discover prompt** from your prompt guide with your problem statement from Phase 1.
2. Review the AI's **law inventory table** (Law ID | Applies Because | NON-NEGOTIABLE?).
3. Look up any unfamiliar law ID in the hangar-ai-constitution README or specification files.
4. Mark the NON-NEGOTIABLE laws in your notes — you will be held to these at every subsequent gate.
5. Confirm the Engineering avatar is active: paste the content of `agent-skills/base/AGENT.md` and ask the AI to confirm it is loaded.

**The priority hierarchy (memorize this):**
```
Constitution
    ↓
Non-Negotiable Laws (ENG-4.1, ENG-6.1, ENG-6.4, ENG-11.1)
    ↓
Domain-Specific Laws
    ↓
Team Preferences
```

When a conflict arises, the higher level always wins. If your team wants to skip tests for velocity, `ENG-4.1` wins.

### Expected Outputs

- Law inventory table (minimum 6 laws, all 4 NON-NEGOTIABLEs identified)
- Avatar manifest confirmation (AI acknowledges `AGENT.md` is loaded)
- Your NON-NEGOTIABLE constraints list

### Constitutional Gate

**✅ Gate: Avatar Manifest Loaded + Applicable Laws Listed**

Before moving to Phase 3, confirm:
- [ ] Avatar is confirmed active in your AI session
- [ ] Law inventory table produced with at least 4 NON-NEGOTIABLE laws
- [ ] `ENG-4.1` is in your NON-NEGOTIABLE column

---

### Your Turn — Phase 2 Workspace

**Law Inventory:**

| Law ID | Applies Because | NON-NEGOTIABLE? |
|---|---|---|
| ENG-4.1 | | ✅ YES |
| ENG-6.1 | | ✅ YES |
| ENG-6.4 | | ✅ YES |
| ENG-11.1 | | ✅ YES |
| | | |
| | | |

**Avatar confirmation received? (Y/N):** _______

---

## Phase 3: Define — 25 Minutes

> **Workflow Phase:** 3 — Define

### Law Citations

> **`ENG-1.5`:** API-First — API contracts must be defined before implementation begins.
>
> **`ENG-4.4`:** BDD Structure — Acceptance criteria must be expressed as Given/When/Then Gherkin scenarios.
>
> **`ENG-11.1`:** Hangar SDD — Significant design decisions must be captured in a `PROPOSAL.md` in `hangar-ai-specs/`.
>
> **`ENG-11.2`:** Proposal Completeness — Proposals must include: problem statement, API contract, BDD scenarios, architecture decision rationale, and law citations.

### Skills Active

`skill-spec-governance`, `skill-03-executable-spec`

### You Will

1. Paste the **Phase 3 Define prompt** with your domain filled in.
2. Review the three outputs from the AI: API contract, BDD scenarios, and `PROPOSAL.md` stub.
3. Validate the **API contract**: Does it include endpoint, method, request body, response body, and error codes?
4. Validate **BDD scenarios**: Are they in valid `Given/When/Then` Gherkin? Do they cover happy path + at least one failure path?
5. Validate **`PROPOSAL.md` stub**: Does it cite `ENG-1.5`, `ENG-4.4`, and `ENG-11.1` by ID?
6. Save the `PROPOSAL.md` stub to `hangar-ai-specs/` in your working copy.

**What valid BDD looks like (loyalty miles example):**
```gherkin
Scenario: Gold-tier member earns miles on qualifying flight
  Given a Gold-tier member with ID "M001"
  When they complete flight FL123 in fare class Y
  Then they earn 1500 base miles × 1.5 Gold multiplier = 2250 miles

Scenario: Non-qualifying fare class earns zero miles
  Given a member with any status tier
  When they complete a flight on Basic Economy (fare class B)
  Then they earn 0 miles and receive a "non-qualifying fare" notification
```

**What invalid BDD looks like (do not accept this):**
```
The system should calculate miles based on fare class and status tier.
(This is a requirement, not a BDD scenario. Reject it.)
```

### Expected Outputs

- API contract (endpoint, method, request/response, error codes)
- At least 3 BDD scenarios in valid Gherkin
- `PROPOSAL.md` stub saved on disk with law citations

### Constitutional Gate

**✅ Gate: All Critical Paths Have Gherkin Scenarios**

Before moving to Phase 4, confirm:
- [ ] API contract is written (actual endpoint + payload, not described)
- [ ] At least 3 BDD scenarios in valid Gherkin format
- [ ] `PROPOSAL.md` stub exists on disk with law citations
- [ ] No implementation code has been written

---

### Your Turn — Phase 3 Workspace

**API Contract:**

```
Endpoint:
Method:
Request body:
Response body:
Error codes:
```

**BDD Scenario 1 (happy path):**

```gherkin
Scenario:
  Given
  When
  Then
```

**BDD Scenario 2 (failure path):**

```gherkin
Scenario:
  Given
  When
  Then
```

**BDD Scenario 3 (edge case):**

```gherkin
Scenario:
  Given
  When
  Then
```

**`PROPOSAL.md` saved? (Y/N):** _______  
**Law citations present? (ENG-1.5, ENG-4.4, ENG-11.1) (Y/N):** _______

---

## Phase 4: Design — 10 Minutes

> **Workflow Phase:** 4 — Design

### Law Citations

> **`ENG-2.1`:** Architecture Standards — Architecture decisions must be documented with rationale.
>
> **`ENG-6.1` (NON-NEGOTIABLE):** Security Threat Model — Every design must include a security threat model. Unmitigated HIGH threats block progression.
>
> **`ENG-11.2`:** Proposal Completeness (carry-forward)

### Skill Active

`skill-spec-governance`

### You Will

1. Paste the **Phase 4 Design prompt** with your `PROPOSAL.md` content.
2. Review the AI's design critique — does it identify any law violations? Unmitigated risks?
3. Confirm at least one ADR (Architecture Decision Record) is filed. An ADR can be brief:
   ```
   Decision: [what was decided]
   Status: Accepted
   Context: [why this decision was needed]
   Consequences: [what becomes easier / harder]
   Laws: [ENG-x.x]
   ```
4. Review the security threat model produced — are HIGH threats identified and mitigated?
5. Update your `PROPOSAL.md` with the design decisions.

**Common security threats for an API like loyalty miles calculation:**
- Input manipulation: a caller passes a `flightId` for a flight they didn't take
- Authorization bypass: caller modifies `memberId` to accumulate miles on another account
- Rate abuse: bulk calculation requests to enumerate valid member IDs

### Expected Outputs

- AI design critique of `PROPOSAL.md`
- At least one ADR stub filed
- Security threat model (2 threats minimum, mitigations described)
- `PROPOSAL.md` updated with design rationale

### Constitutional Gate

**✅ Gate: No Unmitigated HIGH Threats**

Before moving to Phase 5, confirm:
- [ ] Security threat model exists (`ENG-6.1`)
- [ ] All HIGH threats have a documented mitigation
- [ ] At least one ADR filed

---

### Your Turn — Phase 4 Workspace

**Threat 1:**

```
Threat:
OWASP category:
Severity (HIGH/MEDIUM/LOW):
Mitigation:
```

**Threat 2:**

```
Threat:
OWASP category:
Severity (HIGH/MEDIUM/LOW):
Mitigation:
```

**ADR filed? (Y/N):** _______

---

## Phase 5: Plan — 15 Minutes

> **Workflow Phase:** 5 — Plan

### Law Citations

> **`ENG-2.3`:** Vertical Slice Architecture — Work must be organized as thin vertical slices that deliver end-to-end value, not horizontal layers.
>
> **`ENG-4.2`:** Test Pyramid — Unit tests at the base, integration tests in the middle, contract/E2E tests at the top.

### Skill Active

`skill-07-vertical-slice-dev`

### You Will

1. Paste the **Phase 5 Plan prompt**.
2. Review the AI's vertical slice decomposition.
3. Validate each slice: does it deliver end-to-end value independently? (Not "implement the service layer.")
4. Review test types per slice — does the AI respect the `ENG-4.2` test pyramid?
5. Output: `tasks.md` with slices as checkboxes, ordered by dependency.

**A valid vertical slice (loyalty miles example):**
```markdown
- [ ] Slice 1: Calculate base miles for a qualifying flight
  - Tests: unit (MilesCalculatorTest)
  - Depends on: nothing
- [ ] Slice 2: Apply Gold/Platinum/ExecPlat status multiplier  
  - Tests: unit (MilesCalculatorTest — multiplier cases)
  - Depends on: Slice 1
- [ ] Slice 3: Return zero miles for non-qualifying fare class
  - Tests: unit (MilesCalculatorTest — fare class filter)
  - Depends on: Slice 1
- [ ] Slice 4: Persist awarded miles to member account
  - Tests: unit + integration (MilesRepositoryTest)
  - Depends on: Slice 2, Slice 3
```

**An invalid slice:**
```
- [ ] Implement the service layer
(This is horizontal, not vertical. It delivers no end-to-end value by itself.)
```

### Expected Outputs

- Vertical slice decomposition (2–4 slices, each independently shippable)
- `tasks.md` with checkboxes and dependency order
- Test types identified per slice

### Constitutional Gate

**✅ Gate: Implementation Proposal Approved**

Before moving to Phase 6, confirm:
- [ ] `tasks.md` exists with at least 2 vertical slices
- [ ] Each slice has named test types
- [ ] Dependency order is documented
- [ ] `PROPOSAL.md` updated with slice plan

---

### Your Turn — Phase 5 Workspace

**Vertical Slice Decomposition:**

```markdown
- [ ] Slice 1:
  - Tests:
  - Depends on:

- [ ] Slice 2:
  - Tests:
  - Depends on:

- [ ] Slice 3 (optional):
  - Tests:
  - Depends on:
```

**`tasks.md` saved? (Y/N):** _______

---

## Phase 6: Build — 60 Minutes

> **Workflow Phase:** 6 — Build
>
> ⚠️ `ENG-4.1` IS NON-NEGOTIABLE. YOU WILL NOT WRITE A SINGLE LINE OF IMPLEMENTATION BEFORE A FAILING TEST EXISTS.

### Law Citations

> **`ENG-4.1` (NON-NEGOTIABLE):** Atomic TDD — The TDD cycle is mandatory. RED → GREEN → REFACTOR → VERIFY → COMMIT → REPEAT.
>
> **`ENG-3.1`:** Cyclomatic Complexity ≤ 10 — Checked during REFACTOR phase.
>
> **`ENG-3.4`:** Single Responsibility Principle — Checked during REFACTOR phase.
>
> **`ENG-4.5`:** Test Naming Convention — `methodName_condition_expectedBehavior`.
>
> **`ENG-4.6`:** Coverage Threshold — New code must achieve ≥90% test coverage.

### Skill Active

`skill-06-atomic-tdd`

### The TDD Cycle

```
RED → GREEN → REFACTOR → VERIFY → COMMIT → REPEAT
```

**One behavior at a time. No exceptions.**

---

### Full TDD Walkthrough: Loyalty Miles Domain

Follow along with the worked example below. When you reach "Your Turn" at the end, apply the same cycle to your own domain.

---

#### Step 1 — RED Phase

Start with the **RED prompt** from your prompt guide.

The AI should produce a failing test. The test must:
1. Be named following `ENG-4.5`: `methodName_condition_expectedBehavior`
2. Fail — either because the class doesn't exist yet, or because the behavior isn't implemented

**Example test (Java):**
```java
@Test
void calculateMiles_goldStatus_earns150PercentMultiplier() {
    // Arrange
    MilesCalculator calculator = new MilesCalculator();
    Flight flight = new Flight("FL123", 1000); // 1000 base miles
    Member member = new Member("M001", StatusTier.GOLD);

    // Act
    int milesEarned = calculator.calculateMiles(flight, member);

    // Assert
    assertEquals(1500, milesEarned); // 1000 * 1.5 = 1500
}
```

**Run the test now.** It must fail. `Cannot find symbol: MilesCalculator` counts as RED.  
✅ If it fails: proceed to GREEN.  
❌ If it passes: your test is wrong. It's testing something that already exists, not specifying new behavior.

---

#### Step 2 — GREEN Phase

Once you confirm RED, use the **GREEN prompt** from your prompt guide.

The AI should produce the **minimum implementation** to make the one failing test pass. No extra logic, no future cases.

**Example minimum implementation (Java):**
```java
// StatusTier.java
public enum StatusTier { STANDARD, GOLD, PLATINUM, EXECUTIVE_PLATINUM }

// Flight.java
public class Flight {
    private final String flightId;
    private final int baseMiles;
    public Flight(String flightId, int basemiles) {
        this.flightId = flightId;
        this.baseMiles = baseiles;
    }
    public int getBaseiles() { return baseiles; }
}

// Member.java
public class Member {
    private final String memberId;
    private final StatusTier statusTier;
    public Member(String memberId, StatusTier statusTier) {
        this.memberId = memberId;
        this.statusTier = statusTier;
    }
    public StatusTier getStatusTier() { return statusTier; }
}

// MilesCalculator.java
public class MilesCalculator {
    public int calculateMiles(Flight flight, Member member) {
        if (member.getStatusTier() == StatusTier.GOLD) {
            return (int) (flight.getBaseiles() * 1.5);
        }
        return flight.getBaseiles();
    }
}
```

**Run the test now.** It must pass. One test, one passing.  
✅ If it passes: proceed to REFACTOR.  
❌ If it fails: the implementation is wrong. Ask the AI to fix it (GREEN phase, minimum fix only).

---

#### Step 3 — REFACTOR Phase

Use the **REFACTOR prompt** from your prompt guide.

The AI checks three laws:
- **`ENG-3.1`**: Is cyclomatic complexity ≤ 10? (Count your if/else/switch branches)
- **`ENG-3.4`**: Does each class have one responsibility?
- **`ENG-4.5`**: Does your test name follow `methodName_condition_expectedBehavior`?

If the AI says "No refactor needed," accept it and move on.  
If it proposes a refactor, verify that the test still passes after the refactor. **Same behavior, cleaner code.**

> ⚠️ If the AI tries to add Platinum or Executive Platinum support during REFACTOR, stop it. Use the recovery prompt:
> "Stop. REFACTOR means same behavior, cleaner code. Do not add new cases. We will handle those in the next RED cycle."

---

#### Step 4 — VERIFY Phase

Run your full test suite:

```bash
# Java/Gradle
./gradlew test

# Java/Maven
mvn test

# Python
pytest

# TypeScript
npm test
```

Every test that was passing before must still pass. You should see zero failures.

---

#### Step 5 — COMMIT Phase

```bash
git add src/
git commit -m "feat([your-domain]): [describe the behavior implemented]

- Law: ENG-4.1 (Atomic TDD — NON-NEGOTIABLE)
- Test: [test method name]
- Coverage: [approximate %] new code (ENG-4.6)
"
```

---

#### Step 6 — REPEAT

Now begin the next RED-GREEN-REFACTOR-VERIFY-COMMIT cycle for the next behavior.

**For the loyalty miles example, the next test is:**
```java
@Test
void calculateMiles_standardStatus_earnsBaseMilesOnly() {
    MilesCalculator calculator = new MilesCalculator();
    Flight flight = new Flight("FL456", 800);
    Member member = new Member("M002", StatusTier.STANDARD);

    int milesEarned = calculator.calculateMiles(flight, member);

    assertEquals(800, milesEarned);
}
```

---

### Your Turn — Phase 6 Workspace

Complete at minimum two full RED-GREEN-REFACTOR-VERIFY-COMMIT cycles for your domain.

**Cycle 1 — Test name (ENG-4.5 format):**

```
methodName_condition_expectedBehavior:
```

**Cycle 1 status:**
- [ ] RED confirmed (test fails)
- [ ] GREEN confirmed (test passes, minimum implementation)
- [ ] REFACTOR reviewed (ENG-3.1, ENG-3.4, ENG-4.5 checked)
- [ ] VERIFY confirmed (full suite passing)
- [ ] COMMIT made (with law citations)

**Cycle 2 — Test name:**

```
methodName_condition_expectedBehavior:
```

**Cycle 2 status:**
- [ ] RED confirmed
- [ ] GREEN confirmed
- [ ] REFACTOR reviewed
- [ ] VERIFY confirmed
- [ ] COMMIT made

**Coverage estimate on new code:** _______ %  
(Must be ≥ 90% per ENG-4.6)

---

### Constitutional Gate

**✅ Gate: All Slices Green; Coverage ≥90% New Code (ENG-4.6)**

Before moving to Phase 7, confirm:
- [ ] Every test is passing (zero failures)
- [ ] Coverage on new code ≥ 90% (ENG-4.6)
- [ ] Commit message includes law citations
- [ ] No implementation code exists without a corresponding test

---

## Phase 7: Review — Stretch (15 Minutes)

> **Workflow Phase:** 7 — Review _(complete if time permits)_

### Law Citations

> **`ENG-6.1` (NON-NEGOTIABLE):** OWASP Top 10 review before ship.
>
> **`BUS-7.1`:** Audit Trail — Business-critical decisions must have an immutable audit trail.

### You Will

1. Run a constitution compliance review: does your code comply with all laws from your Phase 2 inventory?
2. Check OWASP Top 10 against your API design (focus on A01, A03, A04 for this domain).
3. Identify where the BUS-7.1 audit trail lives in your design — or flag it as a gap.
4. Review your `PROPOSAL.md` completeness against the ENG-11.2 checklist.

### Your Turn — Phase 7 Workspace

**OWASP Top 10 Quick Check:**

| Category | Threat | Addressed? |
|---|---|---|
| A01: Broken Access Control | `memberId` validated against authenticated user | Y / N |
| A03: Injection | `flightId` sanitized before DB query | Y / N |
| A04: Insecure Design | Rate limits on calculation endpoint | Y / N |

**BUS-7.1 Audit Trail — where does it live?**

```
[Describe or note as gap]
```

---

## Debrief Questions

Reflect on these five questions individually or with your pair. Be prepared to share one answer with the group.

1. **The Gate Question:** At which gate did you feel the most friction? Was that friction useful or bureaucratic overhead? How do you tell the difference?

2. **The TDD Question:** Before today, how routinely did you write the test before the implementation? What is the most common rationalization for skipping it — and does `ENG-4.1` accept that rationalization?

3. **The Law Question:** Which law in today's session surprised you? Which one do you think your current team most frequently violates without knowing?

4. **The Prompt Question:** When did your AI assistant produce something unhelpful or wrong? What prompt pattern fixed it? What does that tell you about how to structure a good law-grounded prompt?

5. **The Scale Question:** If every engineer at AA followed this workflow for every greenfield feature, what would change about how we build software? What would get harder? What would get easier?

---

## Session 2 Bridge

Session 2 covers **Legacy Adoption** — the same constitution applied to existing codebases.

**Key differences you will encounter in Session 2:**

| Dimension | Session 1 (Greenfield) | Session 2 (Legacy) |
|---|---|---|
| Starting point | Empty project | Existing code, possibly untested |
| Phase 1 (Capture) | Define new problem | Archaeology — understand existing behavior |
| TDD (`ENG-4.1`) | Write test → write code | Write characterization tests first |
| API contracts | Design from scratch | Discover existing implicit contracts |
| Threat model | Design-time | Runtime analysis of existing vulnerabilities |
| `PROPOSAL.md` | New file | Refactor proposal — what changes and why |
| Primary skill | `skill-06-atomic-tdd` | `skill-09-refactoring` + `skill-06-atomic-tdd` |

**Bridge question — come prepared to answer this at the start of Session 2:**

> "You have a 5-year-old Java service with 12,000 lines of code and 40% test coverage. Tomorrow you need to add a new feature. Walk me through the first three things you do before writing a single line of new code."

Use the Session 2 Bootstrap Prompt from your learner prompt guide to prepare.
