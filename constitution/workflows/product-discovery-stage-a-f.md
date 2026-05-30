---
workflow:
  id: product-discovery-stage-a-f
  name: Product Discovery — Stage A through F
  version: "2.2.0"
  avatar_context: [product, business]
  laws: [PRD-2.1, PRD-2.2, PRD-2.3, PRD-2.4, PRD-2.5, PRD-2.6, PRD-3.1, PRD-3.2, PRD-4.1, PRD-4.2, ENG-4.11, BUS-7.1, ENG-11.1, ENG-11.2, ENG-13.1, ENG-13.2, ENG-10.1, ENG-14.1, ENG-14.2]
  skills: [skill-product-discovery-orchestration, skill-02-user-journey-mapping, skill-03-executable-spec, skill-01-roadmapping, skill-spec-governance]
  preceded_by: adoption
  discovery_modes: [exploratory, accelerated]
  tiers: [tier-1, tier-2]
examples_reference: tools/templates/product-discovery/examples/partner-miles-reference/
steps:
  - name: Initialize
    phase: stage-a
    artifacts: [stage-a-initialize.md]
    laws: [PRD-2.1, PRD-2.5, PRD-2.6, BUS-7.1, ENG-11.1, ENG-11.2, ENG-13.1]  # BUS-7.1: avatar activation and approval are governance-significant actions
    render_gate: true
    jury_gate: true
    template: tools/templates/product-discovery/stage-a-proposal.md
    example: tools/templates/product-discovery/examples/partner-miles-reference/stage-a-proposal.html
  - name: Public Field Study
    phase: stage-b
    artifacts: [stage-b-field-study.md]
    artifacts_tier_1: [personas, "{one of: journey-maps, competitive-analysis}"]
    artifacts_tier_2: [personas, journey-maps, competitive-analysis, user-research-log]
    laws: [PRD-2.3, PRD-2.4, PRD-2.6, PRD-3.1, PRD-3.2, BUS-7.1, ENG-13.1]
    render_gate: true
    jury_gate: true
    template: tools/templates/product-discovery/stage-b-field-study.md
    example: tools/templates/product-discovery/examples/partner-miles-reference/stage-b-field-study.html
  - name: Code Evidence
    phase: stage-c
    artifacts: [stage-c-code-evidence.md]
    laws: [ENG-3.1, ENG-6.7, PRD-2.6, PRD-3.2, BUS-7.1, ENG-13.1]
    render_gate: true
    jury_gate: true
    template: tools/templates/product-discovery/stage-c-code-evidence.md
    example: tools/templates/product-discovery/examples/partner-miles-reference/stage-c-code-evidence.html
  - name: Internal Validation
    phase: stage-d
    artifacts: [stage-d-validation.md]
    laws: [PRD-2.1, PRD-2.2, PRD-2.6, BUS-7.1, ENG-13.1]
    render_gate: true
    jury_gate: true
    template: tools/templates/product-discovery/stage-d-validation.md
    example: tools/templates/product-discovery/examples/partner-miles-reference/stage-d-validation.html
  - name: Metric Rebaseline
    phase: stage-e
    artifacts: [stage-e-metrics.md]
    laws: [PRD-6.1, PRD-2.6, ENG-10.1, BUS-7.1, ENG-13.1]
    render_gate: true
    jury_gate: true
    template: tools/templates/product-discovery/stage-e-metrics.md
    example: tools/templates/product-discovery/examples/partner-miles-reference/stage-e-metrics.html
  - name: Roadmap Lock
    phase: stage-f
    artifacts: [stage-f-roadmap.md, roadmap.md, implementation-proposal.md]
    laws: [PRD-4.1, PRD-4.2, PRD-2.6, ENG-11.1, BUS-7.1, ENG-13.1, ENG-13.3]
    render_gate: true
    jury_gate: true
    template: tools/templates/product-discovery/stage-f-roadmap.md
    example: tools/templates/product-discovery/examples/partner-miles-reference/stage-f-roadmap.html
---

# Workflow: Product Discovery — Stage A through F

> **Laws enforced:** PRD-2.1, PRD-2.5 (NON-NEGOTIABLE), PRD-2.6 (NON-NEGOTIABLE), BUS-7.1 (NON-NEGOTIABLE), ENG-11.1, ENG-13.1 (NON-NEGOTIABLE)
> **Skill:** `skill-product-discovery-orchestration`
> **Render gate:** ENG-13.1 — Every stage transition requires a rendered artifact reviewed by a human before advancement. APPROVE / REJECT / ENHANCE. HTML is the editing surface; **PDF is the cross-platform review surface**.
> **Jury gate:** PRD-2.6 — Every stage exit gate requires a multi-model, multi-persona jury deliberation. A stage with an unresolved CHALLENGED verdict CANNOT advance.

---

## ⚠ READ-BEFORE-PROPOSE GUARD (MANDATORY — ALL AGENTS)

**This guard applies to every agent and every session without exception.**

Before making any proposal, recommendation, correction, or claim within a discovery workflow, an agent MUST:

1. **Read the stage artifact** — Read the current stage's source markdown file in full before proposing changes. Do not rely on memory of a prior turn. Artifacts drift; proposals based on stale reads produce phantom corrections and conflations.
2. **Read the governing law** — For the law cited in the proposal, read the relevant section of the constitution before quoting it. Do not paraphrase laws from memory — cite only what the text actually says.
3. **Read available evidence** — If the proposal makes a causal or quantitative claim, identify the primary source (ADO work item, git commit, grep result, BFF type definition) and read it before asserting the claim. "Should be" or "likely" claims that have a verifiable primary source are not acceptable substitutes.
4. **Declare what was read** — Every proposal MUST begin with a brief provenance statement: what was read, from where, and when in the session. Example: *"I have read stage-c-code-evidence.md (current state), §ENG-3.1 of laws/engineering/quality.md, and ADO work item #1926677 fetched this session."*

**Violation conditions:**
- Proposing a change to an artifact without having read it in the current session → HALT; read then re-propose
- Citing a law by ID without reading its current text → HALT; read then re-cite
- Making a causal claim (root cause, primary driver, primary blocker) based only on pattern matching without reading the underlying source → HALT; read the source
- Reusing a prior-turn read as current without confirming the file has not changed → WARN; re-read if any edits were applied since the last read

> **Rationale (BUS-7.1 · PRD-1.5):** The most common failure mode in discovery sessions is drift — agents paraphrase stale context, conflate IDs, or invent law citations that do not exist. This guard encodes what good human technical writers do instinctively: check the source before writing. It applies to the orchestrating agent and to all sub-agents launched within the discovery workflow.

---

## Pre-Flight (run once per session)

Before initiating Stage A — and any time you have not rendered an artifact in this checkout recently — verify your renderer install is current and matches the constitution repo state:

