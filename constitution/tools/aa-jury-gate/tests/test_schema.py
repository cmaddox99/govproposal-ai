"""Tests for checks/schema.py — S01 through S08b.

Laws: ENG-4.1 (TDD), ENG-2.1 (modular), PRD-2.6 (jury)
Phase 3 §3 check register; Phase 5 §VS-03 test targets.
"""
from __future__ import annotations

from pathlib import Path

from aa_jury_gate.checks.schema import (
    check_s01,
    check_s02,
    check_s03,
    check_s04,
    check_s05,
    check_s06,
    check_s07,
    check_s08a,
    check_s08b,
)
from aa_jury_gate.models import CheckResult


# ── helpers ───────────────────────────────────────────────────────────────────

def _five_jurors(models: list[str] | None = None) -> list[dict]:
    default = [
        "claude-opus-4.6",
        "claude-sonnet-4.6",
        "gpt-5.4",
        "gpt-5.2",
        "gpt-5.4-mini",
    ]
    mods = models if models is not None else default
    return [{"id": f"J{i+1}", "model": m, "role": "Juror"} for i, m in enumerate(mods)]


def _valid_frontmatter() -> dict:
    return {
        "schema_version": 1,
        "juror_count": 5,
        "jurors": _five_jurors(),
    }


# ── S01: file exists and is readable ─────────────────────────────────────────

class TestS01:
    def test_pass_existing_file(self, tmp_path: Path) -> None:
        f = tmp_path / "synthesis.md"
        f.write_text("hello")
        item = check_s01(f)
        assert item.check_id == "S01"
        assert item.result == CheckResult.PASS

    def test_fail_nonexistent(self, tmp_path: Path) -> None:
        item = check_s01(tmp_path / "missing.md")
        assert item.result == CheckResult.FAIL
        assert item.check_id == "S01"
        assert item.detail.startswith("synthesis file not found")

    def test_fail_directory(self, tmp_path: Path) -> None:
        item = check_s01(tmp_path)
        assert item.result == CheckResult.FAIL
        assert item.check_id == "S01"
        assert item.detail.startswith("synthesis path is a directory")

    def test_detail_empty_on_pass(self, tmp_path: Path) -> None:
        f = tmp_path / "s.md"
        f.write_text("x")
        assert check_s01(f).detail == ""

    def test_detail_nonempty_on_fail(self, tmp_path: Path) -> None:
        item = check_s01(tmp_path / "gone.md")
        assert item.detail != ""


# ── S02: extension is .md / .yaml / .yml ─────────────────────────────────────

class TestS02:
    def test_pass_md(self, tmp_path: Path) -> None:
        item = check_s02(tmp_path / "s.md")
        assert item.result == CheckResult.PASS
        assert item.detail == ""

    def test_pass_yaml(self, tmp_path: Path) -> None:
        assert check_s02(tmp_path / "s.yaml").result == CheckResult.PASS

    def test_pass_yml(self, tmp_path: Path) -> None:
        assert check_s02(tmp_path / "s.yml").result == CheckResult.PASS

    def test_fail_txt(self, tmp_path: Path) -> None:
        item = check_s02(tmp_path / "s.txt")
        assert item.result == CheckResult.FAIL
        assert item.check_id == "S02"
        assert item.detail.startswith("unsupported extension")

    def test_fail_json(self, tmp_path: Path) -> None:
        assert check_s02(tmp_path / "s.json").result == CheckResult.FAIL

    def test_fail_no_extension(self, tmp_path: Path) -> None:
        assert check_s02(tmp_path / "synthesis").result == CheckResult.FAIL

    def test_check_id(self, tmp_path: Path) -> None:
        assert check_s02(tmp_path / "s.md").check_id == "S02"

    def test_detail_nonempty_on_fail(self, tmp_path: Path) -> None:
        assert check_s02(tmp_path / "s.txt").detail != ""


# ── S03: file is valid YAML ───────────────────────────────────────────────────

class TestS03:
    def test_pass_valid_yaml(self) -> None:
        item = check_s03("key: value\nother: 1\n")
        assert item.result == CheckResult.PASS
        assert item.detail == ""

    def test_fail_invalid_yaml(self) -> None:
        """Invalid YAML should raise ToolError (exit 2 per Phase 3 §1.3)."""
        import pytest
        from aa_jury_gate.models import ToolError

        with pytest.raises(ToolError, match="not valid YAML"):
            check_s03("key: [unclosed\n")

    def test_fail_tab_indented_yaml(self) -> None:
        """Tab-indented YAML should raise ToolError (exit 2 per Phase 3 §1.3)."""
        import pytest
        from aa_jury_gate.models import ToolError

        with pytest.raises(ToolError, match="not valid YAML"):
            check_s03("key:\n\tvalue\n")

    def test_pass_empty_string(self) -> None:
        # yaml.safe_load("") → None → valid (no document)
        item = check_s03("")
        assert item.result == CheckResult.PASS
        assert item.detail == ""

    def test_check_id(self) -> None:
        assert check_s03("x: 1").check_id == "S03"

    def test_detail_contains_error_on_fail(self) -> None:
        """Invalid YAML should raise ToolError with error message."""
        import pytest
        from aa_jury_gate.models import ToolError

        with pytest.raises(ToolError, match="not valid YAML"):
            check_s03(": bad yaml {{{")


