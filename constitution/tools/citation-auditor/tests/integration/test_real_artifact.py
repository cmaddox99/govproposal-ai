"""Integration tests — real artifact scan using the actual Hangar AI Constitution registry.

Scans a copy of phase-1-capture.md (the citation-auditor Phase 1 artifact) against the
REAL laws/index.yaml in the repository. This is a black-box end-to-end test that exercises
the full 4-layer DI stack on production-grade input.

Phase 3 §4.1 success criteria:
- Known-clean artifact (phase-1-capture.md) → exit 0 with --allow-draft ENG-14.1,ENG-14.2
- Tool runs in < 2 seconds for 500-line artifact (Phase 4 §0 performance criterion)
"""
from __future__ import annotations

import time
from pathlib import Path

from click.testing import CliRunner

from citation_auditor.cli import main

RUNNER = CliRunner()

# Real registry from repo root (not the fixture registry)
REPO_ROOT = Path(__file__).parent.parent.parent.parent.parent  # tools/ → repo root
REAL_LAWS_DIR = REPO_ROOT / "laws"
SAMPLE_ARTIFACT = (
    Path(__file__).parent.parent / "fixtures" / "constitution_sample" / "phase-1-capture.md"
)


def _registry_available() -> bool:
    return (REAL_LAWS_DIR / "index.yaml").exists()


class TestRealArtifactScan:
    def test_phase1_capture_scans_without_tool_error(self):
        """Phase-1-capture.md must not cause exit 2 (tool error)."""
        if not _registry_available():
            import pytest
            pytest.skip("Real registry not available")
        result = RUNNER.invoke(main, [
            str(SAMPLE_ARTIFACT),
            "--laws-dir", str(REAL_LAWS_DIR),
            "--allow-draft", "ENG-14.1,ENG-14.2",
        ])
        # Must not be a tool error
        assert result.exit_code != 2, f"Tool error: {result.output}"

    def test_phase1_capture_exit_0_all_known(self):
        """phase-1-capture.md cites only real laws → should exit 0."""
        if not _registry_available():
            import pytest
            pytest.skip("Real registry not available")
        result = RUNNER.invoke(main, [
            str(SAMPLE_ARTIFACT),
            "--laws-dir", str(REAL_LAWS_DIR),
            "--allow-draft", "ENG-14.1,ENG-14.2",
        ])
        assert result.exit_code == 0, (
            f"Expected 0 for clean artifact, got {result.exit_code}.\n{result.output}"
        )

    def test_phase1_capture_scan_under_2_seconds(self):
        """Performance criterion: < 2 seconds for a 500-line artifact (Phase 4 §0)."""
        if not _registry_available():
            import pytest
            pytest.skip("Real registry not available")
        start = time.monotonic()
        RUNNER.invoke(main, [
            str(SAMPLE_ARTIFACT),
            "--laws-dir", str(REAL_LAWS_DIR),
            "--allow-draft", "ENG-14.1,ENG-14.2",
        ])
        elapsed = time.monotonic() - start
        assert elapsed < 2.0, f"Scan took {elapsed:.2f}s — exceeds 2s threshold"

    def test_summary_line_present_in_output(self):
        """Tool must always emit a 'citations scanned' summary line."""
        if not _registry_available():
            import pytest
            pytest.skip("Real registry not available")
        result = RUNNER.invoke(main, [
            str(SAMPLE_ARTIFACT),
            "--laws-dir", str(REAL_LAWS_DIR),
            "--allow-draft", "ENG-14.1,ENG-14.2",
        ])
        assert "citations scanned" in result.output

    def test_no_fail_verdict_for_known_clean_artifact(self):
        """phase-1-capture.md is APPROVED — must have zero FAILs."""
        if not _registry_available():
            import pytest
            pytest.skip("Real registry not available")
        result = RUNNER.invoke(main, [
            str(SAMPLE_ARTIFACT),
            "--laws-dir", str(REAL_LAWS_DIR),
            "--allow-draft", "ENG-14.1,ENG-14.2",
        ])
        fail_rows = [ln for ln in result.output.splitlines() if "FAIL" in ln
                     and not ln.startswith("Summary")]
        assert len(fail_rows) == 0, "Unexpected FAILs:\n" + "\n".join(fail_rows)
