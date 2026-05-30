"""Unit tests for auditor.py — S-03 (Phase 6 Build).

Covers all verdict rules from Phase 3 §2.2 and BDD scenarios §4.1/§4.2:
- FAIL: law_id not in registry
- WARN TITLE_MISMATCH: explicit title phrase within ±30 chars, partial_ratio < 60
- WARN STATUS_MISMATCH: NON-NEGOTIABLE/STRICTLY ENFORCED claim contradicts registry
- PASS: in registry, no mismatch detected
- Sorting: FAIL → WARN → PASS, then alpha within tier
- AuditResult fields: artifact_path, registry_path, law_count, scanned, results,
  draft_skipped, allow_draft, strict, timestamp, tool_version
- @property: fail_count, warn_count, pass_count, audit_exit_code
- strict=True: exit_code=1 on any WARN
- Zero citations: scanned=0, results=[]
- Context snippet: None for PASS, populated for FAIL/WARN
"""
from __future__ import annotations

from pathlib import Path
from unittest.mock import patch

import pytest
from citation_auditor.exceptions import AuditError
from citation_auditor.models import AuditResult, CitationResult, Verdict
from citation_auditor.registry import RegistryEntry

from citation_auditor.auditor import audit, _check_title_mismatch  # noqa: E402
from citation_auditor.scanner import scan_artifact  # noqa: E402

FIXTURES = Path(__file__).parent.parent / "fixtures" / "auditor"
SCANNER_FIXTURES = Path(__file__).parent.parent / "fixtures" / "scanner"

_VERSION = "0.1.0"
_REG_PATH = "laws/"
_ART_PATH = "artifact.md"
_TS = "2026-05-24T17:00:00Z"


def _entry(law_id: str, non_negotiable: bool = False, title: str = "Some Law") -> RegistryEntry:
    return RegistryEntry(
        law_id=law_id,
        domain="engineering",
        title=title,
        summary=f"Summary of {law_id}",
        non_negotiable=non_negotiable,
    )


def _reg(**kwargs) -> dict[str, RegistryEntry]:
    """Build registry from law_id→RegistryEntry kwargs."""
    return dict(kwargs)


def _citation(law_id: str, snippet: str = "...context...") -> tuple[str, str]:
    return (law_id, snippet)


def _make_result(
    citations: list[tuple[str, str]],
    registry: dict[str, RegistryEntry],
    strict: bool = False,
    draft_skipped: list[str] | None = None,
) -> AuditResult:
    return audit(
        citations=citations,
        registry=registry,
        artifact_path=_ART_PATH,
        registry_path=_REG_PATH,
        law_count=len(registry),
        draft_skipped=draft_skipped or [],
        allow_draft=[],
        strict=strict,
        timestamp=_TS,
        tool_version=_VERSION,
    )


# ---------------------------------------------------------------------------
# Return type contract
# ---------------------------------------------------------------------------
class TestReturnContract:
    def test_returns_audit_result(self):
        result = _make_result([], {})
        assert isinstance(result, AuditResult)

    def test_audit_result_has_all_fields(self):
        result = _make_result([], {})
        assert result.artifact_path == _ART_PATH
        assert result.registry_path == _REG_PATH
        assert result.law_count == 0
        assert result.scanned == 0
        assert result.results == []
        assert result.draft_skipped == []
        assert result.allow_draft == []
        assert result.strict is False
        assert result.timestamp == _TS
        assert result.tool_version == _VERSION

    def test_results_is_list_of_citation_result(self):
        reg = {"ENG-4.1": _entry("ENG-4.1")}
        result = _make_result([_citation("ENG-4.1")], reg)
        for r in result.results:
            assert isinstance(r, CitationResult)


