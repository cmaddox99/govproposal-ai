# Proposal: Constitutional Companion — Updates & Fixes

**Status:** ✅ IMPLEMENT — CCU-01 through CCU-43N complete; CCU-42F/G-GRASP/H/I BLOCKED (Type 2/3 changes needed)
**Spec ID:** `constitutional-companion-updates`
**Skill:** `02-constitutional-companion` (v2.24.0 — amended 2026-05-13)
**Laws:** ENG-1.2, ENG-4.1, ENG-11.1, ENG-12.1
**Branch:** `proposal/constitutional-companion-updates`

Live-use feedback on `skill-02-constitutional-companion`. Amendments will be
added here as problems and improvement ideas are identified during real
adoption sessions.

---

## Amendments

---

## Amendment 1 — Phase ordering confusion, SonarQube dual-role, hard STOP behavior

**Source:** Live session observation — AI thrashed visibly when user typed "continue"
after governance setup completed.

**Four problems identified:**

### A — Task checklist phase order misled AI into wrong SQL dependencies

The generated `tasks.md` listed phases 3a → 3b → 3c → **3d → 3e** → 3f in order,
causing the AI to build SQL deps with 3d (SonarQube) before 3a (Archaeology) — then
had to self-correct mid-session with visible confusion.

**Fix:** Reorder tasks.md template to: 3a → 3b → 3c → 3e → 3d (parallel, unlocks 3f) → 3f.
Add a phase order note explaining the dependency chain explicitly.

### B — SonarQube appeared in two places with no clear distinction

- Step 2 pre-flight check referenced `sonarqube-baseline.md` as "Phase 2b baseline capture"
- Phase 3d is the actual per-iteration SonarQube setup dialog

The AI conflated the two, creating confusion about whether SonarQube was part of
governance setup or iteration work.

**Fix:** Rename Step 2 reference to "SonarQube pre-flight check" with explicit note
"This is NOT Phase 3d setup." Pre-flight only checks existence; 3d provisions.
Also clarify the pre-flight check label in the silent check list.

### C — Hard STOP after governance caused "session ends here" with no escape

The instruction `⛔ STOP after Phase 3 + first proposal creation` caused the AI to
declare the session complete. When the user typed "continue" the AI had to pivot
awkwardly with no guidance in the skill about what to do next.

**Fix:** Replace hard STOP with a checkpoint dialog that presents the human with two
choices: "Continue now into Phase 3a" or "Start fresh next session." Await explicit
choice before proceeding.

### D — Phase 3a–3f overview diagram didn't show dependency chain

The ASCII overview didn't show that 3d is parallel to 3e, or that 3f depends on both.
AI had to infer this, getting it wrong first.

**Fix:** Redraw the overview with arrows showing the checkpoint gates and an explicit
SQL dependency chain note for agents doing task tracking.

**Files modified:**
- `agent-skills/skills-by-domain/development-practices/02-constitutional-companion.md`


---

## Amendment 2 — Stack detection discarded, no session-1 preview, re-scan waste

**Source:** Live session observation — AI detected Java/Spring Boot from `pom.xml` in
its internal reasoning but did not surface this to the user and did not carry it
forward. The gateway also gave no expectation of what session 1 would actually do.

### A — Detected stack silently discarded

The AI found the technology stack during Step 0a but neither told the user nor recorded
it for use in Step 2.1 avatar resolution — forcing a redundant re-scan later.

**Fix:** Add a stack-detection lookup table to Step 0a (build file → stack mapping).
Instruct the AI to record the result and carry it forward to Step 2.1. Explicitly
prohibit re-scanning at Step 2.1.

### B — Gateway dialog didn't confirm detected stack to user

The user had no idea the AI already knew the technology stack. Surfacing this in the
gateway dialog builds trust and allows the user to correct a misdetection early.

**Fix:** Add a one-liner at the top of the gateway dialog:
*"I can see this is a {detected_stack} project — I'll use the `{technology_avatar}`
avatar when we begin. If that's wrong, just say so and I'll adjust."*

### C — No session-1 expectation-setting in Path A description

Users who type "adopt the constitution into this repo" expect immediate code action.
Neither path description said that session 1 is governance scaffolding only (5–10 min,
no code read or changed), causing confusion when the STOP checkpoint arrived.

**Fix:** Add a "Session 1 preview" callout inside Path A's description explaining
what happens and offering to continue immediately or defer to next session.

**Files modified:**
- `agent-skills/skills-by-domain/development-practices/02-constitutional-companion.md`

---

## Amendment 3 — Vague avatar name, noisy status table

**Source:** Live session observation — AI reported "java technology avatar" without
specifying framework level; status table showed ❌ for "hangar-ai-constitution/ adjacent"
which is a migration flag meaningless to new adopters.

### A — Java avatar not refined to framework level

The stack detection table mapped `pom.xml` → "Java" but didn't tell the AI to refine
further. For a Spring Boot project `java-spring` is the correct avatar with Spring-specific
rules; bare `java` would miss them. Same issue applies to Node (React vs Express).

**Fix:** Add a "Refine to avatar" column to the stack detection table. Java: check for
`spring-boot` in build file → `java-spring`, otherwise `java`. Node: check for `react` →
`react`; `express`/`fastify` → `node`; otherwise `typescript`.

### B — "hangar-ai-constitution/ adjacent" ❌ shown to user unnecessarily

This and the `openspec/` check are migration flags for old projects — not actionable
items for new adopters. Showing them as ❌ in the status table creates confusion
("why is this missing? do I need to fix it?").

**Fix:** Move both checks to a silent-only pre-flight note. They are never shown in
the user-facing status table.

**Files modified:**
- `agent-skills/skills-by-domain/development-practices/02-constitutional-companion.md`

---

## Amendment 4 — Product avatar resolved when deferred, AI inventing extra artifacts

**Source:** Live session observation — AI read `pom.xml`, listed Java source files,
analyzed package structure, and self-selected `network-planning-optimization` as the
product avatar despite the explicit skill instruction to defer it. Also created an
`adoption-check.md` artifact not in the prescribed governance list.

### A — Product avatar resolved during Step 2 (should always be deferred)

The skill says "Resolve technology avatar only. Set `product_avatar: none — deferred`"
but the AI overrode this with curiosity-driven source analysis. This adds unnecessary
file operations and makes an architectural decision (product domain) without human
confirmation.

**Fix:** Add a hard-limits callout box immediately after the Step 2 action table with
an explicit prohibition list: no source file reads, no package analysis, no product
avatar selection, no extra artifacts. Include a self-check sentence: "If you find
yourself reading source files or choosing a product avatar during Step 2 — stop."

### B — AI invented `adoption-check.md` outside prescribed artifact list

The prescribed governance artifacts are: AGENTS.md, hangar-ai-specs/ directories,
project-rules.md, adoption-iteration-1/PROPOSAL.md, adoption-iteration-1/tasks.md.
The AI created an additional `adoption-check.md` not in this list. This is benign
but represents scope creep outside the governance template.

**Fix:** The hard-limits callout (Amendment 4A) explicitly prohibits creating any
artifact not in the prescribed list — this covers both product avatar analysis and
artifact invention.

**Files modified:**
- `agent-skills/skills-by-domain/development-practices/02-constitutional-companion.md`

---

## Amendment 5 — Product avatar in templates, missing Progress header, inferred architecture

**Source:** Inspection of governance artifacts created in `/Users/948120/projects/oraa-connect-assist`.

### A — Product avatar hardcoded in AGENTS.md and project-rules.md

