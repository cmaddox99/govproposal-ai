"""Security domain models."""

from datetime import datetime, timezone
from enum import Enum
from typing import Optional, List, Dict, Any
from uuid import uuid4

from sqlalchemy import DateTime, ForeignKey, String, Text
from sqlalchemy.dialects.postgresql import JSON, UUID
from sqlalchemy.orm import Mapped, mapped_column

from govproposal.db.base import Base


def _utc_now() -> datetime:
    """Return current UTC datetime."""
    return datetime.now(timezone.utc)


class AuditEventType(str, Enum):
    """Types of audit events."""

    # Authentication events
    LOGIN_SUCCESS = "login_success"
    LOGIN_FAILURE = "login_failure"
    LOGOUT = "logout"
    PASSWORD_CHANGE = "password_change"
    PASSWORD_RESET_REQUEST = "password_reset_request"
    PASSWORD_RESET_COMPLETE = "password_reset_complete"

    # MFA events
    MFA_SETUP_STARTED = "mfa_setup_started"
    MFA_SETUP_COMPLETED = "mfa_setup_completed"
    MFA_CHALLENGE_SUCCESS = "mfa_challenge_success"
    MFA_CHALLENGE_FAILURE = "mfa_challenge_failure"
    MFA_DISABLED = "mfa_disabled"
    RECOVERY_CODE_USED = "recovery_code_used"
    RECOVERY_CODES_REGENERATED = "recovery_codes_regenerated"

    # Access events
    ACCESS_GRANTED = "access_granted"
    ACCESS_DENIED = "access_denied"

    # User management events
    USER_INVITED = "user_invited"
    USER_JOINED = "user_joined"
    USER_ROLE_CHANGED = "user_role_changed"
    USER_REMOVED = "user_removed"
    USER_CREATED = "user_created"
    USER_UPDATED = "user_updated"
    USER_DELETED = "user_deleted"

    # Organization events
    ORG_CREATED = "org_created"
    ORG_UPDATED = "org_updated"
    ORG_DELETED = "org_deleted"

    # Platform events (super user)
    TENANT_CREATED = "tenant_created"
    TENANT_STATUS_CHANGED = "tenant_status_changed"
    FEATURE_TOGGLE_CHANGED = "feature_toggle_changed"

    # Data events
    DATA_CREATED = "data_created"
    DATA_READ = "data_read"
    DATA_UPDATED = "data_updated"
    DATA_DELETED = "data_deleted"
    DATA_EXPORTED = "data_exported"

    # Proposal events
    PROPOSAL_CREATED = "proposal_created"
    PROPOSAL_UPDATED = "proposal_updated"
    PROPOSAL_DELETED = "proposal_deleted"
    PROPOSAL_SCORED = "proposal_scored"

    # Configuration events
    CONFIG_CHANGED = "config_changed"


class IncidentSeverity(str, Enum):
    """Security incident severity levels."""

    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class IncidentStatus(str, Enum):
    """Security incident status."""

    OPEN = "open"
    INVESTIGATING = "investigating"
    CONTAINED = "contained"
    RESOLVED = "resolved"
    CLOSED = "closed"


class POAMStatus(str, Enum):
    """Plan of Action and Milestones status."""

    OPEN = "open"
    IN_PROGRESS = "in_progress"
    DELAYED = "delayed"
    COMPLETED = "completed"
    ACCEPTED_RISK = "accepted_risk"


class AuditLog(Base):
    """Audit log entry model."""

    __tablename__ = "audit_logs"

    id: Mapped[str] = mapped_column(
        UUID(as_uuid=False), primary_key=True, default=lambda: str(uuid4())
    )
    event_type: Mapped[str] = mapped_column(String(50), nullable=False, index=True)
    event_time: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=_utc_now, nullable=False, index=True
    )

    # Actor information
    actor_id: Mapped[Optional[str]] = mapped_column(
        UUID(as_uuid=False), nullable=True, index=True
    )
    actor_type: Mapped[str] = mapped_column(String(20), default="user", nullable=False)
    actor_email: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)

    # Organization context
    organization_id: Mapped[Optional[str]] = mapped_column(
        UUID(as_uuid=False), nullable=True, index=True
    )

    # Resource information
    resource_type: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    resource_id: Mapped[Optional[str]] = mapped_column(UUID(as_uuid=False), nullable=True)

    # Action details
    action: Mapped[str] = mapped_column(String(100), nullable=False)
    outcome: Mapped[str] = mapped_column(String(20), default="success", nullable=False)

    # Client information
    ip_address: Mapped[Optional[str]] = mapped_column(String(45), nullable=True)
    user_agent: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)

    # Additional details
    details: Mapped[Optional[Dict[str, Any]]] = mapped_column(JSON, nullable=True)

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=_utc_now, nullable=False
    )


class SecurityIncident(Base):
    """Security incident model."""

    __tablename__ = "security_incidents"

    id: Mapped[str] = mapped_column(
        UUID(as_uuid=False), primary_key=True, default=lambda: str(uuid4())
    )
    incident_number: Mapped[str] = mapped_column(
        String(50), unique=True, nullable=False
    )
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    severity: Mapped[str] = mapped_column(String(20), nullable=False)
    status: Mapped[str] = mapped_column(
        String(20), default=IncidentStatus.OPEN.value, nullable=False
    )
    category: Mapped[str] = mapped_column(String(50), nullable=False, index=True)

    affected_systems: Mapped[Optional[List[Any]]] = mapped_column(JSON, nullable=True)

    reported_by: Mapped[Optional[str]] = mapped_column(UUID(as_uuid=False), nullable=True)
    assigned_to: Mapped[Optional[str]] = mapped_column(UUID(as_uuid=False), nullable=True)

    detected_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=_utc_now, nullable=False
    )
    contained_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True), nullable=True
    )
    resolved_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True), nullable=True
    )

    root_cause: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    remediation_steps: Mapped[Optional[List[Any]]] = mapped_column(JSON, nullable=True)
    lessons_learned: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=_utc_now, nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=_utc_now, onupdate=_utc_now, nullable=False
    )


class POAMItem(Base):
    """Plan of Action and Milestones item."""

    __tablename__ = "poam_items"

    id: Mapped[str] = mapped_column(
        UUID(as_uuid=False), primary_key=True, default=lambda: str(uuid4())
    )
    poam_id: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    weakness_name: Mapped[str] = mapped_column(String(255), nullable=False)
    weakness_description: Mapped[str] = mapped_column(Text, nullable=False)
    control_identifier: Mapped[str] = mapped_column(String(50), nullable=False)

    point_of_contact: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    resources_required: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    scheduled_completion: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True), nullable=True
    )
    milestone_changes: Mapped[Optional[List[Any]]] = mapped_column(JSON, nullable=True)

    status: Mapped[str] = mapped_column(
        String(20), default=POAMStatus.OPEN.value, nullable=False
    )
    source_identified: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    vendor_dependency: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    comments: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    risk_level: Mapped[str] = mapped_column(String(20), default="medium", nullable=False)

    original_detection_date: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=_utc_now, nullable=False
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=_utc_now, nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=_utc_now, onupdate=_utc_now, nullable=False
    )