# ---------------------------------------------------------------------------
# PASS verdict
# ---------------------------------------------------------------------------
class TestPassVerdict:
    def test_known_id_no_mismatch_is_pass(self):
        reg = {"ENG-4.1": _entry("ENG-4.1", title="Atomic TDD Law")}
        result = _make_result([_citation("ENG-4.1", "governed by ENG-4.1 for testing")], reg)
        assert result.results[0].verdict == Verdict.PASS

    def test_pass_note_is_none(self):
        reg = {"ENG-4.1": _entry("ENG-4.1", title="Atomic TDD Law")}
        result = _make_result([_citation("ENG-4.1", "ENG-4.1 governs")], reg)
        assert result.results[0].note is None

    def test_pass_context_snippet_is_none(self):
        reg = {"ENG-4.1": _entry("ENG-4.1", title="Atomic TDD Law")}
        result = _make_result([_citation("ENG-4.1", "ENG-4.1 governs")], reg)
        assert result.results[0].context_snippet is None

    def test_exit_code_zero_on_all_pass(self):
        reg = {"ENG-4.1": _entry("ENG-4.1"), "PRD-2.6": _entry("PRD-2.6")}
        result = _make_result([_citation("ENG-4.1"), _citation("PRD-2.6")], reg)
        assert result.audit_exit_code == 0

    def test_non_negotiable_asserted_correctly_is_pass(self):
        # BUS-7.1 is NON-NEGOTIABLE in registry; artifact says "(NON-NEGOTIABLE)" → PASS
        reg = {"BUS-7.1": _entry("BUS-7.1", non_negotiable=True, title="Audit Trail Law")}
        snippet = "BUS-7.1 (NON-NEGOTIABLE) must be followed"
        result = _make_result([_citation("BUS-7.1", snippet)], reg)
        assert result.results[0].verdict == Verdict.PASS


# ---------------------------------------------------------------------------
# FAIL verdict — ID not in registry
# ---------------------------------------------------------------------------
class TestFailVerdict:
    def test_unknown_id_is_fail(self):
        reg = {}
        result = _make_result([_citation("ENG-99.9")], reg)
        assert result.results[0].verdict == Verdict.FAIL

    def test_fail_note_contains_not_in_registry(self):
        reg = {}
        result = _make_result([_citation("ENG-99.9")], reg)
        assert "not in registry" in result.results[0].note.lower()

    def test_fail_context_snippet_populated(self):
        reg = {}
        snippet = "governed by ENG-99.9 fictional law"
        result = _make_result([_citation("ENG-99.9", snippet)], reg)
        assert result.results[0].context_snippet == snippet

    def test_exit_code_one_on_any_fail(self):
        reg = {}
        result = _make_result([_citation("ENG-99.9")], reg)
        assert result.audit_exit_code == 1

    def test_one_fail_among_passes_exit_one(self):
        reg = {"ENG-4.1": _entry("ENG-4.1")}
        result = _make_result([_citation("ENG-4.1"), _citation("ENG-99.9")], reg)
        assert result.audit_exit_code == 1


# ---------------------------------------------------------------------------
# WARN: TITLE_MISMATCH — explicit title phrase, partial_ratio < 60
# ---------------------------------------------------------------------------
class TestTitleMismatchWarn:
    def test_explicit_title_low_score_is_warn(self):
        # "Amendment Process Law" vs "Constitution Metrics Collection Law" — score < 60
        reg = {"ENG-10.1": _entry("ENG-10.1", title="Constitution Metrics Collection Law")}
        # Title phrase in parens within 30 chars of ID
        snippet = "ENG-10.1 (Amendment Process Law) governs this"
        result = _make_result([_citation("ENG-10.1", snippet)], reg)
        assert result.results[0].verdict == Verdict.WARN

    def test_title_mismatch_note_contains_score_info(self):
        reg = {"ENG-10.1": _entry("ENG-10.1", title="Constitution Metrics Collection Law")}
        snippet = "ENG-10.1 (Amendment Process Law) governs this"
        result = _make_result([_citation("ENG-10.1", snippet)], reg)
        note = result.results[0].note.lower()
        assert "title" in note or "score" in note or "mismatch" in note

    def test_title_mismatch_context_snippet_populated(self):
        reg = {"ENG-10.1": _entry("ENG-10.1", title="Constitution Metrics Collection Law")}
        snippet = "ENG-10.1 (Amendment Process Law) governs this"
        result = _make_result([_citation("ENG-10.1", snippet)], reg)
        assert result.results[0].context_snippet is not None

    def test_explicit_title_high_score_is_pass(self):
        # Title phrase closely matches registry — score ≥ 60 → PASS
        reg = {"ENG-3.5": _entry("ENG-3.5", title="Naming Conventions Law")}
        snippet = "ENG-3.5 **Naming Conventions Law** must be applied"
        result = _make_result([_citation("ENG-3.5", snippet)], reg)
        assert result.results[0].verdict == Verdict.PASS

    def test_no_explicit_title_phrase_near_id_is_pass(self):
        # No bold/quoted text within 30 chars → no title check → PASS
        reg = {"ENG-10.1": _entry("ENG-10.1", title="Constitution Metrics Collection Law")}
        snippet = "governed by ENG-10.1 for compliance"
        result = _make_result([_citation("ENG-10.1", snippet)], reg)
        assert result.results[0].verdict == Verdict.PASS

    def test_exit_code_zero_for_warn_without_strict(self):
        reg = {"ENG-10.1": _entry("ENG-10.1", title="Constitution Metrics Collection Law")}
        snippet = "ENG-10.1 (Amendment Process Law)"
        result = _make_result([_citation("ENG-10.1", snippet)], reg, strict=False)
        assert result.audit_exit_code == 0


