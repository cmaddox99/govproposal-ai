"""File, YAML, and schema checks S01 through S08b.

Each function returns a CheckItem — no exceptions raised, no side effects.
Fast-fail ordering (S01→S04) is enforced by the gate orchestrator (gate.py).

Laws: ENG-2.1 (modular), ENG-6.5 (safe_load only — AC-SEC-01)
Phase 3 §3 normative check register; Phase 4 §1.2 CheckItem contract.
"""
from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml

from aa_jury_gate.models import CheckItem, CheckResult, ToolError


# ── S01: file exists and is readable ─────────────────────────────────────────

def check_s01(path: Path) -> CheckItem:
    """S01 — file exists and path.is_file() (Phase 3 §3 Surface 1)."""
    if path.exists() and path.is_file():
        return CheckItem("S01", CheckResult.PASS, "")
    if not path.exists():
        return CheckItem("S01", CheckResult.FAIL, f"synthesis file not found: {path}")
    return CheckItem("S01", CheckResult.FAIL, f"synthesis path is a directory: {path}")


# ── S02: extension is .md / .yaml / .yml ─────────────────────────────────────

_ALLOWED_EXTENSIONS = {".md", ".yaml", ".yml"}


def check_s02(path: Path) -> CheckItem:
    """S02 — extension in {.md, .yaml, .yml} (Phase 3 §3 Surface 1)."""
    if path.suffix in _ALLOWED_EXTENSIONS:
        return CheckItem("S02", CheckResult.PASS, "")
    return CheckItem(
        "S02",
        CheckResult.FAIL,
        f"unsupported extension '{path.suffix}'; expected .md, .yaml, or .yml",
    )


# ── S03: file is valid YAML (yaml.safe_load) ─────────────────────────────────

def check_s03(content: str) -> CheckItem:
    """S03 — content parses as valid YAML via yaml.safe_load (AC-SEC-01).

    `content` is the extracted frontmatter YAML text (the string between the
    opening and closing '---' delimiters, NOT the raw full file content).
    gate.py must call extractor.parse() to extract frontmatter before calling
    this function. Passing raw .md file content is NOT supported.

    Raises ToolError on YAML parse failure per Phase 3 §1.3 (exit 2 — invocation error).
    """
    try:
        yaml.safe_load(content)
    except yaml.YAMLError as exc:
        raise ToolError(f"synthesis file is not valid YAML: {exc}") from exc
    return CheckItem("S03", CheckResult.PASS, "")


# ── S04: YAML root is a mapping ───────────────────────────────────────────────

def check_s04(parsed: Any) -> CheckItem:
    """S04 — parsed YAML root is a dict (Phase 3 §3 Surface 2)."""
    if isinstance(parsed, dict):
        return CheckItem("S04", CheckResult.PASS, "")
    type_name = type(parsed).__name__
    return CheckItem(
        "S04",
        CheckResult.FAIL,
        f"YAML root is a {type_name}; expected a mapping",
    )


# ── S05: schema_version == 1 ─────────────────────────────────────────────────

def check_s05(frontmatter: dict) -> CheckItem:
    """S05 — schema_version == 1 (Phase 3 §3 Surface 3)."""
    if "schema_version" not in frontmatter:
        return CheckItem("S05", CheckResult.FAIL, "field 'schema_version' is missing")
    actual = frontmatter["schema_version"]
    if actual == 1:
        return CheckItem("S05", CheckResult.PASS, "")
    return CheckItem(
        "S05",
        CheckResult.FAIL,
        f"schema_version is {actual}; expected 1",
    )


# ── S06: juror_count == 5 ────────────────────────────────────────────────────

def check_s06(frontmatter: dict) -> CheckItem:
    """S06 — juror_count == 5 (Phase 3 §3 Surface 3)."""
    if "juror_count" not in frontmatter:
        return CheckItem("S06", CheckResult.FAIL, "field 'juror_count' is missing")
    actual = frontmatter["juror_count"]
    if actual == 5:
        return CheckItem("S06", CheckResult.PASS, "")
    return CheckItem(
        "S06",
        CheckResult.FAIL,
        f"juror_count is {actual}; expected 5",
    )


# ── S07: jurors list has exactly 5 entries (hardcoded, NOT juror_count) ───────

