"""ESE-46–47: ref-cpp20-features-part2.md — Aggregates + Calendar/Timezone sections.

Spec: cpp-external-sources-enrichment/tasks.md (ESE-46, ESE-47)
Laws: ENG-3.1 (Code Quality), ENG-4.1 (Atomic TDD)
"""
import pathlib

CPP_DIR = pathlib.Path(__file__).parent.parent.parent.parent / "avatars" / "technology" / "cpp"
REF_FILE = CPP_DIR / "refs" / "language" / "ref-cpp20-features-part2.md"

import pytest

@pytest.fixture(scope="module")
def content():
    return REF_FILE.read_text()


class TestC20AggregateImprovements:
    """ESE-46: C++20 Aggregate Improvements."""

    def test_section_heading_present(self, content):
        assert "Aggregate" in content

    def test_parenthesis_init_mentioned(self, content):
        assert "parenthesis" in content.lower() or "paren" in content.lower() or "FlightRequest(" in content

    def test_ctad_mentioned(self, content):
        assert "CTAD" in content or "deduction" in content.lower()

    def test_has_law_reference_in_body(self, content):
        idx = content.find("Aggregate")
        assert "[ENG-3.1]" in content[idx:idx+700]


class TestCalendarTimezone:
    """ESE-47: Calendar and Timezone (FAR 117 duty periods)."""

    def test_section_heading_present(self, content):
        assert "Calendar" in content or "Timezone" in content or "timezone" in content

    def test_year_month_day_mentioned(self, content):
        assert "year_month_day" in content

    def test_zoned_time_mentioned(self, content):
        assert "zoned_time" in content

    def test_far117_aviation_context(self, content):
        """Aviation context required: FAR 117 or duty period."""
        assert "FAR 117" in content or "duty" in content.lower() or "crew rest" in content.lower()

    def test_has_law_reference_in_body(self, content):
        idx = content.find("Calendar")
        if idx == -1:
            idx = content.find("Timezone")
        assert "[ENG-3.1]" in content[idx:idx+700]

    def test_token_budget(self):
        c = REF_FILE.read_text()
        assert len(c) // 4 <= 3500, f"Over budget: {len(c)//4}t"
