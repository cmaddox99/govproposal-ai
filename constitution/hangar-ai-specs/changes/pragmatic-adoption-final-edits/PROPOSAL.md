# Proposal: Pragmatic Adoption Skill — Final Edits

**Status:** 📋 PROPOSE
**Spec ID:** `pragmatic-adoption-final-edits`
**Skill:** `02-constitutional-companion` (currently v2.17.6)
**Laws:** ENG-1.2, ENG-11.1, ENG-12.1
**Branch:** `proposal/pragmatic-adoption-final-edits`

Catch-all proposal for targeted edits identified during post-v2.17.1 review
of the pragmatic adoption skill. Amendments will be added here as the review
proceeds. See `tasks.md` for the running task list.

---

## Known Items at Opening

### Item 1 — `followed_by` ID bug *(moved to separate PR)*

This bug was discovered during review but is independent of pragmatic adoption content.
It has been moved to its own proposal and branch: `fix/followed-by-skill-ids`.
See `hangar-ai-specs/changes/followed-by-skill-ids/PROPOSAL.md`.

---

## Amendments

---

## Amendment 2 — Seam Narrowness Detection (Phase 3a)

**Problem:** The Phase 3a seam inventory directly defines what "within the seam
boundary" means for the sociable testing invariant in Phase 3c onwards. A seam
defined too narrowly silently widens the permitted mock zone — collaborators that
should be real end up outside the seam and can be mocked, producing shallow
characterization tests. Phase 3a currently has no mechanism to catch this before
the seam is confirmed.

**Two additions to Phase 3a:**

**A — Mock-necessity test in the selection heuristic:**
After "seams almost always span more than one file," add:

> "If writing a characterization test for this seam would require mocking any
> class, that class belongs inside the seam — widen it. A seam is correctly sized
> when you can characterize its full behavior using only real objects."

Also make the sociable invariant connection explicit: the files in the seam
inventory define the no-mock boundary for Phase 3c onwards.

**B — Narrowness validation gate:**
After the user confirms a seam but before the AI writes `phase-1-archaeology.md`,
add a check: if the confirmed seam contains only one file (or is a Micro-level
seam), the AI must name the direct collaborators of the entry point and ask:

> "This seam covers a single class. Its direct collaborators are: [list].
> To characterize its behavior, would you need to mock any of these? If yes,
> they belong inside the seam.
> — Widen to include [collaborators]?
> — Or proceed with the single-class scope (you accept that collaborators will
>   be outside the sociable invariant boundary)?"

**Artifact:** `02-pragmatic-adoption.md` — Phase 3a only; version → 2.17.3

**Problem:** Two gaps in the skill will cause the AI to drift toward solitary
(mockist) tests during Phase 3e refactoring:

1. The Phase 3c bullet "No mocking of internal collaborators" applies only to
   characterization tests. It is silent on tests written during Phase 3e, giving
   the AI implicit permission to mock extracted collaborators in new unit tests.

2. The Phase 3e retirement check says "covered by targeted unit tests" — an AI
   will interpret this as: extract class → write isolated test with mocks →
   retire the facade-anchored characterization test. This is the opposite of the
   intended sociable approach.

**Solution:** Replace the per-phase mock rules with a single seam-wide invariant
that applies to every test written in every phase:

> **No collaborator within the seam boundary is ever mocked.**
> Mocking is only permitted at true system boundaries: database, HTTP, external
> services, clock, random, messaging. Everything inside the seam stays real.

With this invariant, tests may enter at **any public API within the seam** —
outer facade, extracted class, wherever it is most natural — and they are
automatically sociable because collaborators within the seam are always real.

**Specific changes:**
- Phase 3c: replace bullet "No mocking of internal collaborators" with the
  invariant callout. Add that tests may enter at any level within the seam.
- Phase 3e retirement check: replace "covered by targeted unit tests" with
  "covered by tests that introduce no new mocks within the seam."

**Artifact:** `02-pragmatic-adoption.md` — Phase 3c and Phase 3e only; version → 2.17.2

---

## Amendment 3 — God Class / God Method Decomposition Guidance (Phases 3b and 3e)

**Problem:** When a seam contains a god class or god method (many responsibilities,
high complexity violations, many lines), the existing skill leaves three critical
gaps:

