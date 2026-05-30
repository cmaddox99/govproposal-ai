# Proposal: Iterative Adoption for Large Codebases

**ID:** `iterative-adoption-large-codebases`
**Status:** IMPLEMENTED — READY FOR REVIEW
**Branch:** `proposal/iterative-adoption-large-codebases`
**SDD Phase:** IMPLEMENT → ARCHIVE
**Authority:** ENG-11.1

---

## Amendment 17 — P2 Usability Improvements (Panel Review Findings)

**Date:** 2026-05-08
**Source:** 7-member expert review panel — P2 recommendations (usability improvements for a meaningful subset of users)

### Problem

The review panel identified five usability gaps that cause friction for specific user populations — junior developers, Java engineers doing mutation testing, teams encountering cross-context seams, and anyone trying to navigate the skill's structure. None of these are constitutional violations, but each will cause real confusion in practice.

### Findings and Alternatives

**P2-1 — Step numbering inconsistency**
The skill summary at line 251–259 lists items "1. Archaeology … 7. STOP" but wraps them under "Step 3." Line 261 then says "Steps 3 and 5 are separated by mandatory human checkpoints" — but Step 5 in the outer procedure is "Design Principles," not "Implement." This creates two plausible but wrong interpretations for an AI agent or junior developer.
- *Alternative:* Remove the inner numbered list entirely and reference phases by letter (3a–3f). *Chosen.* Renames the summary header to "Phase 3a–3f Overview" and replaces "Steps 3 and 5" with "Phase 3c and Phase 3e."

**P2-2 — Sensing vs. Separation seam types missing**
Feathers distinguishes *Sensing Seams* (observe behavior without changing it) from *Separation Seams* (replace a dependency to enable testing). Both Reviewer 3 (Legacy Codebase Specialist) and Reviewer 4 (Platform/DevOps) flagged this. Without the distinction, an AI agent may choose a seam that requires test infrastructure wiring (Separation) when the correct approach is a Sensing Seam at a higher entry point.
- *Alternative:* Add a full Sensing/Separation table with examples. *Chosen a lighter touch:* one-sentence note in "What Is a Seam?" that names both types and recommends Sensing Seams for characterization.

**P2-3 — Sprout Class / Wrap Method missing for EXTEND verdicts**
The EXTEND verdict in Phase 3b has no Feathers technique guidance. An AI agent given an EXTEND verdict on high-risk legacy code has no instruction for how to add behavior safely. Sprout Class (new class alongside existing) and Wrap Method (wrap the existing call) are the canonical Feathers techniques for this situation. Reviewer 3 flagged this.
- *Alternative:* Expand EXTEND guidance to a full sub-section. *Chosen lighter touch:* one callout note in Phase 3b listing the two techniques with one-sentence descriptions.

**P2-4 — Pitest `targetClasses` not documented**
The skill documents JaCoCo `includes` for seam-scoped coverage but omits the equivalent Pitest filter. Without `targetClasses`, an AI agent will run mutation testing project-wide rather than seam-scoped, violating the coverage scoping requirement the skill itself establishes. Reviewer 1 (Senior Java Engineer) flagged this.
- *No meaningful alternative:* simply add the configuration.

**P2-5 — "Non-trivial" never defined**
The skill's design-rationale.md Section 2 requires "at least one alternative solution" for "every non-trivial problem," but "non-trivial" is never defined. An AI agent will interpret this inconsistently — sometimes requiring alternatives for trivial renames, sometimes skipping them for significant design choices. Reviewer 2 (Junior Developer) and Reviewer 3 flagged this.
- *Alternative:* Replace "non-trivial" with an exhaustive list of qualifying change types. *Chosen simpler:* a parenthetical definition — "non-trivial = any change affecting more than 3 lines or introducing/removing a collaborator."

### Changes

| Artifact | Change |
|----------|--------|
| `02-pragmatic-adoption.md` | Phase 3a–3f summary header renamed; "Steps 3 and 5" → "Phase 3c and Phase 3e" |
| `02-pragmatic-adoption.md` | Sensing vs. Separation note added to "What Is a Seam?" |
| `02-pragmatic-adoption.md` | Sprout Class / Wrap Method callout added to Phase 3b |
| `02-pragmatic-adoption.md` | Pitest `targetClasses` added to Java coverage row |
| `02-pragmatic-adoption.md` | "non-trivial" defined inline in design-rationale.md Section 2 |
| `02-pragmatic-adoption.md` version | `2.14.0` → `2.15.0` |

---

## Amendment 16 — P1 Agent Failure Gaps (Panel Review Findings)

**Date:** 2026-05-08
**Source:** 7-member expert review panel — P1 recommendations (significant gaps that cause agent failures in realistic scenarios)

### Problem

The review panel identified five gaps where an AI agent following the skill will fail silently or loop indefinitely in scenarios that arise frequently in real legacy codebases. These are not constitutional violations but they represent real paths through the skill that have no defined outcome.

### Findings and Alternatives

**P1-1 — ENG-4.10 omission: characterization tests never retired**
ENG-4.10 (Test Evolution Law) states: "Each characterization test SHALL be retired and replaced by targeted unit tests as the code it covers is refactored." The skill creates characterization tests in Phase 3c but provides no instruction to evolve or retire them during Phase 3e (Implement). An AI agent following the skill will leave characterization tests in perpetuity, locking obsolete behavior after the code has been refactored and defeating the purpose of the tests. Reviewer 6 (Constitution Governance) and Reviewer 7 flagged this.
- *Alternative:* Create a Phase 3g "Characterization Test Retirement" as a separate phase. *Rejected:* too heavyweight; retirement is an ongoing activity tied to each TDD cycle in Phase 3e. *Chosen:* add a callout within Phase 3e instructing the agent to tag characterization tests for evolution after each TDD cycle resolves the behavior they cover.

**P1-2 — Jargon undefined: seam, characterization test, bounded context, mutation score**
The skill uses four technical terms before or without defining them. "Bounded context" appears in Step 1; "seam" appears before the seam definition section; "characterization test" is never formally defined; "mutation score" is used in the coverage checklist without explanation. All four terms will cause AI agents to hallucinate definitions and will lose junior developers. Reviewers 1, 2, 3, and 7 flagged this.
- *Alternative:* Define each term inline on first use only. *Chosen over inline:* a dedicated `## Key Definitions` callout at the top of Section 3, before any term is used, so the agent and reader have a single reference point. Keeps the procedural flow clean.

