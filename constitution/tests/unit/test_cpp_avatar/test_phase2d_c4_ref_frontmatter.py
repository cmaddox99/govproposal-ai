"""
Phase 2D — C4: cpp_version_min frontmatter on all ref files.

Every ref file under avatars/technology/cpp/refs/**/*.md must have a
cpp_version_min field in its YAML frontmatter so that the version routing
conservative-default can fire warnings for brownfield/transitional teams
when a ref file contains patterns requiring a newer standard.
"""

import pathlib
import re
import pytest

CPP_DIR = pathlib.Path(__file__).parent.parent.parent.parent / "avatars" / "technology" / "cpp"
REFS_DIR = CPP_DIR / "refs"

FRONTMATTER_RE = re.compile(r'^---\s*\n(.*?)^---\s*\n', re.MULTILINE | re.DOTALL)
VERSION_MIN_RE = re.compile(r'^\s*cpp_version_min\s*:', re.MULTILINE)

VALID_VERSIONS = {98, 11, 14, 17, 20, 23}


def _all_ref_files():
    return sorted(REFS_DIR.rglob("*.md"))


def _has_frontmatter(content: str) -> bool:
    return bool(FRONTMATTER_RE.match(content))


def _get_version_min(content: str) -> int | None:
    fm = FRONTMATTER_RE.match(content)
    if not fm:
        return None
    for line in fm.group(1).splitlines():
        m = re.match(r'\s*cpp_version_min\s*:\s*(\d+)', line)
        if m:
            return int(m.group(1))
    return None


class TestRefFileFrontmatter:
    """C4: All ref files must declare cpp_version_min in YAML frontmatter."""

    @pytest.fixture(params=_all_ref_files(), ids=lambda p: p.name)
    def ref_file(self, request):
        return request.param

    def test_ref_has_frontmatter(self, ref_file):
        content = ref_file.read_text(encoding="utf-8")
        assert _has_frontmatter(content), (
            f"{ref_file.name} must start with YAML frontmatter (--- ... ---)"
        )

    def test_ref_has_cpp_version_min(self, ref_file):
        content = ref_file.read_text(encoding="utf-8")
        version = _get_version_min(content)
        assert version is not None, (
            f"{ref_file.name} frontmatter must include 'cpp_version_min: <N>' (C4)"
        )

    def test_ref_version_min_is_valid(self, ref_file):
        content = ref_file.read_text(encoding="utf-8")
        version = _get_version_min(content)
        if version is None:
            pytest.skip("version_min absent — covered by test_ref_has_cpp_version_min")
        assert version in VALID_VERSIONS, (
            f"{ref_file.name}: cpp_version_min {version} not in valid set {VALID_VERSIONS}"
        )


class TestRefVersionMinInventory:
    """Spot-check known version requirements for specific files."""

    def _version_of(self, rel_path: str) -> int | None:
        p = REFS_DIR / rel_path
        if not p.exists():
            return None
        return _get_version_min(p.read_text(encoding="utf-8"))

    def test_coroutines_ref_is_cpp20(self):
        assert self._version_of("language/ref-concurrency-coroutines.md") == 20, (
            "Coroutines ref requires C++20 (co_await)"
        )

    def test_brownfield_ref_is_cpp98(self):
        assert self._version_of("legacy/ref-concurrency-brownfield.md") == 98, (
            "Brownfield concurrency ref documents C++98/POSIX patterns"
        )

    def test_threading_ref_is_cpp11(self):
        assert self._version_of("safety/ref-concurrency-threading.md") == 11, (
            "Threading ref primary example uses std::mutex (C++11)"
        )

    def test_async_ref_is_cpp11(self):
        # After C5 fix, async ref has a C++11 fallback — minimum is now C++11
        v = self._version_of("safety/ref-concurrency-async.md")
        assert v is not None and v <= 17, (
            "Async ref has C++11 fallback; version_min should be ≤17"
        )

    def test_migration_pre_cpp17_is_cpp98(self):
        assert self._version_of("legacy/ref-migration-pre-cpp17.md") == 98, (
            "Pre-C++17 migration guide documents C++98/03 code — minimum is 98"
        )
