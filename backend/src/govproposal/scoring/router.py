"""Scoring API router.

Constitutional compliance:
- Art. I 1.3: Org membership verified on every endpoint
- Art. VIII 8.3: All scoring actions audit-logged
"""

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query, Request
from sqlalchemy import select, and_

from govproposal.db.base import get_db
from govproposal.identity.dependencies import CurrentUser, DbSession
from govproposal.identity.models import OrganizationMember
from govproposal.proposals.models import Proposal
from govproposal.scoring.models import ColorTeamType
from govproposal.scoring.schemas import (
    BenchmarkResponse,
    GoNoGoSummary,
    ImprovementListResponse,
    ProposalScoreResponse,
    ReadinessResponse,
    ScoreCalculateRequest,
    ReadinessCheckRequest,
    ScoreHistoryResponse,
)
from govproposal.scoring.service import BenchmarkService, ScoringService
from govproposal.events.bus import Event, event_bus
from govproposal.events.types import EventTypes
from govproposal.security.service import AuditService

router = APIRouter(prefix="/api/v1/proposals/{proposal_id}/score", tags=["scoring"])


def get_scoring_service(session: DbSession) -> ScoringService:
    return ScoringService(session)


def get_benchmark_service(session: DbSession) -> BenchmarkService:
    return BenchmarkService(session)


ScoringSvc = Annotated[ScoringService, Depends(get_scoring_service)]
BenchmarkSvc = Annotated[BenchmarkService, Depends(get_benchmark_service)]


async def _verify_proposal_access(
    proposal_id: str,
    user_id: str,
    session: DbSession,
) -> Proposal:
    """Fetch proposal and verify org membership. Art. I 1.3."""
    query = select(Proposal).where(Proposal.id == proposal_id)
    result = await session.execute(query)
    proposal = result.scalar_one_or_none()
    if not proposal:
        raise HTTPException(status_code=404, detail="Proposal not found")

    member = (await session.execute(
        select(OrganizationMember).where(and_(
            OrganizationMember.organization_id == proposal.organization_id,
            OrganizationMember.user_id == user_id,
        ))
    )).scalar_one_or_none()
    if not member:
        raise HTTPException(status_code=403, detail="Not a member of this organization")

    return proposal


@router.post("/calculate", response_model=ProposalScoreResponse)
async def calculate_score(
    proposal_id: str,
    data: ScoreCalculateRequest,
    current_user: CurrentUser,
    session: DbSession,
    service: ScoringSvc,
    request: Request,
) -> ProposalScoreResponse:
    """Calculate or recalculate proposal relevance score."""
    proposal = await _verify_proposal_access(proposal_id, current_user.id, session)

    if not data.force_recalculate:
        existing = await service.get_latest_score(proposal_id)
        if existing:
            return existing

    proposal_data = {
        "title": proposal.title,
        "description": proposal.description or "",
        "executive_summary": proposal.executive_summary or "",
        "technical_approach": proposal.technical_approach or "",
        "management_approach": proposal.management_approach or "",
        "past_performance": proposal.past_performance or "",
        "pricing_summary": proposal.pricing_summary or "",
    }

    result = await service.calculate_score(
        proposal_id=proposal_id,
        user_id=current_user.id,
        proposal_data=proposal_data,
    )

    audit = AuditService(session)
    await audit.log_event(
        event_type="proposal_scored",
        action="Proposal score calculated",
        actor_id=current_user.id,
        actor_email=current_user.email,
        organization_id=proposal.organization_id,
        resource_type="proposal",
        resource_id=proposal_id,
        ip_address=request.client.host if request.client else None,
        details={"overall_score": result.overall_score},
    )

    await event_bus.publish(Event(
        type=EventTypes.PROPOSAL_SCORED,
        data={
            "proposal_id": proposal_id,
            "overall_score": result.overall_score,
            "organization_id": proposal.organization_id,
            "actor_id": current_user.id,
        },
    ))

    return result


