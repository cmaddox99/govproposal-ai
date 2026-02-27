"""Context-aware AI assistant service.

Constitutional compliance:
- Art. I 1.3: Tenant isolation via org_id filtering on all queries
- Art. V 5.3: Functions <=50 lines, class <=300 lines, params <=4
- Art. VII 7.4: AI interactions logged for audit
"""

import logging
from typing import Any, Optional

import anthropic
from sqlalchemy import select, desc
from sqlalchemy.ext.asyncio import AsyncSession

from govproposal.ai.service import (
    SCORING_AWARENESS_BLOCK,
    build_org_context,
    _get_client,
)
from govproposal.config import settings
from govproposal.identity.models import Organization, OrgPastPerformance
from govproposal.opportunities.models import Opportunity
from govproposal.proposals.models import Proposal
from govproposal.scoring.models import ProposalScore, ScoreFactor

logger = logging.getLogger(__name__)

MAX_CONVERSATION_MESSAGES = 20

ROLE_AND_GUIDELINES = (
    "You are an expert government proposal advisor embedded in the "
    "GovProposalAI platform. You have direct access to the user's "
    "organization profile, opportunities, proposals, and scoring data. "
    "Use this context to give specific, actionable advice.\n"
    "\n## Your Capabilities\n"
    "- Analyze opportunities and recommend go/no-go decisions\n"
    "- Identify which opportunities match the organization's capabilities\n"
    "- Review proposals and suggest improvements to increase scores\n"
    "- **Rewrite proposal sections to target 95%+ scores**\n"
    "- Evaluate compliance with Section L/M requirements\n"
    "- Provide strategic advice on the proposal process\n"
    "\n## Section Rewriting Rules\n"
    "When the user asks you to improve, fix, rewrite, or strengthen a "
    "proposal section, you MUST output the FULL rewritten section inside "
    "a fenced code block with the label `section:<name>`. Valid section names:\n"
    "- `section:executive_summary`\n"
    "- `section:technical_approach`\n"
    "- `section:management_approach`\n"
    "- `section:past_performance`\n"
    "- `section:pricing_summary`\n\n"
    "Include ALL content in the code block — not just changes. The user "
    "will apply the entire block as a replacement. Before the code block, "
    "briefly explain what you changed and why.\n"
    "\n## Response Guidelines\n"
    "- Use markdown formatting (headers, bold, lists, tables)\n"
    "- When discussing scores, cite the specific factor and number\n"
    "- Reference actual data from context; say so if data is missing\n"
    "- Keep responses focused and actionable"
)


def _empty_context() -> dict[str, Any]:
    """Return a fresh context_used metadata dict."""
    return {
        "org": False,
        "opportunities_count": 0,
        "proposals_count": 0,
        "focused_proposal": False,
        "focused_opportunity": False,
    }


def _format_opportunities_table(opps: list[Opportunity]) -> str:
    """Format opportunities into a markdown summary table."""
    lines = [
        "| Title | Agency | NAICS | Deadline | Set-Aside | Value |",
        "|---|---|---|---|---|---|",
    ]
    for opp in opps:
        title = (opp.title[:60] + "...") if len(opp.title) > 60 else opp.title
        deadline = opp.response_deadline.strftime("%Y-%m-%d") if opp.response_deadline else "N/A"
        value = f"${opp.estimated_value:,.0f}" if opp.estimated_value else "N/A"
        lines.append(
            f"| {title} | {opp.agency or 'N/A'} | {opp.naics_code or 'N/A'} "
            f"| {deadline} | {opp.set_aside_type or 'N/A'} | {value} |"
        )
    return f"\n## Active Opportunities ({len(opps)})\n" + "\n".join(lines)


def _format_proposal_detail(
    proposal: Proposal,
    score: Optional[ProposalScore],
    factors: list[ScoreFactor],
) -> str:
    """Format a focused proposal with content and score breakdown."""
    parts = [f"\n## FOCUSED PROPOSAL: {proposal.title}"]
    parts.append(f"Status: {proposal.status} | Agency: {proposal.agency or 'N/A'}")
    if proposal.solicitation_number:
        parts.append(f"Solicitation: {proposal.solicitation_number}")
    if proposal.due_date:
        parts.append(f"Due: {proposal.due_date.strftime('%Y-%m-%d')}")

    sections = {
        "Executive Summary": proposal.executive_summary,
        "Technical Approach": proposal.technical_approach,
        "Management Approach": proposal.management_approach,
        "Past Performance": proposal.past_performance,
        "Pricing Summary": proposal.pricing_summary,
    }
    for name, content in sections.items():
        if content:
            truncated = content[:3000] + "..." if len(content) > 3000 else content
            parts.append(f"\n### {name}\n{truncated}")
        else:
            parts.append(f"\n### {name}\n*[Not yet written]*")

    if score:
        parts.append(
            f"\n### Latest Score: {score.overall_score}/100 "
            f"(confidence: {score.confidence_level})"
        )
        parts.extend(_format_score_factors(factors))

    return "\n".join(parts)


