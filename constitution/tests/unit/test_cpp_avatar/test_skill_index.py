"""Test 4.4: platform-engineering index.yaml registers all 8 C++ skill modules.

Scenario ID: c-plus-plus-avatar-enrichment/4.4
Law: ENG-6.7 (skills must be indexed for RAG retrieval)
"""

from pathlib import Path

import yaml

REPO_ROOT = Path(__file__).resolve().parents[3]


def test_platform_engineering_index_contains_cpp_skills():
    """All 8 C++ skill modules must be registered in the platform-engineering index."""
    index_path = (
        REPO_ROOT / "agent-skills" / "skills-by-domain" / "platform-engineering" / "index.yaml"
    )
    data = yaml.safe_load(index_path.read_text(encoding="utf-8"))
    skills = data.get("skills", [])
    skill_files = [s["file"] for s in skills]

    expected_files = [
        "skill-cpp-layering-and-boundaries.md",
        "skill-cpp-api-compatibility-governance.md",
        "skill-cpp-ownership-lifetime-safety.md",
        "skill-cpp-presubmit-and-code-ownership.md",
        "skill-cpp-sanitizer-hardening.md",
        "skill-cpp-performance-benchmark-discipline.md",
        "skill-cpp-template-complexity-management.md",
        "skill-cpp-portable-build-governance.md",
    ]

    for f in expected_files:
        assert f in skill_files, f"index.yaml must register {f}"

    # Count should be updated
    assert data.get("count", 0) >= 15, "count must reflect 7 existing + 8 new = 15+"
