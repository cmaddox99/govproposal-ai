"""Task 5.6a: Constitution compliance validation suite (Amendment A.3).

Scenario ID: c-plus-plus-avatar-enrichment/5.6a
Law: ENG-4.1, ENG-10.1, ENG-6.7

This suite validates that the C++ avatar complies with constitution
governance rules using the avatar_test_helpers and LawRegistry.
"""

import re
import sys
from pathlib import Path

import yaml
import pytest

REPO_ROOT = Path(__file__).resolve().parents[3]
CPP_DIR = REPO_ROOT / "avatars" / "technology" / "cpp"
EXAMPLES_DIR = CPP_DIR / "examples"
LAWS_DIR = REPO_ROOT / "laws"

sys.path.insert(0, str(REPO_ROOT / "tools" / "constitution-lint" / "src"))
sys.path.insert(0, str(REPO_ROOT / "tests" / "unit"))

from test_cpp_avatar.avatar_test_helpers import (
    load_manifest,
    validate_law_references,
    check_example_file_exists,
    check_token_budget,
    get_token_budget,
    check_parity_sections,
    check_citation_format,
)


class TestManifestCompliance:
    """Validate manifest.yaml complies with constitution governance."""

    @pytest.fixture(autouse=True)
    def setup(self):
        self.manifest = load_manifest(CPP_DIR / "manifest.yaml")

    def test_all_specialized_laws_are_valid(self):
        """Every law in specializes_laws must exist in the LawRegistry."""
        results = validate_law_references(self.manifest, LAWS_DIR)
        invalid = [r for r in results if not r["valid"]]
        assert len(invalid) == 0, f"Invalid law references: {[r['law_id'] for r in invalid]}"

    def test_parity_sections_present(self):
        """Manifest must have all cross-avatar parity sections."""
        missing = check_parity_sections(self.manifest)
        assert len(missing) == 0, f"Missing parity sections: {missing}"

    def test_avatar_id_format(self):
        """Avatar ID must follow avatar-{name} convention."""
        avatar_id = self.manifest.get("avatar", {}).get("id", "")
        assert avatar_id.startswith("avatar-"), f"ID must start with 'avatar-': {avatar_id}"

    def test_avatar_has_version(self):
        """Avatar must declare a version."""
        version = self.manifest.get("avatar", {}).get("version", "")
        assert re.match(r'\d+\.\d+\.\d+', version), f"Invalid version format: {version}"


class TestExampleCompliance:
    """Validate all example files comply with constitution governance."""

    @pytest.fixture
    def all_examples(self):
        return sorted(EXAMPLES_DIR.glob("*.md"))

    def test_every_example_has_frontmatter(self, all_examples):
        """Every example must have YAML frontmatter with law_id and avatar."""
        missing_frontmatter = []
        for ex in all_examples:
            content = ex.read_text(encoding="utf-8")
            if not content.startswith("---"):
                missing_frontmatter.append(ex.name)
                continue
            # Check required frontmatter fields
            fm_end = content.index("---", 3)
            fm = content[3:fm_end]
            if "law_id:" not in fm or "avatar:" not in fm:
                missing_frontmatter.append(ex.name)

        assert len(missing_frontmatter) == 0, \
            f"Examples missing frontmatter: {missing_frontmatter}"

    def test_every_example_has_compliant_and_non_compliant(self, all_examples):
        """Every example must have COMPLIANT and NON-COMPLIANT sections."""
        missing = []
        for ex in all_examples:
            content = ex.read_text(encoding="utf-8")
            if "COMPLIANT" not in content or "NON-COMPLIANT" not in content:
                missing.append(ex.name)

        assert len(missing) == 0, f"Examples missing COMPLIANT/NON-COMPLIANT: {missing}"

    def test_every_example_under_token_budget(self, all_examples):
        """Every example must be under the avatar's token budget."""
        budget = get_token_budget(CPP_DIR / "manifest.yaml")
        over = []
        for ex in all_examples:
            passes, tokens = check_token_budget(ex, max_tokens=budget)
            if not passes:
                over.append((ex.name, tokens))

        assert len(over) == 0, f"Examples over {budget}-token budget: {over}"

    def test_every_example_has_cpp_code_block(self, all_examples):
        """Every example must include at least one C++ or CMake code block."""
        missing = []
        for ex in all_examples:
            content = ex.read_text(encoding="utf-8")
            if "```cpp" not in content and "```cmake" not in content:
                missing.append(ex.name)

        assert len(missing) == 0, f"Examples without C++/CMake code blocks: {missing}"


class TestGuidanceCompliance:
    """Validate guidance.md complies with constitution governance."""

    @pytest.fixture(autouse=True)
    def setup(self):
        self.content = (CPP_DIR / "guidance.md").read_text(encoding="utf-8")

    # test_all_law_references_valid removed — duplicate of
    # test_law_citations.py::test_guidance_law_citations_are_valid

    # test_citation_format removed — superseded by
    # test_law_reference_coverage.py::test_minimum_law_coverage (10 critical laws)
    # and test_total_law_reference_count_not_regressed (≥150 refs).


class TestSkillModuleCompliance:
    """Validate C++ skill modules comply with skill format requirements."""

    @pytest.fixture
    def cpp_skills(self):
        skills_dir = REPO_ROOT / "agent-skills" / "skills-by-domain" / "platform-engineering"
        return sorted(skills_dir.glob("skill-cpp-*.md"))

    def test_all_skills_have_valid_frontmatter(self, cpp_skills):
        """Each skill must have YAML frontmatter with id, name, laws, triggers."""
        invalid = []
        for skill in cpp_skills:
            content = skill.read_text(encoding="utf-8")
            if not content.startswith("---"):
                invalid.append((skill.name, "no frontmatter"))
                continue
            for required in ["skill:", "laws:", "triggers:"]:
                if required not in content:
                    invalid.append((skill.name, f"missing {required}"))

        assert len(invalid) == 0, f"Skills with invalid frontmatter: {invalid}"

    def test_all_skills_reference_valid_laws(self, cpp_skills):
        """Each skill's law references must be in the LawRegistry."""
        from aa_constitution_lint.infrastructure.law_registry import LawRegistry

        registry = LawRegistry.load(LAWS_DIR)
        invalid = []
        for skill in cpp_skills:
            refs = set(re.findall(r'\b((?:ENG|PRD|BUS)-\d+\.\d+)\b', skill.read_text(encoding="utf-8")))
            bad = [r for r in refs if r not in registry.law_ids]
            if bad:
                invalid.append((skill.name, bad))

        assert len(invalid) == 0, f"Skills with invalid law refs: {invalid}"
