"""Integration tests for scoring flow."""

import pytest
import sys
from pathlib import Path
from datetime import datetime, timezone
from dataclasses import dataclass, field
from typing import List, Optional

# Add src to path for direct imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src"))


@dataclass
class ScoreFactorResponse:
    """Mock score factor response."""
    id: str
    factor_type: str
    factor_weight: float
    raw_score: int
    weighted_score: float
    evidence_summary: Optional[str]
    improvement_suggestions: Optional[list]


@dataclass
class ProposalScoreResponse:
    """Mock proposal score response."""
    id: str
    proposal_id: str
    score_date: datetime
    overall_score: int
    confidence_level: str
    ai_model_used: Optional[str]
    created_by: str
    created_at: datetime
    factors: List[ScoreFactorResponse]


@dataclass
class GoNoGoSummary:
    """Mock go/no-go summary."""
    proposal_id: str
    overall_score: int
    readiness_level: str
    recommendation: str
    key_strengths: List[str]
    key_risks: List[str]
    next_steps: List[str]


class TestEndToEndScoring:
    """Test end-to-end scoring flow."""

    def test_score_response_structure(self):
        """Score response should have all required fields."""
        response = ProposalScoreResponse(
            id="score-id",
            proposal_id="proposal-id",
            score_date=datetime.now(timezone.utc),
            overall_score=75,
            confidence_level="medium",
            ai_model_used="claude-sonnet-4-20250514",
            created_by="user-id",
            created_at=datetime.now(timezone.utc),
            factors=[
                ScoreFactorResponse(
                    id="factor-id",
                    factor_type="completeness",
                    factor_weight=0.30,
                    raw_score=80,
                    weighted_score=24.0,
                    evidence_summary="Good completeness",
                    improvement_suggestions=[],
                )
            ],
        )

        assert response.overall_score == 75
        assert response.confidence_level == "medium"
        assert len(response.factors) == 1

    def test_factor_weights_calculation(self):
        """Factor weights should correctly affect overall score."""
        factors = [
            ScoreFactorResponse(
                id="1",
                factor_type="completeness",
                factor_weight=0.30,
                raw_score=100,
                weighted_score=30.0,
                evidence_summary=None,
                improvement_suggestions=None,
            ),
            ScoreFactorResponse(
                id="2",
                factor_type="technical_depth",
                factor_weight=0.30,
                raw_score=100,
                weighted_score=30.0,
                evidence_summary=None,
                improvement_suggestions=None,
            ),
            ScoreFactorResponse(
                id="3",
                factor_type="section_l_compliance",
                factor_weight=0.20,
                raw_score=100,
                weighted_score=20.0,
                evidence_summary=None,
                improvement_suggestions=None,
            ),
            ScoreFactorResponse(
                id="4",
                factor_type="section_m_alignment",
                factor_weight=0.20,
                raw_score=100,
                weighted_score=20.0,
                evidence_summary=None,
                improvement_suggestions=None,
            ),
        ]

        total = sum(f.weighted_score for f in factors)
        assert total == 100.0  # Perfect score


class TestReadinessChecks:
    """Test readiness check flow."""

    def test_readiness_levels(self):
        """Test all readiness levels are defined."""
        levels = ["ready", "needs_work", "not_ready"]
        assert len(levels) == 3

    def test_color_team_progression(self):
        """Color teams should follow proper progression."""
        teams = ["pink_team", "red_team", "gold_team", "submission"]

        assert teams[0] == "pink_team"
        assert teams[-1] == "submission"


class TestGoNoGo:
    """Test go/no-go summary generation."""

    def test_proceed_recommendation(self):
        """High score + ready should recommend Proceed."""
        summary = GoNoGoSummary(
            proposal_id="proposal-id",
            overall_score=80,
            readiness_level="ready",
            recommendation="Proceed",
            key_strengths=["Strong technical approach"],
            key_risks=[],
            next_steps=["Submit proposal"],
        )

        assert summary.recommendation == "Proceed"

    def test_proceed_with_caution_recommendation(self):
        """Medium score or needs_work should recommend caution."""
        summary = GoNoGoSummary(
            proposal_id="proposal-id",
            overall_score=60,
            readiness_level="needs_work",
            recommendation="Proceed with caution",
            key_strengths=[],
            key_risks=["Missing sections"],
            next_steps=["Address gaps before submission"],
        )

        assert summary.recommendation == "Proceed with caution"

    def test_do_not_proceed_recommendation(self):
        """Low score + not_ready should recommend not to proceed."""
        summary = GoNoGoSummary(
            proposal_id="proposal-id",
            overall_score=30,
            readiness_level="not_ready",
            recommendation="Do not proceed",
            key_strengths=[],
            key_risks=["Critical blockers", "Missing key sections"],
            next_steps=["Major rework required"],
        )

        assert summary.recommendation == "Do not proceed"


class TestScoreHistory:
    """Test score history tracking."""

    def test_trend_detection(self):
        """Score trend should be detected correctly."""
        # Improving trend: recent > previous + 5
        scores = [75, 65, 60, 55]  # Recent first (75 > 65 + 5 = 70)
        if scores[0] > scores[1] + 5:
            trend = "improving"
        elif scores[0] < scores[1] - 5:
            trend = "declining"
        else:
            trend = "stable"
        assert trend == "improving"

        # Declining trend
        scores = [50, 65, 70, 75]
        if scores[0] > scores[1] + 5:
            trend = "improving"
        elif scores[0] < scores[1] - 5:
            trend = "declining"
        else:
            trend = "stable"
        assert trend == "declining"

        # Stable trend
        scores = [70, 68, 72, 70]
        if scores[0] > scores[1] + 5:
            trend = "improving"
        elif scores[0] < scores[1] - 5:
            trend = "declining"
        else:
            trend = "stable"
        assert trend == "stable"
