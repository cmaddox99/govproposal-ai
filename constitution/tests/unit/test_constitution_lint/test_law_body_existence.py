"""Unit test for LawBodyExistenceRule (lint-law-integrity-checks/S2).

Verifies phantom articles (no .md body, no status) are reported as FAIL severity,
and deferred articles are tolerated as PASS.
"""

from pathlib import Path

import pytest

from aa_constitution_lint.domain.models import EvaluationResult
from aa_constitution_lint.domain.rules.constitution import LawBodyExistenceRule


@pytest.fixture()
def phantom_constitution(tmp_path: Path) -> Path:
    """Constitution with an article declaring law IDs that have no .md body
    and no status field — an unstatused phantom."""
    laws_dir = tmp_path / "laws"
    eng_dir = laws_dir / "engineering"
    eng_dir.mkdir(parents=True)

    # _domain.yaml declares ENG-8.1 and ENG-8.2 in Article VIII,
    # but no .md file will contain these IDs, and no status field is set.
    (eng_dir / "_domain.yaml").write_text(
        """\
domain: engineering
prefix: ENG
articles:
  I:
    title: Foundations
    laws:
      - ENG-1.1  # Real Law
  VIII:
    title: Phantom Article
    laws:
      - ENG-8.1  # Phantom Law A
      - ENG-8.2  # Phantom Law B
"""
    )

    # Only ENG-1.1 has a .md body
    (eng_dir / "foundations.md").write_text(
        """\
---
laws:
  - id: ENG-1.1
    title: Real Law
    summary: This one exists.
---

# Article I — Foundations

## ENG-1.1: Real Law
"""
    )

    (laws_dir / "index.yaml").write_text("domains: [engineering]\n")
    return tmp_path


@pytest.fixture()
def deferred_constitution(tmp_path: Path) -> Path:
    """Constitution where the phantom article has status:deferred — should PASS."""
    laws_dir = tmp_path / "laws"
    eng_dir = laws_dir / "engineering"
    eng_dir.mkdir(parents=True)

    (eng_dir / "_domain.yaml").write_text(
        """\
domain: engineering
prefix: ENG
articles:
  VIII:
    title: Deferred Article
    status: deferred
    laws:
      - ENG-8.1  # Deferred Law
"""
    )

    (laws_dir / "index.yaml").write_text("domains: [engineering]\n")
    return tmp_path


class TestLawBodyExistenceRule:
    """LawBodyExistenceRule must detect unstatused phantom articles."""

    def test_detects_unstatused_phantom_article(self, phantom_constitution: Path) -> None:
        rule = LawBodyExistenceRule()
        results = rule.evaluate(phantom_constitution)

        assert len(results) > 0, "Rule returned no evaluations"

        fail_results = [r for r in results if r.result == EvaluationResult.FAIL]
        assert len(fail_results) > 0, (
            f"Expected FAIL for phantom article, got: "
            f"{[(r.result.value, r.context.get('rule')) for r in results]}"
        )

        phantom_articles = [
            p.get("article")
            for r in fail_results
            for p in r.context.get("phantom_articles", [])
        ]
        assert "Article VIII" in phantom_articles, (
            f"Expected Article VIII in phantom list, got: {phantom_articles}"
        )

    def test_tolerates_deferred_article(self, deferred_constitution: Path) -> None:
        rule = LawBodyExistenceRule()
        results = rule.evaluate(deferred_constitution)

        assert len(results) > 0, "Rule returned no evaluations"

        # Should be PASS — deferred articles are acknowledged
        pass_results = [r for r in results if r.result == EvaluationResult.PASS]
        assert len(pass_results) > 0, (
            f"Expected PASS for deferred article, got: "
            f"{[(r.result, r.context) for r in results]}"
        )
