---
phase: 1
title: Capture — aa-jury-gate CLI
project: aa-jury-gate
workflow: greenfield-development
status: CORRECTED-R1
author: Hangar AI (claude-sonnet-4.6)
date: 2026-05-25
r1_corrections: 19
law_citations:
- PRD-2.1
- PRD-2.6
- ENG-4.1
- ENG-4.6
- ENG-4.11
- ENG-6.1
- ENG-6.4
- ENG-6.7
- ENG-11.1
- ENG-12.1
- ENG-12.2
- ENG-12.3
- ENG-14.1
- ENG-14.2
- BUS-7.1
citation_audit:
  allow_draft: []
  draft_skipped: []
  exit_code: 0
  fail_count: 0
  law_count: 125
  pass_count: 15
  registry: /Users/979925/Repos/governance/hangar-ai-constitution/laws/index.yaml
  scanned: 15
  strict: false
  timestamp: '2026-05-26T00:20:23Z'
  tool: aa-citation-audit
  verdicts:
  - context_snippet: null
    id: BUS-7.1
    verdict: PASS
  - context_snippet: null
    id: ENG-11.1
    verdict: PASS
  - context_snippet: null
    id: ENG-12.1
    verdict: PASS
  - context_snippet: null
    id: ENG-12.2
    verdict: PASS
  - context_snippet: null
    id: ENG-12.3
    verdict: PASS
  - context_snippet: null
    id: ENG-14.1
    verdict: PASS
  - context_snippet: null
    id: ENG-14.2
    verdict: PASS
  - context_snippet: null
    id: ENG-4.1
    verdict: PASS
  - context_snippet: null
    id: ENG-4.11
    verdict: PASS
  - context_snippet: null
    id: ENG-4.6
    verdict: PASS
  - context_snippet: null
    id: ENG-6.1
    verdict: PASS
  - context_snippet: null
    id: ENG-6.4
    verdict: PASS
  - context_snippet: null
    id: ENG-6.7
    verdict: PASS
  - context_snippet: null
    id: PRD-2.1
    verdict: PASS
  - context_snippet: null
    id: PRD-2.6
    verdict: PASS
  version: 0.2.0
  warn_count: 0
---

# Phase 1 — Capture: aa-jury-gate CLI

## 1. Problem Statement

### 1.1 Scope

The Hangar AI Constitution requires a multi-cognition jury (PRD-2.6, NON-NEGOTIABLE)
and human phase-gate enforcement (ENG-12.1, NON-NEGOTIABLE) at every phase boundary in
every workflow. These requirements are currently enforced by language in workflow
documents — prose-advisory instructions that agents can inadvertently bypass.

During the iOS Legacy Rescue Workshop session (2026-05-25), an agent advanced from
Phase 1 (Assess) to opening the artifact for human review without completing the 5-juror
jury deliberation or committing the jury synthesis. The bypass was workflow-sanctioned:
the "Mandatory agent behaviour" block in `legacy-rescue-refactor.md` instructed the
agent to `open` the artifact before the jury gate, creating an implicit "task complete"
signal.

A 5-juror multi-cognition jury identified `aa-jury-gate` as the mechanical solution
during R2 cross-synthesis of the hardening proposal. The judicial synthesis
(claude-opus-4.5) explicitly named this tool as a required backlog item.

> **C-P1-J1-001 applied:** The triggering incident had two concurrent problems:
> (A) a specification bug — the workflow document explicitly instructed the wrong
> sequence (`open` before jury), and (B) an enforcement gap — no mechanical check
> existed to validate jury synthesis presence/quality. The workflow document was
> corrected (commit: `fix: harden phase gate enforcement`, 2026-05-25). That fix
> addresses Problem A. `aa-jury-gate` addresses Problem B as defense-in-depth. Both
> fixes are required: prose hardening prevents compliant-but-careless bypasses;
> the CLI prevents adversarial or tool-induced bypasses even when the workflow is
> correctly specified. The tool is not redundant — it is an independent control layer.

### 1.2 Evidence of Harm

