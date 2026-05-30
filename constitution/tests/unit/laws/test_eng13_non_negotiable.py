"""
RED test — Phase 2 (D17): ENG-13.1 must be NON-NEGOTIABLE globally.

Ensemble deliberation ensemble-pr31-gap6-2026-04-15 (approved 2026-04-15) directed:
  - ENG-13.1 elevated from RECOMMENDED to NON-NEGOTIABLE globally
  - 30-day adoption window clause removed
  - All workflows bound immediately upon merge

Spec scenario: enrich-product-discovery-stage-a-f
"""
import re
from pathlib import Path

REPO_ROOT = Path(__file__).parents[3]
LAW_FILE = REPO_ROOT / "laws" / "engineering" / "artifact-rendering.md"


def _read_law_file() -> str:
    assert LAW_FILE.exists(), f"Law file not found: {LAW_FILE}"
    return LAW_FILE.read_text(encoding="utf-8")


def test_eng13_1_non_negotiable_in_yaml_frontmatter():
    """ENG-13.1 YAML frontmatter must have non_negotiable: true."""
    content = _read_law_file()
    # Extract YAML frontmatter (between first two --- markers)
    fm_match = re.match(r"^---\s*\n(.*?)\n---", content, re.DOTALL)
    assert fm_match, "No YAML frontmatter found in artifact-rendering.md"
    frontmatter = fm_match.group(1)

    # Find the ENG-13.1 law block within the frontmatter laws list
    # non_negotiable: true must appear after the ENG-13.1 id line
    eng13_section = re.search(
        r"id:\s*ENG-13\.1.*?(?=id:\s*ENG-13\.[2-9]|\Z)",
        frontmatter,
        re.DOTALL,
    )
    assert eng13_section, "ENG-13.1 id not found in laws frontmatter"
    eng13_block = eng13_section.group(0)

    assert "non_negotiable: true" in eng13_block, (
        "ENG-13.1 must have non_negotiable: true in YAML frontmatter. "
        f"Found block:\n{eng13_block}"
    )


def test_eng13_1_recommended_false_or_absent():
    """ENG-13.1 YAML frontmatter must NOT have recommended: true (it is now NON-NEGOTIABLE)."""
    content = _read_law_file()
    fm_match = re.match(r"^---\s*\n(.*?)\n---", content, re.DOTALL)
    assert fm_match, "No YAML frontmatter found"
    frontmatter = fm_match.group(1)

    eng13_section = re.search(
        r"id:\s*ENG-13\.1.*?(?=id:\s*ENG-13\.[2-9]|\Z)",
        frontmatter,
        re.DOTALL,
    )
    assert eng13_section, "ENG-13.1 not found"
    eng13_block = eng13_section.group(0)

    assert "recommended: true" not in eng13_block, (
        "ENG-13.1 must NOT have recommended: true — it has been elevated to NON-NEGOTIABLE. "
        f"Found block:\n{eng13_block}"
    )


def test_eng13_1_status_line_says_non_negotiable():
    """ENG-13.1 body text status line must say NON-NEGOTIABLE (not RECOMMENDED)."""
    content = _read_law_file()
    # Find the ENG-13.1 section body
    eng13_body = re.search(
        r"## ENG-13\.1.*?(?=## ENG-13\.[2-9]|\Z)",
        content,
        re.DOTALL,
    )
    assert eng13_body, "ENG-13.1 body section not found"
    body = eng13_body.group(0)

    assert "NON-NEGOTIABLE" in body, (
        "ENG-13.1 body section must contain 'NON-NEGOTIABLE' in the status line. "
        "The law was elevated from RECOMMENDED by ensemble deliberation ensemble-pr31-gap6-2026-04-15."
    )


def test_eng13_1_no_30_day_adoption_window():
    """ENG-13.1 body must NOT contain the 30-day adoption window clause."""
    content = _read_law_file()
    eng13_body = re.search(
        r"## ENG-13\.1.*?(?=## ENG-13\.[2-9]|\Z)",
        content,
        re.DOTALL,
    )
    assert eng13_body, "ENG-13.1 body section not found"
    body = eng13_body.group(0)

    assert "30-day" not in body.lower(), (
        "ENG-13.1 must not contain a '30-day adoption window' clause. "
        "This clause was removed by ensemble deliberation ensemble-pr31-gap6-2026-04-15. "
        "All workflows are bound immediately upon merge."
    )


def test_eng13_1_constitutional_change_record_present():
    """ENG-13.1 body must contain a Constitutional Change Record block."""
    content = _read_law_file()
    eng13_body = re.search(
        r"## ENG-13\.1.*?(?=## ENG-13\.[2-9]|\Z)",
        content,
        re.DOTALL,
    )
    assert eng13_body, "ENG-13.1 body section not found"
    body = eng13_body.group(0)

    assert "ensemble-pr31-gap6-2026-04-15" in body, (
        "ENG-13.1 body must contain a Constitutional Change Record referencing "
        "ensemble deliberation ensemble-pr31-gap6-2026-04-15."
    )