# ── S04: YAML root is a mapping ───────────────────────────────────────────────

class TestS04:
    def test_pass_dict(self) -> None:
        item = check_s04({"key": "value"})
        assert item.result == CheckResult.PASS
        assert item.detail == ""

    def test_fail_list(self) -> None:
        item = check_s04(["a", "b"])
        assert item.result == CheckResult.FAIL
        assert item.check_id == "S04"
        assert item.detail.startswith("YAML root is a")

    def test_fail_none(self) -> None:
        assert check_s04(None).result == CheckResult.FAIL

    def test_fail_string(self) -> None:
        assert check_s04("hello").result == CheckResult.FAIL

    def test_fail_int(self) -> None:
        assert check_s04(42).result == CheckResult.FAIL

    def test_check_id(self) -> None:
        assert check_s04({}).check_id == "S04"

    def test_detail_includes_type_on_fail(self) -> None:
        item = check_s04(["x"])
        assert "list" in item.detail


# ── S05: schema_version == 1 ─────────────────────────────────────────────────

class TestS05:
    def test_pass_version_1(self) -> None:
        item = check_s05({"schema_version": 1})
        assert item.result == CheckResult.PASS
        assert item.detail == ""

    def test_fail_version_2(self) -> None:
        item = check_s05({"schema_version": 2})
        assert item.result == CheckResult.FAIL
        assert item.check_id == "S05"
        assert item.detail.startswith("schema_version is")
        assert "2" in item.detail
        assert "1" in item.detail

    def test_fail_missing_key(self) -> None:
        item = check_s05({})
        assert item.result == CheckResult.FAIL
        assert item.check_id == "S05"
        assert item.detail == "field 'schema_version' is missing"

    def test_fail_string_version(self) -> None:
        # string "1" is not equal to int 1; detail must NOT use repr quotes
        item = check_s05({"schema_version": "1"})
        assert item.result == CheckResult.FAIL
        assert item.detail == "schema_version is 1; expected 1"  # no repr quotes

    def test_check_id(self) -> None:
        assert check_s05({"schema_version": 1}).check_id == "S05"


# ── S06: juror_count == 5 ────────────────────────────────────────────────────

class TestS06:
    def test_pass_count_5(self) -> None:
        item = check_s06({"juror_count": 5})
        assert item.result == CheckResult.PASS
        assert item.detail == ""

    def test_fail_count_4(self) -> None:
        item = check_s06({"juror_count": 4})
        assert item.result == CheckResult.FAIL
        assert item.check_id == "S06"
        assert item.detail.startswith("juror_count is")
        assert "4" in item.detail
        assert "5" in item.detail

    def test_fail_missing_key(self) -> None:
        item = check_s06({})
        assert item.result == CheckResult.FAIL
        assert item.check_id == "S06"
        assert item.detail == "field 'juror_count' is missing"

    def test_check_id(self) -> None:
        assert check_s06({"juror_count": 5}).check_id == "S06"


# ── S07: jurors list has exactly 5 entries (hardcoded, NOT juror_count) ───────

class TestS07:
    def test_pass_five_jurors(self) -> None:
        item = check_s07({"jurors": _five_jurors()})
        assert item.result == CheckResult.PASS
        assert item.detail == ""

    def test_fail_four_jurors(self) -> None:
        item = check_s07({"jurors": _five_jurors()[:4]})
        assert item.result == CheckResult.FAIL
        assert item.check_id == "S07"
        assert item.detail.startswith("jurors list has")
        assert "4" in item.detail
        assert "5" in item.detail

    def test_fail_six_jurors(self) -> None:
        item = check_s07({"jurors": _five_jurors() + [{"id": "J6", "model": "x"}]})
        assert item.result == CheckResult.FAIL

    def test_fail_missing_jurors_key(self) -> None:
        item = check_s07({})
        assert item.result == CheckResult.FAIL
        assert "0" in item.detail  # 0 entries found

    def test_hardcoded_not_juror_count(self) -> None:
        # juror_count=3 but jurors list has 5 → S07 PASS (uses hardcoded 5)
        fm = {"juror_count": 3, "jurors": _five_jurors()}
        assert check_s07(fm).result == CheckResult.PASS

    def test_fail_jurors_not_a_list(self) -> None:
        # jurors is a dict (malformed) → must FAIL, not PASS via len()
        item = check_s07({"jurors": {"key": "value"}})
        assert item.result == CheckResult.FAIL
        assert item.check_id == "S07"
        assert item.detail.startswith("jurors field must be a list")

    def test_fail_jurors_string_of_length_5(self) -> None:
        # jurors is a 5-char string → len("abcde")==5 but it's not a list → FAIL
        item = check_s07({"jurors": "abcde"})
        assert item.result == CheckResult.FAIL

    def test_check_id(self) -> None:
        assert check_s07({"jurors": _five_jurors()}).check_id == "S07"