| Incident | Impact |
|----------|--------|
| iOS Phase 1 jury bypass (2026-05-25) | Human saw pre-jury artifact; PRD-2.6 + ENG-12.1 violated simultaneously |
| Constitution workflow hardening jury | Unanimous 5-juror convergence: language alone cannot close the enforcement gap |
| Recurrence risk assessment | High — any workflow run without CLI enforcement remains at risk |

> **C-P1-J1-003 applied — N=1 statement:** This project is triggered by a single
> observed incident (N=1). No corpus scan of prior workflow runs has been conducted.
> The investment is justified on the grounds that: (a) a single PRD-2.6 + ENG-12.1
> dual-violation is a categorical constitutional breach, not a frequency-threshold
> issue; (b) the tool is low-cost to build (mirrors existing `aa-citation-audit`
> architecture) and has ongoing value across all workflows; (c) absence of additional
> observed incidents may reflect the workflow being newly adopted, not the problem
> being rare. A corpus scan of archived artifacts is earmarked for Phase 2 to
> establish baseline and confirm the fix is effective.

> **C-P1-J1-002 + C-P1-J5-001 applied — reliability estimate:** A prior juror
> (J5, DevSecOps/Tooling Specialist, gpt-5.4-mini) offered a qualitative estimate of
> ~85% language-based enforcement reliability. This is a juror's reasoned assessment,
> not an empirically measured failure rate — no denominator (total workflow runs) or
> numerator (observed bypasses beyond N=1) exists. It is cited as rationale for
> defense-in-depth, not as a quantitative benchmark.

### 1.3 Root Cause

The triggering incident had a proximate cause (workflow specification bug: `open`
appeared before jury in the gate sequence) and an underlying cause (no mechanical
enforcement exists to validate the jury precondition regardless of workflow prose
quality). The workflow fix addressed the proximate cause. This project addresses
the underlying cause.

> **C-P1-J1-004 + C-P1-J5-006 applied — bootstrapping problem:** A valid concern
> is raised: if agents can skip prose-advisory instructions, what prevents them from
> skipping a `aa-jury-gate` call? The answer is defense-in-depth, not elimination
> of the attack surface:
> (1) The CLI call is a single deterministic command (`aa-jury-gate --synthesis <path>`)
> that is easier for a human reviewer to audit and verify in a session transcript
> than a multi-step jury process.
> (2) The CLI call can be integrated into CI pipelines (P3) where it runs
> unconditionally — not relying on agent compliance at all.
> (3) The tool raises the cost of bypass: instead of skipping a prose instruction,
> an agent must generate a structurally valid fake synthesis. This is acknowledged
> as a residual risk (see §7 — Limitations).
> The tool is not a silver bullet; it is one layer in a multi-layer enforcement stack.

### 1.4 Solution Summary

> **C-P1-J3-001 applied:** `aa-jury-gate` is a **phase-boundary enforcement product**.
> Its CLI validation engine is the mechanism; mandatory invocation at phase boundaries
> (in workflow templates and CI) is the product promise.

`aa-jury-gate` is a Python CLI that:

1. Accepts a `phase-N-jury-synthesis.md` path
2. Validates the frontmatter YAML against the PRD-2.6 / ENG-12.1 schema
3. Validates body sections (Round 1, Round 2, Judicial Synthesis Verdict)
4. Checks the file is committed in git
5. Exits with a defined code (see §4 — Exit Codes)
6. Appends a `jury_gate` block to frontmatter with `--output append` (idempotent)
7. Appends a JSON audit log line per invocation (BUS-7.1) with configurable path

---

## 2. Initiating Context

| Item | Detail |
|------|--------|
| Triggering incident | iOS Phase 1 jury bypass — `legacy-rescue-aadvantage-ios` session 2026-05-25 |
| Judicial synthesis reference | `phase-1-jury-synthesis.md` in `legacy-rescue-aadvantage-ios/` — verdict APPROVED with `aa-jury-gate` as required backlog item |
| Workflow hardening commit | `fix: harden phase gate enforcement` in hangar-ai-constitution (2026-05-25) — addresses spec-bug; this project addresses enforcement gap |
| Constitution repo | `~/Repos/governance/hangar-ai-constitution/` |
| Tool will reside at | `tools/jury-gate/` (mirror of `tools/citation-auditor/`) |
| Required Python | ≥ 3.11 (same as citation-auditor) |
| Applicable workflows | greenfield-development, legacy-rescue-refactor, legacy-rescue-decision-track, legacy-rescue-java-guide, adoption |

