"""Test ESE-31: ENG-6.1-condition-variable.md example file.

Scenario ID: cpp-external-sources-enrichment/ESE-31
Law: ENG-6.1 (Security by Design)
cpp_version_min: 11
"""

from pathlib import Path

EXAMPLES = (
    Path(__file__).resolve().parents[3]
    / "avatars/technology/cpp/examples"
)
EXAMPLE = EXAMPLES / "ENG-6.1-condition-variable.md"
INDEX = EXAMPLES / "ENG-6.1-index.md"


def test_condition_variable_example_exists():
    """ENG-6.1-condition-variable.md must exist: bounded queue with predicate
    wait, NON-COMPLIANT bare wait(), lost-wakeup edge case, notify before wait,
    cv with stop_token, COMPLIANT/NON-COMPLIANT, ≤ 700 tokens."""
    assert EXAMPLE.exists(), "ENG-6.1-condition-variable.md not found"
    content = EXAMPLE.read_text(encoding="utf-8")

    assert "condition_variable" in content, "Must cover condition_variable"
    assert "predicate" in content.lower() or "wait(lk," in content, \
        "Must show predicate-protected wait"
    assert "spurious" in content.lower(), "Must explain spurious wakeup"
    assert "stop_token" in content or "stop_source" in content, \
        "Must show cv with stop_token (condition_variable_any)"
    assert "COMPLIANT" in content, "Must have COMPLIANT example"
    assert "NON-COMPLIANT" in content, "Must have NON-COMPLIANT example"
    assert "edge" in content.lower() or "Edge" in content, \
        "Must include edge cases"
    assert len(content) // 4 <= 700, \
        f"ENG-6.1-condition-variable.md exceeds 700-token budget (got {len(content)//4})"


def test_condition_variable_registered_in_index():
    """ENG-6.1-condition-variable.md must be listed in ENG-6.1-index.md."""
    assert INDEX.exists(), "ENG-6.1-index.md not found"
    assert "condition-variable" in INDEX.read_text(encoding="utf-8"), \
        "ENG-6.1-condition-variable.md must be registered in ENG-6.1-index.md"


def test_example_file_count_is_83():
    """Total example files must be 83 after ESE-31 (new file)."""
    count = len(list(EXAMPLES.glob("*.md")))
    assert count == 87, f"Expected 87 example files, found {count}"
