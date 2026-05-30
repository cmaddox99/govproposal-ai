"""Test 1.7: C++ manifest.yaml has anti-patterns and retrieval triggers.

Scenario ID: c-plus-plus-avatar-enrichment/1.7
Law: ENG-11.1, ENG-10.1
"""


def test_cpp_manifest_has_anti_patterns_and_retrieval_triggers(manifest_data):
    """Amendment O (V4): anti_patterns and retrieval_triggers removed from manifest.yaml.
    These blocks violated ENG-11.1 scope constraints. Content moved to example files and AVATAR-RAG-INDEX.yaml."""
    import pytest
    manifest = manifest_data
    assert "anti_patterns" not in manifest, (
        "Amendment O V4: anti_patterns must NOT be in manifest.yaml (scope creep violation)"
    )
    assert "retrieval_triggers" not in manifest, (
        "Amendment O V4: retrieval_triggers must NOT be in manifest.yaml — move to AVATAR-RAG-INDEX.yaml"
    )
