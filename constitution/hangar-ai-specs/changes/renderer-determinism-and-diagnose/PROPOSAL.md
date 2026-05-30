---
spec_id: renderer-determinism-and-diagnose
title: "Renderer determinism + install-drift visibility — golden fixture CI check, --diagnose CLI command, PDF-preferred workshop renders"
status: PROPOSED
triggered_by: "Workshop session — 2026-04-17 · Adeel Ali · cross-machine drift between Adeel (Mac) and Jay (Windows) on AAdvantage stage-a artifact"
author: Amaya (Technical Coach) / Willem (Constitutional Architect)
scope: "tools/artifact-renderer (cli.py, tests, fixtures) + workflows/product-discovery + docs/README"
laws_applied:
  - ENG-4.1
  - ENG-4.2
  - ENG-4.3
  - ENG-13.1
  - ENG-11.1
  - ENG-11.2
  - PRD-2.5
  - BUS-7.1
relates_to:
  - discovery-template-rich-cards
  - renderer-auto-detect-discovery
---

## Problem

During a 2026-04-17 workshop demo on AAdvantage partner-miles discovery, the inventor (Adeel, Mac) and the renderer owner (Jay, Windows) saw different visual output from what should have been identical Stage A artifacts. Investigation surfaced **three latent failure modes**, none currently detectable without manual diagnosis:

1. **Silent install drift.** `pip install -e tools/artifact-renderer` binds the CLI to a specific source path. If a user later pulls main on a different checkout, or has a non-editable `pip install` lurking in site-packages, or runs in a different Python environment, the CLI continues to serve the old templates. `pip show aa-artifact-render` reports the same version. There is no command that surfaces "your install is bound to checkout X, but you're standing in checkout Y." Embarrassment risk: the rendered HTML is the workshop deliverable, and stakeholders see it before anyone notices the drift.

2. **No golden-fixture regression test.** Any change to `discovery.html`, `renderer.py`, the markdown processor, or the YAML loader can silently change the rendered HTML byte-for-byte. There is no CI check that asserts a fixture `proposal.md` continues to render to a known-good HTML. Drift therefore lands on `main` without anyone noticing until a workshop.

3. **HTML is not deterministic across browsers/OSes for visual review.** Even with byte-identical HTML, `font-family: 'Segoe UI', system-ui, sans-serif` resolves to different fonts on Mac vs. Windows; emoji rendering differs; viewport breakpoints reflow at different widths; browser cache may serve a stale version. Workshops that compare rendered HTML across machines therefore have a reproducibility ceiling that the renderer cannot raise. PDFs (rendered via headless Chromium with embedded fonts) **do** normalize across machines and are the appropriate review surface for stakeholder-facing artifacts.

## Proposed Solution — three coordinated changes

### Change A — `aa-artifact-render --diagnose` command

A new top-level CLI subcommand that prints a structured one-screen diagnostic. Targets Jay's exact pain — one command to see whether your install is current.

```
$ aa-artifact-render --diagnose
aa-artifact-render diagnostic — 2026-04-17T23:14:02Z
─────────────────────────────────────────────────────
Package version (pyproject):       1.1.0
Package version (importlib):       1.1.0
Install location:                  /Users/aali/repos/.../tools/artifact-renderer
Source git SHA (HEAD):             a79ef39
Source git status:                 clean
Source branch:                     main
CLI executable:                    /usr/local/bin/aa-artifact-render
Python interpreter:                /usr/local/bin/python3.11 (3.11.7)
Templates dir:                     /Users/aali/repos/.../templates
Available templates (9):           _base, adr, discovery, evidence, generic, proposal, skill, spec, tasks
Library versions:
  click:                           8.1.7
  Jinja2:                          3.1.2
  markdown-it-py:                  3.0.0
  PyYAML:                          6.0.1
  playwright:                      not installed (PDF unavailable)
─────────────────────────────────────────────────────
Drift checks:
  ✓ pyproject version == importlib version
  ✓ install location is inside a git repo
  ⚠ source git status is dirty (uncommitted changes detected)
  ⚠ playwright not installed — PDF generation will fail
```

Exits non-zero (3) when any drift check fails. Plain-text output, parseable. Honors `--quiet` for CI use.

### Change B — Golden-fixture render-determinism test

Add a fixture markdown (`tests/fixtures/golden-discovery-stage-a.md`) and its expected rendered HTML (`tests/fixtures/golden-discovery-stage-a.html`). New test asserts: rendering the fixture today produces byte-identical output to the checked-in golden.

When the test legitimately fails (someone intentionally changed the template), the fix is to re-render the fixture and commit the new golden. The test exists to make accidental drift loud:

```python
def test_discovery_render_is_deterministic(tmp_path):
    """Render a fixture proposal.md and compare bytes against the checked-in golden HTML.

    If this fails, either:
      - You changed the template/renderer intentionally (re-render the fixture and commit)
      - You changed it accidentally (revert)
    """
    fixture = FIXTURES / "golden-discovery-stage-a.md"
    expected = (FIXTURES / "golden-discovery-stage-a.html").read_text(encoding="utf-8")
    actual = run_render(fixture)
    assert actual == expected, "Renderer output drifted from golden fixture. Re-render or revert."
```

