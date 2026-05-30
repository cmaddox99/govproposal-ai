---
spec_id: renderer-enhanced-discovery-template
title: "Enhanced Discovery Template + Ensemble Verdict for aa-artifact-render"
status: PROPOSED
triggered_by: "Jay Tu — 2026-04-16 product discovery field study review"
scope: "tools/artifact-renderer"
laws_applied:
  - ENG-13.1
  - ENG-4.1
  - ENG-4.2
  - BUS-7.1
  - PRD-2.5
---

## Problem

The `aa-artifact-render` tool currently generates print-optimised governance documents
using a generic page-layout design system (AA blue `#003087` / AA red `#C8102E`).
Product-discovery stage artifacts (Stage A–F) require a richer web-native template that:

1. Renders the full stage-navigation bar (A–F with done/active/locked states)
2. Surfaces an **ENG-13.1 Render Gate** panel (APPROVE / ENHANCE / REJECT)
3. Presents an **Ensemble Agent Verdict** — a panel with per-persona PASS/WARN/FAIL
   verdicts that aggregate into one constitutional verdict on the build
4. Uses the enhanced AA constitutional design tokens seen in the gate-mgmt Stage B
   field-study artifact (`stage-b-field-study.html`)

Without this, every product-discovery HTML artifact must be hand-authored rather than
generated from structured Markdown frontmatter, violating PRD-2.5 (Stage-Gate Law)
and making it impossible to enforce ENG-13.1 at render time.

## Proposed Solution

### 1. `VerdictEngine` (`verdict_engine.py`)

A pure-Python class that accepts a list of persona verdict dicts (from frontmatter)
and returns a structured `EnsembleVerdict`:

- Each persona carries: `persona`, `law`, `verdict` (PASS | WARN | FAIL), `note`
- Aggregate rule: ALL PASS → `APPROVED`; any WARN + no FAIL → `APPROVED_WITH_CONDITIONS`;
  any FAIL → `BLOCKED`

### 2. `discovery` Jinja2 Template (`discovery.html`)

A standalone (not `_base.html`) template matching the gate-mgmt design:

- Dark gradient header with stage badge, mode, tier, spec_id, laws
- Stage navigation bar (A–F with done/active/locked CSS)
- Two-column layout (main content + sidebar)
- **Render Gate card** with APPROVE/ENHANCE/REJECT JS buttons
- **Ensemble Verdict panel** — per-persona rows + aggregate badge
- Interactive checklist, discovery progress, spec artifacts sidebar
- All CSS/JS self-contained (no external dependencies)

### 3. Renderer + CLI update

- Add `discovery` to `_KNOWN_TYPES` in `renderer.py` and CLI validation
- Pass ensemble verdict data (pre-aggregated by `VerdictEngine`) to template

### 4. High test coverage with mutation testing

- Add `mutmut` to dev dependencies for mutation testing
- Target ≥ 90% line coverage; ≥ 80% mutation score for `verdict_engine.py`

## Acceptance Criteria

- [ ] `VerdictEngine.evaluate()` correctly aggregates PASS/WARN/FAIL → aggregate verdict
- [ ] `discovery` type renders without error with minimal frontmatter
- [ ] Rendered discovery HTML contains: stage nav, render gate, ensemble panel, law tooltips
- [ ] No external CSS/JS links in rendered output (self-contained — ENG-13.1)
- [ ] `aa-artifact-render --artifact-type discovery` accepted by CLI
- [ ] `pytest` with coverage ≥ 80% (gate already enforced in pyproject.toml)
- [ ] `mutmut run --paths-to-mutate src/aa_artifact_render/verdict_engine.py` → ≥ 80% killed
- [ ] `aa-constitution-lint .` → 0 new failures

## Audit Log

| Date | Actor | Action |
|------|-------|--------|
| 2026-04-16 | Jay Tu | Spec created — renderer-enhanced-discovery-template |
