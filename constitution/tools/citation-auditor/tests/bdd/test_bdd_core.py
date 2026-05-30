"""BDD tests — Phase 3 §4.1 Core scenarios (Sc-1 through Sc-9).

Each scenario maps directly to a gherkin entry in phase-3-define.md §4.1.
Tests run the full CLI stack end-to-end via CliRunner (black-box).
"""
from __future__ import annotations

from pathlib import Path

from click.testing import CliRunner

from citation_auditor.cli import main

RUNNER = CliRunner()
BDD_REGISTRY = Path(__file__).parent.parent / "fixtures" / "bdd" / "registry"


def _artifact(tmp_path: Path, body: str, fm: str | None = None) -> Path:
    """Write a .md artifact with optional frontmatter."""
    p = tmp_path / "artifact.md"
    if fm is None:
        fm = "title: BDD Test\n"
    p.write_text(f"---\n{fm}---\n\n{body}")
    return p


def _run(artifact: Path, extra: list[str] | None = None):
    args = [str(artifact), "--laws-dir", str(BDD_REGISTRY)] + (extra or [])
    return RUNNER.invoke(main, args)


# ---------------------------------------------------------------------------
# §4.1 Scenario 1: Valid citation passes → exit 0, verdict PASS
# ---------------------------------------------------------------------------
class TestSc1ValidCitationPasses:
    def test_verdict_is_pass(self, tmp_path):
        art = _artifact(tmp_path, "This implements ENG-3.5 naming conventions.\n")
        result = _run(art)
        assert result.exit_code == 0

    def test_output_contains_pass(self, tmp_path):
        art = _artifact(tmp_path, "This implements ENG-3.5 naming conventions.\n")
        result = _run(art)
        assert "PASS" in result.output
        assert "ENG-3.5" in result.output


# ---------------------------------------------------------------------------
# §4.1 Scenario 2: Hallucinated ID → FAIL, exit 1
# ---------------------------------------------------------------------------
class TestSc2HallucinatedIdFail:
    def test_exit_code_is_1(self, tmp_path):
        art = _artifact(tmp_path, "Governed by ENG-99.9 (Fictional Law).\n")
        result = _run(art)
        assert result.exit_code == 1

    def test_verdict_is_fail(self, tmp_path):
        art = _artifact(tmp_path, "Governed by ENG-99.9 (Fictional Law).\n")
        result = _run(art)
        assert "FAIL" in result.output
        assert "ENG-99.9" in result.output

    def test_note_contains_not_in_registry(self, tmp_path):
        art = _artifact(tmp_path, "Governed by ENG-99.9 (Fictional Law).\n")
        result = _run(art)
        assert "not in registry" in result.output.lower()


# ---------------------------------------------------------------------------
# §4.1 Scenario 3: Mixed — one FAIL, one PASS → exit 1
# ---------------------------------------------------------------------------
class TestSc3MixedCitations:
    def test_exit_code_is_1(self, tmp_path):
        art = _artifact(tmp_path, "ENG-3.5 naming law and ENG-99.9 unknown.\n")
        result = _run(art)
        assert result.exit_code == 1

    def test_both_ids_in_output(self, tmp_path):
        art = _artifact(tmp_path, "ENG-3.5 naming law and ENG-99.9 unknown.\n")
        result = _run(art)
        assert "ENG-3.5" in result.output
        assert "ENG-99.9" in result.output
        assert "PASS" in result.output
        assert "FAIL" in result.output


# ---------------------------------------------------------------------------
# §4.1 Scenario 4: All citations valid → exit 0
# ---------------------------------------------------------------------------
class TestSc4AllCitationsValid:
    def test_exit_code_is_0(self, tmp_path):
        art = _artifact(tmp_path, "ENG-3.5 and ENG-4.6 are both valid.\n")
        result = _run(art)
        assert result.exit_code == 0

    def test_all_verdicts_pass(self, tmp_path):
        art = _artifact(tmp_path, "ENG-3.5 and ENG-4.6 are both valid.\n")
        result = _run(art)
        assert "0 FAIL" in result.output
        assert "0 WARN" in result.output

