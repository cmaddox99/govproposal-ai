"""Test 1.4: C++ manifest.yaml has a commands section with test/build/lint/format/sanitizer entries.

Scenario ID: c-plus-plus-avatar-enrichment/1.4
Law: ENG-11.1, ENG-5.1
"""


def test_cpp_manifest_has_command_matrix(manifest_data):
    """manifest.yaml must have a commands section covering test, build, lint, format, and sanitizer."""
    manifest = manifest_data

    assert "commands" in manifest, "commands section is required"
    commands = manifest["commands"]

    required_categories = {"test", "build", "lint", "format", "sanitizer"}
    missing = required_categories - commands.keys()
    assert not missing, f"commands section missing categories: {missing}"

    # Each category must have at least one entry
    for category in required_categories:
        cat = commands[category]
        assert isinstance(cat, dict), f"commands.{category} must be a mapping"
        assert len(cat) >= 1, f"commands.{category} must have at least one entry"
