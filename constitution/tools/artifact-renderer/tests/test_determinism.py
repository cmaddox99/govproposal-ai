"""Render-determinism tests — golden fixture comparison.

Spec: hangar-ai-specs/changes/renderer-determinism-and-diagnose/PROPOSAL.md
Laws: ENG-4.1 (Atomic TDD, NON-NEG), ENG-4.3 (CI Quality Gates), ENG-13.1.

Purpose: catch accidental drift in the templates, renderer, or markdown
processor that would silently change the rendered HTML byte-for-byte.

When a test here fails, either:
  1. You changed the template/renderer intentionally — re-run
     `tools/artifact-renderer/regen-golden.sh` and commit the new
     `golden-*.html` files alongside your other changes.
  2. You changed it accidentally — revert.

The comparison is normalized for fields that legitimately vary across
runs (version stamp, timestamps, install paths) — those are NOT what we
are pinning. We pin the structural HTML.
"""
import re
from pathlib import Path

import pytest
from click.testing import CliRunner

from aa_artifact_render.cli import main

FIXTURES = Path(__file__).parent / "fixtures"
LAWS_DIR = Path(__file__).parent.parent.parent.parent / "laws"


def _normalize(html: str) -> str:
    """Strip fields that legitimately vary across runs.

    - aa-artifact-render version (footer)
    - timestamps
    - absolute install paths in any embedded comment
    """
    html = re.sub(r"aa-artifact-render v[\d.]+", "aa-artifact-render vX.Y.Z", html)
    html = re.sub(
        r"\b\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:Z|[+-]\d{2}:?\d{2})?\b",
        "ISO-8601-TIMESTAMP",
        html,
    )
    html = re.sub(r"/[A-Za-z0-9_./-]*hangar-ai-constitution[A-Za-z0-9_./-]*", "/REPO", html)
    return html


@pytest.fixture()
def runner():
    return CliRunner()


def _render(runner, fixture_md: Path, tmp_path: Path) -> str:
    out = tmp_path / (fixture_md.stem + ".html")
    result = runner.invoke(
        main,
        [str(fixture_md), "--output", str(out), "--laws-dir", str(LAWS_DIR)],
    )
    assert result.exit_code == 0, result.output
    return out.read_text(encoding="utf-8")


def test_discovery_render_byte_identical_to_golden(runner, tmp_path):
    """Rendering the discovery fixture produces output byte-identical to the golden HTML."""
    fixture = FIXTURES / "golden-discovery-stage-a.md"
    golden = FIXTURES / "golden-discovery-stage-a.html"
    assert fixture.exists(), "fixture missing"
    assert golden.exists(), (
        "Golden HTML missing. First-run setup: render the fixture and commit "
        "the result to tests/fixtures/golden-discovery-stage-a.html."
    )

    actual = _normalize(_render(runner, fixture, tmp_path))
    expected = _normalize(golden.read_text(encoding="utf-8"))

    assert actual == expected, (
        "Discovery template render drifted from golden fixture.\n"
        "Either re-run tools/artifact-renderer/regen-golden.sh and commit, "
        "or revert the change.\n"
    )


def test_proposal_render_byte_identical_to_golden(runner, tmp_path):
    """Rendering the proposal fixture produces output byte-identical to the golden HTML."""
    fixture = FIXTURES / "golden-proposal.md"
    golden = FIXTURES / "golden-proposal.html"
    assert fixture.exists(), "fixture missing"
    assert golden.exists(), (
        "Golden HTML missing. First-run setup: render the fixture and commit "
        "the result to tests/fixtures/golden-proposal.html."
    )

    actual = _normalize(_render(runner, fixture, tmp_path))
    expected = _normalize(golden.read_text(encoding="utf-8"))

    assert actual == expected, (
        "Proposal template render drifted from golden fixture.\n"
        "Either re-run tools/artifact-renderer/regen-golden.sh and commit, "
        "or revert the change.\n"
    )


def test_discovery_stage_d_render_byte_identical_to_golden(runner, tmp_path):
    """Stage D fixture with assumption_citations renders byte-identical to golden."""
    fixture = FIXTURES / "golden-discovery-stage-d.md"
    golden = FIXTURES / "golden-discovery-stage-d.html"
    assert fixture.exists(), "fixture missing"
    assert golden.exists(), "Golden HTML missing. Run tools/artifact-renderer/regen-golden.sh"
    actual = _normalize(_render(runner, fixture, tmp_path))
    expected = _normalize(golden.read_text(encoding="utf-8"))
    assert actual == expected, (
        "Stage D template render drifted from golden fixture.\n"
        "Re-run tools/artifact-renderer/regen-golden.sh and commit, or revert.\n"
    )


def test_discovery_stage_e_render_byte_identical_to_golden(runner, tmp_path):
    """Stage E fixture with baseline_sources renders byte-identical to golden."""
    fixture = FIXTURES / "golden-discovery-stage-e.md"
    golden = FIXTURES / "golden-discovery-stage-e.html"
    assert fixture.exists(), "fixture missing"
    assert golden.exists(), "Golden HTML missing. Run tools/artifact-renderer/regen-golden.sh"
    actual = _normalize(_render(runner, fixture, tmp_path))
    expected = _normalize(golden.read_text(encoding="utf-8"))
    assert actual == expected, (
        "Stage E template render drifted from golden fixture.\n"
        "Re-run tools/artifact-renderer/regen-golden.sh and commit, or revert.\n"
    )


def test_discovery_stage_f_render_byte_identical_to_golden(runner, tmp_path):
    """Stage F fixture with roadmap_rationale renders byte-identical to golden."""
    fixture = FIXTURES / "golden-discovery-stage-f.md"
    golden = FIXTURES / "golden-discovery-stage-f.html"
    assert fixture.exists(), "fixture missing"
    assert golden.exists(), "Golden HTML missing. Run tools/artifact-renderer/regen-golden.sh"
    actual = _normalize(_render(runner, fixture, tmp_path))
    expected = _normalize(golden.read_text(encoding="utf-8"))
    assert actual == expected, (
        "Stage F template render drifted from golden fixture.\n"
        "Re-run tools/artifact-renderer/regen-golden.sh and commit, or revert.\n"
    )
