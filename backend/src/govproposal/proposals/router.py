"""Proposals API router."""

import json
import logging
from datetime import datetime, timezone
from typing import Annotated, Optional, List

logger = logging.getLogger(__name__)

from fastapi import APIRouter, Depends, Query, HTTPException, Request, status
from fastapi.responses import StreamingResponse
from pydantic import BaseModel, Field
from sqlalchemy import select, and_
from sqlalchemy.ext.asyncio import AsyncSession

from govproposal.db.base import get_db
from govproposal.identity.dependencies import CurrentUser
from govproposal.security.service import AuditService
from govproposal.identity.models import Organization, OrganizationMember, OrgPastPerformance
from govproposal.opportunities.models import Opportunity
from govproposal.proposals.models import Proposal, ProposalStatus
from govproposal.ai.service import (
    build_org_context,
    generate_all_sections,
    generate_executive_summary,
    improve_proposal_section,
)
from govproposal.scoring.service import ScoringService
from govproposal.events.bus import Event, event_bus
from govproposal.events.types import EventTypes

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


class ImproveRequest(BaseModel):
    """Request to improve proposal sections using score feedback."""
    sections: Optional[List[str]] = None  # None = all sections
    target_score: int = Field(default=95, ge=1, le=100)


class ImproveResponse(BaseModel):
    """Response from proposal improvement."""
    proposal: ProposalResponse
    improved_sections: List[str]
    previous_score: Optional[int] = None
    new_score: Optional[int] = None


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
    request: Request,
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

    audit = AuditService(session)
    await audit.log_event(
        event_type="proposal_created",
        action="Proposal created",
        actor_id=current_user.id,
        actor_email=current_user.email,
        organization_id=data.organization_id,
        resource_type="proposal",
        resource_id=proposal.id,
        ip_address=request.client.host if request.client else None,
        details={"title": proposal.title},
    )

    await event_bus.publish(Event(
        type=EventTypes.PROPOSAL_CREATED,
        data={
            "proposal_id": proposal.id,
            "title": proposal.title,
            "organization_id": data.organization_id,
            "actor_id": current_user.id,
        },
    ))

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
    request: Request,
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

    audit = AuditService(session)
    await audit.log_event(
        event_type="proposal_updated",
        action="Proposal updated",
        actor_id=current_user.id,
        actor_email=current_user.email,
        organization_id=proposal.organization_id,
        resource_type="proposal",
        resource_id=proposal_id,
        ip_address=request.client.host if request.client else None,
        details={"updated_fields": list(update_data.keys())},
    )

    return ProposalResponse.model_validate(proposal)


@router.delete("/{proposal_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_proposal(
    proposal_id: str,
    current_user: CurrentUser,
    session: DbSession,
    request: Request,
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

    org_id = proposal.organization_id
    title = proposal.title
    await session.delete(proposal)
    await session.commit()

    audit = AuditService(session)
    await audit.log_event(
        event_type="proposal_deleted",
        action="Proposal deleted",
        actor_id=current_user.id,
        actor_email=current_user.email,
        organization_id=org_id,
        resource_type="proposal",
        resource_id=proposal_id,
        ip_address=request.client.host if request.client else None,
        details={"title": title},
    )


async def _fetch_and_verify_proposal(
    proposal_id: str, user_id: str, session: DbSession,
) -> Proposal:
    """Fetch proposal and verify user's org membership."""
    query = select(Proposal).where(Proposal.id == proposal_id)
    proposal = (await session.execute(query)).scalar_one_or_none()
    if not proposal:
        raise HTTPException(status_code=404, detail="Proposal not found")

    member_query = select(OrganizationMember).where(and_(
        OrganizationMember.organization_id == proposal.organization_id,
        OrganizationMember.user_id == user_id,
    ))
    if not (await session.execute(member_query)).scalar_one_or_none():
        raise HTTPException(status_code=403, detail="Not a member of this organization")
    return proposal


def _resolve_generation_fields(
    proposal: Proposal, opportunity: Optional[Opportunity],
) -> dict:
    """Resolve proposal/opportunity fields for AI section generation."""
    opp = opportunity
    deadline = None
    if opp and opp.response_deadline:
        deadline = opp.response_deadline.strftime('%B %d, %Y')
    elif proposal.due_date:
        deadline = proposal.due_date.strftime('%B %d, %Y')

    return {
        "title": opp.title if opp else proposal.title,
        "description": opp.description if opp else proposal.description,
        "agency": opp.agency if opp else proposal.agency,
        "solicitation_number": opp.solicitation_number if opp else proposal.solicitation_number,
        "naics_code": opp.naics_code if opp else proposal.naics_code,
        "response_deadline": deadline,
        "set_aside_type": opp.set_aside_type if opp else None,
        "estimated_value": float(opp.estimated_value) if opp and opp.estimated_value else proposal.estimated_value,
    }


def _apply_generated_sections(
    proposal: Proposal, generated: dict[str, Optional[str]],
) -> list[str]:
    """Apply AI-generated sections to proposal and return section names."""
    ai_tracking = proposal.ai_generated_content or {}
    for section_name, content in generated.items():
        if content:
            setattr(proposal, section_name, content)
            ai_tracking[section_name] = {"model": "claude", "generated": True}
    proposal.ai_generated_content = ai_tracking
    return list(generated.keys())


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
    request: Request,
) -> ProposalResponse:
    """Generate AI content for proposal sections."""
    proposal = await _fetch_and_verify_proposal(proposal_id, current_user.id, session)

    opportunity = None
    if proposal.opportunity_id:
        opp_q = select(Opportunity).where(Opportunity.id == proposal.opportunity_id)
        opportunity = (await session.execute(opp_q)).scalar_one_or_none()

    fields = _resolve_generation_fields(proposal, opportunity)
    org_context = await _get_org_context(session, proposal.organization_id)

    generated = await generate_all_sections(
        **fields, org_context=org_context, sections=data.sections,
    )

    sections = _apply_generated_sections(proposal, generated)
    proposal.updated_by = current_user.id
    await session.commit()
    await session.refresh(proposal)

    audit = AuditService(session)
    await audit.log_event(
        event_type="proposal_updated",
        action="AI content generated for proposal",
        actor_id=current_user.id,
        actor_email=current_user.email,
        organization_id=proposal.organization_id,
        resource_type="proposal",
        resource_id=proposal_id,
        ip_address=request.client.host if request.client else None,
        details={"sections_generated": sections},
    )

    return ProposalResponse.model_validate(proposal)