```bash
# 1. Install or refresh the renderer (idempotent)
./tools/artifact-renderer/install.sh

# 2. Diagnose install state — confirms version, source SHA, branch, drift
aa-artifact-render --diagnose
```

**What to expect from `--diagnose`:**
- `Package version` — the currently-installed semver (e.g., `1.2.0`)
- `Source git SHA (HEAD)` — the constitution checkout your renderer is bound to
- `Source git branch` — should usually be `main`
- `Source git working tree clean` — ✓ unless you have uncommitted local changes
- `Available templates` — must include `discovery` for Stage A–F

**Drift signals (exit code `3`):**
- Source git working tree is dirty → re-render results may not be reproducible from `git checkout`
- Install location does not match the checkout you are working in → CLI is bound to a stale source path
- Library versions differ between your machine and a teammate's → cross-machine output may differ even with identical source

**When two team members see different rendered output:** both run `aa-artifact-render --diagnose` and compare. Divergence in `Install location`, `Source git SHA`, `Python interpreter`, or library versions explains the difference. If everything matches and renders still differ, the cause is browser/OS rendering — switch the review surface to PDF (see §HTML Evidence Gate Protocol).

> **Engineering note (ENG-4.3):** A CI golden-fixture test (`tests/test_determinism.py`) asserts the discovery and proposal renderers produce byte-identical output to checked-in fixtures. Any change to a template, the renderer, or the markdown processor that drifts the bytes will fail CI loudly. Drift never lands silently on `main`.

---

## Discovery ID Convention

Discovery IDs follow the format: `disc-{YYYY}-{NNN}`

- **YYYY** = calendar year the discovery was initiated
- **NNN** = zero-padded sequential number, restarting at 001 each year (e.g., 001, 002, 047)
- **Validation:** ID MUST match `^disc-[0-9]{4}-[0-9]{3}$`. Lowercase only. No other characters.
- **Uniqueness:** Before creating the spec folder, check `ls hangar-ai-specs/changes/disc-{YYYY}-*/` to find the highest existing NNN and increment. If the agent cannot determine the next sequence number, halt and ask the user.
- The Discovery ID is written into stage-a-initialize.md frontmatter as `id:` and into `hangar-ai-specs/changes/{discovery-id}/`.

All artifact paths in this workflow use `[discovery-id]` as shorthand for the full Discovery ID.

---

## Discovery Modes

Every discovery declares its mode in the Stage A stage-a-initialize.md frontmatter. Mode is set once and recorded in every stage-transition audit event.

| Mode | When to use | Stage A evidence | Reviewer at Stage A |
|------|-------------|-----------------|---------------------|
| **Exploratory** | No existing validated problem statement; full PRD-2.1 validation from scratch | Full problem validation exercise; all 4 PRD-2.1 dimensions completed from evidence | Discovery Sponsor (Director+) |
| **Accelerated** | Pre-validated problem statement exists (cited by source + date) | Problem statement block cites prior source; agent flags if source was NOT PRD-2.1-validated and recommends dropping to Exploratory | Problem Statement Author + Discovery Sponsor (Director+) |

Mode selection is self-evidenced by criteria checklist in Stage A stage-a-initialize.md template. Agent actively guides Accelerated mode validation citation and flags non-compliant sources.

---

## Discovery Package Tiers

Declared in Stage A stage-a-initialize.md frontmatter via complexity rubric (5 questions):

| Tier | When | Artifacts per stage |
|------|------|---------------------|
| **Tier 1** | Simple, ≤1 service | discovery-guide + worksheets 01–03 + forward-roadmap + slice-1-ready-brief |
| **Tier 2** | Complex, 3+ services | Full service-recovery model: all worksheets 01–05 + executive-briefing-deck + discovery-guide + forward-roadmap + slice-1-ready-brief + ado-gap-analysis-brief (optional) + discovery-prompt-guide (optional) |

Package manifest declared at Stage A (required / optional / deferred per artifact). See `tools/templates/product-discovery/discovery-package-index.md` for both Tier 1 and Tier 2 manifests.

---

## Stage Table

| Stage | Name | Entry Gate | Key Activities | Exit Gate |
|---|---|---|---|---|
| A | Initialize | Product need identified | Assign Discovery ID (`disc-YYYY-NNN`); activate Product + Business avatars with confirmation record; create `hangar-ai-specs/changes/[discovery-id]/stage-a-initialize.md` from template; define problem statement (PRD-2.1); obtain named stakeholder approval; declare mode and tier; render + human browser review | Problem statement approved by named Product Owner or Discovery Sponsor (Director+); avatars activated and recorded; BUS-7.1 audit event filed; HTML evidence rendered and APPROVED in browser |
| B | Public Field Study | Stage A exit gate met; audit event filed | Market research; competitive analysis (PRD-2.4); user interviews (PRD-3.1); JTBD framing (PRD-2.3); render + human browser review | ≥3 validated user insights; competitive landscape documented in `hangar-ai-specs/`; `stage-b-field-study.md` rendered and APPROVED in browser; audit event filed |
| C | Code Evidence | Stage B exit gate met; audit event filed | Repository ingestion; codebase assessment; domain model extraction; tech debt inventory (ENG-3.1); render + human browser review | Evidence report in `hangar-ai-specs/`; no unreviewed critical findings; `stage-c-code-evidence.md` rendered and APPROVED in browser; audit event filed |
| D | Internal Validation | Stage C exit gate met; audit event filed | Stakeholder review; assumption mapping (PRD-2.2); problem validation (PRD-2.1); blocker resolution; render + human browser review | All blockers resolved; DVFT matrix complete; `stage-d-validation.md` rendered and APPROVED in browser; audit event filed |
| E | Metric Rebaseline | Stage D exit gate met; audit event filed | Define success metrics; baselines; PMF targets (PRD-6.1); measurability confirmed; render + human browser review | Metrics spec in `hangar-ai-specs/specs/`; `stage-e-metrics.md` rendered and APPROVED in browser; audit event filed |
| F | Roadmap Lock | Stage E exit gate met; audit event filed | Now/Next/Later roadmap (PRD-4.2); outcome framing (PRD-4.1); vertical slices defined; implementation proposal created; render + human browser review + PDF | Roadmap approved; implementation `hangar-ai-specs/changes/[impl-id]/` scaffolded; `stage-f-roadmap.md` rendered and APPROVED in browser; PDF generated (ENG-13.3); audit event filed |

---

## Stage A Detail: Initialize

### Step 1: Assign Discovery ID

```
next_nnn = find highest NNN in hangar-ai-specs/changes/disc-{YYYY}-*/ + 1
discovery_id = "disc-{YYYY}-{next_nnn:03d}"
mkdir hangar-ai-specs/changes/{discovery_id}/
```

### Step 2: Activate Avatars