**P1-3 — 100% line coverage blocks on dead/unreachable code**
Legacy codebases routinely contain dead branches (code paths that can never execute due to removed features), defensive throws (guards that cannot be triggered), and impossible conditions (null-check guards on values guaranteed non-null by the call chain). The skill requires 100% line coverage before Implement but provides no escape hatch. An AI agent will attempt to write tests for unreachable code, loop indefinitely when they can't pass, or worse — modify production code to make the branch reachable (a Phase 3c violation). Reviewers 1, 3, and 7 flagged this.
- *Alternative:* Lower the gate to 90%. *Rejected:* the 100% requirement is intentional — characterization must lock all observable behavior. *Chosen:* add an explicit documented-exception path: if a line is provably unreachable, document it in phase-3-characterize.md with the reason, and mark it exempt. Do not modify the code.

**P1-4 — Seam crosses bounded-context boundary**
The skill states "each iteration targets exactly one bounded context" and the seam discovery protocol identifies seams within a declared context. However, in real codebases, a seam's files may cross context boundaries mid-archaeology (e.g., a pricing seam discovered to include a file from the loyalty context). The skill provides no guidance. An AI agent will either silently truncate the seam (missing behavior) or silently expand scope beyond the declared context (violating the chunking protocol). Reviewer 5 (Technical Lead) and Reviewer 7 flagged this.
- *Alternative:* Allow cross-context seams with a flag. *Rejected:* this undermines the bounded-context isolation that makes iterative adoption tractable. *Chosen:* explicit STOP with a three-option human dialog: (a) expand iteration scope to include the boundary file, (b) truncate seam at context boundary and note the limitation, (c) defer this seam and choose a different one.

**P1-5 — ENG-4.1 missing from frontmatter `implements`**
ENG-4.1 (Atomic TDD Law) is cited extensively in the skill body — in Phase 3e, Step 5, and Step 6 — but is absent from the `laws.implements` frontmatter block. This matters for RAG routing: the skill index uses frontmatter to determine which laws a skill operationalizes. Without ENG-4.1 in `implements`, the skill will not be surfaced by queries about Atomic TDD. Reviewer 5 and Reviewer 6 flagged this; Reviewer 7 confirmed.
- *No meaningful alternative:* simply add the law to the frontmatter.

### Changes

| Artifact | Change |
|----------|--------|
| `02-pragmatic-adoption.md` | ENG-4.1 added to `laws.implements` frontmatter |
| `02-pragmatic-adoption.md` | `## Key Definitions` callout added before Phase 3a |
| `02-pragmatic-adoption.md` | Unreachable-code escape hatch added to Phase 3c 100% gate |
| `02-pragmatic-adoption.md` | Cross-bounded-context STOP + 3-option dialog added to Phase 3a |
| `02-pragmatic-adoption.md` | ENG-4.10 characterization test retirement callout added to Phase 3e |
| `02-pragmatic-adoption.md` version | `2.13.0` → `2.14.0` |

---

## Amendment 15 — P0 Constitutional Violations: Refined Approach (Panel Review + User Validation)

**Date:** 2026-05-08
**Source:** 7-member expert review panel P0 findings, refined through author validation of real-world constraints

### Background

The review panel correctly identified two constitutional tensions. However, the initially proposed fixes (make SonarQube mandatory, enforce 70% mutation gate) were validated against real-world adoption scenarios and found to create a worse problem than they solve: both can block engineers for days or weeks on factors entirely outside their control (corporate credential provisioning, Docker security policies, mutation run times on large legacy codebases). This amendment addresses both findings with solutions that satisfy the skill's primary mission — **get engineers to working code with AI as fast as possible** — while progressing toward constitutional compliance over time.

---

### Finding 1 — ENG-12.1: SonarQube Access Is an Organizational Dependency, Not an Engineer Choice

**The real constraint:** The review panel assumed SonarQube is available. In enterprise environments it often is not:
- **Server access** requires credentials and an analysis key that may take days or weeks to provision through IT/security processes
- **Local Docker** requires Docker Desktop, which corporate security may prohibit entirely
- **Neither can be unblocked by the engineer alone** — they require organizational action

Making SonarQube mandatory would convert this skill into a hard blocker on external organizational processes. An engineer who wants to adopt the constitution cannot do so until their IT ticket resolves. This directly contradicts the skill's reason for existing.

**Alternatives Considered:**

**A. Make SonarQube mandatory with deferral acknowledgement (original P0 fix).** *Rejected.* Creates exactly the multi-day/multi-week block described above. The engineer's only path is to wait for IT.

**B. Remove SonarQube from the skill entirely.** *Rejected.* SonarQube integration is genuinely valuable and many engineers *can* connect quickly. Removing it loses real value.

**C. SonarLint-only fallback.** *Partially accepted as Option C in the dialog.* SonarLint (now "SonarQube for IDE") runs the same rules locally with no server, credentials, or Docker required. It installs in ~2 minutes from any IDE marketplace. This satisfies the *intent* of ENG-12.1 (static analysis gate provisioned) without the access dependency.

**D. Positive-framing informed choice dialog (chosen primary approach).** Replace the "optional" language with an upbeat, informative dialog that presents all paths — including the 2-minute local option — and lets the engineer choose. The dialog is non-blocking: every option (including "skip") produces a documented outcome in `project-rules.md`. The skill then delegates ENG-12.1 gate provisioning to `skill-sonarqube-compliance-gate` (already in the `followed_by` list), which is the architecturally correct owner of that requirement.

**E. Governance exception via `project-rules.md`.** *Available as backstop.* If all options are unavailable (no server access, Docker blocked, IDE plugin not permitted), the engineer records `sonarqube_status: BLOCKED` with a ticket reference. The skill checks in once per iteration — not every phase — and offers to resume setup when access resolves.

**Chosen Solution — Phase 3d Informed Choice Dialog:**

Phase 3d heading changes from "Optional — Recommended" to "SonarQube Setup" (neutral). The agent presents this dialog:

> *"Setting up SonarQube now makes your adoption significantly better — you'll get a real before/after quality comparison as you refactor. Here are your options:*
>
> **A — SonarQube server** *(fastest if you have access):* If you have server credentials and can generate an analysis key, configuration takes ~5 minutes. I can walk you through it.
>
> **B — Local Docker instance** *(~15–45 min):* Full SonarQube Community Edition in Docker. Corporate Docker policies may apply. I can walk you through it.
>
> **C — SonarQube for IDE** *(~2 min, no server or Docker needed):* Installs directly in your IDE (IntelliJ, VS Code, Eclipse). Runs the same rule set locally with no credentials required. I can walk you through it.
>
> **D — Skip for now, mark as blocked:** I'll record `sonarqube_status: BLOCKED` in `project-rules.md`. I'll check in once per iteration (not every phase) to see if access has resolved.
>
> **E — Skip for now, remind me next session:** No setup today. I'll open with this question at your next session.*
>
> *What would you like to do?"*

