"""Test 4.5: AGENTS.md retrieval protocol covers C++ avatar discovery.

Scenario ID: c-plus-plus-avatar-enrichment/4.5
Law: ENG-1.2 (AI-Engineer Pairing — agent must know how to find avatar)
"""

from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[3]


def test_agents_md_has_avatar_retrieval_protocol():
    """AGENTS.md must have a RAG retrieval protocol that can discover technology avatars."""
    agents_path = REPO_ROOT / "AGENTS.md"
    content = agents_path.read_text(encoding="utf-8")

    # Must have the wildcard avatar loading step
    assert "avatars/technology/" in content, "AGENTS.md must reference technology avatar path"
    assert "guidance.md" in content, "AGENTS.md must reference guidance.md for avatar loading"
    assert "skill index" in content.lower() or "index.yaml" in content, \
        "AGENTS.md must reference skill index for routing"
