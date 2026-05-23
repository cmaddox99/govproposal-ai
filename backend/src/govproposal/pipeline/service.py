"""Pipeline match scoring service.

Computes a 0-100 fit score and red/yellow/green tier for an opportunity
based on the organization's NAICS codes, past performance, set-aside fit,
and value-range fit.
"""

import json
from dataclasses import dataclass, field
from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from govproposal.identity.models import Organization, OrgPastPerformance
from govproposal.opportunities.models import Opportunity


# Tier thresholds
GREEN_THRESHOLD = 75
YELLOW_THRESHOLD = 50


@dataclass
class Improvement:
    """An actionable step the user can take to lift the match score."""

    factor: str  # "naics" | "past_performance" | "set_aside" | "value_fit"
    action: str
    potential_gain: int
    effort: str  # "low" | "medium" | "high"

    def to_dict(self) -> dict:
        return {
            "factor": self.factor,
            "action": self.action,
            "potential_gain": self.potential_gain,
            "effort": self.effort,
        }


@dataclass
class MatchBreakdown:
    naics_score: int = 0
    past_performance_score: int = 0
    set_aside_score: int = 0
    value_fit_score: int = 0
    total: int = 0
    tier: str = "red"
    notes: list[str] = field(default_factory=list)
    improvements: list[Improvement] = field(default_factory=list)

    def to_json(self) -> str:
        return json.dumps(
            {
                "naics_score": self.naics_score,
                "past_performance_score": self.past_performance_score,
                "set_aside_score": self.set_aside_score,
                "value_fit_score": self.value_fit_score,
                "total": self.total,
                "tier": self.tier,
                "notes": self.notes,
                "improvements": [i.to_dict() for i in self.improvements],
                "potential_total": min(
                    100, self.total + sum(i.potential_gain for i in self.improvements)
                ),
            }
        )


def _parse_naics_list(raw) -> list[str]:
    if not raw:
        return []
    if isinstance(raw, list):
        return [str(c).strip() for c in raw if c]
    try:
        parsed = json.loads(raw) if isinstance(raw, str) else raw
        if isinstance(parsed, list):
            return [str(c).strip() for c in parsed if c]
    except (json.JSONDecodeError, TypeError):
        pass
    return []


def _set_aside_fit(
    opp_set_aside: Optional[str], org_set_asides: list[str]
) -> tuple[int, str, list[Improvement]]:
    """Score set-aside fit. Max 15."""
    if not opp_set_aside or opp_set_aside.lower() == "none":
        return 15, "No set-aside requirement (open to all)", []
    if not org_set_asides:
        return (
            5,
            "Set-aside required but org has no certifications listed",
            [
                Improvement(
                    factor="set_aside",
                    action=(
                        f"Add the {opp_set_aside.upper()} certification to your "
                        "organization profile if your business qualifies."
                    ),
                    potential_gain=10,
                    effort="medium",
                )
            ],
        )
    normalized = opp_set_aside.lower()
    for sa in org_set_asides:
        if sa.lower() == normalized:
            return 15, f"Org holds matching {sa.upper()} certification", []
    return (
        0,
        f"Set-aside {opp_set_aside.upper()} required, org lacks certification",
        [
            Improvement(
                factor="set_aside",
                action=(
                    f"This opportunity requires {opp_set_aside.upper()}. "
                    "Pursue this certification, or filter to non-set-aside work."
                ),
                potential_gain=15,
                effort="high",
            )
        ],
    )


def _value_fit(
    estimated_value: Optional[float], past_values: list[float]
) -> tuple[int, str, list[Improvement]]:
    """Score value-range fit. Max 15."""
    if not estimated_value:
        return 10, "Opportunity value unknown (neutral)", []
    if not past_values:
        return (
            5,
            "No past performance values to compare",
            [
                Improvement(
                    factor="value_fit",
                    action=(
                        "Add contract values to your past performance records so we "
                        "can judge whether this opportunity fits your delivery scale."
                    ),
                    potential_gain=10,
                    effort="low",
                )
            ],
        )
    max_past = max(past_values)
    avg_past = sum(past_values) / len(past_values)
    if estimated_value <= max_past * 1.5:
        return (
            15,
            f"Value fits within 1.5x of largest past contract (${max_past:,.0f})",
            [],
        )
    if estimated_value <= max_past * 3:
        return (
            10,
            "Value is 1.5-3x largest past contract — stretch goal",
            [
                Improvement(
                    factor="value_fit",
                    action=(
                        f"Document past work at or above ${estimated_value/2:,.0f} "
                        "(teaming or subcontract experience counts) to close the gap."
                    ),
                    potential_gain=5,
                    effort="medium",
                )
            ],
        )
    if estimated_value <= avg_past * 10:
        return (
            5,
            "Value significantly larger than typical past contracts",
            [
                Improvement(
                    factor="value_fit",
                    action=(
                        "Consider teaming with a larger prime, or pursue smaller "
                        "set-aside vehicles in this space first."
                    ),
                    potential_gain=10,
                    effort="high",
                )
            ],
        )
    return (
        0,
        "Value far exceeds prior performance scale",
        [
            Improvement(
                factor="value_fit",
                action=(
                    "Opportunity is far above your historical delivery scale. "
                    "Team with a larger prime or no-bid."
                ),
                potential_gain=15,
                effort="high",
            )
        ],
    )


