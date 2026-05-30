"""
Phase 18: Example quality gate — every non-index example file must contain
a ## Edge Cases & Warnings section.

Per ENG-4.1 each file's test is an independent parametrized case so each
constitutes its own Atomic TDD cycle (RED → GREEN → VERIFY → COMMIT).
"""

import os
import pytest

EXAMPLES_DIR = "avatars/technology/cpp/examples"


def _all_example_files():
    """Return sorted list of non-index .md files in the examples directory."""
    files = []
    for fname in sorted(os.listdir(EXAMPLES_DIR)):
        if not fname.endswith(".md"):
            continue
        path = os.path.join(EXAMPLES_DIR, fname)
        text = open(path, encoding="utf-8").read()
        # Router/index files (type: index) are excluded — edge cases go in the
        # individual topic files they route to, not in the router itself.
        if "type: index" in text:
            continue
        files.append(fname)
    return files


@pytest.mark.parametrize("filename", _all_example_files())
def test_every_example_has_edge_cases_section(filename):
    """Every example file must have a ## Edge Cases (or ## Edge Cases & Warnings) section.

    This is the quality gate for Phase 18. Each parametrized case is an
    independent Atomic TDD RED step per ENG-4.1.
    """
    path = os.path.join(EXAMPLES_DIR, filename)
    text = open(path, encoding="utf-8").read()
    assert "## Edge Cases" in text, (
        f"{filename} is missing '## Edge Cases & Warnings' section.\n"
        f"Add a table with ≥3 rows covering the most dangerous misapplications."
    )
