"""Past Performance API router."""

from datetime import datetime
from typing import Annotated

from fastapi import APIRouter, File, HTTPException, Request, UploadFile, status
from sqlalchemy import select

from govproposal.identity.dependencies import (
    CurrentUser,
    DbSession,
    require_org_admin,
    require_org_member,
)
from govproposal.identity.models import OrgPastPerformance
from govproposal.identity.past_performance_extraction import (
    extract_past_performance,
    extract_text,
)
from govproposal.security.service import AuditService
from govproposal.identity.schemas import (
    PastPerformanceCreate,
    PastPerformanceExtractedFields,
    PastPerformanceExtractResponse,
    PastPerformanceResponse,
    PastPerformanceUpdate,
)
from govproposal.storage import get_storage

router = APIRouter(
    prefix="/api/v1/organizations/{org_id}/past-performance",
    tags=["past-performance"],
)


ALLOWED_EXTRACT_TYPES = {
    "application/pdf",
    "application/msword",
    "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
    "text/plain",
    "text/csv",
}


@router.post("", response_model=PastPerformanceResponse, status_code=status.HTTP_201_CREATED)
async def create_past_performance(
    org_id: str,
    data: PastPerformanceCreate,
    current_user: CurrentUser,
    session: DbSession,
    request: Request,
) -> PastPerformanceResponse:
    """Create a past performance record."""
    await require_org_member(org_id, current_user, session)

    payload = data.model_dump()

    # Guard: source_document_path, if provided, must live under this org's
    # past-performance namespace. Prevents attaching another org's upload.
    src_path = payload.get("source_document_path")
    if src_path:
        expected_prefix = f"past_performance_docs/{org_id}/"
        if not src_path.startswith(expected_prefix):
            raise HTTPException(
                status_code=400,
                detail="source_document_path does not belong to this organization",
            )

    record = OrgPastPerformance(
        organization_id=org_id,
        **payload,
    )
    session.add(record)
    await session.commit()
    await session.refresh(record)

    audit = AuditService(session)
    await audit.log_event(
        event_type="past_performance_created",
        action="Past performance record created",
        actor_id=current_user.id,
        actor_email=current_user.email,
        organization_id=org_id,
        resource_type="past_performance",
        resource_id=record.id,
        ip_address=request.client.host if request.client else None,
        details={"contract_name": data.contract_name},
    )

    return PastPerformanceResponse.model_validate(record)


@router.post(
    "/extract",
    response_model=PastPerformanceExtractResponse,
    status_code=status.HTTP_200_OK,
)
async def extract_from_document(
    org_id: str,
    current_user: CurrentUser,
    session: DbSession,
    file: Annotated[UploadFile, File(...)],
) -> PastPerformanceExtractResponse:
    """Upload a past-performance document and get suggested field values.

    The file is saved to storage. The returned source_document_path can be
    passed to POST /past-performance to attach the file to the new record.
    Nothing in the database is persisted by this endpoint.
    """
    await require_org_member(org_id, current_user, session)

    if file.content_type and file.content_type not in ALLOWED_EXTRACT_TYPES:
        raise HTTPException(
            status_code=415,
            detail=f"Unsupported file type for extraction: {file.content_type}",
        )

    storage = get_storage()
    try:
        stored = storage.write(
            namespace="past_performance_docs",
            owner_id=org_id,
            source=file.file,
            original_filename=file.filename or "past_performance",
            content_type=file.content_type,
        )
    except ValueError as exc:
        raise HTTPException(status_code=413, detail=str(exc)) from exc

    text = extract_text(stored.absolute_path, stored.content_type, stored.original_filename)
    raw = await extract_past_performance(text) if text else None

    if not raw:
        return PastPerformanceExtractResponse(
            extracted=PastPerformanceExtractedFields(),
            source_document_path=stored.relative_path,
            source_document_filename=stored.original_filename,
            source_document_content_type=stored.content_type,
            size_bytes=stored.size_bytes,
            extraction_available=False,
        )

    # Normalize date strings into datetime objects where possible
    def _parse_date(value):
        if not value:
            return None
        if isinstance(value, datetime):
            return value
        try:
            return datetime.fromisoformat(str(value).replace("Z", "+00:00"))
        except (TypeError, ValueError):
            return None

    fields = PastPerformanceExtractedFields(
        contract_name=raw.get("contract_name"),
        agency=raw.get("agency"),
        contract_number=raw.get("contract_number"),
        contract_value=raw.get("contract_value"),
        period_of_performance_start=_parse_date(raw.get("period_of_performance_start")),
        period_of_performance_end=_parse_date(raw.get("period_of_performance_end")),
        description=raw.get("description"),
        contact_name=raw.get("contact_name"),
        contact_email=raw.get("contact_email"),
        contact_phone=raw.get("contact_phone"),
        performance_rating=raw.get("performance_rating"),
        confidence={
            k: float(v)
            for k, v in (raw.get("confidence") or {}).items()
            if isinstance(v, (int, float))
        },
    )

    return PastPerformanceExtractResponse(
        extracted=fields,
        source_document_path=stored.relative_path,
        source_document_filename=stored.original_filename,
        source_document_content_type=stored.content_type,
        size_bytes=stored.size_bytes,
        extraction_available=True,
    )