def _naics_score(
    opp_naics: Optional[str], org_naics: list[str]
) -> tuple[int, str, list[Improvement]]:
    """Score NAICS match. Max 30."""
    if not opp_naics:
        return 10, "Opportunity has no NAICS code (neutral)", []
    if not org_naics:
        return (
            0,
            "Org has no NAICS codes configured",
            [
                Improvement(
                    factor="naics",
                    action=(
                        f"Add NAICS code {opp_naics} to your organization profile "
                        "for an exact match on this and similar opportunities."
                    ),
                    potential_gain=30,
                    effort="low",
                )
            ],
        )
    if opp_naics in org_naics:
        return 30, f"Exact NAICS match on {opp_naics}", []
    # Partial match: same 4-digit industry group
    for code in org_naics:
        if code[:4] == opp_naics[:4]:
            return (
                20,
                f"Industry-group match ({opp_naics[:4]}xx)",
                [
                    Improvement(
                        factor="naics",
                        action=(
                            f"Add NAICS {opp_naics} to your profile — you already "
                            f"hold the related code {code}, so qualifying is straightforward."
                        ),
                        potential_gain=10,
                        effort="low",
                    )
                ],
            )
        if code[:2] == opp_naics[:2]:
            return (
                10,
                f"Sector match ({opp_naics[:2]}xxxx)",
                [
                    Improvement(
                        factor="naics",
                        action=(
                            f"Add NAICS {opp_naics} to your profile to lift this from "
                            "a sector match to an exact match."
                        ),
                        potential_gain=20,
                        effort="low",
                    )
                ],
            )
    return (
        0,
        f"No NAICS overlap (opp: {opp_naics})",
        [
            Improvement(
                factor="naics",
                action=(
                    f"Add NAICS {opp_naics} to your organization profile if your "
                    "business performs work in this industry."
                ),
                potential_gain=30,
                effort="medium",
            )
        ],
    )


def _past_performance_score(
    opp: Opportunity, past_perf: list[OrgPastPerformance]
) -> tuple[int, str, list[float], list[Improvement]]:
    """Score past-performance relevance. Max 40."""
    if not past_perf:
        return (
            0,
            "No past performance records on file",
            [],
            [
                Improvement(
                    factor="past_performance",
                    action=(
                        "Upload at least one past performance record on the "
                        "Organization page. The smart-upload feature will extract "
                        "fields from a contract or CPARS document automatically."
                    ),
                    potential_gain=40,
                    effort="low",
                )
            ],
        )

    title_lower = (opp.title or "").lower()
    desc_lower = (opp.description or "").lower()
    agency_lower = (opp.agency or "").lower()
    opp_text = f"{title_lower} {desc_lower}"

    # Build keyword set from opportunity text
    opp_words = {w for w in opp_text.split() if len(w) > 4}

    best_score = 0
    best_match = ""
    values: list[float] = []
    has_agency_match = False

    for pp in past_perf:
        if pp.contract_value:
            values.append(float(pp.contract_value))
        pp_text = f"{(pp.contract_name or '').lower()} {(pp.description or '').lower()}"
        pp_words = {w for w in pp_text.split() if len(w) > 4}
        overlap = len(opp_words & pp_words)
        pp_score = 0

        # Same agency is worth a lot
        if agency_lower and pp.agency and agency_lower in pp.agency.lower():
            pp_score += 20
            has_agency_match = True

        # Keyword overlap
        if overlap >= 5:
            pp_score += 20
        elif overlap >= 3:
            pp_score += 12
        elif overlap >= 1:
            pp_score += 5

        # Relevance tags
        if pp.relevance_tags:
            tags = pp.relevance_tags if isinstance(pp.relevance_tags, list) else []
            for tag in tags:
                if isinstance(tag, str) and tag.lower() in opp_text:
                    pp_score += 5
                    break

        if pp_score > best_score:
            best_score = pp_score
            best_match = pp.contract_name or "(unnamed)"

    score = min(40, best_score)
    if score == 0:
        note = f"{len(past_perf)} past-performance record(s) found, none relevant"
    else:
        note = f"Best match: {best_match} ({score}/40)"

    improvements: list[Improvement] = []
    if score < 40:
        keywords = sorted(opp_words)[:5]
        kw_hint = f" (keywords: {', '.join(keywords)})" if keywords else ""
        if not has_agency_match and opp.agency:
            improvements.append(
                Improvement(
                    factor="past_performance",
                    action=(
                        f"Add past performance with {opp.agency} as the agency. "
                        "Same-agency relationships are weighted heavily."
                    ),
                    potential_gain=20,
                    effort="medium",
                )
            )
        if score < 20:
            improvements.append(
                Improvement(
                    factor="past_performance",
                    action=(
                        f"Add detailed descriptions to your past performance records that "
                        f"mention the work area for this opportunity{kw_hint}."
                    ),
                    potential_gain=min(20, 40 - score),
                    effort="low",
                )
            )
        if score < 30:
            improvements.append(
                Improvement(
                    factor="past_performance",
                    action=(
                        "Tag your past performance records with relevance tags that match "
                        "this opportunity's scope (e.g. cybersecurity, medical, logistics)."
                    ),
                    potential_gain=5,
                    effort="low",
                )
            )
    return score, note, values, improvements


