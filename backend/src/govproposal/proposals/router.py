"""Proposals API router."""

from datetime import datetime, timezone
from typing import Annotated, Optional, List

from fastapi import APIRouter, Depends, Query, HTTPException, status
from pydantic import BaseModel, Field
from sqlalchemy import select, and_
from sqlalchemy.ext.asyncio import AsyncSession

from govproposal.db.base import get_db
from govproposal.identity.dependencies import CurrentUser
from govproposal.identity.models import OrganizationMember
from govproposal.opportunities.models import Opportunity
from govproposal.proposals.models import Proposal, ProposalStatus
from govproposal.ai.service import generate_executive_summary

router = APIRouter(prefix="/api/v1/proposals", tags=["proposals"])

DbSession = Annotated[AsyncSession, Depends(get_db)]


class ProposalCreate(BaseModel):
    """Create proposal request."""
    organization_id: str
    title: str
    description: Optional[str] = None
    opportunity_id: Optional[str] = None
    solicitation_number: Optional[str] = None
    agency: Optional[str] = None
    naics_code: Optional[str] = None
    due_date: Optional[datetime] = None
    estimated_value: Optional[float] = None


class ProposalUpdate(BaseModel):
    """Update proposal request."""
    title: Optional[str] = None
    description: Optional[str] = None
    status: Optional[str] = None
    solicitation_number: Optional[str] = None
    agency: Optional[str] = None
    naics_code: Optional[str] = None
    due_date: Optional[datetime] = None
    estimated_value: Optional[float] = None
    proposed_value: Optional[float] = None
    executive_summary: Optional[str] = None
    technical_approach: Optional[str] = None
    management_approach: Optional[str] = None
    past_performance: Optional[str] = None
    pricing_summary: Optional[str] = None


class ProposalResponse(BaseModel):
    """Proposal response schema."""
    id: str
    organization_id: str
    opportunity_id: Optional[str] = None
    title: str
    description: Optional[str] = None
    status: str
    solicitation_number: Optional[str] = None
    agency: Optional[str] = None
    naics_code: Optional[str] = None
    due_date: Optional[datetime] = None
    submitted_at: Optional[datetime] = None
    estimated_value: Optional[float] = None
    proposed_value: Optional[float] = None
    executive_summary: Optional[str] = None
    technical_approach: Optional[str] = None
    management_approach: Optional[str] = None
    past_performance: Optional[str] = None
    pricing_summary: Optional[str] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class ProposalListResponse(BaseModel):
    """Paginated proposal list response."""
    proposals: List[ProposalResponse]
    total: int
    limit: int
    offset: int


class GenerateProposalRequest(BaseModel):
    """Request to generate proposal content from opportunity."""
    opportunity_id: str
    organization_id: str
    sections: Optional[List[str]] = None  # Which sections to generate


class GenerateProposalResponse(BaseModel):
    """Generated proposal content."""
    proposal_id: str
    title: str
    executive_summary: Optional[str] = None
    technical_approach: Optional[str] = None
    management_approach: Optional[str] = None


@router.post("", response_model=ProposalResponse, status_code=status.HTTP_201_CREATED)
async def create_proposal(
    data: ProposalCreate,
    current_user: CurrentUser,
    session: DbSession,
) -> ProposalResponse:
    """Create a new proposal."""

    # Verify user is member of org
    member_query = select(OrganizationMember).where(
        and_(
            OrganizationMember.organization_id == data.organization_id,
            OrganizationMember.user_id == current_user.id,
        )
    )
    member = (await session.execute(member_query)).scalar_one_or_none()
    if not member:
        raise HTTPException(status_code=403, detail="Not a member of this organization")

    # If opportunity_id provided, copy data from opportunity
    if data.opportunity_id:
        opp_query = select(Opportunity).where(Opportunity.id == data.opportunity_id)
        opportunity = (await session.execute(opp_query)).scalar_one_or_none()
        if opportunity:
            if not data.title:
                data.title = opportunity.title
            if not data.solicitation_number:
                data.solicitation_number = opportunity.solicitation_number
            if not data.agency:
                data.agency = opportunity.agency
            if not data.naics_code:
                data.naics_code = opportunity.naics_code
            if not data.due_date:
                data.due_date = opportunity.response_deadline
            if not data.estimated_value and opportunity.estimated_value:
                data.estimated_value = float(opportunity.estimated_value)

    proposal = Proposal(
        organization_id=data.organization_id,
        opportunity_id=data.opportunity_id,
        title=data.title,
        description=data.description,
        solicitation_number=data.solicitation_number,
        agency=data.agency,
        naics_code=data.naics_code,
        due_date=data.due_date,
        estimated_value=data.estimated_value,
        created_by=current_user.id,
    )

    session.add(proposal)
    await session.commit()
    await session.refresh(proposal)

    return ProposalResponse.model_validate(proposal)


