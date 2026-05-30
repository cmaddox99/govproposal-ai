"""Correctness tests: assert the DESIRED state of the constitution.

Each test asserts a property that should hold of a healthy constitution.
These tests FAIL while drift exists and PASS once each bug is fixed.
The transition FAIL → PASS is the signal that an atomic fix landed.

Unlike pinning tests (which document current bugs and retire when fixed),
correctness tests are permanent. They become the regression-prevention
layer in CI once all current drift is resolved.

Correctness properties asserted:

  A. Registry-vs-law-file title coherence
     For every law ID declared in any _domain.yaml registry AND authored
     in a law file, the registry comment MUST contain the law file's
     frontmatter title (modulo trailing punctuation).

  B. Non-negotiable flag sync
     Every law whose frontmatter carries non_negotiable:true MUST also
     appear in its domain registry's non_negotiable list for the
     containing article.

  C. No unstatused phantom laws
     For every article in any registry, either
       (a) every declared ID has an authored law file, OR
       (b) the article carries status in {deferred, delegated, draft, superseded}.
     Articles that declare IDs without law files AND without a status
     field are phantoms — this is the failure mode that enabled the
     ENG-1.2 "Monetary Precision" hallucination.

  D. Broad schema — every authored law is registered
     Every law ID found in a law file's frontmatter MUST appear in its
     domain registry. Catches laws that get authored but never indexed.

  E. Broad schema — no law file entries outside declared articles
     Every law ID in a law file's frontmatter MUST appear in exactly
     one article's law list. Catches orphan authored laws that lost
     their article home.
"""

from __future__ import annotations

import re
from pathlib import Path

import pytest
import yaml

pytestmark = pytest.mark.correctness


LAWS_DIR = Path(__file__).resolve().parent.parent.parent / "laws"
FRONTMATTER_RE = re.compile(r"^---\n(.*?)\n---\n", re.DOTALL)


def _normalize_title(title: str) -> str:
    """Strip parenthetical suffixes like '(PNR 7 years)' and trailing punctuation."""
    t = re.sub(r"\s*\([^)]*\)\s*$", "", title).strip()
    return t.rstrip(".,;:")


def _title_matches_comment(law_file_title: str, registry_comment: str) -> bool:
    """Registry comment should contain (or equal) the law file's core title."""
    core = _normalize_title(law_file_title)
    comment_core = _normalize_title(registry_comment)
    if not core or not comment_core:
        return False
    return core.lower() in comment_core.lower() or comment_core.lower() in core.lower()


# ---------------------------------------------------------------------------
# A. Registry-vs-law-file title coherence
# ---------------------------------------------------------------------------


class TestTitleCoherence:
    """Every authored law must have a registry comment title that matches
    its law file frontmatter title."""

    def test_every_authored_law_has_matching_registry_title(
        self, domain_registries, law_id_to_entry
    ):
        mismatches: list[str] = []
        for registry in domain_registries.values():
            for article in registry.articles:
                for law_id in article.law_ids:
                    entry = law_id_to_entry.get(law_id)
                    if entry is None:
                        continue  # unauthored; covered by separate test
                    comment = article.law_comments.get(law_id, "")
                    if not _title_matches_comment(entry.title, comment):
                        mismatches.append(
                            f"  {law_id}: registry comment='{comment}' "
                            f"but law file title='{entry.title}'"
                        )
        assert not mismatches, (
            "Registry comments do not match law file titles. The law file is "
            "authoritative; update the registry comment.\n" + "\n".join(mismatches)
        )


# ---------------------------------------------------------------------------
# B. Non-negotiable flag sync
# ---------------------------------------------------------------------------


class TestNonNegotiableFlagSync:
    """Every law whose frontmatter has non_negotiable:true must appear in
    its domain registry's non_negotiable list for the containing article."""

    def test_non_negotiable_flag_propagates_to_registry(
        self, domain_registries, law_id_to_entry
    ):
        unsynced: list[str] = []
        for registry in domain_registries.values():
            registry_nn = set(registry.non_negotiable_ids)
            for article in registry.articles:
                for law_id in article.law_ids:
                    entry = law_id_to_entry.get(law_id)
                    if entry is None:
                        continue
                    if entry.non_negotiable and law_id not in registry_nn:
                        unsynced.append(
                            f"  {law_id}: non_negotiable:true in law file "
                            f"{entry.source_file.name} but not listed in "
                            f"{registry.source_file.name} Article {article.roman} "
                            f"non_negotiable set"
                        )
        assert not unsynced, (
            "Non-negotiable flag drift detected. Law file is authoritative; "
            "propagate to registry.\n" + "\n".join(unsynced)
        )