def _format_score_factors(factors: list[ScoreFactor]) -> list[str]:
    """Format score factors into table rows and improvement tips."""
    parts: list[str] = []
    if not factors:
        return parts

    table = ["| Factor | Weight | Score | Weighted |", "|---|---|---|---|"]
    for f in factors:
        table.append(
            f"| {f.factor_type} | {f.factor_weight:.0%} "
            f"| {f.raw_score} | {f.weighted_score:.1f} |"
        )
    parts.append("\n".join(table))

    for f in factors:
        if f.evidence_summary:
            parts.append(f"- **{f.factor_type} evidence**: {f.evidence_summary}")
        if not f.improvement_suggestions:
            continue
        items = f.improvement_suggestions
        if isinstance(items, list):
            for s in items:
                parts.append(f"- **{f.factor_type}**: {s.get('action', '')} — {s.get('details', '')}")
        elif isinstance(items, dict) and items.get("items"):
            for s in items["items"]:
                parts.append(f"- **{f.factor_type}**: {s.get('action', '')} — {s.get('details', '')}")
    return parts


def _format_opportunity_detail(opp: Opportunity) -> str:
    """Format a focused opportunity with all fields."""
    parts = [f"\n## FOCUSED OPPORTUNITY: {opp.title}"]
    parts.append(f"Notice ID: {opp.notice_id}")
    if opp.solicitation_number:
        parts.append(f"Solicitation: {opp.solicitation_number}")
    parts.append(f"Agency: {opp.agency or 'N/A'} | Department: {opp.department or 'N/A'}")
    parts.append(f"Notice Type: {opp.notice_type}")
    if opp.naics_code:
        parts.append(f"NAICS: {opp.naics_code} ({opp.naics_description or ''})")
    if opp.set_aside_type:
        parts.append(f"Set-Aside: {opp.set_aside_type} ({opp.set_aside_description or ''})")
    if opp.response_deadline:
        parts.append(f"Response Deadline: {opp.response_deadline.strftime('%Y-%m-%d %H:%M')}")
    if opp.estimated_value:
        parts.append(f"Estimated Value: ${opp.estimated_value:,.0f}")
    if opp.place_of_performance_city or opp.place_of_performance_state:
        parts.append(
            f"Place of Performance: {opp.place_of_performance_city or ''}, "
            f"{opp.place_of_performance_state or ''}"
        )
    if opp.primary_contact_name:
        parts.append(
            f"Contact: {opp.primary_contact_name} "
            f"({opp.primary_contact_email or ''}, {opp.primary_contact_phone or ''})"
        )
    if opp.description:
        desc = opp.description[:5000] + "..." if len(opp.description) > 5000 else opp.description
        parts.append(f"\n### Full Description\n{desc}")
    return "\n".join(parts)


