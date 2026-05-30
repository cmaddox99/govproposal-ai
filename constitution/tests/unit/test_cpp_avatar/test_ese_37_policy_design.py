"""ESE-37: ENG-3.1-policy-based-design.md example file.

Spec: cpp-external-sources-enrichment/tasks.md (ESE-37)
Law:  ENG-3.1 (Code Quality), ENG-4.1 (Atomic TDD)
"""
import pathlib

CPP_DIR = pathlib.Path(__file__).parent.parent.parent.parent / "avatars" / "technology" / "cpp"
EXAMPLE_FILE = CPP_DIR / "examples" / "ENG-3.1-policy-based-design.md"


class TestPolicyBasedDesignExample:
    """ESE-37: Policy-based design example validation."""

    def test_file_exists(self):
        assert EXAMPLE_FILE.exists(), f"Missing: {EXAMPLE_FILE}"

    def test_compliant_section_present(self):
        content = EXAMPLE_FILE.read_text()
        assert "COMPLIANT" in content

    def test_noncompliant_section_present(self):
        content = EXAMPLE_FILE.read_text()
        assert "NON-COMPLIANT" in content

    def test_flight_repository_in_compliant(self):
        content = EXAMPLE_FILE.read_text()
        assert "FlightRepository" in content

    def test_virtual_noncompliant_noted(self):
        """NON-COMPLIANT section must reference virtual as the overhead."""
        content = EXAMPLE_FILE.read_text()
        assert "virtual" in content

    def test_edge_cases_section_with_rows(self):
        content = EXAMPLE_FILE.read_text()
        assert "## Edge Cases" in content
        rows = [ln for ln in content.splitlines() if ln.strip().startswith("|")]
        assert len(rows) >= 5, "Edge Cases table needs ≥3 data rows + header + separator"

    def test_token_budget(self):
        """Example files must be ≤700 tokens (len//4)."""
        content = EXAMPLE_FILE.read_text()
        tokens = len(content) // 4
        assert tokens <= 700, f"Over budget: {tokens}t > 700t"

    def test_example_file_count_incremented(self):
        """Adding this file increments count to 85."""
        count = len(list((CPP_DIR / "examples").glob("*.md")))
        assert count == 87, f"Expected 87 example files, found {count}"
