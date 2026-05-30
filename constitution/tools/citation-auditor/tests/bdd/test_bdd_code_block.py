"""BDD tests — Phase 3 §4.3 Code Block Exclusion (T-07).

Verifies that law IDs inside fenced blocks (backtick, tilde) and inline
code spans are NOT extracted, while body-text IDs are still evaluated.
"""
from __future__ import annotations

from pathlib import Path

from click.testing import CliRunner

from citation_auditor.cli import main

RUNNER = CliRunner()
BDD_REGISTRY = Path(__file__).parent.parent / "fixtures" / "bdd" / "registry"
FIXTURE_CODE_BLOCK = (
    Path(__file__).parent.parent / "fixtures" / "bdd" / "artifact_code_block_ids.md"
)


def _artifact(tmp_path: Path, content: str) -> Path:
    p = tmp_path / "artifact.md"
    p.write_text(content)
    return p


def _run(artifact: Path, extra: list[str] | None = None):
    args = [str(artifact), "--laws-dir", str(BDD_REGISTRY)] + (extra or [])
    return RUNNER.invoke(main, args)


# ---------------------------------------------------------------------------
# §4.3 Sc-1: ID inside backtick fenced block NOT evaluated
# ---------------------------------------------------------------------------
class TestFencedBlockNotExtracted:
    def test_fenced_id_not_in_results(self, tmp_path):
        content = (
            "---\ntitle: T\n---\n\nBody text only.\n\n"
            "```python\n"
            "# ENG-99.9 is hallucinated but inside code block\n"
            "```\n"
        )
        art = _artifact(tmp_path, content)
        result = _run(art)
        # ENG-99.9 is not in registry; if it were extracted → FAIL; must be exit 0
        assert result.exit_code == 0
        assert "ENG-99.9" not in result.output

    def test_exit_code_0_no_fail(self, tmp_path):
        content = (
            "---\ntitle: T\n---\n\n"
            "```\nENG-0.0 inside fence\n```\n"
        )
        art = _artifact(tmp_path, content)
        result = _run(art)
        assert result.exit_code == 0


# ---------------------------------------------------------------------------
# §4.3 Sc-2: ID inside inline code span NOT evaluated
# ---------------------------------------------------------------------------
class TestInlineCodeNotExtracted:
    def test_inline_code_id_not_in_results(self, tmp_path):
        content = (
            "---\ntitle: T\n---\n\n"
            "Use `ENG-99.9` as the draft placeholder.\n"
        )
        art = _artifact(tmp_path, content)
        result = _run(art)
        assert result.exit_code == 0
        assert "ENG-99.9" not in result.output

    def test_only_body_id_evaluated(self, tmp_path):
        content = (
            "---\ntitle: T\n---\n\n"
            "See `ENG-99.9` for the proposal, but ENG-3.5 is active.\n"
        )
        art = _artifact(tmp_path, content)
        result = _run(art)
        # ENG-3.5 PASS, ENG-99.9 excluded → exit 0
        assert result.exit_code == 0
        assert "ENG-3.5" in result.output


# ---------------------------------------------------------------------------
# §4.3 Sc-3: Same ID in code block AND body → only body evaluated (1 FAIL)
# ---------------------------------------------------------------------------
class TestMixedOccurrenceBodyAndFence:
    def test_one_fail_result_for_body_id(self, tmp_path):
        content = (
            "---\ntitle: T\n---\n\n"
            "Body reference: ENG-99.9 is hallucinated.\n\n"
            "```python\nENG-99.9 also in code block\n```\n"
        )
        art = _artifact(tmp_path, content)
        result = _run(art)
        assert result.exit_code == 1
        # Exactly one FAIL row for ENG-99.9
        fail_rows = [ln for ln in result.output.splitlines()
                     if "ENG-99.9" in ln and "FAIL" in ln]
        assert len(fail_rows) == 1

    def test_scanned_count_is_1(self, tmp_path):
        content = (
            "---\ntitle: T\n---\n\n"
            "ENG-99.9 in body.\n\n"
            "```\nENG-99.9 in fence\n```\n"
        )
        art = _artifact(tmp_path, content)
        result = _run(art)
        assert "1 citations scanned" in result.output


# ---------------------------------------------------------------------------
# §4.3 Sc-4: Multiline fenced block stripped correctly
# ---------------------------------------------------------------------------
class TestMultilineFencedBlock:
    def test_multiline_fence_id_not_extracted(self, tmp_path):
        lines = "\n".join(f"Line {i}" for i in range(1, 11))
        content = (
            "---\ntitle: T\n---\n\n"
            f"```\n{lines}\nLine 5 has ENG-0.0 buried in here\n```\n\n"
            "Body: ENG-3.5 is valid.\n"
        )
        art = _artifact(tmp_path, content)
        result = _run(art)
        assert result.exit_code == 0
        assert "ENG-3.5" in result.output
        assert "ENG-0.0" not in result.output

    def test_fixture_file_only_body_id_extracted(self):
        """Use pre-built fixture: only ENG-3.5 from body should appear."""
        result = RUNNER.invoke(main, [
            str(FIXTURE_CODE_BLOCK),
            "--laws-dir", str(BDD_REGISTRY),
        ])
        assert result.exit_code == 0
        assert "ENG-3.5" in result.output
        assert "ENG-99.9" not in result.output
        assert "ENG-0.0" not in result.output

    def test_tilde_fenced_block_stripped(self, tmp_path):
        content = (
            "---\ntitle: T\n---\n\n"
            "~~~yaml\nENG-99.9: inside tilde fence\n~~~\n\n"
            "Body: ENG-3.5 naming.\n"
        )
        art = _artifact(tmp_path, content)
        result = _run(art)
        assert result.exit_code == 0
        assert "ENG-99.9" not in result.output