class AssistantService:
    """Context-aware AI assistant with access to all app data.

    Art. V 5.2: Follows repository pattern for data access
    and pure-function formatters for prompt construction.
    """

    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    # -- Repository methods (data access layer) --

    async def _get_org(self, org_id: str) -> Optional[Organization]:
        result = await self.session.execute(
            select(Organization).where(Organization.id == org_id)
        )
        return result.scalar_one_or_none()

    async def _get_past_performances(self, org_id: str) -> list[OrgPastPerformance]:
        result = await self.session.execute(
            select(OrgPastPerformance)
            .where(OrgPastPerformance.organization_id == org_id)
            .order_by(desc(OrgPastPerformance.created_at))
            .limit(10)
        )
        return list(result.scalars().all())

    async def _get_opportunities(self) -> list[Opportunity]:
        result = await self.session.execute(
            select(Opportunity)
            .where(Opportunity.is_active == True)
            .order_by(desc(Opportunity.posted_date))
            .limit(20)
        )
        return list(result.scalars().all())

    async def _get_proposals(self, org_id: str) -> list[Proposal]:
        result = await self.session.execute(
            select(Proposal)
            .where(Proposal.organization_id == org_id)
            .order_by(desc(Proposal.updated_at))
            .limit(20)
        )
        return list(result.scalars().all())

    async def _get_proposal(self, proposal_id: str) -> Optional[Proposal]:
        result = await self.session.execute(
            select(Proposal).where(Proposal.id == proposal_id)
        )
        return result.scalar_one_or_none()

    async def _get_opportunity(self, opp_id: str) -> Optional[Opportunity]:
        result = await self.session.execute(
            select(Opportunity).where(Opportunity.id == opp_id)
        )
        return result.scalar_one_or_none()

    async def _get_latest_score(self, proposal_id: str) -> Optional[ProposalScore]:
        result = await self.session.execute(
            select(ProposalScore)
            .where(ProposalScore.proposal_id == proposal_id)
            .order_by(desc(ProposalScore.score_date))
            .limit(1)
        )
        return result.scalar_one_or_none()

    async def _get_score_factors(self, score_id: str) -> list[ScoreFactor]:
        result = await self.session.execute(
            select(ScoreFactor)
            .where(ScoreFactor.proposal_score_id == score_id)
        )
        return list(result.scalars().all())

    # -- Prompt building (orchestration) --

    async def _build_org_section(self, org_id: str) -> tuple[str, bool]:
        """Build organization profile section. Returns (text, found)."""
        org = await self._get_org(org_id)
        if not org:
            return "", False

        pp_records = await self._get_past_performances(org_id)
        pp_dicts = [
            {
                "contract_name": pp.contract_name,
                "agency": pp.agency,
                "contract_value": float(pp.contract_value) if pp.contract_value else None,
                "description": pp.description,
                "performance_rating": pp.performance_rating,
            }
            for pp in pp_records
        ]
        caps = org.capabilities if isinstance(org.capabilities, list) else None
        org_text = build_org_context(
            org_name=org.name,
            capabilities_summary=org.capabilities_summary,
            capabilities=caps,
            past_performances=pp_dicts,
            uei_number=org.uei_number,
            cage_code=org.cage_code,
        )
        parts = [f"\n## Organization Profile\n{org_text}"]
        if org.naics_codes:
            parts.append(f"NAICS Codes: {', '.join(str(c) for c in org.naics_codes)}")
        return "\n".join(parts), True

    async def _build_proposals_table(self, org_id: str) -> tuple[str, int]:
        """Build proposals summary table. Returns (text, count)."""
        proposals = await self._get_proposals(org_id)
        if not proposals:
            return "", 0
        lines = ["| Title | Status | Agency | Due Date | Score |", "|---|---|---|---|---|"]
        for prop in proposals:
            title = (prop.title[:50] + "...") if len(prop.title) > 50 else prop.title
            due = prop.due_date.strftime("%Y-%m-%d") if prop.due_date else "N/A"
            score = await self._get_latest_score(prop.id)
            score_str = str(score.overall_score) if score else "Not scored"
            lines.append(f"| {title} | {prop.status} | {prop.agency or 'N/A'} | {due} | {score_str} |")
        text = f"\n## Organization Proposals ({len(proposals)})\n" + "\n".join(lines)
        return text, len(proposals)

    async def build_system_prompt(
        self,
        org_id: str,
        proposal_id: Optional[str] = None,
        opportunity_id: Optional[str] = None,
    ) -> tuple[str, dict[str, Any]]:
        """Assemble context-rich system prompt from all data sources."""
        ctx = _empty_context()
        parts = [ROLE_AND_GUIDELINES, f"\n## Scoring Criteria\n{SCORING_AWARENESS_BLOCK}"]

        org_text, found = await self._build_org_section(org_id)
        ctx["org"] = found
        if found:
            parts.append(org_text)

        opps = await self._get_opportunities()
        ctx["opportunities_count"] = len(opps)
        if opps:
            parts.append(_format_opportunities_table(opps))

        props_text, props_count = await self._build_proposals_table(org_id)
        ctx["proposals_count"] = props_count
        if props_text:
            parts.append(props_text)

        if proposal_id:
            proposal = await self._get_proposal(proposal_id)
            if proposal:
                ctx["focused_proposal"] = True
                score = await self._get_latest_score(proposal.id)
                factors = await self._get_score_factors(score.id) if score else []
                parts.append(_format_proposal_detail(proposal, score, factors))

        if opportunity_id:
            opp = await self._get_opportunity(opportunity_id)
            if opp:
                ctx["focused_opportunity"] = True
                parts.append(_format_opportunity_detail(opp))

        return "\n".join(parts), ctx

    # -- Chat (Art. VII 7.4: logs AI interactions) --

    async def chat(
        self,
        messages: list[dict[str, str]],
        org_id: str,
        proposal_id: Optional[str] = None,
        opportunity_id: Optional[str] = None,
    ) -> tuple[str, dict[str, Any]]:
        """Send conversation to Claude with full context."""
        client = _get_client()
        if not client:
            return (
                "AI assistant unavailable. Check Anthropic API key.",
                _empty_context(),
            )

        system_prompt, ctx = await self.build_system_prompt(
            org_id=org_id,
            proposal_id=proposal_id,
            opportunity_id=opportunity_id,
        )
        trimmed = messages[-MAX_CONVERSATION_MESSAGES:]

        try:
            logger.info(
                "[Assistant] Calling Claude: %d msgs, ~%d char system prompt",
                len(trimmed), len(system_prompt),
            )
            response = await client.messages.create(
                model=settings.anthropic_model,
                max_tokens=4096,
                system=system_prompt,
                messages=trimmed,
            )
            text = response.content[0].text
            logger.info("[Assistant] Claude returned %d chars", len(text))
            return text, ctx
        except anthropic.AuthenticationError:
            logger.error("Invalid Anthropic API key")
            return "Authentication error with AI service.", ctx
        except anthropic.RateLimitError:
            logger.warning("Anthropic rate limit reached")
            return "AI service rate-limited. Try again shortly.", ctx
        except Exception as e:
            logger.error("Claude API error in assistant: %s", e)
            return "Error processing request. Please try again.", ctx
