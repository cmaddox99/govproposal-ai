"""AI Assistant API router.

Constitutional compliance:
- Art. I 1.3: Org membership check before access
- Art. I 1.4: Versioned API (/api/v1/)
- Art. VII 7.4: AI interactions logged for audit
- Art. VIII 8.3: Audit trail for all AI usage
"""

import json
import logging
from typing import Annotated, Optional

from fastapi import APIRouter, Depends, HTTPException, Request
from pydantic import BaseModel, Field
from sqlalchemy.ext.asyncio import AsyncSession

from sqlalchemy import select, and_

from govproposal.ai.service import _get_client
from govproposal.assistant.service import AssistantService
from govproposal.config import settings
from govproposal.db.base import get_db
from govproposal.identity.dependencies import CurrentUser
from govproposal.identity.models import OrganizationMember, OrgPastPerformance
from govproposal.identity.repository import OrganizationRepository
from govproposal.proposals.models import Proposal
from govproposal.security.service import AuditService

logger = logging.getLogger(__name__)

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


# --- Extract structured field updates from freeform content ---

EXTRACTABLE_FIELDS = {
    "title", "description", "agency", "solicitation_number", "naics_code",
    "estimated_value", "proposed_value", "due_date",
    "executive_summary", "technical_approach", "management_approach",
    "past_performance", "pricing_summary",
}


class PastPerformanceRecord(BaseModel):
    contract_name: str
    agency: Optional[str] = None
    contract_value: Optional[float] = None
    description: Optional[str] = None
    contact_name: Optional[str] = None
    contact_email: Optional[str] = None


class ExtractRequest(BaseModel):
    proposal_id: str
    content: str
    instruction: Optional[str] = None


class FieldUpdate(BaseModel):
    field: str
    value: str
    note: Optional[str] = None


class ExtractResponse(BaseModel):
    field_updates: list[FieldUpdate]
    new_past_performance: list[PastPerformanceRecord] = []
    summary: str


EXTRACT_PROMPT = (
    "You are a data-extraction assistant for a government-proposal platform. "
    "The user has pasted content (notes, RFP excerpts, past-performance write-ups, "
    "pricing, or freeform context) into the chat. Your job is to extract structured "
    "field updates for the current proposal and any new past-performance records.\n\n"
    "Return ONLY valid JSON with this exact shape (no markdown, no code fences):\n"
    "{\n"
    '  "field_updates": [ {"field": "<field>", "value": "<value>", "note": "<short why>"} ],\n'
    '  "new_past_performance": [ {"contract_name": "...", "agency": "...", "contract_value": 0, "description": "...", "contact_name": "...", "contact_email": "..."} ],\n'
    '  "summary": "<one-sentence summary>"\n'
    "}\n\n"
    "Valid field names ONLY: title, description, agency, solicitation_number, naics_code, "
    "estimated_value (number), proposed_value (number), due_date (ISO 8601), "
    "executive_summary, technical_approach, management_approach, past_performance, "
    "pricing_summary.\n\n"
    "Rules:\n"
    "- Only include a field_update if the content clearly provides that value.\n"
    "- For long-form content (e.g. past-performance write-ups), prefer adding to "
    "  new_past_performance OR routing into the past_performance section field.\n"
    "- For pricing tables/breakdowns, route into pricing_summary.\n"
    "- Be conservative — better to skip an uncertain field than guess.\n"
    "- Never wrap output in markdown fences. Output raw JSON only."
)


