"""GSA eBuy / GSA Schedule integration service.

GSA eBuy is a closed Angular SPA with no public API. However, GSA Schedule
solicitations and RFQs that are posted publicly appear on SAM.gov. This
service queries SAM.gov for GSA-sourced opportunities (agency = GSA,
notice types including solicitations and combined synopses) and tags them
with source="gsa_ebuy" to distinguish them from general SAM.gov results.
"""

import logging
import httpx
from datetime import datetime, timedelta, timezone
from typing import Optional, List, Dict, Any

from govproposal.config import settings

logger = logging.getLogger(__name__)


class EBuyOpenService:
    """Service for fetching GSA Schedule / eBuy-originated opportunities via SAM.gov."""

    BASE_URL = "https://api.sam.gov/opportunities/v2"

    # GSA-related agencies and subtiers to filter on
    GSA_AGENCIES = [
        "General Services Administration",
        "GSA",
        "FEDERAL ACQUISITION SERVICE",
        "PUBLIC BUILDINGS SERVICE",
    ]

    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or settings.sam_api_key

    async def search_opportunities(
        self,
        keywords: Optional[str] = None,
        limit: int = 100,
    ) -> List[Dict[str, Any]]:
        """Search SAM.gov for GSA-sourced opportunities.

        Fetches solicitations and combined synopses from GSA agencies
        posted in the last 90 days.
        """
        if not self.api_key:
            return []

        now = datetime.now(timezone.utc)
        posted_from = now - timedelta(days=90)

        params: Dict[str, Any] = {
            "api_key": self.api_key,
            "limit": limit,
            "offset": 0,
            "postedFrom": posted_from.strftime("%m/%d/%Y"),
            "postedTo": now.strftime("%m/%d/%Y"),
            # Filter for solicitation types (where RFQs appear)
            "ptype": "k,o,p",  # combined synopsis, solicitation, presolicitation
        }

        if keywords:
            params["title"] = keywords

        all_opportunities: List[Dict[str, Any]] = []

        async with httpx.AsyncClient(timeout=30.0) as client:
            try:
                response = await client.get(
                    f"{self.BASE_URL}/search",
                    params=params,
                )
                response.raise_for_status()
                data = response.json()

                for opp in data.get("opportunitiesData", []):
                    # Filter to GSA-sourced opportunities
                    agency = (opp.get("department") or "").upper()
                    subtier = (opp.get("subtierAgency") or opp.get("agency") or "").upper()

                    is_gsa = any(
                        gsa.upper() in agency or gsa.upper() in subtier
                        for gsa in self.GSA_AGENCIES
                    )

                    if is_gsa:
                        parsed = self.parse_opportunity(opp)
                        if parsed:
                            all_opportunities.append(parsed)

            except httpx.HTTPStatusError as e:
                body = e.response.text
                logger.warning("SAM.gov API error for GSA eBuy sync: %s — %s", e.response.status_code, body)
                if "exceeded your quota" in body.lower() or "throttled" in body.lower():
                    raise RuntimeError(
                        "SAM.gov API daily quota exceeded. The quota resets at midnight UTC. Please try again later."
                    )
            except Exception as e:
                logger.warning("GSA eBuy sync failed: %s", str(e))

        return all_opportunities

    def parse_opportunity(self, data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Parse SAM.gov opportunity data, tagged as gsa_ebuy source."""
        notice_id = data.get("noticeId", "")
        title = data.get("title", "")

        if not notice_id or not title:
            return None

        return {
            "notice_id": notice_id,
            "solicitation_number": data.get("solicitationNumber"),
            "title": title,
            "description": data.get("description"),
            "department": data.get("department"),
            "agency": data.get("subtierAgency") or data.get("agency"),
            "office": data.get("office"),
            "notice_type": data.get("type", "").lower().replace(" ", "_"),
            "naics_code": data.get("naicsCode"),
            "naics_description": data.get("naicsDescription"),
            "psc_code": data.get("classificationCode"),
            "set_aside_type": data.get("typeOfSetAside"),
            "set_aside_description": data.get("typeOfSetAsideDescription"),
            "posted_date": self._parse_date(data.get("postedDate")),
            "response_deadline": self._parse_date(data.get("responseDeadLine")),
            "archive_date": self._parse_date(data.get("archiveDate")),
            "place_of_performance_city": data.get("placeOfPerformanceCity"),
            "place_of_performance_state": data.get("placeOfPerformanceState"),
            "place_of_performance_country": data.get("placeOfPerformanceCountry"),
            "primary_contact_name": (
                data.get("pointOfContact", [{}])[0].get("fullName")
                if data.get("pointOfContact") else None
            ),
            "primary_contact_email": (
                data.get("pointOfContact", [{}])[0].get("email")
                if data.get("pointOfContact") else None
            ),
            "primary_contact_phone": (
                data.get("pointOfContact", [{}])[0].get("phone")
                if data.get("pointOfContact") else None
            ),
            "sam_url": data.get("uiLink"),
            "raw_data": data,
            "source": "gsa_ebuy",
        }

    def _parse_date(self, date_str: Optional[str]) -> Optional[datetime]:
        """Parse date string from SAM.gov API."""
        if not date_str:
            return None
        try:
            for fmt in ["%Y-%m-%d", "%m/%d/%Y", "%Y-%m-%dT%H:%M:%S"]:
                try:
                    return datetime.strptime(date_str[:10], fmt[:10]).replace(
                        tzinfo=timezone.utc
                    )
                except ValueError:
                    continue
            return None
        except Exception:
            return None
