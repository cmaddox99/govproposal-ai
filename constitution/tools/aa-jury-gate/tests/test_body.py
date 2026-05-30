"""Tests for body checks B01–B03 (Phase 3 §3 Surface 4).

B01: R1 section heading present in body
B02: R2 section heading present in body
B03: Synthesis/Final/Judicial section heading present in body

Laws: ENG-4.1 (TDD), ENG-4.6 (coverage ≥ 90%), ENG-4.11 (mutation ≥ 85%)
"""
from __future__ import annotations


from aa_jury_gate.checks.body import check_b01, check_b02, check_b03
from aa_jury_gate.models import CheckResult


# ── B01: R1 section heading ───────────────────────────────────────────────────

class TestCheckB01:
    def test_pass_round_1_heading(self) -> None:
        item = check_b01("## Round 1 Summary\n\nsome text")
        assert item.result == CheckResult.PASS
        assert item.check_id == "B01"
        assert item.detail == ""

    def test_pass_r1_colon(self) -> None:
        item = check_b01("## R1: Results\n\nsome text")
        assert item.result == CheckResult.PASS
        assert item.detail == ""

    def test_pass_r1_dash(self) -> None:
        item = check_b01("## R1 - Jury Findings\n\nsome text")
        assert item.result == CheckResult.PASS

    def test_pass_r1_end_of_line(self) -> None:
        item = check_b01("## R1\n\nsome text")
        assert item.result == CheckResult.PASS

    def test_pass_round_1_case_insensitive(self) -> None:
        item = check_b01("## round 1 summary\n\nsome text")
        assert item.result == CheckResult.PASS

    def test_fail_no_heading(self) -> None:
        item = check_b01("Some text without an R1 heading")
        assert item.result == CheckResult.FAIL
        assert item.check_id == "B01"
        assert item.detail == "R1 section heading not found in body"

    def test_fail_r10_does_not_match(self) -> None:
        # ## R10 must NOT match B01 — trailing digit blocks word boundary
        item = check_b01("## R10 Section\n\ntext")
        assert item.result == CheckResult.FAIL
        assert item.detail == "R1 section heading not found in body"

    def test_fail_r1_subsection_does_not_match(self) -> None:
        # ## R1.1 must NOT match — dot absent from trailing char class
        item = check_b01("## R1.1 Details\n\ntext")
        assert item.result == CheckResult.FAIL

    def test_fail_round_10_does_not_match(self) -> None:
        item = check_b01("## Round 10 heading\n\ntext")
        assert item.result == CheckResult.FAIL

    def test_fail_empty_body(self) -> None:
        item = check_b01("")
        assert item.result == CheckResult.FAIL

    def test_pass_heading_midway_in_body(self) -> None:
        body = "Intro text\n\n## Round 1\n\nJury findings"
        item = check_b01(body)
        assert item.result == CheckResult.PASS

    def test_fail_r1_inline_not_heading(self) -> None:
        # R1 appears in prose, not as ## heading
        item = check_b01("In round R1 results were discussed")
        assert item.result == CheckResult.FAIL

    def test_pass_r1_end_of_string_no_newline(self) -> None:
        # Exercises the $ zero-width branch (no trailing newline or whitespace)
        item = check_b01("## R1")
        assert item.result == CheckResult.PASS

    def test_pass_round_1_end_of_string_no_newline(self) -> None:
        item = check_b01("## Round 1")
        assert item.result == CheckResult.PASS


# ── B02: R2 section heading ───────────────────────────────────────────────────