---

## 3. Personas

### P1 — Constitution Workflow Agent (Primary)
**Who:** Any Hangar AI agent executing a multi-phase constitution workflow.
**Need:** A machine-enforced gate that fails loudly (exit 1) when the jury synthesis
is missing, malformed, incomplete, or uncommitted — so the agent cannot proceed past
the gate without a valid, committed synthesis.

### P2 — Human Practitioner / Workshop Facilitator
**Who:** AA engineers, mobile platform engineers, workshop facilitators, product coaches.
**Need:** Confidence that when `aa-jury-gate` exits 0, all five PRD-2.6 structural
conditions have been machine-verified and the synthesis is committed in git.

> **C-P1-J3-006 + C-P1-J2-001 applied:** Exit 0 means **structural preconditions**
> are satisfied — not that jury deliberation occurred in fact. See §7 — Limitations.

### P3 — CI Pipeline Enforcer
**Who:** GitHub Actions or similar CI checking phase gate completion on PR merge.
**Need:** A CLI tool with clean exit codes integrable into `- run: aa-jury-gate --synthesis <path>` CI steps.

### P4 — Workflow / Template Maintainer (added per C-P1-J3-002)
**Who:** Constitution maintainers embedding the gate call in workflow templates,
`Makefile` targets, and CI YAML.
**Need:** A tool with a stable CLI contract and clean exit codes that can be wired
unconditionally into workflow templates — so invocation is structural, not advisory.
This persona is the enforcement linchpin: P4 makes the CLI call unavoidable for P1.

---

## 4. Problem Boundaries

### In Scope (v1)

- Frontmatter YAML parsing and schema validation
- `juror_count: 5` check (PRD-2.6)
- Exactly 5 juror entries (J1–J5), each with `id`, `role`, `model`
- All 5 `model` values present, non-empty, and **mutually distinct** (PRD-2.6)
- `claude-haiku-4.5` prohibition — enforced as a **string-match on declared `model` value** (not an execution attestation; see §7)
- `rounds.r1_completed: true` and `rounds.r2_completed: true`
- `verdict: APPROVED` (ENG-12.1)
- `schema_version` field presence (ENG-14.1)
- Required body section presence: headings matching "Round 1", "Round 2", "Judicial Synthesis"
- Git committed check: `git ls-files --error-unmatch <path>`
  - **Fails (exit 1) by default if file is not tracked in git** (per C-P1-J4-001, C-P1-J3-005)
  - `--allow-no-git` flag downgrades to WARN and is recorded in audit log
- BUS-7.1 audit log: JSON line per invocation; path configurable via `AA_JURY_GATE_LOG_DIR` env var (default: `~/.aa-jury-gate/`); write failure is **non-fatal** — emits warning to stderr, does not change exit code
- `--output append`: write `jury_gate` block to synthesis frontmatter (idempotent — second call overwrites prior `jury_gate` block, does not duplicate)
- Exit codes as defined in §4.2

> **C-P1-J2-002 deferred to Phase 4 Design:** Commit-timing check (`git log` depth / timestamp
> assertion to verify synthesis was committed before current gate invocation) is a Phase 4
> design decision pending spike on behaviour in shallow clones, worktrees, and detached HEADs.

### 4.1 Invocation Contexts and Enforcement Posture (added per RC-1 — Judicial Synthesis)

`aa-jury-gate` operates in three distinct invocation contexts with different enforcement guarantees:

| Context | Mechanism | Enforcement posture |
|---------|-----------|---------------------|
| **CI pipeline** (GitHub Actions, etc.) | Wired unconditionally by P4 (Template Maintainer) in workflow YAML | **Hard enforcement** — gate runs regardless of agent compliance; exit 1 blocks phase advance |
| **Local developer / workshop learner** | Called explicitly by agent or human per workflow instructions | **Advisory enforcement** — relies on agent/human compliance; same exit-code contract but no structural block if skipped |
| **Pre-commit hook** | Optional P4-managed hook in `.pre-commit-config.yaml` | **Structural enforcement for local** — blocks commit if synthesis fails gate; opt-in for v1 |

> **V1 scope decision (RC-1):** For local (non-CI) workflows — including workshop learner runs and
> local legacy-rescue sessions — enforcement is **advisory for v1**. The agent or human must call
> `aa-jury-gate` as a workflow step; no structural mechanism prevents skipping in local mode.
> Pre-commit hook support is defined as a v1 out-of-the-box option but is not mandatory.
> CI-based enforcement is the primary hard-enforcement path. Local enforcement hardening
> (mandatory hook, session-level gate) is deferred to v1.1 (C-P1-J5-006 backlog).

### 4.2 Exit Code Contract (added per C-P1-J2-003)

| Code | Meaning | Example trigger |
|------|---------|-----------------|
| 0 | Gate passed — all checks satisfied | All schema, body, git checks pass |
| 1 | Gate failed — policy violation | Missing juror, verdict ≠ APPROVED, uncommitted file, non-distinct models |
| 2 | Invocation error — tool cannot execute check | Path not found, YAML unparseable, git binary not on PATH, malformed args |

Exit 2 is **not** a gate verdict. It means the tool could not perform its check. CI pipelines
must treat exit 2 as a build error distinct from policy failure (exit 1).

### Out of Scope (v1)

- Semantic validation of juror deliberation quality (content review)
- Minimum content-length thresholds for body sections (deferred to v1.1 — C-P1-J4-002 backlog)
- Model compliance policy file (hardcoded haiku ban in v1; policy-file approach deferred — C-P1-J4-003 backlog)
- Cross-artifact jury panel consistency across phases
- `aa-constitution-lint` integration
- Network calls of any kind

---

## 5. Compliance Scope

| Law | Non-Negotiable | Applicability |
|-----|---------------|---------------|
| PRD-2.6 | **YES** | Validates the multi-cognition jury structural requirements |
| ENG-12.1 | **YES** | Validates human gate precondition (jury synthesis committed) |
| ENG-12.2 | No | Jury synthesis distinct from authoring agent |
| ENG-12.3 | No | External referee principle |
| ENG-14.1 | No | `schema_version` presence check |
| ENG-14.2 | No | Law authoring requirements for new tools |
| ENG-4.1 | **YES** | Tool itself built via atomic TDD (RED→GREEN→REFACTOR) |
| ENG-4.6 | No | pytest-cov ≥ 90% on tool source |
| ENG-4.11 | No | mutmut ≥ 85% on core validator module |
| ENG-6.1 | **YES** | Secure implementation: no network, no secrets, stdout clean on exit 2 |
| ENG-6.4 | No | No PII handled; synthesis files are governance artifacts only |
| ENG-6.7 | No | Audit trail via BUS-7.1 gate.log |
| ENG-11.1 | No | Spec-driven development — this Phase 1 artifact is the spec entry point |
| BUS-7.1 | No | Audit log (gate.log) per invocation |
| PRD-2.1 | No | Problem validated in §1 before design begins |

---

## 6. Success Criteria

> **C-P1-J3-004 applied:** Split into product outcomes and engineering quality.

### Product Outcomes

| Criterion | Measure |
|-----------|---------|
| Gate enforcement | `aa-jury-gate` exits 1 on any synthesis missing / structurally invalid / uncommitted |
| False-positive definition | Zero exits 1 on a structurally valid, schema-conformant synthesis with correct sections and committed git status (per C-P1-J2-007) |
| Workflow integration | `legacy-rescue-refactor.md` Step 2 calls `aa-jury-gate` before browser-open |
| Invocation unavoidability | P4 (Template Maintainer) can embed call in CI YAML unconditionally; P3 receives clean exit codes |

### Engineering Quality