# ---------------------------------------------------------------------------
# WARN: STATUS_MISMATCH — NON-NEGOTIABLE/STRICTLY ENFORCED assertion
# ---------------------------------------------------------------------------
class TestStatusMismatchWarn:
    def test_non_neg_asserted_on_non_non_neg_law_is_warn(self):
        # ENG-3.5 non_negotiable=False; artifact says "(NON-NEGOTIABLE)" → WARN
        reg = {"ENG-3.5": _entry("ENG-3.5", non_negotiable=False, title="Naming Conventions Law")}
        snippet = "ENG-3.5 (NON-NEGOTIABLE) applies here"
        result = _make_result([_citation("ENG-3.5", snippet)], reg)
        assert result.results[0].verdict == Verdict.WARN

    def test_status_mismatch_note_contains_status_mismatch(self):
        reg = {"ENG-3.5": _entry("ENG-3.5", non_negotiable=False)}
        snippet = "ENG-3.5 (NON-NEGOTIABLE) applies"
        result = _make_result([_citation("ENG-3.5", snippet)], reg)
        assert "status mismatch" in result.results[0].note.lower()

    def test_strictly_enforced_on_non_neg_law_is_warn(self):
        # BUS-7.1 non_negotiable=True; "STRICTLY ENFORCED" is wrong label → WARN
        reg = {"BUS-7.1": _entry("BUS-7.1", non_negotiable=True, title="Audit Trail Law")}
        snippet = "BUS-7.1 (STRICTLY ENFORCED) in all workflows"
        result = _make_result([_citation("BUS-7.1", snippet)], reg)
        assert result.results[0].verdict == Verdict.WARN

    def test_status_mismatch_context_snippet_populated(self):
        reg = {"ENG-3.5": _entry("ENG-3.5", non_negotiable=False)}
        snippet = "ENG-3.5 (NON-NEGOTIABLE) applies"
        result = _make_result([_citation("ENG-3.5", snippet)], reg)
        assert result.results[0].context_snippet is not None

    def test_status_check_only_within_50_chars_of_id(self):
        # Status assertion is 100 chars away — should NOT trigger WARN
        reg = {"ENG-3.5": _entry("ENG-3.5", non_negotiable=False)}
        padding = "x" * 100
        snippet = f"ENG-3.5 {padding} (NON-NEGOTIABLE)"
        result = _make_result([_citation("ENG-3.5", snippet)], reg)
        assert result.results[0].verdict == Verdict.PASS


# ---------------------------------------------------------------------------
# strict mode
# ---------------------------------------------------------------------------
class TestStrictMode:
    def test_strict_warn_yields_exit_code_1(self):
        reg = {"ENG-3.5": _entry("ENG-3.5", non_negotiable=False)}
        snippet = "ENG-3.5 (NON-NEGOTIABLE) applies"
        result = _make_result([_citation("ENG-3.5", snippet)], reg, strict=True)
        assert result.audit_exit_code == 1

    def test_strict_flag_stored_in_result(self):
        result = _make_result([], {}, strict=True)
        assert result.strict is True

    def test_strict_false_warn_yields_exit_code_0(self):
        reg = {"ENG-3.5": _entry("ENG-3.5", non_negotiable=False)}
        snippet = "ENG-3.5 (NON-NEGOTIABLE) applies"
        result = _make_result([_citation("ENG-3.5", snippet)], reg, strict=False)
        assert result.audit_exit_code == 0

    def test_strict_no_warn_yields_exit_code_0(self):
        reg = {"ENG-4.1": _entry("ENG-4.1")}
        result = _make_result([_citation("ENG-4.1")], reg, strict=True)
        assert result.audit_exit_code == 0