class TestCheckB02:
    def test_pass_round_2_heading(self) -> None:
        item = check_b02("## Round 2 Summary\n\nsome text")
        assert item.result == CheckResult.PASS
        assert item.check_id == "B02"
        assert item.detail == ""

    def test_pass_r2_colon(self) -> None:
        item = check_b02("## R2: Results\n\nsome text")
        assert item.result == CheckResult.PASS

    def test_pass_r2_dash(self) -> None:
        item = check_b02("## R2 - Jury Findings\n\nsome text")
        assert item.result == CheckResult.PASS

    def test_pass_r2_end_of_line(self) -> None:
        item = check_b02("## R2\n\nsome text")
        assert item.result == CheckResult.PASS

    def test_pass_round_2_case_insensitive(self) -> None:
        item = check_b02("## ROUND 2 VERDICT\n\nsome text")
        assert item.result == CheckResult.PASS

    def test_fail_no_heading(self) -> None:
        item = check_b02("Some text without an R2 heading")
        assert item.result == CheckResult.FAIL
        assert item.check_id == "B02"
        assert item.detail == "R2 section heading not found in body"

    def test_fail_r20_does_not_match(self) -> None:
        item = check_b02("## R20 Section\n\ntext")
        assert item.result == CheckResult.FAIL

    def test_fail_r2_subsection_does_not_match(self) -> None:
        item = check_b02("## R2.1 Details\n\ntext")
        assert item.result == CheckResult.FAIL

    def test_fail_empty_body(self) -> None:
        item = check_b02("")
        assert item.result == CheckResult.FAIL

    def test_fail_r2_inline_not_heading(self) -> None:
        item = check_b02("Discussion of R2 results follows")
        assert item.result == CheckResult.FAIL

    def test_fail_round_20_does_not_match(self) -> None:
        item = check_b02("## Round 20 heading\n\ntext")
        assert item.result == CheckResult.FAIL

    def test_pass_r2_end_of_string_no_newline(self) -> None:
        # Exercises the $ zero-width branch
        item = check_b02("## R2")
        assert item.result == CheckResult.PASS


# ── B03: Synthesis/Final/Judicial section heading ────────────────────────────

class TestCheckB03:
    def test_pass_synthesis_heading(self) -> None:
        item = check_b03("## Synthesis\n\nsome text")
        assert item.result == CheckResult.PASS
        assert item.check_id == "B03"
        assert item.detail == ""

    def test_pass_final_heading(self) -> None:
        item = check_b03("## Final Verdict\n\nsome text")
        assert item.result == CheckResult.PASS

    def test_pass_judicial_heading(self) -> None:
        item = check_b03("## Judicial Summary\n\nsome text")
        assert item.result == CheckResult.PASS

    def test_pass_synthesis_colon(self) -> None:
        item = check_b03("## Synthesis: Result\n\nsome text")
        assert item.result == CheckResult.PASS

    def test_pass_final_dash(self) -> None:
        item = check_b03("## Final - Decision\n\nsome text")
        assert item.result == CheckResult.PASS

    def test_pass_judicial_end_of_line(self) -> None:
        item = check_b03("## Judicial\n\nsome text")
        assert item.result == CheckResult.PASS

    def test_pass_case_insensitive_synthesis(self) -> None:
        item = check_b03("## SYNTHESIS\n\nsome text")
        assert item.result == CheckResult.PASS

    def test_pass_case_insensitive_final(self) -> None:
        item = check_b03("## final verdict\n\nsome text")
        assert item.result == CheckResult.PASS

    def test_fail_no_heading(self) -> None:
        item = check_b03("Some text without a synthesis heading")
        assert item.result == CheckResult.FAIL
        assert item.check_id == "B03"
        assert item.detail == "synthesis section heading not found in body"

    def test_fail_empty_body(self) -> None:
        # BDD F04: body missing synthesis heading → B03 FAIL
        item = check_b03("")
        assert item.result == CheckResult.FAIL
        assert item.detail == "synthesis section heading not found in body"

    def test_fail_synthesis_inline_not_heading(self) -> None:
        item = check_b03("The synthesis of results is described below")
        assert item.result == CheckResult.FAIL

    def test_pass_all_three_present(self) -> None:
        body = "## Round 1\n\n## Round 2\n\n## Synthesis\n\ntext"
        item = check_b03(body)
        assert item.result == CheckResult.PASS

    def test_fail_judicial_subsection_does_not_match(self) -> None:
        # ## Judicial.1 — dot absent from trailing char class
        item = check_b03("## Judicial.1 Details\n\ntext")
        assert item.result == CheckResult.FAIL

    def test_pass_synthesis_end_of_string_no_newline(self) -> None:
        # Exercises the $ zero-width branch for B03
        item = check_b03("## Synthesis")
        assert item.result == CheckResult.PASS
