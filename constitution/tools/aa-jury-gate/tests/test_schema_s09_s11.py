"""VS-04: Tests for schema checks S09, S10, S11 (ENG-4.1)."""

from __future__ import annotations

from aa_jury_gate.checks.schema import check_s09, check_s10, check_s11
from aa_jury_gate.models import CheckResult


# ── S09: rounds.r1_completed is True ─────────────────────────────────────────

class TestS09:
    def test_pass_r1_true(self) -> None:
        item = check_s09({"rounds": {"r1_completed": True}})
        assert item.result == CheckResult.PASS
        assert item.detail == ""

    def test_fail_r1_false(self) -> None:
        item = check_s09({"rounds": {"r1_completed": False}})
        assert item.result == CheckResult.FAIL
        assert item.check_id == "S09"
        assert item.detail == "rounds.r1_completed is false; expected true"

    def test_fail_rounds_key_absent(self) -> None:
        item = check_s09({})
        assert item.result == CheckResult.FAIL
        assert item.check_id == "S09"
        assert item.detail == "rounds.r1_completed is false; expected true"

    def test_fail_r1_key_absent(self) -> None:
        item = check_s09({"rounds": {}})
        assert item.result == CheckResult.FAIL
        assert item.detail == "rounds.r1_completed is false; expected true"

    def test_fail_rounds_not_a_dict(self) -> None:
        # rounds is a string, not a dict → must FAIL, not raise AttributeError
        item = check_s09({"rounds": "completed"})
        assert item.result == CheckResult.FAIL
        assert item.check_id == "S09"

    def test_fail_r1_string_true(self) -> None:
        # string "true" is not bool True
        item = check_s09({"rounds": {"r1_completed": "true"}})
        assert item.result == CheckResult.FAIL

    def test_fail_r1_integer_1(self) -> None:
        # int 1 is not bool True (uses `is True` not `== True`)
        item = check_s09({"rounds": {"r1_completed": 1}})
        assert item.result == CheckResult.FAIL

    def test_check_id(self) -> None:
        assert check_s09({"rounds": {"r1_completed": True}}).check_id == "S09"

    def test_detail_exact_on_false(self) -> None:
        item = check_s09({"rounds": {"r1_completed": False}})
        assert item.detail.startswith("rounds.r1_completed is false")


# ── S10: rounds.r2_completed is True ─────────────────────────────────────────

class TestS10:
    def test_pass_r2_true(self) -> None:
        item = check_s10({"rounds": {"r2_completed": True}})
        assert item.result == CheckResult.PASS
        assert item.detail == ""

    def test_fail_r2_false(self) -> None:
        item = check_s10({"rounds": {"r2_completed": False}})
        assert item.result == CheckResult.FAIL
        assert item.check_id == "S10"
        assert item.detail == "rounds.r2_completed is false; expected true"

    def test_fail_rounds_key_absent(self) -> None:
        item = check_s10({})
        assert item.result == CheckResult.FAIL
        assert item.detail == "rounds.r2_completed is false; expected true"

    def test_fail_r2_key_absent(self) -> None:
        item = check_s10({"rounds": {}})
        assert item.result == CheckResult.FAIL
        assert item.detail == "rounds.r2_completed is false; expected true"

    def test_fail_rounds_not_a_dict(self) -> None:
        # rounds is a list, not a dict → must FAIL, not raise AttributeError
        item = check_s10({"rounds": ["r1", "r2"]})
        assert item.result == CheckResult.FAIL
        assert item.check_id == "S10"

    def test_fail_r2_string_true(self) -> None:
        item = check_s10({"rounds": {"r2_completed": "true"}})
        assert item.result == CheckResult.FAIL

    def test_fail_r2_integer_1(self) -> None:
        item = check_s10({"rounds": {"r2_completed": 1}})
        assert item.result == CheckResult.FAIL

    def test_check_id(self) -> None:
        assert check_s10({"rounds": {"r2_completed": True}}).check_id == "S10"

    def test_detail_exact_on_false(self) -> None:
        item = check_s10({"rounds": {"r2_completed": False}})
        assert item.detail.startswith("rounds.r2_completed is false")


# ── S11: verdict == "APPROVED" ────────────────────────────────────────────────

class TestS11:
    def test_pass_verdict_approved(self) -> None:
        item = check_s11({"verdict": "APPROVED"})
        assert item.result == CheckResult.PASS
        assert item.detail == ""

    def test_fail_verdict_needs_revision(self) -> None:
        item = check_s11({"verdict": "NEEDS_REVISION"})
        assert item.result == CheckResult.FAIL
        assert item.check_id == "S11"
        assert item.detail == 'verdict is "NEEDS_REVISION"; gate requires "APPROVED"'

    def test_fail_verdict_draft(self) -> None:
        item = check_s11({"verdict": "DRAFT"})
        assert item.result == CheckResult.FAIL
        assert item.detail == 'verdict is "DRAFT"; gate requires "APPROVED"'

    def test_fail_verdict_approved_lowercase(self) -> None:
        # case-sensitive: "approved" is not "APPROVED"
        item = check_s11({"verdict": "approved"})
        assert item.result == CheckResult.FAIL
        assert item.detail == 'verdict is "approved"; gate requires "APPROVED"'

    def test_fail_verdict_key_absent(self) -> None:
        item = check_s11({})
        assert item.result == CheckResult.FAIL
        assert item.check_id == "S11"
        assert "verdict" in item.detail

    def test_fail_verdict_none(self) -> None:
        item = check_s11({"verdict": None})
        assert item.result == CheckResult.FAIL

    def test_check_id(self) -> None:
        assert check_s11({"verdict": "APPROVED"}).check_id == "S11"

    def test_detail_names_actual_verdict(self) -> None:
        item = check_s11({"verdict": "PENDING"})
        assert "PENDING" in item.detail
        assert item.detail.startswith('verdict is "PENDING"')