The adoption workflow (`workflows/adoption.md`) templates use `{product_avatar}` as a
required field. When the skill delegated to that workflow ("Run `workflows/adoption.md`
Phases 1–3"), the AI resolved the product avatar to fill the template — overriding the
explicit deferral instruction. This is a template design trap.

**Fix:** Remove the delegation to `workflows/adoption.md`. Replace with explicit inline
templates for AGENTS.md and project-rules.md inside the skill — both templates use
`none — deferred` as the literal product avatar value, not a `{product_avatar}` slot.
The AI cannot accidentally fill in a deferred value when the literal is already there.

### B — `## Progress: 0 / N` not in prescribed tasks.md template

The AI added a Progress header which is good UX, but it was freelancing. Standardising
it in the template ensures every project gets it consistently.

**Fix:** Add `## Progress: 0 / 6 complete` to the tasks.md template.

### C — project-rules.md architecture section inferred from source

The AI populated the Architecture section with layer names (domain/, application/,
ingress/, egress/) inferred from source analysis during Step 2 — which the hard limits
prohibit. The template should use a placeholder so the AI has nothing to infer.

**Fix:** project-rules.md template uses `[TO BE FILLED IN DURING PHASE 3A ARCHAEOLOGY]`
for the Architecture section and a comment on Local Extensions: fill in after Phase 3a.

**Files modified:**
- `agent-skills/skills-by-domain/development-practices/02-constitutional-companion.md`

---

## Amendment 6 — Priority 3/4 ambiguity, stack row outside status table

**Source:** Live session — AI debated Priority 3 vs 4 for a bare `hangar-ai-specs/`
directory; stack detected row appeared below the table instead of inside it.

### A — Priority 3 vs 4 ambiguity for partially-present artifacts

The Priority 3 description ("artifacts present but stale or incomplete") was too vague.
An empty `hangar-ai-specs/` with only a bare `archive/` folder caused the AI to debate
internally before choosing correctly. Concrete examples eliminate the ambiguity.

**Fix:** Expand Priority 3 description with examples: `hangar-ai-specs/` exists but
`AGENTS.md` is missing; `hangar-ai-specs/` is empty or has only bare directories;
`project-rules.md` is missing. Expand Priority 4 similarly: neither `AGENTS.md`
nor `hangar-ai-specs/` exists.

### B — Stack detected row fell outside status table

Amendment 2 (CCU-06) added the stack confirmation to the gateway dialog but did not
explicitly specify that the stack must appear as a row in the status table. The AI
placed it as a free-standing line below the table.

**Fix:** Add an explicit status table template to Step 0a with "Stack detected" as the
mandatory last row. Instruction: "Always include the Stack detected row — never place
it outside the table as a separate line."

**Files modified:**
- `agent-skills/skills-by-domain/development-practices/02-constitutional-companion.md`

---

## Amendment 7 — pom.xml read for version, wrong version recorded, unexplained placeholders

**Source:** Live session — AI read `pom.xml` during Step 2 to get Spring Boot version
but extracted `3.1` instead of the correct `3.5`; PROPOSAL.md template placeholders
looked like forgotten values to a confused developer.

### A — pom.xml read during Step 2 to extract framework version (prohibited)

The AI read `pom.xml` to get the Spring Boot version despite the hard limits prohibiting
source file reads during Step 2. It also got the wrong answer (3.1 vs 3.5). The
framework version is not needed for governance setup — it belongs in Phase 3a.

**Fix:** Change `{detected_framework}` in the project-rules.md template to
`{build_tool} — version to be confirmed in Phase 3a`. Add inline note: "do not read
pom.xml or build.gradle to extract version numbers."

### B — Constitution path calculation triggered pom.xml read

The `{relative_path_to_hangar-ai-constitution}` placeholder caused the AI to open
`pom.xml` as a proxy for understanding the project layout. The relative path can be
calculated purely from directory names.

**Fix:** Add inline note to the AGENTS.md template: "Calculate from directory names
only — do NOT read pom.xml or any source file to determine this."

### C — PROPOSAL.md placeholders looked like forgotten values

`[Bounded Context Name]`, `[context name]`, `[to be confirmed in Phase 3a]` are
intentional but a developer seeing these for the first time might think the AI failed
to fill them in.

**Fix:** Add a one-liner callout at the top of the PROPOSAL.md template:
"Placeholders in [brackets] are filled in during Phase 3a Archaeology — they are
intentional, not forgotten."

**Files modified:**
- `agent-skills/skills-by-domain/development-practices/02-constitutional-companion.md`

---

## Amendment 8 — Commit order reversed: tasks.md updated after commit

**Source:** Live session — AI committed all artifacts then updated tasks.md, leaving
tasks.md as an uncommitted change in the working tree. The recorded commit hash was
correct but the tasks.md update itself was never committed.

**Root cause:** The "Check off `3a` in `tasks.md`" instruction had no subsequent
commit instruction and no ordering constraint. The AI committed what it had ready
(the archaeology artifacts), then updated tasks.md as a follow-up — forgetting to
commit again.

**Fix:** Add an explicit commit block after every "Check off" instruction (3a, 3c, 3d)
with a template commit message and a hard rule: "tasks.md must be updated BEFORE the
commit — not after. The commit hash recorded in tasks.md must match the commit that
includes the tasks.md update itself."

**Also:** Fixed the uncommitted tasks.md in the live adoption repo (commit `e9d85c5`).

**Files modified:**
- `agent-skills/skills-by-domain/development-practices/02-constitutional-companion.md`

---

## Amendment 9 — All phase-gate checkpoints missing "type X to continue" instruction

**Source:** Live session — after Phase 3a, AI said "Per ENG-1.2, I'm stopping here and
awaiting your confirmation before proceeding to Phase 3b" with no instruction on what
to type. Novice AI users have no idea how to respond to that.

**Audit of all stop points:**
| Stop point | Previous state |
|---|---|
| Step 2 end (governance scaffold) | Had choice dialog but no "type X" instruction |
| Phase 3a end | **No dialog at all** — straight into gate classification table |
| Phase 3b end | "Once user confirms verdict" — no stop/prompt |
| Phase 3c end | Had report format but no "type `continue`" |
| Phase 3e end | "Say 'run SonarQube now'" hint — not a checkpoint |
| Phase 3f end | "Shall I move to archive?" — rhetorical, not a checkpoint |
| Step 6 (end of iteration) | "STOP — await human confirmation" — no instruction |

**Fix:**
1. Added **"Checkpoint Dialog Standard"** block at top of Step 3 defining the exact
   format every stop must follow, with explicit prohibition on "awaiting your
   confirmation" alone.
2. Updated all 7 stop points with explicit checkpoint dialogs containing:
   - ✅ What was just done
   - 📋 What comes next (one sentence)
   - Explicit "type `continue`" instruction
   - Explicit "type `stop here`" option
   - Invitation to ask questions before proceeding
3. Added commit blocks to Phase 3b and Phase 3f (were also missing).

**Files modified:**
- `agent-skills/skills-by-domain/development-practices/02-constitutional-companion.md`

---

## Amendment 10 — Phase 3b: architecture designed before verdict chosen; two gates collapsed

**Source:** Live session — AI said "The REFACTOR approach is the default and most
appropriate here" in its internal reasoning, then designed a full 8-class Target
Architecture, then asked the user "Which verdict do you **confirm**?" — not "choose".
The user was rubber-stamping a pre-decision rather than making a real choice.

**Root causes:**
1. The god class detection block ("Before proceeding to Phase 3c, produce a Target
   Architecture block") immediately follows the verdict options with no explicit stop
   between them. The AI reads this as: assess, design, then confirm all at once.
2. "The user must confirm this design" is passive — no explicit `ask_user` stop.
3. "confirm" framing in ask_user implies the AI already decided.

**Fix:**
- Restructured Phase 3b into two explicit sequential gates:
  - **Gate 1 (Verdict):** Present 3 options + brief recommendation → ⛔ STOP →
    `ask_user "Which verdict do you choose?"` → wait
  - **Gate 2 (Architecture, REFACTOR + god class only):** Present Target Architecture
    → ⛔ STOP → `ask_user "Type confirmed or change..."` → iterate → wait
- Added explicit ⛔ prohibition: "Do NOT design the Target Architecture before the
  user chooses a verdict."
- Changed "confirm" → "choose" in Gate 1 framing.
- Added conditional header to Gate 2: "Skip this gate entirely if REWRITE or EXTEND."

**Note:** The Target Architecture the AI produced was actually high quality (correct
GRASP patterns, leaf-first extraction, good class boundaries). The problem was
sequencing, not content.

**Files modified:**
- `agent-skills/skills-by-domain/development-practices/02-constitutional-companion.md`

---

## Amendment 11 — tasks.md "check off" creates duplicate rows instead of editing in-place

**Source:** Live session — after Phase 3b, tasks.md had:
```
- [x] 3b — ... ✓ f40a31e
- [ ] 3b — ...         ← ghost row — AI added new line instead of editing existing
```
`## Progress: 2/6` was also miscounted.

**Root cause:** "Check off `3b` in `tasks.md`" is ambiguous. The AI interpreted it as
"add a checked entry" rather than "edit the existing unchecked entry in-place".

**Fix:**
1. Added a ⛔ tasks.md editing rule block immediately after the tasks.md template:
   "edit the existing `- [ ]` line in-place — do NOT add a new line; also increment Progress count."
2. Changed every "Check off `XY` in `tasks.md`" instruction to say explicitly:
   "Edit the existing `- [ ] XY` line in-place: change `[ ]` to `[x]` and append the
   commit hash. Increment `## Progress`. Do not add a new row."
   — applies to: 3a, 3b, 3c, 3d (done and deferred), 3f

**Also:** Fixed the live ghost row in `oraa-connect-assist` tasks.md (`2b54c9e`).

**Files modified:**
- `agent-skills/skills-by-domain/development-practices/02-constitutional-companion.md`

---

## Amendment 12 — Missing commit after Step 2 governance scaffold

**Source:** Live session — AI created AGENTS.md, hangar-ai-specs/, project-rules.md,
PROPOSAL.md, and tasks.md then jumped straight to the checkpoint dialog without
committing. All 5 governance artifacts were left uncommitted in the working tree.

**Root cause:** The Step 2 STOP block had no commit instruction before the checkpoint
dialog. Every other phase gate has a commit block; Step 2 did not.

**Fix:** Added a `git commit` block immediately before the Step 2 STOP checkpoint:
```
git add -A && git commit -m "chore(adoption): governance scaffold — constitutional adoption bootstrap
- Add AGENTS.md ({technology avatar}, ...)
- Add hangar-ai-specs/ structure
- Add adoption-iteration-1/PROPOSAL.md (status: PROPOSE)
- ...
Per ENG-11.1, ENG-1.2"
```

**Also fixed:** Committed the governance scaffold in the live `oraa-connect-assist`
repo (`31bcd66`).

**Files modified:**
- `agent-skills/skills-by-domain/development-practices/02-constitutional-companion.md`

---

## Amendment 13 — Seam candidates not numbered; format inconsistent

**Source:** Live session — the closing prompt says "Type `use seam N`" but the skill
never instructs the AI to number the seam candidates. In some runs seams were numbered;
in others they were described with only names. Also, the presentation format varied
between bullet lists and tables across runs.

**Fix:**
1. Added explicit numbering mandate: "Number each candidate sequentially (Seam 1,
   Seam 2, …) — the user will refer to them by number."
2. Added a fixed sub-field template that every candidate must follow:
   Behavior captured / Files in scope / Violation tier / Entry point / Rationale
3. Tightened closing prompt: "Type `use seam N` (e.g., `use seam 1`)" — the
   example makes it unambiguous for novice users.
4. Fixed the hardcoded "seam 2" and "seam 3" references in the closing prompt to
   use generic "Seam N".

**Files modified:**
- `agent-skills/skills-by-domain/development-practices/02-constitutional-companion.md`

---

## Amendment 14 — Hash stamp is chicken-and-egg; PROPOSAL.md title not filled in

**Source:** Live session — two issues in Phase 3a completion:

**Issue A:** Instruction "append the commit hash. Then commit" is impossible atomically.
The AI correctly solved it with two commits (work commit + hash-stamp micro-commit),
but had to invent this approach since the skill was silent. The contradictory rule
"tasks.md must be updated BEFORE the commit" and "append the commit hash" cannot both
be satisfied in one commit.

**Fix A:** Made the two-step process explicit at all 5 check-off points (3a, 3b, 3c,
3d, 3f): (1) edit tasks.md to `[x]`, commit work; (2) `git rev-parse --short HEAD`,
append ` ✓ {hash}`, micro-commit. Also updated the tasks.md editing rule to describe
this pattern. Removed the contradictory "BEFORE the commit" rule.

**Issue B:** PROPOSAL.md title still showed `[Bounded Context Name]` after Phase 3a.
The skill's "Before starting" instruction said "Fill in the bounded context name" but
the AI only updated the Status and skipped the title. The placeholder is correct to
keep in the TEMPLATE — the bug is the AI ignoring the instruction.

**Fix B:** Made the "Before starting" instruction more explicit with a concrete example:
"replace `[Bounded Context Name]` with the confirmed seam/bounded context name
(e.g., `Adoption Iteration 1 — Hold Time Calculation Engine`)".

**Note:** The template placeholder `[Bounded Context Name]` in the skill is correct
and intentional — it is NOT a literal value to keep.

**Files modified:**
- `agent-skills/skills-by-domain/development-practices/02-constitutional-companion.md`

---

## Amendment 15 — Phase 3a leaves two placeholders unfilled (CCU-27)

**Trigger:** Live run of Phase 3a completed correctly (seam inventory written,
collaborators identified, commit made) but two placeholders were left unfilled:
1. `PROPOSAL.md` title still `# Proposal: Adoption Iteration 1 — [Bounded Context Name]`
   — AI updated `Status` to IMPLEMENT but missed the title.
2. `project-rules.md` `## Architecture` section still `[TO BE FILLED IN DURING PHASE 3A
   ARCHAEOLOGY]` — no instruction anywhere in Phase 3a told the AI to fill it in.

**Root causes:**
- A: "Before starting" bundled two edits (status + title) into one sentence; AI only
  did the first. The note "placeholders are intentional" in the live PROPOSAL.md was
  mis-read as permission to leave them empty.
- B: The `## Architecture` placeholder exists in the template but Phase 3a had zero
  instruction to fill it in.

**Fixes:**
- A: Separated status update and title fill-in into two explicit numbered steps with a
  ⛔ clarifying that the note means "fill them in HERE".
- B: Added an explicit "Fill in `project-rules.md`" step with a mini-template just
  before the Phase 3a commit block. Added ⛔ prohibiting leaving the placeholder.

**Files modified:**
- `agent-skills/skills-by-domain/development-practices/02-constitutional-companion.md`

---

## Amendment 16 — PROPOSAL.md Scope body never filled in; product avatar never resolved (CCU-28, CCU-29, CCU-30)

**Trigger:** Full audit of all placeholders in skill templates revealed three that have
no explicit fill-in instruction at the phase where they should be completed:

**CCU-28 (AMEND-16A) — PROPOSAL.md Scope body + Problem Statement (Phase 3a)**
- `- Bounded context: [to be confirmed in Phase 3a Archaeology]`
- `- Seams: [to be identified in Phase 3a]`
- `Adopt the Hangar AI Constitution into the [context name] bounded context.`
All three have no fill-in instruction in Phase 3a. The "Before starting" block only
covered Status and title (Amendment 14). Extended it to cover all five PROPOSAL.md
edits needed at Phase 3a start.

**CCU-29 (AMEND-16B) — PROPOSAL.md Approach line (Phase 3b)**
- `- Approach: [REFACTOR | REWRITE | EXTEND — to be decided in Phase 3b]`
Phase 3b records the verdict in phase-2-decision.md but never updates PROPOSAL.md.
Added explicit "Also edit PROPOSAL.md: change Approach line" instruction immediately
after the phase-2-decision.md write step.

**CCU-30 (AMEND-16C) — Product avatar deferral never resolved**
Both AGENTS.md and project-rules.md say `none — deferred (will be added after Phase 3a
Archaeology)` but no phase ever prompts the user to resolve it. Added a one-time
optional `ask_user`-style prompt at the end of Phase 3a archaeology: name a product
avatar to set it in both files, or type `skip` to leave deferred permanently this session.

**Files modified:**
- `agent-skills/skills-by-domain/development-practices/02-constitutional-companion.md`

---

## Amendment 17 — Phase 3c/3d UX gaps from live session (CCU-31, CCU-32, CCU-33)

**Trigger:** Live Phase 3c+3d run revealed three UX gaps that caused friction without
any skill instruction to prevent them.

**CCU-31 (AMEND-17A) — Environment workaround not documented**
AI diagnosed Java 25/21 mismatch, fixed with `JAVA_HOME=...` inline, then moved on.
No instruction exists to capture environment workarounds. Next session re-diagnoses
from scratch. Fix: added "Environment workaround rule" callout after the "Run the full
test suite" step in Phase 3c — if any non-default env setting is required to build/test,
record it in `project-rules.md ## Environment Notes` before continuing.

**CCU-32 (AMEND-17B) — SonarQube single-token friction**
Choosing Option A (SonarQube server) triggered 3 extra ask_user interactions because
the skill only asked for one credential. PROJECT_ANALYSIS_TOKEN can scan but cannot
read metrics — so the AI had to ask again after the scan failed to return data. Fix:
added an upfront two-credential note immediately after "If A, B, or C chosen" explaining
the two-token pattern and instructing the AI to ask for both in a single prompt.

**CCU-33 (AMEND-17C) — // --- comment dividers trigger SonarQube false positives**
AI used `// --- parseDurationToMinutes: ... ---` section headers in the characterization
test file. SonarQube flagged these as "commented-out code" — a false positive that
pollutes the delta scan. The skill had no comment style guidance. Fix: added a
"Comment style" bullet to the characterization test naming rules: use plain `//` or
`@Nested`/`@DisplayName`; avoid `// ---` dividers with code-like content.

**Files modified:**
- `agent-skills/skills-by-domain/development-practices/02-constitutional-companion.md`

---

## Amendment 18 — Continuous Refactoring Loop (CCU-34)

**Trigger:** Phase 3e/3f live session revealed that refactoring was mechanically correct
but provided no per-refactoring proposals, no task lists, and no teaching moments. The
user wanted a never-ending, proposal-driven refactoring cycle decoupled from adoption.

**Core design change:** Adoption now ends at Phase 3c (characterization). Refactoring
moves to a separate Phase 4 continuous loop driven by `refactoring-backlog.md`.

**CCU-34A — Adoption ends at Phase 3c**
The tasks.md template changes from 6 tasks (3a/3b/3c/3d/3e/3f) to 3 tasks (3a/3b/3c).
The Phase 3c checkpoint archives the proposal and presents a three-path choice:
- `characterize` → run Phase 3c on another seam
- `refactor` → enter Phase 4 loop and pick a backlog entry
- `stop` → pause; backlog is saved

**CCU-34B — Refactoring backlog seeded at Phase 3b**
Phase 3b end now creates `hangar-ai-specs/refactoring-backlog.md` with one row per
identified refactoring. Rows start as `Characterized? = ❌ not yet` / `Status = BLOCKED`.
When Phase 3c completes for a seam, the backlog updates: `✅ {N} tests` / `PROPOSED`.

**CCU-34C — Per-refactoring proposals (Phase 4)**
Each backlog entry becomes a separate proposal folder: `hangar-ai-specs/changes/ref-{id}-{slug}/`.
Contains: `PROPOSAL.md` (problem/pattern/alternatives/scope) and `tasks.md` (R1 RED →
R2 GREEN → R3 REFACTOR → R4 VERIFY → R5 COMMIT).

**CCU-34D — Characterization gate**
Phase 4 blocks any refactoring on an uncharacterized seam with an explicit routing message.
The agent never silently skips the gate.

**CCU-34E — Characterization test invariant**
If any characterization test goes RED during a Phase 4 TDD cycle, the agent MUST fix
the refactored code — NOT the test. This invariant appears in the R4 task and in the
TDD cycle instructions.

**CCU-34F — Three supported paths**
Path A: characterize all seams first → refactor later.
Path B: characterize one seam → refactor it → next seam.
Path C: pick from backlog → gate auto-routes to Phase 3c if needed.

**CCU-34G — Phase 3d/3e/3f restructured**
Phase 3d (SonarQube) is now optional, presented before first refactoring of a seam —
not during adoption. Phases 3e and 3f are removed and replaced by Phase 4. SonarQube
delta is optional after any refactoring or batch.

**CCU-34H — design-rationale.md moved to Phase 4**
The two-section design-rationale format (team lead overview + junior/mid detailed
explanation with alternatives) is now part of Phase 4's TDD cycle, not Phase 3e.

**Files modified:**
- `agent-skills/skills-by-domain/development-practices/02-constitutional-companion.md`

---

## Amendment 19 — Mutation Hardening Integration into Phase 4 (CCU-35)

**Status:** PROPOSE

**Trigger:** Original design intent for mutation testing was never realized in practice.
During live Phase 4 testing, mutation testing was invisible — no async runs, no per-cycle
score tracking, no seam-done gate, and no natural-break prompts. The result: refactoring
cycles completed without test strength ever improving toward the ENG-4.11 ≥70% target.

**Root cause analysis:**
1. Mutation tools (Pitest, Stryker) take minutes to run — they must be async, never blocking
2. Phase 3c records a baseline score but makes no offer to run in the background
3. Phase 4 R4 VERIFY only checks characterization tests pass — mutation score is absent
4. Seam-clean detection is purely backlog-based — no mutation score gate
5. The `## Mutation Testing Progress` ladder in project-rules.md is never consulted during Phase 4
6. Natural-break coaching messages exist in project-rules.md but are disconnected from Phase 4's `stop` checkpoint

**Design intent (restated):**
- Mutation tests run *alongside* characterization, never blocking the user
- Test strength increases incrementally over refactoring cycles
- Natural pauses (`stop`) are the primary opportunity to run longer mutation sessions
- A seam is not "Done" until mutation score ≥ 70% (ENG-4.11); the backlog makes this visible
- Mutation hardening is a first-class backlog entry type, not a side note

---

### CCU-35A — Phase 3c: Async mutation baseline offer

**Gap:** After line/branch coverage is recorded, Pitest/Stryker is run synchronously
(blocking) or silently skipped. The user has no option to run it in the background.

**Fix:** Immediately after recording line coverage, offer an async mutation run:

> *"Mutation testing can take a few minutes. I can kick off Pitest now in the background
> — you won't need to wait. The score will be recorded automatically when it completes.
> Or I can skip it and record the baseline next time you have a break.*
> *→ Type `run mutation` to start it now (background).*
> *→ Type `skip mutation` to defer until a natural break."*

If `run mutation`: launch the scoped Pitest command as a detached background process.
Record the exact command in `phase-3-characterize.md` under `## Mutation Run Command`
so the user can re-run manually if the session ends before it completes.

When the run completes: record the score in `project-rules.md ## Mutation Testing
Progress` and `phase-3-characterize.md`. Announce the result with the ENG-4.10
exemption note (no minimum at baseline — it is just the starting point).

If `skip mutation`: record `mutation_score: DEFERRED` in `phase-3-characterize.md`.
The per-session check-in at Phase 4 `stop` will surface this (CCU-35E).

---

### CCU-35B — Refactoring backlog: MUTATION entry type

**Gap:** The backlog only tracks structural REFACTOR entries. Mutation hardening is
invisible — it is never surfaced as selectable work.

**Fix:** Add a `Type` column to `refactoring-backlog.md` (REFACTOR | MUTATION).
MUTATION entries are added automatically in two situations:
1. When Phase 3c completes and mutation baseline is below 70%
2. When all REFACTOR entries for a seam complete and score is still < 70%

Example row:
```
| REF-007 | TimeCalculator | YES 42 tests | MUTATION | Hardening: 34% to >=70% | ENG-4.11 | PENDING |
```

MUTATION entries follow the same characterization gate as REFACTOR entries.

---

### CCU-35C — Phase 4 R4: Per-cycle mutation delta (async, non-blocking)

**Gap:** Phase 4's R4 VERIFY only checks characterization tests are GREEN. Mutation score
is never tracked during refactoring cycles — there is no sense of progress toward 70%.

**Fix:** After R4 passes (all char tests GREEN), add an optional async R4b:

> *"All {N} characterization tests GREEN. Want me to run a mutation delta for {seam}?
> (Current score: {X}%. Background run — you can proceed to R5 immediately.)*
> *→ Type `run mutation` to start the background run.*
> *→ Type `skip` to proceed to R5 now."*

R5 is NOT gated on mutation score. When the run completes, announce the delta and
update `## Mutation Testing Progress`. Show a running trajectory:
```
{seam} mutation trajectory: 31% -> 38% -> 45% -> ... -> 70% target
```

---

### CCU-35D — Seam-clean gate: mutation score required for "Done"

**Gap:** When all REFACTOR entries complete, the skill declares "Seam fully refactored"
regardless of mutation score. A seam can be silently closed at 20%.

**Fix:** When all REFACTOR backlog entries for a seam are COMPLETE, check mutation score:

**If mutation score ≥ 70% (or MUTATION entry COMPLETE):**
Declare seam fully refactored AND mutation-hardened. Suggest next seams.

**If mutation score < 70% (or DEFERRED):**
Do NOT declare the seam done. Auto-add a MUTATION backlog entry and present:

> *"All structural refactorings done for {seam}. Mutation score: {X}% (target: ≥70%).*
> *I've added a mutation hardening entry to the backlog (REF-{id}). You can:*
> *→ Type `refactor` to pick it next (recommended — seam work is still warm)*
> *→ Type `other seams` to move on and return to mutation hardening later*
> *→ Type `stop` to pause — the PENDING entry will be here next session"*

The user is never hard-blocked, but is always informed and always has a clear path.

---

### CCU-35E — Natural break detection: proactive mutation offer at `stop`

**Gap:** When the user types `stop`, the session ends silently. The coaching messages
in project-rules.md exist but are never surfaced.

**Fix:** When the user types `stop` at any Phase 4 checkpoint, before saving state:
Check `## Mutation Testing Progress` for any seam with score < 70% and at least
one completed refactoring cycle. If found, offer a background run before stopping:

> *"Before you go — {seam} mutation score is {X}% (target: ≥70%). Perfect time to kick
> off Pitest in the background while you are away.*
>
> *Command: `mvn pitest:mutationCoverage -Dpit.targetClasses="{package}.*"`*
>
> *→ Type `run mutation then stop` — I'll start the run and give you the process details.*
> *→ Type `stop` again — skip for now; mutation entry is in the backlog."*

---

### CCU-35F — MUTATION entry tasks.md template

A MUTATION backlog entry uses a 5-step tasks.md (M1–M5):

```markdown
# Tasks: REF-{id} — Mutation Hardening: {seam}

**Type:** MUTATION | **Current score:** {X}% | **Target:** >=70% (ENG-4.11)

## Progress: 0 / 5 complete

- [ ] M1 — RUN: launch scoped mutation tool (background ok):
  `mvn pitest:mutationCoverage -Dpit.targetClasses="{package}.*"`
  Start and proceed — results recorded when complete.
- [ ] M2 — REVIEW: list ALL surviving mutants; classify each:
  KILL (behavior gap, must add a test) or ACCEPT (equivalent/dead, document in register)
- [ ] M3 — ADD TESTS: one RED->GREEN Atomic TDD cycle per KILL mutant.
  Do NOT modify existing characterization tests.
  If any characterization test goes RED: fix the refactored code, NOT the test.
- [ ] M4 — VERIFY: run ALL characterization tests and new mutation-kill tests, all GREEN
- [ ] M5 — COMMIT and update backlog:
  Score >=70% -> COMPLETE (seam mutation-hardened)
  Score <70%  -> PARTIAL ({Y}%); add iteration row and loop back to M1
```

---

### Files to modify
- `agent-skills/skills-by-domain/development-practices/02-constitutional-companion.md`

### Laws
- ENG-4.10 — characterization tests are transitional scaffolding; exempt from threshold at baseline
- ENG-4.11 — ≥70% mutation score for general code (≥85% for critical paths)

**Files modified:**
- `agent-skills/skills-by-domain/development-practices/02-constitutional-companion.md`

---

## Amendment 20 — Panel Review Defect Fixes (CCU-36)

**Source:** 5-person panel review (2 rounds): Alex Chen (Java Architect), Morgan Reyes
(First-Time Adopter), Pat Sullivan (Constitutional Law Expert), Jordan Kim (AI Behavioral
Engineer), Sam Rodriguez (Team Lead / Practitioner).

**Three critical defects and seven significant defects identified.**

---

### CCU-36A — CRITICAL: Phase 3b ordering bug

**Problem:** The `refactoring-backlog.md` seeding block appears AFTER the Phase 3b commit
block. An AI reading linearly will commit `phase-2-decision.md` BEFORE creating the
backlog. The instruction at the end of the seeding block ("Commit the backlog alongside
the phase-2-decision.md commit above — already covered") is unreachable by a forward-reading
AI because the commit already happened.

**Fix:** Move the backlog seeding block to BEFORE the commit block so the single commit
covers both `phase-2-decision.md` and `refactoring-backlog.md`. Update the final line of
the seeding block from "already covered" to a note that both artifacts are included in the
commit below.

---

### CCU-36B — CRITICAL: Restart detection claimed but not written

**Problem:** Step 0a Priority 1 says "Use the existing restart-detection logic already in
this skill" — but no such logic exists anywhere in the skill. A developer resuming
mid-adoption has no explicit protocol.

**Fix:** Replace the vague reference with a concrete 5-step restart protocol inline in
Priority 1's action cell.

---

### CCU-36C — CRITICAL: ENG-4.10 and ENG-4.11 missing from `laws.implements` frontmatter

**Problem:** Both laws are cited extensively (Phase 3c, Phase 4 mutation tasks) but are
not declared in `implements`. RAG routing agents looking for the mutation-testing skill
will not find this skill. Also: `amended` date and version not updated for Amendments 18–19.

**Fix:** Add ENG-4.10 and ENG-4.11 to `implements`. Bump version to 2.20.0. Update
`amended` date. Add Phase 4 loop to `followed_by`.

---

### CCU-36D — SIGNIFICANT: Step 6 iteration report has stale "TDD tests" row

**Problem:** The iteration report table says `{N} characterization + {N} TDD` — but
adoption now ends at Phase 3c (characterization only). There are no TDD tests during
adoption. Stale remnant from old Phase 3e workflow.

**Fix:** Change to `{N} characterization` only.

---

### CCU-36E — SIGNIFICANT: PROPOSAL.md artifact table lists stale SonarQube delta artifact

**Problem:** The adoption PROPOSAL.md template includes a row for `SonarQube delta |
evidence/sonarqube-delta.md`. Phase 3f was removed. Delta is now optional in Phase 4,
not an adoption artifact. An AI will attempt to create this file during adoption.

**Fix:** Remove the SonarQube delta row from the artifact table. Keep SonarQube baseline
(which is still created in Phase 3d before first refactoring).

---

### CCU-36F — SIGNIFICANT: Governance scaffold commit message says `0/6 tasks`

**Problem:** The commit message template in Step 2 says
`Add adoption-iteration-1/tasks.md (0/6 tasks)` — but the tasks.md template now has
3 tasks (3a/3b/3c only, since CCU-34). Misleads the developer and any reviewer.

**Fix:** Change `0/6 tasks` → `0/3 tasks`.

---

### CCU-36G — SIGNIFICANT: "God class" used in Phase 3a but not defined in Key Definitions

**Problem:** "god class" appears in Phase 3a seam discovery heuristics (before Phase 3 Key
Definitions table) but is not in the glossary. A first-time adopter sees the term without
any definition.

**Fix:** Add a "God class" row to the Key Definitions table in Phase 3.

---

### CCU-36H — SIGNIFICANT: Seam-clean mutation check missing third case

**Problem:** Lines ~1651–1663 handle only two cases: (a) score ≥70% or MUTATION COMPLETE,
and (b) score <70% AND no MUTATION entry exists yet. A third case is missing: a MUTATION
entry already exists but is PARTIAL or IN PROGRESS. The agent has no instruction for
that state and may loop or add a duplicate entry.

**Fix:** Add an explicit third branch: "If a MUTATION entry for this seam already exists
and is PARTIAL or IN PROGRESS — do not add a duplicate. Show the existing entry and invite
the user to continue it."

---

### CCU-36I — SIGNIFICANT: Phase 4 has no terminal "all done" state

**Problem:** The infinite loop instruction says "if the backlog is empty, offer to run
Phase 3c on an uncharacterized seam to find more" — but what if ALL seams are characterized
AND the backlog is truly empty (all entries COMPLETE)? The agent has no terminal message.
The loop instruction as written cannot exit gracefully, leaving the user with no sense
of completion.

**Fix:** Add a terminal state: when the backlog is empty AND all seams are characterized
(no `❌` rows anywhere), present a completion message instead of offering more Phase 3c.

---

### CCU-36J — SIGNIFICANT: R5 does not archive per-refactoring proposal folder

**Problem:** After completing a Phase 4 refactoring, R5 commits and updates the backlog
but never archives the `hangar-ai-specs/changes/ref-{id}-{slug}/` folder. Over time,
`changes/` accumulates stale completed proposals. Also means the `Completed Refactorings`
table has no traceable archive path for audit purposes (ENG-6.7).

**Fix:** Add an archive step to R5: move the completed proposal folder to
`hangar-ai-specs/archive/ref-{id}-{slug}/` as part of the R5 commit. Update the backlog
row's commit column to include the archive path for traceability.

---

### CCU-36K — MINOR: Duplicate "Path B — Self-Directed Full Adoption" section heading

**Problem:** The "Path B" section heading and its ⛔ STOP block appear twice (~lines 295
and 320), creating structural ambiguity that confuses AI document parsing.

**Fix:** Remove the duplicate heading block.

---

### Files to modify
- `agent-skills/skills-by-domain/development-practices/02-constitutional-companion.md`

### Laws
- ENG-4.10 — characterization tests are transitional scaffolding
- ENG-4.11 — ≥70% mutation score threshold
- ENG-6.7 — audit trail for completed refactorings

---

## Amendment 21 — Panel Review Moderate Findings (CCU-37)

**Source:** 5-person panel review Round 2 — moderate confidence findings (M1–M8).

---

### CCU-37A — Pitest timing claim misleading for larger seams

**Problem:** Phase 3c and the MUTATION M1 task both say "typically < 1 min scoped."
For seams with 50+ classes this can take 5–10 minutes. Developers who trust the estimate
lose confidence in the skill when reality diverges.

**Fix:** Change to "typically fast for small seams; may take several minutes for larger
seams (50+ classes)." Apply in Phase 3c mutation baseline note and M1 task.

---

### CCU-37B — Dead code exception too narrow

**Problem:** The dead code coverage exemption says "dead branches, defensive throws that
can never be triggered, impossible null guards." Real legacy Java has more uncoverable
patterns: `catch` blocks for exceptions that are declared-throws but never thrown by the
implementation, legacy initializer blocks unreachable by design. These leave developers
stranded at the 100% gate with no guidance.

**Fix:** Expand the exemption to "provably never-executed code" with a broader examples
list.

---

### CCU-37C — Spring Boot entry-point guidance missing

**Problem:** Phase 3c says "Tests may enter at any public API within the seam." On a
Spring Boot project the natural entry is the `@Service` layer, not `@RestController`.
Entering through a controller requires a full `MockMvc`/`@SpringBootTest` web context —
slow, fragile, and couples tests to HTTP serialization. No guidance exists for this
extremely common stack choice.

**Fix:** Add a Spring Boot callout in the Phase 3c sociable testing section.

---

### CCU-37D — Phase 4 Step 2: no error handling for invalid ID input

**Problem:** Step 2 prompts the user to type an ID but gives the agent no instruction
if the user types a COMPLETE, BLOCKED, or nonexistent ID.

**Fix:** Add an explicit re-prompt path for invalid input.

---

### CCU-37E — Phase 4 Step 1: BLOCKED seams invisible to user

**Problem:** Step 1 displays only PROPOSED/PENDING/IN PROGRESS rows (not BLOCKED). If
all entries for a seam are BLOCKED (nothing characterized), that seam is completely
invisible. The user doesn't know characterization would unlock it.

**Fix:** Add a footer note when BLOCKED seams exist: "N seam(s) with only uncharacterized
entries not shown — type `characterize` to unlock them."

---

### CCU-37F — design-rationale.md path rule too brief for reliable AI execution

**Problem:** The instruction "or the active changes folder if adoption is still open"
is too vague. An AI will either always use `archive/` or always use `changes/`. There
is no rule for how to know which state applies.

**Fix:** Replace with an explicit two-case rule keyed on whether the proposal folder
is in `changes/` or `archive/`.

---

### CCU-37G — Minimum Viable Session table buried; not referenced from gateway

**Problem:** Time-constrained developers (the primary audience) won't find the
Minimum Viable Session table because the gateway (Step 0b) never references it.

**Fix:** Add a one-line hint in Step 0b after the path choices.

---

### CCU-37H — ENG-4.12 (Legacy Rescue 90%) not mentioned

**Problem:** ENG-4.11 sets ≥70% threshold for general code. ENG-4.12 sets ≥90% for
Legacy Rescue projects. The skill always applies 70% with no detection or note for
Legacy Rescue contexts. A team on a Legacy Rescue project would silently use the wrong
threshold.

**Fix:** Add a callout in Phase 3c mutation baseline section explaining the project-type
distinction. Add a `## Project Type` entry to the project-rules.md template section.

---

### Files to modify
- `agent-skills/skills-by-domain/development-practices/02-constitutional-companion.md`

### Laws
- ENG-4.11 — ≥70% mutation score (general)
- ENG-4.12 — ≥90% mutation score (Legacy Rescue)

---

## Amendment 22 — Session log analysis findings (CCU-38)

**Source:** Full analysis of `session-log-2026-05-12.md` — complete iOS/Swift adoption
of `americanmobileapp-ios`. Three sessions including crash + recovery.

---

### CCU-38A — Step 0a: Constitution freshness check

**Problem:** First invocation (Turn 2) failed because the constitution repo was stale.
AI said "no skill named constitutional-companion exists." User had to force a `git pull`
manually (Turn 3), losing one full turn.

**Fix:** Add a silent constitution freshness check at the top of Step 0a. Run
`git fetch` + `git status --branch` on the constitution repo. If behind origin,
warn and ask user to pull before continuing. If `git fetch` errors (network), warn
once and proceed. If constitution path not found (new adoption), silently continue.

---

### CCU-38B — Phase 3c: Swift/iOS mutation and coverage tools; stack-not-listed escalation

**Problem:** iOS/Swift project had no mutation or coverage tool listed in the skill's
tool table. The AI skipped Phase 3c mutation baseline entirely. The seam-clean detection
(which checks mutation score ≥70%) was then structurally impossible. No mutation
baseline = no Phase 4 mutation tracking for the entire adoption.

**Fix:**
1. Add iOS/Swift row to the stack tool table:
   - Coverage: `xccov` (via `xcodebuild test -enableCodeCoverage YES`) or slather
   - Mutation: Muter (`muter run --files-to-mutate {seam}`)
2. Replace the vague "if your stack is not listed, ask the avatar" fallback with
   an explicit 4-step escalation: check CI, use if found, otherwise ask user
   A (help set up) / B (defer), never silently skip.

---

### CCU-38C — Phase 4 R4: Hard STOP gate requiring test output before R5

**Problem:** REF-002, REF-003, and REF-004 all moved from R3 directly to R5 with
no R4 appearing in the log. The R4 step existed in the tasks template but nothing
prevented the AI from skipping it (or summarizing it away). No test output was shown.

**Fix:**
1. In tasks.md template: add explicit `⛔ SHOW the test run output before proceeding`.
2. Change `→ After ALL char tests GREEN: offer async mutation delta` to
   `→ After ALL char tests GREEN: offer R4b mutation delta (mandatory offer)`.
3. In Step 6 TDD cycle invariants: add `⛔ Show the raw test run output —
   do not summarize. The human must see it.`

---

### CCU-38D — Step 0b: Explicit re-prompt for ambiguous path selection

**Problem:** User replied "I'd like to buy a vowel" (Turn 4 — a Wheel of Fortune
idiom). AI interpreted this as Path A and immediately created governance artifacts.
Skill says ⛔ "Wait for explicit user selection" (ENG-1.2), but gave no guidance
on what "explicit" means or how to handle non-standard phrasing.

**Fix:** Add re-prompt instruction after the path choices: if the response does not
clearly indicate A or B (idioms, oblique agreement, jokes), re-prompt exactly once:
*"I want to make sure — did you mean A (Guided) or B (Self-Directed)?"*
Only proceed after explicit confirmation of one path.

---

### CCU-38E — Phase 3c: Structurally-blocked coverage (DI coupling)

**Problem:** Turn 9 documented "static singletons require REF-003 DI before full
entry-point coverage." The AI improvised a reasonable handling but the skill had
no guidance. The dead code exemption covers provably unreachable code — it does
not cover code that is currently untestable due to structural coupling and will
become testable after a future refactoring.

**Fix:** Add a second exception category — "Structurally-blocked coverage exception"
— distinct from the dead code exemption. Documents coupling reason, creates a REFACTOR
backlog entry for DI extraction, records actual coverage as `{X}% (blocked: {B} lines
— structurally coupled, unlocked by REF-{id})`, and proceeds with the full 100% gate
deferred until after the DI extraction.

---

### CCU-38F — Phase 4 restart: Cross-check git log vs. backlog state

**Problem:** After the crash, REF-001 was committed (`0944c402e`) but backlog still
showed `PROPOSED`. The AI found and fixed this only because the user explicitly prompted
it. The restart protocol (CCU-36B) covers adoption restarts only. There is no equivalent
protocol for Phase 4 session restarts.

**Fix:** Add a Phase 4 session-resume consistency check at the trigger point for
new-session Phase 4 starts. The check: read backlog for IN PROGRESS rows, run
`git log --oneline -5`, compare — if a commit references `ref-{id}` but backlog shows
the entry as IN PROGRESS or PROPOSED, update to COMPLETE and report the correction.

---

### CCU-38G — Phase 4 R4b: Mandatory offer (not optional/skippable silently)

**Problem:** R4b was described as "optional mutation delta (offered after R4 passes,
before R5)" and the offer dialog had a `skip` option — both of which the AI used as
permission to omit the offer entirely. Zero of the four refactoring cycles in the log
showed the R4b offer.

**Fix:**
1. Rename the section: `R4b — Mutation delta offer (mandatory after R4 passes — offer
   MUST be presented before R5)`.
2. Add `⛔ The R4b offer is mandatory — do not proceed to R5 without presenting it.`
3. Clarify: the user may choose `skip`, but the offer must appear in the output.
4. Update the tasks template to reflect the mandatory nature.

---

### CCU-38H — Step 7: Seam-clean detection guard for missing mutation baseline

**Problem:** After REF-004 the skill instructs seam-clean detection to check mutation
score. With no mutation baseline recorded (C2 cascade), the check was structurally
impossible — there was no score to check. The AI skipped the protocol entirely and
produced a free-form summary.

**Fix:** Add an explicit guard at the top of Step 7: check `phase-3-characterize.md`
for `## Mutation Baseline`. If absent or `NOT RUN`, present a prompt:
- `run mutation` → run scoped tool now and record baseline
- `skip` → treat as DEFERRED, add MUTATION backlog entry, proceed with below-threshold path.
Only evaluate mutation score after a baseline is confirmed (or explicitly skipped).

---

### Files to modify
- `agent-skills/skills-by-domain/development-practices/02-constitutional-companion.md`

### Laws
- ENG-1.2 — AI-Engineer Pairing Law (CCU-38D)
- ENG-4.10 — Characterization Tests (CCU-38E)
- ENG-4.11 — Mutation Score Threshold (CCU-38B, CCU-38G, CCU-38H)

---

## Amendment 23 — AI correction prompts preamble (CCU-39)

**Source:** User observation — common failure modes (lost context, skipped steps,
delegating to user, drifting protocol) need documented correction prompts that are
immediately available without reading the full skill.

---

### CCU-39A — Add "When the AI Loses Track" preamble to skill

**Problem:** When the AI loses context or drifts from the protocol, users have no
quick reference for how to correct it. The skill is 2000+ lines; finding the
relevant rule in the moment is impractical.

**Fix:** Add a `## ⚠️ When the AI Loses Track — Correction Prompts` section directly
after the purpose block (before Step 0a), containing a 14-row table of symptoms →
correction phrases. Each phrase is short enough to paste directly into the chat.
Includes a reference to the full guide for detailed explanations.

---

### CCU-39B — Create `docs/guides/adoption/ai-correction-prompts.md`

**Problem:** 14 correction prompts with full explanations cannot live in the skill
preamble without bloating it. A separate guide is needed with the detailed "why
this happens" explanation, full-length correction prompts, and a quick reference card.

**Fix:** Create `docs/guides/adoption/ai-correction-prompts.md` covering:
- Why context loss happens (context pressure, pattern matching, implicit permission)
- 14 named failure patterns, each with: Symptom description + full correction prompt
- Quick reference card (table of short corrections)

**Failure patterns covered:**
1. AI jumps to code without proposal/task list
2. AI drifts from protocol / gives inconsistent advice
3. AI delegates tasks it could do itself
4. AI summarizes test output instead of showing raw output
5. AI writes production code before a failing test (skipped RED)
6. AI writes multiple tests in one cycle
7. AI moves to next step without confirmation checkpoint
8. AI blocks R5 on mutation score
9. AI reads source files during Step 2 governance setup
10. AI loses context after crash / new session
11. AI skips R4b mutation delta offer
12. AI works on multiple seams / refactorings simultaneously
13. AI cannot find the constitutional-companion skill
14. AI applies ENG-3.1 mechanically (line-count splitting)

---

### Files modified
- `agent-skills/skills-by-domain/development-practices/02-constitutional-companion.md`
- `docs/guides/adoption/ai-correction-prompts.md` *(new)*

### Laws
- ENG-1.2 — AI-Engineer Pairing Law
- ENG-12.1 — Agentic Feedback Loop Law

---

## Amendment 24 — Skill file split: adoption supplement (CCU-40)

**Source:** Size analysis — skill grew to 2,306 lines / ~30K tokens. AI partial-read
risk confirmed in `session-log-2026-05-12.md` (AI read only ~1,100 of 2,100 lines then
started working; Phase 4 R4/R4b/seam-clean all cascade-failed as a result).

**Root cause:** Adoption-time content (governance templates, Phase 3b decision, Phase 3d
SonarQube) is only used once per project, but consumes ~490 lines in a file that is
loaded every session. Phase 4 (the most-used section) sits at lines ~1,495 — past the
point where partial-read failures are observed.

---

### CCU-40A — Mandatory full-read guard at top of main skill

**Fix:** Add `⛔ READ THIS ENTIRE FILE BEFORE TAKING ANY ACTION` at the very first line of
the body (after frontmatter). Partial reads are a known AI failure mode — the explicit
instruction reduces (but does not eliminate) the risk.

---

### CCU-40B — Extract Step 2 (Governance Setup) to supplement

**Fix:** Move Step 2 (lines ~446–684, ~240 lines) — governance setup + AGENTS.md
template + project-rules.md template + tasks.md template + PROPOSAL.md template — to
`02-adoption-setup.md`. Replace with a one-paragraph redirect stub.

---

### CCU-40C — Extract Phase 3b (Decision) to supplement

**Fix:** Move Phase 3b (lines ~984–1146, ~163 lines) — REFACTOR vs REWRITE vs EXTEND
verdict gates, Target Architecture table, Feathers techniques, backlog seeding — to
`02-adoption-setup.md`. Replace with a redirect stub.

---

### CCU-40D — Extract Phase 3d (SonarQube Setup) to supplement

**Fix:** Move Phase 3d (lines ~1409–1493, ~85 lines) — optional SonarQube first-time
dialog, options A–E, credential handling — to `02-adoption-setup.md`. Replace with
redirect stub.

---

### CCU-40E — Create `02-adoption-setup.md`

New file containing Step 2, Phase 3b, Phase 3d with clear header explaining it is
loaded only when a new or in-progress adoption is detected (Priority 3 or 4 in Step 0a).

---

### Net effect

- Main skill: 2,306 → ~1,816 lines
- Supplement: ~490 lines (loaded only once per project)
- Phase 4 moves from ~63% of file depth to ~78% — still late, but the full-read guard
  and reduced total size together meaningfully lower partial-read failure risk

---

### Files modified
- `agent-skills/skills-by-domain/development-practices/02-constitutional-companion.md`
- `agent-skills/skills-by-domain/development-practices/02-adoption-setup.md` *(new)*

### Laws
- ENG-1.2 — AI-Engineer Pairing Law
- ENG-11.1 — Hangar SDD Law

---

## Amendment 25 — CHARACTERIZE-ONLY path + EXTEND verdict removal

**Source:** User feedback — iterative adoption sessions where teams want to lock
behavior seam-by-seam before committing to any refactoring design; the EXTEND
verdict was never used in practice; the user confirmed the preferred pattern
was "record REFACTOR — DEFERRED" so there is a clear trail to return to.

**Three problems identified:**

### CCU-41A — Remove EXTEND verdict from supplement

**Problem:** EXTEND (freeze code, sprout/wrap new behavior) is rarely used and
adds ~12 lines of Feathers technique table that compete with the more common paths.
The Feathers techniques themselves (Sprout Method, Wrap Class, etc.) remain valid
refactoring tools and can be referenced from the WELC guidance section.

**Fix:** Remove EXTEND from Gate 1 verdict list in `02-adoption-setup.md`.
Replace the EXTEND Feathers techniques callout with a CHARACTERIZE-ONLY callout
(see CCU-41B). Update all template strings that include `REFACTOR | REWRITE | EXTEND`.

---

### CCU-41B — Add CHARACTERIZE-ONLY as 4th verdict in Phase 3b

**Problem:** Teams adopting iteratively want to run Phase 3c (characterize) across
multiple seams before committing to any Target Architecture design. Currently this
requires picking REFACTOR then abandoning Gate 2 — awkward and produces incorrect
records.

**Fix:** Add **CHARACTERIZE-ONLY** as a named verdict in Gate 1. When selected:
- Skip Gate 2 (Target Architecture) entirely
- Record verdict in `phase-2-decision.md` as **`REFACTOR — DEFERRED`** (maintains a
  clear trail the team can return to)
- Seed `refactoring-backlog.md` with entries marked `Design deferred — decide after Phase 3c`
- Proceed directly to Phase 3c
- After Phase 3c: offer (a) characterize another seam, (b) return and choose
  REFACTOR/REWRITE now, (c) stop

When a deferred backlog entry is later picked in Phase 4, present Gate 2 at that
point before starting R1.

---

### CCU-41C — Surface CHARACTERIZE-ONLY in main skill

**Problem:** The Companion Mode table (Priority 2) has no entry for "I just want to
characterize without refactoring yet." Phase 4 does not mention deferred entries.

**Fix:**
- Add row to Priority 2 Companion Mode table: "Characterize a seam without refactoring yet"
- Update Phase 3a–3c overview diagram: replace `REFACTOR | REWRITE | EXTEND` with
  `REFACTOR | REWRITE | CHARACTERIZE-ONLY`
- Phase 4 backlog display note: entries with `Design deferred` trigger Gate 2 before R1

---

### Files modified
- `agent-skills/skills-by-domain/development-practices/02-adoption-setup.md`
- `agent-skills/skills-by-domain/development-practices/02-constitutional-companion.md`

### Laws
- ENG-1.2 — AI-Engineer Pairing Law
- ENG-4.1 — Atomic TDD Law
- ENG-11.1 — Hangar SDD Law

---

## Amendment 26 — Type 1 Duplication Removals (cross-reference audit findings F-1.1 through F-1.9)

**Source:** `constitutional-cross-reference-audit.md` — Type 1 findings. Each change
replaces inline prose that already exists in a canonical corpus artifact with a
callout/reference to that artifact. Net effect: ~255 lines removed from the companion
skill and supplement; single point of truth for all referenced content.

**Status legend used below:**
- ✅ **READY** — canonical content confirmed to exist; change is purely a replacement
- ⛔ **BLOCKED** — canonical content does not yet exist; a Type 2 or Type 3 change to another
  constitution file must happen first before this removal can be made

---

### CCU-42A — Reduce correction-prompts table to 3-row quick-reference (F-1.1)

**Status:** ✅ READY

**Current state:** Lines 186–205 of `02-constitutional-companion.md` contain a 13-row
"AI Loses Track" table that duplicates `docs/guides/adoption/ai-correction-prompts.md`.
The skill already cites that guide at line 204, making the table a redundant partial
extraction that must be maintained in two places.

**Proposed change:** Replace the 13-row table with the **3 highest-impact rows** (the
failure modes most often seen in real sessions):

1. *AI starts implementing without a proposal or task list* → prompt
2. *AI ignores constitution guidance / gives degrading advice* → prompt
3. *AI asks you to do something it could do itself* → prompt

Follow with a single callout:
> 📖 Full correction guide (14 failure patterns, detailed prompts, quick-reference card):
> `docs/guides/adoption/ai-correction-prompts.md`

**Lines affected:** companion 186–205 (~18 lines → ~8 lines; saves ~10 lines)
**Risk:** None — the full guide is preserved; only the inline duplication is removed.

---

### CCU-42B — Replace embedded 8-step TDD cycle in AGENTS.md template with law citation (F-1.2)

**Status:** ✅ READY

**Current state:** Lines 117–128 of `02-adoption-setup.md` embed the complete mandatory
8-step TDD cycle verbatim inside the AGENTS.md template that the supplement creates for
the target project. This cycle is the authoritative content of ENG-4.1 and also exists
in `laws/engineering/testing.md` §4.1, `docs/guides/constitution/atomic-tdd-law.md`,
and `docs/guides/testing/atomic-tdd-workflow.md`. Embedding it in a template creates a
third authoritative copy that can drift from the law.

**Proposed change:** Replace the 12-line embedded TDD cycle in the AGENTS.md template
with a single law citation block:

```
# Mandatory Development Protocol (ENG-4.1)
Per [ENG-4.1 — Atomic TDD Law](../laws/engineering/testing.md):
Every code change follows RED → GREEN → REFACTOR → VERIFY → COMMIT.
Full protocol: docs/guides/constitution/atomic-tdd-law.md
```

**Lines affected:** setup 117–128 (~12 lines → ~4 lines; saves ~8 lines)
**Risk:** Low — the full protocol remains in the law and guide; the template stays
constitutionally authoritative by citing the law directly.

---

### CCU-42C — Replace violation-tier table with single-line reference (F-1.6)

**Status:** ✅ READY

**Current state:** Lines 753–760 of `02-constitutional-companion.md` contain an 8-line
HARD_BLOCK / PHASE_GATE / WARNING tier table that is duplicated verbatim in
`docs/guides/adoption/brownfield-adoption.md` §Violation Tiers and in
`skill-sonarqube-compliance-gate.md`. Three copies; any update to tier definitions
must be applied to all three.

**Proposed change:** Replace the 8-line table with:
> Violation tiers (HARD_BLOCK / PHASE_GATE / WARNING) and their remediation rules:
> see `docs/guides/adoption/brownfield-adoption.md` §Violation Tiers.

**Lines affected:** companion 753–760 (~8 lines → ~2 lines; saves ~6 lines)
**Risk:** None — content is fully preserved in the guide.

---

### CCU-42D — Condense "Key Files" section to quick-reference table (F-1.8)

**Status:** ✅ READY

**Current state:** Lines 1767–1812 of `02-constitutional-companion.md` (~45 lines)
explain what AGENTS.md, project-rules.md, `hangar-ai-specs/`, and change-proposal
directories do; how skill routing works; how the authority hierarchy works; and how a
change-proposal lifecycle works. All of this is covered in full depth in:
- `docs/guides/adoption/how-to-adopt-constitution.md` Steps 2–4
- `agent-skills/base/AGENT.md` §2 (authority hierarchy)
- `docs/guides/constitution/constitution-overview.md`
- `agent-skills/skills-by-domain/discovery-research/spec-governance.md`

**Proposed change:** Replace with a 6-row quick-reference table:

| File / Directory | What it does | Deep-dive |
|---|---|---|
| `AGENTS.md` (root) | Constitutional entry point for all AI agents | `docs/guides/adoption/how-to-adopt-constitution.md` Step 2 |
| `hangar-ai-specs/project-rules.md` | Project-specific law overrides and stack config | how-to-adopt Step 2 |
| `hangar-ai-specs/changes/` | SDD change proposals and task lists (ENG-11.1) | `spec-governance.md` |
| `hangar-ai-specs/refactoring-backlog.md` | Living backlog driving Phase 4 | this skill §Phase 4 |
| `agent-skills/` (constitution repo) | Skill routing table | `AGENT.md` §6.3 |
| Authority hierarchy | Laws > Avatars > Skills > Project rules | `AGENT.md` §2 |

**Lines affected:** companion 1767–1812 (~45 lines → ~12 lines; saves ~33 lines)
**Risk:** Low — useful for first-time users; retaining the table preserves discoverability
while eliminating the prose duplication.

---

### CCU-42E — Condense "What's Next" section to 4 lines + starter prompt (F-1.9)

**Status:** ✅ READY

**Current state:** Lines 1816–1862 of `02-constitutional-companion.md` (~45 lines) —
"What's Next After Adoption" 5-row table, 4 bullet points, and a starter prompt template.
`docs/guides/adoption/pragmatic-adoption.md` and `how-to-adopt-constitution.md` Step 4–5
already cover the full post-adoption workflow.

**Proposed change:** Keep only the starter prompt template (the most operationally
useful part) and replace the rest with:

> 🎉 **Adoption complete.** Your project now has a characterized safety net and a
> prioritized refactoring backlog. To continue in a new session, use:
>
> *"Use the constitutional-companion skill to continue the adoption of this repository."*
>
> For what to work on next: `docs/guides/adoption/pragmatic-adoption.md`
> For greenfield features: `docs/guides/adoption/greenfield-mvp.md`

**Lines affected:** companion 1816–1862 (~45 lines → ~8 lines; saves ~37 lines)
**Risk:** Low — the "What's Next" guide is preserved; the starter prompt (most valuable
part) is retained.

---

### CCU-42F — Replace seam-theory definitions with callout to characterization guide (F-1.3)

**Status:** ⛔ BLOCKED

**Current state:** Lines 551–598 of `02-constitutional-companion.md` (~48 lines) define:
- Glossary of seam terms (Seam, Sensing Seam, Separation Seam, Seam Boundary)
- Feathers seam size table (Small / Medium / Large heuristics)
- Mock-necessity test (3-question decision tree)
- Sensing vs Separation seam selection guidance

These belong canonically in `docs/guides/testing/characterization-testing.md`, which
is the dedicated Feathers-pattern guide. The companion's content is either duplicated
or supplementary to that guide.

**Proposed replacement (once unblocked):**
> Seam types, sizing heuristics, Sensing vs Separation guidance, and mock-necessity
> test: see `docs/guides/testing/characterization-testing.md` §Seam Selection.

**Lines affected:** companion 551–598 (~48 lines → ~2 lines; saves ~46 lines)

**🔒 Blocked by:** A Type 2 change to `docs/guides/testing/characterization-testing.md`
is required first:
1. Add the **Feathers seam size table** (Small/Medium/Large) to the guide under a new
   §Seam Sizing section
2. Add the **mock-necessity decision tree** (3 questions) under §No Mocking Rule
3. Add the **Sensing vs Separation** selection guidance under §Seam Selection
4. Confirm that the Sensing/Separation distinction is already present — if so, verify
   the companion's wording matches and no new information is lost before removing

These additions belong in the characterization guide per ENG-4.10 (Test Evolution Law).

---

### CCU-42G — Replace SOLID/DDD tables with references; add GRASP to corpus first for GRASP table (F-1.4)

**Status:** ⛔ BLOCKED (GRASP portion) / ✅ READY (SOLID and DDD portions)

**Current state:** Lines 1509–1551 of `02-constitutional-companion.md` contain three
inline reference tables:
- **GRASP** (9 patterns, lines 1513–1523) — *no canonical home in the corpus*
- **SOLID** (5 principles, lines 1529–1535) — covered in `laws/engineering/quality.md` §3.4
- **DDD** (7 tactical concepts, lines 1543–1551) — covered in `laws/engineering/architecture.md`
  §2.1 and `docs/guides/constitution/ddd-law.md`

**Proposed change (SOLID + DDD — READY):**
Replace the SOLID and DDD tables (22 lines) with:
> SOLID principles: `laws/engineering/quality.md` §3.4 (ENG-3.4) — one principle per law section.
> DDD tactical patterns (Entity, Value Object, Aggregate, Service, Repository, Factory, Domain Event):
> `docs/guides/constitution/ddd-law.md` §Tactical Patterns or `laws/engineering/architecture.md` §2.1.

**Proposed change (GRASP — once unblocked):**
Replace the 9-row GRASP table (12 lines) with:
> GRASP responsibility-assignment patterns: `laws/engineering/architecture.md` §2.1
> (or `docs/guides/constitution/grasp-patterns.md` if a dedicated guide is created).

**Lines affected:** companion 1509–1551 (~45 lines → ~6 lines; saves ~39 lines total once fully done; saves ~27 lines immediately for SOLID+DDD)

**🔒 GRASP portion blocked by:** A Type 3 gap-fill change is required first:
Add the 9-row GRASP table to `laws/engineering/architecture.md` §2.1 under a new
"Responsibility Assignment (GRASP)" subsection — or create a new
`docs/guides/constitution/grasp-patterns.md` guide. The table (9 patterns:
Information Expert, Creator, Controller, Low Coupling, High Cohesion, Polymorphism,
Pure Fabrication, Indirection, Protected Variations) needs to include the "Ask This"
and "Assign Responsibility To" columns currently only in the companion. Once added to
the corpus, the companion can replace its inline table with a one-line citation.

---

### CCU-42H — Reduce Phase 3d SonarQube dialog to routing stub (F-1.5)

**Status:** ⛔ BLOCKED

**Current state:** Lines 449–531 of `02-adoption-setup.md` (~83 lines) contain the
complete SonarQube first-time setup dialog: 5 options (Server / Docker / IDE /
Blocked / Next Session), per-option walkthrough steps, dual-credential collection,
and Option D/E deferred-state logic. The main SonarQube setup flow exists in
`skill-sonarqube-compliance-gate.md` but the adoption-context logic does not.

**Proposed change (once unblocked):** Replace the 83-line dialog with a 6-line
routing stub:
```
Check `project-rules.md` for `sonarqube_status`.
If NOT_SET → load skill-sonarqube-compliance-gate.md §First-Time Setup
If BLOCKED_THIS_ITERATION → record reason; skip; remind at next session start
If DEFERRED → remind at session start; offer to set up now
If CONFIGURED → proceed
```

**Lines affected:** setup 449–531 (~83 lines → ~6 lines; saves ~77 lines)

**🔒 Blocked by:** Two Type 2/3 changes to `skill-sonarqube-compliance-gate.md`:
1. Add the **adoption-context setup dialog** (Options A–E) to the skill's §First-Time
   Setup section — the 5-option flow (Server/Docker/IDE/Blocked/Defer) that is
   currently only in the supplement
2. Add the **dual-credential requirement note** (analysis token ≠ read token; collect
   both upfront) from supplement lines 483–497 — this is the F-3.9 gap finding
3. Add the **BLOCKED_THIS_ITERATION deferral pattern** (Option D) — when SonarQube
   cannot be set up this iteration, record the reason in project-rules.md and set a
   reminder for the next session start

---

### CCU-42I — Move refactoring PROPOSAL.md template to spec-governance; replace inline copy (F-1.7)

**Status:** ⛔ BLOCKED

**Current state:** Lines 1155–1194 of `02-constitutional-companion.md` (~40 lines)
contain a full inline PROPOSAL.md template for per-refactoring proposals, with
adoption-specific fields: Seam name, Backlog ID, characterization test count and
mutation baseline, Problem Statement, Proposed Design (pattern + rationale), Alternatives
considered table (2 rows), Scope and Safety Net. This template has no home in
`spec-governance.md`, which currently only defines the SDD change-proposal format.

**Proposed change (once unblocked):** Replace with:
> Refactoring proposal template: see `spec-governance.md` §Refactoring Proposal Variant.
> Required fields: Seam, Backlog-ID, Characterization Baseline, Problem, Proposed
> Design (pattern + rationale), Alternatives, Scope, Safety Net.

**Lines affected:** companion 1155–1194 (~40 lines → ~4 lines; saves ~36 lines)

**🔒 Blocked by:** A Type 2 change to
`agent-skills/skills-by-domain/discovery-research/spec-governance.md`:
1. Add a **"Refactoring Proposal Variant"** section containing the full template above —
   this is an extension of the standard PROPOSAL.md schema per ENG-11.2 (Proposal
   Completeness Law), adding the adoption-specific fields (Seam, Backlog ID,
   Characterization Baseline) that ENG-11.2 does not currently enumerate
2. Annotate each field with the law that mandates it (e.g., Backlog ID → ENG-6.7;
   Alternatives → ENG-11.2; Safety Net → ENG-4.1)
3. Once added to spec-governance, the companion's inline template becomes a
   cross-reference — any change to the template format is made once

---

### Summary — Amendment 26 task readiness

| Task | Finding | Status | Lines saveable |
|---|---|---|---|
| CCU-42A | F-1.1 Correction-prompts table | ✅ READY | ~10 |
| CCU-42B | F-1.2 Embedded TDD cycle in AGENTS.md template | ✅ READY | ~8 |
| CCU-42C | F-1.6 Violation-tier table | ✅ READY | ~6 |
| CCU-42D | F-1.8 "Key Files" section | ✅ READY | ~33 |
| CCU-42E | F-1.9 "What's Next" section | ✅ READY | ~37 |
| CCU-42F | F-1.3 Seam-theory definitions | ⛔ BLOCKED (characterization-testing.md update needed) | ~46 |
| CCU-42G | F-1.4 SOLID/DDD tables (READY) + GRASP table (BLOCKED) | ⛔ PARTIALLY BLOCKED (F-3.8 gap-fill needed for GRASP) | ~27 now, ~39 total |
| CCU-42H | F-1.5 SonarQube setup dialog | ⛔ BLOCKED (sonarqube skill update needed) | ~77 |
| CCU-42I | F-1.7 Refactoring PROPOSAL.md template | ⛔ BLOCKED (spec-governance update needed) | ~36 |

**Immediately actionable (CCU-42A–E + SOLID/DDD half of 42G): ~121 lines**
**Full potential when all unblocked: ~280 lines**

### Files modified
- `agent-skills/skills-by-domain/development-practices/02-constitutional-companion.md`
- `agent-skills/skills-by-domain/development-practices/02-adoption-setup.md`

### Laws
- ENG-4.1 — Atomic TDD Law (CCU-42B)
- ENG-11.1 — Hangar SDD Law
- ENG-11.2 — Proposal Completeness Law (CCU-42I)

---

## Amendment 27 — Type 4: Add missing law citations with markdown hyperlinks (CCU-43)

**Source:** `constitutional-cross-reference-audit.md` — Type 4 findings.
The companion skill has 52 constraint lines (`⛔`, `MUST`, `SHALL`, mandatory, forbidden)
but only 3 currently cite a law ID. Rules asserted without constitutional authority are:
- harder for AI agents to apply in spirit rather than just letter
- harder to amend correctly when a law changes (no traceability)
- harder for developers to verify ("is this actually required?")

**All citations use markdown hyperlinks** to the exact section in the law file. Relative
paths from `agent-skills/skills-by-domain/development-practices/` to the laws directory.

**Law file path reference:**
```
../../../laws/engineering/foundations.md       ← ENG-1.x
../../../laws/engineering/architecture.md      ← ENG-2.x
../../../laws/engineering/quality.md           ← ENG-3.x
../../../laws/engineering/testing.md           ← ENG-4.x
../../../laws/engineering/security.md          ← ENG-6.7 (Audit Trail)
../../../laws/engineering/governance.md        ← ENG-10.x
../../../laws/engineering/agentic-feedback.md  ← ENG-12.x
```

---

### CCU-43A — Checkpoint dialog gate: add ENG-1.2 citation

**Location:** `02-constitutional-companion.md` ~line 473
**Rule:** "At every ⛔ STOP or 'await human confirmation' point, the agent MUST present
this exact format."
**Add:** `(ENG-1.2)` hyperlink at end of the rule statement.
**Link:** `[ENG-1.2](../../../laws/engineering/foundations.md#section-12-ai-engineer-pairing-law)`

---

### CCU-43B — MUST NOT start refactoring until human explicitly chooses: add ENG-1.2 citation

**Location:** `02-constitutional-companion.md` ~line 519
**Rule:** "The agent MUST NOT start any refactoring until the human explicitly chooses to."
**Add:** `(ENG-1.2)` hyperlink at end of the sentence.
**Link:** `[ENG-1.2](../../../laws/engineering/foundations.md#section-12-ai-engineer-pairing-law)`

---

### CCU-43C — Seam-wide sociable testing invariant: add ENG-4.8 citation

**Location:** `02-constitutional-companion.md` ~line 787
**Rule:** "`⛔ Seam-wide sociable testing invariant` — no collaborator within the seam
boundary is mocked; mocking only at I/O boundaries."
**Add:** `(ENG-4.8)` hyperlink to the title of the invariant callout.
**Link:** `[ENG-4.8](../../../laws/engineering/testing.md#section-48-mock-boundaries-law)`

---

### CCU-43D — Coverage gates apply to seam files only: add ENG-4.6 citation

**Location:** `02-constitutional-companion.md` ~line 830
**Rule:** "⛔ Coverage gates apply to the files in this seam — not to the entire codebase.
The project's overall coverage number is irrelevant here and MUST NOT be used to block."
**Add:** `(ENG-4.6)` hyperlink appended to the callout header.
**Link:** `[ENG-4.6](../../../laws/engineering/testing.md#section-46-coverage-requirements)`

---

### CCU-43E — Do NOT change any logic in Phase 3c: add ENG-4.1 citation

**Location:** `02-constitutional-companion.md` ~line 959
**Rule:** "⛔ Do NOT change any logic in this phase — characterization tests only."
**Add:** `(ENG-4.1)` hyperlink appended.
**Link:** `[ENG-4.1](../../../laws/engineering/testing.md#section-41-atomic-test-driven-development-law)`

---

### CCU-43F — Phase 4 characterization-test RED invariant: add ENG-4.1 citation

**Location:** `02-constitutional-companion.md` ~line 1191
**Rule:** "⛔ Invariant: If any characterization test goes RED during this refactoring,
fix the refactored code. Do NOT change the test."
**Add:** `(ENG-4.1)` hyperlink on the invariant label.
**Link:** `[ENG-4.1](../../../laws/engineering/testing.md#section-41-atomic-test-driven-development-law)`

---

### CCU-43G — SHOW test output before proceeding: add ENG-4.1 citation

**Location:** `02-constitutional-companion.md` ~line 1206
**Rule:** "⛔ SHOW the test run output before proceeding — do not summarize or paraphrase."
**Add:** `(ENG-4.1)` hyperlink appended.
**Link:** `[ENG-4.1](../../../laws/engineering/testing.md#section-41-atomic-test-driven-development-law)`

---

### CCU-43H — R4b mutation delta offer is mandatory: add ENG-4.11 citation

**Location:** `02-constitutional-companion.md` ~line 1232
**Rule:** "⛔ The R4b offer is mandatory — do not proceed to R5 without presenting it."
**Add:** `(ENG-4.11)` hyperlink appended.
**Link:** `[ENG-4.11](../../../laws/engineering/testing.md#section-411-mutation-testing-law)`

---

### CCU-43I — Mutation baseline guard: add ENG-4.11 citation

**Location:** `02-constitutional-companion.md` ~line 1367
**Rule:** "⛔ Mutation baseline guard: Before evaluating mutation score, confirm that a
baseline exists in `phase-3-characterize.md`."
**Add:** `(ENG-4.11)` hyperlink appended to the callout header.
**Link:** `[ENG-4.11](../../../laws/engineering/testing.md#section-411-mutation-testing-law)`

---

### CCU-43J — Prohibited mechanical line-count splitting: add ENG-3.1 citation

**Location:** `02-constitutional-companion.md` ~line 1501 (Step 5 intro / design prohibition)
**Rule:** "⛔ Prohibited: Mechanically splitting a method at line 50 without changing its
logical structure."
**Add:** `(ENG-3.1)` hyperlink on the "Prohibited" label.
**Link:** `[ENG-3.1](../../../laws/engineering/quality.md#section-31-complexity-limits)`

---

### CCU-43K — Agent MUST NOT scan files outside bounded context: add ENG-2.3/ENG-2.4 citations

**Location:** `02-constitutional-companion.md` ~line 1693 (Trust Ramp / MVS section)
**Rule:** "The AI MUST NOT scan or remediate files outside the declared bounded context."
**Add:** `(ENG-2.3, ENG-2.4)` hyperlinks appended.
**Links:**
- `[ENG-2.3](../../../laws/engineering/architecture.md#section-23-vertical-slice-architecture-law)`
- `[ENG-2.4](../../../laws/engineering/architecture.md#section-24-bounded-context-law)`

---

### CCU-43L — Each iteration MUST NOT add new violations: add ENG-12.1 citation

**Location:** `02-constitutional-companion.md` ~line 1706
**Rule:** "Each iteration MUST NOT add new violations."
**Add:** `(ENG-12.1)` hyperlink appended.
**Link:** `[ENG-12.1](../../../laws/engineering/agentic-feedback.md#eng-121-agentic-feedback-loop-law)`

---

### CCU-43M — All refactorings MUST be logged in refactoring-backlog.md: add ENG-6.7 citation

**Location:** `02-constitutional-companion.md` ~lines 997–999 (Phase 4 backlog intro)
**Rule:** "ADOPTION IS NOW COMPLETE. All subsequent work is driven by `refactoring-backlog.md`."
The requirement that all refactorings are logged satisfies ENG-6.7 (Audit Trail), but is
not currently cited.
**Add:** `(ENG-6.7)` hyperlink to the backlog-driven-work statement.
**Link:** `[ENG-6.7](../../../laws/engineering/security.md#eng-67--audit-trail-law)`

---

### CCU-43N — Commit message MUST reference spec scenario ID: add ENG-6.7 citation

**Location:** `02-adoption-setup.md` — commit instruction in Phase 3b backlog seeding
and Phase 3c completion commits (multiple locations).
**Rule:** Each `git commit -m` instruction should note that the message format satisfies
ENG-6.7 (Audit Trail Law) traceability requirement.
**Add:** Inline `(ENG-6.7)` hyperlink after commit-message format instructions.
**Link:** `[ENG-6.7](../../../laws/engineering/security.md#eng-67--audit-trail-law)`

---

### Summary — Amendment 27 tasks

| Task | Location | Law to cite | Hyperlink anchor |
|---|---|---|---|
| CCU-43A | companion ~473 | ENG-1.2 | foundations.md#section-12... |
| CCU-43B | companion ~519 | ENG-1.2 | foundations.md#section-12... |
| CCU-43C | companion ~787 | ENG-4.8 | testing.md#section-48... |
| CCU-43D | companion ~830 | ENG-4.6 | testing.md#section-46... |
| CCU-43E | companion ~959 | ENG-4.1 | testing.md#section-41... |
| CCU-43F | companion ~1191 | ENG-4.1 | testing.md#section-41... |
| CCU-43G | companion ~1206 | ENG-4.1 | testing.md#section-41... |
| CCU-43H | companion ~1232 | ENG-4.11 | testing.md#section-411... |
| CCU-43I | companion ~1367 | ENG-4.11 | testing.md#section-411... |
| CCU-43J | companion ~1501 | ENG-3.1 | quality.md#section-31... |
| CCU-43K | companion ~1693 | ENG-2.3, ENG-2.4 | architecture.md#section-23..., #section-24... |
| CCU-43L | companion ~1706 | ENG-12.1 | agentic-feedback.md#eng-121... |
| CCU-43M | companion ~997–999 | ENG-6.7 | security.md#eng-67... |
| CCU-43N | setup (multiple commit instructions) | ENG-6.7 | security.md#eng-67... |

**Note on anchor format:** GitHub auto-generates heading anchors by lowercasing, replacing
spaces with hyphens, and stripping punctuation. All anchors above follow this convention
from the confirmed section headings. Verify each anchor resolves before merging.

### Files modified
- `agent-skills/skills-by-domain/development-practices/02-constitutional-companion.md`
- `agent-skills/skills-by-domain/development-practices/02-adoption-setup.md`

### Laws
- All laws being cited — no new law requirements; this is citation-only work
