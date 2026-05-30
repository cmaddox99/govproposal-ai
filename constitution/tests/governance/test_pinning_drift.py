"""Pinning tests: document the current (buggy) state of the constitution.

Each test asserts that a known drift/bug currently EXISTS. Pinning tests
PASS while the bug is live and FAIL once the bug is fixed.

The correct response to a failing pinning test is:
  1. Confirm the corresponding bug was actually fixed.
  2. Delete (or skip with a TODO) the pinning test.
  3. Verify the matching correctness test in test_correctness_*.py now passes.

Do not modify these tests to keep them passing. That would defeat the
point of the TDD cycle — they're here to prove fixes took effect.

14 documented drift issues are pinned here:
  - 8 title mismatches (BUS-3.2 through BUS-3.5; ENG-10.1 through ENG-10.4)
  - 1 non-negotiable flag sync failure (ENG-10.1)
  - 5 orphan articles (Business V, VIII; Product VII, VIII, IX) — pinned
    in their current status:deferred state with no corresponding law file
"""

from __future__ import annotations

from pathlib import Path

import pytest

pytestmark = pytest.mark.pinning


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _article_by_roman(registry, roman: str):
    for article in registry.articles:
        if article.roman == roman:
            return article
    return None


def _comment_for(registry, law_id: str) -> str:
    """Return the registry's human-readable comment title for a given law ID."""
    for article in registry.articles:
        if law_id in article.law_comments:
            return article.law_comments[law_id]
    return ""


# ---------------------------------------------------------------------------
# Business Article III — Data Governance Laws: 4 title mismatches — RETIRED
# Title drift fixed in law-registry-reconciliation/S1
# ---------------------------------------------------------------------------


# ---------------------------------------------------------------------------
# Engineering Article X — Constitution Governance: 4 title mismatches — RETIRED
# Title drift fixed in law-registry-reconciliation/S1
# ---------------------------------------------------------------------------


# ---------------------------------------------------------------------------
# Non-negotiable flag sync failure — RETIRED
# NN flag sync fixed in law-registry-reconciliation/S4
# ---------------------------------------------------------------------------


# ---------------------------------------------------------------------------
# Orphan articles — currently labeled status:deferred with no law file
# ---------------------------------------------------------------------------


class TestOrphanArticlesPinnedAsDeferred:
    """Five articles were declared without ever being authored. A prior commit
    labeled them status:deferred to make the state honest. These pinning tests
    assert that labeling is in place AND no law file exists for any declared ID.

    Resolution paths per DEFERRED_LAWS.md: DELEGATE (pointer to external AA
    policy), AUTHOR (write real law text), DELETE (remove from registry). Each
    resolution will flip the relevant pinning test.
    """

    LAWS_DIR = Path(__file__).resolve().parent.parent.parent / "laws"

    def _no_law_file_for(self, law_ids, domain_dir):
        """Return law IDs that have no matching frontmatter entry in any .md file."""
        import re
        import yaml

        FM = re.compile(r"^---\n(.*?)\n---\n", re.DOTALL)
        ids_in_files = set()
        for md in (self.LAWS_DIR / domain_dir).glob("*.md"):
            text = md.read_text(encoding="utf-8")
            m = FM.match(text)
            if not m:
                continue
            front = yaml.safe_load(m.group(1)) or {}
            for law in front.get("laws") or []:
                if isinstance(law, dict) and "id" in law:
                    ids_in_files.add(str(law["id"]))
        return [lid for lid in law_ids if lid not in ids_in_files]

    def test_pinning_business_article_v_security_governance_is_deferred(self, domain_registries):
        article = _article_by_roman(domain_registries["business"], "V")
        assert article is not None, "Business Article V should exist in registry"
        assert article.status == "deferred", (
            f"Pinning broken: Business Article V status changed to {article.status!r}. "
            f"If authored/delegated/deleted, retire this test."
        )
        missing = self._no_law_file_for(article.law_ids, "business")
        assert missing == list(article.law_ids), (
            f"Pinning broken: some BUS-5.x IDs now have law files: "
            f"{set(article.law_ids) - set(missing)}. Retire if authoring began."
        )

    def test_pinning_business_article_viii_vendor_third_party_is_deferred(self, domain_registries):
        article = _article_by_roman(domain_registries["business"], "VIII")
        assert article is not None, "Business Article VIII should exist in registry"
        assert article.status == "deferred", (
            f"Pinning broken: Business Article VIII status changed to {article.status!r}. "
            f"If authored/delegated/deleted, retire this test."
        )
        missing = self._no_law_file_for(article.law_ids, "business")
        assert missing == list(article.law_ids), (
            f"Pinning broken: some BUS-8.x IDs now have law files: "
            f"{set(article.law_ids) - set(missing)}."
        )

    def test_pinning_product_article_vii_prioritization_is_deferred(self, domain_registries):
        article = _article_by_roman(domain_registries["product"], "VII")
        assert article is not None, "Product Article VII should exist in registry"
        assert article.status == "deferred", (
            f"Pinning broken: Product Article VII status changed to {article.status!r}. "
            f"If authored/delegated/deleted, retire this test."
        )
        missing = self._no_law_file_for(article.law_ids, "product")
        assert missing == list(article.law_ids), (
            f"Pinning broken: some PRD-7.x IDs now have law files: "
            f"{set(article.law_ids) - set(missing)}."
        )

    def test_pinning_product_article_viii_metrics_analytics_is_deferred(self, domain_registries):
        article = _article_by_roman(domain_registries["product"], "VIII")
        assert article is not None, "Product Article VIII should exist in registry"
        assert article.status == "deferred", (
            f"Pinning broken: Product Article VIII status changed to {article.status!r}. "
            f"If authored/delegated/deleted, retire this test."
        )
        missing = self._no_law_file_for(article.law_ids, "product")
        assert missing == list(article.law_ids), (
            f"Pinning broken: some PRD-8.x IDs now have law files: "
            f"{set(article.law_ids) - set(missing)}."
        )

    def test_pinning_product_article_ix_stakeholder_comm_is_deferred(self, domain_registries):
        article = _article_by_roman(domain_registries["product"], "IX")
        assert article is not None, "Product Article IX should exist in registry"
        assert article.status == "deferred", (
            f"Pinning broken: Product Article IX status changed to {article.status!r}. "
            f"If authored/delegated/deleted, retire this test."
        )
        missing = self._no_law_file_for(article.law_ids, "product")
        assert missing == list(article.law_ids), (
            f"Pinning broken: some PRD-9.x IDs now have law files: "
            f"{set(article.law_ids) - set(missing)}."
        )
