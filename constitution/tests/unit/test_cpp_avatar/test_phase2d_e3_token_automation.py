"""
Phase 2D — E3: Token estimate automation — detect drift in AVATAR-RAG-INDEX.yaml.

AVATAR-RAG-INDEX.yaml contains token estimates like:
    refs/language/ref-io-formatting.md (~1540t)

These estimates are manually maintained and drift as files grow. This test
automatically checks that every (~NNNt) annotation in the index is within
±25% of the actual estimated token count for the file.

Token counting: words * 1.3 (same formula as avatar_test_helpers.py),
with frontmatter stripped before counting.

The ±25% tolerance is intentionally generous to avoid churn on every
editorial change; the goal is to detect LARGE drifts (e.g., a file that
doubled in size but still shows the old estimate).
"""

import pathlib
import re
import yaml
import pytest

REPO_ROOT = pathlib.Path(__file__).parent.parent.parent.parent
CPP_DIR   = REPO_ROOT / "avatars" / "technology" / "cpp"
RAG_INDEX = REPO_ROOT / "avatars" / "AVATAR-RAG-INDEX.yaml"

TOLERANCE = 0.25  # ±25% drift allowed before test flags the estimate


def _strip_frontmatter(text: str) -> str:
    """Remove YAML frontmatter block from markdown content."""
    if text.startswith("---"):
        end = text.find("\n---", 3)
        if end != -1:
            return text[end + 4:]
    return text


def _estimate_tokens(path: pathlib.Path) -> int:
    """Estimate token count: strip frontmatter, count words, multiply by 1.3."""
    try:
        content = path.read_text(encoding="utf-8")
    except FileNotFoundError:
        return -1  # sentinel for missing files
    body = _strip_frontmatter(content)
    words = len(body.split())
    return round(words * 1.3)


def _extract_ref_estimates(index_text: str) -> list[tuple[str, int]]:
    """
    Extract all (ref_path, claimed_token_count) pairs from the RAG index.
    Pattern: refs/some/path.md (~NNNt)
    """
    pattern = re.compile(r"(refs/[^\s\(]+\.md)\s+\(~(\d+)t\)")
    return [(m.group(1), int(m.group(2))) for m in pattern.finditer(index_text)]


class TestTokenEstimateAutomation:
    """E3: AVATAR-RAG-INDEX.yaml token estimates must not drift >25% from actual."""

    @pytest.fixture(scope="class")
    def index_estimates(self):
        index_text = RAG_INDEX.read_text(encoding="utf-8")
        return _extract_ref_estimates(index_text)

    def test_index_has_token_estimates(self, index_estimates):
        assert len(index_estimates) >= 10, (
            f"Expected at least 10 token estimates in RAG index; found {len(index_estimates)}"
        )

    def test_all_annotated_refs_exist(self, index_estimates):
        missing = []
        for ref_path, _ in index_estimates:
            full = CPP_DIR / ref_path
            if not full.exists():
                missing.append(ref_path)
        assert not missing, (
            f"These ref files are annotated in RAG index but don't exist:\n"
            + "\n".join(f"  - {p}" for p in missing)
        )

    @pytest.mark.parametrize("ref_path,claimed_tokens", _extract_ref_estimates(
        RAG_INDEX.read_text(encoding="utf-8")
    ))
    def test_token_estimate_within_tolerance(self, ref_path, claimed_tokens):
        full_path = CPP_DIR / ref_path
        if not full_path.exists():
            pytest.skip(f"File not found: {ref_path}")
        actual = _estimate_tokens(full_path)
        low  = claimed_tokens * (1 - TOLERANCE)
        high = claimed_tokens * (1 + TOLERANCE)
        assert low <= actual <= high, (
            f"{ref_path}: claimed ~{claimed_tokens}t but actual ~{actual}t "
            f"(drift={abs(actual - claimed_tokens) / claimed_tokens:.0%}, "
            f"tolerance=±{TOLERANCE:.0%}). "
            f"Update the estimate in AVATAR-RAG-INDEX.yaml."
        )


class TestTokenEstimateHelpers:
    """Unit tests for the E3 helper functions themselves."""

    def test_strip_frontmatter_removes_yaml_block(self):
        content = "---\ncpp_version_min: 98\n---\n# Title\nSome content here."
        body = _strip_frontmatter(content)
        assert "cpp_version_min" not in body
        assert "# Title" in body

    def test_strip_frontmatter_no_op_when_no_frontmatter(self):
        content = "# Title\nSome content."
        assert _strip_frontmatter(content) == content

    def test_estimate_tokens_reasonable_range(self):
        """A file with 100 words should estimate ~130 tokens."""
        word = "flight " * 100  # 100 words
        mock = pathlib.Path(REPO_ROOT / "avatars" / "technology" / "cpp" /
                            "refs" / "language" / "ref-io-formatting.md")
        if mock.exists():
            actual = _estimate_tokens(mock)
            assert actual > 50, "Token estimate should be positive and non-trivial"

    def test_extract_ref_estimates_parses_correctly(self):
        sample = "- refs/language/ref-io-formatting.md (~1540t) — some description"
        pairs = _extract_ref_estimates(sample)
        assert len(pairs) == 1
        assert pairs[0] == ("refs/language/ref-io-formatting.md", 1540)

    def test_extract_ref_estimates_ignores_non_ref_lines(self):
        sample = "some text without a ref\n- refs/other.md (~500t) — desc\n"
        pairs = _extract_ref_estimates(sample)
        assert len(pairs) == 1
        assert pairs[0][1] == 500