Record avatar activation in stage-a-initialize.md under `## Participating Avatars`:

| Avatar | Constitutional Context | Load Timestamp | Confirming Agent |
|--------|----------------------|----------------|-----------------|
| Product | `product` | ISO-8601 | name or "GitHub Copilot CLI" |
| Business | `business` | ISO-8601 | name or "GitHub Copilot CLI" |

Both Product and Business avatars MUST be activated and recorded before advancing.

### Step 3: Create stage-a-initialize.md

Use `tools/templates/product-discovery/stage-a-proposal.md` as the starting point. Replace all `<PLACEHOLDER>` values. Declare mode (Exploratory/Accelerated) and tier (Tier 1/Tier 2) in the frontmatter.

### Step 4: Obtain Stakeholder Approval

**Approval authority:**
- Required role: Product Owner or Discovery Sponsor (Director level or above)
- Capture method: Signed entry in stage-a-initialize.md `## Stakeholder Approval` block
- Rejection path: Document blocker in stage-a-initialize.md; resolve before advancing
- **Self-certification is PROHIBITED** — the approver must be distinct from the discovery initiator

### Step 5: Render Gate (ENG-13.1 NON-NEGOTIABLE)

```
aa-artifact-render hangar-ai-specs/changes/[discovery-id]/stage-a-initialize.md --laws-dir laws
open hangar-ai-specs/changes/[discovery-id]/stage-a-initialize.html
→ Human reviewer: APPROVE / REJECT / ENHANCE
```

See §HTML Evidence Gate Protocol below for the full gate procedure.

### Stage A Exit Gate

- [ ] Discovery ID assigned in `disc-YYYY-NNN` format
- [ ] `hangar-ai-specs/changes/[discovery-id]/stage-a-initialize.md` created from template
- [ ] Problem statement complete (all 4 PRD-2.1 dimensions filled)
- [ ] Scope defined (in/out table populated)
- [ ] Both Product and Business avatars activated and recorded
- [ ] Mode (Exploratory/Accelerated) and Tier (1/2) declared in frontmatter
- [ ] Stakeholder approval obtained from named approver (Director+); self-certification PROHIBITED
- [ ] HTML evidence rendered via `aa-artifact-render` and APPROVED in browser
- [ ] BUS-7.1 audit event filed in stage-a-initialize.md §Audit Log

---

## Per-Stage Reviewer Roles

| Stage | Exploratory | Accelerated |
|-------|-------------|-------------|
| A | Discovery Sponsor (Director+) | Problem Statement Author + Discovery Sponsor (Director+) |
| B | Product Owner + ≥1 domain expert interviewed | Product Owner + ≥1 domain expert interviewed |
| C | Engineering Lead + Product Owner | Engineering Lead + Product Owner |
| D | Full DVFT stakeholder group | Full DVFT stakeholder group |
| E | Product Owner + Finance/Analytics representative | Product Owner + Finance/Analytics representative |
| F | Executive Sponsor + Product Owner | Executive Sponsor + Product Owner |

---

## Stage Transition Audit Events (BUS-7.1 NON-NEGOTIABLE)

Every stage transition MUST produce an audit event matching the structure defined in `tools/templates/product-discovery/stage-transition-audit-event.yaml`. Partial or unstructured audit notes do not satisfy BUS-7.1.

### Required Fields

```yaml
audit_event:
  discovery_id: disc-YYYY-NNN
  schema_version: "1.2"
  discovery_mode: exploratory | accelerated
  from_stage: A
  to_stage: B
  timestamp: ISO-8601
  actor:
    name: "<full name>"
    role: "<role/title>"
    system: "GitHub Copilot CLI | manual"
  avatars_active:
    - product
    - business
  evidence_artifact: "hangar-ai-specs/changes/disc-YYYY-NNN/stage-a-initialize.md"
  jury_deliberation:                          # REQUIRED — PRD-2.6 NON-NEGOTIABLE
    stage: A
    conducted_at: ISO-8601
    overall_verdict: VALIDATED | QUALIFIED | CHALLENGED
    juror_count: 4
    models_used: [claude-opus-4.5, gpt-5.2, gpt-5.4-mini, claude-sonnet-4.5]  # must be distinct
    corrections_applied: 0
    unresolved_challenged: 0                  # must be 0 for stage to advance
    law_citation: PRD-2.6
  human_browser_review:
    reviewer_name: "<full name>"
    reviewer_role: "<role>"
    review_timestamp: ISO-8601
    decision: APPROVE | REJECT | ENHANCE
    enhancement_round: 0
  exit_gate_conditions:
    - condition: "<gate condition>"
      met: true
      evidence: "<evidence reference>"
  outcome: APPROVED | REJECTED | DEFERRED
  blocker: null
  law_citations:
    - PRD-2.5
    - PRD-2.6
    - BUS-7.1
    - ENG-11.1
    - ENG-13.1
```

### Rules

1. **Every transition.** Each of A→B, B→C, C→D, D→E, E→F, F→complete MUST produce an audit event.
2. **Inline + machine-readable.** Events are stored as rows in the `## Audit Log` table in stage-a-initialize.md AND optionally in a separate `audit.yaml` alongside stage-a-initialize.md.
3. **Fail closed.** If the audit event cannot be recorded, the agent MUST NOT advance. It asks the user to resolve the issue.
4. **Named actors.** The `actor.name` and `actor.role` fields MUST identify a specific person, not a generic role or team name.

### Transitions

```
(initialize) → A → B → C → D → E → F → (complete)
```

---

## HTML Evidence Gate Protocol (ENG-13.1 NON-NEGOTIABLE)

Every stage transition requires a mandatory HTML evidence gate. ENG-13.1 is NON-NEGOTIABLE — no stage advances without a rendered artifact reviewed by a human in a browser.

### Per-Stage Evidence Artifacts

| Stage | Evidence artifact | Template | Render command |
|-------|------------------|----------|----------------|
| A | `stage-a-initialize.md` | `stage-a-proposal.md` (D18) | `aa-artifact-render hangar-ai-specs/changes/[id]/stage-a-initialize.md --laws-dir laws` |
| B | `stage-b-field-study.md` | `stage-b-field-study.md` (D19) | `aa-artifact-render hangar-ai-specs/changes/[id]/stage-b-field-study.md --laws-dir laws` |
| C | `stage-c-code-evidence.md` | `stage-c-code-evidence.md` (D20) | `aa-artifact-render hangar-ai-specs/changes/[id]/stage-c-code-evidence.md --laws-dir laws` |
| D | `stage-d-validation.md` | `stage-d-validation.md` (D21) | `aa-artifact-render hangar-ai-specs/changes/[id]/stage-d-validation.md --laws-dir laws` |
| E | `stage-e-metrics.md` | `stage-e-metrics.md` (D22) | `aa-artifact-render hangar-ai-specs/changes/[id]/stage-e-metrics.md --laws-dir laws` |
| F | `stage-f-roadmap.md` | `stage-f-roadmap.md` (D23) | `aa-artifact-render hangar-ai-specs/changes/[id]/stage-f-roadmap.md --laws-dir laws` |

