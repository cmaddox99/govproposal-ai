"""Texas SmartBuy (ESBD) integration service.

Texas SmartBuy is the state of Texas procurement portal at txsmartbuy.gov.
The Electronic State Business Daily (ESBD) at /esbd lists current state and
local government solicitations. There's no public API, so this service
scrapes the server-rendered HTML pages.

Pages of interest:
- /esbd?page=N — paginated list, each row links to /esbd/{solicitation_id}
- /esbd/{solicitation_id} — detail page with full fields

For SLED opportunities, we set:
- source = "txsmartbuy"
- market = "sled"
- notice_id = f"txsmartbuy-{solicitation_id}"
- notice_type = "solicitation" (default; ESBD doesn't expose a federal-style notice type)

NIGP / class codes are stored verbatim in naics_code (the first one only).
NIGP codes are 5-digit Texas commodity codes, not NAICS, but the column is
just a String(10) and the UI labels it as "NAICS / commodity code" based on
the opportunity's market.
"""

from __future__ import annotations

import asyncio
import logging
import re
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Any, Optional

import httpx
from bs4 import BeautifulSoup

logger = logging.getLogger(__name__)


BASE_URL = "https://www.txsmartbuy.gov"
USER_AGENT = "GovProposalAI/0.1 (+https://github.com/cmaddox99/govproposal-ai)"
LIST_FETCH_TIMEOUT = 30.0
DETAIL_FETCH_TIMEOUT = 20.0
# Be polite — small delay between detail fetches
INTER_REQUEST_DELAY_SECONDS = 0.25


@dataclass
class _ListEntry:
    solicitation_id: str
    url: str


def _abs_url(href: str) -> str:
    if not href:
        return ""
    if href.startswith("http"):
        return href
    if href.startswith("/"):
        return f"{BASE_URL}{href}"
    return f"{BASE_URL}/{href}"


def _clean(text: Optional[str]) -> str:
    if text is None:
        return ""
    return re.sub(r"\s+", " ", text).strip()


def _parse_date(text: str) -> Optional[datetime]:
    """Parse common ESBD date formats. Returns timezone-aware UTC."""
    if not text:
        return None
    text = _clean(text)
    formats = [
        "%B %d, %Y at %I:%M %p",  # April 22, 2026 at 11:30 PM
        "%B %d, %Y %I:%M %p",     # April 22, 2026 11:30 PM
        "%B %d, %Y",              # April 22, 2026
        "%m/%d/%Y %I:%M %p",
        "%m/%d/%Y",
    ]
    for fmt in formats:
        try:
            dt = datetime.strptime(text, fmt)
            return dt.replace(tzinfo=timezone.utc)
        except ValueError:
            continue
    return None


def _label_value(soup: BeautifulSoup, label_re: re.Pattern) -> str:
    """Find a <dt>/<th>/<label> matching label_re and return the adjacent value text.

    ESBD detail pages tend to use either definition-list (dt/dd) or table
    rows. We try both, prefer <dd> after a <dt>, else next-sibling <td>.
    """
    # dt -> dd
    for dt in soup.find_all(["dt", "th", "label", "strong", "b"]):
        text = _clean(dt.get_text())
        if label_re.search(text):
            sibling = dt.find_next(["dd", "td", "span", "p"])
            if sibling is not None:
                value = _clean(sibling.get_text())
                if value:
                    return value
    return ""


def _extract_list_entries(html: str) -> list[_ListEntry]:
    """Pull /esbd/{id} links out of a list page."""
    soup = BeautifulSoup(html, "html.parser")
    seen: set[str] = set()
    entries: list[_ListEntry] = []
    # Anchors with href="/esbd/something"
    pattern = re.compile(r"^/esbd/([^/?#\s]+)$")
    for a in soup.find_all("a", href=True):
        match = pattern.match(a["href"])
        if not match:
            continue
        solicitation_id = match.group(1)
        if solicitation_id in seen:
            continue
        seen.add(solicitation_id)
        entries.append(_ListEntry(solicitation_id=solicitation_id, url=_abs_url(a["href"])))
    return entries