The iteration summary line changes from `SonarQube → optional baseline now, or defer` to `SonarQube → setup dialog (server / Docker / IDE plugin / defer)`.

The existing reminder pattern (once per iteration until `sonarqube_status: done`) is preserved. Options D and E both produce a `project-rules.md` entry that the agent reads at re-entry so it does not ask again unnecessarily.

**Constitutional position:** ENG-12.1 gate provisioning is delegated to `skill-sonarqube-compliance-gate` (the `followed_by` skill). This skill surfaces the setup dialog and records the outcome; the follow-on skill owns the provisioning requirement. If the governance reviewer requires a formal law exception, the documented `project-rules.md` entry and ticket reference constitute the auditable deferral record required by ENG-6.7.

---

### Finding 2 — ENG-4.11: Mutation Testing Takes Too Long to Run, Score Too Long to Build

**The real constraint:** In large legacy codebases:
- A full Pitest/mutmut run can take 30–90 minutes on even a moderate seam
- Getting from a typical legacy baseline (10–25%) to 70% requires multiple refactoring cycles, not one
- Blocking "get to code" on a 70% threshold in the first session defeats the skill's entire purpose

The review panel's fix ("≥70% required; human waiver to proceed") was validated as creating a session-ending block on an activity that is genuinely valuable — just not on Iteration 1.

**Alternatives Considered:**

**A. Hard gate at 70% from Iteration 1.** *Rejected.* Blocks engineers for hours or sessions. Contradicts the skill's mission.

**B. Exemption: characterization tests are ENG-4.11-exempt scaffolding (original P0 fix).** *Partially correct.* The exemption argument is constitutionally sound (ENG-4.10 establishes characterization tests as transitional scaffolding). However, it still leaves no escalation path toward 70% — the skill would simply never reach compliance.

**C. Background/natural-break scheduling.** *Accepted as primary mechanism.* Mutation testing is an async-friendly activity: kick it off before lunch, at end of session, overnight, or before a PR review, and the results are waiting. The skill frames it this way explicitly.

**D. Progressive iteration ladder (chosen).** Track iteration count in `project-rules.md`. The gate escalates across iterations, framing each check as a coaching message rather than a blocker:

| Iteration | Mutation Gate | Agent Message |
|-----------|--------------|---------------|
| 1–2 | Record score only | *"Mutation score: X% — recorded as your baseline. Nothing to act on now."* |
| 3–4 | Record + compare delta | *"Score is X% (was Y% in Iteration N). Trending right direction — no gate yet."* |
| 5+ (session end) | Gentle nudge at natural break | *"When you have a natural break — overnight, before a meeting, end of sprint — that's a great time to run a longer mutation session and push toward the ENG-4.11 target of 70%. No action needed right now."* |
| Explicit break detected | Offer to run | *"You mentioned you're stepping away — this is a perfect time to kick off mutation testing in the background. Want me to start the run before you go?"* |
| Iteration 7+ | Soft gate | Score below 70% surfaces in the iteration STOP report with a path to resolution, but does not block the next iteration |

**Tracking:** Iteration count and per-iteration mutation scores are recorded in `project-rules.md` under a `## Mutation Testing Progress` section. The agent reads this at session start to know which rung applies.

**Constitutional position:** Characterization tests (Phase 3c) are explicitly ENG-4.10 scaffolding, exempt from ENG-4.11 at that phase. ENG-4.11's ≥70% threshold is the *target state* the ladder progresses toward, not a first-session gate. If the governance reviewer requires a formal exception: the progressive ladder constitutes a documented compliance plan, which satisfies ENG-6.7's audit trail requirement.

---

### Changes

| Artifact | Change |
|----------|--------|
| `02-pragmatic-adoption.md` | Phase 3d heading: "Optional — Recommended" → "SonarQube Setup" (neutral) |
| `02-pragmatic-adoption.md` | Phase 3d: "optional/recommended" language → 5-option informed choice dialog (A–E) |
| `02-pragmatic-adoption.md` | Iteration summary: "optional baseline now, or defer" → "SonarQube setup dialog (server / Docker / IDE plugin / defer)" |
| `02-pragmatic-adoption.md` | Phase 3c mutation note: characterization tests declared ENG-4.10 scaffolding, exempt from ENG-4.11 at this phase |
| `02-pragmatic-adoption.md` | Mutation testing: progressive iteration ladder with natural-break scheduling replacing hard 70% gate |
| `02-pragmatic-adoption.md` | `project-rules.md` templates: add `## Mutation Testing Progress` tracking section |
| `02-pragmatic-adoption.md` version | `2.12.0` → `2.13.0` |

---

## Amendment 14 — Idempotent Governance Setup

**Date:** 2026-05-08

### Problem

If an engineer runs the skill on a project that already has `AGENTS.md` and/or
`hangar-ai-specs/` from a previous adoption run (or a previous session), Step 2 had no
guard against overwriting those files. An AI agent following the skill literally would
re-create `AGENTS.md` with default content, wiping project-specific configuration built
up over previous cycles.

This also blocked re-entry: engineers who had done governance setup but not yet started
characterization had no clean way to resume without re-running the full setup.

### Alternatives Considered

**A. Flag file approach** — write a `.adoption-complete` sentinel file during setup,
check for it at the top of Step 2. *Rejected*: fragile (easy to delete accidentally),
non-obvious to humans reading the directory, doesn't handle partial completion.

**B. Idempotent pre-flight check (chosen)** — before each sub-step, check whether the
artifact already exists. If it does, read it (to understand current state) and skip
creation. This is the standard infrastructure-as-code pattern (Terraform, Ansible
idempotency) applied to governance artifact creation. Handles partial completion
naturally: only missing pieces are created.

**C. Overwrite with merge** — diff existing AGENTS.md against template and apply only
missing sections. *Rejected*: complex to specify for an AI, high risk of corrupting
intentional project-specific customizations. The "don't touch what's there" rule is
safer.

### Solution

- Added a **⚠️ Idempotency rule** callout at the top of Step 2.
- Added an explicit **pre-flight check** table listing 5 artifacts with skip conditions.
- Updated each row of the Step 2 action table with "If present / If missing" branching.
- Updated the Step 1 lead-in to point to the pre-flight check instead of implying a
  binary "exists or not" decision.
- Report language: agent must report what was skipped and what was created. If
  everything already exists, say so clearly and proceed directly to Step 3.

### Changes

| Artifact | Change |
|----------|--------|
| `02-pragmatic-adoption.md` | Step 2 rewritten with idempotency rule + pre-flight check |
| `02-pragmatic-adoption.md` | Step 1 lead-in updated to point to Step 2 pre-flight |
| `02-pragmatic-adoption.md` version | `2.11.0` → `2.12.0` |

