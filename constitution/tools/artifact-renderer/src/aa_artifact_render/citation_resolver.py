"""
citation_resolver.py — Law citation lookup and tooltip metadata provider.

Walks the constitution's laws/ directory, parses each law file's YAML
frontmatter to build an in-memory index keyed by law ID, then resolves
individual citation IDs to title, summary, and non-negotiable flag.

The index is built lazily on the first call to resolve() and cached for
the lifetime of the CitationResolver instance.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import yaml


# ---------------------------------------------------------------------------
# Data classes
# ---------------------------------------------------------------------------

@dataclass
class ResolvedCitation:
    """Tooltip metadata for a single law citation."""
    law_id: str
    found: bool
    title: str = ""
    summary: str = ""
    non_negotiable: bool = False


# ---------------------------------------------------------------------------
# Resolver
# ---------------------------------------------------------------------------

class CitationResolver:
    """
    Resolves law IDs to tooltip metadata by reading the constitution laws/ directory.

    Args:
        laws_dir: Explicit path to the laws/ directory. When None, auto-detects
                  by walking up from the current working directory looking for a
                  laws/ subdirectory that contains at least one domain folder.
    """

    def __init__(self, laws_dir: Path | None = None) -> None:
        self._laws_dir: Path | None = laws_dir if laws_dir is not None else self._auto_detect()
        self._index: dict[str, ResolvedCitation] | None = None

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def resolve(self, law_id: str) -> ResolvedCitation:
        """
        Return tooltip metadata for the given law ID.

        Always returns a ResolvedCitation — never raises. When the law ID is
        not found, returns a ResolvedCitation with found=False and empty fields.
        """
        if self._index is None:
            self._index = self._build_index()

        return self._index.get(law_id, ResolvedCitation(law_id=law_id, found=False))

    # ------------------------------------------------------------------
    # Index building
    # ------------------------------------------------------------------

    def _build_index(self) -> dict[str, ResolvedCitation]:
        """Parse all law .md files and return a dict keyed by law ID."""
        index: dict[str, ResolvedCitation] = {}

        if self._laws_dir is None or not self._laws_dir.is_dir():
            return index

        for law_file in sorted(self._laws_dir.rglob("*.md")):
            try:
                self._parse_law_file(law_file, index)
            except Exception:
                # Never fail on a single unreadable file
                continue

        return index

    def _parse_law_file(self, path: Path, index: dict[str, ResolvedCitation]) -> None:
        """Extract all law definitions from a single law .md file into index."""
        text = path.read_text(encoding="utf-8")
        frontmatter = _extract_frontmatter(text)
        if not frontmatter or "laws" not in frontmatter:
            return

        laws_list = frontmatter.get("laws", [])
        if not isinstance(laws_list, list):
            return

        for law_entry in laws_list:
            if not isinstance(law_entry, dict):
                continue
            law_id = law_entry.get("id", "").strip()
            if not law_id:
                continue
            index[law_id] = ResolvedCitation(
                law_id=law_id,
                found=True,
                title=str(law_entry.get("title", "")),
                summary=str(law_entry.get("summary", "")),
                non_negotiable=bool(law_entry.get("non_negotiable", False)),
            )

    # ------------------------------------------------------------------
    # Auto-detection
    # ------------------------------------------------------------------

    @staticmethod
    def _auto_detect() -> Path | None:
        """
        Walk up from CWD looking for a laws/ directory that contains at least
        one domain subdirectory (engineering/, product/, business/).
        """
        candidate = Path.cwd()
        for _ in range(6):  # max 6 levels up
            laws = candidate / "laws"
            if laws.is_dir() and any(laws.iterdir()):
                return laws
            candidate = candidate.parent
        return None


# ---------------------------------------------------------------------------
# Internal helpers
# ---------------------------------------------------------------------------

_FRONTMATTER_RE = re.compile(r"^---\s*\n(.*?)\n---\s*\n", re.DOTALL)


def _extract_frontmatter(text: str) -> dict[str, Any] | None:
    """Return parsed YAML frontmatter dict, or None if absent/invalid."""
    match = _FRONTMATTER_RE.match(text)
    if not match:
        return None
    raw = match.group(1).strip()
    if not raw:
        return None
    try:
        data = yaml.safe_load(raw)
        return data if isinstance(data, dict) else None
    except yaml.YAMLError:
        return None
