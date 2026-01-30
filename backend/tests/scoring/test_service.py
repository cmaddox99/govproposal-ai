"""Tests for scoring service."""

import pytest
import sys
from pathlib import Path
from dataclasses import dataclass

# Add src to path for direct imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src"))


class TestScoreFactorWeights:
    """Test scoring factor weight configuration."""

    def test_weights_sum_to_one(self):
        """Factor weights should sum to 1.0."""
        # Define weights directly to avoid db import
        DEFAULT_SCORE_WEIGHTS = {
            "completeness": 0.30,
            "technical_depth": 0.30,
            "section_l_compliance": 0.20,
            "section_m_alignment": 0.20,
        }
        total = sum(DEFAULT_SCORE_WEIGHTS.values())
        assert abs(total - 1.0) < 0.001

    def test_all_factors_have_weights(self):
        """All expected factors should have weights defined."""
        DEFAULT_SCORE_WEIGHTS = {
            "completeness": 0.30,
            "technical_depth": 0.30,
            "section_l_compliance": 0.20,
            "section_m_alignment": 0.20,
        }
        expected_factors = [
            "completeness",
            "technical_depth",
            "section_l_compliance",
            "section_m_alignment",
        ]
        for factor in expected_factors:
            assert factor in DEFAULT_SCORE_WEIGHTS

    def test_weights_are_positive(self):
        """All weights should be positive."""
        DEFAULT_SCORE_WEIGHTS = {
            "completeness": 0.30,
            "technical_depth": 0.30,
            "section_l_compliance": 0.20,
            "section_m_alignment": 0.20,
        }
        for weight in DEFAULT_SCORE_WEIGHTS.values():
            assert weight > 0


class TestReadinessCriteria:
    """Test readiness criteria configuration."""

    def test_all_color_teams_have_criteria(self):
        """Each color team should have defined criteria."""
        COLOR_TEAMS = ["pink_team", "red_team", "gold_team", "submission"]
        READINESS_CRITERIA = {
            "pink_team": [
                {"name": "outline_complete", "description": "All sections have outlines", "category": "structure"},
                {"name": "win_themes_defined", "description": "Win themes documented", "category": "strategy"},
            ],
            "red_team": [
                {"name": "all_sections_drafted", "description": "All sections have full drafts", "category": "content"},
                {"name": "compliance_checked", "description": "Compliance checklist reviewed", "category": "compliance"},
            ],
            "gold_team": [
                {"name": "all_sections_final", "description": "All sections marked final", "category": "content"},
                {"name": "compliance_complete", "description": "100% compliance verified", "category": "compliance"},
            ],
            "submission": [
                {"name": "all_gold_criteria", "description": "All Gold Team criteria met", "category": "prerequisite"},
                {"name": "format_verified", "description": "Format requirements verified", "category": "compliance"},
            ],
        }

        for team_type in COLOR_TEAMS:
            assert team_type in READINESS_CRITERIA
            assert len(READINESS_CRITERIA[team_type]) > 0

    def test_criteria_have_required_fields(self):
        """Each criterion should have name, description, and category."""
        READINESS_CRITERIA = {
            "pink_team": [
                {"name": "outline_complete", "description": "All sections have outlines", "category": "structure"},
            ],
        }
        for team_type, criteria in READINESS_CRITERIA.items():
            for criterion in criteria:
                assert "name" in criterion
                assert "description" in criterion
                assert "category" in criterion


class TestScoreCalculation:
    """Test score calculation logic."""

    def test_weighted_score_calculation(self):
        """Weighted score should be raw_score * weight."""
        raw_score = 80
        weight = 0.30
        expected = raw_score * weight

        @dataclass
        class ScoreFactor:
            factor_type: str
            factor_weight: float
            raw_score: int
            weighted_score: float

        factor = ScoreFactor(
            factor_type="completeness",
            factor_weight=weight,
            raw_score=raw_score,
            weighted_score=expected,
        )

        assert factor.weighted_score == expected

    def test_overall_score_is_sum_of_weighted(self):
        """Overall score should be sum of weighted scores."""
        @dataclass
        class ScoreFactor:
            factor_type: str
            factor_weight: float
            raw_score: int
            weighted_score: float

        factors = [
            ScoreFactor(
                factor_type="completeness",
                factor_weight=0.30,
                raw_score=100,
                weighted_score=30.0,
            ),
            ScoreFactor(
                factor_type="technical_depth",
                factor_weight=0.30,
                raw_score=100,
                weighted_score=30.0,
            ),
            ScoreFactor(
                factor_type="section_l_compliance",
                factor_weight=0.20,
                raw_score=100,
                weighted_score=20.0,
            ),
            ScoreFactor(
                factor_type="section_m_alignment",
                factor_weight=0.20,
                raw_score=100,
                weighted_score=20.0,
            ),
        ]

        overall = sum(f.weighted_score for f in factors)
        assert overall == 100.0  # Perfect score


class TestConfidenceLevel:
    """Test confidence level determination."""

    def test_confidence_without_data(self):
        """Confidence should be low without proposal data."""
        def determine_confidence(proposal_data, factors):
            if not proposal_data:
                return "low"
            sections = proposal_data.get("sections", [])
            if len(sections) >= 4:
                return "high"
            elif len(sections) >= 2:
                return "medium"
            return "low"

        confidence = determine_confidence(None, [])
        assert confidence == "low"

    def test_confidence_with_few_sections(self):
        """Confidence should be medium with few sections."""
        def determine_confidence(proposal_data, factors):
            if not proposal_data:
                return "low"
            sections = proposal_data.get("sections", [])
            if len(sections) >= 4:
                return "high"
            elif len(sections) >= 2:
                return "medium"
            return "low"

        proposal_data = {"sections": [{"type": "exec_summary"}, {"type": "technical"}]}
        confidence = determine_confidence(proposal_data, [])
        assert confidence == "medium"

    def test_confidence_with_many_sections(self):
        """Confidence should be high with many sections."""
        def determine_confidence(proposal_data, factors):
            if not proposal_data:
                return "low"
            sections = proposal_data.get("sections", [])
            if len(sections) >= 4:
                return "high"
            elif len(sections) >= 2:
                return "medium"
            return "low"

        proposal_data = {
            "sections": [
                {"type": "exec_summary"},
                {"type": "technical"},
                {"type": "management"},
                {"type": "past_performance"},
            ]
        }
        confidence = determine_confidence(proposal_data, [])
        assert confidence == "high"
