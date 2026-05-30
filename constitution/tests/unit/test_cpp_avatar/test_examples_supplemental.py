"""Test 3a.1–3a.9: All supplemental engineering-law example files exist and comply.

Scenario ID: c-plus-plus-avatar-enrichment/3a.1-3a.9
Law: ENG-4.1, ENG-10.1
"""

import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[3]
EXAMPLES_DIR = REPO_ROOT / "avatars" / "technology" / "cpp" / "examples"

sys.path.insert(0, str(REPO_ROOT / "tools" / "constitution-lint" / "src"))

SUPPLEMENTAL_EXAMPLES = [
    ("ENG-2.1", "ENG-2.1-aggregates.md"),
    ("ENG-2.2", "ENG-2.2-layers.md"),
    ("ENG-3.1", "ENG-3.1-complexity.md"),
    ("ENG-3.2", "ENG-3.2-immutability.md"),
    ("ENG-3.3", "ENG-3.3-demeter.md"),
    ("ENG-3.5", "ENG-3.5-naming.md"),
    ("ENG-4.2", "ENG-4.2-test-pyramid.md"),
    ("ENG-4.4", "ENG-4.4-test-structure.md"),
    ("ENG-6.5", "ENG-6.5-input-validation.md"),
]


@pytest.mark.parametrize("law_id,filename", SUPPLEMENTAL_EXAMPLES)
def test_supplemental_example_complies(law_id, filename):
    """Each supplemental example must exist with correct frontmatter,
    compliant/non-compliant sections, and stay under token budget."""
    from tests.unit.test_cpp_avatar.avatar_test_helpers import check_token_budget

    example_path = EXAMPLES_DIR / filename
    assert example_path.exists(), f"Missing examples/{filename}"

    content = example_path.read_text(encoding="utf-8")

    assert f"law_id: {law_id}" in content, f"Frontmatter must contain law_id: {law_id}"
    assert "avatar: cpp" in content, "Frontmatter must contain avatar: cpp"
    assert "COMPLIANT" in content, f"{filename} must have a COMPLIANT example"
    assert "NON-COMPLIANT" in content, f"{filename} must have a NON-COMPLIANT example"
    assert "```cpp" in content, f"{filename} must contain C++ code blocks"

    passes, tokens = check_token_budget(example_path, max_tokens=700)
    assert passes, f"{filename} exceeds 700 token budget (~{tokens} tokens)"
