"""Tests for `aa-artifact-render --diagnose` CLI command.

Spec: hangar-ai-specs/changes/renderer-determinism-and-diagnose/PROPOSAL.md
Laws: ENG-4.1 (Atomic TDD, NON-NEG), ENG-13.1 (Artifact Rendering, NON-NEG)
"""
from pathlib import Path

import pytest
from click.testing import CliRunner

from aa_artifact_render.cli import main


@pytest.fixture()
def runner():
    return CliRunner()


# ---------------------------------------------------------------------------
# Diagnose command — RED tests
# ---------------------------------------------------------------------------
def test_diagnose_flag_exits_zero_when_clean(runner):
    """--diagnose on a clean install exits 0 (success) or 3 (drift detected) — never crashes."""
    result = runner.invoke(main, ["--diagnose"])
    assert result.exit_code in (0, 3), result.output
    assert "Traceback" not in result.output


def test_diagnose_reports_package_version(runner):
    """Output identifies the installed package version."""
    result = runner.invoke(main, ["--diagnose"])
    assert "Package version" in result.output
    # Version like "1.1.0" or "unknown"
    assert "version" in result.output.lower()


def test_diagnose_reports_install_location(runner):
    """Output identifies where aa-artifact-render is installed (absolute path)."""
    result = runner.invoke(main, ["--diagnose"])
    assert "Install location" in result.output or "Source" in result.output


def test_diagnose_reports_python_interpreter(runner):
    """Output identifies the Python interpreter and version."""
    result = runner.invoke(main, ["--diagnose"])
    assert "Python" in result.output


def test_diagnose_reports_templates(runner):
    """Output lists available templates including the discovery template."""
    result = runner.invoke(main, ["--diagnose"])
    assert "Templates" in result.output or "templates" in result.output
    assert "discovery" in result.output


def test_diagnose_reports_library_versions(runner):
    """Output identifies key library versions."""
    result = runner.invoke(main, ["--diagnose"])
    # At least Jinja2 and markdown-it-py should be named
    assert "Jinja2" in result.output or "jinja" in result.output.lower()
    assert "markdown-it" in result.output or "markdown_it" in result.output


def test_diagnose_includes_drift_check_summary(runner):
    """Output includes a 'Drift checks' or similar status block."""
    result = runner.invoke(main, ["--diagnose"])
    # Either the literal phrase, or a check-mark / cross-mark indicator
    assert any(token in result.output for token in ["Drift checks", "drift", "✓", "⚠", "✗"])


def test_diagnose_quiet_suppresses_output(runner):
    """--diagnose --quiet exits with status code only, no stdout."""
    result = runner.invoke(main, ["--diagnose", "--quiet"])
    assert result.exit_code in (0, 3)
    assert result.output.strip() == ""
