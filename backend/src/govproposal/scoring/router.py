"""Scoring API router."""

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select

from govproposal.db.base import get_db
from govproposal.identity.dependencies import CurrentUser, DbSession
from govproposal.proposals.models import Proposal
from govproposal.scoring.models import ColorTeamType
from govproposal.scoring.schemas import (
    BenchmarkResponse,
    GoNoGoSummary,
    ImprovementListResponse,
    ProposalScoreResponse,
    ReadinessCheckRequest,
    ReadinessResponse,
    ScoreCalculateRequest,
    ScoreExplanationResponse,
    ScoreHistoryResponse,
)
from govproposal.scoring.service import BenchmarkService, ScoringService

router = APIRouter(prefix="/api/v1/proposals/{proposal_id}/score", tags=["scoring"])


def get_scoring_service(session: DbSession) -> ScoringService:
    """Get ScoringService instance."""
    return ScoringService(session)


def get_benchmark_service(session: DbSession) -> BenchmarkService:
    """Get BenchmarkService instance."""
    return BenchmarkService(session)


ScoringSvc = Annotated[ScoringService, Depends(get_scoring_service)]
BenchmarkSvc = Annotated[BenchmarkService, Depends(get_benchmark_service)]


@router.post("/calculate", response_model=ProposalScoreResponse)
async def calculate_score(
    proposal_id: str,
    data: ScoreCalculateRequest,
    current_user: CurrentUser,
    service: ScoringSvc,
) -> ProposalScoreResponse:
    """Calculate or recalculate proposal relevance score.

    If force_recalculate is False and a recent score exists, returns existing score.
    """
    # Check for existing recent score
    if not data.force_recalculate:
        existing = await service.get_latest_score(proposal_id)
        if existing:
            return existing

    # Fetch proposal content for AI scoring
    query = select(Proposal).where(Proposal.id == proposal_id)
    result = await service._session.execute(query)
    proposal = result.scalar_one_or_none()
    if not proposal:
        raise HTTPException(status_code=404, detail="Proposal not found")

    proposal_data = {
        "title": proposal.title,
        "description": proposal.description or "",
        "executive_summary": proposal.executive_summary or "",
        "technical_approach": proposal.technical_approach or "",
        "management_approach": proposal.management_approach or "",
        "past_performance": proposal.past_performance or "",
        "pricing_summary": proposal.pricing_summary or "",
    }

    return await service.calculate_score(
        proposal_id=proposal_id,
        user_id=current_user.id,
        proposal_data=proposal_data,
    )


@router.get("", response_model=ProposalScoreResponse | None)
async def get_current_score(
    proposal_id: str,
    current_user: CurrentUser,
    service: ScoringSvc,
) -> ProposalScoreResponse | None:
    """Get most recent score for proposal."""
    return await service.get_latest_score(proposal_id)


@router.get("/history", response_model=ScoreHistoryResponse)
async def get_score_history(
    proposal_id: str,
    current_user: CurrentUser,
    service: ScoringSvc,
    limit: Annotated[int, Query(ge=1, le=50)] = 10,
) -> ScoreHistoryResponse:
    """Get score history over time."""
    return await service.get_score_history(proposal_id, limit)


@router.get("/improvements", response_model=ImprovementListResponse)
async def get_improvements(
    proposal_id: str,
    current_user: CurrentUser,
    service: ScoringSvc,
) -> ImprovementListResponse:
    """Get prioritized list of improvements to increase score."""
    return await service.get_improvements(proposal_id)


# Benchmark endpoints


@router.get("/benchmarks", response_model=BenchmarkResponse | None)
async def get_benchmarks(
    proposal_id: str,
    current_user: CurrentUser,
    service: BenchmarkSvc,
) -> BenchmarkResponse | None:
    """Get benchmark comparison data."""
    benchmark = await service._benchmark_repo.get_latest_benchmark(proposal_id)
    if not benchmark:
        return None

    return BenchmarkResponse(
        id=benchmark.id,
        proposal_id=benchmark.proposal_id,
        benchmark_date=benchmark.benchmark_date,
        completeness_score=benchmark.completeness_score,
        technical_depth_score=benchmark.technical_depth_score,
        compliance_score=benchmark.compliance_score,
        org_percentile=benchmark.org_percentile,
        org_avg_at_stage=benchmark.org_avg_at_stage,
    )


@router.post("/benchmarks/calculate", response_model=BenchmarkResponse)
async def calculate_benchmarks(
    proposal_id: str,
    current_user: CurrentUser,
    service: BenchmarkSvc,
) -> BenchmarkResponse:
    """Calculate and store benchmark metrics."""
    return await service.calculate_benchmark(proposal_id)


# Readiness endpoints


@router.get("/readiness/{team_type}", response_model=ReadinessResponse | None)
async def get_readiness(
    proposal_id: str,
    team_type: ColorTeamType,
    current_user: CurrentUser,
    service: BenchmarkSvc,
) -> ReadinessResponse | None:
    """Get readiness assessment for color team."""
    return await service.get_readiness(proposal_id, team_type)


@router.post("/readiness/{team_type}/check", response_model=ReadinessResponse)
async def check_readiness(
    proposal_id: str,
    team_type: ColorTeamType,
    data: ReadinessCheckRequest,
    current_user: CurrentUser,
    service: BenchmarkSvc,
) -> ReadinessResponse:
    """Run readiness check for color team."""
    # Check for existing if not forcing recheck
    if not data.force_recheck:
        existing = await service.get_readiness(proposal_id, team_type)
        if existing:
            return existing

    return await service.check_readiness(
        proposal_id=proposal_id,
        team_type=team_type,
        user_id=current_user.id,
    )


# Go/No-Go endpoint


@router.get("/go-no-go", response_model=GoNoGoSummary)
async def get_go_nogo_summary(
    proposal_id: str,
    current_user: CurrentUser,
    service: BenchmarkSvc,
) -> GoNoGoSummary:
    """Get go/no-go decision summary."""
    return await service.get_go_nogo_summary(proposal_id)
