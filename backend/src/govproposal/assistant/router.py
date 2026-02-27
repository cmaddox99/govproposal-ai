"""AI Assistant API router.

Constitutional compliance:
- Art. I 1.3: Org membership check before access
- Art. I 1.4: Versioned API (/api/v1/)
- Art. VII 7.4: AI interactions logged for audit
- Art. VIII 8.3: Audit trail for all AI usage
"""

from typing import Annotated, Optional

from fastapi import APIRouter, Depends, HTTPException, Request
from pydantic import BaseModel, Field
from sqlalchemy.ext.asyncio import AsyncSession

from sqlalchemy import select, and_

from govproposal.assistant.service import AssistantService
from govproposal.db.base import get_db
from govproposal.identity.dependencies import CurrentUser
from govproposal.identity.models import OrganizationMember
from govproposal.identity.repository import OrganizationRepository
from govproposal.proposals.models import Proposal
from govproposal.security.service import AuditService

router = APIRouter(prefix="/api/v1/assistant", tags=["assistant"])

DbSession = Annotated[AsyncSession, Depends(get_db)]


class ChatMessage(BaseModel):
    role: str = Field(..., pattern="^(user|assistant)$")
    content: str


class ChatContext(BaseModel):
    org_id: str
    proposal_id: Optional[str] = None
    opportunity_id: Optional[str] = None


class ChatRequest(BaseModel):
    messages: list[ChatMessage]
    context: ChatContext


class ChatResponse(BaseModel):
    message: str
    context_used: dict


@router.post("/chat", response_model=ChatResponse)
async def assistant_chat(
    data: ChatRequest,
    current_user: CurrentUser,
    session: DbSession,
    request: Request,
) -> ChatResponse:
    """Chat with the context-aware AI assistant."""
    if not data.context.org_id:
        raise HTTPException(
            status_code=400,
            detail="Organization ID is required. Please select an organization first.",
        )

    # Art. I 1.3: Verify org membership
    org_repo = OrganizationRepository(session)
    member = await org_repo.get_member(data.context.org_id, current_user.id)
    if not member:
        raise HTTPException(
            status_code=403,
            detail="Not a member of this organization",
        )

    service = AssistantService(session)
    response_text, context_used = await service.chat(
        messages=[m.model_dump() for m in data.messages],
        org_id=data.context.org_id,
        proposal_id=data.context.proposal_id,
        opportunity_id=data.context.opportunity_id,
    )

    # Art. VII 7.4 + Art. VIII 8.3: Log AI interaction for audit
    audit = AuditService(session)
    await audit.log_event(
        event_type="ai_assistant_chat",
        action="AI assistant chat interaction",
        actor_id=current_user.id,
        actor_email=current_user.email,
        organization_id=data.context.org_id,
        resource_type="assistant",
        ip_address=request.client.host if request.client else None,
        details={
            "message_count": len(data.messages),
            "context_used": context_used,
            "proposal_id": data.context.proposal_id,
            "opportunity_id": data.context.opportunity_id,
        },
    )

    return ChatResponse(message=response_text, context_used=context_used)


# --- Apply section rewrite from assistant ---

VALID_SECTION_NAMES = {
    "executive_summary", "technical_approach", "management_approach",
    "past_performance", "pricing_summary",
}


class ApplySectionRequest(BaseModel):
    proposal_id: str
    section_name: str
    content: str


class ApplySectionResponse(BaseModel):
    proposal_id: str
    section_name: str
    success: bool


@router.post("/apply-section", response_model=ApplySectionResponse)
async def apply_section(
    data: ApplySectionRequest,
    current_user: CurrentUser,
    session: DbSession,
    request: Request,
) -> ApplySectionResponse:
    """Apply an assistant-generated section rewrite to a proposal."""
    # Validate section name
    if data.section_name not in VALID_SECTION_NAMES:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid section name. Must be one of: {', '.join(sorted(VALID_SECTION_NAMES))}",
        )

    # Fetch proposal
    query = select(Proposal).where(Proposal.id == data.proposal_id)
    proposal = (await session.execute(query)).scalar_one_or_none()
    if not proposal:
        raise HTTPException(status_code=404, detail="Proposal not found")

    # Verify org membership
    member_query = select(OrganizationMember).where(and_(
        OrganizationMember.organization_id == proposal.organization_id,
        OrganizationMember.user_id == current_user.id,
    ))
    if not (await session.execute(member_query)).scalar_one_or_none():
        raise HTTPException(status_code=403, detail="Not a member of this organization")

    # Apply the section content
    setattr(proposal, data.section_name, data.content)

    # Track as assistant rewrite
    ai_tracking = proposal.ai_generated_content or {}
    ai_tracking[data.section_name] = {"model": "assistant_rewrite", "generated": True}
    proposal.ai_generated_content = ai_tracking
    proposal.updated_by = current_user.id

    await session.commit()

    # Audit log
    audit = AuditService(session)
    await audit.log_event(
        event_type="proposal_section_applied",
        action="Assistant section rewrite applied",
        actor_id=current_user.id,
        actor_email=current_user.email,
        organization_id=proposal.organization_id,
        resource_type="proposal",
        resource_id=data.proposal_id,
        ip_address=request.client.host if request.client else None,
        details={"section_name": data.section_name},
    )

    return ApplySectionResponse(
        proposal_id=data.proposal_id,
        section_name=data.section_name,
        success=True,
    )
