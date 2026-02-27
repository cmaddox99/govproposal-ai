"""AI service for generating proposal content and scoring using Claude."""

import json
import logging
from typing import Any, Optional

import anthropic

from govproposal.config import settings

logger = logging.getLogger(__name__)


def _get_client() -> Optional[anthropic.AsyncAnthropic]:
    """Get an async Anthropic client, or None if not configured."""
    if not settings.anthropic_api_key:
        print("[AI] ANTHROPIC_API_KEY is not set or empty")
        return None
    print(f"[AI] Anthropic async client initialized, key starts with: {settings.anthropic_api_key[:12]}...")
    return anthropic.AsyncAnthropic(api_key=settings.anthropic_api_key)



async def score_with_claude(
    system_prompt: str,
    user_prompt: str,
) -> Optional[dict[str, Any]]:
    """Call Claude to score a proposal factor.

    Returns parsed JSON dict on success, None on failure (caller should use fallback).
    """
    client = _get_client()
    if not client:
        logger.info("Anthropic API key not configured, skipping AI scoring")
        return None

    try:
        message = await client.messages.create(
            model=settings.anthropic_model,
            max_tokens=1024,
            messages=[
                {"role": "user", "content": user_prompt}
            ],
            system=system_prompt,
        )

        text = message.content[0].text

        # Claude may wrap JSON in markdown code blocks
        if "```json" in text:
            text = text.split("```json")[1].split("```")[0]
        elif "```" in text:
            text = text.split("```")[1].split("```")[0]

        return json.loads(text.strip())

    except json.JSONDecodeError as e:
        logger.warning(f"Claude returned non-JSON response: {e}")
        return None
    except anthropic.AuthenticationError:
        logger.error("Invalid Anthropic API key")
        return None
    except anthropic.RateLimitError:
        logger.warning("Anthropic rate limit reached")
        return None
    except Exception as e:
        logger.error(f"Claude API error during scoring: {e}")
        return None


# --- Organization context builder ---


def build_org_context(
    org_name: str,
    capabilities_summary: Optional[str] = None,
    capabilities: Optional[list[dict]] = None,
    past_performances: Optional[list[dict]] = None,
    uei_number: Optional[str] = None,
    cage_code: Optional[str] = None,
) -> str:
    """Build organization context block for AI prompts."""
    parts = [f"Organization: {org_name}"]

    if uei_number:
        parts.append(f"UEI: {uei_number}")
    if cage_code:
        parts.append(f"CAGE Code: {cage_code}")

    if capabilities_summary:
        parts.append(f"\nCompany Overview:\n{capabilities_summary}")

    if capabilities:
        cap_lines = []
        for cap in capabilities[:10]:
            name = cap.get("name", "")
            desc = cap.get("description", "")
            cap_lines.append(f"- {name}: {desc}" if desc else f"- {name}")
        parts.append(f"\nKey Capabilities:\n" + "\n".join(cap_lines))

    if past_performances:
        pp_lines = []
        for pp in past_performances[:5]:
            line = f"- {pp.get('contract_name', 'Unknown')}"
            if pp.get("agency"):
                line += f" ({pp['agency']})"
            if pp.get("contract_value"):
                line += f" — ${pp['contract_value']:,.0f}"
            if pp.get("description"):
                desc = pp["description"][:200]
                line += f"\n  {desc}"
            if pp.get("performance_rating"):
                line += f"\n  Rating: {pp['performance_rating']}"
            pp_lines.append(line)
        parts.append(f"\nRelevant Past Performance:\n" + "\n".join(pp_lines))

    return "\n".join(parts)


# --- Scoring-awareness block appended to all section instructions ---