1. **No target design sketch (Phase 3b):** The Phase 3b decision table records a
   REFACTOR verdict but does not require a decomposition plan. Without knowing which
   classes will be extracted and what responsibility each carries *before* writing
   characterization tests, TDD cycles thrash — the AI extracts opportunistically and
   then reorganizes mid-stream.

2. **No extraction ordering (Phase 3e):** Phase 3e says "one violation at a time" but
   does not guide the order. For god class decomposition, extracting a class before
   its dependencies are extracted forces rework. The correct order is
   leaf-first (topological sort of the dependency graph).

3. **No stopping condition (Phase 3e):** The skill does not name the expected final
   form of a god class after decomposition. The AI may over-extract (delete the entry
   class and break the characterization test anchor) or under-extract (leave residual
   logic in the original class). The natural stopping condition is the
   *thin coordinator* pattern: the original class becomes a pure delegation hub
   with no logic of its own, only constructor injection and delegation calls.

**Three additions:**

**A — Phase 3b: God class detection + Target Architecture section**

When the Phase 3b scan reveals a god class (heuristic: file exceeds the ENG-3.1
complexity limit, has PHASE_GATE violations, AND contains two or more identifiable
responsibility clusters), the agent must produce a **Target Architecture** block in
`phase-2-decision.md` before proceeding to Phase 3c:

```
## Target Architecture — [God Class Name]

| Extracted Class | Responsibility (one sentence) | GRASP/SOLID/DDD Pattern | Depends On |
|---|---|---|---|
| `PricingEngine` | Calculates line-item prices from rate tables | GRASP Information Expert | `RateTable` (extracted) |
| `DiscountPolicy` | Applies promotional rules to a basket | GRASP Creator, Strategy | — |
| `OrderCoordinator` | Delegates to the above; replaces `OrderService` | GRASP Controller, Facade | `PricingEngine`, `DiscountPolicy` |

Entry point (coordinator): `OrderCoordinator` — characterization tests anchor here throughout.
Extraction order (leaf-first): DiscountPolicy → PricingEngine → OrderCoordinator
```

The user must confirm this design before the agent proceeds to Phase 3c. If the user
wants to change the design, iterate here — not during TDD cycles in Phase 3e.

**B — Phase 3e: Extraction ordering callout**

Before the TDD cycle loop, add:

> **God class extraction order:** Work leaf-first — extract the class with no
> dependency on any other *planned-but-not-yet-extracted* class first. The
> coordinator (original class thinned to delegation) is always extracted last.
> Check off each extracted class in the Target Architecture table as it is
> completed.

**C — Phase 3e: Thin coordinator stopping condition**

After the TDD cycle loop, add a stopping condition callout:

> **God class done when:** The original class contains only:
> - Constructor injection of its collaborators
> - Delegation calls (one-liners that call a collaborator method)
> - No conditional logic, no instance-variable state beyond injected collaborators
>
> When this is true, the class has become a thin coordinator (Facade / GRASP
> Controller). Characterization tests entered at this coordinator are still valid —
> they now exercise the full network of extracted classes. Do not delete the
> coordinator; it is the stable public API.

**Artifact:** `02-pragmatic-adoption.md` — Phase 3b and Phase 3e; version → 2.17.4

---

## Amendment 4 — Reposition as Constitutional Companion (Whole-Skill Reframe)

