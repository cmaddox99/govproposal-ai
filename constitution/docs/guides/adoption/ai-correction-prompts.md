# AI Correction Prompts — Constitutional Companion

> **Use this guide when the AI loses context, skips steps, or behaves in ways that
> feel wrong.** The prompts below are designed to be pasted directly into the chat
> to get the AI back on track. You should not need to understand *why* the AI went
> off script — just match the symptom and paste the correction.

---

## Why This Happens

AI assistants are stateless across turns and can lose track of long procedural skills.
The most common causes:

- **Context window pressure** — the skill file is long; after many turns the AI may be
  working from a compressed memory of the steps rather than the actual text.
- **Pattern matching over protocol** — the AI recognizes a familiar-looking situation
  and defaults to a general coding pattern instead of the constitutional procedure.
- **Implicit permission** — if you don't push back on a skipped step, the AI treats
  your silence as approval and keeps going.

The correction prompts below are specific and firm. Use them without apology — the AI
is not offended by correction and will respond well to explicit instruction.

---

## Correction Prompts

---

### 1 — AI jumps straight to writing code without a proposal or task list

**Symptom:** The AI starts creating source files, writing tests, or editing existing code
without first creating `PROPOSAL.md` and `tasks.md` in
`hangar-ai-specs/changes/ref-{id}-{slug}/`. Or it announces what it is going to do and
immediately starts doing it.

**Paste this:**
> Stop. Before writing any code, you must create a `PROPOSAL.md` and `tasks.md` for this
> refactoring in a new `hangar-ai-specs/changes/ref-{id}-{slug}/` folder. The proposal
> describes the problem, the pattern being applied, and the design rationale. The task list
> has exactly five steps: R1 RED → R2 GREEN → R3 REFACTOR → R4 VERIFY → R5 COMMIT.
> Please create those two files now and wait for my confirmation before starting R1.

---

### 2 — AI drifts from the protocol, gives inconsistent advice, or seems to forget how it works

**Symptom:** Steps come in the wrong order, checkpoints are missing, the AI gives advice
that contradicts what it said earlier, or it seems to be making up a procedure rather
than following a documented one.

**Paste this:**
> Please stop and re-read the active skill file for this session, including all ⛔ rules
> and checkpoint dialogs. Then resume from where we left off, following its steps exactly.
> If you are not sure where we are, re-read `workflows/adoption.md` and identify which
> phase applies to this project before continuing.

---

### 3 — AI asks you to do things it could do itself

**Symptom:** The AI says things like "you should now run X," "please create file Y,"
"you'll need to install Z," or "go ahead and commit this" — tasks that are entirely
within its ability to perform in this environment.

**Paste this:**
> Please do not ask me to perform tasks you are capable of doing yourself. Run the
> command, create the file, or make the edit directly. Only ask me to act if you have
> genuinely tried at least three different approaches and cannot proceed, or if the
> action requires credentials, physical access, or a decision only I can make.

---

### 4 — AI summarizes test results instead of showing the actual output

**Symptom:** Instead of showing the test runner output (pass/fail counts, stack traces,
timing), the AI says things like "the tests passed" or "I ran the suite and everything
is green" without displaying the actual terminal output.

**Paste this:**
> Please show me the raw test runner output — do not summarize, paraphrase, or replace
> it with a sentence. I need to see the actual counts, any failure messages, and the
> exit status. This is required by the R4 VERIFY step before we can proceed to R5.

---

### 5 — AI writes production code before showing a failing test (skipped RED step)

**Symptom:** The AI writes a new class, method, or logic change without first writing a
test and showing it fail. Or it writes the test and the implementation in the same
response without showing the test fail in between.

**Paste this:**
> You have skipped the RED step. Per ENG-4.1 (Atomic TDD Law), you must write exactly
> ONE test first, run it, and show me that it FAILS before writing any production code.
> Please delete or ignore what you just wrote, go back to R1, write one failing test,
> show the failure output, and wait for my confirmation before writing the implementation.

---

### 6 — AI writes multiple tests in one cycle

**Symptom:** The AI writes a test class, a test file, or several test methods at once
instead of exactly one test per TDD cycle.

**Paste this:**
> Per ENG-4.1, each TDD cycle contains exactly ONE test — not a test class, not a test
> file, ONE test method. Please reduce this to a single test, run it to confirm it fails,
> and wait for my confirmation before proceeding to R2.

---

### 7 — AI moves to the next step or next refactoring without asking for confirmation

**Symptom:** The AI completes a step and immediately starts the next one without
presenting a checkpoint and waiting for you to type `continue`, `confirmed`, or similar.

**Paste this:**
> Please stop. Per ENG-1.2, you must wait for my explicit confirmation at every checkpoint
> before moving to the next step. Present the checkpoint summary and wait for my response.
> Do not proceed until I have confirmed.

