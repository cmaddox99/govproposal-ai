"""Integration tests — T-03/ADR-003 ReDoS regression guards.

Phase 4 §2 threat model T-03: crafted strings with deeply nested repetition
must not cause the regex engine to hang. Each pattern must scan a ≥10,000-char
adversarial string in under 100ms.

ADR-003 patterns tested:
1. Fenced block regex (backtick/tilde, re.DOTALL)
2. Inline code regex
3. Law ID regex (ENG|PRD|BUS)-N.N

All regexes are extracted from scanner.py to test them in isolation.
"""
from __future__ import annotations

import re
import time


# Regex patterns from scanner.py (keep in sync)
_FENCED_BLOCK_RE = re.compile(r"```.*?```|~~~.*?~~~", re.DOTALL)
_INLINE_CODE_RE = re.compile(r"`[^`]+`")
_LAW_ID_RE = re.compile(r"\b(ENG|PRD|BUS)-\d+\.\d+\b")

_THRESHOLD_MS = 100


def _elapsed_ms(pattern: re.Pattern, text: str) -> float:
    start = time.monotonic()
    pattern.findall(text)
    return (time.monotonic() - start) * 1000


class TestFencedBlockReDoS:
    def test_deeply_nested_backticks_under_threshold(self):
        """Adversarial: many unclosed backtick fences — must not catastrophically backtrack."""
        # 10,000 backtick sequences that don't form complete pairs
        text = "``" * 5000 + "a" * 100
        elapsed = _elapsed_ms(_FENCED_BLOCK_RE, text)
        assert elapsed < _THRESHOLD_MS, (
            f"Fenced block regex took {elapsed:.1f}ms on adversarial input "
            f"(threshold: {_THRESHOLD_MS}ms)"
        )

    def test_alternating_fences_under_threshold(self):
        """10,000-char string alternating ``` and ~~~ delimiters."""
        text = ("```code``` ~~~ text ~~~ " * 500)[:10_000]
        elapsed = _elapsed_ms(_FENCED_BLOCK_RE, text)
        assert elapsed < _THRESHOLD_MS

    def test_large_valid_fenced_block_under_threshold(self):
        """Single 10,000-char fenced block — DOTALL must not hang."""
        inner = "x" * 9990
        text = f"```\n{inner}\n```"
        elapsed = _elapsed_ms(_FENCED_BLOCK_RE, text)
        assert elapsed < _THRESHOLD_MS


class TestInlineCodeReDoS:
    def test_many_unclosed_backticks_under_threshold(self):
        """10,000 individual backtick chars — no pair closure."""
        text = "`" * 10_000
        elapsed = _elapsed_ms(_INLINE_CODE_RE, text)
        assert elapsed < _THRESHOLD_MS

    def test_many_small_inline_spans_under_threshold(self):
        """`word` repeated 2,000 times → 10,000 chars total."""
        text = "`word` " * 2_000
        elapsed = _elapsed_ms(_INLINE_CODE_RE, text)
        assert elapsed < _THRESHOLD_MS

    def test_large_text_no_inline_code_under_threshold(self):
        """10,000-char plain text with no backticks — regex must scan quickly."""
        text = "the quick brown fox jumps over the lazy dog " * 250
        elapsed = _elapsed_ms(_INLINE_CODE_RE, text)
        assert elapsed < _THRESHOLD_MS


class TestLawIdReDoS:
    def test_many_fake_id_prefixes_under_threshold(self):
        """10,000-char string with partial ENG-/PRD-/BUS- patterns."""
        text = "ENG- PRD- BUS- " * 700
        elapsed = _elapsed_ms(_LAW_ID_RE, text)
        assert elapsed < _THRESHOLD_MS

    def test_many_valid_ids_under_threshold(self):
        """2,000 valid law IDs — must scan in < 100ms."""
        text = " ".join(["ENG-3.5", "PRD-2.6", "BUS-7.1"] * 700)
        elapsed = _elapsed_ms(_LAW_ID_RE, text)
        assert elapsed < _THRESHOLD_MS

    def test_digit_sequences_under_threshold(self):
        """Long digit sequences near ENG prefix — no catastrophic backtrack."""
        text = "ENG-" + "1234567890." * 1_000
        elapsed = _elapsed_ms(_LAW_ID_RE, text)
        assert elapsed < _THRESHOLD_MS
