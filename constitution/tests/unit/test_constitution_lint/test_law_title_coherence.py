"""Unit test for LawTitleCoherenceRule (lint-law-integrity-checks/S1).

Verifies title mismatches between _domain.yaml comments and .md frontmatter
are reported as FAIL severity.
"""

from pathlib import Path

import pytest

from aa_constitution_lint.domain.models import EvaluationResult
from aa_constitution_lint.domain.rules.constitution import LawTitleCoherenceRule


@pytest.fixture()
def mismatched_constitution(tmp_path: Path) -> Path:
    """Minimal constitution with a title mismatch between _domain.yaml and .md."""
    laws_dir = tmp_path / "laws"
    eng_dir = laws_dir / "engineering"
    eng_dir.mkdir(parents=True)

    (eng_dir / "_domain.yaml").write_text(
        """\
domain: engineering
prefix: ENG
articles:
  I:
    title: Foundations
    laws:
      - ENG-1.1  # Wrong Title Law
"""
    )

    (eng_dir / "foundations.md").write_text(
        """\
---
laws:
  - id: ENG-1.1
    title: Correct Title Law
    summary: A test law.
---

# Article I — Foundations

## ENG-1.1: Correct Title Law
"""
    )

    (laws_dir / "index.yaml").write_text("domains: [engineering]\n")

    return tmp_path


class TestLawTitleCoherenceRule:
    """LawTitleCoherenceRule must FAIL on _domain.yaml vs .md title drift."""

    def test_title_mismatch_is_fail_with_law_id(self, mismatched_constitution: Path) -> None:
        rule = LawTitleCoherenceRule()
        results = rule.evaluate(mismatched_constitution)

        assert len(results) > 0, "Rule returned no evaluations"

        fail_results = [r for r in results if r.result == EvaluationResult.FAIL]
        assert len(fail_results) > 0, (
            f"Expected FAIL for title mismatch, got: "
            f"{[(r.result.value, r.context.get('rule')) for r in results]}"
        )

        mismatched_ids = [
            m.get("law_id")
            for r in fail_results
            for m in r.context.get("mismatches", [])
        ]
        assert "ENG-1.1" in mismatched_ids, (
            f"Expected ENG-1.1 in mismatch list, got: {mismatched_ids}"
        )
