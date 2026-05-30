---
spec_id: render-gate-source-of-truth-capture
title: "ENG-13.1 Render Gate — Source-of-Truth Capture via Markdown Checkbox (not DOM-only buttons)"
status: PROPOSED
triggered_by: "Workshop session — 2026-04-17 · Adeel Ali (inventor), Ram, Ahmed · AAdvantage partner-miles Stage A demo"
author: Willem (Constitutional Architect)
scope: "tools/artifact-renderer (discovery.html template, renderer docs) + proposal templates (stage-a-proposal.md)"
laws_applied:
  - ENG-13.1
  - PRD-2.5
  - BUS-7.1
  - ENG-11.1
  - ENG-11.2
  - ENG-4.1
relates_to:
  - renderer-enhanced-discovery-template  # Jay's v1.0 that shipped 2026-04-16
---

## Problem

The `aa-artifact-render` tool's **ENG-13.1 Render Gate panel** currently exposes three DOM-only JavaScript buttons — `APPROVE`, `ENHANCE`, `REJECT` — whose `onclick` handlers mutate a local `<div>` and nothing else. The decision:

1. Is never written to any durable store.
2. Is not observable by any agent (Claude, Copilot, Cursor, Windsurf) because agents read the `.md` source-of-truth, not the rendered HTML.
3. Evaporates on page refresh.
4. Produces no audit-trail artifact required by **BUS-7.1**.
5. Gives no BLOCK / PASS signal that can gate Stage B entry under **PRD-2.5**.

Discovered live during a workshop demonstration on 2026-04-17 with the inventor and two stakeholders. When the inventor clicked `APPROVE` in the browser, the agent could not detect the decision — the button was **governance theater**, not governance capture.

This is a latent constitutional violation. Any proposal rendered with `--artifact-type discovery` today passes the "render gate" visually without leaving a decision record in the .md source. A future agent re-reading the source has **no way to distinguish an approved artifact from a drafted one.**

## Proposed Change

Promote the Render Gate decision from a DOM-only click to a **markdown-checkbox row in the artifact's §Audit Log**. The HTML button is demoted to a visual *nudge* — pressing it reminds the reviewer to update the .md file, where the decision actually lives.

### 1. Template change — `stage-a-proposal.md` (and all stage templates)

Add a dedicated Render Gate section with markdown checkboxes, in this canonical shape:

```markdown
## Render Gate (ENG-13.1)

> **NON-NEGOTIABLE:** Reviewer ticks exactly one decision below and fills in the metadata.
> The source-of-truth for the gate decision is THIS FILE, not the rendered HTML.

- [ ] ✅ **APPROVE** — artifact is complete, accurate, law-compliant; next stage may begin
- [ ] 🔄 **ENHANCE** — artifact needs targeted improvement; agent re-renders (max 3 rounds)
- [ ] ❌ **REJECT** — artifact has a blocker; document below and do NOT advance

| Field | Value |
|-------|-------|
| **Reviewer name** | <full name> |
| **Reviewer role** | <Director+ / Product Owner / Discovery Sponsor> |
| **Decision timestamp** | <ISO-8601> |
| **Review method** | <in-browser render · async written · PR approval> |
| **Self-cert?** | <No — distinct from initiator> |
| **Blocker (if REJECT)** | <description or "N/A"> |
| **Enhancement request (if ENHANCE)** | <description or "N/A"> |
```

### 2. Renderer change — `discovery.html` template

The three JavaScript buttons remain visible but their behaviour changes:

- On click, they surface an instructional message:
  > **To record your decision, tick the `[ ]` next to APPROVE in `§Render Gate` of your PROPOSAL.md and fill in the reviewer metadata. The button click alone does not advance the stage.**
- The rendered HTML reads the checkbox state from `§Render Gate` and displays the **persisted decision** (from the .md source) prominently at the top of the Render Gate card, with timestamp and reviewer.
- If no box is ticked: card shows `⏳ PENDING — decision not yet recorded in source`.

### 3. Renderer change — `verdict_engine.py` or new `gate_engine.py`

