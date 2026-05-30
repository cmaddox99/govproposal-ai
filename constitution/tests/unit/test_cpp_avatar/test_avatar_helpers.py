"""Test 2.7a: avatar_test_helpers module provides reusable governance validators.

Scenario ID: c-plus-plus-avatar-enrichment/2.7a
Law: ENG-4.1, ENG-10.1
"""

import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[3]
AVATAR_DIR = REPO_ROOT / "avatars" / "technology" / "cpp"
LAWS_DIR = REPO_ROOT / "laws"

# Ensure constitution-lint is importable
sys.path.insert(0, str(REPO_ROOT / "tools" / "constitution-lint" / "src"))


def test_avatar_test_helpers_provides_governance_validators():
    """avatar_test_helpers must export all 6 governance validator functions."""
    from tests.unit.test_cpp_avatar import avatar_test_helpers as h

    required_functions = [
        "load_manifest",
        "validate_law_references",
        "check_example_file_exists",
        "check_token_budget",
        "check_parity_sections",
        "check_citation_format",
    ]

    for fn_name in required_functions:
        assert hasattr(h, fn_name), f"avatar_test_helpers missing function: {fn_name}"
        assert callable(getattr(h, fn_name)), f"{fn_name} must be callable"

    # Smoke-test: load_manifest returns a dict with 'avatar' key
    manifest = h.load_manifest(AVATAR_DIR / "manifest.yaml")
    assert isinstance(manifest, dict), "load_manifest must return a dict"
    assert "avatar" in manifest, "loaded manifest must contain 'avatar' key"

    # Smoke-test: validate_law_references returns a list of results
    results = h.validate_law_references(manifest, LAWS_DIR)
    assert isinstance(results, list), "validate_law_references must return a list"

    # Smoke-test: check_token_budget returns (bool, int)
    # Use the guidance.md as a test file (it exists and is large enough)
    guidance_path = AVATAR_DIR / "guidance.md"
    passes, token_count = h.check_token_budget(guidance_path, max_tokens=999999)
    assert isinstance(passes, bool), "check_token_budget must return bool as first element"
    assert isinstance(token_count, int), "check_token_budget must return int as second element"

    # Smoke-test: check_citation_format returns a list of violations
    content = "[ENG-4.1](laws/engineering/eng-4-testing.md) is good. ENG-6.1 is bare."
    violations = h.check_citation_format(content)
    assert isinstance(violations, list), "check_citation_format must return a list"
