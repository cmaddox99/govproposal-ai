# aa-artifact-render

Renders Hangar AI Constitution governance artifacts (proposals, ADRs, evidence, tasks, specs, skills) from Markdown into self-contained, print-ready HTML with interactive law citation tooltips. Optionally generates PDFs via headless Chromium.

Implements **ENG-13.1** (Artifact Rendering Standard).

## Quick Start

```bash
# Install (preferred — helper that installs editable + verifies)
./tools/artifact-renderer/install.sh

# Install (manual)
pip install -e tools/artifact-renderer

# For PDF support — install Playwright + headless Chromium
pip install playwright
playwright install chromium

# Render a proposal as HTML (law citations become interactive tooltips)
aa-artifact-render PROPOSAL.md

# Render with PDF
aa-artifact-render PROPOSAL.md --pdf

# Render to custom output path
aa-artifact-render PROPOSAL.md --output dist/PROPOSAL.html

# PDF only (no HTML file kept)
aa-artifact-render PROPOSAL.md --pdf-only --pdf-output dist/PROPOSAL.pdf

# Quiet mode for CI pipelines
aa-artifact-render PROPOSAL.md --quiet
```

## Options Reference

| Option | Description |
|--------|-------------|
| `ARTIFACT` | Path to the markdown governance artifact (.md file) |
| `--output`, `-o TEXT` | Output HTML path (default: `<artifact>.html`) |
| `--pdf` | Also generate a PDF alongside the HTML |
| `--pdf-only` | Generate PDF only — no HTML output file kept |
| `--pdf-output TEXT` | Output PDF path (default: `<artifact>.pdf`) |
| `--artifact-type TEXT` | Override type detection (`proposal\|tasks\|adr\|evidence\|spec\|skill\|generic\|discovery`). Auto-detects `discovery` when frontmatter has `workflow: product-discovery*` + `stage: A\|B\|C\|D\|E\|F`. |
| `--laws-dir TEXT` | Path to constitution `laws/` directory (auto-detected if omitted) |
| `--quiet`, `-q` | Suppress stdout on success (CI-friendly — errors still appear on stderr) |

## Usage Examples

### 1. Render a PROPOSAL.md

```bash
aa-artifact-render hangar-ai-specs/changes/my-feature/PROPOSAL.md --laws-dir laws
# → hangar-ai-specs/changes/my-feature/PROPOSAL.html
# ✓ Rendered: ... [7 citations resolved, 0 unresolved]
```

### 2. Render tasks.md

```bash
aa-artifact-render hangar-ai-specs/changes/my-feature/tasks.md
# → hangar-ai-specs/changes/my-feature/tasks.html
```

### 3. Render an ADR

```bash
aa-artifact-render hangar-ai-specs/changes/my-feature/adr.md --artifact-type adr
```

### 4. Render evidence

```bash
aa-artifact-render hangar-ai-specs/evidence/adoption-check.md --artifact-type evidence
```

### 5. Render and generate PDF

```bash
aa-artifact-render PROPOSAL.md --pdf --pdf-output reports/PROPOSAL.pdf
# ✓ PDF: reports/PROPOSAL.pdf
# ✓ Rendered: PROPOSAL.html [7 citations resolved, 0 unresolved]
```

## Artifact Frontmatter

All artifacts should include a YAML frontmatter block. The `type` field controls which template is used:

```yaml
---
type: proposal          # proposal | tasks | adr | evidence | spec | skill | generic
title: My Proposal
status: PROPOSED        # PROPOSED | IMPLEMENTED | ARCHIVED (for proposals)
spec_id: ENG-42
laws: [ENG-13.1, ENG-4.1]
---
```

See `agent-skills/skills-by-domain/development-practices/skill-artifact-html-rendering.md` for the full frontmatter contract per artifact type.

## Integration with the SDD Lifecycle

The `aa-artifact-render` tool is invoked at the evidence-producing phases of each workflow:

- **Adoption workflow** — after `hangar-ai-specs/evidence/adoption-check.md` and `adoption-verified.md` are committed
- **Greenfield workflow** — after the PROPOSAL.md and SonarQube gate evidence are committed
- **Legacy Rescue (all tracks)** — after ADR, characterization report, and certify evidence
- **Product Discovery** — after Stage C evidence and Stage F implementation proposal

## Diagnostics — `aa-artifact-render --diagnose`

When two team members get different rendered HTML from the same source, the cause is usually install drift (CLI bound to a stale checkout, multiple Python envs, non-editable install lurking). Run:

```bash
aa-artifact-render --diagnose
```

This prints:
- Installed package version + install location
- Source git SHA, branch, dirty/clean status
- Python interpreter path + version
- Templates directory + which templates are available
- Versions of key libraries (Jinja2, markdown-it-py, PyYAML, click, playwright)
- Drift checks (exits non-zero with status 3 when drift detected)

Compare two team members' diagnose output side-by-side — divergence in `Install location`, `Source git SHA`, or `Python interpreter` explains the rendering difference. Pair with `regen-golden.sh` and the `tests/test_determinism.py` golden-fixture check to catch drift in CI before it reaches a workshop.

## Cross-platform reproducibility — prefer PDF for stakeholder review

Rendered HTML is **not byte-deterministic across browsers and operating systems** — `font-family: 'Segoe UI', system-ui, sans-serif` falls back to SF Pro on Mac and to actual Segoe UI on Windows; emoji rendering differs; viewport breakpoints reflow at different widths; browser cache may serve a stale version.

For workshop and stakeholder reviews, render to **PDF** (Playwright/Chromium embeds fonts and normalizes layout):

```bash
aa-artifact-render PROPOSAL.md --pdf --pdf-output reports/PROPOSAL.pdf
```

HTML is for live editing. PDF is for review.

## Troubleshooting

| Problem | Solution |
|---------|----------|
| Different output on two machines, same source | Run `aa-artifact-render --diagnose` on both — compare versions, install location, git SHA |
| `Chromium is not installed` | Run `playwright install chromium` |
| `[3 unresolved]` in output | Run with `--laws-dir path/to/laws` pointing to the constitution `laws/` directory |
| Missing frontmatter / wrong template | Add `type:` field to frontmatter or use `--artifact-type` flag |
| Output directory does not exist | Create the parent directory before running |
| PDF looks unstyled | Ensure the HTML was rendered first with the same tool (not hand-crafted) |
| Determinism test fails on PR | Either re-run `tools/artifact-renderer/regen-golden.sh` and commit, or revert the change |
