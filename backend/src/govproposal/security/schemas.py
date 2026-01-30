"""Pydantic schemas for security module."""

from datetime import datetime

from pydantic import BaseModel, Field


class AuditLogResponse(BaseModel):
    """Schema for audit log response."""

    id: str
    event_type: str
    event_time: datetime
    actor_id: str | None
    actor_email: str | None
    organization_id: str | None
    resource_type: str | None
    resource_id: str | None
    action: str
    outcome: str
    ip_address: str | None
    details: dict | None

    model_config = {"from_attributes": True}


class AuditLogListResponse(BaseModel):
    """Schema for paginated audit log list."""

    items: list[AuditLogResponse]
    total: int
    limit: int
    offset: int


class SecurityIncidentResponse(BaseModel):
    """Schema for security incident response."""

    id: str
    incident_number: str
    title: str
    description: str
    severity: str
    status: str
    category: str
    affected_systems: list[str] | None
    detected_at: datetime
    contained_at: datetime | None
    resolved_at: datetime | None

    model_config = {"from_attributes": True}


class POAMItemResponse(BaseModel):
    """Schema for POAM item response."""

    id: str
    poam_id: str
    weakness_name: str
    weakness_description: str
    control_identifier: str
    status: str
    risk_level: str
    scheduled_completion: datetime | None

    model_config = {"from_attributes": True}
