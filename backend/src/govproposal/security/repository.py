"""Repository layer for security models."""

from datetime import datetime

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from govproposal.security.models import AuditLog, POAMItem, SecurityIncident


class AuditLogRepository:
    """Repository for audit log operations."""

    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def create(self, log: AuditLog) -> AuditLog:
        """Create a new audit log entry."""
        self._session.add(log)
        await self._session.flush()
        await self._session.refresh(log)
        return log

    async def list_logs(
        self,
        organization_id: str | None = None,
        event_type: str | None = None,
        actor_id: str | None = None,
        start_date: datetime | None = None,
        end_date: datetime | None = None,
        limit: int = 100,
        offset: int = 0,
    ) -> tuple[list[AuditLog], int]:
        """List audit logs with filtering and pagination."""
        query = select(AuditLog)

        if organization_id:
            query = query.where(AuditLog.organization_id == organization_id)
        if event_type:
            query = query.where(AuditLog.event_type == event_type)
        if actor_id:
            query = query.where(AuditLog.actor_id == actor_id)
        if start_date:
            query = query.where(AuditLog.event_time >= start_date)
        if end_date:
            query = query.where(AuditLog.event_time <= end_date)

        # Count query
        count_query = select(func.count()).select_from(query.subquery())
        count_result = await self._session.execute(count_query)
        total = count_result.scalar_one()

        # Apply pagination and ordering
        query = query.order_by(AuditLog.event_time.desc()).limit(limit).offset(offset)
        result = await self._session.execute(query)
        logs = list(result.scalars().all())

        return logs, total

    async def get_platform_logs(
        self,
        event_types: list[str] | None = None,
        start_date: datetime | None = None,
        end_date: datetime | None = None,
        limit: int = 100,
        offset: int = 0,
    ) -> tuple[list[AuditLog], int]:
        """Get platform-wide audit logs (for super users)."""
        query = select(AuditLog)

        if event_types:
            query = query.where(AuditLog.event_type.in_(event_types))
        if start_date:
            query = query.where(AuditLog.event_time >= start_date)
        if end_date:
            query = query.where(AuditLog.event_time <= end_date)

        count_query = select(func.count()).select_from(query.subquery())
        count_result = await self._session.execute(count_query)
        total = count_result.scalar_one()

        query = query.order_by(AuditLog.event_time.desc()).limit(limit).offset(offset)
        result = await self._session.execute(query)
        logs = list(result.scalars().all())

        return logs, total


class IncidentRepository:
    """Repository for security incident operations."""

    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def create(self, incident: SecurityIncident) -> SecurityIncident:
        """Create a new security incident."""
        self._session.add(incident)
        await self._session.flush()
        await self._session.refresh(incident)
        return incident

    async def get_by_id(self, incident_id: str) -> SecurityIncident | None:
        """Get incident by ID."""
        result = await self._session.execute(
            select(SecurityIncident).where(SecurityIncident.id == incident_id)
        )
        return result.scalar_one_or_none()

    async def get_by_number(self, incident_number: str) -> SecurityIncident | None:
        """Get incident by number."""
        result = await self._session.execute(
            select(SecurityIncident).where(
                SecurityIncident.incident_number == incident_number
            )
        )
        return result.scalar_one_or_none()

    async def update(self, incident: SecurityIncident) -> SecurityIncident:
        """Update an incident."""
        await self._session.flush()
        await self._session.refresh(incident)
        return incident

    async def list_incidents(
        self,
        status: str | None = None,
        severity: str | None = None,
        category: str | None = None,
        limit: int = 100,
        offset: int = 0,
    ) -> tuple[list[SecurityIncident], int]:
        """List incidents with filtering."""
        query = select(SecurityIncident)

        if status:
            query = query.where(SecurityIncident.status == status)
        if severity:
            query = query.where(SecurityIncident.severity == severity)
        if category:
            query = query.where(SecurityIncident.category == category)

        count_query = select(func.count()).select_from(query.subquery())
        count_result = await self._session.execute(count_query)
        total = count_result.scalar_one()

        query = (
            query.order_by(SecurityIncident.detected_at.desc()).limit(limit).offset(offset)
        )
        result = await self._session.execute(query)
        incidents = list(result.scalars().all())

        return incidents, total


class POAMRepository:
    """Repository for POAM operations."""

    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def create(self, item: POAMItem) -> POAMItem:
        """Create a new POAM item."""
        self._session.add(item)
        await self._session.flush()
        await self._session.refresh(item)
        return item

    async def get_by_id(self, item_id: str) -> POAMItem | None:
        """Get POAM item by ID."""
        result = await self._session.execute(
            select(POAMItem).where(POAMItem.id == item_id)
        )
        return result.scalar_one_or_none()

    async def update(self, item: POAMItem) -> POAMItem:
        """Update a POAM item."""
        await self._session.flush()
        await self._session.refresh(item)
        return item

    async def list_items(
        self,
        status: str | None = None,
        risk_level: str | None = None,
        limit: int = 100,
        offset: int = 0,
    ) -> tuple[list[POAMItem], int]:
        """List POAM items with filtering."""
        query = select(POAMItem)

        if status:
            query = query.where(POAMItem.status == status)
        if risk_level:
            query = query.where(POAMItem.risk_level == risk_level)

        count_query = select(func.count()).select_from(query.subquery())
        count_result = await self._session.execute(count_query)
        total = count_result.scalar_one()

        query = (
            query.order_by(POAMItem.scheduled_completion.asc().nullsfirst())
            .limit(limit)
            .offset(offset)
        )
        result = await self._session.execute(query)
        items = list(result.scalars().all())

        return items, total
