"""AI service for generating proposal content using Claude."""

import logging
from typing import Optional

import anthropic

from govproposal.config import settings

logger = logging.getLogger(__name__)


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

    Returns None if the API key is not configured or the call fails,
    allowing the caller to fall back to a template.
    """
    if not settings.anthropic_api_key:
        logger.info("Anthropic API key not configured, skipping AI generation")
        return None

    # Build context about the opportunity
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

    prompt = f"""You are a senior government proposal writer. Generate a professional executive summary for a government contract proposal based on the following opportunity.

Opportunity Title: {title}

Opportunity Description:
{description_text}

Opportunity Details:
{opportunity_details}

Write a compelling executive summary in markdown format that:
1. Opens with a clear statement of understanding of the requirement
2. Summarizes the opportunity details (solicitation number, NAICS, deadline)
3. Outlines a high-level technical approach tailored to the specific requirements
4. Highlights key differentiators relevant to this specific contract
5. Closes with a strong commitment statement

Use markdown headers (##, ###) for structure. Keep it professional, specific to the opportunity (avoid generic boilerplate), and approximately 300-500 words. Do not include a title header - start with the content directly."""

    try:
        client = anthropic.Anthropic(api_key=settings.anthropic_api_key)

        message = client.messages.create(
            model=settings.anthropic_model,
            max_tokens=1024,
            messages=[
                {"role": "user", "content": prompt}
            ],
        )

        return message.content[0].text

    except anthropic.AuthenticationError:
        logger.error("Invalid Anthropic API key")
        return None
    except anthropic.RateLimitError:
        logger.warning("Anthropic rate limit reached, falling back to template")
        return None
    except Exception as e:
        logger.error(f"Claude API error: {e}")
        return None
