---
workflow: greenfield-development
avatar: engineering
laws: [ENG-4.1, ENG-11.1, ENG-11.2, PRD-2.1, ENG-6.1]
skills: [skill-spec-governance, skill-04-business-domain-modeling, skill-06-atomic-tdd, skill-07-vertical-slice-dev]
session: 1
type: instructor-lab-guide
---

# Session 1: Agentic SDLC Self-Service Track — Instructor Lab Guide

> **Laws cited in this document:** ENG-4.1, ENG-11.1, ENG-11.2, PRD-2.1, BUS-7.1

---

## Instructor Overview

| Item | Detail |
|---|---|
| **Session** | Session 1 of 2 |
| **Total Time** | 3 hours (180 minutes) |
| **Format** | Instructor-led lab with live AI co-pilot |
| **Audience** | AA engineers, architects, and senior developers |
| **Domain used in examples** | Loyalty Miles Calculation |

### Materials Needed

- [ ] Printed prompt guides (one per participant) — `learner-prompt-guide.md`
- [ ] Projected slides (connect to projector before participants arrive)
- [ ] Laptop per participant with internet access
- [ ] hangar-ai-constitution repository cloned locally on each machine
- [ ] AI coding assistant available (GitHub Copilot or equivalent)
- [ ] Printed participant lab guides — `lab-participant.md`
- [ ] Whiteboard or digital canvas for architecture sketching (Phase 4)
- [ ] Timer visible to participants for each phase

### Pre-Workshop Checklist

- [ ] Verify all machines have the hangar-ai-constitution repo cloned
- [ ] Confirm AI assistant access for every participant
- [ ] Load `greenfield-development.md` workflow in a visible browser tab on the projected screen
- [ ] Pre-write the TDD example on the whiteboard (RED → GREEN → REFACTOR → VERIFY → COMMIT → REPEAT cycle)
- [ ] Print extra copies of the prompt guide — participants frequently reference it during Phase 6
- [ ] Test that `skill-06-atomic-tdd` skill file loads correctly in the AI assistant
- [ ] Queue up the "loyalty miles" domain context so you can paste it quickly during the Phase 6 demo
- [ ] Confirm timing: if you run over in Phase 3, compress Phase 4 — **never** compress Phase 6

### Common Pitfalls

1. **Participants write code before tests (ENG-4.1 violation)** — This is the #1 issue. Intervene immediately. See Phase 6 instructor notes.
2. **Agents over-generate in Phase 3** — Participants forget to constrain output. Remind them to use recovery prompts.
3. **Phase 2 law inventory feels academic** — Ground it by asking "which law would you violate first if you just started building?"
4. **Weak personas in Phase 1** — Push for specificity: name, role, concrete pain point, not just "user wants X."
5. **Skipping the gate checks** — Gate checks are constitutional; treat them as mandatory stops, not suggestions.
6. **Phase 6 running long** — The TDD cycle demo is immutable. If you're running late, cut the Phase 7 stretch, not Phase 6.
7. **Participants conflate REFACTOR and REDESIGN** — REFACTOR means same behavior, cleaner code. Redesign is out of scope per-slice.

### What to Watch For During the Session

- Participants who "pre-implement" during RED phase — watch for code appearing before a failing test
- Groups where one person dominates the AI interaction — encourage pairing with role rotation every 15 min
- Confusion between `ENG-4.4` (BDD) and `ENG-4.1` (TDD) — they are complementary, not alternatives
- Participants who skip law citations in their prompts — law-grounded prompts produce better outputs
- Anyone who tries to skip Phase 1 and 2 to "get to the coding" — the gates exist for a reason
- Clock carefully: Phase 6 is 60 minutes and feels short. Brief them at the 45-minute mark.

---

## Phase 1: Capture — 20 Minutes

> **Workflow Phase:** 1 — Capture

### Law Citations

> **PRD-2.1:** Problem Validation — The problem domain must be validated against real personas before any design begins. Output must include a documented problem statement and at least two user personas.

### Skill Activated

`skill-spec-governance`

### What Participants Do

