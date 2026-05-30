"""Test 1.1: C++ avatar manifest.yaml exists and has required structure.

Scenario ID: c-plus-plus-avatar-enrichment/1.1
Law: ENG-11.1, ENG-4.1
"""

from pathlib import Path

import yaml

REPO_ROOT = Path(__file__).resolve().parents[3]
MANIFEST_PATH = REPO_ROOT / "avatars" / "technology" / "cpp" / "manifest.yaml"


def test_cpp_manifest_exists_and_has_required_top_level_keys():
    """The C++ manifest.yaml must exist and contain avatar, stack, and activates keys."""
    assert MANIFEST_PATH.exists(), f"Missing {MANIFEST_PATH.relative_to(REPO_ROOT)}"

    with open(MANIFEST_PATH) as f:
        manifest = yaml.safe_load(f)

    assert isinstance(manifest, dict), "manifest.yaml must be a YAML mapping"

    required_keys = {"avatar", "stack", "activates"}
    missing = required_keys - manifest.keys()
    assert not missing, f"manifest.yaml missing required top-level keys: {missing}"

    # avatar section
    avatar = manifest["avatar"]
    assert avatar.get("id") == "avatar-technology-cpp", f"avatar.id must be 'avatar-technology-cpp', got {avatar.get('id')}"
    assert avatar.get("type") == "technology", f"avatar.type must be 'technology'"

    # stack section
    stack = manifest["stack"]
    assert "language" in stack, "stack.language is required"
    assert "testing" in stack, "stack.testing is required"
    assert "build" in stack, "stack.build is required"