SCORING_AWARENESS_BLOCK = """

SCORING CRITERIA — optimize your content to score 95+ on EACH of these factors:

1. COMPLETENESS (30% weight):
   - Include ALL required subsections with substantive, detailed content
   - Never use placeholder text, "TBD", "[INSERT]", or leave any gaps
   - Meet or exceed the target word count for this section
   - Reference all required attachments and exhibits
   - Every expected element must be present and fully developed

2. TECHNICAL DEPTH (30% weight):
   - Name specific methodologies, tools, technologies, frameworks, and standards (e.g., "PMI PMBOK 7th Edition", "Agile SAFe 6.0", "NIST SP 800-53 Rev 5") — not just "industry best practices"
   - Describe concrete processes step-by-step, not abstract concepts
   - Show deep domain understanding by using precise terminology from this work area
   - Justify each technical choice — explain WHY this approach fits THIS requirement
   - Avoid generic boilerplate that could apply to any proposal
   - Connect every technical element back to a specific requirement

3. SECTION L COMPLIANCE (20% weight):
   - Follow standard government proposal format conventions
   - Use proper section numbering and organization (##, ###)
   - Address every element that would typically appear in Section L instructions
   - Include required certifications and representations references where relevant
   - Structure content so evaluators can easily find each required element

4. SECTION M ALIGNMENT (20% weight):
   - Organize content so each evaluation criterion is explicitly and visibly addressed
   - Present clear discriminators — what makes this offeror uniquely qualified
   - Weave win themes throughout (not just in the summary)
   - Use headings and structure that mirror typical evaluation factors
   - Make it effortless for an evaluator to award maximum points on every factor

CRITICAL INSTRUCTIONS:
- Do NOT use vague phrases: "best practices", "industry standard", "as needed", "as appropriate", "state-of-the-art", "cutting-edge", "world-class"
- DO use specific names: tools, frameworks, standards, regulations, methodologies
- Every paragraph must contain at least one concrete, verifiable detail
- Structure content with clear headers that map to evaluation criteria
"""

SECTION_SCORING_GUIDANCE: dict[str, str] = {
    "executive_summary": """
SECTION-SPECIFIC SCORING GUIDANCE (Executive Summary):
- Demonstrate completeness by touching on every major proposal theme (technical, management, past performance, pricing approach) even briefly
- Show technical depth by naming your primary methodology and key tools in the summary
- For compliance, reference the solicitation number, NAICS, set-aside type, and agency explicitly
- For evaluation alignment, state your top 3 discriminators as a bulleted list and present 2-3 win themes clearly
""",
    "technical_approach": """
SECTION-SPECIFIC SCORING GUIDANCE (Technical Approach):
- Name specific tools, frameworks, platforms, and standards (e.g., "Jira for task tracking", "Jenkins CI/CD pipeline", "ISO 27001 controls")
- Include a phased work breakdown with named phases, deliverables per phase, and milestone dates
- For each technical solution element, state: the requirement it addresses, the approach, and why it is superior
- Include a risk register with at least 3 risks, their likelihood, impact, and specific mitigation strategies
- Reference relevant FAR/DFAR clauses, OMB circulars, or agency-specific standards by number
- Quantify where possible: team size, response times, SLA targets, throughput metrics
""",
    "management_approach": """
SECTION-SPECIFIC SCORING GUIDANCE (Management Approach):
- Name specific management frameworks (PMI PMBOK, ITIL 4, SAFe, CMMI Level 3+, ISO 9001)
- Define an explicit organizational chart description with named roles and reporting relationships
- Include specific staffing numbers, labor categories, and FTE allocations
- Detail your transition plan with a timeline for the first 30/60/90 days
- Describe specific QA/QC tools and processes (e.g., peer review checklists, automated quality gates)
- Include communication cadence: weekly status reports, monthly program reviews, quarterly executive briefings
""",
    "past_performance": """
SECTION-SPECIFIC SCORING GUIDANCE (Past Performance):
- For each contract, quantify outcomes: "delivered 15% under budget", "99.9% uptime", "zero security incidents over 3 years"
- Draw explicit parallels: "This contract required [X], which directly mirrors the current requirement for [Y]"
- Include performance ratings (Exceptional, Very Good, Satisfactory) and CPARS references where available
- Organize by relevance to the current opportunity, most relevant first
- If past performance records are limited, emphasize transferable skills with specific evidence and measurable outcomes
""",
    "pricing_summary": """
SECTION-SPECIFIC SCORING GUIDANCE (Pricing Summary):
- Name the specific pricing methodology (e.g., "bottom-up engineering estimate", "parametric modeling using SEER-SEM")
- Reference specific labor categories from the relevant SCA/WD or GSA Schedule
- Describe cost control mechanisms with measurable thresholds (e.g., "variance analysis triggered at 5% deviation")
- Explain your basis of estimate approach with enough specificity to demonstrate realism
- Address price reasonableness and how your approach delivers best value to the government
""",
}


# --- Section-specific prompt templates ---