async def compute_match_score(
    session: AsyncSession,
    organization_id: str,
    opportunity_id: str,
) -> MatchBreakdown:
    """Compute the match score for an opportunity against an organization."""

    org = (
        await session.execute(select(Organization).where(Organization.id == organization_id))
    ).scalar_one_or_none()
    opp = (
        await session.execute(select(Opportunity).where(Opportunity.id == opportunity_id))
    ).scalar_one_or_none()

    if not org or not opp:
        return MatchBreakdown(notes=["Organization or opportunity not found"])

    past_perf = (
        await session.execute(
            select(OrgPastPerformance).where(OrgPastPerformance.organization_id == organization_id)
        )
    ).scalars().all()

    org_naics = _parse_naics_list(org.naics_codes)
    org_set_asides = _parse_naics_list(getattr(org, "set_asides", None))

    naics_pts, naics_note, naics_imps = _naics_score(opp.naics_code, org_naics)
    pp_pts, pp_note, pp_values, pp_imps = _past_performance_score(opp, past_perf)
    sa_pts, sa_note, sa_imps = _set_aside_fit(opp.set_aside_type, org_set_asides)
    val_pts, val_note, val_imps = _value_fit(
        float(opp.estimated_value) if opp.estimated_value else None, pp_values
    )

    total = naics_pts + pp_pts + sa_pts + val_pts
    if total >= GREEN_THRESHOLD:
        tier = "green"
    elif total >= YELLOW_THRESHOLD:
        tier = "yellow"
    else:
        tier = "red"

    # Sort improvements by potential gain (biggest impact first)
    improvements = naics_imps + pp_imps + sa_imps + val_imps
    improvements.sort(key=lambda i: i.potential_gain, reverse=True)

    return MatchBreakdown(
        naics_score=naics_pts,
        past_performance_score=pp_pts,
        set_aside_score=sa_pts,
        value_fit_score=val_pts,
        total=total,
        tier=tier,
        notes=[naics_note, pp_note, sa_note, val_note],
        improvements=improvements,
    )


# Set-aside normalization map for SAM.gov raw values
SET_ASIDE_NORMALIZATION = {
    "total small business set-aside": "sba",
    "total small business": "sba",
    "small business set-aside": "sba",
    "small business set aside": "sba",
    "sba": "sba",
    "sbsa": "sbsa",
    "partial small business set-aside": "sbsa",
    "women-owned small business": "wosb",
    "women owned small business": "wosb",
    "wosb": "wosb",
    "economically disadvantaged women-owned small business": "edwosb",
    "edwosb": "edwosb",
    "service-disabled veteran-owned small business": "sdvosb",
    "service disabled veteran owned small business": "sdvosb",
    "sdvosb": "sdvosb",
    "hubzone": "hubzone",
    "hubzone set-aside": "hubzone",
    "8(a)": "8a",
    "8a": "8a",
    "8(a) competitive": "8a",
    "8(a) sole source": "8a",
}


def normalize_set_aside(raw: Optional[str]) -> Optional[str]:
    """Map SAM.gov raw set-aside text to a canonical code."""
    if not raw:
        return None
    key = raw.strip().lower()
    if key in SET_ASIDE_NORMALIZATION:
        return SET_ASIDE_NORMALIZATION[key]
    # Try partial match
    for k, v in SET_ASIDE_NORMALIZATION.items():
        if k in key or key in k:
            return v
    return None
