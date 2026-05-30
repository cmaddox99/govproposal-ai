"""Test 1.5: C++ manifest.yaml has conventions section with naming, patterns, and testing layout.

Scenario ID: c-plus-plus-avatar-enrichment/1.5
Law: ENG-11.1, ENG-3.5
"""


def test_cpp_manifest_has_conventions_section(manifest_data):
    """manifest.yaml must have a conventions section with naming, patterns, and testing_layout."""
    manifest = manifest_data

    assert "conventions" in manifest, "conventions section is required"
    conventions = manifest["conventions"]

    # Naming conventions
    assert "naming" in conventions, "conventions.naming is required"
    naming = conventions["naming"]
    required_naming = {"classes", "functions", "variables", "constants"}
    missing = required_naming - naming.keys()
    assert not missing, f"conventions.naming missing entries: {missing}"

    # Patterns
    assert "patterns" in conventions, "conventions.patterns is required"
    assert len(conventions["patterns"]) >= 3, "conventions.patterns must have at least 3 entries"

    # Testing layout
    assert "testing_layout" in conventions, "conventions.testing_layout is required"
    testing = conventions["testing_layout"]
    assert "unit_dir" in testing, "conventions.testing_layout.unit_dir is required"
    assert "integration_dir" in testing, "conventions.testing_layout.integration_dir is required"
