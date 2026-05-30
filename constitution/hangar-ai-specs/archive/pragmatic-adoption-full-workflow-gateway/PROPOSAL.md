# Proposal: Pragmatic Adoption as Universal Entry Point with Full Workflow Gateway

**Status:** ✅ IMPLEMENT
**Spec ID:** `pragmatic-adoption-full-workflow-gateway`
**Skill:** `02-pragmatic-adoption` (currently v2.16.0)
**Laws:** ENG-1.2, ENG-11.1, ENG-12.1
**Triggered by:** User discovery — "I want to adopt the constitution into this project"
routes to 02-pragmatic-adoption, but the skill only offers paths for users with
specific known constraints. Users who want the standard full adoption have no
guided path from here.

---

## Problem Statement

The constitution has two adoption paths:

1. **Full Adoption Workflow** (`workflows/adoption.md`) — the governed three-phase
   process (Check → Adopt → Verify). Complete, structured, produces all governance
   artifacts. Requires knowing the right prompt from
   `docs/guides/prompts/adoption-workflow-prompt.md`. **Hard to discover.**

2. **Pragmatic Adoption Skill** (`02-pragmatic-adoption`) — the iterative,
   constraint-aware path for large codebases, AI skeptics, and low-bandwidth teams.
   Now also the entry point for any user who says "I want to adopt the constitution."

The current skill presents three entry patterns at the top (complex constraints,
AI on-ramp, low bandwidth) with a Trust Ramp that helps users self-select.
However, **a user who simply wants to do a standard full adoption has no path
from this skill to the full workflow**. The skill assumes the user needs the
pragmatic path; it never asks.

### The Discovery Problem

The full adoption workflow requires a user to:
1. Know `workflows/adoption.md` exists
2. Know `docs/guides/prompts/adoption-workflow-prompt.md` contains ready-made prompts
3. Know to say one of the exact trigger phrases in that workflow's frontmatter

A user who says any plain-language variant ("I want to adopt the constitution,"
"how do I get started," "add the constitution to my project") gets routed to
**02-pragmatic-adoption** (v2.16.0). From there, they currently hit the
pragmatic paths only. The standard full workflow is invisible to them.

### What's Missing

At the very beginning of the skill — before the Trust Ramp and entry pattern
selection — the skill must:

1. **Check adoption status** — detect whether this repo is already adopted, already
   partially adopted, or not yet adopted, so it does not present adoption options
   to a team that has already completed them.
2. **Present a clear two-path choice** — explain the difference between the full
   governed workflow and the pragmatic lightweight path in plain language.
3. **Hand off correctly for each path** — generate a ready-to-use prompt for the
   full workflow; continue into the existing Trust Ramp for the pragmatic path.

---

## Solution

### Step 0a — Adoption Status Check (before any choice is presented)

The skill already checks adoption status when restarting or entering a bare-minimum
refactoring session. This same check must run as the very first action for ALL
trigger phrases.

The agent triggers the adoption Phase 1 check by running:

```
Adopt the Hangar AI Constitution — Phase 1
```

This YAML frontmatter trigger reads the adoption workflow and checks the repo for:
- `AGENTS.md` at repo root
- `hangar-ai-specs/` directory
- `hangar-ai-constitution/` adjacent directory
- `openspec/` presence (pre-rename migration flag)

And produces a **pre-adoption checklist** showing what is present and what is missing.

**Decision from check output (evaluated in order — first match wins):**

| Priority | Check result | Action |
|---|---|---|
| 1 | An open pragmatic adoption proposal exists in `hangar-ai-specs/changes/` (not yet moved to `hangar-ai-specs/archive/`) | Skip gateway entirely — resume the in-progress pragmatic adoption from where it left off. This reuses the existing skill restart-detection logic. |
| 2 | All adoption artifacts present and current | Skip gateway entirely — user is already adopted. Offer Legacy Rescue, Greenfield, or other post-adoption workflows. |
| 3 | Artifacts present but stale or incomplete | Present gateway with "update" context pre-filled |
| 4 | No adoption artifacts found | Present full gateway (Step 0b) |

### Step 0b — Gateway Dialog (two-path choice)

After confirming adoption is needed, present a brief gateway:

> **"Before we start — which of these fits your situation best?**
>
> **Full Adoption** — runs the complete governed process: Check → Adopt → Verify.
> Creates all governance artifacts (AGENTS.md, hangar-ai-specs/, project-rules.md)
> in one structured session. Best for teams ready to spend ~1–2 hours on setup and governance
> before getting to code.
>
> **Guided Lightweight Adoption (Pragmatic)** — guided, iterative, and designed to
> get you to real coding work as fast as possible. Sets up governance incrementally
> around your sprints. Best for large or complex codebases, teams that have tried
> adoption before and got stuck, or anyone who wants to start delivering value
> immediately and layer in governance over time.
>
> Which fits your situation?"

Options:
- **A — Full Adoption** (structured governed process, ~1–2 hours, all artifacts)
- **B — Guided Lightweight (Pragmatic)** (get to coding ASAP, iterative governance)