@router.get("", response_model=ProposalListResponse)
async def list_proposals(
    current_user: CurrentUser,
    session: DbSession,
    org_id: Annotated[str, Query(description="Organization ID")],
    status_filter: Annotated[Optional[str], Query(description="Status filter")] = None,
    limit: Annotated[int, Query(ge=1, le=100)] = 50,
    offset: Annotated[int, Query(ge=0)] = 0,
) -> ProposalListResponse:
    """List proposals for an organization."""

    # Verify user is member of org
    member_query = select(OrganizationMember).where(
        and_(
            OrganizationMember.organization_id == org_id,
            OrganizationMember.user_id == current_user.id,
        )
    )
    member = (await session.execute(member_query)).scalar_one_or_none()
    if not member:
        raise HTTPException(status_code=403, detail="Not a member of this organization")

    # Build query
    query = select(Proposal).where(Proposal.organization_id == org_id)

    if status_filter:
        query = query.where(Proposal.status == status_filter)

    # Get total count
    count_query = select(Proposal.id).where(Proposal.organization_id == org_id)
    if status_filter:
        count_query = count_query.where(Proposal.status == status_filter)
    total_result = await session.execute(count_query)
    total = len(total_result.all())

    # Add ordering and pagination
    query = query.order_by(Proposal.updated_at.desc())
    query = query.limit(limit).offset(offset)

    result = await session.execute(query)
    proposals = result.scalars().all()

    return ProposalListResponse(
        proposals=[ProposalResponse.model_validate(p) for p in proposals],
        total=total,
        limit=limit,
        offset=offset,
    )


@router.get("/{proposal_id}", response_model=ProposalResponse)
async def get_proposal(
    proposal_id: str,
    current_user: CurrentUser,
    session: DbSession,
) -> ProposalResponse:
    """Get proposal details."""
    query = select(Proposal).where(Proposal.id == proposal_id)
    result = await session.execute(query)
    proposal = result.scalar_one_or_none()

    if not proposal:
        raise HTTPException(status_code=404, detail="Proposal not found")

    # Verify user is member of org
    member_query = select(OrganizationMember).where(
        and_(
            OrganizationMember.organization_id == proposal.organization_id,
            OrganizationMember.user_id == current_user.id,
        )
    )
    member = (await session.execute(member_query)).scalar_one_or_none()
    if not member:
        raise HTTPException(status_code=403, detail="Not a member of this organization")

    return ProposalResponse.model_validate(proposal)


@router.put("/{proposal_id}", response_model=ProposalResponse)
async def update_proposal(
    proposal_id: str,
    data: ProposalUpdate,
    current_user: CurrentUser,
    session: DbSession,
) -> ProposalResponse:
    """Update a proposal."""
    query = select(Proposal).where(Proposal.id == proposal_id)
    result = await session.execute(query)
    proposal = result.scalar_one_or_none()

    if not proposal:
        raise HTTPException(status_code=404, detail="Proposal not found")

    # Verify user is member of org
    member_query = select(OrganizationMember).where(
        and_(
            OrganizationMember.organization_id == proposal.organization_id,
            OrganizationMember.user_id == current_user.id,
        )
    )
    member = (await session.execute(member_query)).scalar_one_or_none()
    if not member:
        raise HTTPException(status_code=403, detail="Not a member of this organization")

    # Update fields
    update_data = data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(proposal, field, value)

    proposal.updated_by = current_user.id

    await session.commit()
    await session.refresh(proposal)

    return ProposalResponse.model_validate(proposal)


