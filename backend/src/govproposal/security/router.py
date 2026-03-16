"""Security API routers."""

from datetime import datetime, timezone
from typing import Annotated
from uuid import uuid4

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from govproposal.db.base import get_db
from govproposal.identity.dependencies import CurrentUser, DbSession, SuperUser, require_org_admin
from govproposal.security.models import SecurityIncident, POAMItem
from govproposal.security.schemas import (
    AuditLogListResponse,
    AuditLogResponse,
    SecurityIncidentCreate,
    SecurityIncidentListResponse,
    SecurityIncidentResponse,
    SecurityIncidentUpdate,
    POAMItemCreate,
    POAMItemListResponse,
    POAMItemResponse,
    POAMItemUpdate,
)
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


# --- Security Incidents ---


@audit_router.get(
    "/organizations/{org_id}/incidents",
    response_model=SecurityIncidentListResponse,
)
async def list_incidents(
    org_id: str,
    current_user: CurrentUser,
    session: DbSession,
    status: Annotated[str | None, Query()] = None,
    severity: Annotated[str | None, Query()] = None,
) -> SecurityIncidentListResponse:
    """List security incidents. Requires admin role."""
    await require_org_admin(org_id, current_user, session)
    q = select(SecurityIncident).order_by(SecurityIncident.detected_at.desc())
    if status:
        q = q.where(SecurityIncident.status == status)
    if severity:
        q = q.where(SecurityIncident.severity == severity)
    result = await session.execute(q)
    items = result.scalars().all()
    return SecurityIncidentListResponse(
        items=[SecurityIncidentResponse.model_validate(i) for i in items],
        total=len(items),
    )


@audit_router.post(
    "/organizations/{org_id}/incidents",
    response_model=SecurityIncidentResponse,
    status_code=201,
)
async def create_incident(
    org_id: str,
    data: SecurityIncidentCreate,
    current_user: CurrentUser,
    session: DbSession,
) -> SecurityIncidentResponse:
    """Create a security incident. Requires admin role."""
    await require_org_admin(org_id, current_user, session)

    # Generate incident number
    count_q = select(func.count()).select_from(SecurityIncident)
    count = (await session.execute(count_q)).scalar_one()
    incident_number = f"INC-{count + 1:04d}"

    incident = SecurityIncident(
        incident_number=incident_number,
        title=data.title,
        description=data.description,
        severity=data.severity,
        category=data.category,
        affected_systems=data.affected_systems,
        reported_by=current_user.id,
    )
    session.add(incident)
    await session.commit()
    await session.refresh(incident)
    return SecurityIncidentResponse.model_validate(incident)


@audit_router.put(
    "/organizations/{org_id}/incidents/{incident_id}",
    response_model=SecurityIncidentResponse,
)
async def update_incident(
    org_id: str,
    incident_id: str,
    data: SecurityIncidentUpdate,
    current_user: CurrentUser,
    session: DbSession,
) -> SecurityIncidentResponse:
    """Update a security incident. Requires admin role."""
    await require_org_admin(org_id, current_user, session)
    q = select(SecurityIncident).where(SecurityIncident.id == incident_id)
    incident = (await session.execute(q)).scalar_one_or_none()
    if not incident:
        raise HTTPException(status_code=404, detail="Incident not found")

    update_data = data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(incident, field, value)

    # Auto-set timestamps based on status
    now = datetime.now(timezone.utc)
    if data.status == "contained" and not incident.contained_at:
        incident.contained_at = now
    if data.status in ("resolved", "closed") and not incident.resolved_at:
        incident.resolved_at = now

    await session.commit()
    await session.refresh(incident)
    return SecurityIncidentResponse.model_validate(incident)


# --- POAM Items ---


@audit_router.get(
    "/organizations/{org_id}/poam",
    response_model=POAMItemListResponse,
)
async def list_poam_items(
    org_id: str,
    current_user: CurrentUser,
    session: DbSession,
    status: Annotated[str | None, Query()] = None,
) -> POAMItemListResponse:
    """List POAM items. Requires admin role."""
    await require_org_admin(org_id, current_user, session)
    q = select(POAMItem).order_by(POAMItem.scheduled_completion.asc().nullslast())
    if status:
        q = q.where(POAMItem.status == status)
    result = await session.execute(q)
    items = result.scalars().all()
    return POAMItemListResponse(
        items=[POAMItemResponse.model_validate(i) for i in items],
        total=len(items),
    )


@audit_router.post(
    "/organizations/{org_id}/poam",
    response_model=POAMItemResponse,
    status_code=201,
)
async def create_poam_item(
    org_id: str,
    data: POAMItemCreate,
    current_user: CurrentUser,
    session: DbSession,
) -> POAMItemResponse:
    """Create a POAM item. Requires admin role."""
    await require_org_admin(org_id, current_user, session)

    count_q = select(func.count()).select_from(POAMItem)
    count = (await session.execute(count_q)).scalar_one()
    poam_id = f"POAM-{count + 1:04d}"

    item = POAMItem(
        poam_id=poam_id,
        weakness_name=data.weakness_name,
        weakness_description=data.weakness_description,
        control_identifier=data.control_identifier,
        risk_level=data.risk_level,
        scheduled_completion=data.scheduled_completion,
        point_of_contact=data.point_of_contact,
        resources_required=data.resources_required,
    )
    session.add(item)
    await session.commit()
    await session.refresh(item)
    return POAMItemResponse.model_validate(item)


@audit_router.put(
    "/organizations/{org_id}/poam/{poam_item_id}",
    response_model=POAMItemResponse,
)
async def update_poam_item(
    org_id: str,
    poam_item_id: str,
    data: POAMItemUpdate,
    current_user: CurrentUser,
    session: DbSession,
) -> POAMItemResponse:
    """Update a POAM item. Requires admin role."""
    await require_org_admin(org_id, current_user, session)
    q = select(POAMItem).where(POAMItem.id == poam_item_id)
    item = (await session.execute(q)).scalar_one_or_none()
    if not item:
        raise HTTPException(status_code=404, detail="POAM item not found")

    update_data = data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(item, field, value)

    await session.commit()
    await session.refresh(item)
    return POAMItemResponse.model_validate(item)


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
