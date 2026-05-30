"""Test 1.2: C++ avatar guidance.md exists as a slim index; extended sections in full-reference.md.

Scenario ID: c-plus-plus-avatar-enrichment/1.2
Law: ENG-11.1, ENG-4.1
Amendment O V7: guidance.md rebuilt to ≤450 tokens; rich content moved to docs/guides/avatars/cpp/full-reference.md
Amendment P: full-reference.md relocated to avatars/technology/cpp/full-reference.md
"""

from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[3]
GUIDANCE_PATH = REPO_ROOT / "avatars" / "technology" / "cpp" / "guidance.md"
CPP_DIR = REPO_ROOT / "avatars" / "technology" / "cpp"


def _read_full_reference():
    """Read all ref-*.md files (replacing full-reference.md)."""
    return "\n".join(p.read_text(encoding="utf-8") for p in sorted(CPP_DIR.rglob("ref-*.md")))

# Required sections exist in full-reference.md (moved from guidance.md per Amendment O V7)
REQUIRED_HEADINGS = [
    "Overview",
    "Testing Framework",
    "Domain Modeling",
    "Anti-Patterns",
]


def test_cpp_guidance_exists_and_is_slim_index():
    """guidance.md must exist as a slim index (≤450 tokens) with a link to reference-index.md."""
    assert GUIDANCE_PATH.exists(), f"Missing {GUIDANCE_PATH.relative_to(REPO_ROOT)}"
    content = GUIDANCE_PATH.read_text(encoding="utf-8")
    # Must reference the extended reference docs (via index or ref-*.md)
    assert "reference-index" in content.lower() or "ref-" in content.lower(), (
        "guidance.md must contain a link to reference-index.md or ref-*.md files"
    )
    # Token budget check (word_count × 1.3 ≤ 450)
    estimated_tokens = int(len(content.split()) * 1.3)
    assert estimated_tokens <= 450, (
        f"guidance.md exceeds 450-token RAG budget: ~{estimated_tokens} tokens"
    )


def test_cpp_full_reference_has_required_sections():
    """Amendment O V7: extended sections moved to ref-*.md files — verify they are present there."""
    content = _read_full_reference()
    for heading in REQUIRED_HEADINGS:
        assert heading.lower() in content.lower(), (
            f"ref-*.md files missing required section: '{heading}' (moved from guidance.md per Amendment O V7)"
        )