# --- Improve endpoint ---


ALL_SECTION_NAMES = [
    "executive_summary", "technical_approach", "management_approach",
    "past_performance", "pricing_summary",
]


@router.post("/{proposal_id}/improve", response_model=ImproveResponse)
async def improve_proposal(
    proposal_id: str,
    data: ImproveRequest,
    current_user: CurrentUser,
    session: DbSession,
    request: Request,
) -> ImproveResponse:
    """Improve proposal sections using AI with score feedback."""
    proposal = await _fetch_and_verify_proposal(proposal_id, current_user.id, session)

    # Get latest score (or calculate fresh)
    scoring_svc = ScoringService(session)
    score_resp = await scoring_svc.get_latest_score(proposal_id)
    if not score_resp:
        proposal_data = {
            "title": proposal.title,
            "description": proposal.description,
            "executive_summary": proposal.executive_summary,
            "technical_approach": proposal.technical_approach,
            "management_approach": proposal.management_approach,
            "past_performance": proposal.past_performance,
            "pricing_summary": proposal.pricing_summary,
        }
        score_resp = await scoring_svc.calculate_score(
            proposal_id, current_user.id, proposal_data,
        )

    previous_score = score_resp.overall_score if score_resp else None

    # Build score feedback from factors
    score_feedback = []
    if score_resp and score_resp.factors:
        for f in score_resp.factors:
            score_feedback.append({
                "factor_type": f.factor_type,
                "raw_score": f.raw_score,
                "evidence_summary": f.evidence_summary or "",
                "improvement_suggestions": f.improvement_suggestions,
            })

    # Determine which sections to improve
    target_sections = data.sections or ALL_SECTION_NAMES
    target_sections = [s for s in target_sections if s in ALL_SECTION_NAMES]

    # Get org context
    org_context = await _get_org_context(session, proposal.organization_id)

    # Improve each section that has content or is requested
    improved_sections: list[str] = []
    ai_tracking = proposal.ai_generated_content or {}

    for section_name in target_sections:
        current_content = getattr(proposal, section_name, None)
        if not current_content:
            continue

        improved = await improve_proposal_section(
            section_type=section_name,
            current_content=current_content,
            score_feedback=score_feedback,
            title=proposal.title,
            description=proposal.description,
            agency=proposal.agency,
            solicitation_number=proposal.solicitation_number,
            naics_code=proposal.naics_code,
            org_context=org_context,
        )
        if improved:
            setattr(proposal, section_name, improved)
            ai_tracking[section_name] = {"model": "claude_improvement", "generated": True}
            improved_sections.append(section_name)

    proposal.ai_generated_content = ai_tracking
    proposal.updated_by = current_user.id
    await session.commit()
    await session.refresh(proposal)

    # Re-score with improved content
    new_score_val = None
    if improved_sections:
        proposal_data = {
            "title": proposal.title,
            "description": proposal.description,
            "executive_summary": proposal.executive_summary,
            "technical_approach": proposal.technical_approach,
            "management_approach": proposal.management_approach,
            "past_performance": proposal.past_performance,
            "pricing_summary": proposal.pricing_summary,
        }
        new_score = await scoring_svc.calculate_score(
            proposal_id, current_user.id, proposal_data,
        )
        new_score_val = new_score.overall_score if new_score else None

    audit = AuditService(session)
    await audit.log_event(
        event_type="proposal_improved",
        action="AI-powered proposal improvement",
        actor_id=current_user.id,
        actor_email=current_user.email,
        organization_id=proposal.organization_id,
        resource_type="proposal",
        resource_id=proposal_id,
        ip_address=request.client.host if request.client else None,
        details={
            "improved_sections": improved_sections,
            "previous_score": previous_score,
            "new_score": new_score_val,
        },
    )

    return ImproveResponse(
        proposal=ProposalResponse.model_validate(proposal),
        improved_sections=improved_sections,
        previous_score=previous_score,
        new_score=new_score_val,
    )


