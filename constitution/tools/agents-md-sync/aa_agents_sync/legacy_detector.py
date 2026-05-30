"""Legacy AGENTS.md detector for aa-agents-sync.

Detects AGENTS.md files that contain the unversioned ENG-4.1 anchor block
(no BEGIN/END markers) and reports what would be replaced.
"""
from __future__ import annotations

import difflib
from dataclasses import dataclass, field
from pathlib import Path

from .parser import parse_markers

LEGACY_ANCHOR = "MANDATORY AGENT PROTOCOL (Per ENG-4.1"


@dataclass
class LegacyDetectResult:
    """Result of a detect_legacy call."""

    has_legacy: bool = False
    diff: str = ""
    errors: list[str] = field(default_factory=list)


def _find_legacy_block_bounds(lines: list[str]) -> tuple[int, int] | None:
    """Find start and end line indices of the legacy unversioned protocol block.

    Returns (start_idx, end_idx) inclusive, or None if not found.
    The block runs from the heading line containing the anchor to the next
    top-level heading (or end of file).
    """
    start: int | None = None
    for i, line in enumerate(lines):
        if LEGACY_ANCHOR in line:
            start = i
            break
    if start is None:
        return None

    # End at the next level-1 or level-2 heading after the start, or EOF
    for j in range(start + 1, len(lines)):
        stripped = lines[j].rstrip()
        if stripped.startswith("# ") or stripped.startswith("## "):
            return (start, j - 1)
    return (start, len(lines) - 1)


def detect_legacy(agents_md_path: Path, constitution_path: Path) -> LegacyDetectResult:
    """Detect whether AGENTS.md has a legacy (unversioned) protocol block.

    If found, builds a diff showing what the migration would look like.
    Only operates in dry-run context — does NOT modify any files.
    """
    agents_md_path = Path(agents_md_path)
    constitution_path = Path(constitution_path)

    if not agents_md_path.exists():
        return LegacyDetectResult(
            errors=[f"AGENTS.md not found at {agents_md_path}"]
        )

    content = agents_md_path.read_text()
    lines = content.splitlines(keepends=True)

    # If the file already has markers, it is NOT legacy
    existing_sections, _ = parse_markers(content)
    if existing_sections:
        return LegacyDetectResult(has_legacy=False)

    bounds = _find_legacy_block_bounds(lines)
    if bounds is None:
        return LegacyDetectResult(has_legacy=False)

    start, end = bounds

    # Load canonical replacement from templates
    templates_dir = constitution_path / "templates" / "agents-md-sections"
    canonical_file = templates_dir / "mandatory-protocol.md"
    if not canonical_file.exists():
        return LegacyDetectResult(
            errors=[f"canonical template not found at {canonical_file}"]
        )
    canonical_block = canonical_file.read_text()

    # Build unified diff
    old_block = "".join(lines[start : end + 1])
    diff = "".join(
        difflib.unified_diff(
            old_block.splitlines(keepends=True),
            canonical_block.splitlines(keepends=True),
            fromfile="AGENTS.md (legacy)",
            tofile="AGENTS.md (migrated)",
        )
    )

    return LegacyDetectResult(has_legacy=True, diff=diff)
