"""Test 4.1: avatars/index.yaml contains C++ avatar entry.

Scenario ID: c-plus-plus-avatar-enrichment/4.1
Law: ENG-6.7 (Audit Trail — avatar must be indexed for discovery)
"""

from pathlib import Path

import yaml

REPO_ROOT = Path(__file__).resolve().parents[3]


def test_index_yaml_contains_cpp_avatar():
    """The master avatar registry must include the C++ avatar with correct metadata."""
    index_path = REPO_ROOT / "avatars" / "index.yaml"
    data = yaml.safe_load(index_path.read_text(encoding="utf-8"))

    tech_avatars = data.get("technology", [])
    cpp_entry = next((a for a in tech_avatars if a["id"] == "avatar-technology-cpp"), None)

    assert cpp_entry is not None, "avatars/index.yaml must contain id: avatar-technology-cpp"
    assert cpp_entry["name"] == "C++ (Modern)"
    assert cpp_entry["path"] == "technology/cpp/"
    assert "C++20" in cpp_entry["stack"]["language"]
    assert "GoogleTest" in cpp_entry["stack"]["testing"]
    assert "CMake" in str(cpp_entry["stack"].get("build", ""))

    # Must activate the same skills as the manifest (without skill- prefix)
    skills = cpp_entry.get("activates", {}).get("skills", [])
    assert "06-atomic-tdd" in skills
    assert "07-vertical-slice-dev" in skills
    assert "08-code-review" in skills

    # Must specialize the core non-negotiable laws
    laws = cpp_entry.get("specializes_laws", [])
    assert "ENG-4.1" in laws
    assert "ENG-6.1" in laws
    assert "ENG-3.1" in laws