# --- Export endpoint ---


def _build_export_data(
    proposal: Proposal, org: Optional[Organization],
) -> tuple[dict, dict]:
    """Build proposal and org dicts for export service."""
    proposal_data = {
        "title": proposal.title, "description": proposal.description,
        "agency": proposal.agency, "solicitation_number": proposal.solicitation_number,
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
    return proposal_data, org_data


@router.get("/{proposal_id}/export")
async def export_proposal(
    proposal_id: str,
    current_user: CurrentUser,
    session: DbSession,
    request: Request,
    format: Annotated[str, Query(description="Export format")] = "docx",
) -> StreamingResponse:
    """Export proposal as a formatted document."""
    proposal = await _fetch_and_verify_proposal(proposal_id, current_user.id, session)

    org_q = select(Organization).where(Organization.id == proposal.organization_id)
    org = (await session.execute(org_q)).scalar_one_or_none()

    proposal_data, org_data = _build_export_data(proposal, org)

    from govproposal.proposals.export_service import ProposalExportService
    buffer = ProposalExportService().generate_docx(proposal_data, org_data)

    audit = AuditService(session)
    await audit.log_event(
        event_type="proposal_exported", action="Proposal exported",
        actor_id=current_user.id, actor_email=current_user.email,
        organization_id=proposal.organization_id,
        resource_type="proposal", resource_id=proposal_id,
        ip_address=request.client.host if request.client else None,
        details={"format": format},
    )

    filename = f"Proposal_{proposal.solicitation_number or proposal_id}.docx"
    return StreamingResponse(
        buffer,
        media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        headers={"Content-Disposition": f'attachment; filename="{filename}"'},
    )


# --- Create from opportunity ---


async def _populate_ai_content(
    proposal: Proposal, opportunity: Opportunity,
    session: DbSession, data: GenerateProposalRequest,
) -> None:
    """Generate AI content for a new proposal from an opportunity."""
    fields = _resolve_generation_fields(proposal, opportunity)
    org_context = await _get_org_context(session, data.organization_id)

    if data.generate_all_content:
        generated = await generate_all_sections(
            **fields, org_context=org_context, sections=data.sections,
        )
        _apply_generated_sections(proposal, generated)
        if not proposal.ai_generated_content:
            _apply_template_content(proposal, opportunity)
    else:
        ai_summary = await generate_executive_summary(
            title=fields["title"], agency=fields["agency"],
            description=fields["description"],
            solicitation_number=fields["solicitation_number"],
            naics_code=fields["naics_code"],
            response_deadline=fields["response_deadline"],
            set_aside_type=fields["set_aside_type"],
            estimated_value=fields["estimated_value"],
        )
        if ai_summary:
            proposal.executive_summary = ai_summary
            proposal.ai_generated_content = {"executive_summary": {"model": "claude", "generated": True}}
        else:
            _apply_template_content(proposal, opportunity)


@router.post("/from-opportunity", response_model=ProposalResponse)
async def create_proposal_from_opportunity(
    data: GenerateProposalRequest,
    current_user: CurrentUser,
    session: DbSession,
    request: Request,
) -> ProposalResponse:
    """Create a new proposal from an opportunity with AI-generated content."""
    member_q = select(OrganizationMember).where(and_(
        OrganizationMember.organization_id == data.organization_id,
        OrganizationMember.user_id == current_user.id,
    ))
    if not (await session.execute(member_q)).scalar_one_or_none():
        raise HTTPException(status_code=403, detail="Not a member of this organization")

    opp_q = select(Opportunity).where(Opportunity.id == data.opportunity_id)
    opportunity = (await session.execute(opp_q)).scalar_one_or_none()
    if not opportunity:
        raise HTTPException(status_code=404, detail="Opportunity not found")

    proposal = Proposal(
        organization_id=data.organization_id, opportunity_id=data.opportunity_id,
        title=f"Proposal: {opportunity.title}", description=opportunity.description,
        solicitation_number=opportunity.solicitation_number, agency=opportunity.agency,
        naics_code=opportunity.naics_code, due_date=opportunity.response_deadline,
        estimated_value=float(opportunity.estimated_value) if opportunity.estimated_value else None,
        created_by=current_user.id,
    )

    await _populate_ai_content(proposal, opportunity, session, data)

    session.add(proposal)
    await session.commit()
    await session.refresh(proposal)

    audit = AuditService(session)
    await audit.log_event(
        event_type="proposal_created", action="Proposal created from opportunity",
        actor_id=current_user.id, actor_email=current_user.email,
        organization_id=data.organization_id,
        resource_type="proposal", resource_id=proposal.id,
        ip_address=request.client.host if request.client else None,
        details={"opportunity_id": data.opportunity_id, "ai_generated": data.generate_all_content},
    )
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