@router.delete("/{proposal_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_proposal(
    proposal_id: str,
    current_user: CurrentUser,
    session: DbSession,
) -> None:
    """Delete a proposal."""
    query = select(Proposal).where(Proposal.id == proposal_id)
    result = await session.execute(query)
    proposal = result.scalar_one_or_none()

    if not proposal:
        raise HTTPException(status_code=404, detail="Proposal not found")

    # Verify user is admin/owner of org
    member_query = select(OrganizationMember).where(
        and_(
            OrganizationMember.organization_id == proposal.organization_id,
            OrganizationMember.user_id == current_user.id,
            OrganizationMember.role.in_(["admin", "owner"]),
        )
    )
    member = (await session.execute(member_query)).scalar_one_or_none()
    if not member:
        raise HTTPException(status_code=403, detail="Admin or owner role required")

    await session.delete(proposal)
    await session.commit()


@router.post("/from-opportunity", response_model=ProposalResponse)
async def create_proposal_from_opportunity(
    data: GenerateProposalRequest,
    current_user: CurrentUser,
    session: DbSession,
) -> ProposalResponse:
    """Create a new proposal from an opportunity with AI-generated content."""

    # Verify user is member of org
    member_query = select(OrganizationMember).where(
        and_(
            OrganizationMember.organization_id == data.organization_id,
            OrganizationMember.user_id == current_user.id,
        )
    )
    member = (await session.execute(member_query)).scalar_one_or_none()
    if not member:
        raise HTTPException(status_code=403, detail="Not a member of this organization")

    # Get opportunity
    opp_query = select(Opportunity).where(Opportunity.id == data.opportunity_id)
    opportunity = (await session.execute(opp_query)).scalar_one_or_none()
    if not opportunity:
        raise HTTPException(status_code=404, detail="Opportunity not found")

    # Create base proposal from opportunity data
    proposal = Proposal(
        organization_id=data.organization_id,
        opportunity_id=data.opportunity_id,
        title=f"Proposal: {opportunity.title}",
        description=opportunity.description,
        solicitation_number=opportunity.solicitation_number,
        agency=opportunity.agency,
        naics_code=opportunity.naics_code,
        due_date=opportunity.response_deadline,
        estimated_value=float(opportunity.estimated_value) if opportunity.estimated_value else None,
        created_by=current_user.id,
    )

    # Generate executive summary using Claude AI (falls back to template if no API key)
    ai_summary = await generate_executive_summary(
        title=opportunity.title,
        agency=opportunity.agency,
        description=opportunity.description,
        solicitation_number=opportunity.solicitation_number,
        naics_code=opportunity.naics_code,
        response_deadline=opportunity.response_deadline.strftime('%B %d, %Y') if opportunity.response_deadline else None,
        set_aside_type=opportunity.set_aside_type,
        estimated_value=float(opportunity.estimated_value) if opportunity.estimated_value else None,
    )

    if ai_summary:
        proposal.executive_summary = ai_summary
        proposal.ai_generated_content = {"executive_summary": {"model": "claude", "generated": True}}
    else:
        # Fallback template when Claude is not available
        proposal.executive_summary = f"""## Executive Summary

This proposal responds to {opportunity.agency}'s requirement for {opportunity.title}.

### Opportunity Overview
- **Solicitation Number:** {opportunity.solicitation_number or 'N/A'}
- **NAICS Code:** {opportunity.naics_code or 'N/A'}
- **Response Deadline:** {opportunity.response_deadline.strftime('%B %d, %Y') if opportunity.response_deadline else 'N/A'}

### Our Approach
We are pleased to submit our proposal demonstrating our capability to meet all requirements outlined in this solicitation. Our team brings extensive experience and proven expertise in delivering similar solutions.

### Key Differentiators
1. **Proven Track Record** - Demonstrated success with similar government contracts
2. **Technical Excellence** - Cutting-edge solutions tailored to agency needs
3. **Cost Efficiency** - Competitive pricing with maximum value delivery

### Conclusion
We are committed to delivering exceptional results that meet and exceed the government's requirements."""

    session.add(proposal)
    await session.commit()
    await session.refresh(proposal)

    return ProposalResponse.model_validate(proposal)
