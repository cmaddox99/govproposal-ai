"""Service layer for security operations."""

from datetime import datetime, timezone
from typing import Any

from sqlalchemy.ext.asyncio import AsyncSession

from govproposal.security.models import AuditEventType, AuditLog
from govproposal.security.repository import (
    AuditLogRepository,
    IncidentRepository,
    POAMRepository,
)


class AuditService:
    """Service for audit logging operations."""

    def __init__(self, session: AsyncSession) -> None:
        self._session = session
        self._repo = AuditLogRepository(session)

    async def log_event(
        self,
        event_type: AuditEventType | str,
        action: str,
        actor_id: str | None = None,
        actor_email: str | None = None,
        organization_id: str | None = None,
        resource_type: str | None = None,
        resource_id: str | None = None,
        outcome: str = "success",
        ip_address: str | None = None,
        user_agent: str | None = None,
        details: dict | None = None,
    ) -> AuditLog:
        """Log an audit event.

        Args:
            event_type: Type of event (from AuditEventType enum or string)
            action: Description of the action taken
            actor_id: ID of the user performing the action
            actor_email: Email of the actor (for display purposes)
            organization_id: Organization context for the action
            resource_type: Type of resource affected (e.g., "proposal", "user")
            resource_id: ID of the affected resource
            outcome: Result of the action ("success" or "failure")
            ip_address: Client IP address
            user_agent: Client user agent string
            details: Additional details as JSON

        Returns:
            Created AuditLog entry
        """
        event_type_str = (
            event_type.value if isinstance(event_type, AuditEventType) else event_type
        )

        log = AuditLog(
            event_type=event_type_str,
            action=action,
            actor_id=actor_id,
            actor_email=actor_email,
            organization_id=organization_id,
            resource_type=resource_type,
            resource_id=resource_id,
            outcome=outcome,
            ip_address=ip_address,
            user_agent=user_agent,
            details=details,
        )

        return await self._repo.create(log)

    async def get_org_audit_logs(
        self,
        organization_id: str,
        event_type: str | None = None,
        actor_id: str | None = None,
        start_date: datetime | None = None,
        end_date: datetime | None = None,
        limit: int = 100,
        offset: int = 0,
    ) -> tuple[list[AuditLog], int]:
        """Get audit logs for an organization."""
        return await self._repo.list_logs(
            organization_id=organization_id,
            event_type=event_type,
            actor_id=actor_id,
            start_date=start_date,
            end_date=end_date,
            limit=limit,
            offset=offset,
        )

    async def get_platform_audit_logs(
        self,
        event_types: list[str] | None = None,
        start_date: datetime | None = None,
        end_date: datetime | None = None,
        limit: int = 100,
        offset: int = 0,
    ) -> tuple[list[AuditLog], int]:
        """Get platform-wide audit logs (for super users)."""
        return await self._repo.get_platform_logs(
            event_types=event_types,
            start_date=start_date,
            end_date=end_date,
            limit=limit,
            offset=offset,
        )


class SecurityService:
    """Combined security service for incidents, POAM, and audit."""

    def __init__(self, session: AsyncSession) -> None:
        self._session = session
        self.audit = AuditService(session)
        self._incident_repo = IncidentRepository(session)
        self._poam_repo = POAMRepository(session)

    # Convenience methods for common audit events

    async def log_login_success(
        self,
        user_id: str,
        email: str,
        ip_address: str | None = None,
        user_agent: str | None = None,
    ) -> AuditLog:
        """Log successful login."""
        return await self.audit.log_event(
            event_type=AuditEventType.LOGIN_SUCCESS,
            action="User logged in successfully",
            actor_id=user_id,
            actor_email=email,
            ip_address=ip_address,
            user_agent=user_agent,
        )

    async def log_login_failure(
        self,
        email: str,
        ip_address: str | None = None,
        user_agent: str | None = None,
        reason: str | None = None,
    ) -> AuditLog:
        """Log failed login attempt."""
        return await self.audit.log_event(
            event_type=AuditEventType.LOGIN_FAILURE,
            action="Login attempt failed",
            actor_email=email,
            outcome="failure",
            ip_address=ip_address,
            user_agent=user_agent,
            details={"reason": reason} if reason else None,
        )

    async def log_mfa_event(
        self,
        event_type: AuditEventType,
        user_id: str,
        email: str,
        success: bool = True,
        ip_address: str | None = None,
    ) -> AuditLog:
        """Log MFA-related event."""
        return await self.audit.log_event(
            event_type=event_type,
            action=f"MFA event: {event_type.value}",
            actor_id=user_id,
            actor_email=email,
            outcome="success" if success else "failure",
            ip_address=ip_address,
        )

    async def log_user_management_event(
        self,
        event_type: AuditEventType,
        actor_id: str,
        actor_email: str,
        target_user_id: str,
        target_email: str,
        organization_id: str,
        details: dict | None = None,
    ) -> AuditLog:
        """Log user management event."""
        return await self.audit.log_event(
            event_type=event_type,
            action=f"User management: {event_type.value}",
            actor_id=actor_id,
            actor_email=actor_email,
            organization_id=organization_id,
            resource_type="user",
            resource_id=target_user_id,
            details={"target_email": target_email, **(details or {})},
        )

    async def log_platform_event(
        self,
        event_type: AuditEventType,
        actor_id: str,
        actor_email: str,
        action: str,
        details: dict | None = None,
    ) -> AuditLog:
        """Log platform-level event (super user actions)."""
        return await self.audit.log_event(
            event_type=event_type,
            action=action,
            actor_id=actor_id,
            actor_email=actor_email,
            details=details,
        )
