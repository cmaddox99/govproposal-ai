"""Shared parser for _domain.yaml and .md law files.

Provides cached parsing used by LawTitleCoherenceRule, LawBodyExistenceRule,
and DomainRegistrationCompletenessRule. Extracts _domain.yaml article structure
(including inline # comment titles via line-anchored regex) and .md frontmatter
law entries.

Per lint-law-integrity-checks/D1: this is a performance requirement — all three
rules share a single parse per lint run.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from functools import lru_cache
from pathlib import Path

import yaml

FRONTMATTER_RE = re.compile(r"^---\n(.*?)\n---\n", re.DOTALL)
VALID_DEFERRED_STATUSES = frozenset({"deferred", "delegated", "draft", "superseded"})


@dataclass(frozen=True)
class LawFileEntry:
    """One law declared in a .md file's YAML frontmatter."""

    id: str
    title: str
    source_file: Path


@dataclass(frozen=True)
class RegistryArticle:
    """One article in a domain's _domain.yaml."""

    roman: str
    title: str
    status: str  # "active" (default) | deferred | delegated | draft | superseded
    law_ids: tuple[str, ...]
    law_comments: dict[str, str] = field(default_factory=dict)


@dataclass(frozen=True)
class DomainRegistry:
    """Parsed _domain.yaml for one domain."""

    prefix: str
    domain: str
    articles: tuple[RegistryArticle, ...]
    source_file: Path


def parse_law_file_entries(path: Path) -> list[LawFileEntry]:
    """Return all law entries from a .md file's YAML frontmatter."""
    text = path.read_text(encoding="utf-8")
    match = FRONTMATTER_RE.match(text)
    if not match:
        return []
    front = yaml.safe_load(match.group(1)) or {}
    laws = front.get("laws") or []
    return [
        LawFileEntry(
            id=str(law["id"]),
            title=str(law.get("title", "")),
            source_file=path,
        )
        for law in laws
        if isinstance(law, dict) and "id" in law
    ]


def parse_domain_yaml(path: Path) -> DomainRegistry:
    """Parse a _domain.yaml, extracting articles with law_ids and comment titles.

    Uses a line-anchored regex to extract inline ``# Comment`` titles, avoiding
    false matches from unrelated YAML comments.
    """
    raw_text = path.read_text(encoding="utf-8")
    raw = yaml.safe_load(raw_text) or {}
    raw_lines = raw_text.splitlines()
    articles_raw = raw.get("articles") or {}

    articles: list[RegistryArticle] = []
    for roman, body in articles_raw.items():
        if not isinstance(body, dict):
            continue
        law_ids = tuple(str(x) for x in (body.get("laws") or []) if isinstance(x, str))
        law_comments: dict[str, str] = {}
        for law_id in law_ids:
            pattern = re.compile(
                rf'^\s*-\s*["\']?{re.escape(law_id)}["\']?\s*#\s*(.*)$'
            )
            for line in raw_lines:
                m = pattern.match(line)
                if m:
                    law_comments[law_id] = m.group(1).strip()
                    break
        articles.append(RegistryArticle(
            roman=str(roman),
            title=str(body.get("title", "")),
            status=str(body.get("status", "active")),
            law_ids=law_ids,
            law_comments=law_comments,
        ))

    return DomainRegistry(
        prefix=str(raw.get("prefix", "")),
        domain=str(raw.get("domain", "")),
        articles=tuple(articles),
        source_file=path,
    )


def normalize_title(title: str) -> str:
    """Strip parenthetical suffixes and trailing punctuation for comparison."""
    t = re.sub(r"\s*\([^)]*\)\s*$", "", title).strip()
    return t.rstrip(".,;:")


def title_matches_comment(law_file_title: str, registry_comment: str) -> bool:
    """Registry comment should contain (or equal) the law file's core title."""
    core = normalize_title(law_file_title)
    comment_core = normalize_title(registry_comment)
    if not core or not comment_core:
        return False
    return core.lower() in comment_core.lower() or comment_core.lower() in core.lower()


class ConstitutionData:
    """Cached parsed view of a constitution's laws/ directory.

    Instantiate once per lint run and pass to all integrity rules.
    """

    def __init__(self, laws_dir: Path) -> None:
        self._laws_dir = laws_dir
        self._registries: list[DomainRegistry] | None = None
        self._law_file_titles: dict[str, str] | None = None
        self._law_file_ids_by_domain: dict[str, set[str]] | None = None

    @property
    def registries(self) -> list[DomainRegistry]:
        if self._registries is None:
            self._registries = [
                parse_domain_yaml(p)
                for p in sorted(self._laws_dir.glob("*/_domain.yaml"))
            ]
        return self._registries

    @property
    def law_file_titles(self) -> dict[str, str]:
        """Map law_id -> frontmatter title across all .md files."""
        if self._law_file_titles is None:
            self._law_file_titles = {}
            for md_file in self._laws_dir.glob("*/*.md"):
                for entry in parse_law_file_entries(md_file):
                    if entry.id and entry.title:
                        self._law_file_titles[entry.id] = entry.title
        return self._law_file_titles

    @property
    def law_file_ids_by_domain_dir(self) -> dict[str, set[str]]:
        """Map domain dir name -> set of law IDs from .md frontmatter."""
        if self._law_file_ids_by_domain is None:
            self._law_file_ids_by_domain = {}
            for md_file in self._laws_dir.glob("*/*.md"):
                domain_name = md_file.parent.name
                ids = self._law_file_ids_by_domain.setdefault(domain_name, set())
                for entry in parse_law_file_entries(md_file):
                    if entry.id:
                        ids.add(entry.id)
        return self._law_file_ids_by_domain
