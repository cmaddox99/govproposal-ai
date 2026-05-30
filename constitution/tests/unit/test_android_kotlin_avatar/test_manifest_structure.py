"""Tasks 4–6 — manifest.yaml correctness.

Scenario IDs: android-kotlin-avatar-assess-correct/1.4, 1.5, 1.6
Laws: ENG-10.1, ENG-11.1
"""


def test_manifest_has_no_android_notes(manifest_data):
    """manifest.yaml specializes_laws entries must not contain android_note fields.

    Scenario ID: android-kotlin-avatar-assess-correct/1.4
    Law: ENG-10.1
    android_note fields belong in guidance-detail.md or examples/; in the manifest
    they bloat the token budget and duplicate content that belongs elsewhere.
    """
    violations = []
    for law in manifest_data.get("specializes_laws", []):
        if "android_note" in law:
            violations.append(law.get("id", "unknown"))
    assert not violations, (
        f"manifest.yaml has android_note on laws: {violations}. "
        "Remove android_note fields — move content to guidance-detail.md or examples/."
    )


def test_manifest_activates_legacy_rescue_workflow(manifest_data):
    """manifest.yaml activates.workflows must include legacy-rescue-decision-track.

    Scenario ID: android-kotlin-avatar-assess-correct/1.5
    Law: ENG-11.1

    androidapps is a legacy codebase (4.7/10 composite score, 80 files >500 LOC).
    Per ENG-11.1 every legacy avatar must activate legacy-rescue-decision-track
    so agents route discovery/refactor work through the correct workflow.
    """
    workflows = manifest_data.get("activates", {}).get("workflows", [])
    assert "legacy-rescue-decision-track" in workflows, (
        f"manifest.yaml activates.workflows is missing 'legacy-rescue-decision-track'. "
        f"Current workflows: {workflows}. "
        "androidapps is a legacy codebase — this workflow is required per ENG-11.1."
    )


def test_eng_10_1_example_exists_and_valid(examples_dir):
    """examples/ENG-10.1-constitution-governance.md must exist with correct frontmatter.

    Scenario ID: android-kotlin-avatar-assess-correct/1.7
    Law: ENG-10.1

    Schema §1: one example file per law in specializes_laws. ENG-10.1 is declared
    in manifest but has no example file — this is a schema violation.
    The file must have YAML frontmatter with law_id: ENG-10.1 and avatar: android-kotlin.
    """
    import yaml as _yaml

    example_file = examples_dir / "ENG-10.1-constitution-governance.md"
    assert example_file.exists(), (
        "examples/ENG-10.1-constitution-governance.md does not exist. "
        "Schema §1 requires one example file per specializes_law."
    )
    content = example_file.read_text(encoding="utf-8")
    assert content.startswith("---"), "Example file must begin with YAML frontmatter (---)"
    end = content.index("---", 3)
    frontmatter = _yaml.safe_load(content[3:end])
    assert frontmatter.get("law_id") == "ENG-10.1", (
        f"Frontmatter law_id must be 'ENG-10.1', got: {frontmatter.get('law_id')}"
    )
    assert frontmatter.get("avatar") == "android-kotlin", (
        f"Frontmatter avatar must be 'android-kotlin', got: {frontmatter.get('avatar')}"
    )


def test_eng_11_1_example_exists_and_valid(examples_dir):
    """examples/ENG-11.1-spec-driven-development.md must exist with correct frontmatter.

    Scenario ID: android-kotlin-avatar-assess-correct/1.8
    Law: ENG-11.1 (NON-NEGOTIABLE — Hangar SDD Law)

    Schema §1: one example file per law in specializes_laws. ENG-11.1 is NON-NEGOTIABLE;
    a missing example is a schema violation and a constitutional breach.
    The file must have YAML frontmatter with law_id: ENG-11.1 and avatar: android-kotlin,
    and must demonstrate the PROPOSE → IMPLEMENT → ARCHIVE lifecycle.
    """
    import yaml as _yaml

    example_file = examples_dir / "ENG-11.1-spec-driven-development.md"
    assert example_file.exists(), (
        "examples/ENG-11.1-spec-driven-development.md does not exist. "
        "ENG-11.1 is NON-NEGOTIABLE — missing example is a constitutional breach."
    )
    content = example_file.read_text(encoding="utf-8")
    assert content.startswith("---"), "Example file must begin with YAML frontmatter (---)"
    end = content.index("---", 3)
    frontmatter = _yaml.safe_load(content[3:end])
    assert frontmatter.get("law_id") == "ENG-11.1", (
        f"Frontmatter law_id must be 'ENG-11.1', got: {frontmatter.get('law_id')}"
    )
    assert frontmatter.get("avatar") == "android-kotlin", (
        f"Frontmatter avatar must be 'android-kotlin', got: {frontmatter.get('avatar')}"
    )
    # Must demonstrate the SDD lifecycle stages
    assert "PROPOSE" in content, "Example must demonstrate PROPOSE stage (ENG-11.1 §3)"
    assert "IMPLEMENT" in content, "Example must demonstrate IMPLEMENT stage (ENG-11.1 §3)"
    assert "ARCHIVE" in content, "Example must demonstrate ARCHIVE stage (ENG-11.1 §3)"
    assert "hangar-ai-specs/" in content, (
        "Example must reference hangar-ai-specs/ folder (ENG-11.1 §1)"
    )
