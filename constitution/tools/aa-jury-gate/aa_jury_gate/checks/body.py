"""Body checks B01–B03: section heading detection.

Operates on the body portion of a synthesis file (text after the closing ---
frontmatter delimiter). The gate orchestrator (gate.py) is responsible for
extracting the body and for SKIP logic (B01–B03 are skipped when S11 fails).

Laws: ENG-2.1 (modular), ENG-4.1 (TDD)
Phase 3 §3 Surface 4; Phase 4 §1.2 CheckItem contract.
"""
from __future__ import annotations

import re

from aa_jury_gate.models import CheckItem, CheckResult

# Compiled patterns — multiline + case-insensitive (Phase 3 §3 Surface 4)
_B01 = re.compile(r"^##\s+(Round\s+1|R1)(\s|:|-|$)", re.MULTILINE | re.IGNORECASE)
_B02 = re.compile(r"^##\s+(Round\s+2|R2)(\s|:|-|$)", re.MULTILINE | re.IGNORECASE)
_B03 = re.compile(r"^##\s+(Synthesis|Final|Judicial)(\s|:|-|$)", re.MULTILINE | re.IGNORECASE)


def check_b01(body: str) -> CheckItem:
    """B01 — body contains an R1 section heading (Phase 3 §3)."""
    if _B01.search(body):
        return CheckItem("B01", CheckResult.PASS, "")
    return CheckItem("B01", CheckResult.FAIL, "R1 section heading not found in body")


def check_b02(body: str) -> CheckItem:
    """B02 — body contains an R2 section heading (Phase 3 §3)."""
    if _B02.search(body):
        return CheckItem("B02", CheckResult.PASS, "")
    return CheckItem("B02", CheckResult.FAIL, "R2 section heading not found in body")


def check_b03(body: str) -> CheckItem:
    """B03 — body contains a Synthesis/Final/Judicial section heading (Phase 3 §3)."""
    if _B03.search(body):
        return CheckItem("B03", CheckResult.PASS, "")
    return CheckItem("B03", CheckResult.FAIL, "synthesis section heading not found in body")