### Gate Procedure

1. **Render:** `aa-artifact-render hangar-ai-specs/changes/[discovery-id]/{evidence-artifact}.md --laws-dir laws`
   - The renderer auto-detects `discovery` artifact type from frontmatter (`workflow: product-discovery*` + `stage: A|B|C|D|E|F`). No `--artifact-type` flag needed.
   - The success line includes `aa-artifact-render v<version> · type=<type>` for provenance.
2. **For stakeholder / cross-machine / workshop review — also render PDF:**
   ```
   aa-artifact-render hangar-ai-specs/changes/[discovery-id]/{evidence-artifact}.md --pdf --laws-dir laws
   ```
   PDFs embed fonts and normalize layout across browsers and operating systems. **HTML is non-deterministic across machines** (font fallback, emoji rendering, viewport breakpoints, browser cache). Use HTML for live editing; use PDF when more than one person will look at it.
3. **Open:** `open hangar-ai-specs/changes/[discovery-id]/{evidence-artifact}.html` (macOS) or `xdg-open` (Linux). For PDF, open the `.pdf` instead.
4. **Review:** Human reviewer examines the rendered artifact:
   - **"Read correctly" means:** (a) layout renders without broken formatting, (b) law citation tooltips resolve in HTML view (ENG-13.2), (c) all template fields are populated (no `<PLACEHOLDER>` tokens remain), (d) content is complete for the stage's purpose
   - **If the artifact looks wrong on your machine but right on someone else's:** run `aa-artifact-render --diagnose` on both machines and compare. Differences in install location, source SHA, or library versions explain the divergence.
5. **Decision:**
   - **APPROVE** → `human_browser_review.decision: APPROVE` is recorded in the audit event. Stage advances.
   - **REJECT** → Agent documents blocker. Stage does NOT advance. Discovery may be DEFERRED.
   - **ENHANCE** → Agent produces structured checklist of missing items, actively guides remediation, re-renders, re-presents. Maximum **3 enhancement rounds** per stage. Each round logged as a separate audit entry with `enhancement_round: 1/2/3`. After 3 rounds, escalate to Discovery Sponsor.
6. **Stage F formal gate review — PDF is required** per ENG-13.3, not optional. Other stages strongly recommend PDF for any review involving more than the agent + initiator.
7. Record reviewer name, role, decision, and timestamp in the `human_browser_review` block of the audit event.

> **Pending constitutional follow-up:** the source-of-truth for the gate decision should live as a markdown checkbox in the artifact's `## Render Gate` section (per `hangar-ai-specs/changes/render-gate-source-of-truth-capture/stage-a-initialize.md`), not as a DOM-only button click in the rendered HTML. Until that lands, reviewers MUST manually update the artifact's audit log after clicking the in-browser button — the click alone does not record the decision.

---

## Multi-Cognition Jury Gate Protocol (PRD-2.6 NON-NEGOTIABLE)

Every stage exit gate requires a completed two-round jury deliberation before the stage may advance. The human reviewer MUST only ever see the jury-corrected artifact. This section defines the mandatory procedure.

### When to Conduct

The jury deliberation MUST occur after the stage artifact is complete and before the HTML render gate (ENG-13.1) is submitted for human APPROVE. Presenting a pre-jury draft for human approval is a constitutional violation.

```
Stage artifact drafted
    ↓
aa-citation-audit (ENG-14.1) ← pre-jury citation gate; all law IDs verified
    ↓
JURY ROUND 1 (PRD-2.6) ← 5 jurors deliberate independently in parallel
    ↓                     corrections assigned sequential IDs (C-X-001, C-X-002…)
Corrections applied to artifact
    ↓
JURY ROUND 2 (PRD-2.6) ← 5 jurors re-deliberate on corrected artifact
    ↓                     each juror acknowledges Round 1 corrections by ID
JUDICIAL SYNTHESIS      ← confirms zero unresolved CHALLENGED verdicts
    ↓
HTML render gate (ENG-13.1) ← human sees only the jury-corrected artifact
    ↓
Stage advances
```

### Jury Composition (NON-NEGOTIABLE)

Minimum **five jurors**. Each juror MUST be backed by a **distinct LLM model**. Mandatory role coverage:

| Role | **Canonical Model** | What they challenge |
|------|---------------------|---------------------|
| **J1 — Domain Sceptic** | `claude-opus-4.6` | Evidence methodology, source reliability, sample bias, survivorship effects |
| **J2 — Technical Expert** | `claude-sonnet-4.6` | Causal vs correlative claims, root-cause vs symptom, absolute language ("always", "never", "the reason") |
| **J3 — Strategic / Product Lens** | `gpt-5.4` | Framing appropriateness, scope accuracy, audience-readiness, overclaiming vs underclaiming |
| **J4 — Defense Counsel** | `gpt-5.2` | Builds the strongest credible case for the claims — surfaces the minimum defensible version; flags where the artifact is too weak, not too strong |
| **J5 — Devil's Advocate** | `gpt-5.4-mini` | Stress-tests the most dangerous implicit assumptions; actively seeks disconfirming evidence; challenges the problem framing itself, not only the claims within it; flags beliefs that have never been tested |
| **J6 — Citation Auditor** | `aa-citation-audit` | Verifies all law IDs in the artifact are registered and correctly represented (ENG-14.1) |
| **Judicial Synthesizer** | `claude-opus-4.5` | Gate-locking synthesis — MUST be distinct from all 5 juror models |

> **PRD-2.6 HARD REQUIREMENT:** No two jurors (J1–J5) may share the same model ID in the same jury panel. Assigning J3 and J4 to the same model collapses two cognitive perspectives into one and constitutes a non-compliant 4-juror panel. The Judicial Synthesizer must also be distinct from all five juror models.
>
> **Known model limitation:** `claude-haiku-4.5` consistently breaks juror role assignment and refuses to deliberate. Do NOT assign any juror role to `claude-haiku-4.5`.

Four-juror panels are **non-compliant** under this version of the law.

### Investigation Powers (MANDATORY)

Jurors are **empowered and expected** to investigate. Opining on text alone is insufficient for any claim rated Strong or Critical evidence. Jurors SHALL:

- Search git history (`git log`, `git blame`) for commit messages, timestamps, authorship
- Query ADO via REST API for work item descriptions, tags, history, comments, linked items
- Grep source code repositories for function definitions, flag names, call sites
- Read prior stage artifacts for traceability chain consistency
- Fetch any URL or file reference cited in the artifact to verify it exists and says what it is claimed to say
- Declare explicitly when a claim cannot be verified because the source is inaccessible (e.g., external remote config dashboard) — this is a QUALIFIED condition, not silent acceptance

