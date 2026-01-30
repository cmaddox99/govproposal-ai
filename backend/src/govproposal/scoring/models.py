"""Scoring domain models."""

from datetime import datetime, timezone
from enum import Enum
from typing import Optional, List, Dict, Any
from uuid import uuid4

from sqlalchemy import DateTime, ForeignKey, String, Text
from sqlalchemy.dialects.postgresql import JSON, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from govproposal.db.base import Base


def _utc_now() -> datetime:
    """Return current UTC datetime."""
    return datetime.now(timezone.utc)


class ScoreFactorType(str, Enum):
    """Types of scoring factors."""

    SECTION_M_ALIGNMENT = "section_m_alignment"
    SOW_COVERAGE = "sow_coverage"
    PP_MAPPING = "pp_mapping"  # Past Performance mapping
    SECTION_L_COMPLIANCE = "section_l_compliance"
    TECHNICAL_DEPTH = "technical_depth"
    COMPLETENESS = "completeness"


class ReadinessLevel(str, Enum):
    """Readiness level for color team reviews."""

    READY = "ready"
    NEEDS_WORK = "needs_work"
    NOT_READY = "not_ready"


class ColorTeamType(str, Enum):
    """Color team review types."""

    PINK_TEAM = "pink_team"  # Outline/storyboard review
    RED_TEAM = "red_team"  # Full draft review
    GOLD_TEAM = "gold_team"  # Final review
    SUBMISSION = "submission"  # Ready to submit


# Default scoring weights (configurable per organization)
DEFAULT_SCORE_WEIGHTS: Dict[ScoreFactorType, float] = {
    ScoreFactorType.COMPLETENESS: 0.30,  # Basic completeness
    ScoreFactorType.TECHNICAL_DEPTH: 0.30,  # Technical content quality
    ScoreFactorType.SECTION_L_COMPLIANCE: 0.20,  # Format/instruction compliance
    ScoreFactorType.SECTION_M_ALIGNMENT: 0.20,  # Evaluation criteria alignment
}


class ProposalScore(Base):
    """Overall proposal relevance score."""

    __tablename__ = "proposal_scores"

    id: Mapped[str] = mapped_column(
        UUID(as_uuid=False), primary_key=True, default=lambda: str(uuid4())
    )
    proposal_id: Mapped[str] = mapped_column(
        UUID(as_uuid=False), nullable=False, index=True
    )
    score_date: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=_utc_now, nullable=False
    )
    overall_score: Mapped[int] = mapped_column(nullable=False)  # 0-100
    confidence_level: Mapped[str] = mapped_column(
        String(20), nullable=False
    )  # high, medium, low
    ai_model_used: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    created_by: Mapped[str] = mapped_column(UUID(as_uuid=False), nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=_utc_now, nullable=False
    )

    # Relationships
    factors: Mapped[List["ScoreFactor"]] = relationship(
        back_populates="score", cascade="all, delete-orphan"
    )
    explanations: Mapped[List["ScoreExplanation"]] = relationship(
        back_populates="score", cascade="all, delete-orphan"
    )


class ScoreFactor(Base):
    """Individual scoring factor result."""

    __tablename__ = "score_factors"

    id: Mapped[str] = mapped_column(
        UUID(as_uuid=False), primary_key=True, default=lambda: str(uuid4())
    )
    proposal_score_id: Mapped[str] = mapped_column(
        UUID(as_uuid=False),
        ForeignKey("proposal_scores.id", ondelete="CASCADE"),
        nullable=False,
    )
    factor_type: Mapped[str] = mapped_column(String(50), nullable=False)
    factor_weight: Mapped[float] = mapped_column(nullable=False)  # 0.0-1.0
    raw_score: Mapped[int] = mapped_column(nullable=False)  # 0-100
    weighted_score: Mapped[float] = mapped_column(nullable=False)
    evidence_summary: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    improvement_suggestions: Mapped[Optional[Dict[str, Any]]] = mapped_column(JSON, nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=_utc_now, nullable=False
    )

    # Relationships
    score: Mapped["ProposalScore"] = relationship(back_populates="factors")


class ScoreExplanation(Base):
    """Detailed explanation for transparency."""

    __tablename__ = "score_explanations"

    id: Mapped[str] = mapped_column(
        UUID(as_uuid=False), primary_key=True, default=lambda: str(uuid4())
    )
    proposal_score_id: Mapped[str] = mapped_column(
        UUID(as_uuid=False),
        ForeignKey("proposal_scores.id", ondelete="CASCADE"),
        nullable=False,
    )
    section: Mapped[str] = mapped_column(String(100), nullable=False)
    explanation_text: Mapped[str] = mapped_column(Text, nullable=False)
    supporting_evidence: Mapped[Optional[Dict[str, Any]]] = mapped_column(JSON, nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=_utc_now, nullable=False
    )

    # Relationships
    score: Mapped["ProposalScore"] = relationship(back_populates="explanations")


class ProposalBenchmark(Base):
    """Benchmark comparison for a proposal."""

    __tablename__ = "proposal_benchmarks"

    id: Mapped[str] = mapped_column(
        UUID(as_uuid=False), primary_key=True, default=lambda: str(uuid4())
    )
    proposal_id: Mapped[str] = mapped_column(
        UUID(as_uuid=False), nullable=False, index=True
    )
    benchmark_date: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=_utc_now, nullable=False
    )

    # Metrics
    completeness_score: Mapped[int] = mapped_column(nullable=False)
    technical_depth_score: Mapped[int] = mapped_column(nullable=False)
    compliance_score: Mapped[int] = mapped_column(nullable=False)

    # Historical comparison
    org_percentile: Mapped[Optional[int]] = mapped_column(
        nullable=True
    )  # Where this ranks vs org history
    org_avg_at_stage: Mapped[Optional[int]] = mapped_column(
        nullable=True
    )  # Avg score for proposals at same stage

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=_utc_now, nullable=False
    )


class ReadinessIndicator(Base):
    """Color team / submission readiness assessment."""

    __tablename__ = "readiness_indicators"

    id: Mapped[str] = mapped_column(
        UUID(as_uuid=False), primary_key=True, default=lambda: str(uuid4())
    )
    proposal_id: Mapped[str] = mapped_column(
        UUID(as_uuid=False), nullable=False, index=True
    )
    team_type: Mapped[str] = mapped_column(String(20), nullable=False)

    readiness_score: Mapped[int] = mapped_column(nullable=False)  # 0-100
    readiness_level: Mapped[str] = mapped_column(String(20), nullable=False)

    blockers: Mapped[Optional[List[Any]]] = mapped_column(JSON, nullable=True)  # Critical issues
    warnings: Mapped[Optional[List[Any]]] = mapped_column(
        JSON, nullable=True
    )  # Non-critical issues

    checked_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=_utc_now, nullable=False
    )
    checked_by: Mapped[str] = mapped_column(UUID(as_uuid=False), nullable=False)