# ---------------------------------------------------------------------------
# Sorting: FAIL → WARN → PASS, then alpha within tier
# ---------------------------------------------------------------------------
class TestResultSorting:
    def test_fail_before_warn_before_pass(self):
        reg = {
            "ENG-4.1": _entry("ENG-4.1", non_negotiable=False),
            "PRD-2.6": _entry("PRD-2.6"),
        }
        citations = [
            _citation("PRD-2.6"),                                        # PASS
            _citation("ENG-4.1", "ENG-4.1 (NON-NEGOTIABLE)"),            # WARN
            _citation("ENG-99.9"),                                        # FAIL
        ]
        result = _make_result(citations, reg)
        verdicts = [r.verdict for r in result.results]
        # FAIL first, then WARN, then PASS
        fail_idx = verdicts.index(Verdict.FAIL)
        warn_idx = verdicts.index(Verdict.WARN)
        pass_idx = verdicts.index(Verdict.PASS)
        assert fail_idx < warn_idx < pass_idx

    def test_alpha_within_fail_tier(self):
        reg = {}
        citations = [_citation("PRD-9.9"), _citation("ENG-9.9"), _citation("BUS-9.9")]
        result = _make_result(citations, reg)
        fail_ids = [r.law_id for r in result.results if r.verdict == Verdict.FAIL]
        assert fail_ids == sorted(fail_ids)

    def test_alpha_within_pass_tier(self):
        reg = {
            "PRD-2.6": _entry("PRD-2.6"),
            "ENG-4.1": _entry("ENG-4.1"),
            "BUS-7.1": _entry("BUS-7.1"),
        }
        citations = [_citation("PRD-2.6"), _citation("ENG-4.1"), _citation("BUS-7.1")]
        result = _make_result(citations, reg)
        pass_ids = [r.law_id for r in result.results if r.verdict == Verdict.PASS]
        assert pass_ids == sorted(pass_ids)


# ---------------------------------------------------------------------------
# Zero citations
# ---------------------------------------------------------------------------
class TestZeroCitations:
    def test_zero_citations_scanned_is_zero(self):
        result = _make_result([], {})
        assert result.scanned == 0

    def test_zero_citations_results_empty(self):
        result = _make_result([], {})
        assert result.results == []

    def test_zero_citations_exit_code_zero(self):
        result = _make_result([], {})
        assert result.audit_exit_code == 0


# ---------------------------------------------------------------------------
# scanned count
# ---------------------------------------------------------------------------
class TestScannedCount:
    def test_scanned_reflects_citations_list_length(self):
        reg = {"ENG-4.1": _entry("ENG-4.1"), "PRD-2.6": _entry("PRD-2.6")}
        citations = [_citation("ENG-4.1"), _citation("PRD-2.6"), _citation("ENG-99.9")]
        result = _make_result(citations, reg)
        assert result.scanned == 3

    def test_draft_skipped_not_in_scanned(self):
        reg = {"ENG-4.1": _entry("ENG-4.1")}
        # scanned = len(citations); draft_skipped passed separately
        result = audit(
            citations=[_citation("ENG-4.1")],
            registry=reg,
            artifact_path=_ART_PATH,
            registry_path=_REG_PATH,
            law_count=1,
            draft_skipped=["ENG-14.1"],
            allow_draft=["ENG-14.1"],
            strict=False,
            timestamp=_TS,
            tool_version=_VERSION,
        )
        assert result.scanned == 1  # only ENG-4.1 in citations
        assert "ENG-14.1" in result.draft_skipped


# ---------------------------------------------------------------------------
# @property counts
# ---------------------------------------------------------------------------
class TestPropertyCounts:
    def test_fail_count(self):
        reg = {}
        result = _make_result([_citation("ENG-9.9"), _citation("PRD-9.9")], reg)
        assert result.fail_count == 2

    def test_warn_count(self):
        reg = {"ENG-3.5": _entry("ENG-3.5", non_negotiable=False)}
        snippet = "ENG-3.5 (NON-NEGOTIABLE)"
        result = _make_result([_citation("ENG-3.5", snippet)], reg)
        assert result.warn_count == 1

    def test_pass_count(self):
        reg = {"ENG-4.1": _entry("ENG-4.1"), "PRD-2.6": _entry("PRD-2.6")}
        result = _make_result([_citation("ENG-4.1"), _citation("PRD-2.6")], reg)
        assert result.pass_count == 2

    def test_internal_failure_raises_audit_error(self):
        # Pass a citation tuple where snippet is not a string → triggers internal error
        reg = {"ENG-4.1": _entry("ENG-4.1")}
        with pytest.raises((AuditError, TypeError)):
            audit(
                citations=[("ENG-4.1", None)],  # type: ignore[arg-type]
                registry=reg,
                artifact_path=_ART_PATH,
                registry_path=_REG_PATH,
                law_count=1,
                draft_skipped=[],
                allow_draft=[],
                strict=False,
                timestamp=_TS,
                tool_version=_VERSION,
            )

    def test_empty_title_phrase_no_warn(self):
        # Parenthesised phrase that is empty after strip — no title WARN raised
        reg = {"ENG-4.1": _entry("ENG-4.1", title="Atomic TDD Law")}
        snippet = "ENG-4.1 () governs testing"
        result = _make_result([_citation("ENG-4.1", snippet)], reg)
        assert result.results[0].verdict == Verdict.PASS


