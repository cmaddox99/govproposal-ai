"""BDD tests — Phase 3 §4.2 Status Mismatch scenarios (Sc-5, Sc-6, Sc-7).

Also covers §4.2 Sc-1–4 (Title Mismatch).

Fixture registry: tests/fixtures/bdd/registry/
- ENG-3.5: non_negotiable=false
- ENG-10.1: non_negotiable=false  (title: "Constitution Metrics Collection Law")
- ENG-12.1: non_negotiable=true
- BUS-7.1: non_negotiable=true
"""
from __future__ import annotations

from pathlib import Path

from click.testing import CliRunner

from citation_auditor.cli import main

RUNNER = CliRunner()
BDD_REGISTRY = Path(__file__).parent.parent / "fixtures" / "bdd" / "registry"


def _artifact(tmp_path: Path, body: str) -> Path:
    p = tmp_path / "artifact.md"
    p.write_text(f"---\ntitle: BDD Status Mismatch Test\n---\n\n{body}")
    return p


def _run(artifact: Path, extra: list[str] | None = None):
    args = [str(artifact), "--laws-dir", str(BDD_REGISTRY)] + (extra or [])
    return RUNNER.invoke(main, args)


# ---------------------------------------------------------------------------
# §4.2 Sc-1: Explicit title phrase score < 60 → WARN
# ---------------------------------------------------------------------------
class TestTitleMismatchWarn:
    def test_wrong_title_phrase_produces_warn(self, tmp_path):
        # ENG-10.1 registry title: "Constitution Metrics Collection Law"
        # Phrase "Amendment Process Law" has low similarity → WARN
        art = _artifact(tmp_path, 'ENG-10.1 (Amendment Process Law) governs metrics.\n')
        result = _run(art)
        assert "WARN" in result.output
        assert "ENG-10.1" in result.output

    def test_warn_exit_code_is_0_without_strict(self, tmp_path):
        art = _artifact(tmp_path, 'ENG-10.1 (Amendment Process Law) governs metrics.\n')
        result = _run(art)
        assert result.exit_code == 0

    def test_warn_note_mentions_title_phrase_score(self, tmp_path):
        art = _artifact(tmp_path, 'ENG-10.1 (Amendment Process Law) governs metrics.\n')
        result = _run(art)
        assert "score" in result.output.lower() or "title" in result.output.lower() \
               or "mismatch" in result.output.lower()


# ---------------------------------------------------------------------------
# §4.2 Sc-2: No explicit title phrase → no WARN
# ---------------------------------------------------------------------------
class TestNoTitlePhraseNoWarn:
    def test_bare_id_no_warn(self, tmp_path):
        art = _artifact(tmp_path, "governed by ENG-10.1 for observability.\n")
        result = _run(art)
        assert "0 WARN" in result.output
        assert "ENG-10.1" in result.output
        assert "PASS" in result.output
        assert result.exit_code == 0


# ---------------------------------------------------------------------------
# §4.2 Sc-3: Explicit title phrase with score >= 60 → PASS
# ---------------------------------------------------------------------------
class TestTitlePhraseHighScore:
    def test_correct_title_phrase_passes(self, tmp_path):
        # "Naming Conventions Law" ≈ registry title for ENG-3.5
        art = _artifact(tmp_path, "ENG-3.5 **Naming Conventions Law** must be followed.\n")
        result = _run(art)
        assert "0 WARN" in result.output
        assert result.exit_code == 0


# ---------------------------------------------------------------------------
# §4.2 Sc-4: WARN in --strict mode → exit 1
# ---------------------------------------------------------------------------
class TestWarnStrictModeExit1:
    def test_warn_with_strict_exits_1(self, tmp_path):
        art = _artifact(tmp_path, 'ENG-10.1 (Amendment Process Law) governs metrics.\n')
        result = _run(art, ["--strict"])
        # WARN is produced; --strict makes exit 1
        assert result.exit_code == 1

    def test_warn_verdict_still_warn_not_fail(self, tmp_path):
        # --strict does NOT upgrade WARN → FAIL in output
        art = _artifact(tmp_path, 'ENG-10.1 (Amendment Process Law) governs metrics.\n')
        result = _run(art, ["--strict"])
        assert "WARN" in result.output
        # No FAIL verdict rows (only "0 FAIL" in summary)
        assert "0 FAIL" in result.output


# ---------------------------------------------------------------------------
# §4.2 Sc-5: STATUS_MISMATCH — NON-NEGOTIABLE on non-NON-NEG law → WARN
# ---------------------------------------------------------------------------
class TestStatusMismatchNonNegOnFalseLaw:
    def test_non_neg_assertion_on_non_non_neg_law_warns(self, tmp_path):
        # ENG-3.5 is non_negotiable=false in fixture registry
        # Asserting NON-NEGOTIABLE → STATUS_MISMATCH → WARN
        art = _artifact(tmp_path, "ENG-3.5 (NON-NEGOTIABLE) naming law applies.\n")
        result = _run(art)
        assert "WARN" in result.output
        assert "ENG-3.5" in result.output

    def test_note_mentions_status_mismatch(self, tmp_path):
        art = _artifact(tmp_path, "ENG-3.5 (NON-NEGOTIABLE) naming law applies.\n")
        result = _run(art)
        assert "status mismatch" in result.output.lower() \
               or "mismatch" in result.output.lower()

    def test_exit_code_is_0(self, tmp_path):
        art = _artifact(tmp_path, "ENG-3.5 (NON-NEGOTIABLE) naming law applies.\n")
        result = _run(art)
        assert result.exit_code == 0


# ---------------------------------------------------------------------------
# §4.2 Sc-6: STATUS_MISMATCH — NON-NEGOTIABLE on actual NON-NEG law → PASS
# ---------------------------------------------------------------------------
class TestStatusMatchNonNegOnTrueLaw:
    def test_non_neg_assertion_on_non_neg_law_passes(self, tmp_path):
        # BUS-7.1 is non_negotiable=true in fixture registry
        art = _artifact(tmp_path, "BUS-7.1 (NON-NEGOTIABLE) audit trail required.\n")
        result = _run(art)
        assert "0 WARN" in result.output
        assert "0 FAIL" in result.output
        assert result.exit_code == 0

    def test_verdict_is_pass(self, tmp_path):
        art = _artifact(tmp_path, "BUS-7.1 (NON-NEGOTIABLE) audit trail required.\n")
        result = _run(art)
        assert "BUS-7.1" in result.output
        assert "PASS" in result.output


# ---------------------------------------------------------------------------
# §4.2 Sc-7: STATUS_MISMATCH — STRICTLY ENFORCED on NON-NEG law → WARN
# ---------------------------------------------------------------------------
class TestStatusMismatchStrictlyEnforcedOnNonNeg:
    def test_strictly_enforced_on_non_neg_warns(self, tmp_path):
        # BUS-7.1 is non_negotiable=true; "STRICTLY ENFORCED" ≠ correct phrasing
        art = _artifact(tmp_path, "BUS-7.1 (STRICTLY ENFORCED) audit trail required.\n")
        result = _run(art)
        assert "WARN" in result.output
        assert "BUS-7.1" in result.output

    def test_note_mentions_mismatch(self, tmp_path):
        art = _artifact(tmp_path, "BUS-7.1 (STRICTLY ENFORCED) audit trail required.\n")
        result = _run(art)
        assert "mismatch" in result.output.lower()

    def test_exit_code_is_0(self, tmp_path):
        art = _artifact(tmp_path, "BUS-7.1 (STRICTLY ENFORCED) audit trail required.\n")
        result = _run(art)
        assert result.exit_code == 0
