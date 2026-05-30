"""
Phase 2D — D2: refs/language/ref-io-formatting.md

New reference file covering the full I/O progression:
printf (C++98, security risks), iostream (all versions),
fmtlib (C++11+ polyfill), std::format (C++20), std::print (C++23),
AA-specific spdlog guidance.
"""

import pathlib
import yaml
import pytest

REPO_ROOT = pathlib.Path(__file__).parent.parent.parent.parent
CPP_DIR   = REPO_ROOT / "avatars" / "technology" / "cpp"
REFS_DIR  = CPP_DIR / "refs"
RAG_INDEX = REPO_ROOT / "avatars" / "AVATAR-RAG-INDEX.yaml"

IO_REF = REFS_DIR / "language" / "ref-io-formatting.md"


class TestD2IoFormattingRef:
    """D2: ref-io-formatting.md covers C++98 -> C++23 I/O progression."""

    def test_ref_file_exists(self):
        assert IO_REF.exists(), "refs/language/ref-io-formatting.md must exist (D2)"

    def test_cpp_version_min_is_98(self):
        content = IO_REF.read_text(encoding="utf-8")
        assert "cpp_version_min: 98" in content, (
            "I/O ref covers printf (C++98) — minimum version must be 98"
        )

    def test_covers_printf_security(self):
        content = IO_REF.read_text(encoding="utf-8")
        assert "printf" in content and ("security" in content.lower() or "inject" in content.lower() or "format string" in content.lower()), (
            "Must document printf format string security risks"
        )

    def test_covers_iostream(self):
        content = IO_REF.read_text(encoding="utf-8")
        assert "iostream" in content or "std::cout" in content, (
            "Must cover iostream (all versions)"
        )

    def test_covers_fmtlib_or_spdlog(self):
        content = IO_REF.read_text(encoding="utf-8")
        assert "fmt::" in content or "spdlog" in content or "fmtlib" in content, (
            "Must cover fmtlib/spdlog as C++11+ polyfill"
        )

    def test_covers_std_format(self):
        content = IO_REF.read_text(encoding="utf-8")
        assert "std::format" in content, (
            "Must document std::format (C++20)"
        )

    def test_covers_std_print(self):
        content = IO_REF.read_text(encoding="utf-8")
        assert "std::print" in content, (
            "Must document std::print (C++23)"
        )

    def test_has_governance_rules(self):
        content = IO_REF.read_text(encoding="utf-8")
        assert "ENG-6.1" in content, (
            "Ref file must cite ENG-6.1 (security by design) for format string rules"
        )

    def test_routed_in_rag_index(self):
        index = yaml.safe_load(RAG_INDEX.read_text(encoding="utf-8"))
        cpp = index.get("technology_avatars", {}).get("cpp", {})
        files_text   = str(cpp.get("files", {}))
        queries_text = str(cpp.get("search_queries", []))
        combined = files_text + queries_text
        assert "ref-io-formatting" in combined, (
            "ref-io-formatting.md must be referenced in AVATAR-RAG-INDEX.yaml"
        )
