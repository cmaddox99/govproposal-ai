"""Proposals API router."""

import json
import logging
from datetime import datetime, timezone
from typing import Annotated, Optional, List

logger = logging.getLogger(__name__)

from fastapi import APIRouter, Depends, Query, HTTPException, status
from fastapi.responses import StreamingResponse
from pydantic import BaseModel, Field
from sqlalchemy import select, and_
from sqlalchemy.ext.asyncio import AsyncSession

from govproposal.db.base import get_db
from govproposal.identity.dependencies import CurrentUser
from govproposal.identity.models import Organization, OrganizationMember, OrgPastPerformance
from govproposal.opportunities.models import Opportunity
from govproposal.proposals.models import Proposal, ProposalStatus
from govproposal.ai.service import (
    build_org_context,
    generate_all_sections,
    generate_executive_summary,
)

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
    ai_generated_content: Optional[dict] = None
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
    generate_all_content: bool = False
    sections: Optional[List[str]] = None  # Which sections to generate


class GenerateSectionsRequest(BaseModel):
    """Request to generate AI content for proposal sections."""
    sections: Optional[List[str]] = None  # None means all sections


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


# --- Helper to fetch org context for AI ---

async def _get_org_context(session: AsyncSession, org_id: str) -> str:
    """Fetch organization data and build AI context string."""
    org_query = select(Organization).where(Organization.id == org_id)
    org = (await session.execute(org_query)).scalar_one_or_none()
    if not org:
        return ""

    # Fetch past performance records
    pp_query = (
        select(OrgPastPerformance)
        .where(OrgPastPerformance.organization_id == org_id)
        .order_by(OrgPastPerformance.created_at.desc())
        .limit(5)
    )
    pp_result = await session.execute(pp_query)
    pp_records = pp_result.scalars().all()

    pp_dicts = [
        {
            "contract_name": pp.contract_name,
            "agency": pp.agency,
            "contract_number": pp.contract_number,
            "contract_value": float(pp.contract_value) if pp.contract_value else None,
            "description": pp.description,
            "performance_rating": pp.performance_rating,
        }
        for pp in pp_records
    ]

    return build_org_context(
        org_name=org.name,
        capabilities_summary=org.capabilities_summary,
        capabilities=org.capabilities,
        past_performances=pp_dicts,
        uei_number=org.uei_number,
        cage_code=org.cage_code,
    )


# --- AI content generation endpoint ---


@router.post("/{proposal_id}/generate", response_model=ProposalResponse)
async def generate_proposal_content(
    proposal_id: str,
    data: GenerateSectionsRequest,
    current_user: CurrentUser,
    session: DbSession,
) -> ProposalResponse:
    """Generate AI content for proposal sections."""
    # Fetch proposal
    query = select(Proposal).where(Proposal.id == proposal_id)
    result = await session.execute(query)
    proposal = result.scalar_one_or_none()

    if not proposal:
        raise HTTPException(status_code=404, detail="Proposal not found")

    # Verify membership
    member_query = select(OrganizationMember).where(
        and_(
            OrganizationMember.organization_id == proposal.organization_id,
            OrganizationMember.user_id == current_user.id,
        )
    )
    member = (await session.execute(member_query)).scalar_one_or_none()
    if not member:
        raise HTTPException(status_code=403, detail="Not a member of this organization")

    # Fetch opportunity for context (if linked)
    opportunity = None
    if proposal.opportunity_id:
        opp_query = select(Opportunity).where(Opportunity.id == proposal.opportunity_id)
        opportunity = (await session.execute(opp_query)).scalar_one_or_none()

    # Build org context
    org_context = await _get_org_context(session, proposal.organization_id)

    # Use opportunity data if available, otherwise use proposal data
    title = opportunity.title if opportunity else proposal.title
    description = opportunity.description if opportunity else proposal.description
    agency = opportunity.agency if opportunity else proposal.agency
    solicitation_number = opportunity.solicitation_number if opportunity else proposal.solicitation_number
    naics_code = opportunity.naics_code if opportunity else proposal.naics_code
    response_deadline = None
    if opportunity and opportunity.response_deadline:
        response_deadline = opportunity.response_deadline.strftime('%B %d, %Y')
    elif proposal.due_date:
        response_deadline = proposal.due_date.strftime('%B %d, %Y')
    set_aside_type = opportunity.set_aside_type if opportunity else None
    estimated_value = float(opportunity.estimated_value) if opportunity and opportunity.estimated_value else proposal.estimated_value

    # Generate sections
    print(f"[GENERATE] Generating sections for proposal {proposal_id}, sections={data.sections}, title={title[:50] if title else 'None'}")
    generated = await generate_all_sections(
        title=title,
        description=description,
        agency=agency,
        solicitation_number=solicitation_number,
        naics_code=naics_code,
        response_deadline=response_deadline,
        set_aside_type=set_aside_type,
        estimated_value=estimated_value,
        org_context=org_context,
        sections=data.sections,
    )

    # Update proposal with generated content
    print(f"[GENERATE] Results: {', '.join(f'{k}={len(v) if v else 0} chars' for k, v in generated.items())}")
    ai_tracking = proposal.ai_generated_content or {}
    for section_name, content in generated.items():
        if content:
            setattr(proposal, section_name, content)
            ai_tracking[section_name] = {"model": "claude", "generated": True}

    proposal.ai_generated_content = ai_tracking
    proposal.updated_by = current_user.id

    await session.commit()
    await session.refresh(proposal)

    return ProposalResponse.model_validate(proposal)


