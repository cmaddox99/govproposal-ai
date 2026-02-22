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
    """Generate a single proposal section using Claude.

    Returns None if API key is not configured or call fails.
    """
    client = _get_client()
    if not client:
        logger.info("Anthropic API key not configured, skipping AI generation")
        return None

    prompts = SECTION_PROMPTS.get(section_type)
    if not prompts:
        logger.warning(f"Unknown section type: {section_type}")
        return None

    # Build opportunity context
    details = []
    if agency:
        details.append(f"Agency: {agency}")
    if solicitation_number:
        details.append(f"Solicitation Number: {solicitation_number}")
    if naics_code:
        details.append(f"NAICS Code: {naics_code}")
    if response_deadline:
        details.append(f"Response Deadline: {response_deadline}")
    if set_aside_type:
        details.append(f"Set-Aside Type: {set_aside_type}")
    if estimated_value:
        details.append(f"Estimated Value: ${estimated_value:,.0f}")

    opportunity_details = "\n".join(details) if details else "No additional details available."
    description_text = description or "No description provided."

    user_prompt = f"""{prompts['instruction']}

Opportunity Title: {title}

Opportunity Description:
{description_text}

Opportunity Details:
{opportunity_details}"""

    if org_context:
        user_prompt += f"""

Company Information:
{org_context}"""

    try:
        print(f"[AI] Calling Claude for section: {section_type}, model: {settings.anthropic_model}")
        message = await client.messages.create(
            model=settings.anthropic_model,
            max_tokens=4096,
            messages=[
                {"role": "user", "content": user_prompt}
            ],
            system=prompts["system"],
        )

        result_text = message.content[0].text
        print(f"[AI] Claude returned {len(result_text)} chars for {section_type}")
        return result_text

    except anthropic.AuthenticationError as e:
        print(f"[AI] ERROR: Invalid Anthropic API key: {e}")
        return None
    except anthropic.RateLimitError as e:
        print(f"[AI] ERROR: Anthropic rate limit reached: {e}")
        return None
    except Exception as e:
        print(f"[AI] ERROR generating {section_type}: {type(e).__name__}: {e}")
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