1. Open the Session Bootstrap Prompt from the learner prompt guide.
2. Replace `[MY DOMAIN]` with their chosen domain (or use the suggested default: "loyalty miles calculation").
3. Replace `[MY STACK]` with their actual tech stack.
4. Paste the Phase 1 Capture prompt into their AI assistant.
5. Engage in a dialogue with the AI: answer questions about who has the problem, what success looks like, and what failure looks like.
6. Produce and record two outputs:
   - A validated problem statement (2–4 sentences, specific and measurable)
   - 2–3 user personas (name, role, pain point, success criterion)

**Step-by-step:**
```
1. Read the Phase 1 prompt aloud before pasting it (builds habit of reading prompts before sending).
2. Paste into AI assistant.
3. Answer AI questions iteratively — do not write the problem statement yourself; let the AI help surface it.
4. When AI produces the problem statement, review it: Is it specific? Is it measurable? Does it name a real pain?
5. When AI produces personas, check: Do they have a name? A role? A concrete scenario?
6. Copy validated outputs into your workbook or a local markdown file.
7. Signal readiness at the gate check.
```

### Instructor Notes

> 🎓 **INSTRUCTOR ONLY**
>
> **Timing:** This phase should feel easy and generative. If participants are stuck after 5 minutes, they are probably being too broad. Ask: "What is the one thing your user cannot do today that they should be able to do?"
>
> **Pitfall:** Some participants will write "As a user, I want to…" personas. Push back — PRD-2.1 requires personas with enough specificity to identify compliance risk. "Maria, a Gold-tier loyalty member who travels 150,000 miles/year and files for partner miles manually each month" is far better than "frequent flyer."
>
> **Intervention:** If anyone tries to open a code editor at this stage, pause the room and reinforce the gate model. No code until Phase 6.
>
> **Fast finishers:** Have them produce a third persona that represents an edge case (e.g., a member whose account is under fraud review).

### Expected Outputs

- **Problem Statement:** 2–4 sentence description, specific and measurable
- **Personas:** 2–3 documented personas with name, role, and pain point
- **Gate artifact:** Can be captured in a local `PROBLEM.md` or directly in `PROPOSAL.md` stub

### Constitutional Gate

**✅ Gate: Problem Validated (PRD-2.1) + Personas Documented**

_Before proceeding to Phase 2, confirm:_
- [ ] Problem statement is written down (not just in the AI chat)
- [ ] At least 2 personas are documented with concrete pain points
- [ ] No code or API designs have been started

---

## Phase 2: Discover — 15 Minutes

> **Workflow Phase:** 2 — Discover

### Law Citations

> **ENG-1.1:** Priority Hierarchy — Constitution laws are applied in priority order. Non-negotiable laws (ENG-4.1, ENG-6.1, ENG-6.4, ENG-11.1) override all other considerations.
>
> **PRD-2.1:** Problem Validation (carry-forward from Phase 1)

### Skill Activated

`skill-04-business-domain-modeling`

### What Participants Do

1. Paste the Phase 2 Discover prompt, inserting their problem statement from Phase 1.
2. Review the AI's law inventory table (Law ID | Applies Because | NON-NEGOTIABLE?).
3. Identify which constraints are domain-specific vs. universal.
4. Note any avatar specializations the AI suggests for their domain.
5. Confirm activation of the Engineering avatar by referencing `AGENT.md` in `agent-skills/base/`.

**Step-by-step:**
```
1. Paste problem statement from Phase 1 into the Phase 2 prompt.
2. Send to AI.
3. Review the law inventory table. Ask: "Are there any laws in this table I don't recognize?"
4. Look up any unfamiliar law ID in the hangar-ai-constitution README or spec files.
5. Mark the NON-NEGOTIABLE laws in your notes — you will be held to these at every gate.
6. Confirm avatar: paste the content of AGENT.md and ask the AI to confirm it is loaded and active.
7. Signal readiness at the gate check.
```

### Instructor Notes