---

## Amendment 13 — "What's Next" Post-Adoption Section

**Date:** 2026-05-07

### Problem

The skill ended at the Key Files reference section with no forward direction. Engineers
who completed adoption had no signal about what to do next or how the pattern they just
learned connects to their ongoing feature development work.

### Solution

Added a "What's Next — After Adoption Is Complete" section at the end of the skill:

1. **Pattern continuity** — explicit statement that Proposal → tasks.md → implementation
   is the same cycle for every future change (features, bug fixes, refactoring). Nothing
   structurally changes; only the proposal content changes.

2. **5-step next steps table** with links to the relevant skill or guide for each:
   - Archive adoption iterations (spec-governance)
   - Start first feature (skill-spec-governance trigger)
   - Atomic TDD for all new code (06-atomic-tdd)
   - Continue refactoring iteratively (09-refactoring)
   - Full how-to guide prompt patterns (how-to-adopt-constitution.md Step 5)

3. **Starter prompt template** — a copy-paste prompt the engineer sends to their AI
   assistant to kick off their first feature, pre-wired with the correct constitutional
   instructions (ENG-11.1 proposal, ENG-4.1 TDD, Trust Ramp rung from project-rules.md).

4. **"What the constitution gives you from here"** — a short list reinforcing that the
   skills they built during adoption (seam selection, characterization, TDD cycles,
   design rationale, session sizing, Trust Ramp) all apply permanently, not just during
   the adoption period.

### Changes

| Artifact | Change |
|----------|--------|
| `02-pragmatic-adoption.md` | "What's Next" section added at end of Key Files block |
| `02-pragmatic-adoption.md` version | `2.10.0` → `2.11.0` |

---

## Amendment 12 — Seam-Scoped Coverage Gates (Not Project-Wide)

**Date:** 2026-05-07

### Problem

Coverage gates were expressed as applying to "the seam" in Phase 3c, but without an
explicit prohibition on project-wide numbers the AI could still run a project-wide
report, see a low overall percentage, and treat that as a gate failure. The PHASE_GATE
tier said "new and changed code only" without tying that back to the seam boundary.
SonarQube baseline phase did not specify that metrics should be recorded per-seam-file.

### Changes

| Artifact | Change |
|----------|--------|
| `02-pragmatic-adoption.md` Phase 3c step 3 | ⛔ callout added: "coverage gates apply to the files in this seam — not the entire codebase; project-wide numbers MUST NOT be used to block or judge this phase"; tool scoping guidance (JaCoCo `includes`, pytest `--cov=path`, Stryker glob); fallback for tools that only produce project-wide output |
| `02-pragmatic-adoption.md` PHASE_GATE tier | Updated to "new and changed code **within the seam only**; files outside the seam are exempt" |
| `02-pragmatic-adoption.md` Phase 3d SonarQube baseline | Metrics recorded "for the seam's files only"; ⛔ callout: project-wide numbers informational only; gates measured against seam files |
| `02-pragmatic-adoption.md` version | `2.9.0` → `2.10.0` |

---

## Amendment 11 — Missing Tool Handling in Phase 3c

**Date:** 2026-05-07

### Problem

The skill named coverage and mutation tools per stack but was silent on what to do
if those tools were not installed. Observed behavior: the agent silently skipped the
coverage step rather than asking the human, producing a STOP report with test counts
but no coverage numbers — the exact failure mode Amendment 10 was meant to prevent.

### Solution

Added a pre-run tool check before the coverage/mutation step. If a tool is missing,
the agent does NOT silently skip. It asks the human with three explicit options:

- **A — Install now:** agent runs the install command then proceeds
- **B — You install:** agent waits for human confirmation then proceeds  
- **C — Defer:** agent records `coverage_status: INCOMPLETE` in
  `phase-3-characterize.md` and flags in the STOP report that the 100% line
  coverage gate cannot be confirmed; proceeding to Implement is at the human's
  explicit risk acknowledgement

The STOP report checklist updated to show the `| NOT RUN — tool not installed`
alternative for each metric field, so the deferred case is still a complete report
(just with acknowledged gaps rather than silent omissions).

### Changes

| Artifact | Change |
|----------|--------|
| `02-pragmatic-adoption.md` Phase 3c step 3 | Tool pre-check added; A/B/C dialog block; defer path records `coverage_status: INCOMPLETE`; risk acknowledgement language |
| `02-pragmatic-adoption.md` Phase 3c STOP report | Each metric field shows `{X}% \| NOT RUN — tool not installed` alternative |
| `02-pragmatic-adoption.md` version | `2.8.0` → `2.9.0` |

---

## Amendment 10 — Technology-Agnostic Coverage Tools and Explicit STOP Report Checklist

**Date:** 2026-05-07

### Problem

Reported by the AI agent during live skill execution: coverage and mutation scores were
not included in the Phase 3c STOP report. Root cause: two gaps in the skill text.

**Gap 1 — Java-specific tool names:** Step 3 named JaCoCo and Pitest directly. On
non-Java stacks (Python, Node, .NET) the AI had no guidance and silently skipped the
step rather than substituting the stack-appropriate tool.

**Gap 2 — STOP report content not enumerated:** The instruction said "report the
phase-3-characterize.md baseline" but did not specify which numbers must appear. The
AI reported test counts (easy to observe) but not coverage or mutation percentages
(require running tools). Implicit expectation ≠ enforced behavior.

### Solution

**Step 3 of Phase 3c** replaced with a technology-agnostic instruction that:
- Names coverage and mutation tools for four stacks (Java, Python, Node/TS, .NET)
- Instructs the agent to ask the avatar or check CI pipeline if the stack is unlisted
- States the requirement is the same regardless of tool

**STOP block** replaced with an explicit mandatory checklist. The AI MUST include
every item in the report before asking the SonarQube question:

```
Characterization baseline for: {seam name}
Files in scope: {list}
Tests written: {N} characterization tests
Line coverage (seam): {X}%   ← must be 100% to proceed
Branch coverage (seam): {X}%
Mutation score (seam): {X}%  ← baseline; no minimum required
Tool used: {coverage tool} / {mutation tool}
Full suite: GREEN / FAILING
phase-3-characterize.md: written ✓
```

Note: "do not substitute test counts for coverage numbers" is explicit — the most
common failure mode is reporting "wrote 12 tests" instead of running the tool.

### Changes

| Artifact | Change |
|----------|--------|
| `02-pragmatic-adoption.md` Phase 3c step 3 | Technology-agnostic; stack tool table (Java/Python/Node/TS/.NET); requirement stated as tool-independent |
| `02-pragmatic-adoption.md` Phase 3c STOP block | Explicit mandatory report checklist with all required fields; anti-substitution note |
| `02-pragmatic-adoption.md` version | `2.7.0` → `2.8.0` |