# ── S08a: all juror model values distinct (case-sensitive) ───────────────────

class TestS08a:
    def test_pass_all_distinct(self) -> None:
        item = check_s08a({"jurors": _five_jurors()})
        assert item.result == CheckResult.PASS
        assert item.detail == ""

    def test_fail_duplicate(self) -> None:
        models = ["claude-opus-4.6", "claude-opus-4.6", "gpt-5.4", "gpt-5.2", "gpt-5.4-mini"]
        item = check_s08a({"jurors": _five_jurors(models)})
        assert item.result == CheckResult.FAIL
        assert item.check_id == "S08a"
        assert "claude-opus-4.6" in item.detail
        assert "duplicate" in item.detail

    def test_case_sensitive(self) -> None:
        # "GPT-5.4" and "gpt-5.4" are distinct (case-sensitive)
        models = ["claude-opus-4.6", "claude-sonnet-4.6", "GPT-5.4", "gpt-5.4", "gpt-5.2"]
        assert check_s08a({"jurors": _five_jurors(models)}).result == CheckResult.PASS

    def test_fail_missing_jurors(self) -> None:
        # No jurors key → 0 entries → no duplicates → PASS
        assert check_s08a({}).result == CheckResult.PASS

    def test_pass_jurors_not_a_list(self) -> None:
        # non-list jurors → S07 catches the structure; S08a defers → PASS
        item = check_s08a({"jurors": {"key": "val"}})
        assert item.result == CheckResult.PASS
        assert item.check_id == "S08a"
        assert item.detail == ""

    def test_check_id(self) -> None:
        assert check_s08a({"jurors": _five_jurors()}).check_id == "S08a"

    def test_detail_names_duplicate_model(self) -> None:
        models = ["m1", "m2", "m1", "m3", "m4"]
        item = check_s08a({"jurors": _five_jurors(models)})
        assert "m1" in item.detail

    def test_fail_jurors_missing_model_key(self) -> None:
        # Two jurors with no "model" key → both yield "" → detected as duplicate
        jurors = [{"id": f"J{i}"} for i in range(1, 6)]
        item = check_s08a({"jurors": jurors})
        assert item.result == CheckResult.FAIL
        # detail must contain the empty-string duplicate, not "XXXX"
        assert item.detail == "duplicate model: "


class TestS08b:
    def test_pass_no_haiku(self) -> None:
        item = check_s08b({"jurors": _five_jurors()})
        assert item.result == CheckResult.PASS
        assert item.detail == ""

    def test_fail_haiku_present(self) -> None:
        models = [
            "claude-opus-4.6", "claude-sonnet-4.6", "claude-haiku-4.5",
            "gpt-5.2", "gpt-5.4-mini",
        ]
        item = check_s08b({"jurors": _five_jurors(models)})
        assert item.result == CheckResult.FAIL
        assert item.check_id == "S08b"
        assert item.detail.startswith("prohibited model")

    def test_case_sensitive_no_false_positive(self) -> None:
        # "Claude-Haiku-4.5" is NOT the prohibited model (case-sensitive)
        models = ["Claude-Haiku-4.5", "claude-sonnet-4.6", "gpt-5.4", "gpt-5.2", "gpt-5.4-mini"]
        assert check_s08b({"jurors": _five_jurors(models)}).result == CheckResult.PASS

    def test_pass_no_jurors_key(self) -> None:
        assert check_s08b({}).result == CheckResult.PASS

    def test_pass_jurors_not_a_list(self) -> None:
        # non-list jurors → S07 catches the structure; S08b defers → PASS
        item = check_s08b({"jurors": {"key": "val"}})
        assert item.result == CheckResult.PASS
        assert item.check_id == "S08b"
        assert item.detail == ""

    def test_check_id(self) -> None:
        assert check_s08b({"jurors": _five_jurors()}).check_id == "S08b"

    def test_detail_names_prohibited_on_fail(self) -> None:
        models = ["claude-haiku-4.5", "claude-sonnet-4.6", "gpt-5.4", "gpt-5.2", "gpt-5.4-mini"]
        item = check_s08b({"jurors": _five_jurors(models)})
        assert "prohibited" in item.detail
        assert "claude-haiku-4.5" in item.detail