# ---------------------------------------------------------------------------
# Mutation-killing tests — targeted at survived mutants from mutmut run
# ---------------------------------------------------------------------------
class TestMutationKilling:

    # --- Mutant 4: _STATUS_STRICT regex broken —
    # If regex breaks, "STRICTLY ENFORCED" would be caught as a title phrase instead.
    # Test that note specifically says "status mismatch" (not a title note).
    def test_strictly_enforced_note_says_status_mismatch(self):
        reg = {"BUS-7.1": _entry("BUS-7.1", non_negotiable=True, title="Audit Trail Law")}
        snippet = "BUS-7.1 (STRICTLY ENFORCED) in all workflows"
        result = _make_result([_citation("BUS-7.1", snippet)], reg)
        assert "status mismatch" in result.results[0].note.lower()

    # --- Mutant 7: WARN tier=2 (same as PASS) → WARN would sort after PASS if PASS law_id < WARN law_id
    def test_warn_before_pass_when_warn_id_greater_alphabetically(self):
        # ZNG-9.9 (WARN) > AAA-1.1 (PASS) alphabetically; tier must still sort WARN before PASS
        reg = {
            "ZNG-9.9": _entry("ZNG-9.9", non_negotiable=False),
            "AAA-1.1": _entry("AAA-1.1"),
        }
        citations = [
            _citation("AAA-1.1"),                              # PASS
            _citation("ZNG-9.9", "ZNG-9.9 (NON-NEGOTIABLE)"),  # WARN
        ]
        result = _make_result(citations, reg)
        verdicts = [r.verdict for r in result.results]
        assert verdicts[0] == Verdict.WARN
        assert verdicts[1] == Verdict.PASS

    # --- Mutant 10: threshold 60→61 → score=60 would flip from PASS to WARN
    def test_title_score_exactly_60_is_pass(self):
        reg = {"ENG-4.1": _entry("ENG-4.1", title="Some Law Title")}
        with patch("citation_auditor.auditor.fuzz") as mock_fuzz:
            mock_fuzz.partial_ratio.return_value = 60
            # score=60 is NOT < 60, so should be PASS
            snippet = 'ENG-4.1 "Different Phrase Here"'
            result = _make_result([_citation("ENG-4.1", snippet)], reg)
        assert result.results[0].verdict == Verdict.PASS

    # --- Mutant 12: _STATUS_WINDOW 50→51 — pad=36 is the exact boundary
    # "NON-NEGOTIABLE" (14 chars) at id_end+37..+50 = exactly inside WINDOW=51, outside WINDOW=50
    def test_status_assertion_50_chars_away_no_warn(self):
        reg = {"ENG-3.5": _entry("ENG-3.5", non_negotiable=False)}
        padding = "x" * 36  # verified: WINDOW50 misses "NON-NEGOTIABLE", WINDOW51 finds it
        snippet = f"ENG-3.5{padding}(NON-NEGOTIABLE)"
        result = _make_result([_citation("ENG-3.5", snippet)], reg)
        assert result.results[0].verdict == Verdict.PASS

    # --- Mutant 14: _TITLE_WINDOW 120→121 — pad=116 is the exact boundary
    # '"Bad"' (5 chars) at id_end+116..+120 = exactly inside WINDOW=121, outside WINDOW=120
    def test_title_phrase_120_chars_window_boundary_no_warn(self):
        reg = {"ENG-4.1": _entry("ENG-4.1", title="Atomic TDD Law")}
        padding = "x" * 116  # verified: WINDOW120 misses '"Bad"', WINDOW121 finds it
        snippet = f'ENG-4.1{padding}"Bad"'
        result = _make_result([_citation("ENG-4.1", snippet)], reg)
        assert result.results[0].verdict == Verdict.PASS

    # --- Mutant 19: FAIL note prefix "XX" added — note must START with "ID not in registry"
    def test_fail_note_starts_with_id_not_in_registry(self):
        reg = {}
        result = _make_result([_citation("ENG-99.9")], reg)
        assert result.results[0].note.startswith("ID not in registry")

    # --- Mutant 24: continue→break in title_note branch — second citation would be skipped
    def test_title_warn_continues_processing_subsequent_citations(self):
        reg = {
            "ENG-10.1": _entry("ENG-10.1", title="Constitution Metrics Collection Law"),
            "PRD-2.6": _entry("PRD-2.6"),
        }
        citations = [
            _citation("ENG-10.1", "ENG-10.1 (Amendment Process Law)"),  # WARN
            _citation("PRD-2.6"),                                         # PASS
        ]
        result = _make_result(citations, reg)
        assert len(result.results) == 2
        result_ids = {r.law_id for r in result.results}
        assert "PRD-2.6" in result_ids

    # --- Mutant 26: AuditError note prefix "XX" added
    def test_internal_failure_error_starts_with_internal_auditor(self):
        reg = {"ENG-4.1": _entry("ENG-4.1")}
        try:
            audit(
                citations=[("ENG-4.1", None)],  # type: ignore[arg-type]
                registry=reg,
                artifact_path=_ART_PATH,
                registry_path=_REG_PATH,
                law_count=1,
                draft_skipped=[],
                allow_draft=[],
                strict=False,
                timestamp=_TS,
                tool_version=_VERSION,
            )
        except (AuditError, TypeError) as exc:
            if isinstance(exc, AuditError):
                assert str(exc).startswith("Internal auditor failure")

    # --- Mutant 44: NON-NEG status mismatch note prefix "XX" added
    def test_non_neg_status_mismatch_note_starts_with_status_mismatch(self):
        reg = {"ENG-3.5": _entry("ENG-3.5", non_negotiable=False)}
        snippet = "ENG-3.5 (NON-NEGOTIABLE) applies"
        result = _make_result([_citation("ENG-3.5", snippet)], reg)
        assert result.results[0].note.startswith("Status mismatch")

    # --- Mutant 46: STRICTLY ENFORCED status mismatch note prefix "XX" added
    def test_strictly_enforced_mismatch_note_starts_with_status_mismatch(self):
        reg = {"BUS-7.1": _entry("BUS-7.1", non_negotiable=True, title="Audit Trail Law")}
        snippet = "BUS-7.1 (STRICTLY ENFORCED) in all workflows"
        result = _make_result([_citation("BUS-7.1", snippet)], reg)
        assert result.results[0].note.startswith("Status mismatch")

    # --- Mutant 58: continue→break after status-keyword phrase in title check
    # Need NON-NEG law so STATUS check passes, then title check sees status phrase + bad title.
    # With non_negotiable=True, "(NON-NEGOTIABLE)" assertion is correct → no STATUS_MISMATCH.
    # In title check: "(NON-NEGOTIABLE)" is skipped (status keyword); "(Bad)" is checked → WARN.
    # With break: "(NON-NEGOTIABLE)" breaks the loop → "(Bad)" never checked → PASS (mutant detected).
    def test_status_phrase_skip_continues_to_check_other_phrases(self):
        reg = {"ENG-4.1": _entry("ENG-4.1", non_negotiable=True, title="Atomic TDD Law")}
        # Both phrases within 30-char TITLE_WINDOW; "Bad" scores 50/100 < 60 → WARN on continue
        snippet = "ENG-4.1 (NON-NEGOTIABLE)(Bad)"
        result = _make_result([_citation("ENG-4.1", snippet)], reg)
        assert result.results[0].verdict == Verdict.WARN

    # --- Mutant 60: score < 60 → score <= 60 → score=60 should be PASS
    def test_title_score_60_boundary_is_pass_not_warn(self):
        reg = {"ENG-4.1": _entry("ENG-4.1", title="Some Law Title")}
        with patch("citation_auditor.auditor.fuzz") as mock_fuzz:
            mock_fuzz.partial_ratio.return_value = 60  # boundary: < 60 is False → PASS
            snippet = 'ENG-4.1 "Any Phrase"'
            result = _make_result([_citation("ENG-4.1", snippet)], reg)
        assert result.results[0].verdict == Verdict.PASS

    # --- Mutant 61: title score note f-string prefix "XX" added
    def test_title_mismatch_note_starts_with_title_phrase_score(self):
        reg = {"ENG-10.1": _entry("ENG-10.1", title="Constitution Metrics Collection Law")}
        snippet = "ENG-10.1 (Amendment Process Law)"
        result = _make_result([_citation("ENG-10.1", snippet)], reg)
        assert result.results[0].note.startswith("Title phrase score")

    # --- Mutant 62: title score note f-string suffix "XX" added — check note ends with registry title
    def test_title_mismatch_note_ends_with_registry_title(self):
        reg = {"ENG-10.1": _entry("ENG-10.1", title="Constitution Metrics Collection Law")}
        snippet = "ENG-10.1 (Amendment Process Law)"
        result = _make_result([_citation("ENG-10.1", snippet)], reg)
        note = result.results[0].note
        assert "artifact says" in note
        assert note.endswith("'Constitution Metrics Collection Law'")

    # --- T-37a: score boundary — exactly 60 must NOT warn (< 60, not <=)
    def test_T37a_score_exactly_60_is_pass(self):
        reg = {"ENG-4.1": _entry("ENG-4.1", title="Some Law Title")}
        with patch("citation_auditor.auditor.fuzz") as mock_fuzz:
            mock_fuzz.partial_ratio.return_value = 60
            snippet = "ENG-4.1 (Any Phrase)"
            result = _make_result([_citation("ENG-4.1", snippet)], reg)
        assert result.results[0].verdict == Verdict.PASS  # 60 is NOT < 60

    # --- T-37b: score boundary — 59 must warn (59 IS < 60)
    def test_T37b_score_59_is_warn(self):
        reg = {"ENG-4.1": _entry("ENG-4.1", title="Some Law Title")}
        with patch("citation_auditor.auditor.fuzz") as mock_fuzz:
            mock_fuzz.partial_ratio.return_value = 59
            snippet = "ENG-4.1 (Any Phrase)"
            result = _make_result([_citation("ENG-4.1", snippet)], reg)
        assert result.results[0].verdict == Verdict.WARN  # 59 IS < 60