---

## Amendment 9 — Seam Definition, Size Spectrum, and Interactive Discovery

**Date:** 2026-05-07

### Problem

The skill used the word "seam" throughout but never defined it. Phase 3a was a
silent batch scan: the AI scanned, wrote `phase-1-archaeology.md`, checked the task,
and moved on — no user interaction, no scope negotiation. The `ClassName.method()`
example in Phase 3b anchored the AI's (and the engineer's) mental model at
single-class / single-method granularity, even though a well-chosen seam often spans
several collaborating files.

Two consequences observed in practice:
1. AI picked the narrowest possible seam (one class), missing cross-file behavior
2. Engineer had no opportunity to say "I want to focus on just this one file today"
   or "show me the wider cluster" before the seam was already locked

### Solution

**Seam definition block added** at the top of Phase 3a:
- Feathers' definition verbatim: "a place where you can alter behavior in your
  program without editing in that place" — behavioral boundary, not file boundary
- Size spectrum table: Micro (single method) → Object (class + direct collaborators)
  → Cluster (network of small objects) → Subsystem (everything behind a stable interface)
- Selection heuristic: prefer the outermost natural entry point that fully captures
  the behavior under change; seams almost always span more than one file

**Phase 3a restructured into a two-step interactive protocol:**

*Step 1 — Silent scan:* AI reads the bounded context and identifies candidates at
multiple granularities. Nothing is written to disk yet.

*Step 2 — Present + invite exploration:* AI presents 2–4 starter seam candidates
at different sizes with files, violation tiers, and rationale. Then explicitly says:

> "These are starting suggestions — not a final list. Feel free to explore... I will
> not write phase-1-archaeology.md until you confirm the seam."

The agent answers follow-up questions and adjusts scope as many times as needed.
`phase-1-archaeology.md` is only written after explicit user confirmation. The STOP
gate is moved from *after* the file is written to *before* it.

`phase-1-archaeology.md` format updated to record: seam name, behavioral description,
all files in scope, violation tier per file, entry point, and boundary rationale.

**Phase 3b decision table** updated: `ClassName.method()` column replaced with
`SeamName` + `Files in Scope` columns — makes multi-file seams a first-class record.

### Changes

| Artifact | Change |
|----------|--------|
| `02-pragmatic-adoption.md` Phase 3a | Full rewrite: seam definition block; size spectrum table; selection heuristic; two-step interactive protocol; explicit "explore before confirming" instruction; phase-1-archaeology.md written only after confirmation |
| `02-pragmatic-adoption.md` Phase 3b | Decision table gains `Files in Scope` column; `ClassName.method()` example replaced with named-seam + multi-file example |
| `02-pragmatic-adoption.md` version | `2.6.0` → `2.7.0` |

---

## Amendment 8 — GRASP/SOLID/DDD Design Principles and design-rationale.md

**Date:** 2026-05-07

### Problem

The skill referenced ENG-3.1 and listed GoF patterns (Strategy, Command, etc.) but gave
the AI no vocabulary for *why* a particular design was right. Engineers observing the AI
saw it splitting methods mechanically rather than applying principled responsibility
assignment. There was also no requirement to record the reasoning — so the team learned
nothing from the refactoring and junior developers had no reference to understand the
decisions made.

Two specific gaps:
1. **No GRASP/SOLID/DDD framework** — the skill named patterns but not the principles
   that govern when to apply them. Without the framework, the AI defaults to line-counting.
2. **No design rationale artifact** — each iteration produced tests and commits but no
   durable explanation of what was wrong, what was chosen, and why.

### Solution

**Step 5 expanded** into a full Design Principles section covering three frameworks:
- **GRASP** (9 patterns): responsibility assignment by asking "who has the information?"
- **SOLID** (5 principles): class and interface design quality signals and responses
- **DDD** (7 concepts): alignment of code structure with business model and ubiquitous language

ENG-3.1 line limits are explicitly stated as **subservient to good object design**. A
correct design that exceeds 50 lines must be documented with GRASP/SOLID reasoning, not
mechanically split.

**Pattern Application Rule added:** Every refactoring decision must name the pattern(s)
applied and explain why. If no pattern can be named, the decision must be reconsidered.

**Phase 3b (Decision) expanded:** The phase-2-decision.md table now has mandatory
"Pattern(s) Applied" and "Rationale" columns. A verdict without a named pattern is
not accepted.

**Phase 3e (Implement) expanded:** After every non-trivial refactoring step, the agent
updates `design-rationale.md` in the change directory. This file has two mandatory sections:

*Section 1 — Overview (~200 lines, for team leads and senior engineers):*
Covers every significant design decision across all TDD cycles in the iteration.
Format: Decision name → Problem (GRASP/SOLID/DDD violation named) → Pattern(s) →
Chosen design → Alternatives considered → Why this choice. Cumulative; appended after
each cycle.

*Section 2 — Detailed Explanation (for junior and mid-level Java developers):*
Before/after code from the actual codebase. Every pattern named explicitly. For every
non-trivial problem: at least one alternative with either (a) a clear reason for
rejection (primary teaching) or (b) an acknowledgement that both were acceptable
(teaches that engineering judgment matters more than finding the one right answer).
The alternatives discussion is explicitly marked NOT optional.

### Changes

| Artifact | Change |
|----------|--------|
| `02-pragmatic-adoption.md` Step 5 | Expanded to full GRASP/SOLID/DDD reference with tables, pattern application rule, and citation format example |
| `02-pragmatic-adoption.md` Phase 3b | Decision table gains mandatory Pattern(s)/Rationale columns |
| `02-pragmatic-adoption.md` Phase 3e | `design-rationale.md` artifact defined with Section 1 (overview) and Section 2 (detailed) templates and requirements |
| `02-pragmatic-adoption.md` Step 2 tasks.md template | Phase 3e task updated to include design-rationale.md |
| `02-pragmatic-adoption.md` version | `2.5.0` → `2.6.0` |

---

## Amendment 7 — Proposal-First Governance for Each Iteration

**Date:** 2026-05-07

### Problem

The skill created files inside `hangar-ai-specs/changes/{context}/` during Phase 3
(archaeology, decision, characterize) but never explicitly instructed the creation of
`PROPOSAL.md` and `tasks.md` first. Engineers using this skill were working the
content of the SDD lifecycle without experiencing the Proposal → tasks.md →
implementation metaphor the constitution teaches.

### Solution

Two insertion points:

**Step 2 (Governance Setup):** Immediately after `hangar-ai-specs/` is created, create
the first iteration's change directory with a `PROPOSAL.md` and `tasks.md` before any
code work begins. The PROPOSAL.md uses the standard SDD format (ID, status, problem,
scope, laws). The tasks.md pre-populates the Phase 3a–3f checklist. An explicit
explanation note tells the engineer *why* this matters and points to `skill-spec-governance`.

**Phase 3a (Archaeology):** Requires confirming PROPOSAL.md + tasks.md exist before
scanning any code. For iterations 2+, creates them first. Updates PROPOSAL.md status
from `PROPOSE` → `IMPLEMENT` at the start of the work phase.

**Phases 3c, 3d, 3e, 3f:** Each phase checks off its corresponding task in `tasks.md`
when complete, giving the engineer visibility of progress against the proposal.

**Phase 3f (Delta Scan):** After all tasks are checked off, updates PROPOSAL.md to
`IMPLEMENT → ARCHIVE PENDING` and asks the human to confirm archival before proposing
the next bounded context.

### Changes

| Artifact | Change |
|----------|--------|
| `02-pragmatic-adoption.md` Step 2 | PROPOSAL.md + tasks.md templates added; "why this matters" explanation with ENG-6.7 citation and spec-governance pointer |
| `02-pragmatic-adoption.md` Phase 3a | Requires proposal artifacts before archaeology; instructs status update to IMPLEMENT |
| `02-pragmatic-adoption.md` Phase 3b | task check-off added |
| `02-pragmatic-adoption.md` Phase 3c | task check-off added before STOP |
| `02-pragmatic-adoption.md` Phase 3d | task check-off added |
| `02-pragmatic-adoption.md` Phase 3e | task check-off per violation added |
| `02-pragmatic-adoption.md` Phase 3f | task check-off + PROPOSAL.md archive prompt added |
| `02-pragmatic-adoption.md` version | `2.4.0` → `2.5.0` |

---

## Amendment 6 — Optional SonarQube Checkpoint with Persistent Reminder

**Date:** 2026-05-07

### Problem

SonarQube was only at the end of the iteration (Phase 3e Delta Scan). Engineers wanted
the option to run it right after characterization — giving a richer before/after delta —
but without it being a hard gate that blocks Implement. At the same time, deferring it
indefinitely silently loses the baseline value.

### Solution

Inserted Phase 3d (SonarQube — optional, recommended) between Phase 3c (Characterize)
and Phase 3e (Implement). At the end of Phase 3c, the agent explicitly asks:

> "Would you like to run SonarQube now (recommended) or proceed to Implement and run
> it later? I will remind you at each checkpoint until it is done."

If deferred, the agent records `sonarqube_baseline: deferred` in
`phase-3-characterize.md` and includes a reminder callout at every subsequent
checkpoint (start of Implement, start of Delta Scan) until `sonarqube_baseline: done`
is recorded. The Delta Scan phase carries a final "last reminder" note.

### Reminder pattern

| Checkpoint | Reminder shown if deferred? |
|---|---|
| End of Phase 3c (Characterize STOP) | ✅ Explicit ask — run now or defer? |
| Start of Phase 3e (Implement) | ✅ Reminder callout |
| Phase 3f (Delta Scan) | ✅ Final reminder — "last chance before closing iteration" |
| After `sonarqube_baseline: done` recorded | ❌ No further reminders |

### Changes

| Artifact | Change |
|----------|--------|
| `02-pragmatic-adoption.md` | Phase 3d added (SonarQube optional/recommended); Phase 3e Implement carries deferred reminder; Phase 3f Delta Scan restructured to handle both baseline-recorded and deferred cases; final reminder at Phase 3f; sequence summary updated (6 steps → 7 steps); Step 6 report line updated |
| `02-pragmatic-adoption.md` version | `2.3.0` → `2.4.0` |

### What did NOT change

The SonarQube gate tier model (HARD_BLOCK / PHASE_GATE / WARNING), the
characterization phase process, and the Implement phase are unchanged.

---

## Amendment 5 — Feathers Characterization Phase (Phase 3c)

**Date:** 2026-05-07

### Problem

When prompted to "do characterization tests," the AI was observed jumping directly into
refactoring. The root cause: Step 3's iteration sequence had no explicit characterization
phase. The sequence `Archaeology → Decision → Implement` placed the AI in "Implement"
context, which it associates with the Atomic TDD cycle — and the TDD cycle includes
refactoring. There was no hard stop between "write tests" and "change code."

### Solution

Restructured Step 3 to follow the Michael Feathers legacy code approach explicitly:
**identify seams → lock behavior → then (and only then) change logic.**

The sequence is now:
```
1. Archaeology (3a)  → seam discovery + violation inventory
2. Decision    (3b)  → REFACTOR | REWRITE | EXTEND verdict per seam
3. Characterize(3c)  → lock ALL observed behavior — ZERO logic changes  ⛔ HARD STOP
4. Implement   (3d)  → Atomic TDD cycles
5. Delta scan  (3e)  → compare before/after
6. STOP              → await human confirmation before next context
```

Phase 3c enforces the Feathers rule as four explicit mandatory steps:

1. For each seam in the cycle's task list: write characterization tests locking all
   observed behavior before any logic is changed (ENG-4.3). Follows
   `docs/guides/testing/characterization-testing.md` (no internal mocking, test
   behavior not structure, full path coverage).
2. Run full test suite. CI must be green. If existing tests fail, stop and report —
   do NOT fix them; document in `phase-3-characterize.md` and await human decision.
3. Run JaCoCo + Pitest. Document baseline in
   `hangar-ai-specs/changes/{context}/phase-3-characterize.md`:
   - 100% line coverage of the seam (required before proceeding)
   - Pitest mutation score recorded as baseline (no minimum at this phase)
4. ⛔ Do NOT change any logic in this phase. Any production code change is a
   protocol violation.

A mandatory human checkpoint separates Phase 3c and Phase 3d: the agent reports the
`phase-3-characterize.md` baseline and awaits explicit "proceed to implement" before
starting Atomic TDD cycles.

Phase 3d (Implement) carries a safety-net rule: if any characterization test goes red
during Implement, stop immediately and investigate before continuing.

### Changes

| Artifact | Change |
|----------|--------|
| `02-pragmatic-adoption.md` | Step 3 restructured; Phase 3a–3e sub-sections; Phase 3c Characterize with 4 explicit steps, hard stop, and human checkpoint; Phase 3d Implement with characterization safety-net rule |
| `02-pragmatic-adoption.md` frontmatter | ENG-4.3 (Test Quality Law) and ENG-4.6 (Coverage Requirements) added to `laws.references` |
| `02-pragmatic-adoption.md` version | `2.2.0` → `2.3.0` |

### What did NOT change