**Problem:** The skill is framed as an adoption tool — once adoption is complete,
it hands off to other workflows. But the target audience (developers unfamiliar with
characterization testing, GRASP/SOLID, Feathers-style refactoring, and seam thinking)
doesn't graduate out of needing guidance just because `AGENTS.md` now exists. The
other workflows assume this knowledge; developers without it will get lost immediately.
Additionally, the gateway frames the Guided (Pragmatic) path as a "lighter" option
for constrained situations, when it should be the recommended default — and the Full
workflow should be positioned as requiring prerequisite knowledge the target audience
typically lacks (though they often don't realize it).

The target audience does not self-identify as needing help. They consider themselves
competent programmers. The UX must not suggest otherwise — it must frame guided
adoption as the smart, recommended default for anyone new to constitutional techniques.

**Five changes:**

**A — Skill title and purpose statement**

Title: `Skill: Pragmatic Adoption` → `Skill: Constitutional Companion — Guided Development`

Purpose rewrites to lead with the permanent companion role and explicitly names the
techniques so developers unfamiliar with them self-select without feeling judged:

> The guided entry point for any developer who wants to use the Hangar AI Constitution
> effectively — whether adopting for the first time, continuing an adoption in progress,
> or working on an already-adopted project and not sure which constitutional technique
> applies next. Teaches seam discovery, characterization testing, GRASP/SOLID/DDD
> design patterns, and Feathers-style safe refactoring by applying them step-by-step
> to your actual codebase. If any of those terms are unfamiliar, this is the right
> place to start — regardless of how long you have been programming.

**B — Step 0b gateway: flip path ordering and labels**

Path A (Guided) becomes the first option and recommended default.
Path B (Full) becomes the second option, explicitly positioned as requiring
prerequisite knowledge.

**C — Step 0a Priority 2: adoption complete → Companion Mode**

Replace "offer next workflows" with an interactive Companion Mode dialog that asks
what the developer is working on today and routes them into the right guided phase
with technique explanations.

**D — "When to Invoke": inclusive single statement**

Replace the three-pattern trigger table with a single inclusive statement that names
the unfamiliar techniques, plus a brief "who this is NOT for" guard pointing
experienced self-directed teams to the specialized skills directly.

**E — Frontmatter triggers: add ongoing-development and technique-curiosity phrases**

Add phrases that developers without constitutional knowledge would naturally say
when working on code: "my service class is getting too big", "I have a SonarQube
violation I don't understand", "what is a characterization test", "I want to improve
my code quality", "I don't know where to start", "help me refactor this", etc.

**Artifact:** `02-pragmatic-adoption.md` — skill title, purpose, Step 0a Priority 2,
Step 0b, "When to Invoke", frontmatter triggers; version → 2.17.5

---

## Known Item 2 — Skill File and ID Rename (FINAL-06)

Amendment 4 changed the skill's title and purpose but left the filename and skill ID
using the old "pragmatic-adoption" identity. The file and ID should match the new name.

**Changes required:**

| Artifact | From | To |
|---|---|---|
| Filename | `02-pragmatic-adoption.md` | `02-constitutional-companion.md` |
| Skill ID (frontmatter) | `skill-02-pragmatic-adoption` | `skill-02-constitutional-companion` |
| `index.yaml` `file:` field | `02-pragmatic-adoption.md` | `02-constitutional-companion.md` |
| `index.yaml` `name:` field | `Pragmatic Adoption` | `Constitutional Companion` |
| `workflows/adoption.md` | `02-pragmatic-adoption` reference | `02-constitutional-companion` |
| `docs/guides/adoption/pragmatic-adoption.md` | skill ID references | updated |
| `hangar-ai-specs/changes/llm-skill-behavioral-testing/` | skill file path references | updated |
| `hangar-ai-specs/changes/pragmatic-adoption-final-edits/PROPOSAL.md` | artifact references | updated |

**Archived proposals** (`hangar-ai-specs/archive/`, `hangar-ai-specs/changes/iterative-adoption-large-codebases/`)
are historical records — leave unchanged.

---

## Amendment 5 — Trigger Audit: Remove Collisions, Tighten Scope, Fix Step 0b Loop

**Problem:** After Amendment 4 expanded the trigger set, three issues emerged:

1. **Collisions with skill-09 (Refactoring):** Triggers `"help me refactor this"`,
   `"I want to improve my code quality"`, and `"what are SOLID principles"` directly
   overlap with skill-09's indexed triggers (`refactor`, `improve code`, `code quality`,
   `SOLID principles`). These steal routing from users who are already oriented and
   want targeted refactoring help.

2. **Over-broad triggers:** `"very busy"` matches any user mentioning time pressure
   in any context. `"how do I get started"` matches any introductory question.
   Neither signals constitutional orientation need specifically.

3. **Step 0b loop (unresolved from earlier analysis):** Path B still recommended
   `"Adopt the Hangar AI Constitution"` as the handoff phrase. This is semantically
   equivalent to skill-02's own `"adopt the constitution"` trigger — with LLM
   semantic routing the user cycles back to this skill instead of reaching the
   adoption workflow. Fix: replace with `"Set up constitutional governance in my repo"`,
   a workflow alias absent from skill-02's trigger list. Add fallback aliases
   (`"Initialize hangar-ai-specs"`, `"Create AGENTS.md"`) in the presentation text
   for resilience.

