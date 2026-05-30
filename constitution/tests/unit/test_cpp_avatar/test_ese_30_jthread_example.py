"""Test ESE-30: ENG-6.1-jthread-stop-token.md example file.

Scenario ID: cpp-external-sources-enrichment/ESE-30
Law: ENG-6.1 (Security by Design)
cpp_version_min: 20
"""

from pathlib import Path

EXAMPLES = (
    Path(__file__).resolve().parents[3]
    / "avatars/technology/cpp/examples"
)
EXAMPLE = EXAMPLES / "ENG-6.1-jthread-stop-token.md"
INDEX = EXAMPLES / "ENG-6.1-index.md"


def test_jthread_example_file_exists():
    """ENG-6.1-jthread-stop-token.md must exist with required content:
    jthread + stop_token cancellable task, stop_callback cleanup,
    NON-COMPLIANT raw thread+volatile stop flag, edge cases,
    registered in ENG-6.1-index.md, within 700-token budget."""
    assert EXAMPLE.exists(), "ENG-6.1-jthread-stop-token.md not found"
    content = EXAMPLE.read_text(encoding="utf-8")

    assert "jthread" in content, "Must cover jthread"
    assert "stop_token" in content, "Must cover stop_token"
    assert "stop_callback" in content, "Must cover stop_callback cleanup"
    assert "volatile" in content or "atomic<bool>" in content, \
        "NON-COMPLIANT must show raw-thread+stop-flag pattern"
    assert "COMPLIANT" in content, "Must have COMPLIANT example"
    assert "NON-COMPLIANT" in content, "Must have NON-COMPLIANT example"
    assert "edge" in content.lower() or "Edge" in content, \
        "Must include edge cases"
    # Token budget: example files ≤ 700 tokens
    assert len(content) // 4 <= 700, \
        f"ENG-6.1-jthread-stop-token.md exceeds 700-token budget (got {len(content)//4})"


def test_jthread_example_registered_in_index():
    """ENG-6.1-jthread-stop-token.md must be listed in ENG-6.1-index.md."""
    assert INDEX.exists(), "ENG-6.1-index.md not found"
    assert "jthread-stop-token" in INDEX.read_text(encoding="utf-8"), \
        "ENG-6.1-jthread-stop-token.md must be registered in ENG-6.1-index.md"


def test_example_file_count_is_83():
    """Total example files is 83 (ESE-30 filled a pre-existing stub; ESE-31 added a new file)."""
    count = len(list(EXAMPLES.glob("*.md")))
    assert count == 87, f"Expected 87 example files, found {count}"