The SonarQube delta model (Phase 3e), ENG-3.1 guidance, Trust Ramp, and Minimum Viable
Session are unchanged. The restructuring is confined to Step 3's iteration sequence.

---

## Amendment 4 — Remove Mandatory Linter Run from Governance Setup

**Date:** 2026-05-07

### Problem

Step 2 (Governance Setup) included a `Verify (Phase 3)` row that instructed the AI to
run `aa-constitution-lint` and require all structural checks to pass before proceeding.

This was copied verbatim from `workflows/adoption.md` Phase 3 without considering what
the linter actually checks:

| Linter check | State after governance-only pass |
|---|---|
| `AGENTS.md` exists at root | ✅ Will pass |
| `hangar-ai-specs/` exists | ✅ Will pass |
| Test pyramid structure (`tests/unit/`, `tests/integration/`) | ❌ Not yet created — deferred by design |
| Law reference validity | ✅ Will pass |

Running the linter after a governance-only pass **produces failures for work that is
intentionally deferred**. This is a false gate — exactly the kind of all-or-nothing
blocker that pragmatic adoption exists to eliminate. The linter was observed instructing
engineers to fix test directory structure before they had written a single line of code.

### Change

Removed the `| Verify (Phase 3) | Run aa-constitution-lint... |` row from the Step 2
governance setup table. The two linter checks that would pass (AGENTS.md and
hangar-ai-specs/ presence) are verifiable by eye; there is no need to run a tool.

The linter remains appropriate at the end of a **remediation iteration** (Step 3), after
test structure and code changes have been made in that bounded context.

### Skill version

`2.1.0` → `2.2.0`

---

## Amendment 3 — Orientation Triggers and Key Files Reference

**Date:** 2026-05-07

### Problem

After completing an adoption session, engineers and AI agents frequently ask orientation
questions about the files and mechanics that were just created. Examples observed:

- "What happened to my project?"
- "What are these files for?"
- "How does `AGENTS.md` work?"
- "What is `project-rules.md`?"
- "How do lookups work?" / "How does the AI find skills?"
- "What is a Change Proposal?"
- "I don't understand what was created."

These questions arise **mid-adoption** — the person is already working with the pragmatic
adoption skill. However, no skill had trigger phrases matching these questions, so the AI
would fail to route to any guidance. The content that answers them exists (in
`how-to-adopt-constitution.md`, `constitution-overview.md`, `AGENT.md`, and
`spec-governance.md`) but was unreachable via trigger matching from an orientation question.

### Alternatives Considered

| Option | Description | Decision |
|--------|-------------|----------|
| **A — Add triggers + reference section to `02-pragmatic-adoption`** | Orientation trigger phrases added to this skill's frontmatter; a "Key Files" section added to the skill body that answers the four most common questions with one-liners and links to authoritative guides | ✅ **Chosen** |
| **B — Create a new `skill-constitution-orientation.md`** | Separate skill with sole purpose of answering "what is this?" questions | ❌ Rejected — over-engineering; these questions arise in adoption context, not in isolation; adds a 13th skill to maintain with no unique procedure |
| **C — Add content to `constitution-overview.md`** | Expand the existing overview guide with an orientation FAQ | ❌ Rejected — the overview guide is not trigger-routable from mid-adoption questions; adding more prose to a non-skill document does not solve the RAG discoverability gap |

**Why Option A is correct:** The pragmatic adoption skill is the active context when an
engineer is mid-adoption and asks "what is this file?" Adding orientation triggers to the
existing skill means the AI is already loaded and can answer in context. The "Key Files"
section deliberately does NOT reproduce the deep explanations from other guides — it
provides one-liners and explicit links, keeping the skill's focus on procedure while
satisfying the orientation need.

### Changes

| Artifact | Change |
|----------|--------|
| `02-pragmatic-adoption.md` triggers | 16 new orientation phrases added (mid-adoption "what is this?" questions) |
| `02-pragmatic-adoption.md` body | "Key Files — What Was Created and Why" section added at end; covers AGENTS.md, project-rules.md, hangar-ai-specs/, change directories; explains skill routing and authority hierarchy with links; explains Change Proposal lifecycle |
| `02-pragmatic-adoption.md` version | Bumped to 2.1.0 |
| `development-practices/index.yaml` | Trigger list updated with 12 orientation phrases |

### What did NOT change

No guide files were modified. The section deliberately links to existing authoritative
sources rather than reproducing their content.

---

## Amendment 2 — Rename to Pragmatic Adoption

**Date:** 2026-05-07

### Rationale

The original "large codebase" framing undersold the scope of the skill and guide.
The three entry patterns (complex constraints, AI on-ramp, low bandwidth) are equally
applicable to codebases of any size when other adoption barriers are present. Centering
the name on codebase size excluded the audience who needs this guidance most.

"Pragmatic Adoption" captures the unifying intent: adoption that meets the engineer
where they are, on their terms, without prerequisites.

### Changes

| Artifact | Before | After |
|----------|--------|-------|
| Skill filename | `skill-iterative-adoption.md` | `02-pragmatic-adoption.md` |
| Skill `id` | `skill-iterative-adoption` | `02-pragmatic-adoption` |
| Skill `name` | `Iterative Adoption (Large Codebases, AI On-Ramp, Low Bandwidth)` | `Pragmatic Adoption` |
| Guide filename | `iterative-adoption-large-codebases.md` | `pragmatic-adoption.md` |
| Guide title (H1) | `Iterative Adoption for Large Codebases, AI On-Ramp, and Low-Bandwidth Teams` | `Pragmatic Adoption` |
| "Who This Guide Is For" situation label | `Large codebase` (×4) | `Complex constraints` |
| Part 1 Step 1 lead-in | `For large projects, explicitly defer it:` | `In pragmatic adoption, explicitly defer it:` |
| Part 1 Step 3 heading | `Add Iterative Adoption Rules...` | `Add Pragmatic Adoption Rules...` |
| Summary session description | `Add iterative adoption rules...` | `Add pragmatic adoption rules...` |
| `index.yaml` entry | `Iterative Adoption (Large Codebases...)` | `Pragmatic Adoption` |
| `workflows/adoption.md` callout | `skill-iterative-adoption` + large-codebase-only trigger | `02-pragmatic-adoption` + broader trigger including AI on-ramp and low bandwidth |
| Skill version | `1.1.0` | `2.0.0` |

**What did NOT change:** The technique-specific content — the SonarQube delta model,
ENG-3.1 design-first guidance, bounded-context iteration sequence, the Trust Ramp, and
the Minimum Viable Session — all remain unchanged. The rename is a labelling change to
the umbrella concept, not a revision of the approaches within it.

---

**Date:** 2026-05-07

