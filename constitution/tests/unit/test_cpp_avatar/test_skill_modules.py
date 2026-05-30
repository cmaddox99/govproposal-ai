"""Test 4.3: C++ platform-engineering skill modules exist with correct frontmatter.

Scenario ID: c-plus-plus-avatar-enrichment/4.3
Law: ENG-6.7, ENG-10.1
"""

from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[3]
SKILLS_DIR = REPO_ROOT / "agent-skills" / "skills-by-domain" / "platform-engineering"

CPP_SKILL_MODULES = [
    ("skill-cpp-layering-and-boundaries.md", "ENG-2.2"),
    ("skill-cpp-api-compatibility-governance.md", "ENG-2.3"),
    ("skill-cpp-ownership-lifetime-safety.md", "ENG-6.1"),
    ("skill-cpp-presubmit-and-code-ownership.md", "ENG-4.1"),
    ("skill-cpp-sanitizer-hardening.md", "ENG-6.1"),
    ("skill-cpp-performance-benchmark-discipline.md", "ENG-3.1"),
    ("skill-cpp-template-complexity-management.md", "ENG-3.1"),
    ("skill-cpp-portable-build-governance.md", "ENG-5.1"),
]


@pytest.mark.parametrize("filename,primary_law", CPP_SKILL_MODULES)
def test_cpp_skill_module_exists_and_complies(filename, primary_law):
    """Each C++ skill module must exist with YAML frontmatter, law references, and triggers."""
    path = SKILLS_DIR / filename
    assert path.exists(), f"Missing skill module: {filename}"

    content = path.read_text(encoding="utf-8")

    # Must have YAML frontmatter
    assert content.startswith("---"), f"{filename} must start with YAML frontmatter"
    assert content.count("---") >= 2, f"{filename} must have closing frontmatter delimiter"

    # Must reference at least the primary law
    assert primary_law in content, f"{filename} must reference {primary_law}"

    # Must have triggers section
    assert "triggers:" in content, f"{filename} must define triggers"

    # Must have a heading after frontmatter
    assert "# " in content, f"{filename} must have a markdown heading"

    # Must reference C++ or cpp
    content_lower = content.lower()
    assert "c++" in content_lower or "cpp" in content_lower, f"{filename} must reference C++"
