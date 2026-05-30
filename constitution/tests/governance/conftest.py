"""Shared fixtures for constitution governance tests.

Provides parsed views of the constitution's registry and law files so
individual tests don't each re-parse YAML.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from pathlib import Path

import pytest
import yaml

CONSTITUTION_ROOT = Path(__file__).resolve().parent.parent.parent
LAWS_DIR = CONSTITUTION_ROOT / "laws"

# Law-file frontmatter is a YAML block delimited by --- lines at the top.
FRONTMATTER_RE = re.compile(r"^---\n(.*?)\n---\n", re.DOTALL)


@dataclass(frozen=True)
class LawFileEntry:
    """One law declared in a law file's frontmatter."""

    id: str
    title: str
    non_negotiable: bool
    source_file: Path
    summary: str = ""


@dataclass(frozen=True)
class RegistryArticle:
    """One article in a domain's _domain.yaml."""

    roman: str
    title: str
    status: str  # "active" (default) | "deferred" | "delegated" | "draft" | "superseded"
    law_ids: tuple[str, ...]
    law_comments: dict[str, str] = field(default_factory=dict)
    source_file: Path = None


@dataclass(frozen=True)
class DomainRegistry:
    """Parsed _domain.yaml for one domain."""

    prefix: str
    domain: str
    articles: tuple[RegistryArticle, ...]
    non_negotiable_ids: tuple[str, ...]
    source_file: Path


def _parse_law_file(path: Path) -> list[LawFileEntry]:
    """Return all law entries declared in a law file's YAML frontmatter."""
    text = path.read_text(encoding="utf-8")
    match = FRONTMATTER_RE.match(text)
    if not match:
        return []
    front = yaml.safe_load(match.group(1)) or {}
    laws = front.get("laws") or []
    entries: list[LawFileEntry] = []
    for law in laws:
        if not isinstance(law, dict):
            continue
        entries.append(
            LawFileEntry(
                id=str(law.get("id", "")),
                title=str(law.get("title", "")),
                non_negotiable=bool(law.get("non_negotiable", False)),
                summary=str(law.get("summary", "")),
                source_file=path,
            )
        )
    return entries


def _parse_domain_registry(path: Path) -> DomainRegistry:
    """Parse a laws/<domain>/_domain.yaml file."""
    raw = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    articles_raw = raw.get("articles") or {}

    # Preserve the raw text so we can extract `# Comment` titles adjacent
    # to each law ID — those are the registry's human-readable titles.
    raw_text = path.read_text(encoding="utf-8").splitlines()

    articles: list[RegistryArticle] = []
    for roman, body in articles_raw.items():
        if not isinstance(body, dict):
            continue
        law_ids_raw = body.get("laws") or []
        law_ids = tuple(str(x) for x in law_ids_raw if isinstance(x, str))
        law_comments: dict[str, str] = {}
        # Scan raw text for each law ID and capture its trailing comment.
        for law_id in law_ids:
            for line in raw_text:
                if law_id in line and "#" in line:
                    comment = line.split("#", 1)[1].strip()
                    law_comments[law_id] = comment
                    break
        articles.append(
            RegistryArticle(
                roman=str(roman),
                title=str(body.get("title", "")),
                status=str(body.get("status", "active")),
                law_ids=law_ids,
                law_comments=law_comments,
                source_file=path,
            )
        )

    # Non-negotiable IDs can appear at article level or domain level.
    nn_ids: list[str] = []
    for roman, body in articles_raw.items():
        if isinstance(body, dict):
            nn_list = body.get("non_negotiable") or []
            if isinstance(nn_list, list):
                nn_ids.extend(str(x) for x in nn_list)

    return DomainRegistry(
        prefix=str(raw.get("prefix", "")),
        domain=str(raw.get("domain", "")),
        articles=tuple(articles),
        non_negotiable_ids=tuple(nn_ids),
        source_file=path,
    )


@pytest.fixture(scope="session")
def domain_registries() -> dict[str, DomainRegistry]:
    """All _domain.yaml files, keyed by domain name."""
    result: dict[str, DomainRegistry] = {}
    for domain_yaml in LAWS_DIR.glob("*/_domain.yaml"):
        reg = _parse_domain_registry(domain_yaml)
        result[reg.domain or domain_yaml.parent.name] = reg
    return result


@pytest.fixture(scope="session")
def law_files_by_domain() -> dict[str, list[LawFileEntry]]:
    """All law file frontmatter entries, grouped by domain directory name."""
    result: dict[str, list[LawFileEntry]] = {}
    for law_md in LAWS_DIR.glob("*/*.md"):
        domain = law_md.parent.name
        result.setdefault(domain, []).extend(_parse_law_file(law_md))
    return result


@pytest.fixture(scope="session")
def all_law_entries(law_files_by_domain) -> list[LawFileEntry]:
    """Flat list of every law declared in any law file."""
    out: list[LawFileEntry] = []
    for entries in law_files_by_domain.values():
        out.extend(entries)
    return out


@pytest.fixture(scope="session")
def law_id_to_entry(all_law_entries) -> dict[str, LawFileEntry]:
    """Map law ID to its law-file entry (authoritative source of truth)."""
    return {entry.id: entry for entry in all_law_entries if entry.id}
