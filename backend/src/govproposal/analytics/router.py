"""Analytics API router."""

from typing import Annotated

from fastapi import APIRouter, Depends

from govproposal.identity.dependencies import CurrentUser, DbSession, require_org_member
from govproposal.analytics.schemas import AnalyticsOverviewResponse, DashboardResponse
from govproposal.analytics.service import AnalyticsService

router = APIRouter(prefix="/api/v1/organizations/{org_id}", tags=["analytics"])


def get_analytics_service(session: DbSession) -> AnalyticsService:
    return AnalyticsService(session)


AnalyticsSvc = Annotated[AnalyticsService, Depends(get_analytics_service)]


@router.get("/dashboard", response_model=DashboardResponse)
async def get_dashboard(
    org_id: str,
    current_user: CurrentUser,
    session: DbSession,
    service: AnalyticsSvc,
) -> DashboardResponse:
    """Get dashboard metrics for organization."""
    await require_org_member(org_id, current_user, session)
    metrics = await service.get_dashboard_metrics(org_id)
    pipeline = await service.get_pipeline_breakdown(org_id)
    recent = await service.get_recent_proposals(org_id)
    return DashboardResponse(
        **metrics,
        pipeline=pipeline,
        recent_proposals=recent,
    )


@router.get("/analytics", response_model=AnalyticsOverviewResponse)
async def get_analytics(
    org_id: str,
    current_user: CurrentUser,
    session: DbSession,
    service: AnalyticsSvc,
) -> AnalyticsOverviewResponse:
    """Get full analytics overview for organization."""
    await require_org_member(org_id, current_user, session)
    data = await service.get_analytics_overview(org_id)
    return AnalyticsOverviewResponse(**data)