@router.get("", response_model=list[PastPerformanceResponse])
async def list_past_performance(
    org_id: str,
    current_user: CurrentUser,
    session: DbSession,
) -> list[PastPerformanceResponse]:
    """List all past performance records for an organization."""
    await require_org_member(org_id, current_user, session)

    query = (
        select(OrgPastPerformance)
        .where(OrgPastPerformance.organization_id == org_id)
        .order_by(OrgPastPerformance.created_at.desc())
    )
    result = await session.execute(query)
    records = result.scalars().all()

    return [PastPerformanceResponse.model_validate(r) for r in records]


@router.get("/{pp_id}", response_model=PastPerformanceResponse)
async def get_past_performance(
    org_id: str,
    pp_id: str,
    current_user: CurrentUser,
    session: DbSession,
) -> PastPerformanceResponse:
    """Get a specific past performance record."""
    await require_org_member(org_id, current_user, session)

    query = select(OrgPastPerformance).where(
        OrgPastPerformance.id == pp_id,
        OrgPastPerformance.organization_id == org_id,
    )
    result = await session.execute(query)
    record = result.scalar_one_or_none()

    if not record:
        raise HTTPException(status_code=404, detail="Past performance record not found")

    return PastPerformanceResponse.model_validate(record)


@router.put("/{pp_id}", response_model=PastPerformanceResponse)
async def update_past_performance(
    org_id: str,
    pp_id: str,
    data: PastPerformanceUpdate,
    current_user: CurrentUser,
    session: DbSession,
    request: Request,
) -> PastPerformanceResponse:
    """Update a past performance record."""
    await require_org_admin(org_id, current_user, session)

    query = select(OrgPastPerformance).where(
        OrgPastPerformance.id == pp_id,
        OrgPastPerformance.organization_id == org_id,
    )
    result = await session.execute(query)
    record = result.scalar_one_or_none()

    if not record:
        raise HTTPException(status_code=404, detail="Past performance record not found")

    update_data = data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(record, field, value)

    await session.commit()
    await session.refresh(record)

    audit = AuditService(session)
    await audit.log_event(
        event_type="past_performance_updated",
        action="Past performance record updated",
        actor_id=current_user.id,
        actor_email=current_user.email,
        organization_id=org_id,
        resource_type="past_performance",
        resource_id=pp_id,
        ip_address=request.client.host if request.client else None,
        details={"updated_fields": list(update_data.keys())},
    )

    return PastPerformanceResponse.model_validate(record)


@router.delete("/{pp_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_past_performance(
    org_id: str,
    pp_id: str,
    current_user: CurrentUser,
    session: DbSession,
    request: Request,
) -> None:
    """Delete a past performance record."""
    await require_org_admin(org_id, current_user, session)

    query = select(OrgPastPerformance).where(
        OrgPastPerformance.id == pp_id,
        OrgPastPerformance.organization_id == org_id,
    )
    result = await session.execute(query)
    record = result.scalar_one_or_none()

    if not record:
        raise HTTPException(status_code=404, detail="Past performance record not found")

    contract_name = record.contract_name
    src_path = record.source_document_path
    await session.delete(record)
    await session.commit()

    # Clean up the source document file once the record is gone
    if src_path:
        try:
            get_storage().delete(src_path)
        except Exception:
            pass

    audit = AuditService(session)
    await audit.log_event(
        event_type="past_performance_deleted",
        action="Past performance record deleted",
        actor_id=current_user.id,
        actor_email=current_user.email,
        organization_id=org_id,
        resource_type="past_performance",
        resource_id=pp_id,
        ip_address=request.client.host if request.client else None,
        details={"contract_name": contract_name},
    )


@router.get("/{pp_id}/document")
async def download_past_performance_document(
    org_id: str,
    pp_id: str,
    current_user: CurrentUser,
    session: DbSession,
):
    """Download the source document attached to a past-performance record."""
    from fastapi.responses import FileResponse

    await require_org_member(org_id, current_user, session)

    record = (
        await session.execute(
            select(OrgPastPerformance).where(
                OrgPastPerformance.id == pp_id,
                OrgPastPerformance.organization_id == org_id,
            )
        )
    ).scalar_one_or_none()
    if not record:
        raise HTTPException(status_code=404, detail="Past performance record not found")
    if not record.source_document_path:
        raise HTTPException(status_code=404, detail="No source document attached")

    storage = get_storage()
    try:
        abs_path = storage.absolute_path(record.source_document_path)
    except FileNotFoundError as exc:
        raise HTTPException(status_code=404, detail="File missing from storage") from exc

    return FileResponse(
        abs_path,
        filename=record.source_document_filename or "past_performance",
        media_type=record.source_document_content_type or "application/octet-stream",
    )
