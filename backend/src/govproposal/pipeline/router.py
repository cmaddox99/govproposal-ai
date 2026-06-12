"""Pipeline API router."""

from datetime import datetime
from typing import Annotated, List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from pydantic import BaseModel
from sqlalchemy import and_, select
from sqlalchemy.ext.asyncio import AsyncSession

from govproposal.db.base import get_db
from govproposal.identity.dependencies import CurrentUser
from govproposal.identity.models import OrganizationMember
from govproposal.opportunities.models import Opportunity
from govproposal.pipeline.models import (
    ArchiveStatus,
    PipelineItem,
    PipelineStatus,
)
from govproposal.pipeline.service import compute_match_score
from govproposal.proposals.models import Proposal, ProposalStatus

router = APIRouter(prefix="/api/v1/pipeline", tags=["pipeline"])

DbSession = Annotated[AsyncSession, Depends(get_db)]


class OpportunitySummary(BaseModel):
    id: str
    title: str
    solicitation_number: Optional[str] = None
    agency: Optional[str] = None
    naics_code: Optional[str] = None
    set_aside_type: Optional[str] = None
    response_deadline: Optional[datetime] = None
    estimated_value: Optional[float] = None
    primary_contact_name: Optional[str] = None
    primary_contact_email: Optional[str] = None
    sam_url: Optional[str] = None
    source: str = "sam_gov"
    market: str = "federal"

    class Config:
        from_attributes = True


class PipelineItemResponse(BaseModel):
    id: str
    organization_id: str
    opportunity_id: str
    proposal_id: Optional[str] = None
    status: str
    dollar_value_text: Optional[str] = None
    questions_due_date: Optional[datetime] = None
    proposal_due_date_override: Optional[datetime] = None
    contact_name_override: Optional[str] = None
    contact_email_override: Optional[str] = None
    has_rfp: bool
    has_ppqs: bool
    has_resume: bool
    has_price: bool
    has_details: bool
    archive_status: Optional[str] = None
    no_bid_reason: Optional[str] = None
    match_score: Optional[int] = None
    match_tier: Optional[str] = None
    match_breakdown: Optional[str] = None
    notes: Optional[str] = None
    created_at: datetime
    updated_at: datetime
    opportunity: Optional[OpportunitySummary] = None

    class Config:
        from_attributes = True


class PipelineListResponse(BaseModel):
    items: List[PipelineItemResponse]
    total: int


class AddToPipelineRequest(BaseModel):
    organization_id: str
    opportunity_id: str
    dollar_value_text: Optional[str] = None
    questions_due_date: Optional[datetime] = None
    notes: Optional[str] = None


class UpdatePipelineRequest(BaseModel):
    status: Optional[str] = None
    dollar_value_text: Optional[str] = None
    questions_due_date: Optional[datetime] = None
    proposal_due_date_override: Optional[datetime] = None
    contact_name_override: Optional[str] = None
    contact_email_override: Optional[str] = None
    has_rfp: Optional[bool] = None
    has_ppqs: Optional[bool] = None
    has_resume: Optional[bool] = None
    has_price: Optional[bool] = None
    has_details: Optional[bool] = None
    archive_status: Optional[str] = None
    no_bid_reason: Optional[str] = None
    notes: Optional[str] = None


async def _verify_org_member(
    session: AsyncSession, user_id: str, organization_id: str
) -> None:
    member = (
        await session.execute(
            select(OrganizationMember).where(
                and_(
                    OrganizationMember.organization_id == organization_id,
                    OrganizationMember.user_id == user_id,
                )
            )
        )
    ).scalar_one_or_none()
    if not member:
        raise HTTPException(status_code=403, detail="Not a member of this organization")


async def _hydrate(session: AsyncSession, item: PipelineItem) -> PipelineItemResponse:
    opp = (
        await session.execute(
            select(Opportunity).where(Opportunity.id == item.opportunity_id)
        )
    ).scalar_one_or_none()
    payload = PipelineItemResponse.model_validate(item)
    if opp:
        payload.opportunity = OpportunitySummary.model_validate(opp)
    return payload


@router.get("", response_model=PipelineListResponse)
async def list_pipeline(
    current_user: CurrentUser,
    session: DbSession,
    org_id: Annotated[str, Query(description="Organization ID")],
    status_filter: Annotated[Optional[str], Query(alias="status")] = None,
) -> PipelineListResponse:
    """List pipeline items for an org, optionally filtered by status."""
    await _verify_org_member(session, current_user.id, org_id)

    conditions = [PipelineItem.organization_id == org_id]
    if status_filter:
        conditions.append(PipelineItem.status == status_filter)

    rows = (
        await session.execute(
            select(PipelineItem).where(and_(*conditions)).order_by(PipelineItem.updated_at.desc())
        )
    ).scalars().all()

    items = [await _hydrate(session, row) for row in rows]
    return PipelineListResponse(items=items, total=len(items))


