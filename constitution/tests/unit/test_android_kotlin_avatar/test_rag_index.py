"""Task 9 — AVATAR-RAG-INDEX.yaml android-kotlin entry correctness.

Scenario ID: android-kotlin-avatar-assess-correct/1.9
Laws: ENG-10.1, ENG-11.1

The RAG index is the routing table agents use to find this avatar.
Stale entries cause shadow governance: agents are routed to correct avatar
but served wrong information (JUnit 5, fastlane) that contradicts guidance.md.
"""

import yaml
from pathlib import Path

import pytest


@pytest.fixture(scope="module")
def rag_entry():
    repo_root = Path(__file__).resolve().parents[3]
    index = yaml.safe_load(
        (repo_root / "avatars" / "AVATAR-RAG-INDEX.yaml").read_text(encoding="utf-8")
    )
    # Index has a top-level "technology_avatars:" block containing "android-kotlin:"
    return index["technology_avatars"]["android-kotlin"]


def test_rag_index_android_kotlin_entry(rag_entry):
    """AVATAR-RAG-INDEX.yaml android-kotlin entry must reflect current avatar state.

    Scenario ID: android-kotlin-avatar-assess-correct/1.9
    Laws: ENG-10.1, ENG-11.1

    Checks (all in one atomic test per ENG-4.1 — these are properties of the same
    RAG index entry; splitting them would create artificial seams):
    1. No 'JUnit 5' references — live codebase uses JUnit 4
    2. No 'fastlane' references — androidapps uses Gradle + Jenkins, not fastlane
    3. eng_10_1 and eng_11_1 present in files block
    4. ENG-10.1 and ENG-11.1 present in specializes_laws
    """
    import json

    entry_text = json.dumps(rag_entry)

    # 1 — No JUnit 5
    assert "JUnit 5" not in entry_text, (
        "AVATAR-RAG-INDEX.yaml android-kotlin entry contains 'JUnit 5'. "
        "The live codebase uses JUnit 4.13.2. Shadow governance: agents will "
        "scaffold wrong test dependencies."
    )

    # 2 — No fastlane
    assert "fastlane" not in entry_text, (
        "AVATAR-RAG-INDEX.yaml android-kotlin entry contains 'fastlane'. "
        "androidapps uses Gradle + Jenkins — fastlane is not configured. "
        "Shadow governance: agents will generate unusable CI commands."
    )

    # 3 — Example files for ENG-10.1 and ENG-11.1 registered
    files = rag_entry.get("files", {})
    assert "eng_10_1" in files, (
        "files block is missing 'eng_10_1'. "
        "examples/ENG-10.1-constitution-governance.md was created in Task 7 "
        "but is not registered in the RAG index."
    )
    assert "eng_11_1" in files, (
        "files block is missing 'eng_11_1'. "
        "examples/ENG-11.1-spec-driven-development.md was created in Task 8 "
        "but is not registered in the RAG index."
    )

    # 4 — ENG-10.1 and ENG-11.1 in specializes_laws
    law_ids = []
    for entry in rag_entry.get("specializes_laws", []):
        if isinstance(entry, dict):
            law_ids.extend(entry.keys())
        elif isinstance(entry, str):
            law_ids.append(entry)
    assert any(k.startswith("ENG-10.1") for k in law_ids), (
        "specializes_laws is missing ENG-10.1 entry. "
        "ENG-10.1 is declared in manifest.yaml but absent from the RAG index."
    )
    assert any(k.startswith("ENG-11.1") for k in law_ids), (
        "specializes_laws is missing ENG-11.1 entry. "
        "ENG-11.1 is NON-NEGOTIABLE and declared in manifest.yaml "
        "but absent from the RAG index."
    )
