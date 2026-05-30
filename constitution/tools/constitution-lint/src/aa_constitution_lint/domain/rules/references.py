"""Reference rules - validate law references in project files."""

from __future__ import annotations

import re
from datetime import UTC, datetime
from pathlib import Path
from typing import TYPE_CHECKING, Any

from aa_constitution_lint.domain.models import EvaluationResult, LawEvaluation
from aa_constitution_lint.domain.rules.base import Rule

if TYPE_CHECKING:
    from aa_constitution_lint.infrastructure.law_registry import LawRegistry


# Pattern to match law references like ENG-4.1
LAW_REFERENCE_PATTERN = re.compile(r"\b(ENG|PRD|BUS)-\d+\.\d+\b")

# File extensions to scan for law references
SCANNABLE_EXTENSIONS = {".md", ".py", ".yaml", ".yml", ".json", ".txt", ".rst"}


class LawReferenceRule(Rule):
    """Validate that law references in files are valid."""

    def __init__(self, registry: LawRegistry) -> None:
        """
        Initialize with a LawRegistry for validation.

        Args:
            registry: LawRegistry containing valid law IDs.
        """
        self._registry = registry

    @property
    def id(self) -> str:
        return "references.law_references"

    @property
    def law_id(self) -> str:
        return "ENG-10.1"  # Constitution Metrics - ensures law refs are valid

    @property
    def description(self) -> str:
        return "All law references (ENG-*, PRD-*, BUS-*) must be valid"

    def evaluate(self, project_path: Path) -> list[LawEvaluation]:
        """
        Scan project files for law references and validate them.

        Args:
            project_path: Path to project root.

        Returns:
            List containing a single LawEvaluation with pass/fail result.
        """
        invalid_references: list[dict[str, Any]] = []

        # Scan all files in project (except laws/ directory)
        for file_path in self._get_scannable_files(project_path):
            file_invalid_refs = self._scan_file(file_path, project_path)
            invalid_references.extend(file_invalid_refs)

        if invalid_references:
            # Build message with all invalid references
            ref_list = ", ".join(
                f"{ref['law_id']} ({ref['file_path']}:{ref['line_number']})"
                for ref in invalid_references[:5]  # Limit to first 5
            )
            if len(invalid_references) > 5:
                ref_list += f" and {len(invalid_references) - 5} more"

            return [
                LawEvaluation(
                    law_id=self.law_id,
                    result=EvaluationResult.FAIL,
                    evaluation_point="aa-constitution-lint",
                    timestamp=datetime.now(UTC),
                    context={
                        "rule": self.id,
                        "message": f"Invalid law references found: {ref_list}",
                        "invalid_references": invalid_references,
                        "file_path": invalid_references[0]["file_path"],
                        "line_number": invalid_references[0]["line_number"],
                    },
                )
            ]

        return [
            LawEvaluation(
                law_id=self.law_id,
                result=EvaluationResult.PASS,
                evaluation_point="aa-constitution-lint",
                timestamp=datetime.now(UTC),
                context={
                    "rule": self.id,
                    "message": "All law references are valid",
                },
            )
        ]

    def _get_scannable_files(self, project_path: Path) -> list[Path]:
        """
        Get all files that should be scanned for law references.

        Excludes:
        - laws/ directory (law definitions)
        - Hidden directories (.git, .venv, etc.)
        - Test directories (tests/, test/) - may contain intentional fake law IDs
        - Non-scannable file types

        Args:
            project_path: Path to project root.

        Returns:
            List of file paths to scan.
        """
        files = []
        # Directories to skip (root level)
        skip_dirs = {"laws", "tests", "test", "node_modules", "__pycache__"}
        # Files to skip (governance docs that reference historical/removed law IDs)
        skip_files = {"DEFERRED_LAWS.md"}

        for file_path in project_path.rglob("*"):
            if not file_path.is_file():
                continue

            # Skip hidden directories
            if any(part.startswith(".") for part in file_path.parts):
                continue

            # Skip excluded directories
            rel_path = file_path.relative_to(project_path)
            if rel_path.parts and rel_path.parts[0] in skip_dirs:
                continue

            # Skip governance meta-documents that reference historical law IDs
            if rel_path.name in skip_files:
                continue

            # Also skip nested test directories
            if "tests" in rel_path.parts or "test" in rel_path.parts:
                continue

            # Skip hangar-ai-specs/changes (contains spec examples with intentional fake law IDs)
            if len(rel_path.parts) >= 2 and rel_path.parts[:2] == ("hangar-ai-specs", "changes"):
                continue

            # Skip hangar-ai-specs/archive (historical documents with stale law references)
            if len(rel_path.parts) >= 2 and rel_path.parts[:2] == ("hangar-ai-specs", "archive"):
                continue

            # Skip generated reports (may contain stale law IDs in diagnostics)
            if "reports" in rel_path.parts:
                continue

            # Only scan certain file types
            if file_path.suffix.lower() in SCANNABLE_EXTENSIONS:
                files.append(file_path)

        return files

    def _scan_file(self, file_path: Path, project_path: Path) -> list[dict[str, Any]]:
        """
        Scan a single file for invalid law references.

        Args:
            file_path: Path to the file to scan.
            project_path: Project root for relative path calculation.

        Returns:
            List of dicts with invalid reference details.
        """
        invalid_refs = []

        try:
            content = file_path.read_text(encoding="utf-8")
        except (OSError, UnicodeDecodeError):
            return []

        for line_num, line in enumerate(content.splitlines(), start=1):
            for match in LAW_REFERENCE_PATTERN.finditer(line):
                law_id = match.group(0)
                if not self._registry.law_exists(law_id):
                    rel_path = file_path.relative_to(project_path)
                    invalid_refs.append(
                        {
                            "law_id": law_id,
                            "file_path": str(rel_path),
                            "line_number": line_num,
                        }
                    )

        return invalid_refs
