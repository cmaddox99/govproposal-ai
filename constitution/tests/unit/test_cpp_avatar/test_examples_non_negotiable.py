"""Test 3.2–3.18: All non-negotiable law example files exist and comply.

Scenario ID: c-plus-plus-avatar-enrichment/3.2-3.18
Law: ENG-4.1, ENG-10.1
"""

import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[3]
AVATAR_DIR = REPO_ROOT / "avatars" / "technology" / "cpp"
EXAMPLES_DIR = AVATAR_DIR / "examples"

sys.path.insert(0, str(REPO_ROOT / "tools" / "constitution-lint" / "src"))

NON_NEGOTIABLE_EXAMPLES = [
    ("ENG-6.1", "ENG-6.1-security-by-design.md"),
    ("ENG-6.4", "ENG-6.4-data-protection.md"),
    ("ENG-6.7", "ENG-6.7-audit-trail.md"),
]


@pytest.mark.parametrize("law_id,filename", NON_NEGOTIABLE_EXAMPLES)
def test_non_negotiable_example_complies(law_id, filename):
    """Each non-negotiable law example must exist with correct frontmatter,
    compliant/non-compliant sections, and stay under token budget."""
    from tests.unit.test_cpp_avatar.avatar_test_helpers import (
        check_token_budget, get_token_budget,
    )

    example_path = EXAMPLES_DIR / filename
    assert example_path.exists(), f"Missing examples/{filename}"

    content = example_path.read_text(encoding="utf-8")

    assert f"law_id: {law_id}" in content, f"Frontmatter must contain law_id: {law_id}"
    assert "avatar: cpp" in content, "Frontmatter must contain avatar: cpp"
    assert "COMPLIANT" in content, f"{filename} must have a COMPLIANT example"
    assert "NON-COMPLIANT" in content or "NON_COMPLIANT" in content, (
        f"{filename} must have a NON-COMPLIANT example"
    )

    budget = get_token_budget(AVATAR_DIR / "manifest.yaml")
    passes, tokens = check_token_budget(example_path, max_tokens=budget)
    assert passes, f"{filename} exceeds {budget}-token budget (~{tokens} tokens)"
