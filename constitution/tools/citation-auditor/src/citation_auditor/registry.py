"""Registry loader for aa-citation-audit.

Architecture: Infrastructure layer (Phase 3 §2.3 / Phase 4 §4.1).
Responsibility: Load and parse laws/index.yaml + scan all domain law files
for title/summary (ADR-002: no per-law title/summary in index.yaml — must
scan individual law .md files).
"""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import yaml

from citation_auditor.exceptions import RegistryLoadError


@dataclass(frozen=True)
class RegistryEntry:
    law_id: str
    domain: str
    non_negotiable: bool
    title: str | None
    summary: str | None


def load_registry(laws_dir: Path) -> dict[str, RegistryEntry]:
    """Load the law registry from laws_dir/index.yaml.

    Scans ALL domain law .md files to extract title/summary from frontmatter.
    Raises RegistryLoadError on any failure.

    Returns:
        dict mapping law_id → RegistryEntry
    """
    laws_dir = Path(laws_dir)

    if not laws_dir.exists() or not laws_dir.is_dir():
        raise RegistryLoadError(f"Registry directory not found: {laws_dir}")

    index_path = laws_dir / "index.yaml"
    if not index_path.exists():
        raise RegistryLoadError(f"Registry file not found: {index_path}")

    try:
        with index_path.open(encoding="utf-8") as f:
            index = yaml.safe_load(f)
    except yaml.YAMLError as exc:
        raise RegistryLoadError(f"Registry load failed: {exc}") from exc

    if not isinstance(index, dict):
        raise RegistryLoadError("Registry load failed: index.yaml must be a YAML mapping")

    # Build set of non-negotiable IDs per domain
    non_neg: set[str] = set()
    for domain_ids in (index.get("non_negotiable") or {}).values():
        if isinstance(domain_ids, list):
            non_neg.update(domain_ids)

    # Build set of all known IDs and their domains
    domain_for_id: dict[str, str] = {}
    for domain, ids in (index.get("law_ids") or {}).items():
        if isinstance(ids, list):
            for law_id in ids:
                domain_for_id[law_id] = domain

    # Scan all domain law .md files for title/summary (ADR-002)
    title_map: dict[str, str] = {}
    summary_map: dict[str, str] = {}
    domains_meta = index.get("domains") or {}
    for domain_name, domain_data in domains_meta.items():
        if not isinstance(domain_data, dict):
            continue
        for rel_path in domain_data.get("files") or []:
            law_file = laws_dir / rel_path
            if not law_file.exists():
                continue
            _parse_law_file(law_file, title_map, summary_map)

    # Assemble registry
    registry: dict[str, RegistryEntry] = {}
    for law_id, domain in domain_for_id.items():
        registry[law_id] = RegistryEntry(
            law_id=law_id,
            domain=domain,
            non_negotiable=law_id in non_neg,
            title=title_map.get(law_id),
            summary=summary_map.get(law_id),
        )

    return registry


def _parse_law_file(
    law_file: Path,
    title_map: dict[str, str],
    summary_map: dict[str, str],
) -> None:
    """Parse a law .md file and extract id/title/summary from frontmatter."""
    try:
        content = law_file.read_text(encoding="utf-8")
    except OSError:
        return

    # Extract YAML frontmatter between first --- delimiters
    if not content.startswith("---"):
        return
    end = content.find("\n---", 3)
    if end == -1:
        return
    frontmatter_text = content[3:end]

    try:
        frontmatter = yaml.safe_load(frontmatter_text)
    except yaml.YAMLError:
        return

    if not isinstance(frontmatter, dict):
        return

    for law_entry in frontmatter.get("laws") or []:
        if not isinstance(law_entry, dict):
            continue
        law_id = law_entry.get("id")
        if not law_id:
            continue
        if "title" in law_entry:
            title_map[law_id] = law_entry["title"]
        if "summary" in law_entry:
            summary_map[law_id] = law_entry["summary"]
