"""Security API routers."""

from datetime import datetime
from typing import Annotated

from fastapi import APIRouter, Depends, Query

from govproposal.db.base import get_db
from govproposal.identity.dependencies import CurrentUser, DbSession, SuperUser, require_org_admin
from govproposal.security.schemas import AuditLogListResponse, AuditLogResponse
from govproposal.security.service import AuditService

audit_router = APIRouter(prefix="/api/v1", tags=["audit"])


def get_audit_service(session: DbSession) -> AuditService:
    """Get AuditService instance."""
    return AuditService(session)


AuditSvc = Annotated[AuditService, Depends(get_audit_service)]


@audit_router.get(
    "/organizations/{org_id}/audit-logs", response_model=AuditLogListResponse
)
async def get_org_audit_logs(
    org_id: str,
    current_user: CurrentUser,
    session: DbSession,
    service: AuditSvc,
    event_type: Annotated[str | None, Query()] = None,
    actor_id: Annotated[str | None, Query()] = None,
    start_date: Annotated[datetime | None, Query()] = None,
    end_date: Annotated[datetime | None, Query()] = None,
    limit: Annotated[int, Query(ge=1, le=100)] = 50,
    offset: Annotated[int, Query(ge=0)] = 0,
) -> AuditLogListResponse:
    """Get organization audit logs. Requires admin role."""
    await require_org_admin(org_id, current_user, session)

    logs, total = await service.get_org_audit_logs(
        organization_id=org_id,
        event_type=event_type,
        actor_id=actor_id,
        start_date=start_date,
        end_date=end_date,
        limit=limit,
        offset=offset,
    )

    return AuditLogListResponse(
        items=[AuditLogResponse.model_validate(log) for log in logs],
        total=total,
        limit=limit,
        offset=offset,
    )


@audit_router.get("/platform/audit-logs", response_model=AuditLogListResponse)
async def get_platform_audit_logs(
    super_user: SuperUser,
    service: AuditSvc,
    event_types: Annotated[list[str] | None, Query()] = None,
    start_date: Annotated[datetime | None, Query()] = None,
    end_date: Annotated[datetime | None, Query()] = None,
    limit: Annotated[int, Query(ge=1, le=100)] = 50,
    offset: Annotated[int, Query(ge=0)] = 0,
) -> AuditLogListResponse:
    """Get system-wide audit logs. Requires super user role."""
    logs, total = await service.get_platform_audit_logs(
        event_types=event_types,
        start_date=start_date,
        end_date=end_date,
        limit=limit,
        offset=offset,
    )

    return AuditLogListResponse(
        items=[AuditLogResponse.model_validate(log) for log in logs],
        total=total,
        limit=limit,
        offset=offset,
    )
