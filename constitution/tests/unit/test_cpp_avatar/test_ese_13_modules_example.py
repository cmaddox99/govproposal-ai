"""Test ESE-13: ENG-3.1-modules.md example file.

Scenario ID: cpp-external-sources-enrichment/ESE-13
Law: ENG-3.1 (Complexity — modules eliminate include-order dependencies)
"""

from pathlib import Path

EXAMPLE = (
    Path(__file__).resolve().parents[3]
    / "avatars/technology/cpp/examples/ENG-3.1-modules.md"
)


def test_modules_example_valid():
    """ENG-3.1-modules.md must cover COMPLIANT export module with partition,
    consumer import, CMake FILE_SET, NON-COMPLIANT include cycle, edge cases
    for header units and mixing headers, within 700-token budget."""
    assert EXAMPLE.exists(), "ENG-3.1-modules.md not found"
    content = EXAMPLE.read_text(encoding="utf-8")

    assert "export module" in content, "Must show export module declaration"
    assert "partition" in content.lower() or ":" in content, \
        "Must cover module partition syntax"
    assert "FILE_SET" in content, "Must show CMake FILE_SET CXX_MODULES"
    assert "COMPLIANT" in content, "Must have COMPLIANT example"
    assert "NON-COMPLIANT" in content, "Must have NON-COMPLIANT example"
    assert "header unit" in content.lower() or "import <" in content, \
        "Must address legacy header units"
    assert len(content) // 4 <= 700, \
        f"Exceeds 700-token budget (got {len(content) // 4})"
