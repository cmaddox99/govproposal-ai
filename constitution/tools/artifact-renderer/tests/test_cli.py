"""CLI integration tests for aa-artifact-render (Phase 5 — RED)."""
import os
import textwrap
from pathlib import Path

import pytest
from click.testing import CliRunner

# Import will fail until cli.py is created — that's the RED phase.
from aa_artifact_render.cli import main

LAWS_DIR = Path(__file__).parent.parent.parent.parent / "laws"

SAMPLE_PROPOSAL = textwrap.dedent("""\
    ---
    type: proposal
    title: Test Proposal
    status: PROPOSED
    spec_id: TEST-001
    ---

    # Test Proposal

    This references ENG-13.1 as a law citation.
""")


@pytest.fixture()
def runner():
    return CliRunner()


@pytest.fixture()
def sample_md(tmp_path):
    f = tmp_path / "PROPOSAL.md"
    f.write_text(SAMPLE_PROPOSAL)
    return f


# ---------------------------------------------------------------------------
# 5.1a — --help shows all options
# ---------------------------------------------------------------------------
def test_help(runner):
    result = runner.invoke(main, ["--help"])
    assert result.exit_code == 0
    assert "--output" in result.output
    assert "--pdf" in result.output
    assert "--artifact-type" in result.output
    assert "--laws-dir" in result.output
    assert "--quiet" in result.output


# ---------------------------------------------------------------------------
# 5.1b — basic render writes HTML to default output path
# ---------------------------------------------------------------------------
def test_basic_render_default_output(runner, sample_md, tmp_path):
    result = runner.invoke(main, [str(sample_md), "--laws-dir", str(LAWS_DIR)])
    assert result.exit_code == 0, result.output
    default_out = sample_md.with_suffix(".html")
    assert default_out.exists()
    content = default_out.read_text()
    assert "<html" in content
    assert "Test Proposal" in content


# ---------------------------------------------------------------------------
# 5.1c — --output writes to specified path
# ---------------------------------------------------------------------------
def test_output_flag(runner, sample_md, tmp_path):
    out = tmp_path / "out.html"
    result = runner.invoke(
        main, [str(sample_md), "--output", str(out), "--laws-dir", str(LAWS_DIR)]
    )
    assert result.exit_code == 0, result.output
    assert out.exists()
    assert "<html" in out.read_text()


# ---------------------------------------------------------------------------
# 5.1d — unknown --artifact-type shows helpful error (not a traceback)
# ---------------------------------------------------------------------------
def test_unknown_artifact_type(runner, sample_md):
    result = runner.invoke(
        main,
        [str(sample_md), "--artifact-type", "banana", "--laws-dir", str(LAWS_DIR)],
    )
    # Should either succeed (falls back to generic) or show a graceful error —
    # it must NOT raise an unhandled exception (exit code 2 is fine for bad option).
    assert "Traceback" not in result.output
    assert "Error" in result.output or result.exit_code in (0, 2)


# ---------------------------------------------------------------------------
# 5.1e — missing input file shows helpful error
# ---------------------------------------------------------------------------
def test_missing_input_file(runner, tmp_path):
    ghost = tmp_path / "ghost.md"
    result = runner.invoke(main, [str(ghost), "--laws-dir", str(LAWS_DIR)])
    assert result.exit_code != 0
    assert "Traceback" not in result.output
    # Should mention the file path in the message
    assert "ghost.md" in result.output or "Error" in result.output


# ---------------------------------------------------------------------------
# 5.1f — --laws-dir path not found shows helpful error
# ---------------------------------------------------------------------------
def test_laws_dir_not_found(runner, sample_md, tmp_path):
    missing = tmp_path / "no_such_laws"
    result = runner.invoke(
        main, [str(sample_md), "--laws-dir", str(missing)]
    )
    assert result.exit_code != 0
    assert "Traceback" not in result.output


