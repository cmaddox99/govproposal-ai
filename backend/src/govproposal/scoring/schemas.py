"""Pydantic schemas for scoring module."""

from datetime import datetime

from pydantic import BaseModel, Field


class ScoreFactorResponse(BaseModel):
    """Schema for score factor response."""

    id: str
    factor_type: str
    factor_weight: float
    raw_score: int
    weighted_score: float
    evidence_summary: str | None
    improvement_suggestions: list[dict] | None

    model_config = {"from_attributes": True}


class ScoreExplanationResponse(BaseModel):
    """Schema for score explanation response."""

    id: str
    section: str
    explanation_text: str
    supporting_evidence: dict | None

    model_config = {"from_attributes": True}


class ProposalScoreResponse(BaseModel):
    """Schema for proposal score response."""

    id: str
    proposal_id: str
    score_date: datetime
    overall_score: int
    confidence_level: str
    ai_model_used: str | None
    created_by: str
    created_at: datetime
    factors: list[ScoreFactorResponse]

    model_config = {"from_attributes": True}


class ProposalScoreSummaryResponse(BaseModel):
    """Schema for brief score summary."""

    id: str
    proposal_id: str
    score_date: datetime
    overall_score: int
    confidence_level: str

    model_config = {"from_attributes": True}


class ScoreCalculateRequest(BaseModel):
    """Schema for score calculation request."""

    force_recalculate: bool = False


class ScoreImprovementResponse(BaseModel):
    """Schema for score improvement suggestion."""

    priority: int
    factor: str
    current_score: int
    potential_gain: int
    action: str
    details: str


class ImprovementListResponse(BaseModel):
    """Schema for list of improvements."""

    proposal_id: str
    current_score: int
    improvements: list[ScoreImprovementResponse]


# Benchmark schemas


class BenchmarkResponse(BaseModel):
    """Schema for benchmark response."""

    id: str
    proposal_id: str
    benchmark_date: datetime
    completeness_score: int
    technical_depth_score: int
    compliance_score: int
    org_percentile: int | None
    org_avg_at_stage: int | None

    model_config = {"from_attributes": True}


# Readiness schemas


class BlockerItem(BaseModel):
    """Schema for readiness blocker."""

    category: str
    description: str
    section: str | None = None


class WarningItem(BaseModel):
    """Schema for readiness warning."""

    category: str
    description: str
    recommendation: str


class ReadinessResponse(BaseModel):
    """Schema for readiness assessment response."""

    id: str
    proposal_id: str
    team_type: str
    readiness_score: int
    readiness_level: str  # ready, needs_work, not_ready
    blockers: list[BlockerItem]
    warnings: list[WarningItem]
    checked_at: datetime
    checked_by: str

    model_config = {"from_attributes": True}


class ReadinessCheckRequest(BaseModel):
    """Schema for readiness check request."""

    force_recheck: bool = False


# Go/No-Go schemas


class GoNoGoSummary(BaseModel):
    """Schema for go/no-go decision summary."""

    proposal_id: str
    overall_score: int
    readiness_level: str
    recommendation: str  # "Proceed", "Proceed with caution", "Do not proceed"
    key_strengths: list[str]
    key_risks: list[str]
    next_steps: list[str]


# Score history


class ScoreHistoryResponse(BaseModel):
    """Schema for score history response."""

    proposal_id: str
    scores: list[ProposalScoreSummaryResponse]
    trend: str  # "improving", "declining", "stable"