# ---------------------------------------------------------------------------
# Phase 6 S-02 — Widened L2 title-context detection (T-09 through T-35)
# ---------------------------------------------------------------------------
class TestTitleContextWidened:
    """Widened _TITLE_WINDOW (30→120) + before-window + plain-text dual-anchor."""

    # T-09: table pipe after-window — dual-anchor fires WARN
    def test_T09_table_pipe_after_window_warns(self):
        reg = {"ENG-6.4": _entry("ENG-6.4", title="Data Protection Law")}
        snippet = "before | ENG-6.4 | No God Classes |"
        result = _make_result([_citation("ENG-6.4", snippet)], reg)
        assert result.results[0].verdict == Verdict.WARN

    # T-10: em-dash separator in table — dual-anchor fires WARN
    def test_T10_em_dash_separator_warns(self):
        reg = {"ENG-6.4": _entry("ENG-6.4", title="Data Protection Law")}
        snippet = "| ENG-6.4 — No God Classes |"
        result = _make_result([_citation("ENG-6.4", snippet)], reg)
        assert result.results[0].verdict == Verdict.WARN

    # T-11: before-window open-paren anchor extracts plain phrase → WARN
    def test_T11_before_window_paren_anchor_warns(self):
        reg = {"ENG-6.4": _entry("ENG-6.4", title="Data Protection Law")}
        # before-window = "God classes decomposed (" → anchor=(, extracts "God classes decomposed"
        snippet = "God classes decomposed (ENG-6.4) was identified"
        result = _make_result([_citation("ENG-6.4", snippet)], reg)
        assert result.results[0].verdict == Verdict.WARN

    # T-12: pure prose — no structural separator in either window → PASS (known limitation)
    def test_T12_pure_prose_no_anchor_pass(self):
        reg = {"ENG-4.3": _entry("ENG-4.3", title="Test Quality Law")}
        snippet = "some text ENG-4.3 WireMock consumer contracts more text"
        result = _make_result([_citation("ENG-4.3", snippet)], reg)
        assert result.results[0].verdict == Verdict.PASS

    # T-13: correct title in table cell — dual-anchor but score ≥ 60 → PASS
    def test_T13_correct_title_table_pass(self):
        reg = {"ENG-6.4": _entry("ENG-6.4", title="Data Protection Law")}
        # after-window has no trailing separator → dual-anchor NOT met → PASS
        snippet = "| ENG-6.4 | Data Protection | other"
        result = _make_result([_citation("ENG-6.4", snippet)], reg)
        assert result.results[0].verdict == Verdict.PASS

    # T-14: correct title in parens — formatted phrase, high score → PASS
    def test_T14_correct_title_in_parens_pass(self):
        reg = {"ENG-3.4": _entry("ENG-3.4", title="Single Responsibility Principle")}
        snippet = "ENG-3.4 (Single Responsibility) — rule"
        result = _make_result([_citation("ENG-3.4", snippet)], reg)
        assert result.results[0].verdict == Verdict.PASS

    # T-15: no phrase or anchor near ID → PASS
    def test_T15_no_phrase_near_id_pass(self):
        reg = {"ENG-6.4": _entry("ENG-6.4", title="Data Protection Law")}
        snippet = "see ENG-6.4 for details"
        result = _make_result([_citation("ENG-6.4", snippet)], reg)
        assert result.results[0].verdict == Verdict.PASS

    # T-16: prose without separator — no false WARN → PASS
    def test_T16_prose_false_warn_prevention_pass(self):
        reg = {"ENG-3.4": _entry("ENG-3.4", title="Single Responsibility Principle")}
        snippet = "must review ENG-3.4 carefully"
        result = _make_result([_citation("ENG-3.4", snippet)], reg)
        assert result.results[0].verdict == Verdict.PASS

    # T-17: colon after ID but no trailing separator — dual-anchor NOT met → PASS
    def test_T17_colon_prose_no_trailing_sep_pass(self):
        reg = {"ENG-6.4": _entry("ENG-6.4", title="Data Protection Law")}
        snippet = "ENG-6.4: This requirement must not be violated"
        result = _make_result([_citation("ENG-6.4", snippet)], reg)
        assert result.results[0].verdict == Verdict.PASS

    # T-18: _extract_title_candidates — dual-anchor window yields plain-text candidate
    def test_T18_extract_candidates_dual_anchor(self):
        from citation_auditor.auditor import _extract_title_candidates  # noqa: PLC0415
        candidates = _extract_title_candidates("| No God Classes |", plain_text_allowed=True)
        assert "No God Classes" in candidates

    # T-19: _extract_title_candidates — colon leading but no trailing sep → empty
    def test_T19_extract_candidates_colon_only_empty(self):
        from citation_auditor.auditor import _extract_title_candidates  # noqa: PLC0415
        candidates = _extract_title_candidates(
            ": This requirement is essential", plain_text_allowed=True
        )
        assert candidates == []

    # T-20: before-window reversed iteration picks the closest (last) formatted phrase
    def test_T20_before_window_picks_closest_phrase(self):
        # before-window = "**First Title** and then **Second Title** ("
        # findall gives [First Title, Second Title]; reversed → Second Title chosen first
        snippet = "**First Title** and then **Second Title** (ENG-6.4)"
        note = _check_title_mismatch("ENG-6.4", snippet, "Data Protection Law")
        assert note is not None, "Expected WARN — before-window should find Second Title"
        assert "Second Title" in note
        assert "First Title" not in note

    # T-21: 4-char phrase "FAIL" — not length-filtered, scores < 60 → WARN
    def test_T21_four_char_phrase_scores_low_warns(self):
        reg = {"ENG-6.4": _entry("ENG-6.4", title="Data Protection Law")}
        snippet = "| ENG-6.4 | FAIL |"
        result = _make_result([_citation("ENG-6.4", snippet)], reg)
        assert result.results[0].verdict == Verdict.WARN

    # T-30: regression — ENG-6.4 in Markdown table → full audit produces WARN
    def test_T30_regression_eng64_table_warns(self):
        fixture = SCANNER_FIXTURES / "artifact_regression_disc2026004_eng64.md"
        reg = {"ENG-6.4": _entry("ENG-6.4", title="Data Protection Law")}
        citations, draft_skipped = scan_artifact(fixture, reg, [])
        result = _make_result(citations, reg, draft_skipped=draft_skipped)
        warn_ids = {r.law_id for r in result.results if r.verdict == Verdict.WARN}
        assert "ENG-6.4" in warn_ids, (
            f"Expected WARN for ENG-6.4 (table mismatch); results: {result.results}"
        )

    # T-31: regression — ENG-4.3 in pure prose → full audit produces PASS (known limitation)
    def test_T31_regression_eng43_prose_pass(self):
        fixture = SCANNER_FIXTURES / "artifact_regression_disc2026004_eng43.md"
        reg = {"ENG-4.3": _entry("ENG-4.3", title="Test Quality Law")}
        citations, draft_skipped = scan_artifact(fixture, reg, [])
        result = _make_result(citations, reg, draft_skipped=draft_skipped)
        eng43 = [r for r in result.results if r.law_id == "ENG-4.3"]
        assert eng43, "ENG-4.3 must appear in results"
        assert eng43[0].verdict == Verdict.PASS, (
            f"Expected PASS for pure-prose ENG-4.3; got {eng43[0].verdict}, note={eng43[0].note}"
        )

    # T-35: empty registry_title passed directly → _check_title_mismatch returns None immediately
    def test_T35_empty_registry_title_no_warn(self):
        result = _check_title_mismatch("ENG-6.4", "| ENG-6.4 | No God Classes |", "")
        assert result is None