SECTION_PROMPTS: dict[str, dict[str, str]] = {
    "executive_summary": {
        "system": "You are a senior government proposal writer specializing in executive summaries for federal contracts. Write compelling, specific content that demonstrates clear understanding of the requirement and positions the offeror as the best choice.",
        "instruction": """Write a professional executive summary for this government contract proposal.

The executive summary must:
1. Open with a clear statement of understanding of the requirement
2. Reference the solicitation details (number, NAICS, deadline, set-aside if applicable)
3. Outline a high-level technical approach tailored to the specific requirements
4. Highlight key differentiators and strategic advantages the company brings
5. Reference relevant past performance that demonstrates capability
6. Close with a strong commitment statement

Use markdown headers (##, ###) for structure. Keep it professional, specific to the opportunity, and approximately 300-500 words. Do not include a title header — start with the content directly.""",
    },
    "technical_approach": {
        "system": "You are a senior government proposal writer specializing in technical volumes for federal contracts. Write detailed, specific technical approaches that demonstrate deep understanding and innovative solutions.",
        "instruction": """Write a detailed technical approach section for this government contract proposal.

The technical approach must:
1. Demonstrate thorough understanding of the technical requirements
2. Present a clear methodology with specific tools, technologies, and processes
3. Include a phased approach or work breakdown structure where applicable
4. Address quality control and risk mitigation strategies
5. Reference the company's relevant technical capabilities and past experience
6. Show innovation while maintaining compliance with requirements
7. Include specific deliverables and milestones

Use markdown headers (##, ###) for structure. Be specific — avoid generic boilerplate. Reference actual methodologies, tools, and frameworks relevant to this NAICS code and work area. Approximately 800-1200 words.""",
    },
    "management_approach": {
        "system": "You are a senior government proposal writer specializing in management volumes for federal contracts. Write comprehensive management approaches that demonstrate organizational capability and proven processes.",
        "instruction": """Write a management approach section for this government contract proposal.

The management approach must:
1. Describe the organizational structure and key personnel roles
2. Outline the staffing plan and transition approach
3. Detail the quality assurance and quality control processes
4. Present the risk management framework
5. Describe the communication plan with the government client
6. Address subcontractor management if applicable
7. Include performance measurement and continuous improvement processes

Use markdown headers (##, ###) for structure. Be specific about management methodologies (e.g., PMI, ITIL, Agile, CMMI). Approximately 600-1000 words.""",
    },
    "past_performance": {
        "system": "You are a senior government proposal writer specializing in past performance volumes. Write compelling past performance narratives that demonstrate relevance, quality, and reliability.",
        "instruction": """Write a past performance section for this government contract proposal.

Using the company's past performance records provided in the organization context, write a narrative that:
1. Presents each relevant contract with proper formatting (contract name, agency, number, value, period of performance)
2. Describes the scope of work performed and its relevance to the current opportunity
3. Highlights successful outcomes, performance ratings, and lessons learned
4. Draws clear connections between past work and the current requirement
5. Demonstrates the company's track record of on-time, on-budget delivery

If no past performance records are available, write a general capability statement explaining the company's qualifications and readiness. Use markdown headers (##, ###) for structure. Approximately 500-800 words.""",
    },
    "pricing_summary": {
        "system": "You are a senior government proposal writer specializing in cost/price volumes for federal contracts. Write pricing narratives that demonstrate value without revealing specific dollar amounts.",
        "instruction": """Write a pricing summary section for this government contract proposal.

The pricing summary must:
1. Describe the cost/pricing methodology and basis of estimate
2. Explain the value proposition and cost efficiency approach
3. Outline the pricing structure (e.g., FFP, T&M, CPFF) appropriate for this work
4. Address cost control and containment strategies
5. Highlight any cost advantages or efficiencies the company can offer
6. Reference industry-standard labor categories if applicable

Do NOT include specific dollar amounts or hourly rates — this is a narrative summary of the pricing approach. Use markdown headers (##, ###) for structure. Approximately 400-600 words.""",
    },
}


def _build_opportunity_details(**kwargs: Optional[str | float]) -> str:
    """Format opportunity fields into a details string."""
    labels = {
        "agency": "Agency",
        "solicitation_number": "Solicitation Number",
        "naics_code": "NAICS Code",
        "response_deadline": "Response Deadline",
        "set_aside_type": "Set-Aside Type",
    }
    lines: list[str] = []
    for key, label in labels.items():
        val = kwargs.get(key)
        if val:
            lines.append(f"{label}: {val}")
    est = kwargs.get("estimated_value")
    if est:
        lines.append(f"Estimated Value: ${est:,.0f}")
    return "\n".join(lines) if lines else "No additional details available."


