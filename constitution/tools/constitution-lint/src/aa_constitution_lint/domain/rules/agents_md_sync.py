"""A01 — AGENTS.md drift check rule for aa-constitution-lint.

Checks that AGENTS.md bounded sections (hangar-ai-constitution markers) are
current with the project's constitution-version.txt.

- FAIL: any section marker version < constitution-version.txt
- WARNING: AGENTS.md present but has no markers (legacy / not yet migrated)
- PASS: all markers current, or no AGENTS.md (not adopted)
"""
from __future__ import annotations

import re
from datetime import UTC, datetime
from pathlib import Path

from aa_constitution_lint.domain.models import EvaluationResult, LawEvaluation
from aa_constitution_lint.domain.rules.base import Rule

BEGIN_RE = re.compile(
    r"<!-- BEGIN hangar-ai-constitution:([a-z][a-z0-9-]+) v(\d+\.\d+\.\d+) -->"
)

# MVP valid section name enum (C5/C7)
VALID_SECTION_NAMES: frozenset[str] = frozenset({"mandatory-protocol"})


def _now() -> datetime:
    return datetime.now(UTC)


class AgentsMdDriftRule(Rule):
    """A01 — Checks that AGENTS.md marker versions match constitution-version.txt."""

    def __init__(self, constitution_path: Path | None = None) -> None:
        self._constitution_path = Path(constitution_path) if constitution_path else None

    @property
    def id(self) -> str:
        return "agents_md_sync.A01"

    @property
    def law_id(self) -> str:
        return "ENG-1.2"

    @property
    def description(self) -> str:
        return (
            "AGENTS.md bounded sections must be current with constitution-version.txt; "
            "WARN if no markers present (legacy state)"
        )

    def _resolve_constitution_version(self, project_path: Path) -> str | None:
        """Read constitution-version.txt from constitution_path or project_path."""
        for candidate in filter(None, [self._constitution_path, project_path]):
            version_file = Path(candidate) / "constitution-version.txt"
            if version_file.exists():
                return version_file.read_text().strip()
        return None

    def evaluate(self, project_path: Path) -> list[LawEvaluation]:
        agents_md = project_path / "AGENTS.md"

        if not agents_md.exists():
            # Not adopted — not our concern
            return []

        content = agents_md.read_text()
        sections = BEGIN_RE.findall(content)  # list of (name, version) tuples

        if not sections:
            # AGENTS.md present but no markers — legacy state
            return [
                LawEvaluation(
                    law_id=self.law_id,
                    result=EvaluationResult.WARNING,
                    evaluation_point="aa-constitution-lint",
                    timestamp=_now(),
                    context={
                        "rule": self.id,
                        "file_path": "AGENTS.md",
                        "message": (
                            "AGENTS.md has no hangar-ai-constitution markers. "
                            "Run `aa-agents-sync --apply AGENTS.md` to auto-insert canonical sections."
                        ),
                    },
                )
            ]

        constitution_version = self._resolve_constitution_version(project_path)
        if constitution_version is None:
            if sections:
                # Markers present (repo IS adopted) but no version source —
                # warn explicitly rather than silently skip so CI is visible.
                return [
                    LawEvaluation(
                        law_id=self.law_id,
                        result=EvaluationResult.WARNING,
                        evaluation_point="aa-constitution-lint",
                        timestamp=_now(),
                        context={
                            "rule": self.id,
                            "file_path": "AGENTS.md",
                            "message": (
                                "constitution-version.txt not found — A01 drift check disabled. "
                                "Set AA_CONSTITUTION_PATH=/path/to/hangar-ai-constitution "
                                "(env var), or run `aa-agents-sync --apply AGENTS.md` to "
                                "create constitution-version.txt in this repo."
                            ),
                        },
                    )
                ]
            # No markers and no version source — not adopted, skip cleanly
            return [
                LawEvaluation(
                    law_id=self.law_id,
                    result=EvaluationResult.SKIP,
                    evaluation_point="aa-constitution-lint",
                    timestamp=_now(),
                    context={
                        "rule": self.id,
                        "message": "constitution-version.txt not found; skipping A01 check",
                    },
                )
            ]

        # Validate section names against MVP enum (C5/C7)
        unknown = [(name, ver) for name, ver in sections if name not in VALID_SECTION_NAMES]
        if unknown:
            return [
                LawEvaluation(
                    law_id=self.law_id,
                    result=EvaluationResult.FAIL,
                    evaluation_point="aa-constitution-lint",
                    timestamp=_now(),
                    context={
                        "rule": self.id,
                        "file_path": "AGENTS.md",
                        "message": (
                            f"{len(unknown)} unknown section name(s) in markers: "
                            + ", ".join(n for n, _ in unknown)
                            + f"; valid names: {sorted(VALID_SECTION_NAMES)}"
                        ),
                    },
                )
            ]

        stale = [
            (name, ver)
            for name, ver in sections
            if ver != constitution_version
        ]

        if stale:
            return [
                LawEvaluation(
                    law_id=self.law_id,
                    result=EvaluationResult.FAIL,
                    evaluation_point="aa-constitution-lint",
                    timestamp=_now(),
                    context={
                        "rule": self.id,
                        "file_path": "AGENTS.md",
                        "message": (
                            f"{len(stale)} section(s) behind constitution "
                            f"v{constitution_version}: "
                            + ", ".join(f"{n}@v{v}" for n, v in stale)
                        ),
                    },
                )
            ]

        return [
            LawEvaluation(
                law_id=self.law_id,
                result=EvaluationResult.PASS,
                evaluation_point="aa-constitution-lint",
                timestamp=_now(),
                context={
                    "rule": self.id,
                    "file_path": "AGENTS.md",
                    "message": (
                        f"All {len(sections)} AGENTS.md section(s) current "
                        f"at constitution v{constitution_version}"
                    ),
                },
            )
        ]
