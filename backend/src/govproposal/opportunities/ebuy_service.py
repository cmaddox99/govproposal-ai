"""GSA eBuy Open integration service."""

import httpx
from datetime import datetime, timezone
from typing import Optional, Dict, Any

try:
    from bs4 import BeautifulSoup

    HAS_BS4 = True
except ImportError:
    HAS_BS4 = False


class EBuyOpenService:
    """Service for fetching solicitations from GSA eBuy Open."""

    EBUY_OPEN_URL = "https://www.ebuy.gsa.gov/ebuyopen"
    # Known eBuy Open API endpoints (Angular SPA backend)
    EBUY_API_BASE = "https://www.ebuy.gsa.gov/ebuyopen/api"

    async def search_opportunities(
        self,
        keywords: Optional[str] = None,
        limit: int = 50,
    ) -> list[Dict[str, Any]]:
        """Search for open RFQs on GSA eBuy Open.

        Attempts the underlying API first. Falls back to HTML scraping
        if the API is unavailable. Note: eBuy Open is an Angular SPA,
        so full scraping may require Playwright in the future.
        """
        opportunities: list[Dict[str, Any]] = []

        async with httpx.AsyncClient(timeout=30.0, follow_redirects=True) as client:
            # Attempt 1: Try the eBuy Open API directly
            try:
                opportunities = await self._fetch_from_api(client, keywords, limit)
                if opportunities:
                    return opportunities
            except Exception:
                pass

            # Attempt 2: Fall back to scraping the HTML page
            try:
                opportunities = await self._fetch_from_html(client, keywords, limit)
            except Exception:
                pass

        return opportunities

    async def _fetch_from_api(
        self,
        client: httpx.AsyncClient,
        keywords: Optional[str],
        limit: int,
    ) -> list[Dict[str, Any]]:
        """Try fetching from eBuy Open's backend API."""
        params: Dict[str, Any] = {
            "status": "open",
            "limit": limit,
        }
        if keywords:
            params["keywords"] = keywords

        response = await client.get(
            f"{self.EBUY_API_BASE}/rfqs",
            params=params,
            headers={
                "Accept": "application/json",
                "User-Agent": "GovProposal-AI/1.0",
            },
        )
        response.raise_for_status()
        data = response.json()

        results = []
        items = data if isinstance(data, list) else data.get("results", data.get("rfqs", []))
        for item in items[:limit]:
            parsed = self.parse_opportunity(item)
            if parsed:
                results.append(parsed)
        return results

    async def _fetch_from_html(
        self,
        client: httpx.AsyncClient,
        keywords: Optional[str],
        limit: int,
    ) -> list[Dict[str, Any]]:
        """Fall back to scraping the eBuy Open HTML page.

        Note: Since eBuy Open is an Angular SPA, this may only capture
        server-rendered content. For full support, Playwright integration
        may be needed in the future.
        """
        if not HAS_BS4:
            return []

        url = self.EBUY_OPEN_URL
        if keywords:
            url += f"?keywords={keywords}"

        response = await client.get(
            url,
            headers={
                "User-Agent": "GovProposal-AI/1.0",
                "Accept": "text/html",
            },
        )
        response.raise_for_status()

        soup = BeautifulSoup(response.text, "html.parser")
        results = []

        # Look for RFQ listing elements — CSS selectors may need
        # refinement as the eBuy Open UI evolves
        rfq_rows = soup.select("table tbody tr, .rfq-item, .rfq-row, [class*='rfq']")
        for row in rfq_rows[:limit]:
            try:
                parsed = self._parse_html_row(row)
                if parsed:
                    results.append(parsed)
            except Exception:
                continue

        return results

    def _parse_html_row(self, row: Any) -> Optional[Dict[str, Any]]:
        """Parse a single HTML row/element into opportunity format."""
        cells = row.find_all("td") if hasattr(row, "find_all") else []
        if len(cells) < 3:
            # Try extracting from any element with text content
            text = row.get_text(strip=True) if hasattr(row, "get_text") else ""
            if not text:
                return None
            return {
                "notice_id": f"ebuy-{hash(text) & 0xFFFFFFFF:08x}",
                "title": text[:500],
                "description": None,
                "department": "General Services Administration",
                "agency": "GSA",
                "office": None,
                "notice_type": "solicitation",
                "naics_code": None,
                "naics_description": None,
                "psc_code": None,
                "set_aside_type": None,
                "set_aside_description": None,
                "posted_date": None,
                "response_deadline": None,
                "archive_date": None,
                "place_of_performance_city": None,
                "place_of_performance_state": None,
                "place_of_performance_country": "US",
                "primary_contact_name": None,
                "primary_contact_email": None,
                "primary_contact_phone": None,
                "sam_url": self.EBUY_OPEN_URL,
                "raw_data": {"html_text": text},
                "source": "gsa_ebuy",
            }

        # Table-based layout
        title = cells[0].get_text(strip=True) if cells else ""
        rfq_number = cells[1].get_text(strip=True) if len(cells) > 1 else ""
        deadline_str = cells[2].get_text(strip=True) if len(cells) > 2 else ""

        return {
            "notice_id": f"ebuy-{rfq_number}" if rfq_number else f"ebuy-{hash(title) & 0xFFFFFFFF:08x}",
            "solicitation_number": rfq_number or None,
            "title": title[:500],
            "description": None,
            "department": "General Services Administration",
            "agency": "GSA",
            "office": None,
            "notice_type": "solicitation",
            "naics_code": None,
            "naics_description": None,
            "psc_code": None,
            "set_aside_type": None,
            "set_aside_description": None,
            "posted_date": None,
            "response_deadline": self._parse_date(deadline_str),
            "archive_date": None,
            "place_of_performance_city": None,
            "place_of_performance_state": None,
            "place_of_performance_country": "US",
            "primary_contact_name": None,
            "primary_contact_email": None,
            "primary_contact_phone": None,
            "sam_url": self.EBUY_OPEN_URL,
            "raw_data": {"rfq_number": rfq_number, "title": title},
            "source": "gsa_ebuy",
        }

    def parse_opportunity(self, data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Parse eBuy API response data into Opportunity model format."""
        rfq_id = data.get("rfqId") or data.get("id") or data.get("rfqNumber", "")
        title = data.get("title") or data.get("description") or data.get("rfqTitle", "")

        if not title:
            return None

        return {
            "notice_id": f"ebuy-{rfq_id}" if rfq_id else f"ebuy-{hash(title) & 0xFFFFFFFF:08x}",
            "solicitation_number": data.get("rfqNumber"),
            "title": title[:500],
            "description": data.get("description") or data.get("details"),
            "department": "General Services Administration",
            "agency": data.get("agency") or "GSA",
            "office": data.get("office"),
            "notice_type": "solicitation",
            "naics_code": data.get("naicsCode"),
            "naics_description": data.get("naicsDescription"),
            "psc_code": data.get("pscCode"),
            "set_aside_type": data.get("setAside"),
            "set_aside_description": data.get("setAsideDescription"),
            "posted_date": self._parse_date(data.get("openDate") or data.get("postedDate")),
            "response_deadline": self._parse_date(
                data.get("closeDate") or data.get("responseDeadline")
            ),
            "archive_date": None,
            "place_of_performance_city": data.get("city"),
            "place_of_performance_state": data.get("state"),
            "place_of_performance_country": data.get("country", "US"),
            "primary_contact_name": data.get("contactName"),
            "primary_contact_email": data.get("contactEmail"),
            "primary_contact_phone": data.get("contactPhone"),
            "sam_url": data.get("url") or self.EBUY_OPEN_URL,
            "raw_data": data,
            "source": "gsa_ebuy",
        }

    def _parse_date(self, date_str: Optional[str]) -> Optional[datetime]:
        """Parse date string from eBuy API or HTML."""
        if not date_str:
            return None
        try:
            for fmt in [
                "%Y-%m-%dT%H:%M:%S",
                "%Y-%m-%d",
                "%m/%d/%Y",
                "%m/%d/%Y %I:%M %p",
                "%b %d, %Y",
            ]:
                try:
                    return datetime.strptime(date_str.strip()[:19], fmt[:19]).replace(
                        tzinfo=timezone.utc
                    )
                except ValueError:
                    continue
            return None
        except Exception:
            return None
