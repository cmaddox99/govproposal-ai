"""Test 1.6: C++ manifest.yaml has a project_structure template.

Scenario ID: c-plus-plus-avatar-enrichment/1.6
Law: ENG-11.1, ENG-2.2
"""

from test_cpp_avatar.avatar_test_helpers import load_manifest


def test_cpp_manifest_has_project_structure(manifest_data):
    """manifest.yaml must have a project_structure string showing the canonical directory layout."""
    manifest = manifest_data

    assert "project_structure" in manifest, "project_structure section is required"
    structure = manifest["project_structure"]
    assert isinstance(structure, str), "project_structure must be a multi-line string"
    assert len(structure) >= 100, "project_structure must be a meaningful directory tree"

    required_dirs = ["src/", "unit/", "integration/", "include/", "CMakeLists"]
    for d in required_dirs:
        assert d.lower() in structure.lower(), (
            f"project_structure must reference '{d}'"
        )