Two complementary tests: golden bytes for `discovery` artifact, and golden bytes for `proposal` artifact (prevent drift in non-discovery templates too).

### Change C — Workflow doc: prefer PDF for workshop / stakeholder renders

Update the MCP-served `product-discovery` workflow content so the recommended Stage F handoff is the PDF, not HTML:

```markdown
> **Render evidence (ENG-13.1 + ENG-14.3):**
> aa-artifact-render <stage>.md --pdf --pdf-output reports/<stage>.pdf
> Use the PDF (not the HTML) for stakeholder review and cross-machine comparison.
> HTML is for live editing only; rendering is not byte-deterministic across browsers/OSes.
```

Plus a one-paragraph note in the renderer README explaining the cross-platform reproducibility contract.

## Laws Enforced

| Law | How this PR complies |
|---|---|
| **ENG-4.1** (Atomic TDD, NON-NEG) | RED tests before GREEN code for `--diagnose` and the golden-fixture comparison. |
| **ENG-4.2** (Coverage ≥ per-module gate) | New code paths covered ≥90% per module. |
| **ENG-4.3** (CI Quality Gates) | Golden-fixture test runs in CI; failure blocks merge. |
| **ENG-13.1** (Artifact Rendering, NON-NEG) | Strengthens: rendered output is now provably stable run-to-run; install drift is now detectable. |
| **PRD-2.5** (Stage-Gate, NON-NEG) | The render-gate decision can no longer be invalidated by silent template drift. |
| **BUS-7.1** (Audit Trail, NON-NEG) | `--diagnose` output is the toolchain's auditable provenance. PDF embeds the same metadata. |

## Scope

### In Scope
- `tools/artifact-renderer/src/aa_artifact_render/diagnose.py` — new module producing the diagnostic snapshot
- `tools/artifact-renderer/src/aa_artifact_render/cli.py` — wire `--diagnose` flag (mutually exclusive with normal render path)
- `tools/artifact-renderer/tests/test_diagnose.py` — RED → GREEN tests for diagnostic output
- `tools/artifact-renderer/tests/test_determinism.py` — golden-fixture test
- `tools/artifact-renderer/tests/fixtures/golden-discovery-stage-a.md`, `.html`
- `tools/artifact-renderer/tests/fixtures/golden-proposal.md`, `.html`
- `tools/artifact-renderer/README.md` — document `--diagnose`, golden-fixture workflow, PDF-preferred review
- Workflow content (MCP `product-discovery`) — prefer-PDF guidance — separate task
- `pyproject.toml` — bump version to 1.2.0

### Out of Scope
- A web service or daemon — `--diagnose` is single-shot CLI only
- Auto-fix for install drift — `--diagnose` reports; user re-runs `install.sh`
- Fixing all golden-fixture drift in existing artifacts (no regenerate-everything sweep)
- Changing PDF generation engine (still Playwright/Chromium)

## Test Plan

### RED phase tests (must fail before implementation)

`tests/test_diagnose.py`:
1. `test_diagnose_flag_exits_zero_when_clean` — running `--diagnose` on a clean install exits 0
2. `test_diagnose_reports_package_version` — output contains `Package version (pyproject):  1.x.x`
3. `test_diagnose_reports_install_location` — output contains an absolute path
4. `test_diagnose_reports_python_interpreter` — output contains the python3 path
5. `test_diagnose_reports_templates_dir_and_count` — lists 9 templates including discovery
6. `test_diagnose_reports_library_versions` — click, Jinja2, markdown-it-py, PyYAML present
7. `test_diagnose_dirty_git_emits_warning_and_exits_3` — when source has uncommitted changes
8. `test_diagnose_quiet_suppresses_output` — `--diagnose --quiet` exits with status code only

`tests/test_determinism.py`:
9. `test_discovery_render_byte_identical_to_golden` — render fixture, compare bytes
10. `test_proposal_render_byte_identical_to_golden` — same for the proposal template

### GREEN phase

Implement `diagnose.py` + wire `--diagnose` flag + create golden fixtures by running the current renderer and committing the output.

### REFACTOR

Extract any duplicated path / git introspection helpers into a `_repo_introspection.py` if it grows beyond ~50 lines.

## Open Questions

1. Should `--diagnose` exit non-zero on dirty git status, or just warn and exit 0? **Amaya's call:** non-zero (3) so CI can fail when reviewer re-renders from a dirty tree. Reviewers can override with `--allow-dirty`.
2. Should the golden HTML include the version stamp (which changes every bump) and timestamp? **Amaya's call:** Strip them from the comparison via a normalizer in the test (replace version + timestamp tokens with placeholders before byte compare). Keeps the golden stable across version bumps.
3. Should the golden fixture be regenerated by a `make golden` or `aa-artifact-render --regen-golden` command? **Amaya's call:** Add a separate `tools/artifact-renderer/regen-golden.sh` script. Keeps the CLI focused.

## Next Steps

1. RED tests committed
2. GREEN implementation
3. Coverage check (≥80% global, ≥90% per new module)
4. PR opened against main; @jay-turpin on review
5. Bump version 1.1.0 → 1.2.0 as part of this PR
6. After merge: announce in Teams with a one-liner Jay can run to verify drift detection working
