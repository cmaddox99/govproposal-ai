---
spec_id: renderer-auto-detect-discovery
title: "Auto-detect discovery artifact type + version stamp + install helper"
status: PROPOSED
triggered_by: "Workshop session — 2026-04-17 · Adeel Ali · AAdvantage partner-miles Stage A/C demo"
author: Amaya (Technical Coach) / Willem (Constitutional Architect)
scope: "tools/artifact-renderer (cli.py, renderer, tests) + tools/templates/product-discovery (all 6 stage templates) + docs/README"
laws_applied:
  - ENG-4.1
  - ENG-4.2
  - ENG-13.1
  - ENG-11.1
  - ENG-11.2
  - PRD-2.5
  - BUS-7.1
relates_to:
  - discovery-template-rich-cards
  - render-gate-source-of-truth-capture
---

## Problem

Two defects surfaced during the 2026-04-17 workshop demo on AAdvantage partner-miles discovery:

1. **`discovery` artifact type is never auto-detected.** `cli.py:108` resolves artifact_type only from `frontmatter.type` or `frontmatter.artifact`, falling back to `"generic"`. None of the canonical Stage A–F markdown templates in `tools/templates/product-discovery/` declare `type: discovery`. Every render of a stage artifact therefore needs `--artifact-type discovery` on the CLI, or the tool silently falls back to the generic skeleton template — producing a visually regressed artifact that looks nothing like the hand-crafted Stage A–F artifacts teams already ship.

2. **No version visibility.** Multiple team members run `pip install -e tools/artifact-renderer` at different times against different revisions of the constitution. A stale install produces outdated artifacts with no signal to the user. Nothing in the CLI output tells the reviewer which version of the renderer produced the HTML.

## Proposed Solution

### 1. Auto-detect `discovery` type from frontmatter

Extract type resolution in `cli.py` into a pure helper:

```python
def _resolve_artifact_type(fm: dict, cli_override: str | None) -> str:
    if cli_override:
        return cli_override
    explicit = fm.get("type") or fm.get("artifact")
    if explicit:
        return explicit
    # Auto-detect discovery: product-discovery workflow + stage A-F
    workflow = str(fm.get("workflow", "")).lower()
    stage = str(fm.get("stage", "")).strip().upper()
    if "product-discovery" in workflow and stage in {"A", "B", "C", "D", "E", "F"}:
        return "discovery"
    return "generic"
```

Precedence (highest first): `--artifact-type` CLI flag → explicit `type:` frontmatter → `artifact:` frontmatter → auto-detect (workflow+stage) → `generic` fallback.

### 2. Add `type: discovery` to canonical stage templates

Update all 6 markdown templates in `tools/templates/product-discovery/`:
- `stage-a-proposal.md`
- `stage-b-field-study.md`
- `stage-c-code-evidence.md`
- `stage-d-validation.md`
- `stage-e-metrics.md`
- `stage-f-roadmap.md`

Add `type: discovery` to each frontmatter as a belt-and-suspenders default alongside the auto-detect logic. Teams copying these templates inherit the right type automatically.

### 3. Version stamp in CLI success output

Emit the installed package version alongside the success message:

```
✓ Rendered: path/to/artifact.html [N citations resolved, M unresolved]
  aa-artifact-render v1.0.0 · /path/to/installed/package
```

Read version from `importlib.metadata.version("aa-artifact-render")`. Stays terse in `--quiet` mode.

### 4. Install helper script

Add `tools/artifact-renderer/install.sh` (executable) that runs `pip install -e tools/artifact-renderer` from repo root. Update README with a "before rendering, ensure latest install" note. Not enforced programmatically — documented ergonomics.

### 5. Workflow documentation

Update the MCP-served `product-discovery` workflow content to reference the install helper explicitly.

## Laws Enforced

| Law | How this PR complies |
|---|---|
| **ENG-4.1** (Atomic TDD, NON-NEG) | Tests RED before code GREEN. `_resolve_artifact_type()` + CLI version output both test-driven. |
| **ENG-4.2** (Coverage ≥90%) | New helper gets ≥90% branch coverage; CLI wiring covered by integration tests. |
| **ENG-13.1** (Artifact Rendering, NON-NEG) | The fix directly addresses a rendering-standard violation: discovery artifacts currently render with the wrong template unless flagged. |
| **PRD-2.5** (Stage-Gate, NON-NEG) | Visual parity is part of the gate criterion — stages must be reviewable in browser with the canonical design system. |
| **BUS-7.1** (Audit Trail, NON-NEG) | Version stamp in rendered output is an auditable record of which toolchain produced the artifact. |
| **ENG-11.1 / ENG-11.2** (SDD + Proposal Completeness) | This proposal exists; tasks.md to follow. |

## Scope

### In Scope
- `tools/artifact-renderer/src/aa_artifact_render/cli.py` — refactor type resolution into pure helper
- `tools/artifact-renderer/tests/test_cli.py` — new test cases for auto-detect precedence
- `tools/templates/product-discovery/stage-*-*.md` — add `type: discovery` to all 6 files
- `tools/artifact-renderer/install.sh` (new, executable)
- `tools/artifact-renderer/README.md` — note the install helper
- Workflow content update (MCP `product-discovery`) — separate task

### Out of Scope
- Bumping the `aa-artifact-render` semver (should be handled by a release PR once tests pass)
- Applying the rich-card design to non-discovery templates (separate proposal: `discovery-template-rich-cards-all-types`)
- Linter rule enforcing `type:` field presence (separate proposal if desired)

## Test Plan

### RED — write failing tests first (ENG-4.1)
1. `test_auto_detect_discovery_from_workflow_and_stage` — file with `workflow: product-discovery` + `stage: A` and no `type:` renders with discovery template
2. `test_auto_detect_falls_back_to_generic` — file with no workflow hint renders with generic template
3. `test_explicit_frontmatter_type_overrides_auto_detect` — `type: proposal` beats workflow=discovery auto-detect
4. `test_cli_flag_overrides_frontmatter_type` — `--artifact-type discovery` beats `type: proposal` in frontmatter
5. `test_stage_case_insensitive` — `stage: a` works same as `stage: A`
6. `test_version_in_success_output` — CLI success line contains `v<version>` token
7. `test_quiet_flag_suppresses_version_line` — `--quiet` still silent on success

### GREEN — implement `_resolve_artifact_type` helper + version stamp

### REFACTOR — extract any duplicated logic

## Open Questions

1. Should `workflow: product-discovery-stage-a-f` (legacy form used in `avatars/product-type/loyalty-aadvantage/manifest.yaml`) also auto-detect? **Willem's answer:** Yes — the substring match on `"product-discovery"` handles both forms. Confirmed.
2. Should the version stamp land in the rendered HTML footer as well, so a saved artifact carries its provenance? **Willem's recommendation:** Yes, as follow-up. Scope defer to keep this PR focused.

## Next Steps

1. Land tests (RED)
2. Implement helper + templates + install.sh (GREEN)
3. Run full `aa-constitution-lint` + `pytest` suites
4. Update PR #36 or file a new PR on the same branch
5. Request review from Jay (renderer owner)
