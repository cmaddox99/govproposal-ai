"""ESE-48: ENG-5.5-source-location.md example file.

Spec: cpp-external-sources-enrichment/tasks.md (ESE-48)
Laws: ENG-5.5 (Observability), ENG-4.1 (Atomic TDD)
"""
import pathlib

CPP_DIR = pathlib.Path(__file__).parent.parent.parent.parent / "avatars" / "technology" / "cpp"
EXAMPLE_FILE = CPP_DIR / "examples" / "ENG-5.5-source-location.md"


class TestSourceLocationExample:

    def test_file_exists(self):
        assert EXAMPLE_FILE.exists()

    def test_compliant_section(self):
        assert "COMPLIANT" in EXAMPLE_FILE.read_text()

    def test_noncompliant_section(self):
        assert "NON-COMPLIANT" in EXAMPLE_FILE.read_text()

    def test_source_location_current(self):
        assert "source_location::current()" in EXAMPLE_FILE.read_text()

    def test_noncompliant_uses_macro(self):
        content = EXAMPLE_FILE.read_text()
        assert "__FILE__" in content or "__LINE__" in content

    def test_edge_cases_section_with_rows(self):
        content = EXAMPLE_FILE.read_text()
        assert "## Edge Cases" in content
        rows = [ln for ln in content.splitlines() if ln.strip().startswith("|")]
        assert len(rows) >= 5

    def test_token_budget(self):
        content = EXAMPLE_FILE.read_text()
        assert len(content) // 4 <= 700

    def test_file_count_86(self):
        count = len(list((CPP_DIR / "examples").glob("*.md")))
        assert count == 87, f"Expected 87, found {count}"