> 🎓 **INSTRUCTOR ONLY**
>
> **Timing:** 15 minutes is tight. If participants get absorbed in reading every law in the inventory, redirect them: "Focus on the NON-NEGOTIABLE column. Those are the ones that will stop your PR."
>
> **Key teaching moment:** ENG-1.1 priority hierarchy. Draw it on the whiteboard:
> `Constitution > Non-Negotiable Laws > Domain Laws > Team Preferences`
> Ask: "If your team wants to skip tests for velocity, which law wins?"
>
> **Avatar activation:** Some participants will wonder why we "load" an avatar. Explain: the AI assistant has no intrinsic knowledge of AA's constitution. The avatar file is the mechanism by which we inject that context. It is the equivalent of briefing a contractor on your house rules before they start work.
>
> **Common confusion:** Participants may conflate "applies to my domain" with "I have to implement this now." Clarify: the law inventory is a discovery, not a backlog.

### Expected Outputs

- **Law inventory table** (minimum: 6 laws identified, including all 4 NON-NEGOTIABLEs)
- **Avatar manifest confirmation** (screenshot or copy of AI acknowledgment)
- **Non-negotiable constraints list** (the four laws that are absolute)

### Constitutional Gate

**✅ Gate: Avatar Manifest Loaded + Applicable Laws Listed**

_Before proceeding to Phase 3, confirm:_
- [ ] Avatar is confirmed active in AI assistant session
- [ ] Law inventory table produced with at least 4 NON-NEGOTIABLE laws identified
- [ ] ENG-4.1 is in the NON-NEGOTIABLE column (test before code — this will govern Phase 6)

---

## Phase 3: Define — 25 Minutes

> **Workflow Phase:** 3 — Define

### Law Citations

> **ENG-1.5:** API-First — API contracts must be defined before implementation begins.
>
> **ENG-4.4:** BDD Structure — Acceptance criteria must be expressed as Given/When/Then Gherkin scenarios.
>
> **ENG-11.1:** Hangar SDD — Significant design decisions must be captured in a PROPOSAL.md in `hangar-ai-specs/`.
>
> **ENG-11.2:** Proposal Completeness — Proposals must include: problem statement, API contract, BDD scenarios, architecture decision rationale, and law citations.

### Skill Activated

`skill-spec-governance`, `skill-03-executable-spec`

### What Participants Do

1. Paste the Phase 3 Define prompt with their domain filled in.
2. Review the three outputs: API contract, BDD scenarios, PROPOSAL.md stub.
3. Validate the API contract: Does it include request/response structure? Error codes? Does it follow REST conventions?
4. Validate BDD scenarios: Are they Given/When/Then? Do they cover happy path and at least one failure path?
5. Validate PROPOSAL.md stub: Does it cite ENG-1.5, ENG-4.4, and ENG-11.1 by ID?
6. Save the PROPOSAL.md stub to `hangar-ai-specs/` (or a local equivalent for the workshop).

**Step-by-step for the loyalty miles example:**
```
API endpoint example:
  POST /api/v1/loyalty/calculate-miles
  Request: { memberId, flightId, fareClass, statusTier }
  Response: { milesEarned, multiplierApplied, calculatedAt }
  Errors: 400 (invalid input), 404 (member not found), 422 (ineligible fare class)

BDD scenario examples:
  Scenario: Gold-tier member earns miles on qualifying flight
    Given a Gold-tier member with ID "M001"
    When they complete flight FL123 in fare class Y
    Then they earn 1500 base miles × 1.5 Gold multiplier = 2250 miles

  Scenario: Non-qualifying fare class earns zero miles
    Given a member with any status tier
    When they complete a flight on Basic Economy (fare class B)
    Then they earn 0 miles and receive a "non-qualifying fare" notification
```

### Instructor Notes

