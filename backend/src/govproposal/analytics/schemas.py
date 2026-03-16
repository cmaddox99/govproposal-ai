"""Pydantic schemas for analytics module."""

from pydantic import BaseModel


class PipelineStage(BaseModel):
    status: str
    count: int


class RecentProposal(BaseModel):
    id: str
    title: str
    agency: str | None
    status: str
    estimated_value: float | None
    due_date: str | None
    updated_at: str


class DashboardResponse(BaseModel):
    active_proposals: int
    new_opportunities: int
    win_rate: float
    pending_deadlines: int
    pipeline: list[PipelineStage]
    recent_proposals: list[RecentProposal]


class AnalyticsOverviewResponse(BaseModel):
    active_proposals: int
    new_opportunities: int
    win_rate: float
    pending_deadlines: int
    pipeline: list[PipelineStage]
    recent_proposals: list[RecentProposal]
    total_contract_value: float
    total_submitted: int
    average_score: float


class TrendPoint(BaseModel):
    month: str
    proposals_created: int
    proposals_submitted: int
    proposals_awarded: int
    avg_score: float | None


class ScoreTrend(BaseModel):
    proposal_id: str
    title: str
    scores: list[dict]


class TrendsResponse(BaseModel):
    monthly_activity: list[TrendPoint]
    score_trends: list[ScoreTrend]
    top_agencies: list[dict]
