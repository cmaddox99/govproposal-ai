"""Pydantic schemas for compliance module."""

from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class ComplianceItemCreate(BaseModel):
    framework: str
    clause_number: str
    title: str
    status: Optional[str] = "pending_review"
    evidence_notes: Optional[str] = None
    due_date: Optional[datetime] = None


class ComplianceItemUpdate(BaseModel):
    status: Optional[str] = None
    evidence_notes: Optional[str] = None
    due_date: Optional[datetime] = None


class ComplianceItemResponse(BaseModel):
    id: str
    organization_id: str
    framework: str
    clause_number: str
    title: str
    status: str
    evidence_notes: Optional[str]
    due_date: Optional[datetime]
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


class ComplianceItemListResponse(BaseModel):
    items: list[ComplianceItemResponse]
    total: int
    limit: int
    offset: int


class CertificationCreate(BaseModel):
    certification_type: str
    identifier: Optional[str] = None
    status: Optional[str] = "pending_review"
    issued_date: Optional[datetime] = None
    expiry_date: Optional[datetime] = None
    notes: Optional[str] = None


class CertificationUpdate(BaseModel):
    status: Optional[str] = None
    identifier: Optional[str] = None
    issued_date: Optional[datetime] = None
    expiry_date: Optional[datetime] = None
    notes: Optional[str] = None


class CertificationResponse(BaseModel):
    id: str
    organization_id: str
    certification_type: str
    identifier: Optional[str]
    status: str
    issued_date: Optional[datetime]
    expiry_date: Optional[datetime]
    notes: Optional[str]
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


class CertificationListResponse(BaseModel):
    items: list[CertificationResponse]
    total: int
    limit: int
    offset: int


class CMMCAssessmentCreate(BaseModel):
    target_level: str
    total_controls: int = 0
    implemented_controls: int = 0
    partially_implemented: int = 0
    not_implemented: int = 0
    findings_count: int = 0
    assessment_date: Optional[datetime] = None
    notes: Optional[str] = None


class CMMCAssessmentResponse(BaseModel):
    id: str
    organization_id: str
    target_level: str
    total_controls: int
    implemented_controls: int
    partially_implemented: int
    not_implemented: int
    findings_count: int
    assessment_date: Optional[datetime]
    notes: Optional[str]
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


class CMMCAssessmentListResponse(BaseModel):
    items: list[CMMCAssessmentResponse]
    total: int
    limit: int
    offset: int


class ComplianceSummaryResponse(BaseModel):
    overall_compliance_percentage: float
    total_items: int
    compliant_items: int
    partial_items: int
    non_compliant_items: int
    action_required: int
    total_certifications: int
    active_certifications: int