def _build_section_prompt(
    prompts: dict[str, str],
    section_type: str,
    title: str,
    description: Optional[str],
    opportunity_details: str,
    org_context: Optional[str],
) -> str:
    """Assemble the user prompt for a section generation call."""
    guidance = SECTION_SCORING_GUIDANCE.get(section_type, "")
    desc_text = description or "No description provided."

    prompt = (
        f"{prompts['instruction']}\n{SCORING_AWARENESS_BLOCK}\n{guidance}\n\n"
        f"Opportunity Title: {title}\n\n"
        f"Opportunity Description:\n{desc_text}\n\n"
        f"Opportunity Details:\n{opportunity_details}"
    )
    if org_context:
        prompt += f"\n\nCompany Information:\n{org_context}"
    return prompt


async def generate_proposal_section(
    section_type: str,
    title: str,
    description: Optional[str] = None,
    agency: Optional[str] = None,
    solicitation_number: Optional[str] = None,
    naics_code: Optional[str] = None,
    response_deadline: Optional[str] = None,
    set_aside_type: Optional[str] = None,
    estimated_value: Optional[float] = None,
    org_context: Optional[str] = None,
) -> Optional[str]:
    """Generate a single proposal section using Claude."""
    client = _get_client()
    if not client:
        logger.info("Anthropic API key not configured, skipping AI generation")
        return None

    prompts = SECTION_PROMPTS.get(section_type)
    if not prompts:
        logger.warning(f"Unknown section type: {section_type}")
        return None

    opp_details = _build_opportunity_details(
        agency=agency, solicitation_number=solicitation_number,
        naics_code=naics_code, response_deadline=response_deadline,
        set_aside_type=set_aside_type, estimated_value=estimated_value,
    )
    user_prompt = _build_section_prompt(
        prompts, section_type, title, description, opp_details, org_context,
    )

    try:
        logger.info("Calling Claude for section: %s", section_type)
        message = await client.messages.create(
            model=settings.anthropic_model,
            max_tokens=4096,
            messages=[{"role": "user", "content": user_prompt}],
            system=prompts["system"],
        )
        result_text = message.content[0].text
        logger.info("Claude returned %d chars for %s", len(result_text), section_type)
        return result_text
    except anthropic.AuthenticationError:
        logger.error("Invalid Anthropic API key")
        return None
    except anthropic.RateLimitError:
        logger.warning("Anthropic rate limit reached")
        return None
    except Exception as e:
        logger.error("Error generating %s: %s", section_type, e)
        return None


async def generate_all_sections(
    title: str,
    description: Optional[str] = None,
    agency: Optional[str] = None,
    solicitation_number: Optional[str] = None,
    naics_code: Optional[str] = None,
    response_deadline: Optional[str] = None,
    set_aside_type: Optional[str] = None,
    estimated_value: Optional[float] = None,
    org_context: Optional[str] = None,
    sections: Optional[list[str]] = None,
) -> dict[str, Optional[str]]:
    """Generate multiple proposal sections.

    Args:
        sections: List of section types to generate. If None, generates all 5.

    Returns:
        Dict mapping section type to generated content (or None if failed).
    """
    all_sections = [
        "executive_summary", "technical_approach", "management_approach",
        "past_performance", "pricing_summary",
    ]
    target_sections = sections or all_sections

    results: dict[str, Optional[str]] = {}
    for section in target_sections:
        if section not in all_sections:
            continue
        results[section] = await generate_proposal_section(
            section_type=section,
            title=title,
            description=description,
            agency=agency,
            solicitation_number=solicitation_number,
            naics_code=naics_code,
            response_deadline=response_deadline,
            set_aside_type=set_aside_type,
            estimated_value=estimated_value,
            org_context=org_context,
        )

    return results