> 🎓 **INSTRUCTOR ONLY**
>
> **Timing:** 25 minutes. The AI will want to generate more than three outputs — use the recovery prompt ("Token budget: brief") if it over-generates. Three things: API contract, BDD scenarios, PROPOSAL stub. Nothing else.
>
> **Key teaching moment:** ENG-11.1 and ENG-11.2 together form the "constitution of documentation." The proposal is not a bureaucratic artifact — it is the source of truth for reviewers, auditors (BUS-7.1), and the AI in future sessions. A well-formed proposal makes Phase 7 (Review) trivially easy.
>
> **Common error:** Participants write BDD scenarios in free prose, not Gherkin. Reject any "scenario" that doesn't have a `Given`, `When`, and `Then` keyword. ENG-4.4 is explicit.
>
> **Watch for:** Participants starting to design database schemas or class hierarchies. Phase 3 is contracts-only. If you see entity diagrams, redirect.
>
> **PROPOSAL.md save location:** For the workshop, save to a local `hangar-ai-specs/` directory in their working copy. Explain that in production this would be a separate repository with PR-based approval.

### Expected Outputs

- **API contract** (endpoint, method, request body, response body, error codes)
- **BDD scenarios** (minimum 3: happy path, failure path, edge case)
- **PROPOSAL.md stub** (saved to `hangar-ai-specs/`, citing ENG-1.5, ENG-4.4, ENG-11.1)

### Constitutional Gate

**✅ Gate: All Critical Paths Have Gherkin Scenarios**

_Before proceeding to Phase 4, confirm:_
- [ ] API contract is written (not just described — actual endpoint + payload)
- [ ] At least 3 BDD scenarios in valid Gherkin format
- [ ] PROPOSAL.md stub exists on disk with law citations
- [ ] No implementation code has been written

---

## Phase 4: Design — 10 Minutes

> **Workflow Phase:** 4 — Design

### Law Citations

> **ENG-2.1:** Architecture Standards — Architecture decisions must be documented with rationale.
>
> **ENG-6.1 (NON-NEGOTIABLE):** Security Threat Model — Every design must include a security threat model. Unmitigated HIGH threats block progression.
>
> **ENG-11.2:** Proposal Completeness (carry-forward)

### Skill Activated

`skill-spec-governance`

### What Participants Do

1. Paste the Phase 4 Design prompt with their PROPOSAL.md content.
2. Review the AI's design critique: does it identify any law violations? Unmitigated risks?
3. Confirm an ADR (Architecture Decision Record) is filed for any significant design choice.
4. Review the security threat model produced — are HIGH threats mitigated?
5. Update PROPOSAL.md with any design decisions surfaced.

**Note:** Phase 4 is intentionally compressed to 10 minutes in Session 1 because participants are learning the workflow. In production use, architecture review is a dedicated session.

### Instructor Notes

> 🎓 **INSTRUCTOR ONLY**
>
> **Timing:** 10 minutes. Do not let this expand. The goal is to experience the architectural law-check, not conduct a full design review. If participants want to go deeper, note it for Session 2 or post-workshop.
>
> **Key teaching moment:** ENG-6.1 is NON-NEGOTIABLE. The security threat model doesn't need to be exhaustive right now, but it must exist. A common threat for loyalty miles: "What happens if someone manipulates `flightId` to earn miles for flights they didn't take?" — i.e., input validation + authorization checks.
>
> **ADR filing:** Keep it simple in the workshop. An ADR can be a 5-line markdown block: Decision, Status, Context, Consequences, Law Citations. Don't let this become a 2-page document.
>
> **Watch for:** AI assistants sometimes skip the security threat model if not explicitly prompted. Remind participants to check that ENG-6.1 is addressed in the response.

### Expected Outputs

- **AI design critique** acknowledging or flagging PROPOSAL.md
- **ADR** (even a stub) for at least one architecture decision
- **Security threat model** (at minimum: 2 threats identified, mitigation described)
- **PROPOSAL.md updated** with design rationale

### Constitutional Gate

**✅ Gate: No Unmitigated HIGH Threats**

_Before proceeding to Phase 5, confirm:_
- [ ] Security threat model exists (ENG-6.1)
- [ ] All HIGH threats have a documented mitigation
- [ ] At least one ADR filed in `hangar-ai-specs/`

---

## Phase 5: Plan — 15 Minutes

> **Workflow Phase:** 5 — Plan

