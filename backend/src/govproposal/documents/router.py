"""Opportunity document attachment API."""

from typing import Annotated

from fastapi import APIRouter, File, Form, HTTPException, UploadFile, status
from fastapi.responses import FileResponse
from sqlalchemy import select

from govproposal.documents.models import OpportunityDocument
from govproposal.documents.schemas import (
    OpportunityDocumentList,
    OpportunityDocumentResponse,
)
from govproposal.identity.dependencies import CurrentUser, DbSession, require_org_member
from govproposal.opportunities.models import Opportunity
from govproposal.storage import get_storage

router = APIRouter(
    prefix="/api/v1/organizations/{org_id}/opportunities/{opportunity_id}/documents",
    tags=["opportunity-documents"],
)

ALLOWED_CONTENT_TYPES = {
    "application/pdf",
    "application/msword",
    "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
    "application/vnd.ms-excel",
    "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    "text/plain",
    "text/csv",
    "image/png",
    "image/jpeg",
}


@router.get("", response_model=OpportunityDocumentList)
async def list_documents(
    org_id: str,
    opportunity_id: str,
    current_user: CurrentUser,
    session: DbSession,
) -> OpportunityDocumentList:
    """List documents attached by this org to this opportunity."""
    await require_org_member(org_id, current_user, session)

    rows = (
        await session.execute(
            select(OpportunityDocument)
            .where(
                OpportunityDocument.organization_id == org_id,
                OpportunityDocument.opportunity_id == opportunity_id,
            )
            .order_by(OpportunityDocument.uploaded_at.desc())
        )
    ).scalars().all()

    items = [OpportunityDocumentResponse.model_validate(r) for r in rows]
    return OpportunityDocumentList(items=items, total=len(items))


@router.post(
    "",
    response_model=OpportunityDocumentResponse,
    status_code=status.HTTP_201_CREATED,
)
async def upload_document(
    org_id: str,
    opportunity_id: str,
    current_user: CurrentUser,
    session: DbSession,
    file: Annotated[UploadFile, File(...)],
    description: Annotated[str | None, Form()] = None,
) -> OpportunityDocumentResponse:
    """Upload a document and attach it to this opportunity for this org."""
    await require_org_member(org_id, current_user, session)

    opp = (
        await session.execute(select(Opportunity).where(Opportunity.id == opportunity_id))
    ).scalar_one_or_none()
    if not opp:
        raise HTTPException(status_code=404, detail="Opportunity not found")

    if file.content_type and file.content_type not in ALLOWED_CONTENT_TYPES:
        raise HTTPException(
            status_code=415,
            detail=f"Unsupported file type: {file.content_type}",
        )

    storage = get_storage()
    try:
        stored = storage.write(
            namespace="opportunity_docs",
            owner_id=opportunity_id,
            source=file.file,
            original_filename=file.filename or "document",
            content_type=file.content_type,
        )
    except ValueError as exc:
        raise HTTPException(status_code=413, detail=str(exc)) from exc

    record = OpportunityDocument(
        organization_id=org_id,
        opportunity_id=opportunity_id,
        filename=stored.original_filename,
        stored_path=stored.relative_path,
        content_type=stored.content_type,
        size_bytes=stored.size_bytes,
        description=description,
        uploaded_by=current_user.id,
    )
    session.add(record)
    await session.commit()
    await session.refresh(record)

    return OpportunityDocumentResponse.model_validate(record)


@router.get("/{document_id}/download")
async def download_document(
    org_id: str,
    opportunity_id: str,
    document_id: str,
    current_user: CurrentUser,
    session: DbSession,
) -> FileResponse:
    """Stream a stored document back to the caller."""
    await require_org_member(org_id, current_user, session)

    record = (
        await session.execute(
            select(OpportunityDocument).where(
                OpportunityDocument.id == document_id,
                OpportunityDocument.organization_id == org_id,
                OpportunityDocument.opportunity_id == opportunity_id,
            )
        )
    ).scalar_one_or_none()
    if not record:
        raise HTTPException(status_code=404, detail="Document not found")

    storage = get_storage()
    try:
        abs_path = storage.absolute_path(record.stored_path)
    except FileNotFoundError as exc:
        raise HTTPException(status_code=404, detail="File missing from storage") from exc

    return FileResponse(
        abs_path,
        filename=record.filename,
        media_type=record.content_type or "application/octet-stream",
    )


@router.delete("/{document_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_document(
    org_id: str,
    opportunity_id: str,
    document_id: str,
    current_user: CurrentUser,
    session: DbSession,
) -> None:
    """Delete a document attachment."""
    await require_org_member(org_id, current_user, session)

    record = (
        await session.execute(
            select(OpportunityDocument).where(
                OpportunityDocument.id == document_id,
                OpportunityDocument.organization_id == org_id,
                OpportunityDocument.opportunity_id == opportunity_id,
            )
        )
    ).scalar_one_or_none()
    if not record:
        raise HTTPException(status_code=404, detail="Document not found")

    storage = get_storage()
    storage.delete(record.stored_path)
    await session.delete(record)
    await session.commit()