Add a `RenderGate` parser:
- Reads the `§Render Gate` section from the markdown source.
- Validates exactly one of APPROVE / ENHANCE / REJECT is ticked.
- Returns `GateDecision(verdict, reviewer, timestamp, method, blocker?, enhancement?)`.
- Raises `GateViolation` if multiple boxes ticked, reviewer is the same as initiator (self-cert), or required fields are missing.

### 4. Audit-log automation

On every render, `aa-artifact-render` appends a row to the artifact's `§Audit Log`:

```
| HTML rendered | aa-artifact-render | renderer (ENG-13.1) | CLI | <ISO-8601> | — | <artifact>.html | RENDERED |
```

If a valid APPROVE is parsed from `§Render Gate`, append:

```
| Gate APPROVED | <reviewer> | <role> | <method> | <timestamp> | — | §Render Gate | APPROVED |
```

This satisfies **BUS-7.1** automatically — no agent needs to remember to hand-write the audit event.

## Rationale

| Constitutional principle | Why the checkbox pattern matters |
|---|---|
| **ENG-13.1** (Artifact Rendering) | Renders must carry decisions, not just visuals. Source-of-truth is .md. |
| **PRD-2.5** (Stage-Gate, NON-NEG) | Stage advancement requires a durable, reviewable decision record. DOM is not durable. |
| **BUS-7.1** (Audit Trail, NON-NEG) | Every significant action: who / what / when / where / why / outcome. A JS onclick doesn't log. |
| **ENG-11.1** (Hangar SDD) | The spec directory (`hangar-ai-specs/changes/<id>/`) is the unit of governance. Decisions belong there. |
| **Agent-agnostic** | Claude, Copilot, Cursor all read markdown. None of them observe DOM state. Governance must work across all. |

## Scope

### In Scope
- All Stage A–F proposal markdown templates under `tools/templates/product-discovery/`
- `discovery.html` Jinja template (renderer)
- `verdict_engine.py` / new `gate_engine.py` (decision parsing)
- CLI `aa-artifact-render` (audit-log append on render + gate parsing)
- Renderer docs (README.md)
- Test coverage for the new gate parser (≥90% per ENG-4.1)

### Out of Scope
- Workflow-state management across stages (already handled by `workflow-state.md`)
- Web-UI decision capture (beyond the scope of a static renderer; would require a service)
- Retroactive migration of already-approved artifacts

## Impact

- **Agents** can read gate decisions in any future session — constitutional coherence across agent boundaries.
- **Humans** gain a durable, git-diffable decision record. Every APPROVE is a commit.
- **Governance** — PRD-2.5 and BUS-7.1 become automatically enforceable by the linter (future: `aa-constitution-lint` rule to fail any stage-advance PR whose prior stage lacks a ticked Render Gate).
- **Adoption** — no breaking change to rendered output shape; button remains visible. Reviewer workflow gains one markdown edit per gate (small cost, large governance gain).

## Open Questions

1. Should `ENHANCE` carry a round counter (max 3 per PRD-2.5 Jay-version semantics) stored in frontmatter (`gate_rounds: 2`) rather than in the checkbox section?
2. Should the renderer refuse to render an artifact where initiator == reviewer (self-cert prevention at render time), or log a WARN and let the lint rule hard-block?
3. Should the linter (`aa-constitution-lint`) own the self-cert check, or the renderer? *(Willem's instinct: linter. Renderer should stay single-purpose.)*

## Next Steps

1. Review this proposal with Jay (renderer owner) and Adeel (inventor).
2. If approved, create `tasks.md` with implementation slice (template update → renderer parser → tests → docs → lint rule).
3. Branch: `feat/render-gate-source-of-truth-capture`.
4. Target: release alongside template v1.1 enrichment (see follow-on proposal covering stage-gate cards, PRD-2.1 grid, domain landscape visuals).

---

**Approver (Discovery Sponsor level or above):**

| Field | Value |
|-------|-------|
| Name | Adeel Ali |
| Role | Inventor, Hangar AI Constitution |
| Decision | APPROVED — proceed to tasks.md + implementation |
| Date | 2026-04-17 |
| Method | In-session verbal approval during workshop demo |
| Witnesses | Amal (Product Coach), Amaya (Technical Coach), Ram, Ahmed |
