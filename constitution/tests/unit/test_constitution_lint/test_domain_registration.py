"""Unit test for DomainRegistrationCompletenessRule (lint-law-integrity-checks/S3).

Verifies orphan authored laws (in .md but not in _domain.yaml) are reported
as FAIL severity.
"""

from pathlib import Path

import pytest

from aa_constitution_lint.domain.models import EvaluationResult
from aa_constitution_lint.domain.rules.constitution import DomainRegistrationCompletenessRule


@pytest.fixture()
def orphan_constitution(tmp_path: Path) -> Path:
    """Constitution where a .md file declares a law ID not in _domain.yaml."""
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
      - ENG-1.1  # Real Law
"""
    )

    (eng_dir / "foundations.md").write_text(
        """\
---
laws:
  - id: ENG-1.1
    title: Real Law
    summary: Registered.
---

# Article I — Foundations

## ENG-1.1: Real Law
"""
    )

    (eng_dir / "orphan-feature.md").write_text(
        """\
---
laws:
  - id: ENG-13.1
    title: Orphan Law
    summary: Not in any _domain.yaml article.
---

# Orphan Feature

## ENG-13.1: Orphan Law
"""
    )

    (laws_dir / "index.yaml").write_text("domains: [engineering]\n")
    return tmp_path


class TestDomainRegistrationCompletenessRule:
    """DomainRegistrationCompletenessRule must FAIL on orphan authored laws."""

    def test_orphan_law_is_fail_with_law_id(self, orphan_constitution: Path) -> None:
        rule = DomainRegistrationCompletenessRule()
        results = rule.evaluate(orphan_constitution)

        assert len(results) > 0, "Rule returned no evaluations"

        fail_results = [r for r in results if r.result == EvaluationResult.FAIL]
        assert len(fail_results) > 0, (
            f"Expected FAIL for orphan law, got: "
            f"{[(r.result.value, r.context.get('rule')) for r in results]}"
        )

        orphan_ids = [
            o.get("law_id")
            for r in fail_results
            for o in r.context.get("orphan_laws", [])
        ]
        assert "ENG-13.1" in orphan_ids, (
            f"Expected ENG-13.1 in orphan list, got: {orphan_ids}"
        )
