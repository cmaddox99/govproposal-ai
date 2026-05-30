"""ESE-49: ENG-3.1-constinit.md example file.

Spec: cpp-external-sources-enrichment/tasks.md (ESE-49)
Laws: ENG-3.1 (Code Quality), ENG-4.1 (Atomic TDD)
"""
import pathlib

CPP_DIR = pathlib.Path(__file__).parent.parent.parent.parent / "avatars" / "technology" / "cpp"
EXAMPLE_FILE = CPP_DIR / "examples" / "ENG-3.1-constinit.md"


class TestConstinitExample:

    def test_file_exists(self):
        assert EXAMPLE_FILE.exists()

    def test_compliant_section(self):
        assert "COMPLIANT" in EXAMPLE_FILE.read_text()

    def test_noncompliant_section(self):
        assert "NON-COMPLIANT" in EXAMPLE_FILE.read_text()

    def test_constinit_keyword_present(self):
        assert "constinit" in EXAMPLE_FILE.read_text()

    def test_atomic_constinit_present(self):
        content = EXAMPLE_FILE.read_text()
        assert "atomic" in content.lower()

    def test_init_order_fiasco_mentioned(self):
        content = EXAMPLE_FILE.read_text()
        assert "fiasco" in content.lower() or "init-order" in content.lower() or "initialization order" in content.lower()

    def test_edge_cases_section_with_rows(self):
        content = EXAMPLE_FILE.read_text()
        assert "## Edge Cases" in content
        rows = [ln for ln in content.splitlines() if ln.strip().startswith("|")]
        assert len(rows) >= 5

    def test_token_budget(self):
        content = EXAMPLE_FILE.read_text()
        assert len(content) // 4 <= 700

    def test_file_count_87(self):
        count = len(list((CPP_DIR / "examples").glob("*.md")))
        assert count == 87, f"Expected 87, found {count}"