# ---------------------------------------------------------------------------
# C. No unstatused phantom laws
# ---------------------------------------------------------------------------


def _authored_law_ids_by_domain(domain_dir: Path) -> set[str]:
    ids: set[str] = set()
    for md in domain_dir.glob("*.md"):
        text = md.read_text(encoding="utf-8")
        m = FRONTMATTER_RE.match(text)
        if not m:
            continue
        front = yaml.safe_load(m.group(1)) or {}
        for law in front.get("laws") or []:
            if isinstance(law, dict) and "id" in law:
                ids.add(str(law["id"]))
    return ids


class TestNoUnstatusedPhantoms:
    """Every article must either author every declared law OR carry a status
    field acknowledging the gap (deferred, delegated, draft, superseded)."""

    VALID_STATUSES = {"deferred", "delegated", "draft", "superseded"}

    def test_articles_with_missing_law_files_must_be_statused(self, domain_registries):
        phantoms: list[str] = []
        for registry in domain_registries.values():
            domain_dir_name = registry.source_file.parent.name
            authored = _authored_law_ids_by_domain(LAWS_DIR / domain_dir_name)
            for article in registry.articles:
                missing = [lid for lid in article.law_ids if lid not in authored]
                if missing and article.status not in self.VALID_STATUSES:
                    phantoms.append(
                        f"  {registry.prefix} Article {article.roman} "
                        f"('{article.title}'): declares {len(missing)} law IDs with "
                        f"no law file and has no acknowledgement status. "
                        f"Missing: {missing}"
                    )
        assert not phantoms, (
            "Phantom laws detected — declared IDs with no law file AND no status "
            "field. Either author the laws or mark the article status:deferred "
            "(see DEFERRED_LAWS.md).\n" + "\n".join(phantoms)
        )


# ---------------------------------------------------------------------------
# D. Every authored law is registered somewhere
# ---------------------------------------------------------------------------


class TestEveryAuthoredLawIsRegistered:
    """A law file declaring an ID in frontmatter must have that ID listed
    in its domain's _domain.yaml article."""

    def test_no_authored_law_is_missing_from_registry(
        self, domain_registries, law_files_by_domain
    ):
        unregistered: list[str] = []
        for domain_dir_name, entries in law_files_by_domain.items():
            registry = None
            for r in domain_registries.values():
                if r.source_file.parent.name == domain_dir_name:
                    registry = r
                    break
            if registry is None:
                unregistered.append(
                    f"  Domain dir '{domain_dir_name}' has {len(entries)} law "
                    f"entries but no _domain.yaml registry"
                )
                continue
            registered_ids = {
                lid for article in registry.articles for lid in article.law_ids
            }
            for entry in entries:
                if entry.id and entry.id not in registered_ids:
                    unregistered.append(
                        f"  {entry.id}: authored in {entry.source_file.name} but "
                        f"not listed in {registry.source_file.name}"
                    )
        assert not unregistered, (
            "Authored laws missing from domain registry. Add them to the "
            "appropriate article.\n" + "\n".join(unregistered)
        )


# ---------------------------------------------------------------------------
# E. No authored law belongs to zero registry articles
# ---------------------------------------------------------------------------


class TestNoOrphanAuthoredLaws:
    """Every law file ID must appear in exactly one article's law list
    within its domain registry. Catches authored laws that lost their home."""

    def test_every_authored_law_belongs_to_one_article(
        self, domain_registries, all_law_entries
    ):
        orphans: list[str] = []
        duplicates: list[str] = []
        for entry in all_law_entries:
            if not entry.id:
                continue
            homes: list[str] = []
            for registry in domain_registries.values():
                for article in registry.articles:
                    if entry.id in article.law_ids:
                        homes.append(
                            f"{registry.prefix} Article {article.roman}"
                        )
            if len(homes) == 0:
                orphans.append(
                    f"  {entry.id}: authored in {entry.source_file.name} but "
                    f"not claimed by any article"
                )
            elif len(homes) > 1:
                duplicates.append(
                    f"  {entry.id}: claimed by {homes}"
                )
        messages = []
        if orphans:
            messages.append(
                "Orphan authored laws (no article home):\n" + "\n".join(orphans)
            )
        if duplicates:
            messages.append(
                "Laws claimed by multiple articles:\n" + "\n".join(duplicates)
            )
        assert not messages, "\n\n".join(messages)