async def improve_proposal_section(
    section_type: str,
    current_content: str,
    score_feedback: list[dict],
    title: str,
    description: Optional[str] = None,
    agency: Optional[str] = None,
    solicitation_number: Optional[str] = None,
    naics_code: Optional[str] = None,
    org_context: Optional[str] = None,
) -> Optional[str]:
    """Regenerate a proposal section using current score feedback to target 95+.

    Args:
        section_type: One of the 5 section types.
        current_content: The existing section text.
        score_feedback: List of dicts with keys: factor_type, raw_score,
            evidence_summary, improvement_suggestions.
        title: Proposal/opportunity title.
        description: Proposal/opportunity description.
        agency: Contracting agency.
        solicitation_number: Solicitation number.
        naics_code: NAICS code.
        org_context: Organization context string.

    Returns:
        Improved section content, or None on failure.
    """
    client = _get_client()
    if not client:
        logger.info("Anthropic API key not configured, skipping AI improvement")
        return None

    prompts = SECTION_PROMPTS.get(section_type)
    if not prompts:
        logger.warning(f"Unknown section type for improvement: {section_type}")
        return None

    # Build score feedback block
    feedback_parts: list[str] = []
    for fb in score_feedback:
        factor = fb.get("factor_type", "unknown")
        raw = fb.get("raw_score", "?")
        evidence = fb.get("evidence_summary", "")
        feedback_parts.append(f"- **{factor}**: {raw}/100 — {evidence}")

        suggestions = fb.get("improvement_suggestions")
        if isinstance(suggestions, list):
            for s in suggestions:
                action = s.get("action", "")
                details = s.get("details", "")
                if action:
                    feedback_parts.append(f"  - Action: {action} — {details}")
        elif isinstance(suggestions, dict) and suggestions.get("items"):
            for s in suggestions["items"]:
                action = s.get("action", "")
                details = s.get("details", "")
                if action:
                    feedback_parts.append(f"  - Action: {action} — {details}")

    feedback_block = "\n".join(feedback_parts) if feedback_parts else "No specific feedback available."

    guidance = SECTION_SCORING_GUIDANCE.get(section_type, "")

    user_prompt = (
        f"You are improving an existing proposal section. Your goal is to rewrite "
        f"it so it scores 95+ on ALL four scoring factors.\n\n"
        f"## Current Score Feedback\n{feedback_block}\n\n"
        f"## Instructions\n"
        f"Rewrite this section to score 95+ on ALL factors. Keep what works, fix what doesn't. "
        f"Include ALL content — produce the complete rewritten section, not just changes.\n\n"
        f"{SCORING_AWARENESS_BLOCK}\n{guidance}\n\n"
        f"## Proposal Context\n"
        f"Title: {title}\n"
        f"Description: {description or 'N/A'}\n"
        f"Agency: {agency or 'N/A'}\n"
        f"Solicitation: {solicitation_number or 'N/A'}\n"
        f"NAICS: {naics_code or 'N/A'}\n"
    )
    if org_context:
        user_prompt += f"\n## Company Information\n{org_context}\n"

    user_prompt += f"\n## Current Section Content\n{current_content}\n"

    try:
        logger.info("Calling Claude to improve section: %s", section_type)
        message = await client.messages.create(
            model=settings.anthropic_model,
            max_tokens=4096,
            messages=[{"role": "user", "content": user_prompt}],
            system=prompts["system"],
        )
        result_text = message.content[0].text
        logger.info("Claude returned %d chars for improved %s", len(result_text), section_type)
        return result_text
    except anthropic.AuthenticationError:
        logger.error("Invalid Anthropic API key")
        return None
    except anthropic.RateLimitError:
        logger.warning("Anthropic rate limit reached")
        return None
    except Exception as e:
        logger.error("Error improving %s: %s", section_type, e)
        return None


# Keep backward-compatible standalone function
async def generate_executive_summary(
    title: str,
    agency: Optional[str] = None,
    description: Optional[str] = None,
    solicitation_number: Optional[str] = None,
    naics_code: Optional[str] = None,
    response_deadline: Optional[str] = None,
    set_aside_type: Optional[str] = None,
    estimated_value: Optional[float] = None,
) -> Optional[str]:
    """Generate an executive summary for a proposal using Claude.

    Returns None if the API key is not configured or the call fails.
    """
    return await generate_proposal_section(
        section_type="executive_summary",
        title=title,
        description=description,
        agency=agency,
        solicitation_number=solicitation_number,
        naics_code=naics_code,
        response_deadline=response_deadline,
        set_aside_type=set_aside_type,
        estimated_value=estimated_value,
    )
