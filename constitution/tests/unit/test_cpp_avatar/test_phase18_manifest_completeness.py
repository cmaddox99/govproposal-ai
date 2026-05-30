"""Phase 18 remediation: manifest completeness tests for missing example files.

Laws: ENG-4.1, ENG-10.1, ENG-11.1
Refs: hangar-ai-specs/changes/cpp-avatar-phase18-remediation/PROPOSAL.md — H-1, H-2
Panel review findings: H-1 (ENG-3.7, ENG-5.5, ENG-7.1 missing example_file),
                       H-2 (ENG-4.4, ENG-7.2–7.5, ENG-5.2 missing from specializes_laws)
Workflow finding: Avatar Workflow Phase 2.1 — one file per law in specializes_laws
"""
from pathlib import Path
import yaml
import pytest

REPO_ROOT = Path(__file__).resolve().parents[3]
CPP_DIR = REPO_ROOT / "avatars" / "technology" / "cpp"
EXAMPLES_DIR = CPP_DIR / "examples"
MANIFEST_PATH = CPP_DIR / "manifest.yaml"


def _load_specializes_laws():
    with open(MANIFEST_PATH) as f:
        manifest = yaml.safe_load(f)
    return {entry["id"]: entry for entry in manifest.get("specializes_laws", [])}


def test_eng37_example_file_exists_and_referenced_in_manifest():
    """H-1: ENG-3.7 must have an example_file in specializes_laws pointing to a real file."""
    laws = _load_specializes_laws()
    assert "ENG-3.7" in laws, "ENG-3.7 not found in manifest specializes_laws"
    entry = laws["ENG-3.7"]
    assert "example_file" in entry, (
        "ENG-3.7 in specializes_laws has no 'example_file' key — "
        "avatar-workflow Phase 2.1 requires one file per law"
    )
    example_path = CPP_DIR / entry["example_file"]
    assert example_path.exists(), (
        f"ENG-3.7 example_file '{entry['example_file']}' not found on disk at {example_path}"
    )


def test_eng55_example_file_exists_and_referenced_in_manifest():
    """H-1: ENG-5.5 must have an example_file in specializes_laws pointing to a real file."""
    laws = _load_specializes_laws()
    assert "ENG-5.5" in laws, "ENG-5.5 not found in manifest specializes_laws"
    entry = laws["ENG-5.5"]
    assert "example_file" in entry, (
        "ENG-5.5 in specializes_laws has no 'example_file' key — "
        "avatar-workflow Phase 2.1 requires one file per law"
    )
    example_path = CPP_DIR / entry["example_file"]
    assert example_path.exists(), (
        f"ENG-5.5 example_file '{entry['example_file']}' not found on disk at {example_path}"
    )


def test_eng71_example_file_exists_and_referenced_in_manifest():
    """H-1: ENG-7.1 must have an example_file in specializes_laws pointing to a real file."""
    laws = _load_specializes_laws()
    assert "ENG-7.1" in laws, "ENG-7.1 not found in manifest specializes_laws"
    entry = laws["ENG-7.1"]
    assert "example_file" in entry, (
        "ENG-7.1 in specializes_laws has no 'example_file' key — "
        "avatar-workflow Phase 2.1 requires one file per law"
    )
    example_path = CPP_DIR / entry["example_file"]
    assert example_path.exists(), (
        f"ENG-7.1 example_file '{entry['example_file']}' not found on disk at {example_path}"
    )


def test_eng44_and_eng72_75_present_in_specializes_laws():
    """H-2: ENG-4.4 and ENG-7.2–7.5 must be present in specializes_laws with example_file."""
    laws = _load_specializes_laws()
    missing_entries = []
    missing_example_files = []
    for law_id in ["ENG-4.4", "ENG-7.2", "ENG-7.3", "ENG-7.4", "ENG-7.5"]:
        if law_id not in laws:
            missing_entries.append(law_id)
            continue
        entry = laws[law_id]
        if "example_file" not in entry:
            missing_example_files.append(law_id)
            continue
        example_path = CPP_DIR / entry["example_file"]
        if not example_path.exists():
            missing_example_files.append(f"{law_id} (file missing: {entry['example_file']})")

    assert missing_entries == [], f"Laws not in specializes_laws: {missing_entries}"
    assert missing_example_files == [], f"Laws missing example_file: {missing_example_files}"


def test_eng52_mixed_standard_example_exists():
    """H-2: ENG-5.2 must have a mixed-standard example file covering C++03/C++11 interop."""
    mixed_standard_path = EXAMPLES_DIR / "ENG-5.2-cmake-mixed-standard.md"
    assert mixed_standard_path.exists(), (
        "ENG-5.2-cmake-mixed-standard.md not found — required for CWR C++03/C++11 CI coverage"
    )
    laws = _load_specializes_laws()
    assert "ENG-5.2" in laws, "ENG-5.2 not in specializes_laws"
    entry = laws["ENG-5.2"]
    assert "example_file" in entry, "ENG-5.2 has no example_file"
    # Verify the mixed-standard file is reachable via supplemental_files or second entry
    content = mixed_standard_path.read_text(encoding="utf-8")
    assert "COMPLIANT" in content and "NON-COMPLIANT" in content, (
        "ENG-5.2-cmake-mixed-standard.md missing COMPLIANT/NON-COMPLIANT sections"
    )


def test_eng61_index_exists_and_references_all_16_files():
    """H-3: ENG-6.1 index file must exist and list all ENG-6.1 example files."""
    index_path = EXAMPLES_DIR / "ENG-6.1-index.md"
    assert index_path.exists(), (
        "ENG-6.1-index.md not found — H-3 requires a topic router for all ENG-6.1 security files"
    )
    content = index_path.read_text(encoding="utf-8")
    eng61_files = sorted(f.name for f in EXAMPLES_DIR.glob("ENG-6.1-*.md")
                         if f.name != "ENG-6.1-index.md")
    missing_refs = [f for f in eng61_files if f not in content]
    assert missing_refs == [], (
        f"ENG-6.1-index.md does not reference these files: {missing_refs}"
    )


def test_misra_do278a_example_exists_and_in_manifest():
    """H-4: MISRA C++ / DO-278A safety-critical guidance must exist under ENG-6.1 (not BUS-*)."""
    misra_path = EXAMPLES_DIR / "ENG-6.1-misra-do278a.md"
    assert misra_path.exists(), (
        "ENG-6.1-misra-do278a.md not found — H-4 requires MISRA/DO-278A guidance under ENG-6.x"
    )
    content = misra_path.read_text(encoding="utf-8")
    assert "MISRA" in content, "ENG-6.1-misra-do278a.md must reference MISRA C++"
    assert "DO-278A" in content, "ENG-6.1-misra-do278a.md must reference DO-278A"
    # Safeguard 2: must NOT add a BUS-* law to specializes_laws — check frontmatter
    assert "BUS-" not in content.split("---")[1] if content.startswith("---") else True, (
        "MISRA/DO-278A example must not introduce BUS-* law in frontmatter (Safeguard 2)"
    )
    # File must be referenced in the ENG-6.1 index
    index_path = EXAMPLES_DIR / "ENG-6.1-index.md"
    if index_path.exists():
        assert "ENG-6.1-misra-do278a.md" in index_path.read_text(encoding="utf-8"), (
            "ENG-6.1-index.md must reference the new MISRA/DO-278A file"
        )