def _parse_detail(solicitation_id: str, html: str, detail_url: str) -> Optional[dict[str, Any]]:
    """Parse a /esbd/{id} detail page into an Opportunity-shaped dict."""
    soup = BeautifulSoup(html, "html.parser")

    # Title — try h1 / h2, fall back to a "Title:" label
    title = ""
    for tag in ["h1", "h2"]:
        h = soup.find(tag)
        if h:
            title = _clean(h.get_text())
            if title:
                break
    if not title:
        title = _label_value(soup, re.compile(r"^title", re.I))

    if not title:
        # Without a title we don't store the record
        logger.info("txsmartbuy: skipping %s — no title parsed", solicitation_id)
        return None

    agency = _label_value(soup, re.compile(r"agency", re.I))
    posted = _label_value(soup, re.compile(r"posted\s*date", re.I))
    deadline = _label_value(soup, re.compile(r"response\s*deadline|due\s*date|closing", re.I))
    contact_name = _label_value(soup, re.compile(r"contact\s*name", re.I))
    contact_phone = _label_value(soup, re.compile(r"contact\s*phone|phone", re.I))
    contact_email = _label_value(soup, re.compile(r"contact\s*email|email", re.I))
    description = _label_value(soup, re.compile(r"description|scope", re.I))
    nigp_text = _label_value(soup, re.compile(r"nigp|class\s*code|commodity\s*code", re.I))

    # First NIGP code (5 digits)
    nigp_code: Optional[str] = None
    if nigp_text:
        match = re.search(r"\b(\d{5})\b", nigp_text)
        if match:
            nigp_code = match.group(1)

    return {
        "notice_id": f"txsmartbuy-{solicitation_id}",
        "solicitation_number": solicitation_id,
        "title": title[:500],
        "description": description[:5000] if description else None,
        "agency": agency or None,
        "notice_type": "solicitation",
        "naics_code": nigp_code,
        "naics_description": nigp_text or None,
        "posted_date": _parse_date(posted),
        "response_deadline": _parse_date(deadline),
        "primary_contact_name": contact_name or None,
        "primary_contact_email": contact_email or None,
        "primary_contact_phone": contact_phone or None,
        "sam_url": detail_url,
        "source": "txsmartbuy",
        "market": "sled",
        "is_active": True,
        "last_synced_at": datetime.now(timezone.utc),
    }


class TxSmartBuyService:
    """Service for fetching Texas SmartBuy ESBD solicitations."""

    BASE_URL = BASE_URL

    async def search_opportunities(
        self,
        pages: int = 1,
        keywords: Optional[str] = None,
        per_page_limit: Optional[int] = None,
    ) -> list[dict[str, Any]]:
        """Fetch ESBD list pages and return parsed opportunity dicts.

        pages: how many list pages to walk (each page has ~25 results).
               Capped at 5 to keep sync time bounded.
        keywords: optional substring matched against title (post-filter, the
                  ESBD search form requires a different endpoint).
        per_page_limit: stop early if we have this many results.
        """
        pages = max(1, min(pages, 5))
        results: list[dict[str, Any]] = []
        seen_ids: set[str] = set()

        async with httpx.AsyncClient(
            timeout=LIST_FETCH_TIMEOUT,
            headers={"User-Agent": USER_AGENT},
            follow_redirects=True,
        ) as client:
            for page in range(1, pages + 1):
                list_url = f"{BASE_URL}/esbd?page={page}"
                try:
                    resp = await client.get(list_url)
                    resp.raise_for_status()
                except httpx.HTTPError as exc:
                    logger.warning("txsmartbuy list fetch failed (page %d): %s", page, exc)
                    continue

                entries = _extract_list_entries(resp.text)
                if not entries:
                    logger.info("txsmartbuy: page %d returned no entries", page)
                    break

                for entry in entries:
                    if entry.solicitation_id in seen_ids:
                        continue
                    seen_ids.add(entry.solicitation_id)

                    try:
                        detail_resp = await client.get(
                            entry.url, timeout=DETAIL_FETCH_TIMEOUT
                        )
                        detail_resp.raise_for_status()
                    except httpx.HTTPError as exc:
                        logger.warning(
                            "txsmartbuy detail fetch failed (%s): %s",
                            entry.solicitation_id,
                            exc,
                        )
                        continue

                    parsed = _parse_detail(entry.solicitation_id, detail_resp.text, entry.url)
                    if parsed is None:
                        continue

                    if keywords:
                        haystack = f"{parsed.get('title') or ''} {parsed.get('description') or ''}".lower()
                        if keywords.lower() not in haystack:
                            await asyncio.sleep(INTER_REQUEST_DELAY_SECONDS)
                            continue

                    results.append(parsed)
                    if per_page_limit is not None and len(results) >= per_page_limit:
                        return results

                    await asyncio.sleep(INTER_REQUEST_DELAY_SECONDS)

        return results
