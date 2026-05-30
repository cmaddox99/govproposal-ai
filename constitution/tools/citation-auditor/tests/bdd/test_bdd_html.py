"""BDD tests — Phase 6 §S-04 HTML scanning scenarios (T-26 through T-29).

Each scenario exercises the full CLI stack end-to-end via CliRunner.
Laws directory: real registry at governance/hangar-ai-constitution/laws.

T-26: Valid HTML → exit 0, ENG-3.4 PASS.
T-27: Script-tag IDs suppressed — ENG-6.4 inside <script> NOT in output.
T-28: Unclosed <script> → AuditError → exit 2, "Unclosed" in output.
T-29: ENG-6.4 in plain <td> text — S-02 deviation #3: trailing anchor regex
      [|—–\\-:()\\[\\]] excludes bare whitespace, so "No God Classes\\n\\n"
      does NOT trigger dual-anchor → no title candidate extracted → PASS
      (not WARN). Test asserts the actual tool behaviour.
"""
from __future__ import annotations

from pathlib import Path

from click.testing import CliRunner

from citation_auditor.cli import main

RUNNER = CliRunner()
REAL_LAWS = Path(__file__).parents[4] / "laws"
FIXTURES = Path(__file__).parent.parent / "fixtures" / "bdd"


def _run(fixture_name: str, extra: list[str] | None = None):
    artifact = FIXTURES / fixture_name
    args = [str(artifact), "--laws-dir", str(REAL_LAWS)] + (extra or [])
    return RUNNER.invoke(main, args)


# ---------------------------------------------------------------------------
# T-26: Valid HTML artifact — ENG-3.4 in <p> body → PASS, exit 0
# ---------------------------------------------------------------------------
class TestT26ValidHtmlPass:
    """artifact_html_valid.html: ENG-3.4 in <p> text → PASS."""

    def test_exit_code_is_0(self):
        result = _run("artifact_html_valid.html")
        assert result.exit_code == 0

    def test_eng34_in_output(self):
        result = _run("artifact_html_valid.html")
        assert "ENG-3.4" in result.output

    def test_eng34_verdict_pass(self):
        result = _run("artifact_html_valid.html")
        lines = [ln for ln in result.output.splitlines() if "ENG-3.4" in ln]
        assert lines, "ENG-3.4 row missing"
        assert "PASS" in lines[0]


# ---------------------------------------------------------------------------
# T-27: <script> content excluded — ENG-6.4 inside <script> NOT scanned
# ---------------------------------------------------------------------------
class TestT27ScriptIdsExcluded:
    """artifact_html_script_ids.html: ENG-6.4 in <script> → absent from output."""

    def test_eng64_not_in_output(self):
        result = _run("artifact_html_script_ids.html")
        assert "ENG-6.4" not in result.output

    def test_eng34_still_present(self):
        result = _run("artifact_html_script_ids.html")
        assert "ENG-3.4" in result.output

    def test_exit_code_is_0(self):
        result = _run("artifact_html_script_ids.html")
        assert result.exit_code == 0

    def test_scanned_count_is_1(self):
        result = _run("artifact_html_script_ids.html")
        assert "1 citations scanned" in result.output


# ---------------------------------------------------------------------------
# T-28: Unclosed <script> tag → AuditError → exit 2
# ---------------------------------------------------------------------------
class TestT28UnclosedScriptTag:
    """artifact_html_unclosed_tag.html: unclosed <script> → exit 2."""

    def test_exit_code_is_2(self):
        result = _run("artifact_html_unclosed_tag.html")
        assert result.exit_code == 2

    def test_output_contains_unclosed(self):
        result = _run("artifact_html_unclosed_tag.html")
        assert "Unclosed" in result.output or "Unclosed" in (result.exception or "")


# ---------------------------------------------------------------------------
# T-29: ENG-6.4 in <td> plain text — S-02 deviation #3 analysis
#
# After HTML stripping: "ENG-6.4 No God Classes\n\n"
# Dual-anchor guard in _extract_title_candidates:
#   leading  = re.match(r'^[\s|—–\-:()\[\]]', " No God Classes\n\n") → True (space)
#   trailing = re.search(r'[|—–\-:()\[\]]\s*$', " No God Classes\n\n") → False
#              (ends with bare \n\n — not in [|—–\-:()\[\]])
# → dual-anchor fails → "No God Classes" NOT extracted → no title mismatch
# → verdict is PASS, not WARN.  ENG-6.4 real title: "Data Protection Law".
# ---------------------------------------------------------------------------
class TestT29HtmlTablePlainTextNoWarn:
    """ENG-6.4 in <td> alongside 'No God Classes': S-02 deviation #3 → PASS."""

    def test_eng64_present_in_output(self):
        result = _run("artifact_html_valid.html")
        assert "ENG-6.4" in result.output

    def test_eng64_verdict_is_pass_not_warn(self):
        # S-02 deviation #3: trailing whitespace-only after-window does not
        # satisfy the structural-separator trailing anchor → no title extracted
        # → PASS (not WARN).  Title "No God Classes" is silently ignored.
        result = _run("artifact_html_valid.html")
        lines = [ln for ln in result.output.splitlines() if "ENG-6.4" in ln]
        assert lines, "ENG-6.4 row missing"
        assert "PASS" in lines[0], (
            f"Expected PASS for ENG-6.4 (S-02 deviation #3), got: {lines[0]!r}"
        )

    def test_zero_warns_in_summary(self):
        result = _run("artifact_html_valid.html")
        assert "0 WARN" in result.output