### Additional Problem Statement

The original proposal addressed large-codebase adoption blockers. Review identified two
further situations that benefit from the same iterative approach but arrive from different
starting points:

| Situation | Symptom | Root Cause |
|-----------|---------|-----------|
| **Experienced developers new to AI** | "I don't trust AI to write my code" / "How do I verify what it produces?" | No graduated on-ramp; constitution assumes developer is ready for AI pair programming at full autonomy |
| **Low-bandwidth teams** | "I'm too busy to adopt" / "Can I do this in 30 minutes?" | No minimum viable session guidance; adoption perceived as a large block commitment |

Both situations are solved by the same iterative adoption model already established for
large codebases. The amendment adds:

1. A **Trust Ramp** (4 rungs, Observe → Accelerate) that gives experienced developers
   explicit control over how much the AI does. The developer chooses the rung; the AI
   never suggests moving up. Grounded in ENG-1.2 (AI-Engineer Pairing Law).

2. A **Minimum Viable Session** model with a session-size reference table showing that
   a 30-minute single Atomic TDD cycle is a complete, valid adoption session. State
   is always preserved in `hangar-ai-specs/changes/{context}/` so sessions of any
   length are safe to interrupt.

### Amendment Scope

| Artifact | Change |
|----------|--------|
| `skill-iterative-adoption.md` | Name updated; 20 new trigger phrases added (AI on-ramp + low bandwidth); Trust Ramp and Minimum Viable Session sections added; version bumped to 1.1.0 |
| `docs/guides/adoption/iterative-adoption-large-codebases.md` | Title and "Who This Guide Is For" table updated; Part 6 (Trust Ramp) and Part 7 (Minimum Viable Session) added |
| `development-practices/index.yaml` | Skill name and trigger list updated to reflect amended scope |

---

## Problem Statement

Teams adopting the Hangar AI Constitution on large brownfield codebases encounter four
compounding blockers that cause adoption to stall or be abandoned:

| Blocker | Symptom | Root Cause |
|---------|---------|-----------|
| **Sonar as all-or-nothing gate** | "We have 400 SonarQube violations; we can't fix them all before adopting" | AI conflates HARD_BLOCK, PHASE_GATE, and WARNING tiers — treats all violations as blocking |
| **Monolithic adoption scope** | "The proposal is huge; we can't deliver it in one sprint" | No guidance on scoping adoption to a single bounded context per session |
| **ENG-3.1 line-counting** | "The AI thrashes splitting methods to meet 50-line limits, ignoring object design" | ENG-3.1 interpreted as a counting rule rather than a design quality signal |
| **Forced product avatar analysis** | "We're required to do full product avatar creation before we can start" | Adoption workflow does not make clear that product avatar is deferrable |

There is currently no skill, guide, or workflow callout that addresses any of these
blockers. Teams either push through and abandon, or avoid adopting entirely.

---

## Scope

### In Scope

| Artifact | Path | Description |
|----------|------|-------------|
| New skill | `agent-skills/skills-by-domain/development-practices/skill-iterative-adoption.md` | AI-executable procedure with 17 trigger phrases; includes `project-rules.md` copy-paste templates |
| New guide | `docs/guides/adoption/iterative-adoption-large-codebases.md` | Full reference guide: governance-only first pass, bounded-context iteration sequence, SonarQube delta model, ENG-3.1 design-first interpretation |
| Index update | `agent-skills/skills-by-domain/development-practices/index.yaml` | Register new skill (count: 11 → 12) |
| Workflow callout | `workflows/adoption.md` | Add large-codebase routing note at the top of the workflow |

### Out of Scope

- Changes to existing laws (ENG-3.1, ENG-12.1, ENG-4.6 are unchanged in substance)
- Changes to `workflows/adoption.md` core phases (only a callout note is added)
- Product avatar governance (product avatar deferral is explicitly permitted by the
  existing workflow; this proposal makes it visible and documented)
- SonarQube gate conditions (unchanged; this proposal clarifies how the AI should
  interpret the existing tier model)

---

## Laws Referenced

| Law | How Referenced |
|-----|---------------|
| **ENG-1.2** — AI-Engineer Pairing | Skill implements pairing protocol for large-codebase sessions |
| **ENG-11.1** — Hangar SDD Law | Change governed via `hangar-ai-specs/changes/`; this proposal file |
| **ENG-12.1** — Agentic Feedback Loop | SonarQube delta model clarifies when gate blocks vs. when it informs |
| **ENG-3.1** — Complexity Limits | Guide clarifies design-first interpretation; line limits are design prompts |
| **ENG-3.4** — Single Responsibility | Guide requires extracted units to have single responsibility |
| **ENG-2.3** — Vertical Slice | Bounded-context iteration follows vertical slice decomposition principle |
| **ENG-4.6** — Coverage Requirements | Guide clarifies `new_coverage ≥ 90%` applies to changed code, not full codebase |

---

## Motivation

The four blockers above were identified through direct adoption experience on a large
brownfield project. The existing `docs/guides/adoption/brownfield-adoption.md` covers
the mechanics of brownfield TDD (characterization tests, strangler fig) but does not
address adoption scope, SonarQube delta strategy, or the ENG-3.1 design interpretation
issue.

The Application Guide from the Hangar AI Constitution Workflows course (`exercises/
application-guide.html`) already validates the bounded-context-per-session approach:

> *"Module Size Sweet Spot: 1K–5K LOC per bounded context. For larger systems: pick
> one bounded context to start. Work in separate sessions."*

This proposal encodes that guidance as a first-class, AI-executable skill so it is
automatically discovered — without requiring engineers to know the guide exists.

---

## Acceptance Criteria

1. `aa-constitution-lint .` passes with 0 failures
2. `skill-iterative-adoption.md` is present and indexed in `development-practices/index.yaml`
3. `docs/guides/adoption/iterative-adoption-large-codebases.md` is present
4. `workflows/adoption.md` contains large-codebase routing callout
5. Trigger phrases in the skill cover all four documented blockers
6. `project-rules.md` templates in the skill are copy-paste ready with no unexplained placeholders

---

## Changes Delivered

All changes were implemented in commit `bb0f6ee` on `main`.

| File | Change Type | Notes |
|------|------------|-------|
| `agent-skills/skills-by-domain/development-practices/skill-iterative-adoption.md` | **Created** | 232 lines; skill frontmatter + procedure + templates |
| `docs/guides/adoption/iterative-adoption-large-codebases.md` | **Created** | 426 lines; full guide with worked examples |
| `agent-skills/skills-by-domain/development-practices/index.yaml` | **Updated** | Registered skill; count 11 → 12 |
| `workflows/adoption.md` | **Updated** | Added 2-line large-codebase callout |