Every juror MUST declare in their verdict which sources they consulted OR state explicitly why a source was inaccessible. "I reviewed the artifact text" alone is not a valid sources declaration.

### Two-Round Protocol (NON-NEGOTIABLE)

**Round 1 — Independent deliberation:**
- All five jurors deliberate in parallel on the drafted artifact.
- Each returns a structured verdict: VALIDATED | QUALIFIED | CHALLENGED with evidence citations.
- The agent collects all verdicts and applies corrections for every CHALLENGED finding and every QUALIFIED condition shared by ≥2 jurors.
- Each correction is assigned a sequential ID (format: `C-[stage letter]-[NNN]`, e.g. `C-A-001`).
- If any juror issues CHALLENGED, the artifact CANNOT advance to Round 2 without applying the correction first.

**Round 2 — Cross-pass on corrected artifact:**
- All five jurors re-deliberate in parallel on the corrected artifact.
- Each juror MUST explicitly acknowledge whether their Round 1 concerns are resolved (by correction ID) and declare any new issues introduced by the corrections.
- Round 2 jurors who do not reference Round 1 corrections are producing an independent re-review, not a cross-pass — this does not satisfy Round 2.
- Any new CHALLENGED verdicts in Round 2 require further corrections before judicial synthesis.

**Single-round deliberation does not satisfy this law** regardless of verdict outcome.

### Verdict Categories

Each juror returns one verdict per evaluated claim (or per artifact section for broad deliberation):

| Verdict | Meaning |
|---------|---------|
| `VALIDATED` | Claim is supported by primary evidence that was independently verified. Juror cites the source. |
| `QUALIFIED` | Claim is plausible but carries conditions, uncertainty, or scope limits that must be stated. Juror specifies the qualifier. |
| `CHALLENGED` | Claim is overclaimed, unverified, or contradicted by available evidence. Juror specifies the correction required. |

### Synthesis Requirement

After Round 2, a **synthesis agent** (distinct from all jurors, may use any model) produces a consolidated judicial finding confirming zero unresolved CHALLENGED verdicts. The synthesis is the gate-locking event:

```
JUDICIAL FINDING — Stage [X]
═══════════════════════════════════════════════════
PROVEN (VALIDATED by ≥3 jurors with independent evidence):
  • [claim] — [evidence citation]

INFERRED (QUALIFIED, stated as conditional):
  • [claim] — Condition: [what must be true]

OVERCLAIMED (CHALLENGED, correction applied):
  • [original claim] → [corrected claim]
  • Correction rationale: [source citation]

UNVERIFIABLE (source not accessible):
  • [claim] — Cannot confirm without [access needed]

OVERALL VERDICT: VALIDATED | QUALIFIED | CHALLENGED
═══════════════════════════════════════════════════
Rounds completed: 2
Corrections applied: [N] (Round 1: [n1], Round 2: [n2])
Unresolved CHALLENGED: 0   ← MUST be 0 to advance
```

An `OVERALL VERDICT: CHALLENGED` or `Unresolved CHALLENGED > 0` blocks stage advancement until corrections are applied and synthesis is re-run.

### Correction Application

- Every CHALLENGED item MUST produce a specific correction to the artifact — not a hedge phrase, a substantive change
- Every QUALIFIED item shared by ≥2 jurors MUST add an explicit qualifier in the artifact (confidence level, scope statement, or uncertainty note)
- Corrections are applied to the source markdown, not only to the HTML
- Each correction is assigned a sequential ID for Round 2 traceability
- After Round 2 corrections, the synthesis is updated and the judicial finding is appended to the artifact's `## Jury Deliberation` section

### Audit Event Extension (BUS-7.1)

The BUS-7.1 stage-transition audit event MUST include a `jury_deliberation` block with `rounds_completed: 2` and `unresolved_challenged: 0`:

```yaml
jury_deliberation:
  stage: C
  rounds_completed: 2
  conducted_at: ISO-8601
  round_1:
    jurors:
      - persona: "Domain Sceptic"
        model: claude-opus-4.6
        verdict: QUALIFIED
        finding: "13 flags conflates two distinct mechanisms — feature gating flags vs data-presence relevancy checks. Grep pattern overcounts."
        sources_consulted: ["ios/featurecontracts-ios/", "grep AAFeatureServiceRecovery"]
      - persona: "Technical Expert"
        model: gpt-5.2
        verdict: CHALLENGED
        finding: "buildFlightDisruptionInfo() returning undefined in test mock ≠ confirmed production failure. No production log evidence cited."
        sources_consulted: ["bff/Mobile-FLIFO-BFF/src/api/services/builders/flightStatusBuilder.ts:807"]
      - persona: "Strategic Lens"
        model: claude-sonnet-4.6
        verdict: QUALIFIED
        finding: "Root cause framing attributes all 4-PI re-planning to FLIFO; ADO feature descriptions cite Combined Eligibility as primary driver."
        sources_consulted: ["ADO Features #1910603, #2047862, #2177921, #2305188, #2441556"]
      - persona: "Defense Counsel"
        model: claude-haiku-4.5
        verdict: VALIDATED
        finding: "FLIFO BFF type gap is real and verifiable. client type lacks reason codes. Minimum defensible claim: FLIFO is a confirmed secondary dependency."
        sources_consulted: ["bff/Mobile-FLIFO-BFF/src/types/flightStatus.ts"]
      - persona: "Devil's Advocate"
        model: gpt-5.4-mini
        verdict: CHALLENGED
        finding: "Implicit assumption that FLIFO is the only BFF affected is untested. Boarding Pass BFF uses same type pattern — blast radius understated."
        sources_consulted: ["bff/Mobile-BP-BFF/src/types/"]
    corrections_applied: 5
  round_2:
    jurors:
      - persona: "Domain Sceptic"
        model: claude-opus-4.6
        verdict: VALIDATED
        round_1_resolution: "C-C-001 (flag count correction) confirmed. Grep re-run validated 2 IROPS flags + 1 relevancy mechanism."
        sources_consulted: ["ios/featurecontracts-ios/ re-grepped post-correction"]
      - persona: "Technical Expert"
        model: gpt-5.2
        verdict: VALIDATED
        round_1_resolution: "C-C-002 resolved — claim now scoped to test mock only, production log caveat added."
        sources_consulted: ["artifact corrected section reviewed"]
      - persona: "Strategic Lens"
        model: claude-sonnet-4.6
        verdict: VALIDATED
        round_1_resolution: "C-C-003 resolved — Combined Eligibility now named as primary driver."
        sources_consulted: ["ADO cross-reference confirmed"]
      - persona: "Defense Counsel"
        model: claude-haiku-4.5
        verdict: VALIDATED
        round_1_resolution: "No Round 1 concerns raised. C-C-004 and C-C-005 (blast radius) strengthen the artifact."
        sources_consulted: ["artifact reviewed"]
      - persona: "Devil's Advocate"
        model: gpt-5.4-mini
        verdict: VALIDATED
        round_1_resolution: "C-C-005 applied — Boarding Pass BFF blast radius now documented. Concern resolved."
        sources_consulted: ["bff/Mobile-BP-BFF/src/types/ re-checked post-correction"]
    corrections_applied: 0
  synthesis:
    overall_verdict: VALIDATED
    rounds_completed: 2
    proven: ["FLIFO BFF exposes {title, message} only — no reason codes", "Two stories and one Feature explicitly tagged flifo_codes"]
    inferred: ["Combined Eligibility is the primary 4-PI re-planning driver — all feature descriptions confirm, but no explicit sequencing study conducted"]
    overclaimed: ["'13 IROPS flags' overcounted — corrected to 2 IROPS gating flags + FLIFO data-presence relevancy mechanism (not a flag)"]
    unverifiable: ["Feature flag production state — requires remote config dashboard access"]
  total_corrections_applied: 5
  unresolved_challenged: 0
  law_citation: PRD-2.6
```