**Three changes:**

**A — Remove skill-09 collisions; replace with orientation-specific phrases**

Removed: `"help me refactor this"`, `"I want to improve my code quality"`,
`"what are SOLID principles"`

Added: `"I want to write better code but don't know where to start"`,
`"how do I approach improving this codebase"`, `"I don't know which technique to use"`

These replacements signal orientation need (the companion's job) rather than
execution intent (skill-09's job).

**B — Drop over-broad triggers**

Removed: `"very busy"` (replaced by already-present `"no time for adoption"`),
`"how do I get started"` (replaced by already-present `"get started with adoption"`)

**C — Fix Step 0b loop**

Replace handoff phrase `"Adopt the Hangar AI Constitution"` with
`"Set up constitutional governance in my repo"`. Add note in the presentation text
explaining that this phrase routes to the adoption workflow (not back to this skill)
and offering two fallback aliases for resilience.

**Also added:** Orientation-intent comment block at top of trigger list explaining the
routing philosophy — triggers capture orientation need only; specialized skills own
execution.

**Artifact:** `02-pragmatic-adoption.md` — frontmatter triggers and Step 0b; version → 2.17.6

---

## Amendment 6 — User Opt-Out Notice

**Problem:** Experienced developers who have graduated past needing guided development
keep getting routed into the Constitutional Companion via trigger phrase matching. There
is no documented mechanism for permanently suppressing auto-triggering without modifying
a repo file (which would affect the whole team).

**Discovery:** The Copilot CLI loads `~/.copilot/copilot-instructions.md` at session
start as a user-scoped instruction file. It is never committed to version control and
applies across all repositories for that user.

**Two additions:**

**A — Skill intro:** One-line `> **Opt-out:**` callout in the purpose block pointing
to the guide's opt-out section.

**B — Guide:** New "Opting Out of Auto-Triggering" section at the top of
`docs/guides/adoption/pragmatic-adoption.md` with the exact
`~/.copilot/copilot-instructions.md` snippet and a note that it is user-scoped and
never committed to version control.

**Artifact:** `02-constitutional-companion.md` (skill intro); `docs/guides/adoption/pragmatic-adoption.md` (new section) ✓ fd70b72

---

## Amendment 7 — Guide Title: Pragmatic Adoption → Constitutional Companion

**Problem:** The guide's H1 title `Pragmatic Adoption` reflects the old framing.
After Amendment 4 repositioned the skill as a permanent Constitutional Companion,
the guide title no longer matches the skill's identity. "Pragmatic Adoption" still
attracts the right audience (developers who want iterative, practical help) but does
not surface the companion concept to readers who have already been redirected here.

**Change:** H1 title in `docs/guides/adoption/pragmatic-adoption.md`:

`# Pragmatic Adoption` → `# Constitutional Companion — Pragmatic Adoption Guide`

Filename unchanged (`pragmatic-adoption.md`) — preserves discoverability for the
target audience and avoids breaking existing links.

**Artifact:** `docs/guides/adoption/pragmatic-adoption.md` — H1 title only

---

## Amendment 8 — Restore "Adopt the Hangar AI Constitution" as Step 0b Handoff; Prune Adoption-Intent Triggers

**Problem:** Amendment 5 replaced the Step 0b handoff phrase with
`"Set up constitutional governance in my repo"` to avoid a routing loop — the concern
being that `"Adopt the Hangar AI Constitution"` (the canonical phrase from the adoption
guide) was too close to skill-02's own `"adopt the constitution"` trigger.

The correct fix is not to use a non-canonical phrase; it is to remove from skill-02 all
triggers that would semantically intercept `"Adopt the Hangar AI Constitution"` before
it reaches the adoption workflow. The companion's true triggers are **orientation need**,
not adoption intent. A developer who says "Adopt the Hangar AI Constitution" knows what
they want — they should reach the workflow, not this skill.

**Two changes:**

**A — Prune adoption-intent triggers from skill frontmatter and index.yaml**

Removed the entire "First-time / plain-language adoption intent" group (11 phrases):
`adopt the constitution`, `adopt the constitution into my project`,
`I want to adopt the constitution`, `how do I adopt the constitution`,
`get started with adoption`, `start adopting`, `begin adoption`,
`adopt this project`, `adopt my project`, `add the constitution to my project`,
`set up the constitution`.

Retained 5 first-time phrases specific enough not to intercept the canonical phrase:
`pragmatic adoption`, `constitution setup`, `onboard my project to the constitution`,
`new project adoption`, `where do I start with the constitution`.

Updated trigger comment block to document the routing boundary explicitly.

**B — Restore Step 0b handoff to canonical phrase**

`"Set up constitutional governance in my repo"` → `"Adopt the Hangar AI Constitution"`

Removed the compensating note ("if you find yourself back at this screen, try...") and
the fallback aliases — they were only needed to work around the routing loop, which is
now resolved at the trigger level.

**Artifact:** `02-constitutional-companion.md` — frontmatter triggers, trigger comment,
Step 0b; `index.yaml` — trigger list sync

---

## Amendment 9 — Add Adoption Decision and Guided Companion Trigger Groups

**Problem:** Two categories of developer intent are not captured by the current trigger
list:

1. **Adoption decision/guidance** — developers asking *which* adoption path to take.
   These are question-form phrases (`"how do I"`, `"which should I"`, `"what is the
   difference"`) that should route to the companion because it presents the gateway
   choice between guided and full adoption. They are distinct from `"Adopt the Hangar
   AI Constitution"` (an execution command) and do not conflict with the adoption
   workflow trigger.

2. **Guided companion mode** — developers who want to be *taught and walked through*
   constitutional techniques, not just assisted. The key differentiator from skill-09
   (Refactoring) triggers (`refactor`, `improve code`, `code quality`) is a
   guided-learning prefix: `"guide me through"`, `"walk me through"`, `"show me how"`,
   `"coach me"`. Bare execution intent stays with skill-09; learning intent routes here.

**Two new trigger groups:**

**A — Adoption decision/guidance (7 phrases)**

```yaml
# Adoption decision — which path? (question form, not execution command)
- "which adoption process should I use"
- "how do I adopt the constitution"
- "what adoption path should I choose"
- "should I use pragmatic or full adoption"
- "what is the difference between adoption paths"
- "help me choose how to adopt"
- "I don't know which adoption approach to use"
```

**B — Guided companion mode (8 phrases)**

```yaml
# Guided companion — wants to be taught, not just assisted
- "show me how to use the constitution better"
- "guide me through using the constitutional AI"
- "can you guide me through refactoring my code"
- "walk me through my next task"
- "coach me on constitutional development"
- "help me learn how to work with the constitution"
- "show me how to approach this ticket"
- "I want to be walked through my code changes"
```

**Collision watch item:** `"can you guide me through refactoring my code"` contains
`refactor`, which is a skill-09 indexed trigger. The `"guide me through"` prefix is
expected to disambiguate in LLM semantic routing (learning intent vs. execution intent),
but this phrase should be monitored. If routing misbehaves, soften to
`"can you guide me through improving my code constitutionally"`.

**Artifact:** `02-constitutional-companion.md` — frontmatter triggers (two new groups);
`index.yaml` — trigger list sync

---

## Amendment 10 — Trigger Audit: Remove Over-Broad and Redundant Phrases

**Problem:** A review of the full trigger list identified 13 phrases that fall into one
of three problem categories:

1. **Too broad — no constitutional signal:** Phrases that would match everyday
   development conversation with no indication the user is thinking about constitutional
   technique. These steal routing from general-purpose assistance or other skills.

2. **Command-oriented interference:** Phrases whose execution intent overlaps with
   specialized skills (skill-09 Refactoring) that should own that routing.

3. **Near-duplicates:** Phrases that express the same intent as an existing trigger
   with only minor wording variation, adding noise without adding coverage.

**13 removals across four groups:**

*Ongoing development (5 removed — too broad):*
- `"help me work on my code"` — matches any coding question
- `"I want to add a feature to existing code"` — normal development, no constitutional signal
- `"I don't know where to start"` — too general, matches any domain
- `"where do I start on this ticket"` — no constitutional signal
- `"help me with my next coding task"` — too general

*Technique-curiosity (2 removed):*
- `"I don't know which pattern to use"` — near-duplicate of retained `"I don't know which technique to use"`
- `"help me design this better"` — too broad, no constitutional signal

*Complex constraints (3 removed):*
- `"can't fix all sonar issues"` — SonarQube support question without adoption framing
- `"my project is too big"` — too broad, no constitutional signal
- `"iterative constitution adoption"` — near-duplicate of retained `"adopt iteratively"`

*Orientation (3 removed — too broad):*
- `"what happened to my project"` — matches git, deployments, anything
- `"what are these files for"` — no constitutional signal
- `"how do lookups work"` — no constitutional context

**Retained in each group:** All phrases with a specific constitutional signal remain
unchanged. The two `"SonarQube"` phrases, all `AGENTS.md`/`hangar-ai-specs` orientation
phrases, and all technique-curiosity phrases naming specific constitutional patterns are
unaffected.

**Artifact:** `02-constitutional-companion.md` — frontmatter triggers (13 removals);
`index.yaml` — trigger list sync

**Amendment 10 — Addendum: Add 11 Orientation-Specific Phrases**

A second pass identified three groups of high-signal phrases that are missing. All
use question or decision form and carry specific constitutional context — no collision
with skill-09 or skill-06 execution triggers.

*Adoption uncertainty (4 phrases — externally directed or pre-decision):*
- `"what is the best way to do a constitutional adoption"`
- `"can you help me figure out how to adopt the constitution"`
- `"what is the easiest way to adopt the constitution so I can get back to coding"`
- `"my team says I need to adopt the constitution, where do I start"`
- `"what does adopting the constitution actually involve"`
- `"what do I get when I adopt the constitution"`
- `"someone told me to use the hangar AI constitution, what do I do"`

*Code quality / technical debt (2 phrases — decision form, no execution collision):*
- `"I don't know where to start improving my code quality"`
- `"help me decide where to start reducing my technical debt"`
- `"my codebase has a lot of issues and I don't know which to tackle first"`

*Post-adoption confusion (3 phrases — Companion Mode scenario):*
- `"I adopted the constitution but don't know what to do next"`
- `"the constitution is set up but I'm not sure how to work with it"`
- `"what should I be doing differently now that I've adopted the constitution"`

**Artifact:** `02-constitutional-companion.md` — frontmatter triggers (11 additions);
`index.yaml` — trigger list sync

---

## Amendment 11 — Phase 3b Verdict Dialog: Explain Before Asking

**Problem:** Phase 3b asks the user to choose REFACTOR, REWRITE, or EXTEND before
explaining what those choices mean. REFACTOR and REWRITE are everyday words with
intuitive meanings; EXTEND is not — it sounds like "add to" (normal development) rather
than signalling its actual constraint: the existing code is deliberately left frozen and
new behavior sprouts or wraps alongside it. Renaming the verdict would just trade one
ambiguous label for another. The correct fix is to move the explanation to the moment
of decision.

**Change:** Before recording the verdict, the agent now presents all three options with
a one-sentence constraint description and a *use when* condition:

> **Which approach fits this seam?**
>
> - **REFACTOR** — keep the existing code; improve its structure using Atomic TDD.
>   *Use when:* the logic is correct but poorly structured.
>
> - **REWRITE** — characterize the contract, replace from scratch, delete the original.
>   *Use when:* the code is too tangled to work within safely.
>
> - **EXTEND** — leave existing code completely frozen; sprout or wrap new behavior
>   alongside it using Feathers safe-modification techniques.
>   *Use when:* the code is high-risk or untouchable and the task is adding capability.

The verdict decision table and EXTEND Feathers technique callout are unchanged — they
record and elaborate after the user has already understood the choice.

**Artifact:** `02-constitutional-companion.md` — Phase 3b only

---

## Amendment 12 — Phase 3a: Learning-Rich Seam Candidates

**Problem:** The Phase 3a seam discovery protocol presents 2–4 starter candidates at
different granularities, but does not help the user identify which seams will teach
them the most. A developer new to constitutional techniques benefits most from starting
with classes that concentrate multiple design problems — these are the richest learning
opportunities, not just the biggest violations.

**Change:** In Step 2 (Present starter seams), the agent also identifies up to 3
**Learning-Rich seam candidates** using four heuristics:
- High cyclomatic complexity or ENG-3.1 violations (god class / god method)
- Multiple identifiable responsibility clusters
- High fan-out (heavily coupled to collaborators)
- High git churn (frequently changed — worth improving)

These are presented in a separate named block with honest framing: not "worst" code,
but classes that will teach the most about seam thinking, sociable testing, and
responsibility decomposition. The block includes an effort estimate:

> Expect each to be a **half-day to full-day activity** to get into good shape —
> they are the most rewarding but also the most challenging places to start.

The existing starter seam candidates and narrowness validation gate are unchanged.
Learning-Rich candidates are an additional option presented alongside them.

**Artifact:** `02-constitutional-companion.md` — Phase 3a Step 2 only

---

## Amendment 13 — Phase 3b Verdict Dialog: Add Frequency Hints

**Problem:** The verdict dialog (Amendment 11) explains what each option means but
gives no indication of how common each choice is. A developer who is unsure will
hesitate rather than defaulting to the right answer.

**Change:** One-word frequency hints added inline to each verdict:

- **REFACTOR** → `(common, default to this)`
- **REWRITE** → `(rare)`
- **EXTEND** → `(ultra rare)`

These hints steer uncertain developers toward REFACTOR without requiring them to
reason through all three options every time.

**Artifact:** `02-constitutional-companion.md` — Phase 3b verdict dialog only ✓ 24d619a

---

## Amendment 14 — New Skill: Design Quality Assessment (skill-10) + Phase 3f Integration

**Status:** ⛔ OUT OF SCOPE — moved to separate proposal.

**Reason:** The design quality scorecard (SOLID/GRASP/Encapsulation/Cohesion/
Complexity/Coverage scored 0–10 with examples and deltas across iterations) is
a valuable idea but is too large and complex to embed in the companion skill.
It warrants its own dedicated skill (`skill-10-design-quality-assessment`) with
its own proposal, scoring rubric, artifact format, and trigger phrases. Embedding
it here would make the companion skill harder to maintain and harder for the AI
to execute reliably within a single session. A future proposal should be opened
under `hangar-ai-specs/changes/design-quality-assessment/` to design and
implement skill-10 independently.

**Problem:** SonarQube tracks rule violations but does not assess object design quality.
After each adoption iteration there is no record of whether the design actually improved
— only whether violations decreased. Developers need a design trajectory they can point
to across iterations.

**Solution:** Create a new dedicated skill (`10-design-quality-assessment`) that
produces a design quality delta report. Making it a standalone skill (rather than
embedding it in the companion) allows it to be invoked independently and reused by
skill-09 (Refactoring) or other skills.

**New skill: `agent-skills/skills-by-domain/development-practices/10-design-quality-assessment.md`**

- Skill ID: `skill-10-design-quality-assessment`
- Placed at number 10 (natural gap between skill-09 Refactoring and skill-11 Mutation Testing)
- Invokable standalone OR called from Phase 3f of the companion
- Scans a confirmed seam/class cluster and produces `evidence/design-quality-delta.md`

Assessment covers per class:
- GRASP patterns present before and after
- Responsibility count (SRP — how many distinct concerns)
- Fan-out (how many classes directly instantiated or called)
- Cohesion (qualitative — do methods use most of the class's fields?)
- Overall design score 1–10 (holistic AI judgment with brief justification)

**Scoring rubric:**

| Score | What it means |
|-------|---------------|
| 9–10 | Clear GRASP patterns, 1 responsibility per class, low fan-out, high cohesion |
| 7–8  | Good patterns, minor coupling or SRP drift |
| 5–6  | Some patterns applied, multiple responsibilities remain |
| 3–4  | Few patterns, significant coupling, 2–3 responsibility clusters |
| 1–2  | God class/method, no patterns, high fan-out |

**Output artifact — `evidence/design-quality-delta.md`:**

```markdown
| Class | GRASP Before | GRASP After | Responsibilities Before→After | Fan-out Before→After | Design Score |
|---|---|---|---|---|---|
| OrderService | none | Controller, Facade | 5 → 1 | 12 → 3 | 8/10 |
| PricingEngine | — (new) | Information Expert | — → 1 | — → 2 | 9/10 |
```

**Phase 3f integration in companion:** After the SonarQube delta step, add:
> Invoke `skill-10-design-quality-assessment` to produce
> `evidence/design-quality-delta.md` for this iteration.

**Not yet implemented.** Will be a separate commit once design is confirmed.
