"""Test: legacy-rescue-java.md exists and satisfies the java-spring avatar contract.

Scenario ID: legacy-rescue-java-guide/1.1
Laws: ENG-10.1 (Constitution Metrics — file reference integrity)
"""

from pathlib import Path


def test_legacy_rescue_java_guide_exists(java_spring_dir: Path) -> None:
    """avatars/technology/java-spring/legacy-rescue-java.md must exist.

    Scenario ID: legacy-rescue-java-guide/1.1
    Law: ENG-10.1

    manifest.yaml declares workflow_guides.legacy-rescue-refactor: legacy-rescue-java.md
    and AVATAR-RAG-INDEX.yaml indexes it. The file must exist or every PR fails
    the ENG-10.1 constitution lint gate.
    """
    guide = java_spring_dir / "legacy-rescue-java.md"
    assert guide.exists(), (
        "avatars/technology/java-spring/legacy-rescue-java.md does not exist. "
        "manifest.yaml and AVATAR-RAG-INDEX.yaml both reference this file. "
        "Per ENG-10.1, all indexed files must be present. "
        "Author this guide per hangar-ai-specs/changes/legacy-rescue-java-guide/PROPOSAL.md."
    )
