"""SAM.gov API integration service."""

import httpx
from datetime import datetime, timedelta, timezone
from typing import Optional, List, Dict, Any

from govproposal.config import settings


class SAMGovService:
    """Service for interacting with SAM.gov API."""

    BASE_URL = "https://api.sam.gov/opportunities/v2"

    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or settings.sam_api_key
        if not self.api_key:
            raise ValueError("SAM.gov API key is required")

    async def search_opportunities(
        self,
        naics_codes: Optional[List[str]] = None,
        keywords: Optional[str] = None,
        posted_from: Optional[datetime] = None,
        posted_to: Optional[datetime] = None,
        response_deadline_from: Optional[datetime] = None,
        response_deadline_to: Optional[datetime] = None,
        notice_type: Optional[str] = None,
        set_aside: Optional[str] = None,
        limit: int = 100,
        offset: int = 0,
    ) -> Dict[str, Any]:
        """Search for opportunities on SAM.gov."""
        now = datetime.now(timezone.utc)

        # postedFrom and postedTo are REQUIRED by the SAM.gov API
        if not posted_from:
            posted_from = now - timedelta(days=365)
        if not posted_to:
            posted_to = now

        params: Dict[str, Any] = {
            "api_key": self.api_key,
            "limit": limit,
            "offset": offset,
            "postedFrom": posted_from.strftime("%m/%d/%Y"),
            "postedTo": posted_to.strftime("%m/%d/%Y"),
        }

        if response_deadline_from:
            params["rdlfrom"] = response_deadline_from.strftime("%m/%d/%Y")
        if response_deadline_to:
            params["rdlto"] = response_deadline_to.strftime("%m/%d/%Y")

        # SAM.gov uses 'ncode' for NAICS filter (one code per request)
        # Make multiple requests if needed, or use the first code
        if naics_codes:
            params["ncode"] = naics_codes[0]

        # Add title search (SAM.gov doesn't support full-text keyword search)
        if keywords:
            params["title"] = keywords

        # Add notice type
        if notice_type:
            params["ptype"] = notice_type

        # Add set-aside
        if set_aside:
            params["typeOfSetAside"] = set_aside

        all_opportunities: List[Dict[str, Any]] = []

        async with httpx.AsyncClient(timeout=30.0) as client:
            # If multiple NAICS codes, search each one
            codes_to_search = naics_codes if naics_codes and len(naics_codes) > 1 else [None]

            for i, code in enumerate(codes_to_search):
                if code:
                    params["ncode"] = code
                elif not naics_codes:
                    params.pop("ncode", None)

                response = await client.get(
                    f"{self.BASE_URL}/search",
                    params=params,
                )
                response.raise_for_status()
                data = response.json()

                opps = data.get("opportunitiesData", [])
                all_opportunities.extend(opps)

            # Deduplicate by noticeId
            seen = set()
            unique_opps = []
            for opp in all_opportunities:
                nid = opp.get("noticeId")
                if nid and nid not in seen:
                    seen.add(nid)
                    unique_opps.append(opp)

            return {
                "totalRecords": len(unique_opps),
                "opportunitiesData": unique_opps,
            }

    async def get_opportunity(self, notice_id: str) -> Dict[str, Any]:
        """
        Get details for a specific opportunity.

        Args:
            notice_id: The SAM.gov notice ID

        Returns:
            Dictionary with opportunity details
        """
        params = {
            "api_key": self.api_key,
            "noticeid": notice_id,
        }

        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.get(
                f"{self.BASE_URL}/search",
                params=params,
            )
            response.raise_for_status()
            return response.json()

    def parse_opportunity(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Parse SAM.gov opportunity data into our model format.

        Args:
            data: Raw opportunity data from SAM.gov

        Returns:
            Dictionary formatted for our Opportunity model
        """
        # SAM.gov API response structure may vary, this is a common format
        return {
            "notice_id": data.get("noticeId", ""),
            "solicitation_number": data.get("solicitationNumber"),
            "title": data.get("title", ""),
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
            "primary_contact_name": data.get("pointOfContact", [{}])[0].get("fullName") if data.get("pointOfContact") else None,
            "primary_contact_email": data.get("pointOfContact", [{}])[0].get("email") if data.get("pointOfContact") else None,
            "primary_contact_phone": data.get("pointOfContact", [{}])[0].get("phone") if data.get("pointOfContact") else None,
            "sam_url": data.get("uiLink"),
            "raw_data": data,
        }

    def _parse_date(self, date_str: Optional[str]) -> Optional[datetime]:
        """Parse date string from SAM.gov API."""
        if not date_str:
            return None
        try:
            # SAM.gov uses various date formats
            for fmt in ["%Y-%m-%d", "%m/%d/%Y", "%Y-%m-%dT%H:%M:%S"]:
                try:
                    return datetime.strptime(date_str[:10], fmt[:10]).replace(tzinfo=timezone.utc)
                except ValueError:
                    continue
            return None
        except Exception:
            return None


# Singleton instance
_sam_service: Optional[SAMGovService] = None


def get_sam_service() -> SAMGovService:
    """Get or create SAM.gov service instance."""
    global _sam_service
    if _sam_service is None:
        _sam_service = SAMGovService()
    return _sam_service