| Criterion | Measure |
|-----------|---------|
| Test coverage | pytest-cov ≥ 90% (ENG-4.6) |
| Mutation score | mutmut ≥ 85% on `validator.py` core module (ENG-4.11) |
| Audit trail | Every invocation appends one JSON line to gate.log (BUS-7.1); write failure non-fatal |
| Audit log configurability | `AA_JURY_GATE_LOG_DIR` env var overrides default; CI-safe behaviour documented |

> **C-P1-J3-003 applied:** Phase 0 environment check integration (`aa-jury-gate --version`
> in all workflow env checks) is a Phase 8 — Ship deliverable, not a Phase 1 scope item.

---

## 7. Limitations (added per C-P1-J2-001, C-P1-J5-002, C-P1-J3-007)

> **C-P1-J3-007:** This section distinguishes **artifact validity** from **process validity**.

`aa-jury-gate` enforces **structural preconditions** for a valid jury synthesis. It cannot
verify that the declared juror invocations actually occurred.

**What exit 0 means:**
- The synthesis file exists, is committed in git, and its frontmatter parses as valid YAML
- `juror_count` is 5; exactly 5 juror entries are present with distinct declared model strings
- No declared model matches the `claude-haiku-4.5` prohibition pattern
- Both round-completion flags are `true`
- `verdict` is `APPROVED`
- `schema_version` is present
- Required section headings are present in the body

**What exit 0 does NOT mean:**
- That five independent cognitions deliberated (this cannot be verified from file content alone)
- That the declared model strings correspond to actual model invocations
- That the body content is substantive vs. minimal/stub

**Residual bypass surface — known sub-cases:**

| Sub-case | Description | Planned remediation |
|----------|-------------|---------------------|
| Stub synthesis | Agent generates schema-conformant YAML+sections without running any jurors | v1.1: minimum body content thresholds (C-P1-J4-002 backlog) |
| Frontmatter/body divergence | Frontmatter has `verdict: APPROVED`; markdown body says NEEDS_REVISION or is absent | v1: check body for `VERDICT: APPROVED` string in Phase 3 Define scope decision; in §7 as named bypass surface until then |
| Same-pipeline commit | Agent writes + commits synthesis immediately before calling the gate in one step | Phase 4 Design: commit-timing spike (shallow clone / worktree / detached HEAD test matrix) |
| Model string forgery | Agent declares 5 distinct model strings without invoking those models | Requires API invocation log attestation — out of scope; model distinctness is a declared-value check only |

**Model distinctness canonicalization (T-01):** Two jurors are considered distinct if and only if
their declared `model:` strings are non-identical (case-sensitive full-string comparison). Different
version suffixes (`claude-opus-4.5` vs `claude-opus-4.6`) are treated as distinct. Architectural
similarity is not evaluated — only string identity.

**Path enforcement (T-02):** v1 does not enforce the `hangar-ai-specs/changes/<spec-id>/phase-N-jury-synthesis.md`
path convention. Any file path may be passed. Path convention enforcement is deferred to v1.1.

**Schema version forward-compatibility (T-03):** Unknown `schema_version` values fail closed (exit 1).
The CLI validates only `schema_version: 1`. Files declaring `schema_version: 2` or higher exit 1
with `UNKNOWN_SCHEMA_VERSION` until the CLI is updated.

**Bootstrapping self-exemption:** The initial v1.0.0 release of `aa-jury-gate` cannot validate
its own jury synthesis (the tool did not exist when its Phase 1 synthesis was produced). The initial
release is self-exempt by necessity. All subsequent versions must pass their own gate before ship.

> **C-P1-J4-005 applied — false-positive protocol:** If `aa-jury-gate` exits 1 on a
> genuinely valid synthesis, the remediation path is: (1) run with `--output console` to
> identify the failing check; (2) file a bug report with the synthesis file path and exact
> error output; (3) unblock via `--allow-no-git` (git check only) or by fixing the
> synthesis frontmatter. No break-glass override flag exists in v1 — a false-positive
> must be fixed at the synthesis file, not bypassed at the tool level.