---

### 8 — AI treats mutation score as a hard gate on R5 (blocks commit until score is ≥70%)

**Symptom:** The AI refuses to proceed to R5 (commit) because the mutation score is
below 70%, or it starts writing additional tests to improve the score before committing.

**Paste this:**
> R5 is NOT gated on mutation score. The mutation score is informational and improves
> over time through dedicated MUTATION backlog entries. Please proceed to R5 now — commit
> the refactoring. If the mutation score is below 70%, add a MUTATION entry to the
> refactoring backlog and we will address it separately.

---

### 9 — AI analyzes source code or suggests a product avatar during governance setup (Step 2)

**Symptom:** During Step 2 (creating AGENTS.md, hangar-ai-specs/, project-rules.md),
the AI starts reading `.java`, `.ts`, `.py` or other source files, lists package names,
suggests a product domain, or tries to select a product avatar.

**Paste this:**
> Stop. Step 2 is governance setup only — no source file reading, no product avatar
> selection, no code analysis. Those activities belong in Phase 3a (Archaeology), which
> comes after governance setup is complete and committed. Please continue Step 2 using
> only the prescribed templates. Do not read any source files.

---

### 10 — After a crash or new session, AI does not know where you left off

**Symptom:** The AI starts fresh, re-introduces itself, or asks what you want to do —
without picking up the in-progress adoption or refactoring from the previous session.

**Paste this:**
> Please run Step 0a — the adoption status check. Check `hangar-ai-specs/changes/` for
> an open adoption proposal or open refactoring folder. Check `refactoring-backlog.md`
> for any IN PROGRESS or PROPOSED entries. Check `git log --oneline -5` to see what was
> last committed. Then resume from where we left off and tell me what the next step is.

---

### 11 — AI skips the R4b mutation delta offer and goes straight from R3 to R5

**Symptom:** After R3 REFACTOR, the AI runs the tests and immediately moves to the R5
commit without presenting the "want to run a quick mutation delta?" offer.

**Paste this:**
> You skipped R4b. After R4 VERIFY passes (all characterization tests GREEN), you must
> present the mutation delta offer before proceeding to R5. The offer is: "Want to run a
> quick mutation delta? Type `run mutation` or `skip`." Please present it now.

---

### 12 — AI starts working on multiple seams or refactorings at the same time

**Symptom:** The AI proposes changes to multiple classes across different seams in a single
response, or begins planning refactorings for several backlog entries simultaneously.

**Paste this:**
> Please focus on one seam and one backlog entry at a time. Complete the full R1 → R5
> cycle for the current entry before discussing or touching anything else. If you have
> suggestions for other seams, add them to the refactoring backlog — do not act on them now.

---

### 13 — AI seems to be applying ENG-3.1 line limits by mechanically splitting methods

**Symptom:** The AI is splitting long methods into small private helpers without a design
rationale, producing many tiny methods with no conceptual identity, or prioritizing line
counts over good object design.

**Paste this:**
> ENG-3.1 line limits are a design signal, not a counting rule. Do not split methods
> mechanically to meet line counts. Instead, apply GRASP Information Expert and SRP:
> ask "who owns this responsibility?" and extract only when a coherent, reusable concept
> emerges. When a correct design produces a method longer than 50 lines, prefer the correct
> design and document the exception in `project-rules.md` with the GRASP/SOLID reasoning.

---

## Quick Reference Card

Paste these shorter versions when you don't have time to use the full prompts above:

| Symptom | Short correction |
|---------|-----------------|
| Writing code without a proposal | *"Stop — create PROPOSAL.md and tasks.md first."* |
| Forgetting the protocol | *"Re-read the active skill file and resume."* |
| Asking you to do its work | *"Please do that yourself — don't delegate to me."* |
| Summarizing test output | *"Show raw test output, not a summary."* |
| No failing test before code | *"RED step first — write one failing test and show the failure."* |
| Multiple tests at once | *"One test per cycle — reduce to a single test method."* |
| No confirmation checkpoint | *"Stop and wait for my confirmation per ENG-1.2."* |
| Blocking R5 on mutation score | *"Mutation score does not gate R5 — proceed to commit."* |
| Reading source during Step 2 | *"Step 2 is governance-only — no source file reads."* |
| Lost context after crash | *"Run Step 0a and tell me where we left off."* |
| Skipped R4b | *"Present the R4b mutation delta offer before R5."* |
| Multiple seams at once | *"One seam, one backlog entry, one cycle at a time."* |
| Skill not found | *"git pull the constitution, re-read the skill file, re-run Step 0a."* |
| Line-count splitting | *"Apply GRASP/SRP — design first, line count follows."* |

---

*Add new patterns here as they are observed in adoption sessions.*
