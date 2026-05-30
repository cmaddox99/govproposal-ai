"""Test 4.6: Law citations in guidance.md and example files use correct format.

Scenario ID: c-plus-plus-avatar-enrichment/4.6
Law: ENG-10.1 (all law references must be valid)
"""

import re
import sys
from pathlib import Path

import yaml

REPO_ROOT = Path(__file__).resolve().parents[3]
CPP_DIR = REPO_ROOT / "avatars" / "technology" / "cpp"
LAWS_DIR = REPO_ROOT / "laws"

sys.path.insert(0, str(REPO_ROOT / "tools" / "constitution-lint" / "src"))


def _get_known_law_ids():
    """Load known law IDs from the constitution-lint LawRegistry."""
    from aa_constitution_lint.infrastructure.law_registry import LawRegistry

    registry = LawRegistry.load(LAWS_DIR)
    return registry.law_ids


def _extract_law_refs(text):
    """Extract all ENG-*, PRD-*, BUS-* references from text."""
    return set(re.findall(r'\b((?:ENG|PRD|BUS)-\d+\.\d+)\b', text))


def test_guidance_law_citations_are_valid():
    """Every ENG-*, PRD-*, BUS-* reference in guidance.md must be a known law."""
    content = (CPP_DIR / "guidance.md").read_text(encoding="utf-8")
    refs = _extract_law_refs(content)
    known = _get_known_law_ids()

    invalid = [r for r in refs if r not in known]
    assert len(invalid) == 0, f"guidance.md has invalid law references: {sorted(invalid)}"


def test_example_files_law_citations_are_valid():
    """Every example file's frontmatter law_id must be a known law."""
    known = _get_known_law_ids()
    examples_dir = CPP_DIR / "examples"
    all_invalid = {}

    for example in sorted(examples_dir.glob("*.md")):
        refs = _extract_law_refs(example.read_text(encoding="utf-8"))
        invalid = [r for r in refs if r not in known]
        if invalid:
            all_invalid[example.name] = invalid

    assert len(all_invalid) == 0, f"Example files with invalid law refs: {all_invalid}"

# test_guidance_citation_format removed — superseded by
# test_law_reference_coverage.py::test_minimum_law_coverage (10 critical laws)
# and test_total_law_reference_count_not_regressed (≥150 refs).
