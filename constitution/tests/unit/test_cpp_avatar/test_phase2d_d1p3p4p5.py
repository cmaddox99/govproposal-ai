"""
Phase 2D — D1-P3: ENG-6.1-smart-pointers-cpp11.md
D1-P4: ENG-3.1-sfinae-cpp11.md
D1-P5: ENG-6.1-format-string-safety.md

Tests for the three remaining D1 priority example files.
"""

import pathlib
import pytest

CPP_DIR = pathlib.Path(__file__).parent.parent.parent.parent / "avatars" / "technology" / "cpp"
EXAMPLES_DIR = CPP_DIR / "examples"


# ── D1-P3: ENG-6.1-smart-pointers-cpp11.md ──────────────────────────────────

class TestD1P3SmartPointersCpp11:
    """C++11 unique_ptr without make_unique; manual new/reset patterns."""

    F = EXAMPLES_DIR / "ENG-6.1-smart-pointers-cpp11.md"

    def test_file_exists(self):
        assert self.F.exists(), "ENG-6.1-smart-pointers-cpp11.md must exist (D1-P3)"

    def test_cpp_version_min_is_11(self):
        assert "cpp_version_min: 11" in self.F.read_text(encoding="utf-8")

    def test_covers_unique_ptr_manual_new(self):
        c = self.F.read_text(encoding="utf-8")
        # C++11 unique_ptr construction — no make_unique (that's C++14)
        assert "unique_ptr" in c and "new " in c, (
            "Must show unique_ptr<T>(new T(...)) — C++11 pattern before make_unique"
        )

    def test_covers_make_unique_callout(self):
        c = self.F.read_text(encoding="utf-8")
        assert "make_unique" in c, (
            "Must document make_unique as C++14 upgrade and explain absence in C++11"
        )

    def test_covers_shared_ptr(self):
        c = self.F.read_text(encoding="utf-8")
        assert "shared_ptr" in c, "Must cover shared_ptr patterns"

    def test_has_non_compliant(self):
        assert "NON-COMPLIANT" in self.F.read_text(encoding="utf-8")

    def test_has_edge_cases(self):
        assert "## Edge Cases" in self.F.read_text(encoding="utf-8")


# ── D1-P4: ENG-3.1-sfinae-cpp11.md ─────────────────────────────────────────

class TestD1P4SfinaeCpp11:
    """enable_if SFINAE patterns for C++11/14 teams pre-C++20."""

    F = EXAMPLES_DIR / "ENG-3.1-sfinae-cpp11.md"

    def test_file_exists(self):
        assert self.F.exists(), "ENG-3.1-sfinae-cpp11.md must exist (D1-P4)"

    def test_cpp_version_min_is_11(self):
        assert "cpp_version_min: 11" in self.F.read_text(encoding="utf-8")

    def test_covers_enable_if(self):
        c = self.F.read_text(encoding="utf-8")
        assert "enable_if" in c, "Must document std::enable_if SFINAE pattern"

    def test_covers_type_traits(self):
        c = self.F.read_text(encoding="utf-8")
        assert "type_traits" in c or "is_integral" in c or "is_same" in c, (
            "Must use <type_traits> predicates"
        )

    def test_covers_concepts_migration_path(self):
        c = self.F.read_text(encoding="utf-8")
        assert "C++20" in c or "concept" in c, (
            "Must document C++20 concepts as the migration target"
        )

    def test_has_non_compliant(self):
        assert "NON-COMPLIANT" in self.F.read_text(encoding="utf-8")

    def test_has_edge_cases(self):
        assert "## Edge Cases" in self.F.read_text(encoding="utf-8")


# ── D1-P5: ENG-6.1-format-string-safety.md ──────────────────────────────────

class TestD1P5FormatStringSafety:
    """printf safety → iostream → fmtlib → std::format progression."""

    F = EXAMPLES_DIR / "ENG-6.1-format-string-safety.md"

    def test_file_exists(self):
        assert self.F.exists(), "ENG-6.1-format-string-safety.md must exist (D1-P5)"

    def test_cpp_version_min_is_98(self):
        assert "cpp_version_min: 98" in self.F.read_text(encoding="utf-8")

    def test_covers_printf_risks(self):
        c = self.F.read_text(encoding="utf-8")
        assert "printf" in c, "Must document printf security risks"

    def test_covers_iostream(self):
        c = self.F.read_text(encoding="utf-8")
        assert "iostream" in c or "std::cout" in c or "std::cerr" in c, (
            "Must cover iostream (all versions)"
        )

    def test_covers_std_format(self):
        c = self.F.read_text(encoding="utf-8")
        assert "std::format" in c, "Must document std::format (C++20)"

    def test_covers_fmtlib_or_spdlog(self):
        c = self.F.read_text(encoding="utf-8")
        assert "fmt::" in c or "spdlog" in c or "fmtlib" in c, (
            "Must cover fmtlib/spdlog as C++11+ polyfill"
        )

    def test_has_non_compliant(self):
        assert "NON-COMPLIANT" in self.F.read_text(encoding="utf-8")

    def test_has_edge_cases(self):
        assert "## Edge Cases" in self.F.read_text(encoding="utf-8")
