"""Compliance API router."""

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query

from govproposal.identity.dependencies import CurrentUser, DbSession, require_org_member
from govproposal.compliance.models import CMMCAssessment, Certification, ComplianceItem
from govproposal.compliance.repository import (
    CMMCAssessmentRepository,
    CertificationRepository,
    ComplianceItemRepository,
)
from govproposal.compliance.schemas import (
    CMMCAssessmentCreate,
    CMMCAssessmentListResponse,
    CMMCAssessmentResponse,
    CertificationCreate,
    CertificationListResponse,
    CertificationResponse,
    CertificationUpdate,
    ComplianceItemCreate,
    ComplianceItemListResponse,
    ComplianceItemResponse,
    ComplianceItemUpdate,
    ComplianceSummaryResponse,
)
from govproposal.compliance.service import ComplianceService

router = APIRouter(
    prefix="/api/v1/organizations/{org_id}/compliance",
    tags=["compliance"],
)


def get_compliance_service(session: DbSession) -> ComplianceService:
    return ComplianceService(session)


ComplianceSvc = Annotated[ComplianceService, Depends(get_compliance_service)]


# --- Summary ---


@router.get("/summary", response_model=ComplianceSummaryResponse)
async def get_compliance_summary(
    org_id: str,
    current_user: CurrentUser,
    session: DbSession,
    service: ComplianceSvc,
) -> ComplianceSummaryResponse:
    """Get compliance summary for organization."""
    await require_org_member(org_id, current_user, session)
    data = await service.get_compliance_summary(org_id)
    return ComplianceSummaryResponse(**data)


# --- Compliance Items ---


@router.get("/items", response_model=ComplianceItemListResponse)
async def list_compliance_items(
    org_id: str,
    current_user: CurrentUser,
    session: DbSession,
    framework: Annotated[str | None, Query()] = None,
    status: Annotated[str | None, Query()] = None,
    limit: Annotated[int, Query(ge=1, le=100)] = 50,
    offset: Annotated[int, Query(ge=0)] = 0,
) -> ComplianceItemListResponse:
    """List compliance items for organization."""
    await require_org_member(org_id, current_user, session)
    repo = ComplianceItemRepository(session)
    items, total = await repo.list_by_org(org_id, framework=framework, status=status, limit=limit, offset=offset)
    return ComplianceItemListResponse(
        items=[ComplianceItemResponse.model_validate(i) for i in items],
        total=total, limit=limit, offset=offset,
    )


@router.post("/items", response_model=ComplianceItemResponse, status_code=201)
async def create_compliance_item(
    org_id: str,
    data: ComplianceItemCreate,
    current_user: CurrentUser,
    session: DbSession,
) -> ComplianceItemResponse:
    """Create a compliance item."""
    await require_org_member(org_id, current_user, session)
    repo = ComplianceItemRepository(session)
    item = ComplianceItem(organization_id=org_id, **data.model_dump())
    item = await repo.create(item)
    return ComplianceItemResponse.model_validate(item)


@router.put("/items/{item_id}", response_model=ComplianceItemResponse)
async def update_compliance_item(
    org_id: str,
    item_id: str,
    data: ComplianceItemUpdate,
    current_user: CurrentUser,
    session: DbSession,
) -> ComplianceItemResponse:
    """Update a compliance item."""
    await require_org_member(org_id, current_user, session)
    repo = ComplianceItemRepository(session)
    item = await repo.get_by_id(item_id)
    if not item or item.organization_id != org_id:
        raise HTTPException(status_code=404, detail="Compliance item not found")
    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(item, field, value)
    item = await repo.update(item)
    return ComplianceItemResponse.model_validate(item)


# --- Certifications ---


@router.get("/certifications", response_model=CertificationListResponse)
async def list_certifications(
    org_id: str,
    current_user: CurrentUser,
    session: DbSession,
    certification_type: Annotated[str | None, Query()] = None,
    limit: Annotated[int, Query(ge=1, le=100)] = 50,
    offset: Annotated[int, Query(ge=0)] = 0,
) -> CertificationListResponse:
    """List certifications for organization."""
    await require_org_member(org_id, current_user, session)
    repo = CertificationRepository(session)
    certs, total = await repo.list_by_org(org_id, certification_type=certification_type, limit=limit, offset=offset)
    return CertificationListResponse(
        items=[CertificationResponse.model_validate(c) for c in certs],
        total=total, limit=limit, offset=offset,
    )


@router.post("/certifications", response_model=CertificationResponse, status_code=201)
async def create_certification(
    org_id: str,
    data: CertificationCreate,
    current_user: CurrentUser,
    session: DbSession,
) -> CertificationResponse:
    """Create a certification."""
    await require_org_member(org_id, current_user, session)
    repo = CertificationRepository(session)
    cert = Certification(organization_id=org_id, **data.model_dump())
    cert = await repo.create(cert)
    return CertificationResponse.model_validate(cert)


@router.put("/certifications/{cert_id}", response_model=CertificationResponse)
async def update_certification(
    org_id: str,
    cert_id: str,
    data: CertificationUpdate,
    current_user: CurrentUser,
    session: DbSession,
) -> CertificationResponse:
    """Update a certification."""
    await require_org_member(org_id, current_user, session)
    repo = CertificationRepository(session)
    cert = await repo.get_by_id(cert_id)
    if not cert or cert.organization_id != org_id:
        raise HTTPException(status_code=404, detail="Certification not found")
    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(cert, field, value)
    cert = await repo.update(cert)
    return CertificationResponse.model_validate(cert)


# --- CMMC Assessments ---


@router.get("/cmmc", response_model=CMMCAssessmentListResponse)
async def list_cmmc_assessments(
    org_id: str,
    current_user: CurrentUser,
    session: DbSession,
    limit: Annotated[int, Query(ge=1, le=100)] = 50,
    offset: Annotated[int, Query(ge=0)] = 0,
) -> CMMCAssessmentListResponse:
    """List CMMC assessments for organization."""
    await require_org_member(org_id, current_user, session)
    repo = CMMCAssessmentRepository(session)
    assessments, total = await repo.list_by_org(org_id, limit=limit, offset=offset)
    return CMMCAssessmentListResponse(
        items=[CMMCAssessmentResponse.model_validate(a) for a in assessments],
        total=total, limit=limit, offset=offset,
    )


@router.post("/cmmc", response_model=CMMCAssessmentResponse, status_code=201)
async def create_cmmc_assessment(
    org_id: str,
    data: CMMCAssessmentCreate,
    current_user: CurrentUser,
    session: DbSession,
) -> CMMCAssessmentResponse:
    """Create a CMMC assessment."""
    await require_org_member(org_id, current_user, session)
    repo = CMMCAssessmentRepository(session)
    assessment = CMMCAssessment(organization_id=org_id, **data.model_dump())
    assessment = await repo.create(assessment)
    return CMMCAssessmentResponse.model_validate(assessment)