# --- Export endpoint ---


@router.get("/{proposal_id}/export")
async def export_proposal(
    proposal_id: str,
    current_user: CurrentUser,
    session: DbSession,
    format: Annotated[str, Query(description="Export format")] = "docx",
) -> StreamingResponse:
    """Export proposal as a formatted document."""
    # Fetch proposal
    query = select(Proposal).where(Proposal.id == proposal_id)
    result = await session.execute(query)
    proposal = result.scalar_one_or_none()

    if not proposal:
        raise HTTPException(status_code=404, detail="Proposal not found")

    # Verify membership
    member_query = select(OrganizationMember).where(
        and_(
            OrganizationMember.organization_id == proposal.organization_id,
            OrganizationMember.user_id == current_user.id,
        )
    )
    member = (await session.execute(member_query)).scalar_one_or_none()
    if not member:
        raise HTTPException(status_code=403, detail="Not a member of this organization")

    # Fetch organization
    org_query = select(Organization).where(Organization.id == proposal.organization_id)
    org = (await session.execute(org_query)).scalar_one_or_none()

    # Build data dicts
    proposal_data = {
        "title": proposal.title,
        "description": proposal.description,
        "agency": proposal.agency,
        "solicitation_number": proposal.solicitation_number,
        "naics_code": proposal.naics_code,
        "due_date": proposal.due_date.strftime('%B %d, %Y') if proposal.due_date else None,
        "estimated_value": proposal.estimated_value,
        "executive_summary": proposal.executive_summary,
        "technical_approach": proposal.technical_approach,
        "management_approach": proposal.management_approach,
        "past_performance": proposal.past_performance,
        "pricing_summary": proposal.pricing_summary,
    }
    org_data = {
        "name": org.name if org else "Organization",
        "uei_number": org.uei_number if org else None,
        "cage_code": org.cage_code if org else None,
    }

    from govproposal.proposals.export_service import ProposalExportService
    export_svc = ProposalExportService()
    buffer = export_svc.generate_docx(proposal_data, org_data)

    filename = f"Proposal_{proposal.solicitation_number or proposal_id}.docx"
    return StreamingResponse(
        buffer,
        media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        headers={"Content-Disposition": f'attachment; filename="{filename}"'},
    )


# --- Create from opportunity ---


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

    # Determine what to generate
    response_deadline_str = opportunity.response_deadline.strftime('%B %d, %Y') if opportunity.response_deadline else None
    est_value = float(opportunity.estimated_value) if opportunity.estimated_value else None

    if data.generate_all_content:
        # Generate all sections with org context
        org_context = await _get_org_context(session, data.organization_id)
        generated = await generate_all_sections(
            title=opportunity.title,
            description=opportunity.description,
            agency=opportunity.agency,
            solicitation_number=opportunity.solicitation_number,
            naics_code=opportunity.naics_code,
            response_deadline=response_deadline_str,
            set_aside_type=opportunity.set_aside_type,
            estimated_value=est_value,
            org_context=org_context,
            sections=data.sections,
        )

        ai_tracking = {}
        for section_name, content in generated.items():
            if content:
                setattr(proposal, section_name, content)
                ai_tracking[section_name] = {"model": "claude", "generated": True}

        if ai_tracking:
            proposal.ai_generated_content = ai_tracking
        else:
            # Fallback: set template content if AI failed
            _apply_template_content(proposal, opportunity)
    else:
        # Original behavior: just generate executive summary
        ai_summary = await generate_executive_summary(
            title=opportunity.title,
            agency=opportunity.agency,
            description=opportunity.description,
            solicitation_number=opportunity.solicitation_number,
            naics_code=opportunity.naics_code,
            response_deadline=response_deadline_str,
            set_aside_type=opportunity.set_aside_type,
            estimated_value=est_value,
        )

        if ai_summary:
            proposal.executive_summary = ai_summary
            proposal.ai_generated_content = {"executive_summary": {"model": "claude", "generated": True}}
        else:
            _apply_template_content(proposal, opportunity)

    session.add(proposal)
    await session.commit()
    await session.refresh(proposal)

    return ProposalResponse.model_validate(proposal)


def _apply_template_content(proposal: Proposal, opportunity: Opportunity) -> None:
    """Apply template fallback content when AI is not available."""
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