# ---------------------------------------------------------------------------
# 5.1g — success message includes citation counts
# ---------------------------------------------------------------------------
def test_success_message_citations(runner, sample_md, tmp_path):
    out = tmp_path / "out.html"
    result = runner.invoke(
        main, [str(sample_md), "--output", str(out), "--laws-dir", str(LAWS_DIR)]
    )
    assert result.exit_code == 0, result.output
    # Should include "Rendered" and mention citations
    assert "Rendered" in result.output or "rendered" in result.output
    assert "citation" in result.output.lower() or "ENG-" in result.output


# ---------------------------------------------------------------------------
# 5.1h — --quiet suppresses stdout on success
# ---------------------------------------------------------------------------
def test_quiet_flag(runner, sample_md, tmp_path):
    out = tmp_path / "out.html"
    result = runner.invoke(
        main,
        [str(sample_md), "--output", str(out), "--laws-dir", str(LAWS_DIR), "--quiet"],
    )
    assert result.exit_code == 0, result.output
    assert result.output.strip() == ""
    assert out.exists()


# ---------------------------------------------------------------------------
# 5.1j — discovery type accepted by CLI (renderer-enhanced-discovery-template)
# ---------------------------------------------------------------------------
def test_discovery_artifact_type_accepted(runner, tmp_path):
    """discovery must be in valid types and render without error."""
    md = tmp_path / "stage-b.md"
    md.write_text(
        "---\nartifact: discovery\ntitle: Test Discovery\nstage: B\n---\n\n## Body\n"
    )
    out = tmp_path / "stage-b.html"
    result = runner.invoke(
        main,
        [str(md), "--output", str(out), "--artifact-type", "discovery", "--laws-dir", str(LAWS_DIR)],
    )
    assert result.exit_code == 0, result.output
    assert out.exists()
    content = out.read_text(encoding="utf-8")
    assert "<!DOCTYPE html>" in content
    assert "APPROVE" in content  # render gate present


# ---------------------------------------------------------------------------
# 5.1i — --artifact-type override is used (bypasses frontmatter detection)
# ---------------------------------------------------------------------------
def test_artifact_type_override(runner, tmp_path):
    """A file without type frontmatter can be rendered with explicit --artifact-type."""
    md = tmp_path / "some.md"
    md.write_text("# Plain Markdown\n\nNo frontmatter at all.\n")
    out = tmp_path / "out.html"
    result = runner.invoke(
        main,
        [str(md), "--output", str(out), "--artifact-type", "generic", "--laws-dir", str(LAWS_DIR)],
    )
    assert result.exit_code == 0, result.output
    assert out.exists()


# ---------------------------------------------------------------------------
# renderer-auto-detect-discovery — auto-detect from workflow + stage frontmatter
# Laws: ENG-13.1, PRD-2.5, ENG-4.1
# ---------------------------------------------------------------------------
DISCOVERY_SIGNATURE = "ENG-13.1 Render Gate"


def _discovery_stage_md(workflow: str = "product-discovery", stage: str = "A") -> str:
    return textwrap.dedent(f"""\
        ---
        spec_id: disc-2026-099
        stage: {stage}
        stage_label: Initialize
        workflow: {workflow}
        title: Auto-detect Test
        mode: Exploratory
        tier: Tier 2
        ---

        # Auto-detect Test

        Body content.
    """)


def test_auto_detect_discovery_from_workflow_and_stage(runner, tmp_path):
    """File with workflow=product-discovery and stage=A renders with discovery template (no CLI flag)."""
    md = tmp_path / "stage-a-proposal.md"
    md.write_text(_discovery_stage_md(workflow="product-discovery", stage="A"))
    out = tmp_path / "stage-a.html"
    result = runner.invoke(main, [str(md), "--output", str(out), "--laws-dir", str(LAWS_DIR)])
    assert result.exit_code == 0, result.output
    assert DISCOVERY_SIGNATURE in out.read_text(encoding="utf-8")


