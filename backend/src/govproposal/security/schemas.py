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
    created_at: datetime

    model_config = {"from_attributes": True}


class SecurityIncidentCreate(BaseModel):
    """Schema for creating a security incident."""

    title: str
    description: str
    severity: str = "medium"
    category: str = "general"
    affected_systems: list[str] | None = None


class SecurityIncidentUpdate(BaseModel):
    """Schema for updating a security incident."""

    status: str | None = None
    severity: str | None = None
    root_cause: str | None = None
    remediation_steps: list[str] | None = None
    lessons_learned: str | None = None


class SecurityIncidentListResponse(BaseModel):
    """Schema for paginated security incident list."""

    items: list[SecurityIncidentResponse]
    total: int


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
    point_of_contact: str | None
    comments: str | None
    created_at: datetime

    model_config = {"from_attributes": True}


class POAMItemCreate(BaseModel):
    """Schema for creating a POAM item."""

    weakness_name: str
    weakness_description: str
    control_identifier: str
    risk_level: str = "medium"
    scheduled_completion: datetime | None = None
    point_of_contact: str | None = None
    resources_required: str | None = None


class POAMItemUpdate(BaseModel):
    """Schema for updating a POAM item."""

    status: str | None = None
    risk_level: str | None = None
    scheduled_completion: datetime | None = None
    point_of_contact: str | None = None
    comments: str | None = None


class POAMItemListResponse(BaseModel):
    """Schema for paginated POAM item list."""

    items: list[POAMItemResponse]
    total: int
