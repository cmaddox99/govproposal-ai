"""Extract structured opportunity fields from an uploaded RFP / solicitation document.

Mirrors the past-performance extraction flow: read the file, convert to text
based on content type, ask Claude to map it to OpportunityExtractedFields.

The extraction never persists anything — the caller decides whether to create
an opportunity. The source file remains in storage either way.
"""

from __future__ import annotations

import json
import logging
from typing import Any, Optional

import anthropic

from govproposal.config import settings
from govproposal.identity.past_performance_extraction import extract_text

logger = logging.getLogger(__name__)

MAX_EXTRACT_CHARS = 30_000


EXTRACTION_SYSTEM_PROMPT = """You extract structured fields from government contracting solicitation documents (RFPs, RFIs, RFQs, sources sought, etc.) for a proposal-management platform.

You receive the plain text of a solicitation or related document, and you produce a JSON object matching this schema:

{
  "title": string,                       // required — the opportunity title (e.g. "Cybersecurity Operations Support Services")
  "solicitation_number": string | null,  // e.g. "W912DY-26-R-0001"
  "agency": string | null,               // contracting agency (e.g. "Department of Defense")
  "department": string | null,           // parent department if distinct from agency
  "office": string | null,               // contracting office
  "naics_code": string | null,           // 6-digit NAICS code (digits only)
  "naics_description": string | null,
  "set_aside_type": string | null,       // canonical code only: one of "sba", "wosb", "edwosb", "sdvosb", "hubzone", "8a", "sbsa", or null for full-and-open
  "notice_type": string | null,          // one of "solicitation", "presolicitation", "combined_synopsis", "sources_sought", "special_notice", or null
  "response_deadline": string | null,    // ISO 8601 datetime "YYYY-MM-DDTHH:MM:SS" (use 17:00:00 if only a date is given)
  "posted_date": string | null,          // ISO 8601 date "YYYY-MM-DD"
  "estimated_value": number | null,      // USD, number only, no currency symbol. If a ceiling is given, use it; if a range, use the maximum.
  "place_of_performance_city": string | null,
  "place_of_performance_state": string | null,
  "primary_contact_name": string | null, // contracting officer or POC
  "primary_contact_email": string | null,
  "primary_contact_phone": string | null,
  "description": string | null,          // 3-6 sentence summary of the scope of work
  "sam_url": string | null,              // direct URL to SAM.gov listing if present
  "confidence": {                        // 0.0 - 1.0 per field
    "title": number, "solicitation_number": number, "agency": number,
    "naics_code": number, "set_aside_type": number, "response_deadline": number,
    "estimated_value": number, "primary_contact_name": number, "description": number
  }
}

Rules:
- Output ONLY the JSON object. No prose, no markdown fences, no commentary.
- If a field cannot be found, set it to null and confidence to 0.
- title is required — if no clear title, build one from agency + scope.
- For set_aside_type, normalize to the canonical codes above. "Total Small Business Set-Aside" -> "sba", "WOSB" -> "wosb", "8(a)" -> "8a", etc.
- For naics_code, return just the 6 digits, no description.
"""


async def extract_opportunity(text: str) -> Optional[dict[str, Any]]:
    """Run Claude over solicitation text and return the structured fields."""
    if not text or not text.strip():
        return None
    if not settings.anthropic_api_key:
        logger.info("Anthropic key not configured; skipping opportunity extraction")
        return None

    snippet = text[:MAX_EXTRACT_CHARS]
    client = anthropic.AsyncAnthropic(api_key=settings.anthropic_api_key)

    try:
        message = await client.messages.create(
            model=settings.anthropic_model,
            max_tokens=2048,
            system=EXTRACTION_SYSTEM_PROMPT,
            messages=[
                {
                    "role": "user",
                    "content": (
                        "Extract opportunity fields from this solicitation document. "
                        "Return only the JSON object as specified.\n\n"
                        f"<document>\n{snippet}\n</document>"
                    ),
                }
            ],
        )
    except anthropic.AuthenticationError:
        logger.error("Invalid Anthropic API key for opportunity extraction")
        return None
    except anthropic.RateLimitError:
        logger.warning("Anthropic rate limit reached during extraction")
        return None
    except Exception as exc:
        logger.error("Claude opportunity extraction error: %s", exc)
        return None

    try:
        raw = message.content[0].text
        if "```json" in raw:
            raw = raw.split("```json", 1)[1].split("```", 1)[0]
        elif "```" in raw:
            raw = raw.split("```", 1)[1].split("```", 1)[0]
        return json.loads(raw.strip())
    except (json.JSONDecodeError, IndexError, AttributeError) as exc:
        logger.warning("Could not parse opportunity extraction JSON: %s", exc)
        return None


# Re-export for symmetry with past_performance_extraction
__all__ = ["extract_opportunity", "extract_text"]
