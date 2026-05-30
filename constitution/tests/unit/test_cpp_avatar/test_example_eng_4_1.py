"""Test 3.1: C++ avatar has ENG-4.1 Atomic TDD example file.

Scenario ID: c-plus-plus-avatar-enrichment/3.1
Law: ENG-4.1
"""

import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[3]
AVATAR_DIR = REPO_ROOT / "avatars" / "technology" / "cpp"
EXAMPLES_DIR = AVATAR_DIR / "examples"
LAWS_DIR = REPO_ROOT / "laws"

sys.path.insert(0, str(REPO_ROOT / "tools" / "constitution-lint" / "src"))


def test_cpp_eng_4_1_atomic_tdd_example():
    """ENG-4.1 example must exist with correct frontmatter, compliant and
    non-compliant C++ examples, and stay under token budget."""
    from tests.unit.test_cpp_avatar.avatar_test_helpers import (
        check_token_budget,
        validate_law_references,
        load_manifest,
    )

    example_path = EXAMPLES_DIR / "ENG-4.1-atomic-tdd.md"
    assert example_path.exists(), "Missing examples/ENG-4.1-atomic-tdd.md"

    content = example_path.read_text(encoding="utf-8")

    # Frontmatter must reference correct law and avatar
    assert "law_id: ENG-4.1" in content, "Frontmatter must contain law_id: ENG-4.1"
    assert "avatar: cpp" in content, "Frontmatter must contain avatar: cpp"

    # Must have compliant and non-compliant sections
    assert "COMPLIANT" in content, "Must have a COMPLIANT example"
    assert "NON-COMPLIANT" in content or "NON_COMPLIANT" in content, "Must have a NON-COMPLIANT example"

    # Must contain C++ code
    assert "```cpp" in content, "Must contain C++ code blocks"

    # Must reference GoogleTest
    assert "TEST_F" in content or "TEST(" in content, "Must use GoogleTest macros"

    # Token budget check
    passes, tokens = check_token_budget(example_path, max_tokens=600)
    assert passes, f"ENG-4.1 example exceeds 600 token budget (~{tokens} tokens)"
