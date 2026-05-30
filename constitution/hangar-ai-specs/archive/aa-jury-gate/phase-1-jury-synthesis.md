---
schema_version: 1
workflow: greenfield-development
spec_id: aa-jury-gate
phase: 1
subject: "Phase 1 — Capture artifact for aa-jury-gate CLI (phase-boundary enforcement product)"
artifact_under_review: phase-1-capture.md
timestamp: 2026-05-25T19:35:00Z

juror_count: 5
distinct_models_required: true
jurors:
  - id: J1
    role: Domain Sceptic
    model: claude-opus-4.6
  - id: J2
    role: Technical Expert
    model: claude-sonnet-4.6
  - id: J3
    role: Strategic / Product Lens
    model: gpt-5.4
  - id: J4
    role: Defense Counsel
    model: gpt-5.2
  - id: J5
    role: Devil's Advocate
    model: gpt-5.4-mini

rounds:
  r1_completed: true
  r2_completed: true

verdict: APPROVED
---

# Multi-Cognition Jury Synthesis — Phase 1 Capture

> **Workflow:** greenfield-development
> **Phase:** 1 — Capture
> **Project:** aa-jury-gate CLI
> **Subject:** Phase-boundary enforcement product for PRD-2.6 / ENG-12.1 mechanical enforcement
> **Timestamp:** 2026-05-25T19:35:00Z

---

## Round 1 — Individual Juror Deliberations

### J1 — Domain Sceptic (claude-opus-4.6)

**Analysis:** Challenged evidence methodology and single-incident justification. Identified that
the artifact conflated a specification bug (workflow instructing wrong sequence) with an enforcement
gap (no mechanical validation). Noted that the ~85% reliability claim was an LLM's estimate, not
empirical data. Identified five corrections.

**Key finding:** The problem statement conflated a specification bug with an enforcement gap. The
single triggering incident is better explained by the former, yet the proposed solution addresses
the latter. No evidence demonstrated the tool would have prevented the actual incident if the
workflow still told the agent to act before calling the gate.

**R1 corrections raised:** C-P1-J1-001 through C-P1-J1-005

**Confidence:** HIGH

---

### J2 — Technical Expert (claude-sonnet-4.6)

**Analysis:** Challenged the causal chain from "tool exits 0" to "jury actually happened." Identified
that the solution validates structural conformance, not jury execution — an agent generating
pre-jury output could commit a conformant-but-fake synthesis. Raised exit code under-specification,
`--output append` idempotency, audit log CI-safety, haiku check as string-match, and the
single-sentence commit-timing deferral as inadequate documentation.

**Key finding:** `aa-jury-gate` validates structural conformance, not jury execution. P2's
confidence that "exit 0 means all PRD-2.6 conditions machine-verified" was architecturally false
as written — PRD-2.6 requires multi-cognition deliberation; the CLI verifies multi-cognition
declaration.

**R1 corrections raised:** C-P1-J2-001 through C-P1-J2-007

**Confidence:** HIGH

---

### J3 — Strategic / Product Lens (gpt-5.4)

**Analysis:** Challenged framing and scope accuracy. Identified that the artifact conflated
file validation with workflow enforcement; the product must define the minimum enforcement
surface as both schema validation AND mandatory invocation. Noted missing Workflow/Template
Maintainer persona (the enforcement linchpin), and that Phase 0 version-check belonged in Ship.

**Key finding:** The artifact conflated "file validation" with "workflow enforcement." Strategically,
the product must define the minimum enforcement surface as both schema validation and mandatory
invocation at phase boundaries.

**R1 corrections raised:** C-P1-J3-001 through C-P1-J3-007

**Confidence:** HIGH

---

### J4 — Defense Counsel (gpt-5.2)

**Analysis:** Surfaced the most dangerous remaining exposure: "presence-only" checks allow trivially
fake syntheses. Non-git WARN was too weak (changed to FAIL). Hardcoded haiku ban is brittle.
Verdict object cross-check (frontmatter vs body) missing. Audit log path problematic for CI.

**Key finding:** Presence-only checks (sections + `verdict: APPROVED`) allow trivially fake
syntheses that still pass, defeating PRD-2.6/ENG-12.1 while appearing compliant.

**R1 corrections raised:** C-P1-J4-001 through C-P1-J4-006

**Confidence:** HIGH

---

### J5 — Devil's Advocate (gpt-5.4-mini)

**Analysis:** Challenged core implicit assumptions. The ~85% claim is ungrounded; the CLI
validates YAML shape, not deliberation; git committed check is weak evidence; model blacklist
is brittle; the real failure may already be fixed by workflow hardening. Most critically:
who enforces that `aa-jury-gate` is actually called?

**Key finding:** The core untested assumption is that a mechanically validated artifact is
equivalent to a mechanically enforced deliberation.

**R1 corrections raised:** C-P1-J5-001 through C-P1-J5-006

**Confidence:** HIGH

---

## Round 1 — Corrections Applied to Artifact

19 corrections applied before R2. Key changes:

| Correction IDs | Change |
|---------------|--------|
| C-P1-J2-001, J5-002 | §7 Limitations added: structural vs. process validity, bypass sub-cases table, remediation cross-refs |
| C-P1-J1-001, J5-005 | Defense-in-depth rationale: spec-bug fix and enforcement gap are distinct; both required |
| C-P1-J1-002, J5-001 | ~85% claim reframed as qualitative juror estimate, not empirical data |
| C-P1-J1-003 | N=1 acknowledged explicitly; cost/benefit justified; corpus scan deferred to Phase 2 |
| C-P1-J1-004, J5-006 | P4 — Workflow/Template Maintainer persona added as enforcement linchpin |
| C-P1-J2-003 | Exit code contract table: 0=gate passed, 1=policy violation, 2=invocation error |
| C-P1-J2-004 | `--output append` idempotency specified (second call overwrites, no duplication) |
| C-P1-J2-005, J4-006 | BUS-7.1 log non-fatal; `AA_JURY_GATE_LOG_DIR` env var; CI-safe |
| C-P1-J2-006 | Haiku check explicitly string-match on declared value (not execution attestation) |
| C-P1-J3-001 | Reframed as phase-boundary enforcement product |
| C-P1-J3-003 | Phase 0 version check moved to Phase 8 Ship scope |
| C-P1-J3-004 | Success criteria split: Product Outcomes / Engineering Quality |
| C-P1-J3-005, J4-001 | Non-git WARN → FAIL by default; `--allow-no-git` flag added |
| C-P1-J4-002 | Minimum body content thresholds deferred to v1.1 backlog |
| C-P1-J4-003 | Model policy-file deferred to backlog (v1: hardcoded haiku string-match) |
| C-P1-J4-005 | False-positive protocol documented in §7 |
| J2 T-01/T-02/T-03 | Model distinctness canonicalization, path enforcement policy, schema version forward-compat |

---

## Round 2 — Cross-Juror Synthesis

### R2 Verdicts

| Juror | R2 Verdict | Key position |
|-------|-----------|--------------|
| J1 (claude-opus-4.6) | ✅ APPROVED | All 5 corrections satisfied; 3 non-blocking notes (verdict enum, malformed YAML exit code, P4 first-mover) |
| J2 (claude-sonnet-4.6) | 🔴 NEEDS_REVISION | 2 blockers: C-P1-J4-004 scope decision; C-P1-J2-002 one-sentence deferral inadequate |
| J3 (gpt-5.4) | ✅ APPROVED | Mostly satisfied; P4 integration contract slightly thin (non-blocking) |
| J4 (gpt-5.2) | 🔴 NEEDS_REVISION | C-P1-J4-004 still open; C-P1-J4-003 deferral contested |
| J5 (gpt-5.4-mini) | 🔴 NEEDS_REVISION | P4 persona realism; CI not universal for local/learner flows; §7 as exploit guide |

### Converging Themes

1. **Structural vs. process validity** — All 5 jurors converged: the CLI validates schema
   conformance, not deliberation occurrence. §7 must be explicit about this. ✅ Applied.

2. **Exit code contract** — J1, J2, J3 all identified the need for formal 0/1/2 semantics.
   ✅ Applied as §4.2.

3. **P4 as enforcement linchpin** — J1 (bootstrapping), J3 (maintainer persona), J4 (unconditional
   invocation) all independently arrived at the same architectural insight: a human-controlled
   CI configuration is the only enforcement mechanism that doesn't rely on agent compliance.
   ✅ Applied as P4 persona and §4.1 invocation contexts.

4. **~85% claim** — J1, J5 both challenged it as ungrounded; J3 implicitly accepted the
   reframing. ✅ Applied.

### Points of Divergence Adjudicated

| Point | J2/J4 position | J1/J3 position | Judicial ruling |
|-------|---------------|----------------|-----------------|
| C-P1-J4-004 verdict body/frontmatter | Blocking (v1 requirement) | Not blocking (design concern) | NOT BLOCKING — editorial addition to §7 sufficient |
| C-P1-J2-002 commit-timing expansion | Blocking (4-element subsection required) | Acceptable deferral | NOT BLOCKING — Phase 4 design scope |
| C-P1-J4-003 model policy file | NOT SATISFIED (J4) | Acceptable deferral (J1) | NOT BLOCKING — hardcoded v1 + named backlog is sufficient capture |
| J5 — CI universality for local/learner | Blocking (capture gap) | Not raised separately | **BLOCKING (RC-1)** — requires invocation context table |
| J5 — §7 as exploit guide | Concern | Not raised | NOT BLOCKING — honest limitations are constitutionally required |

---

## Judicial Synthesis Verdict

### Required Changes Applied

**RC-1 (sole blocking requirement):** §4.1 — Invocation Contexts table added, explicitly declaring:
- CI pipeline: hard enforcement
- Local/workshop learner: advisory enforcement for v1
- Pre-commit hook: optional structural enforcement for local

RC-1 applied to artifact before this synthesis was written. ✅

### Ruling

**VERDICT: APPROVED**

All 19 R1 corrections applied. RC-1 (sole R2 blocking item) applied. The artifact now:

- Honestly scopes what the CLI enforces (structural preconditions, not deliberation occurrence)
- Explicitly declares the local/non-CI enforcement posture as advisory for v1
- Provides a defensible cost/benefit justification for N=1 triggering incident
- Grounds the ~85% claim appropriately as qualitative estimate
- Names all known bypass surfaces with remediation phase assignments
- Defines exit code contract, invocation contexts, model distinctness rule, path enforcement
  policy, and schema version forward-compatibility
- Establishes P4 as the enforcement linchpin and CI as the hard-enforcement path

No third jury round required. Phase 1 Capture is constitutionally sound and ready for human
review and Phase 2 advance authorisation.

---

*Judicial synthesis produced by: claude-opus-4.5*
*Jurors: J1 claude-opus-4.6 · J2 claude-sonnet-4.6 · J3 gpt-5.4 · J4 gpt-5.2 · J5 gpt-5.4-mini*
*Timestamp: 2026-05-25T19:35:00Z*
*R1 corrections: 19 · R2 contested items: 6 · Blocking: 1 (RC-1) · All resolved*