---

## Evidence Traceability Requirements

All discovery evidence must be traceable to its source. The question *"where does this information come from?"* must be answerable from the rendered artifact alone — without the agent, without notes, without memory.

### Stage A — Problem Evidence Registry (PRD-2.1 · BUS-7.1)

Every PRD-2.1 problem statement dimension in Stage A **must** cite at least one source from the `problem_evidence` frontmatter block using the inline syntax `[SRC-A-NNN]`.

**Required fields per problem_evidence entry:**

| Field | Description |
|-------|-------------|
| `id` | Unique ID: `SRC-A-001`, `SRC-A-002`, … |
| `dimension` | One of the 4 PRD-2.1 dimension labels |
| `claim` | The specific assertion being supported |
| `source_type` | `stakeholder_statement` · `market_report` · `prior_discovery` · `complaint_data` · `analytics` · `compliance_mandate` · `field_study` · `other` |
| `source_ref` | Doc path, URL, or prior `disc-YYYY-NNN` ID |
| `system_of_record` | Source system name, `"stakeholder"`, or `"artifact"` |
| `date` | ISO date the source was accessed: `YYYY-MM-DD` |
| `quote` | Verbatim excerpt from the source |
| `confidence` | `High` · `Medium` · `Low` |

**Attribution note (BUS-7.1):** The Stage A stakeholder approval block (`stakeholder.approver` + `stakeholder.date`) satisfies BUS-7.1 attribution for all problem statement decisions. The `problem_evidence` block provides source traceability; the approval block provides decision provenance.

**Rendered output:** The Problem Evidence Registry card appears in the HTML sidebar showing each SRC-A-NNN entry with dimension, source type, date, and verbatim quote.

**Stage A exit gate addition:** `problem_evidence` populated — all 4 PRD-2.1 dimensions cite ≥1 `SRC-A-NNN` entry with `source_ref`, `date`, and `quote`. Uncited dimensions CANNOT satisfy Stage A exit gate.

---

### Stage B — Source Registry (PRD-3.1 · BUS-7.1)

Every insight, persona frustration, JTBD statement, and journey map pain point in Stage B **must** cite at least one source from the `source_registry` frontmatter block using the inline syntax `[SRC-B-NNN]`.

**Required fields per source entry (Tier 1 minimum):**

| Field | Description |
|-------|-------------|
| `id` | Unique ID: `SRC-B-001`, `SRC-B-002`, … |
| `label` | Short human-readable name — e.g. "App Store iOS Reviews" |
| `platform` | One of: `app_store_ios` · `google_play` · `reddit` · `trustpilot` · `user_interview` · `survey` · `analytics` · `internal_report` · `other` |
| `url` | Direct URL or `"internal"` for proprietary sources |
| `retrieved` | ISO date the source was accessed: `YYYY-MM-DD` |

**Additional fields required at Tier 2:**

| Field | Description |
|-------|-------------|
| `record_count` | Number of reviews / responses / records in the source |
| `description` | What this source is and why it was selected |
| `sample_quotes` | Array with at least one verbatim quote per insight category; each quote has `text`, `date`, `rating` (nullable), `category` |
| `methodology_note` | Top-level field describing how all sources were collected and filtered |

**Rendered output:** The Source Registry card appears in the HTML sidebar. Each `[SRC-B-NNN]` citation in prose renders as a clickable chip with platform icon, label, and link. Hovering shows full source metadata.

**Stage B exit gate addition:** `source_registry` populated — all cited sources meet minimum fields; ≥1 verbatim `sample_quote` per insight category (Tier 2).

---

### Stage C — Evidence Glossary (ENG-3.1 · BUS-7.1)

Every critical finding and every HIGH or MEDIUM severity tech debt item in Stage C **must** reference at least one `EVI-C-NNN` entry in the `evidence_glossary` frontmatter block.

**Required fields per glossary entry:**

| Field | Description |
|-------|-------------|
| `id` | Unique ID: `EVI-C-001`, `EVI-C-002`, … |
| `claim` | The specific assertion being supported — e.g. *"BookingViewModel.kt is 2,286 LOC"* |
| `source_file` | Relative path to the evidence document — e.g. `reports/android/androidapps/code-quality-analysis.md` |
| `section` | Section heading or §label within the source |
| `quote` | Verbatim extract from the source document |
| `verified_by` | Full name and date, or `"GitHub Copilot CLI · YYYY-MM-DD (pending human review)"` |
| `verification_method` | One of the five methods below |
| `confidence` | `High` · `Medium` · `Low` — with `confidence_rationale` |

**Verification methods:**

| Method | When to use |
|--------|-------------|
| `direct-file-inspection` | `wc -l`, `grep`, manual read of the actual source file |
| `automated-metrics` | `metrics-snapshot.csv`, `quality-scores.csv` — machine-extracted |
| `report-cross-reference` | Reference to a `reports/` analysis document |
| `manual-code-review` | A human engineer reviewed the code and confirmed |
| `agent-extracted-human-verified` | Agent authored the entry from the corpus; Engineering Lead or Product Owner certified it during Stage C review |

**Agent authorship model:** The agent generates the initial glossary entries from the evidence corpus it analyzed (code quality reports, statechart analyses, metrics CSVs). The human gate is **verification, not authorship** — the Engineering Lead updates `verified_by` to certify each entry before the Stage C exit gate.

**Rendered output:** The Evidence Glossary card appears in the main column as a collapsible table with claim, source file (linked), section, truncated verbatim quote, verification method badge, and confidence indicator (🟢 High / 🟡 Medium / 🔴 Low).