@router.post("", response_model=PipelineItemResponse)
async def add_to_pipeline(
    body: AddToPipelineRequest,
    current_user: CurrentUser,
    session: DbSession,
) -> PipelineItemResponse:
    """Promote an opportunity into the pipeline. Computes match score on add."""
    await _verify_org_member(session, current_user.id, body.organization_id)

    # Check existing
    existing = (
        await session.execute(
            select(PipelineItem).where(
                and_(
                    PipelineItem.organization_id == body.organization_id,
                    PipelineItem.opportunity_id == body.opportunity_id,
                )
            )
        )
    ).scalar_one_or_none()

    if existing:
        return await _hydrate(session, existing)

    opp = (
        await session.execute(
            select(Opportunity).where(Opportunity.id == body.opportunity_id)
        )
    ).scalar_one_or_none()
    if not opp:
        raise HTTPException(status_code=404, detail="Opportunity not found")

    breakdown = await compute_match_score(session, body.organization_id, body.opportunity_id)

    item = PipelineItem(
        organization_id=body.organization_id,
        opportunity_id=body.opportunity_id,
        status=PipelineStatus.ACTIVE.value,
        dollar_value_text=body.dollar_value_text,
        questions_due_date=body.questions_due_date,
        notes=body.notes,
        created_by=current_user.id,
        match_score=breakdown.total,
        match_tier=breakdown.tier,
        match_breakdown=breakdown.to_json(),
    )
    session.add(item)
    await session.commit()
    await session.refresh(item)
    return await _hydrate(session, item)


@router.patch("/{item_id}", response_model=PipelineItemResponse)
async def update_pipeline_item(
    item_id: str,
    body: UpdatePipelineRequest,
    current_user: CurrentUser,
    session: DbSession,
) -> PipelineItemResponse:
    """Update a pipeline item (status, checkmarks, reasons, notes)."""
    item = (
        await session.execute(select(PipelineItem).where(PipelineItem.id == item_id))
    ).scalar_one_or_none()
    if not item:
        raise HTTPException(status_code=404, detail="Pipeline item not found")

    await _verify_org_member(session, current_user.id, item.organization_id)

    updates = body.model_dump(exclude_unset=True)
    for key, value in updates.items():
        setattr(item, key, value)
    await session.commit()
    await session.refresh(item)
    return await _hydrate(session, item)


@router.delete("/{item_id}")
async def delete_pipeline_item(
    item_id: str,
    current_user: CurrentUser,
    session: DbSession,
) -> dict:
    """Remove an item from the pipeline."""
    item = (
        await session.execute(select(PipelineItem).where(PipelineItem.id == item_id))
    ).scalar_one_or_none()
    if not item:
        raise HTTPException(status_code=404, detail="Pipeline item not found")
    await _verify_org_member(session, current_user.id, item.organization_id)
    await session.delete(item)
    await session.commit()
    return {"deleted": True}


@router.post("/{item_id}/rescore", response_model=PipelineItemResponse)
async def rescore_pipeline_item(
    item_id: str,
    current_user: CurrentUser,
    session: DbSession,
) -> PipelineItemResponse:
    """Recompute the match score for a pipeline item."""
    item = (
        await session.execute(select(PipelineItem).where(PipelineItem.id == item_id))
    ).scalar_one_or_none()
    if not item:
        raise HTTPException(status_code=404, detail="Pipeline item not found")
    await _verify_org_member(session, current_user.id, item.organization_id)

    breakdown = await compute_match_score(session, item.organization_id, item.opportunity_id)
    item.match_score = breakdown.total
    item.match_tier = breakdown.tier
    item.match_breakdown = breakdown.to_json()
    await session.commit()
    await session.refresh(item)
    return await _hydrate(session, item)


@router.post("/{item_id}/create-proposal")
async def create_proposal_from_pipeline(
    item_id: str,
    current_user: CurrentUser,
    session: DbSession,
) -> dict:
    """Create a proposal from a pipeline item, link them, return proposal id."""
    item = (
        await session.execute(select(PipelineItem).where(PipelineItem.id == item_id))
    ).scalar_one_or_none()
    if not item:
        raise HTTPException(status_code=404, detail="Pipeline item not found")
    await _verify_org_member(session, current_user.id, item.organization_id)

    if item.proposal_id:
        return {"id": item.proposal_id, "already_existed": True}

    opp = (
        await session.execute(
            select(Opportunity).where(Opportunity.id == item.opportunity_id)
        )
    ).scalar_one_or_none()
    if not opp:
        raise HTTPException(status_code=404, detail="Linked opportunity missing")

    proposal = Proposal(
        organization_id=item.organization_id,
        opportunity_id=opp.id,
        title=opp.title,
        description=opp.description,
        status=ProposalStatus.DRAFT.value,
        solicitation_number=opp.solicitation_number,
        agency=opp.agency,
        naics_code=opp.naics_code,
        due_date=item.proposal_due_date_override or opp.response_deadline,
        estimated_value=float(opp.estimated_value) if opp.estimated_value else None,
        market=opp.market,
        created_by=current_user.id,
    )
    session.add(proposal)
    await session.flush()
    item.proposal_id = proposal.id
    await session.commit()
    return {"id": proposal.id, "already_existed": False}