def check_s07(frontmatter: dict) -> CheckItem:
    """S07 — len(jurors) == 5 (hardcoded constant per Phase 3 §3 C-P3-J2-001).

    If `jurors` is not a list (e.g., a dict or string), returns FAIL immediately
    with a type error detail (a non-list jurors field cannot contain 5 entries).
    """
    jurors = frontmatter.get("jurors", [])
    if not isinstance(jurors, list):
        return CheckItem(
            "S07",
            CheckResult.FAIL,
            f"jurors field must be a list; got {type(jurors).__name__}",
        )
    actual = len(jurors)
    if actual == 5:  # noqa: PLR2004
        return CheckItem("S07", CheckResult.PASS, "")
    return CheckItem(
        "S07",
        CheckResult.FAIL,
        f"jurors list has {actual} entries; expected 5",
    )


# ── S08a: all juror model values distinct (case-sensitive) ───────────────────

def check_s08a(frontmatter: dict) -> CheckItem:
    """S08a — all juror model strings are distinct (Phase 3 §3 C-P3-J2-002).

    Non-list `jurors` field: returns PASS (no models to compare; S07 catches the
    structural problem). Non-dict juror entries are skipped (isinstance guard).
    """
    jurors = frontmatter.get("jurors", [])
    if not isinstance(jurors, list):
        return CheckItem("S08a", CheckResult.PASS, "")
    models = [j.get("model", "") for j in jurors if isinstance(j, dict)]
    seen: set[str] = set()
    for model in models:
        if model in seen:
            return CheckItem(
                "S08a",
                CheckResult.FAIL,
                f"duplicate model: {model}",
            )
        seen.add(model)
    return CheckItem("S08a", CheckResult.PASS, "")


# ── S08b: no juror model equals "claude-haiku-4.5" ───────────────────────────

_PROHIBITED_MODEL = "claude-haiku-4.5"


def check_s08b(frontmatter: dict) -> CheckItem:
    """S08b — no juror uses claude-haiku-4.5 (Phase 3 §3 C-P3-J2-002).

    Non-list `jurors` field: returns PASS (no entries to check; S07 catches the
    structural problem). Non-dict juror entries are skipped (isinstance guard).
    """
    jurors = frontmatter.get("jurors", [])
    if not isinstance(jurors, list):
        return CheckItem("S08b", CheckResult.PASS, "")
    for j in jurors:
        if isinstance(j, dict) and j.get("model") == _PROHIBITED_MODEL:
            return CheckItem(
                "S08b",
                CheckResult.FAIL,
                f"prohibited model: {_PROHIBITED_MODEL}",
            )
    return CheckItem("S08b", CheckResult.PASS, "")


# ── S09–S11: Rounds & Verdict ─────────────────────────────────────────────────


def check_s09(frontmatter: dict) -> CheckItem:
    """S09 — rounds.r1_completed is True (Phase 3 §1.4).

    Uses `is True` (identity check) — YAML boolean `true` → Python `True`;
    `false`, absent key, string "true", int 1 all fail.
    If `rounds` is present but is not a dict (e.g. a string), treats
    r1_completed as absent → FAIL (no AttributeError raised).
    """
    rounds = frontmatter.get("rounds")
    completed = rounds.get("r1_completed") if isinstance(rounds, dict) else None
    if completed is True:
        return CheckItem("S09", CheckResult.PASS, "")
    return CheckItem("S09", CheckResult.FAIL, "rounds.r1_completed is false; expected true")


def check_s10(frontmatter: dict) -> CheckItem:
    """S10 — rounds.r2_completed is True (Phase 3 §1.4).

    Uses `is True` (identity check) — same rationale as S09.
    If `rounds` is present but is not a dict, treats r2_completed as absent → FAIL.
    """
    rounds = frontmatter.get("rounds")
    completed = rounds.get("r2_completed") if isinstance(rounds, dict) else None
    if completed is True:
        return CheckItem("S10", CheckResult.PASS, "")
    return CheckItem("S10", CheckResult.FAIL, "rounds.r2_completed is false; expected true")


def check_s11(frontmatter: dict) -> CheckItem:
    """S11 — verdict == "APPROVED" (Phase 3 §1.4).

    Case-sensitive equality. Any other value (including missing key → None)
    returns FAIL with `verdict is "<actual>"; gate requires "APPROVED"`.
    """
    actual = frontmatter.get("verdict")
    if actual == "APPROVED":
        return CheckItem("S11", CheckResult.PASS, "")
    return CheckItem(
        "S11",
        CheckResult.FAIL,
        f'verdict is "{actual}"; gate requires "APPROVED"',
    )