### Law Citations

> **ENG-2.3:** Vertical Slice Architecture — Work must be organized as thin vertical slices that deliver end-to-end value, not horizontal layers.
>
> **ENG-4.2:** Test Pyramid — Unit tests at the base, integration tests in the middle, contract/E2E tests at the top.

### Skill Activated

`skill-07-vertical-slice-dev`

### What Participants Do

1. Paste the Phase 5 Plan prompt.
2. Review the AI's vertical slice decomposition.
3. Validate: does each slice deliver end-to-end value (not "implement the controller layer")?
4. Review test types listed for each slice — does the AI respect the ENG-4.2 test pyramid?
5. Output: `tasks.md` with slices as checkboxes ordered by dependency.

**For the loyalty miles example, slices might be:**
```
Slice 1: Calculate base miles for a qualifying flight (unit tests only)
Slice 2: Apply status multiplier (Gold, Platinum, Executive Platinum) (unit + integration)
Slice 3: Handle non-qualifying fare classes (unit tests)
Slice 4: Persist miles to member account (integration + contract test)
```

### Instructor Notes

> 🎓 **INSTRUCTOR ONLY**
>
> **Timing:** 15 minutes. The most common mistake here is slices that are too large ("implement the entire miles calculation feature") or too horizontal ("implement the service layer").
>
> **Key teaching moment:** A vertical slice can be implemented, tested, and deployed independently. Ask: "If I gave you only Slice 1, could you ship it?" If not, it's too big.
>
> **Dependency order matters:** Slice 4 (persist miles) depends on Slice 1 (calculate miles). The tasks.md must reflect this dependency.
>
> **Test pyramid check:** If the AI suggests only unit tests for everything, push back. Slice 4 (persistence) must have integration tests. The pyramid isn't optional — it's ENG-4.2.

### Expected Outputs

- **Vertical slice decomposition** (2–4 slices, each end-to-end)
- **`tasks.md`** with slices as checkboxes, ordered by dependency
- **Test types** identified per slice

### Constitutional Gate

**✅ Gate: Implementation Proposal in `hangar-ai-specs/changes/` Approved**

_Before proceeding to Phase 6, confirm:_
- [ ] `tasks.md` exists with at least 2 vertical slices
- [ ] Each slice has named test types (unit/integration/contract)
- [ ] Dependency order is documented
- [ ] PROPOSAL.md updated with slice plan

---

## Phase 6: Build — 60 Minutes (NON-NEGOTIABLE)

> **Workflow Phase:** 6 — Build
>
> ⚠️ **ENG-4.1 IS NON-NEGOTIABLE. NO PARTICIPANT WRITES A SINGLE LINE OF IMPLEMENTATION BEFORE A FAILING TEST EXISTS.**

### Law Citations

> **ENG-4.1 (NON-NEGOTIABLE):** Atomic TDD — The TDD cycle is mandatory. RED → GREEN → REFACTOR → VERIFY → COMMIT → REPEAT. No implementation without a failing test.
>
> **ENG-3.1:** Cyclomatic Complexity ≤ 10 — No method may exceed complexity 10. Checked during REFACTOR phase.
>
> **ENG-3.4:** Single Responsibility Principle — Each class and method has one reason to change. Checked during REFACTOR phase.
>
> **ENG-4.5:** Test Naming Convention — Test methods must follow: `methodName_condition_expectedBehavior`.
>
> **ENG-4.6:** Coverage Threshold — New code must achieve ≥90% test coverage.

### Skill Activated

`skill-06-atomic-tdd`

### The TDD Cycle (Write This on the Whiteboard)

```
RED → GREEN → REFACTOR → VERIFY → COMMIT → REPEAT
```

Each iteration handles **one behavior at a time**. No exceptions.

---

### Full TDD Walkthrough: Loyalty Miles Domain

The example below uses Java. Participants should follow the same cycle in their own stack.

---

#### Step 1 — RED Phase (Write a Failing Test First)