# ---------------------------------------------------------------------------
# §4.1 Scenario 5: Draft ID excluded → SKIP in output, exit 0
# ---------------------------------------------------------------------------
class TestSc5DraftIdExcluded:
    def test_exit_code_is_0(self, tmp_path):
        art = _artifact(tmp_path, "ENG-14.1 (proposed) governs citation audit.\n")
        result = _run(art, ["--allow-draft", "ENG-14.1"])
        assert result.exit_code == 0

    def test_skip_appears_in_output(self, tmp_path):
        art = _artifact(tmp_path, "ENG-14.1 (proposed) governs citation audit.\n")
        result = _run(art, ["--allow-draft", "ENG-14.1"])
        assert "SKIP" in result.output
        assert "ENG-14.1" in result.output

    def test_draft_not_evaluated_note(self, tmp_path):
        art = _artifact(tmp_path, "ENG-14.1 (proposed) governs citation audit.\n")
        result = _run(art, ["--allow-draft", "ENG-14.1"])
        assert "draft" in result.output.lower()

    def test_no_fail_for_draft_id(self, tmp_path):
        art = _artifact(tmp_path, "ENG-14.1 (proposed) governs citation audit.\n")
        result = _run(art, ["--allow-draft", "ENG-14.1"])
        assert "0 FAIL" in result.output


# ---------------------------------------------------------------------------
# §4.1 Scenario 6: --allow-draft ID not present in body → no SKIP, exit 0
# ---------------------------------------------------------------------------
class TestSc6DraftIdNotInBody:
    def test_exit_code_is_0(self, tmp_path):
        art = _artifact(tmp_path, "This artifact does not cite ENG-3.5 by law.\n"
                                  "Wait — it does: ENG-3.5.\n")
        result = _run(art, ["--allow-draft", "ENG-14.1"])
        assert result.exit_code == 0

    def test_draft_id_not_in_output_rows(self, tmp_path):
        art = _artifact(tmp_path, "This cites ENG-3.5 only.\n")
        result = _run(art, ["--allow-draft", "ENG-14.1"])
        # ENG-14.1 not in body → should not appear as SKIP row
        assert "ENG-14.1" not in result.output


# ---------------------------------------------------------------------------
# §4.1 Scenario 7: ENG-12.1 PASS (it IS in the fixture registry)
# ---------------------------------------------------------------------------
class TestSc7Eng121Pass:
    def test_eng_12_1_verdict_pass(self, tmp_path):
        art = _artifact(tmp_path, "ENG-12.1 is the agentic phase gate law.\n")
        result = _run(art)
        assert result.exit_code == 0
        assert "ENG-12.1" in result.output
        assert "PASS" in result.output
        assert "0 FAIL" in result.output


# ---------------------------------------------------------------------------
# §4.1 Scenario 8: Artifact with zero law citations → exit 0, scanned=0
# ---------------------------------------------------------------------------
class TestSc8ZeroCitations:
    def test_exit_code_is_0(self, tmp_path):
        art = _artifact(tmp_path, "No law IDs here — just prose.\n")
        result = _run(art)
        assert result.exit_code == 0

    def test_summary_shows_zero_scanned(self, tmp_path):
        art = _artifact(tmp_path, "No law IDs here — just prose.\n")
        result = _run(art)
        assert "0 citations scanned" in result.output

    def test_summary_shows_zero_counts(self, tmp_path):
        art = _artifact(tmp_path, "No law IDs here — just prose.\n")
        result = _run(art)
        assert "0 FAIL" in result.output
        assert "0 WARN" in result.output
        assert "0 PASS" in result.output


# ---------------------------------------------------------------------------
# §4.1 Scenario 9: Same law ID appears multiple times — deduplicated
# ---------------------------------------------------------------------------
class TestSc9Deduplication:
    def test_scanned_count_is_1(self, tmp_path):
        body = "ENG-3.5 on first line.\n\nENG-3.5 again on third line.\n"
        art = _artifact(tmp_path, body)
        result = _run(art)
        assert result.exit_code == 0
        assert "1 citations scanned" in result.output

    def test_only_one_row_in_output(self, tmp_path):
        body = "ENG-3.5 mentioned here and also ENG-3.5 mentioned again.\n"
        art = _artifact(tmp_path, body)
        result = _run(art)
        # Count occurrences of ENG-3.5 in table rows
        rows = [ln for ln in result.output.splitlines() if "ENG-3.5" in ln
                and ("PASS" in ln or "FAIL" in ln or "WARN" in ln)]
        assert len(rows) == 1