@router.get("", response_model=ProposalScoreResponse | None)
async def get_current_score(
    proposal_id: str,
    current_user: CurrentUser,
    session: DbSession,
    service: ScoringSvc,
) -> ProposalScoreResponse | None:
    """Get most recent score for proposal."""
    await _verify_proposal_access(proposal_id, current_user.id, session)
    return await service.get_latest_score(proposal_id)


@router.get("/history", response_model=ScoreHistoryResponse)
async def get_score_history(
    proposal_id: str,
    current_user: CurrentUser,
    session: DbSession,
    service: ScoringSvc,
    limit: Annotated[int, Query(ge=1, le=50)] = 10,
) -> ScoreHistoryResponse:
    """Get score history over time."""
    await _verify_proposal_access(proposal_id, current_user.id, session)
    return await service.get_score_history(proposal_id, limit)


@router.get("/improvements", response_model=ImprovementListResponse)
async def get_improvements(
    proposal_id: str,
    current_user: CurrentUser,
    session: DbSession,
    service: ScoringSvc,
) -> ImprovementListResponse:
    """Get prioritized list of improvements to increase score."""
    await _verify_proposal_access(proposal_id, current_user.id, session)
    return await service.get_improvements(proposal_id)


@router.get("/benchmarks", response_model=BenchmarkResponse | None)
async def get_benchmarks(
    proposal_id: str,
    current_user: CurrentUser,
    session: DbSession,
    service: BenchmarkSvc,
) -> BenchmarkResponse | None:
    """Get benchmark comparison data."""
    await _verify_proposal_access(proposal_id, current_user.id, session)
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
    session: DbSession,
    service: BenchmarkSvc,
    request: Request,
) -> BenchmarkResponse:
    """Calculate and store benchmark metrics."""
    proposal = await _verify_proposal_access(proposal_id, current_user.id, session)
    result = await service.calculate_benchmark(proposal_id)

    audit = AuditService(session)
    await audit.log_event(
        event_type="proposal_scored",
        action="Benchmark calculated",
        actor_id=current_user.id,
        actor_email=current_user.email,
        organization_id=proposal.organization_id,
        resource_type="proposal",
        resource_id=proposal_id,
        ip_address=request.client.host if request.client else None,
    )

    return result


@router.get("/readiness/{team_type}", response_model=ReadinessResponse | None)
async def get_readiness(
    proposal_id: str,
    team_type: ColorTeamType,
    current_user: CurrentUser,
    session: DbSession,
    service: BenchmarkSvc,
) -> ReadinessResponse | None:
    """Get readiness assessment for color team."""
    await _verify_proposal_access(proposal_id, current_user.id, session)
    return await service.get_readiness(proposal_id, team_type)


@router.post("/readiness/{team_type}/check", response_model=ReadinessResponse)
async def check_readiness(
    proposal_id: str,
    team_type: ColorTeamType,
    data: ReadinessCheckRequest,
    current_user: CurrentUser,
    session: DbSession,
    service: BenchmarkSvc,
    request: Request,
) -> ReadinessResponse:
    """Run readiness check for color team."""
    proposal = await _verify_proposal_access(proposal_id, current_user.id, session)

    if not data.force_recheck:
        existing = await service.get_readiness(proposal_id, team_type)
        if existing:
            return existing

    result = await service.check_readiness(
        proposal_id=proposal_id,
        team_type=team_type,
        user_id=current_user.id,
    )

    audit = AuditService(session)
    await audit.log_event(
        event_type="proposal_scored",
        action=f"Readiness check: {team_type.value}",
        actor_id=current_user.id,
        actor_email=current_user.email,
        organization_id=proposal.organization_id,
        resource_type="proposal",
        resource_id=proposal_id,
        ip_address=request.client.host if request.client else None,
        details={"team_type": team_type.value, "readiness_score": result.readiness_score},
    )

    return result


@router.get("/go-no-go", response_model=GoNoGoSummary)
async def get_go_nogo_summary(
    proposal_id: str,
    current_user: CurrentUser,
    session: DbSession,
    service: BenchmarkSvc,
) -> GoNoGoSummary:
    """Get go/no-go decision summary."""
    await _verify_proposal_access(proposal_id, current_user.id, session)
    return await service.get_go_nogo_summary(proposal_id)