**Prompt to use:**
```
Greenfield Phase 6: Build — Atomic TDD.
Skill: skill-06-atomic-tdd.
Law: ENG-4.1 (NON-NEGOTIABLE — no implementation without failing test first).

I am implementing: Slice 1 — Calculate miles with Gold status multiplier.
Step 1 — RED: Write the failing test first. Test name must follow ENG-4.5: "methodName_condition_expectedBehavior".
Do NOT write implementation yet. Show me only the test. I will confirm RED before you proceed.
```

**Expected test output (Java):**
```java
// File: src/test/java/com/aa/loyalty/MilesCalculatorTest.java

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

**Why this test must fail first:**
- `MilesCalculator` class does not exist yet → compilation failure = RED
- `StatusTier.GOLD` enum does not exist yet → compilation failure = RED
- This is intentional. RED means the test either fails to compile or fails at runtime.

**Instructor action:** Walk through what "RED" means physically:
- Run `./gradlew test` (or `mvn test`)
- Show the failure output: `Cannot find symbol: MilesCalculator`
- That failure IS the gate passing. The test is RED. ✓

---

#### Step 2 — GREEN Phase (Minimum Implementation)

**Prompt to use:**
```
Test confirmed RED. 
Step 2 — GREEN: Write the minimum implementation to make this test pass.
No gold-plating. One failing test → one passing test. 
Show me only the implementation change.
```

**Expected minimum implementation (Java):**
```java
// File: src/main/java/com/aa/loyalty/StatusTier.java
public enum StatusTier {
    STANDARD, GOLD, PLATINUM, EXECUTIVE_PLATINUM
}

// File: src/main/java/com/aa/loyalty/Flight.java
public class Flight {
    private final String flightId;
    private final int baseMiles;

    public Flight(String flightId, int baseMiles) {
        this.flightId = flightId;
        this.baseMiles = baseMiles;
    }

    public int getBaseMiles() { return baseMiles; }
}

// File: src/main/java/com/aa/loyalty/Member.java
public class Member {
    private final String memberId;
    private final StatusTier statusTier;

    public Member(String memberId, StatusTier statusTier) {
        this.memberId = memberId;
        this.statusTier = statusTier;
    }

    public StatusTier getStatusTier() { return statusTier; }
}

// File: src/main/java/com/aa/loyalty/MilesCalculator.java
public class MilesCalculator {
    public int calculateMiles(Flight flight, Member member) {
        if (member.getStatusTier() == StatusTier.GOLD) {
            return (int) (flight.getBaseMiles() * 1.5);
        }
        return flight.getBaseMiles();
    }
}
```

**Key principle:** This implementation handles ONLY the Gold case. It does NOT implement Platinum or Executive Platinum yet. Minimum code to pass one test.

**Instructor action:** Run `./gradlew test`. The single test should pass. GREEN. ✓

---

#### Step 3 — REFACTOR Phase (Check Laws ENG-3.1, ENG-3.4, ENG-4.5)

**Prompt to use:**
```
Test is GREEN.
Step 3 — REFACTOR: Identify any code smell, duplication, or law violation in what we just wrote.
Laws to check: ENG-3.1 (complexity ≤10), ENG-3.4 (single responsibility), ENG-4.5 (test naming).
If clean, say "No refactor needed." If not, show the refactored version.
```

**Expected AI response for this simple case:**
- `ENG-3.1 (CC≤10)`: `calculateMiles` has CC=2 (one if-branch). ✓ Compliant.
- `ENG-3.4 (SRP)`: `MilesCalculator` calculates miles. Single responsibility. ✓ Compliant.
- `ENG-4.5 (test naming)`: `calculateMiles_goldStatus_earns150PercentMultiplier` — method `calculateMiles`, condition `goldStatus`, expected behavior `earns150PercentMultiplier`. ✓ Compliant.
- **Verdict:** No refactor needed for this iteration.

**Note for participants:** Refactor does NOT mean "add more features." It means "same behavior, cleaner code." If the AI suggests adding Platinum support during REFACTOR, use the recovery prompt to stop it.

---

#### Step 4 — VERIFY Phase (Run All Tests)

Run the full test suite — not just the new test. Every test that was passing before must still pass.

```bash
./gradlew test --info
```

Output should show: 1 test passing, 0 failures, 0 errors.

**Instructor note:** This is the anti-regression check. Even with one test, the habit of running the full suite starts now.

---

#### Step 5 — COMMIT Phase

```bash
git add src/
git commit -m "feat(loyalty): calculate miles with Gold status multiplier

