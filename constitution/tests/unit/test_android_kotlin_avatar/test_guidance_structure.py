"""Task 1 — guidance.md must contain a Non-Negotiable Laws section per schema §5.

Scenario ID: android-kotlin-avatar-assess-correct/1.1
Law: ENG-11.1 (Hangar SDD), ENG-10.1 (Constitution Metrics Collection)
Schema Reference: docs/guides/avatar-model-schema.md §5
"""

NON_NEGOTIABLE_HEADING = "## Non-Negotiable Laws"


def test_guidance_has_non_negotiable_laws_section(guidance_content):
    """guidance.md must have a '## Non-Negotiable Laws' section (avatar-model-schema.md §5)."""
    assert NON_NEGOTIABLE_HEADING in guidance_content, (
        f"guidance.md is missing the required '{NON_NEGOTIABLE_HEADING}' section. "
        "Per avatar-model-schema.md §5, this section lists each non-negotiable law "
        "with what it requires, what violates it, and an implementation note."
    )


def test_guidance_stack_reflects_junit4_not_junit5(guidance_content):
    """guidance.md must reference JUnit 4 (not JUnit 5) and must not mention fastlane.

    Scenario ID: android-kotlin-avatar-assess-correct/1.2
    Law: ENG-10.1
    """
    assert "JUnit 5" not in guidance_content, (
        "guidance.md mentions 'JUnit 5' — the live codebase uses JUnit 4.13.2. "
        "Shadow governance: agents trained on this file will scaffold wrong test deps."
    )
    assert "fastlane" not in guidance_content, (
        "guidance.md mentions 'fastlane' — androidapps does not use fastlane. "
        "Remove or replace with the actual CI toolchain (Gradle + Jenkins)."
    )
    assert "JUnit 4" in guidance_content, (
        "guidance.md must explicitly state JUnit 4 as the test framework."
    )


def test_guidance_version_matches_manifest(guidance_content, manifest_data):
    """guidance.md frontmatter version must match manifest.yaml version.

    Scenario ID: android-kotlin-avatar-assess-correct/1.3
    Law: ENG-10.1
    """
    import re
    match = re.search(r'^version:\s*["\']?([^"\'\n]+)["\']?', guidance_content, re.MULTILINE)
    assert match, "guidance.md frontmatter has no 'version:' field"
    guidance_version = match.group(1).strip()
    manifest_version = str(manifest_data["avatar"]["version"])
    assert guidance_version == manifest_version, (
        f"guidance.md version '{guidance_version}' != manifest version '{manifest_version}'. "
        "Versions must stay in sync — stale guidance version misleads RAG retrieval."
    )