@router.post("/extract", response_model=ExtractResponse)
async def extract_proposal_updates(
    data: ExtractRequest,
    current_user: CurrentUser,
    session: DbSession,
    request: Request,
) -> ExtractResponse:
    """Extract structured field updates from freeform chat content.

    The user pastes notes, past performance, pricing, or RFP excerpts into the
    chat; this endpoint asks Claude to map that into a structured set of field
    updates the frontend can preview and apply.
    """
    proposal = (await session.execute(
        select(Proposal).where(Proposal.id == data.proposal_id)
    )).scalar_one_or_none()
    if not proposal:
        raise HTTPException(status_code=404, detail="Proposal not found")

    member = (await session.execute(select(OrganizationMember).where(and_(
        OrganizationMember.organization_id == proposal.organization_id,
        OrganizationMember.user_id == current_user.id,
    )))).scalar_one_or_none()
    if not member:
        raise HTTPException(status_code=403, detail="Not a member of this organization")

    client = _get_client()
    if not client:
        raise HTTPException(
            status_code=503,
            detail="AI extraction unavailable — Anthropic API key not configured.",
        )

    proposal_context = (
        f"Proposal title: {proposal.title}\n"
        f"Agency: {proposal.agency or '(none)'}\n"
        f"Solicitation: {proposal.solicitation_number or '(none)'}\n"
        f"NAICS: {proposal.naics_code or '(none)'}\n"
    )
    user_msg = (
        f"{proposal_context}\n\n"
        f"User instruction: {data.instruction or 'Extract relevant updates from this content.'}\n\n"
        f"Content to extract from:\n{data.content}"
    )

    try:
        response = await client.messages.create(
            model=settings.anthropic_model,
            max_tokens=2000,
            system=EXTRACT_PROMPT,
            messages=[{"role": "user", "content": user_msg}],
        )
    except Exception as exc:
        logger.exception("Extract call failed")
        raise HTTPException(status_code=503, detail=f"AI extraction failed: {exc}")

    raw_text = response.content[0].text if response.content else ""
    # Be lenient: strip code fences if model included them anyway
    cleaned = raw_text.strip()
    if cleaned.startswith("```"):
        cleaned = cleaned.split("\n", 1)[1] if "\n" in cleaned else cleaned
        if cleaned.endswith("```"):
            cleaned = cleaned[:-3]
        cleaned = cleaned.strip()
        if cleaned.startswith("json"):
            cleaned = cleaned[4:].strip()

    try:
        parsed = json.loads(cleaned)
    except json.JSONDecodeError:
        logger.warning("Extract returned non-JSON: %s", raw_text[:200])
        raise HTTPException(
            status_code=502,
            detail="AI returned malformed output. Try rephrasing your content.",
        )

    # Filter to allowed fields only
    updates = []
    for entry in parsed.get("field_updates", []) or []:
        if not isinstance(entry, dict):
            continue
        field = entry.get("field")
        value = entry.get("value")
        if field in EXTRACTABLE_FIELDS and value is not None:
            updates.append(FieldUpdate(
                field=field,
                value=str(value),
                note=entry.get("note"),
            ))

    new_pp = []
    for entry in parsed.get("new_past_performance", []) or []:
        if not isinstance(entry, dict) or not entry.get("contract_name"):
            continue
        new_pp.append(PastPerformanceRecord(**{
            k: v for k, v in entry.items()
            if k in {"contract_name", "agency", "contract_value", "description",
                     "contact_name", "contact_email"}
        }))

    return ExtractResponse(
        field_updates=updates,
        new_past_performance=new_pp,
        summary=parsed.get("summary", ""),
    )


# --- Apply extracted updates ---

class ApplyExtractRequest(BaseModel):
    proposal_id: str
    field_updates: list[FieldUpdate] = []
    new_past_performance: list[PastPerformanceRecord] = []


class ApplyExtractResponse(BaseModel):
    applied_fields: list[str]
    created_past_performance_ids: list[str]


@router.post("/apply-extract", response_model=ApplyExtractResponse)
async def apply_extract(
    data: ApplyExtractRequest,
    current_user: CurrentUser,
    session: DbSession,
) -> ApplyExtractResponse:
    """Apply extracted field updates and add new past-performance records."""
    from datetime import datetime, timezone

    proposal = (await session.execute(
        select(Proposal).where(Proposal.id == data.proposal_id)
    )).scalar_one_or_none()
    if not proposal:
        raise HTTPException(status_code=404, detail="Proposal not found")

    member = (await session.execute(select(OrganizationMember).where(and_(
        OrganizationMember.organization_id == proposal.organization_id,
        OrganizationMember.user_id == current_user.id,
    )))).scalar_one_or_none()
    if not member:
        raise HTTPException(status_code=403, detail="Not a member of this organization")

    applied = []
    for update in data.field_updates:
        if update.field not in EXTRACTABLE_FIELDS:
            continue
        value: object = update.value
        if update.field in {"estimated_value", "proposed_value"}:
            try:
                value = float(str(update.value).replace("$", "").replace(",", "").strip())
            except (ValueError, TypeError):
                continue
        elif update.field == "due_date":
            try:
                value = datetime.fromisoformat(str(update.value).replace("Z", "+00:00"))
            except ValueError:
                continue
        setattr(proposal, update.field, value)
        applied.append(update.field)
    proposal.updated_by = current_user.id

    created_ids = []
    for pp in data.new_past_performance:
        record = OrgPastPerformance(
            organization_id=proposal.organization_id,
            contract_name=pp.contract_name,
            agency=pp.agency,
            contract_value=pp.contract_value,
            description=pp.description,
            contact_name=pp.contact_name,
            contact_email=pp.contact_email,
        )
        session.add(record)
        await session.flush()
        created_ids.append(record.id)

    await session.commit()
    return ApplyExtractResponse(
        applied_fields=applied,
        created_past_performance_ids=created_ids,
    )