- Implements calculateMiles for GOLD StatusTier (ENG-4.1: Atomic TDD)
- Test: calculateMiles_goldStatus_earns150PercentMultiplier
- Coverage: 100% new code (ENG-4.6)
- Law: ENG-4.1 (NON-NEGOTIABLE), ENG-4.5 (test naming)
"
```

---

#### Step 6 — REPEAT (Next Behavior)

Now participants implement Slice 1, behavior 2: Standard (no-multiplier) case.

**Next test:**
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

Repeat the full cycle: RED → GREEN → REFACTOR → VERIFY → COMMIT.

---

### Instructor Notes — Phase 6 (CRITICAL)

> 🎓 **INSTRUCTOR ONLY**
>
> **ENG-4.1 IS NON-NEGOTIABLE. INTERVENE IMMEDIATELY if anyone writes implementation code before a test.**
>
> The intervention script:
> "Stop. ENG-4.1 is non-negotiable. Delete what you just wrote. Before a single line of implementation exists, I need to see a failing test. Show me the test first."
>
> Do not soften this intervention. The law is explicit. The point of the workshop is to internalize this reflex.
>
> **Common violations to watch for:**
> - Participant creates the class file before the test file
> - AI assistant writes implementation "to explain the test" — tell participants to use the RED recovery prompt immediately
> - Participant writes a test that passes immediately (tests their own implementation, not a spec) — this means they wrote implementation thinking first
>
> **TDD cycle timing:** At 60 minutes, participants should complete at minimum:
> - Full RED-GREEN-REFACTOR-VERIFY-COMMIT for behavior 1 (Gold multiplier)
> - RED-GREEN for behavior 2 (Standard, no multiplier)
> - Discussion of behavior 3 (non-qualifying fare class)
>
> **Check coverage at the end:** Even informally — if the class has 3 conditions and they've written 2 tests, coverage is approximately 67%. ENG-4.6 requires 90% new code. They need at least one more test.
>
> **Stack diversity:** Participants on Python/FastAPI should write pytest tests. TypeScript participants should write Jest tests. The TDD cycle is language-agnostic. The naming convention `calculateMiles_goldStatus_earns150PercentMultiplier` is Java convention; for Python it would be `test_calculate_miles_gold_status_earns_150_percent_multiplier`.

### Expected Outputs

- **Failing test** (RED confirmed)
- **Minimum implementation** (GREEN confirmed)
- **Refactor check** (ENG-3.1, ENG-3.4, ENG-4.5 reviewed)
- **All tests passing** (VERIFY confirmed)
- **Git commit** with law citations in commit message
- **At minimum:** 2 complete RED-GREEN-REFACTOR-VERIFY-COMMIT cycles by end of session

### Constitutional Gate

**✅ Gate: All Slices Green; Coverage ≥90% New Code (ENG-4.6)**

_Before proceeding to Phase 7, confirm:_
- [ ] Every test is passing (zero failures)
- [ ] Coverage on new code ≥ 90% (ENG-4.6)
- [ ] Commit message includes law citations
- [ ] No implementation code exists without a corresponding test

---

## Phase 7: Review — Stretch (15 Minutes, If Time Allows)

> **Workflow Phase:** 7 — Review

### Law Citations

> **ENG-6.1 (NON-NEGOTIABLE):** Security — OWASP Top 10 review must be completed before ship.
>
> **BUS-7.1:** Audit Trail — Business-critical decisions must have an immutable audit trail.
>
> **ENG-11.1:** Hangar SDD — All artifacts must be present and correctly filed.

### Skill Activated

`skill-spec-governance`

### What Participants Do

1. Run a constitution compliance review: does the code comply with all laws identified in Phase 2?
2. Check OWASP Top 10 against the API design (ENG-6.1):
   - A01: Broken Access Control — is the `memberId` validated against the authenticated user?
   - A03: Injection — is `flightId` sanitized before database query?
   - A04: Insecure Design — are there rate limits on the calculation endpoint?
3. Verify BUS-7.1 audit trail: is there a record of who calculated miles, when, and what inputs were used?
4. Review PROPOSAL.md completeness against ENG-11.2 checklist.

### Instructor Notes

> 🎓 **INSTRUCTOR ONLY**
>
> **This is a stretch phase.** If Phase 6 ran to time, skip the hands-on portion and walk through the review conceptually with the full group.
>
> **BUS-7.1 teaching moment:** The audit trail is not a log file. It is an immutable, queryable record of business decisions. For loyalty miles: who requested the calculation, what inputs were used, what was the output, what laws governed the calculation. This is an important concept for airline operations (passenger disputes, regulatory audits).
>
> **OWASP connection:** The security threat model from Phase 4 should map directly to OWASP categories. If it doesn't, that's a gap in the threat model. Good teaching moment.

### Expected Outputs

- **Compliance checklist** (law-by-law review)
- **OWASP Top 10 check** (A01, A03, A04 at minimum)
- **BUS-7.1 audit trail** discussion or stub
- **PROPOSAL.md completeness** confirmed against ENG-11.2

### Constitutional Gate

**✅ Gate: Zero P0 Violations; Security Sign-Off**

_Confirm:_
- [ ] No NON-NEGOTIABLE law violations remain
- [ ] OWASP A01, A03 addressed
- [ ] BUS-7.1 audit trail identified in design

---

## Debrief Questions

Ask these five questions to the full group at the end of Session 1 (10 minutes):

1. **The Gate Question:** "At which gate did you feel the most friction? Was that friction useful or was it bureaucratic overhead? How would you distinguish between the two?"

2. **The TDD Question:** "Before today, how many of you routinely wrote the test before the implementation? What is the most common rationalization for skipping it — and does ENG-4.1 accept that rationalization?"

3. **The Law Question:** "Which law in today's session surprised you? Which one do you think your current team most frequently violates without knowing?"

4. **The Prompt Question:** "When did your AI assistant produce something unhelpful or wrong? What prompt pattern fixed it? What does that tell you about how to structure a good law-grounded prompt?"

5. **The Scale Question:** "If every engineer at AA followed this workflow for every greenfield feature, what would change about how we build software? What would get harder? What would get easier?"

---

## Session 2 Bridge

Session 2 covers **Legacy Adoption** — the same constitution applied to existing codebases.

**Key differences participants will encounter in Session 2:**

| Dimension | Session 1 (Greenfield) | Session 2 (Legacy) |
|---|---|---|
| Starting point | Empty project | Existing code, possibly untested |
| Phase 1 (Capture) | Define new problem | Archaeology — understand existing behavior |
| TDD (ENG-4.1) | Write test → write code | Write characterization tests first |
| API contracts | Design from scratch | Discover existing implicit contracts |
| Threat model | Design-time | Runtime analysis of existing vulnerabilities |
| PROPOSAL.md | New file | Refactor proposal — what changes and why |
| Primary skill | `skill-06-atomic-tdd` | `skill-09-refactoring` + `skill-06-atomic-tdd` |

**Bridge question to leave participants with:**
> "You have a 5-year-old Java service with 12,000 lines of code and 40% test coverage. Tomorrow you need to add a new feature. Walk me through the first three things you do before writing a single line of new code."

The answer — using the workflow — is:
1. Phase 1 (Capture): Understand the domain as it exists, not as it was intended.
2. Write characterization tests to lock current behavior (ENG-4.1 still NON-NEGOTIABLE).
3. Phase 2 (Discover): Run the law inventory against the existing code — what violations already exist?

Session 2 starts with the `legacy-rescue-refactor` workflow. Participants should bring a real legacy class from their own codebase if possible.
