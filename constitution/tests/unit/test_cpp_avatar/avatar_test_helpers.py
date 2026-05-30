"""Reusable governance validators for avatar testing.

Created per Amendment A.1 of the C++ avatar enrichment proposal.
These helpers integrate with the constitution-lint LawRegistry to provide
behavioral governance checks rather than simple text-presence assertions.

Scenario ID: c-plus-plus-avatar-enrichment/2.7a
Laws: ENG-4.1, ENG-10.1
"""

from __future__ import annotations

import re
from pathlib import Path
from typing import Any

import yaml


def load_manifest(manifest_path: Path) -> dict[str, Any]:
    """Load and parse an avatar manifest.yaml file."""
    with open(manifest_path) as f:
        data = yaml.safe_load(f)
    if not isinstance(data, dict):
        raise ValueError(f"{manifest_path} is not a valid YAML mapping")
    return data


def validate_law_references(
    manifest: dict[str, Any], laws_dir: Path
) -> list[dict[str, Any]]:
    """Validate that all law IDs in specializes_laws are valid per LawRegistry.

    Returns a list of result dicts: [{"law_id": str, "valid": bool}].
    """
    from aa_constitution_lint.infrastructure.law_registry import LawRegistry

    registry = LawRegistry.load(laws_dir)
    results: list[dict[str, Any]] = []

    for law_entry in manifest.get("specializes_laws", []):
        law_id = law_entry.get("id", "") if isinstance(law_entry, dict) else str(law_entry)
        results.append({"law_id": law_id, "valid": registry.law_exists(law_id)})

    return results


def check_example_file_exists(
    manifest: dict[str, Any], avatar_dir: Path
) -> list[dict[str, str | bool]]:
    """Verify every specializes_laws entry with example_file has a matching file.

    Returns a list of result dicts: [{"law_id": str, "example_file": str, "exists": bool}].
    """
    results: list[dict[str, str | bool]] = []

    for law_entry in manifest.get("specializes_laws", []):
        if not isinstance(law_entry, dict):
            continue
        example_file = law_entry.get("example_file")
        if example_file:
            full_path = avatar_dir / example_file
            results.append({
                "law_id": law_entry.get("id", "unknown"),
                "example_file": example_file,
                "exists": full_path.exists(),
            })

    return results


# Default token budget; overridden per-avatar via governance_overrides.
_DEFAULT_TOKEN_BUDGET = 850


def get_token_budget(manifest_path: Path) -> int:
    """Return the example token budget from the manifest, or the default."""
    manifest = load_manifest(manifest_path)
    overrides = manifest.get("governance_overrides", {})
    return int(overrides.get("example_token_budget", _DEFAULT_TOKEN_BUDGET))


def check_token_budget(
    file_path: Path, max_tokens: int = _DEFAULT_TOKEN_BUDGET
) -> tuple[bool, int]:
    """Check whether a file stays under the token budget.

    Uses word_count * 1.3 as a token estimate.
    YAML frontmatter is excluded — it is metadata and should not count against the content budget.
    Returns (passes, estimated_tokens).
    """
    content = file_path.read_text(encoding="utf-8")
    # Strip YAML frontmatter before counting
    if content.startswith("---"):
        parts = content.split("---", 2)
        if len(parts) >= 3:
            content = parts[2]
    word_count = len(content.split())
    estimated_tokens = int(word_count * 1.3)
    return (estimated_tokens <= max_tokens, estimated_tokens)


def check_parity_sections(
    manifest: dict[str, Any],
    required_sections: set[str] | None = None,
) -> list[str]:
    """Verify manifest contains required top-level sections for avatar parity.

    Returns list of missing section names (empty = full parity).
    """
    if required_sections is None:
        required_sections = {
            "avatar", "stack", "activates", "specializes_laws",
            "conventions", "commands",
        }
    return sorted(required_sections - set(manifest.keys()))


def find_section(content: str, heading: str, n_lines: int = 60) -> str | None:
    """Return up to n_lines of content starting from the first heading that
    contains `heading` (case-insensitive). Returns None if heading not found."""
    lines = content.split("\n")
    for i, line in enumerate(lines):
        if line.startswith("#") and heading.lower() in line.lower():
            return "\n".join(lines[i:i + n_lines])
    return None


def check_citation_format(content: str) -> list[str]:
    """Check for bare law ID references that should be hyperlinks.

    Valid format: [ENG-4.1](path) or [PRD-1.2](path)
    Invalid (bare): ENG-4.1 without surrounding []()

    Returns list of bare law ID strings found.
    """
    # Match all law ID patterns in content
    all_refs = set(re.findall(r"(?:ENG|PRD|BUS)-\d+\.\d+", content))

    # Match law IDs that are inside markdown hyperlinks [ID](path)
    linked_refs = set(re.findall(r"\[((?:ENG|PRD|BUS)-\d+\.\d+)\]\(", content))

    # Bare refs are those found in content but never inside a hyperlink
    bare_refs = all_refs - linked_refs
    return sorted(bare_refs)
