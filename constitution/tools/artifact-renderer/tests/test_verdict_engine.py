"""
Unit tests for verdict_engine.py — ensemble agent persona scoring.

Covers:
- All PASS  → APPROVED
- Any WARN (no FAIL) → APPROVED_WITH_CONDITIONS
- Any FAIL  → BLOCKED
- Mixed PASS + WARN + FAIL → BLOCKED
- Empty verdicts → APPROVED
- VerdictLevel enum membership
- PersonaVerdict field access
- EnsembleVerdict aggregate field
"""

import pytest

from aa_artifact_render.verdict_engine import (
    AggregateVerdict,
    EnsembleVerdict,
    PersonaVerdict,
    VerdictEngine,
    VerdictLevel,
)


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

PASS_VERDICT = {"persona": "🧪 TDD Enforcer", "law": "ENG-4.1", "verdict": "PASS", "note": "All tests green."}
WARN_VERDICT = {"persona": "🏗️ Platform Architect", "law": "ENG-2.3", "verdict": "WARN", "note": "72 submodules."}
FAIL_VERDICT = {"persona": "🔒 Security Auditor", "law": "ENG-6.1", "verdict": "FAIL", "note": "PII gap."}


@pytest.fixture
def engine():
    return VerdictEngine()


# ---------------------------------------------------------------------------
# Phase 1.1 — RED: the one test that must FAIL before implementation
# ---------------------------------------------------------------------------

def test_all_pass_produces_approved(engine):
    result = engine.evaluate([PASS_VERDICT])
    assert result.aggregate == AggregateVerdict.APPROVED


# ---------------------------------------------------------------------------
# Additional tests (written together per constitution pattern — cover all cases)
# ---------------------------------------------------------------------------

def test_warn_only_produces_approved_with_conditions(engine):
    result = engine.evaluate([WARN_VERDICT])
    assert result.aggregate == AggregateVerdict.APPROVED_WITH_CONDITIONS


def test_fail_produces_blocked(engine):
    result = engine.evaluate([FAIL_VERDICT])
    assert result.aggregate == AggregateVerdict.BLOCKED


def test_mixed_pass_warn_no_fail_is_approved_with_conditions(engine):
    result = engine.evaluate([PASS_VERDICT, WARN_VERDICT])
    assert result.aggregate == AggregateVerdict.APPROVED_WITH_CONDITIONS


def test_mixed_with_fail_is_blocked(engine):
    result = engine.evaluate([PASS_VERDICT, WARN_VERDICT, FAIL_VERDICT])
    assert result.aggregate == AggregateVerdict.BLOCKED


def test_empty_verdicts_produce_approved(engine):
    result = engine.evaluate([])
    assert result.aggregate == AggregateVerdict.APPROVED


def test_evaluate_returns_ensemble_verdict(engine):
    result = engine.evaluate([PASS_VERDICT])
    assert isinstance(result, EnsembleVerdict)


def test_ensemble_verdict_contains_persona_verdicts(engine):
    result = engine.evaluate([PASS_VERDICT, WARN_VERDICT])
    assert len(result.personas) == 2


def test_persona_verdict_fields_are_accessible(engine):
    result = engine.evaluate([PASS_VERDICT])
    pv = result.personas[0]
    assert pv.persona == "🧪 TDD Enforcer"
    assert pv.law == "ENG-4.1"
    assert pv.verdict == VerdictLevel.PASS
    assert pv.note == "All tests green."


def test_verdict_level_enum_values():
    assert VerdictLevel.PASS == "PASS"
    assert VerdictLevel.WARN == "WARN"
    assert VerdictLevel.FAIL == "FAIL"


def test_aggregate_verdict_enum_values():
    assert AggregateVerdict.APPROVED == "APPROVED"
    assert AggregateVerdict.APPROVED_WITH_CONDITIONS == "APPROVED_WITH_CONDITIONS"
    assert AggregateVerdict.BLOCKED == "BLOCKED"


def test_multiple_fail_still_blocked(engine):
    result = engine.evaluate([FAIL_VERDICT, FAIL_VERDICT])
    assert result.aggregate == AggregateVerdict.BLOCKED


def test_unknown_verdict_string_raises_value_error(engine):
    bad = {"persona": "Ghost", "law": "ENG-0.0", "verdict": "UNKNOWN", "note": ""}
    with pytest.raises(ValueError, match="UNKNOWN"):
        engine.evaluate([bad])


def test_missing_required_field_raises_key_error(engine):
    bad = {"persona": "Ghost", "law": "ENG-0.0", "note": "no verdict field"}
    with pytest.raises((KeyError, TypeError)):
        engine.evaluate([bad])