**Stage C exit gate addition:** `evidence_glossary` populated — all critical findings and HIGH/MEDIUM severity tech debt items carry ≥1 `EVI-C-NNN` entry with `source_file`, `quote`, `verification_method`, and `confidence`.

---

### Stage D — Cross-Stage Evidence Map (PRD-2.2 · BUS-7.1)

Every assumption marked **Validated** or **Invalidated** in Stage D **must** reference at least one upstream evidence entry from Stage A, B, or C in the `assumption_citations` frontmatter block.

**Required fields per assumption_citations entry:**

| Field | Description |
|-------|-------------|
| `assumption_id` | Stable ID matching DVFT matrix row: `A1`, `A2`, … |
| `assumption` | Short label matching the DVFT assumption text |
| `status` | `Validated` · `Invalidated` · `Untested` |
| `evaluated_by` | Full name and date, or `"GitHub Copilot CLI · YYYY-MM-DD (pending human review)"` |
| `supporting_evidence` | Array of `{ref, how}` — ref must be a valid upstream ID |
| `confidence` | `High` · `Medium` · `Low` |

**Valid upstream ref formats:**

| Format | Source |
|--------|--------|
| `SRC-A-NNN` | Stage A problem evidence |
| `SRC-B-NNN` | Stage B field study source registry |
| `EVI-C-NNN` | Stage C code evidence glossary |

**Rendered output:** The Cross-Stage Evidence Map card appears in the main column as a collapsible table with assumption ID, status badge, upstream evidence chips (color-coded by stage), and confidence indicators.

**Stage D exit gate addition:** `assumption_citations` populated — all `Validated`/`Invalidated` assumptions carry ≥1 `supporting_evidence` ref with `evaluated_by` (BUS-7.1). No `Validated`/`Invalidated` assumption may have an empty `supporting_evidence` list.

---

### Stage E — Baseline Source Registry (PRD-6.1 · ENG-10.1 · BUS-7.1)

Every metric baseline in Stage E's AARRR table **must** cite at least one `BSL-E-NNN` entry from the `baseline_sources` frontmatter block.

**Required fields per baseline_sources entry:**

| Field | Description |
|-------|-------------|
| `id` | Unique ID: `BSL-E-001`, `BSL-E-002`, … |
| `metric_id` | Stable short ID for cross-referencing from Stage F: `M1`, `M2`, … |
| `metric` | Display name matching the AARRR table metric |
| `baseline_value` | Current measured value with unit |
| `tool` | Analytics tool or dashboard (e.g. Amplitude, Adobe Analytics) |
| `query_or_method` | **Required** — SQL snippet, dashboard filter, or reproducible export method |
| `snapshot_at` | ISO-8601 timestamp when data was captured: `YYYY-MM-DDTHH:MM:SSZ` |
| `owner` | Full name of the metric owner |

**Rendered output:** The Baseline Sources card appears in the HTML sidebar with metric ID, tool, snapshot timestamp, query method, and clickable dashboard link.

**Stage E exit gate addition:** `baseline_sources` populated — all AARRR metric baselines carry ≥1 `BSL-E-NNN` citation with `snapshot_at`, `tool`, and `query_or_method`. Baselines without reproducible sources CANNOT satisfy Stage E exit gate.

---

### Stage F — Decision Traceability (PRD-4.1 · PRD-4.2 · BUS-7.1)

Every roadmap initiative in Stage F — **Now, Next, AND Later** horizons — **must** reference at least one upstream discovery evidence entry in the `roadmap_rationale` frontmatter block.

**Required fields per roadmap_rationale entry:**

| Field | Description |
|-------|-------------|
| `initiative_id` | Stable ID matching roadmap table row: `NOW-1`, `NEXT-1`, `LATER-1`, … |
| `initiative` | Label matching the roadmap row |
| `horizon` | `Now` · `Next` · `Later` |
| `driven_by` | Array of `{ref, type, reason}` — ref must be a valid upstream evidence ID |
| `rationale_confidence` | `High` · `Medium` · `Low` — Low is acceptable for Later items |

**Valid `driven_by` ref formats (any upstream stage):**

| Format | Source |
|--------|--------|
| `SRC-A-NNN` | Stage A problem evidence |
| `SRC-B-NNN` | Stage B field study source |
| `EVI-C-NNN` | Stage C code evidence glossary |
| `BSL-E-NNN` | Stage E baseline source |
| `A#` (e.g. `A1`) | Stage D validated/invalidated assumption |

**`driven_by.type` values:** `user_insight` · `tech_debt` · `market_signal` · `compliance` · `metric_gap` · `assumption`

**Rendered output:** The Decision Traceability card appears in the HTML sidebar showing each initiative with its horizon badge, upstream evidence refs (color-coded by stage), and confidence level.

**Stage F exit gate addition:** `roadmap_rationale` populated — all `Now`, `Next`, and `Later` initiatives carry ≥1 `driven_by` entry. `Later` items may carry `Low` confidence. Roadmap decisions not grounded in discovery evidence CANNOT advance.

---

## Governance Rules

- Stages are sequential. No skipping. (PRD-2.5 NON-NEGOTIABLE)
- Each stage transition requires evidence in `hangar-ai-specs/`. (ENG-11.1)
- Each stage transition requires HTML render + human browser APPROVE. (ENG-13.1 NON-NEGOTIABLE)
- Each stage transition requires a structured BUS-7.1 audit event matching `tools/templates/product-discovery/stage-transition-audit-event.yaml`. Partial or unstructured audit notes do not satisfy BUS-7.1. (NON-NEGOTIABLE)
- **Each stage exit gate requires a completed multi-model jury deliberation with no unresolved CHALLENGED verdicts. (PRD-2.6 NON-NEGOTIABLE)**
- **Each stage exit gate requires `aa-jury-gate` mechanical validation PASS before human review. (PRD-2.6 enforcement)**
- Self-certification is PROHIBITED at Stage A approval. Approver must be distinct from initiator.
- Stage F produces the next implementation proposal.
- All decisions auditable. (BUS-7.1)
- **Agents MUST read artifacts, laws, and primary evidence sources before proposing. See § READ-BEFORE-PROPOSE GUARD.**

---

## Resumability

If session ends mid-workflow, read `hangar-ai-specs/changes/[discovery-id]/stage-a-initialize.md`:
- Check `status:` field in frontmatter (IN_PROGRESS / APPROVED / REJECTED / DEFERRED)
- Check `## Audit Log` for the last recorded stage transition
- Check `## Exit Gate Checklist` for incomplete items
- Resume from the earliest uncompleted stage. PRD-2.5 enforcement: verify all prior stage evidence artifacts and audit events exist before continuing.

---

## Failure Modes

