"""LawRegistry - loads and validates law IDs from Constitution markdown files."""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import yaml


@dataclass
class LawRegistry:
    """Registry of valid law IDs loaded from Constitution markdown files."""

    law_ids: set[str] = field(default_factory=set)
    laws: dict[str, dict[str, Any]] = field(default_factory=dict)

    @classmethod
    def load(cls, laws_dir: Path) -> LawRegistry:
        """
        Load law IDs from all markdown and YAML files in the laws directory.

        Parses:
        - YAML frontmatter from markdown files (laws array)
        - YAML domain files (_domain.yaml) with nested law definitions

        Args:
            laws_dir: Path to the laws/ directory.

        Returns:
            LawRegistry with all discovered law IDs.
        """
        law_ids: set[str] = set()
        laws: dict[str, dict[str, Any]] = {}

        if not laws_dir.exists():
            return cls(law_ids=law_ids, laws=laws)

        # Find all markdown files recursively
        for md_file in laws_dir.rglob("*.md"):
            try:
                frontmatter = cls._extract_frontmatter(md_file)
                if frontmatter and "laws" in frontmatter:
                    for law in frontmatter["laws"]:
                        if isinstance(law, dict) and "id" in law:
                            law_id = law["id"]
                            law_ids.add(law_id)
                            laws[law_id] = law
            except Exception:
                # Skip files with malformed frontmatter
                continue

        # Also parse YAML domain files for law definitions
        for yaml_file in laws_dir.rglob("*.yaml"):
            try:
                content = yaml_file.read_text(encoding="utf-8")
                data = yaml.safe_load(content)
                if data:
                    cls._extract_laws_from_yaml(data, law_ids, laws)
            except Exception:
                continue

        return cls(law_ids=law_ids, laws=laws)

    @classmethod
    def _extract_laws_from_yaml(
        cls,
        data: Any,
        law_ids: set[str],
        laws: dict[str, dict[str, Any]],
    ) -> None:
        """
        Recursively extract law IDs from a YAML structure.

        Looks for:
        - Dicts with 'id' keys that match the law pattern
        - Strings that match the law pattern (e.g., in lists)
        """
        if isinstance(data, str):
            # Check if this string is a law ID
            if re.match(r"^(ENG|PRD|BUS)-\d+\.\d+$", data):
                law_ids.add(data)
                # Create minimal law entry if not already present
                if data not in laws:
                    laws[data] = {"id": data}

        elif isinstance(data, dict):
            # Check if this dict has an 'id' that looks like a law
            if "id" in data:
                law_id = data["id"]
                if isinstance(law_id, str) and re.match(r"^(ENG|PRD|BUS)-\d+\.\d+$", law_id):
                    law_ids.add(law_id)
                    laws[law_id] = data

            # Recurse into dict values
            for value in data.values():
                cls._extract_laws_from_yaml(value, law_ids, laws)

        elif isinstance(data, list):
            # Recurse into list items
            for item in data:
                cls._extract_laws_from_yaml(item, law_ids, laws)

    @staticmethod
    def _extract_frontmatter(file_path: Path) -> dict[str, Any] | None:
        """
        Extract YAML frontmatter from a markdown file.

        Args:
            file_path: Path to the markdown file.

        Returns:
            Parsed YAML frontmatter as dict, or None if not found.
        """
        content = file_path.read_text(encoding="utf-8")

        # Match YAML frontmatter between --- delimiters
        match = re.match(r"^---\s*\n(.*?)\n---", content, re.DOTALL)
        if not match:
            return None

        try:
            result = yaml.safe_load(match.group(1))
            if isinstance(result, dict):
                return result
            return None
        except yaml.YAMLError:
            return None

    def law_exists(self, law_id: str) -> bool:
        """
        Check if a law ID exists in the registry.

        Args:
            law_id: The law ID to check (e.g., "ENG-4.1").

        Returns:
            True if the law exists, False otherwise.
        """
        return law_id in self.law_ids

    def get_law(self, law_id: str) -> dict[str, Any] | None:
        """
        Get law metadata by ID.

        Args:
            law_id: The law ID to retrieve.

        Returns:
            Law metadata dict if found, None otherwise.
        """
        return self.laws.get(law_id)