No diagnostic path. Users self-select. The descriptions are written to be self-sorting.

### Path A — Full Adoption Output

Agent inlines the ready-to-paste trigger phrase:

```
Adopt the Hangar AI Constitution
```

Presents it with:

> "Paste this prompt into a new Copilot Chat session in your project repository.
> It will run the full governed adoption workflow (Check → Adopt → Verify).
>
> For persona-specific onboarding (Technical Coach / Architect / Engineer) and a
> human-readable companion guide, see:
> https://github.com/adeel-ali-aa/hangar-ai-constitution-adoption-guide
>
> Note: SonarQube provisioning (Phase 2b) is optional — if your project isn't
> ready for it, you can skip that phase and adoption is still constitutionally valid."

Agent STOPs — it does not attempt to run the full adoption itself; it hands off
via the inline prompt. The adoption guide is surfaced as a companion resource for
human context, persona routing, and phase-gate evidence guidance.

### Path B — Guided Lightweight (Pragmatic) Adoption

Continues into the existing Trust Ramp and entry pattern selection unchanged.

---

## Relationship to Existing Content

| Existing element | Change |
|-----------------|--------|
| Adoption status check (restart / bare-minimum logic) | Reused as Step 0a — runs for ALL trigger phrases, not just restarts |
| Trust Ramp (Step 1) | Unchanged — becomes Path B |
| Entry pattern selector (complex / AI on-ramp / low bandwidth) | Unchanged — stays inside Path B |
| Step 2 onwards | Unchanged |
| `workflows/adoption.md` | Referenced by Phase 1 check trigger; not modified |
| `docs/guides/prompts/adoption-workflow-prompt.md` | Replaced by inline primary trigger phrase; still valid reference |
| `docs/guides/adoption/how-to-adopt-constitution.md` | Referenced in Path A companion resources |
| `hangar-ai-constitution-adoption-guide` (external) | Surfaced in Path A output as human-facing companion; not modified |

---

## Changes

| Artifact | Change |
|----------|--------|
| `02-pragmatic-adoption.md` | Add Step 0a (adoption check) and Step 0b (gateway dialog) before Trust Ramp; version → 2.17.0 |
| `agent-skills/skills-by-domain/development-practices/index.yaml` | No trigger changes needed (v2.16.0 already covers plain-language phrases) |

---

## Tasks

See `tasks.md`.

---

## Constitutional Notes

- **ENG-1.2 (AI-Engineer Pairing Law):** The gateway is a human-confirmation
  checkpoint — agent does not proceed to either path without explicit user choice.
  Step 0a (adoption check) is read-only; Step 0b waits for explicit user selection.
- **ENG-11.1 (Hangar SDD):** Full adoption (Path A) generates compliant AGENTS.md
  and hangar-ai-specs/ via the governed workflow prompt.
- **ENG-12.1 (Agentic Feedback Loop):** Path A hands off via an inline prompt
  rather than attempting to run the full workflow inline — correct architectural
  boundary between skill and workflow.

---

## Resolved Design Decisions

1. **Inline prompt vs. navigate to prompt file** — Do both: the primary trigger
   phrase is inlined for immediate use; the adoption guide URL is surfaced as a
   companion resource for human-readable context and persona-specific onboarding.

2. **Which triggers fire the gateway** — All adoption triggers. The gateway fires
   for every trigger phrase, but Step 0a (adoption check) runs first. If the repo
   is already adopted, the gateway is skipped entirely and the user is directed to
   post-adoption workflows instead.

3. **Diagnostic LOC threshold** — Removed. The adoption check (Step 0a) detects
   repo status directly from filesystem artifacts, making a LOC-based heuristic
   unnecessary. The two-path descriptions are written to be self-sorting: teams
   who need iterative governance will recognise themselves in Path B without being
   asked to count lines of code.

---

## Amendment 1 — Feathers Technique Completeness (Phase 3b)

**Problem:** The EXTEND verdict callout in Phase 3b names only Sprout Class and
Wrap Method — two of Feathers' five core safe-modification techniques. Sprout
Method (the most commonly used middle-ground technique) and Wrap Class (the
class-level Decorator equivalent) are absent, creating gaps that cause the AI
to reach for Sprout Class when Sprout Method would be the better fit, and to
miss Wrap Class for multi-method seams entirely. The list also implies it is
exhaustive, discouraging use of other WELC techniques.

**Change:** Expand the EXTEND verdict callout in Phase 3b to:
1. Add **Sprout Method** — new behavior as a new method in the same class;
   smallest-footprint extension technique.
2. Add **Wrap Class** — Decorator pattern at the class level; use when EXTEND
   spans multiple methods on the same class.
3. Add an **escape hatch** line opening the language to other WELC techniques
   (Extract Interface, Parameterize Constructor, Subclass and Override) with a
   pointer to WELC Chapter 25 for the full decision tree.
4. Add a concise **selection heuristic** so the AI can choose among the four
   named techniques without asking the human every time.

**Artifact:** `02-pragmatic-adoption.md` — Phase 3b EXTEND callout only; version → 2.17.1