| Failure | Detection | Action |
|---------|-----------|--------|
| Discovery ID collision | `ls hangar-ai-specs/changes/disc-{YYYY}-*/` finds existing NNN | Increment NNN; if unclear, ask user |
| Avatar activation not recorded | Missing rows in §Participating Avatars | Agent halts Stage A; cannot advance |
| Stakeholder approval missing | §Stakeholder Approval status not APPROVED | Agent halts; cannot advance to Stage B |
| Self-certification attempted | Approver name matches initiator name | Agent rejects; requires distinct approver |
| HTML render gate REJECTED | Human answers REJECT | Agent documents blocker; stage does not advance |
| HTML render gate ENHANCE x3 | 3 enhancement rounds exhausted | Escalate to Discovery Sponsor |
| Audit event incomplete | Missing BUS-7.1 required fields | Agent halts; MUST NOT advance until audit event is complete |
| Missing stage evidence | PRD-2.5 check at next stage entry | Return to prior stage; produce missing artifacts |
| Stage B source_registry missing or incomplete | Exit gate check fails | Agent halts; populate `source_registry` with minimum fields before advancing to Stage C |
| Stage B insight has no `[SRC-B-NNN]` citation | Exit gate check fails | Agent flags uncited insight; requires source ID before APPROVE |
| Stage C evidence_glossary entry missing for HIGH/MEDIUM debt item | Exit gate check fails | Agent halts; populate `evidence_glossary` entry with source_file, quote, and verification_method |
| Stage C `verified_by` is agent-only with no human certifier | Exit gate check warns | Agent flags for human certification; advance blocked until a named human is added |
| Stage A `problem_evidence` missing or incomplete | Exit gate check fails | Agent halts; populate `problem_evidence` with ≥1 entry per PRD-2.1 dimension before advancing to Stage B |
| Stage A dimension has no `[SRC-A-NNN]` citation | Exit gate check fails | Agent flags uncited dimension; requires SRC-A-NNN citation before APPROVE |
| Stage D `assumption_citations` entry missing for Validated/Invalidated assumption | Exit gate check fails | Agent halts; populate `assumption_citations` with `supporting_evidence` and `evaluated_by` before advancing to Stage E |
| Stage D `assumption_citations` entry has empty `supporting_evidence` for Validated/Invalidated status | Exit gate check fails | Agent flags assumption as unsupported; requires at least one SRC-A-NNN, SRC-B-NNN, or EVI-C-NNN ref |
| Stage E `baseline_sources` missing or incomplete for AARRR metric | Exit gate check fails | Agent halts; populate `baseline_sources` with `snapshot_at`, `tool`, and `query_or_method` before advancing to Stage F |
| Stage E metric baseline has no `[BSL-E-NNN]` citation | Exit gate check fails | Agent flags uncited baseline; requires BSL-E-NNN citation before APPROVE |
| Stage F `roadmap_rationale` missing for Now/Next/Later initiative | Exit gate check fails | Agent halts; all horizon initiatives require ≥1 `driven_by` entry before Stage F exit gate |
| Stage F `driven_by` ref does not match any upstream evidence ID | Exit gate check fails | Agent flags invalid reference; requires valid SRC-A-NNN, SRC-B-NNN, EVI-C-NNN, BSL-E-NNN, or assumption ID |
| `aa-artifact-render` not available | Command not found | Run `./tools/artifact-renderer/install.sh` from repo root |
| Renderer install drift | `aa-artifact-render --diagnose` exits non-zero (3) or shows wrong source SHA / install location | Re-run install helper; if persistent, `pip uninstall -y aa-artifact-render` then re-install |
| Cross-machine HTML rendering mismatch | Two reviewers see different rendered output from same source | Both run `aa-artifact-render --diagnose`; compare. If installs match, switch to PDF (`--pdf`) — HTML is non-deterministic across browsers/OSes |
| Determinism CI test fails on a PR | `tests/test_determinism.py` reports drift from golden fixture | Either intentional change (re-run `tools/artifact-renderer/regen-golden.sh` and commit the new goldens) or accidental change (revert) |
| Jury gate not conducted before stage advancement | PRD-2.6 check at stage exit | Return to prior stage; conduct jury deliberation; apply corrections before advancing |
| All jury jurors backed by same model | PRD-2.6 §Requirements | Invalidate jury; re-run with at least 4 distinct models |
| Juror verdict lacks evidence citation | PRD-2.6 §Prohibited Anti-Patterns | Return CHALLENGED with note; juror must cite specific source or ADO/git reference |
| CHALLENGED verdict not corrected before gate | PRD-2.6 §Stage blocks on unresolved CHALLENGED verdicts | Agent halts; document unresolved CHALLENGED claim; request correction or formal rebuttal before advancing |
| Proposal made without reading artifact | READ-BEFORE-PROPOSE GUARD | Agent halts; reads current artifact state then re-proposes |
| Law cited from memory without reading text | READ-BEFORE-PROPOSE GUARD | Agent halts; reads law section; corrects citation |
| Causal claim made without reading primary source | READ-BEFORE-PROPOSE GUARD | Agent halts; fetches ADO/git/code source; substantiates or withdraws claim |

---

## Validation Scenarios

### Scenario 1: Happy path (Exploratory / Tier 1)

```
A: Assign disc-2026-003, activate avatars, create stage-a-initialize.md from template,
   obtain Director approval, render HTML, human APPROVES
   → Audit event filed (A → B)
B: Produce field study evidence, render HTML, human APPROVES
   → Audit event filed (B → C)
C: Produce code evidence report, render HTML, human APPROVES
   → Audit event filed (C → D)
D: Complete DVFT matrix, resolve blockers, render HTML, human APPROVES
   → Audit event filed (D → E)
E: Define metrics + PMF targets, render HTML, human APPROVES
   → Audit event filed (E → F)
F: Lock roadmap, produce implementation proposal, render HTML + PDF,
   human APPROVES → Audit event filed (F → complete)
Verify: 6 audit events in §Audit Log, all with APPROVE decision
```

### Scenario 2: ENHANCE loop

```
B: stage-b-field-study.md rendered, human selects ENHANCE
   → Agent produces remediation checklist, guides fixes, re-renders
   → Round 2: human selects ENHANCE again
   → Agent fixes remaining items, re-renders
   → Round 3: human APPROVES
Verify: 3 audit entries for B→C with enhancement_round 1, 2, 0 (final APPROVE)
```

### Scenario 3: Self-certification blocked

```
A: Initiator "Jane Smith" attempts to approve as Discovery Sponsor
   → Agent detects initiator == approver, rejects
   → Agent prompts for a different approver (Director+)
```

### Scenario 4: Accelerated mode with pre-validated source

```
A: Mode = Accelerated, cites disc-2025-047 as prior PRD-2.1 source
   → Agent validates citation exists and was PRD-2.1 compliant
   → If not PRD-2.1-validated: agent recommends dropping to Exploratory
```