def test_auto_detect_discovery_legacy_workflow_name(runner, tmp_path):
    """Legacy workflow name 'product-discovery-stage-a-f' also auto-detects to discovery."""
    md = tmp_path / "stage-b.md"
    md.write_text(_discovery_stage_md(workflow="product-discovery-stage-a-f", stage="B"))
    out = tmp_path / "stage-b.html"
    result = runner.invoke(main, [str(md), "--output", str(out), "--laws-dir", str(LAWS_DIR)])
    assert result.exit_code == 0, result.output
    assert DISCOVERY_SIGNATURE in out.read_text(encoding="utf-8")


def test_auto_detect_stage_case_insensitive(runner, tmp_path):
    """stage: 'c' (lowercase) is accepted same as 'C'."""
    md = tmp_path / "stage-c.md"
    md.write_text(_discovery_stage_md(workflow="product-discovery", stage="c"))
    out = tmp_path / "stage-c.html"
    result = runner.invoke(main, [str(md), "--output", str(out), "--laws-dir", str(LAWS_DIR)])
    assert result.exit_code == 0, result.output
    assert DISCOVERY_SIGNATURE in out.read_text(encoding="utf-8")


def test_auto_detect_falls_back_to_generic_without_workflow(runner, tmp_path):
    """A file with stage but no product-discovery workflow does NOT auto-detect discovery."""
    md = tmp_path / "random.md"
    md.write_text(textwrap.dedent("""\
        ---
        title: Random
        stage: A
        workflow: some-other-workflow
        ---

        Body.
    """))
    out = tmp_path / "random.html"
    result = runner.invoke(main, [str(md), "--output", str(out), "--laws-dir", str(LAWS_DIR)])
    assert result.exit_code == 0, result.output
    # Should use generic template, not discovery — no render-gate signature
    assert DISCOVERY_SIGNATURE not in out.read_text(encoding="utf-8")


def test_explicit_frontmatter_type_overrides_auto_detect(runner, tmp_path):
    """Explicit 'type: proposal' in frontmatter beats workflow+stage auto-detect."""
    md = tmp_path / "PROPOSAL.md"
    md.write_text(textwrap.dedent("""\
        ---
        type: proposal
        title: Explicit proposal
        workflow: product-discovery
        stage: A
        ---

        Body.
    """))
    out = tmp_path / "proposal.html"
    result = runner.invoke(main, [str(md), "--output", str(out), "--laws-dir", str(LAWS_DIR)])
    assert result.exit_code == 0, result.output
    # Used proposal template, not discovery
    assert DISCOVERY_SIGNATURE not in out.read_text(encoding="utf-8")


def test_cli_flag_overrides_frontmatter_type(runner, tmp_path):
    """--artifact-type discovery on CLI overrides explicit 'type: proposal' frontmatter."""
    md = tmp_path / "PROPOSAL.md"
    md.write_text(textwrap.dedent("""\
        ---
        type: proposal
        title: Forced discovery
        stage: A
        workflow: product-discovery
        ---

        Body.
    """))
    out = tmp_path / "forced.html"
    result = runner.invoke(
        main,
        [str(md), "--output", str(out), "--artifact-type", "discovery", "--laws-dir", str(LAWS_DIR)],
    )
    assert result.exit_code == 0, result.output
    assert DISCOVERY_SIGNATURE in out.read_text(encoding="utf-8")


# ---------------------------------------------------------------------------
# renderer-auto-detect-discovery — version stamp in CLI output
# Laws: BUS-7.1, ENG-13.1
# ---------------------------------------------------------------------------
def test_version_stamp_in_success_output(runner, sample_md, tmp_path):
    """Success line includes 'aa-artifact-render v<version>' token."""
    result = runner.invoke(main, [str(sample_md), "--laws-dir", str(LAWS_DIR)])
    assert result.exit_code == 0, result.output
    assert "aa-artifact-render v" in result.output


def test_quiet_flag_suppresses_version_stamp(runner, sample_md, tmp_path):
    """--quiet suppresses stdout on success, including version stamp."""
    result = runner.invoke(main, [str(sample_md), "--laws-dir", str(LAWS_DIR), "--quiet"])
    assert result.exit_code == 0
    assert result.output.strip() == ""
