"""Opportunities API router."""

from datetime import datetime, timedelta, timezone
from typing import Annotated, Optional, List

from fastapi import APIRouter, Depends, Query, HTTPException, status
from pydantic import BaseModel, Field
from sqlalchemy import select, or_, and_
from sqlalchemy.ext.asyncio import AsyncSession

from govproposal.db.base import get_db
from govproposal.identity.dependencies import CurrentUser
from govproposal.identity.models import Organization, OrganizationMember
from govproposal.opportunities.models import Opportunity
from govproposal.opportunities.sam_service import SAMGovService
from govproposal.opportunities.ebuy_service import EBuyOpenService
from govproposal.config import settings

router = APIRouter(prefix="/api/v1/opportunities", tags=["opportunities"])

DbSession = Annotated[AsyncSession, Depends(get_db)]


class OpportunityResponse(BaseModel):
    """Opportunity response schema."""
    id: str
    notice_id: str
    solicitation_number: Optional[str] = None
    title: str
    description: Optional[str] = None
    department: Optional[str] = None
    agency: Optional[str] = None
    office: Optional[str] = None
    notice_type: str
    naics_code: Optional[str] = None
    naics_description: Optional[str] = None
    set_aside_type: Optional[str] = None
    set_aside_description: Optional[str] = None
    posted_date: Optional[datetime] = None
    response_deadline: Optional[datetime] = None
    place_of_performance_city: Optional[str] = None
    place_of_performance_state: Optional[str] = None
    primary_contact_name: Optional[str] = None
    primary_contact_email: Optional[str] = None
    sam_url: Optional[str] = None
    estimated_value: Optional[float] = None
    source: str = "sam_gov"

    class Config:
        from_attributes = True


class OpportunityListResponse(BaseModel):
    """Paginated opportunity list response."""
    opportunities: List[OpportunityResponse]
    total: int
    limit: int
    offset: int


class SyncResponse(BaseModel):
    """Sync operation response."""
    synced: int
    errors: int
    message: str


@router.get("", response_model=OpportunityListResponse)
async def list_opportunities(
    current_user: CurrentUser,
    session: DbSession,
    org_id: Annotated[str, Query(description="Organization ID")],
    naics_codes: Annotated[Optional[str], Query(description="Comma-separated NAICS codes")] = None,
    keywords: Annotated[Optional[str], Query(description="Search keywords")] = None,
    notice_type: Annotated[Optional[str], Query(description="Notice type filter")] = None,
    set_aside_type: Annotated[Optional[str], Query(description="Comma-separated set-aside types")] = None,
    value_min: Annotated[Optional[float], Query(description="Minimum estimated value")] = None,
    value_max: Annotated[Optional[float], Query(description="Maximum estimated value")] = None,
    posted_from: Annotated[Optional[str], Query(description="Posted from date (YYYY-MM-DD)")] = None,
    posted_to: Annotated[Optional[str], Query(description="Posted to date (YYYY-MM-DD)")] = None,
    deadline_from: Annotated[Optional[str], Query(description="Response deadline from date (YYYY-MM-DD)")] = None,
    deadline_to: Annotated[Optional[str], Query(description="Response deadline to date (YYYY-MM-DD)")] = None,
    date_from: Annotated[Optional[str], Query(description="Date from - matches posted date OR deadline (YYYY-MM-DD)")] = None,
    date_to: Annotated[Optional[str], Query(description="Date to - matches posted date OR deadline (YYYY-MM-DD)")] = None,
    source: Annotated[Optional[str], Query(description="Source filter (sam_gov, gsa_ebuy)")] = None,
    active_only: Annotated[bool, Query(description="Only show opportunities with future deadlines")] = True,
    limit: Annotated[int, Query(ge=1, le=100)] = 50,
    offset: Annotated[int, Query(ge=0)] = 0,
) -> OpportunityListResponse:
    """List opportunities, optionally filtered by organization's NAICS codes."""

    # Verify user is member of org
    member_query = select(OrganizationMember).where(
        and_(
            OrganizationMember.organization_id == org_id,
            OrganizationMember.user_id == current_user.id,
        )
    )
    member = (await session.execute(member_query)).scalar_one_or_none()
    if not member:
        raise HTTPException(status_code=403, detail="Not a member of this organization")

    # Only apply org NAICS codes when no other filters are active
    has_filters = any([
        set_aside_type, value_min is not None, value_max is not None,
        posted_from, posted_to, deadline_from, deadline_to,
        date_from, date_to, source, keywords,
    ])
    if not naics_codes and not has_filters:
        org_query = select(Organization).where(Organization.id == org_id)
        org = (await session.execute(org_query)).scalar_one_or_none()
        if org and org.naics_codes:
            # Parse NAICS codes from stored format
            import json
            try:
                naics_list = json.loads(org.naics_codes) if isinstance(org.naics_codes, str) else org.naics_codes
                if naics_list:
                    naics_codes = ",".join(naics_list)
            except:
                pass

    # Build query
    query = select(Opportunity)
    conditions = []

    if active_only:
        conditions.append(
            or_(
                Opportunity.response_deadline.is_(None),
                Opportunity.response_deadline > datetime.now(timezone.utc),
            )
        )

    if naics_codes:
        naics_list = [n.strip() for n in naics_codes.split(",")]
        conditions.append(Opportunity.naics_code.in_(naics_list))

    if keywords:
        keyword_filter = or_(
            Opportunity.title.ilike(f"%{keywords}%"),
            Opportunity.description.ilike(f"%{keywords}%"),
        )
        conditions.append(keyword_filter)

    if notice_type:
        conditions.append(Opportunity.notice_type == notice_type)

    if set_aside_type:
        conditions.append(Opportunity.set_aside_type.in_(set_aside_type.split(",")))

    if value_min is not None:
        conditions.append(Opportunity.estimated_value >= value_min)

    if value_max is not None:
        conditions.append(Opportunity.estimated_value <= value_max)

    if posted_from:
        conditions.append(
            Opportunity.posted_date >= datetime.strptime(posted_from, "%Y-%m-%d").replace(
                tzinfo=timezone.utc
            )
        )

    if posted_to:
        # Use end of day so "posted_to=2026-02-23" includes the entire day
        conditions.append(
            Opportunity.posted_date <= datetime.strptime(posted_to, "%Y-%m-%d").replace(
                hour=23, minute=59, second=59, tzinfo=timezone.utc
            )
        )

    if deadline_from:
        conditions.append(
            Opportunity.response_deadline >= datetime.strptime(deadline_from, "%Y-%m-%d").replace(
                tzinfo=timezone.utc
            )
        )

    if deadline_to:
        conditions.append(
            Opportunity.response_deadline <= datetime.strptime(deadline_to, "%Y-%m-%d").replace(
                hour=23, minute=59, second=59, tzinfo=timezone.utc
            )
        )

    # Unified date filter: matches opportunities where EITHER posted_date
    # OR response_deadline falls within the range
    if date_from or date_to:
        date_conditions = []
        if date_from:
            d_from = datetime.strptime(date_from, "%Y-%m-%d").replace(tzinfo=timezone.utc)
            if date_to:
                d_to = datetime.strptime(date_to, "%Y-%m-%d").replace(
                    hour=23, minute=59, second=59, tzinfo=timezone.utc
                )
                date_conditions.append(
                    and_(Opportunity.posted_date >= d_from, Opportunity.posted_date <= d_to)
                )
                date_conditions.append(
                    and_(Opportunity.response_deadline >= d_from, Opportunity.response_deadline <= d_to)
                )
            else:
                date_conditions.append(Opportunity.posted_date >= d_from)
                date_conditions.append(Opportunity.response_deadline >= d_from)
        elif date_to:
            d_to = datetime.strptime(date_to, "%Y-%m-%d").replace(
                hour=23, minute=59, second=59, tzinfo=timezone.utc
            )
            date_conditions.append(Opportunity.posted_date <= d_to)
            date_conditions.append(Opportunity.response_deadline <= d_to)
        conditions.append(or_(*date_conditions))

    if source:
        conditions.append(Opportunity.source == source)

    if conditions:
        query = query.where(and_(*conditions))

    # Get total count
    count_query = select(Opportunity.id)
    if conditions:
        count_query = count_query.where(and_(*conditions))
    total_result = await session.execute(count_query)
    total = len(total_result.all())

    # Add ordering and pagination
    query = query.order_by(Opportunity.response_deadline.asc().nullslast())
    query = query.limit(limit).offset(offset)

    result = await session.execute(query)
    opportunities = result.scalars().all()

    return OpportunityListResponse(
        opportunities=[OpportunityResponse.model_validate(o) for o in opportunities],
        total=total,
        limit=limit,
        offset=offset,
    )


@router.get("/{opportunity_id}", response_model=OpportunityResponse)
async def get_opportunity(
    opportunity_id: str,
    current_user: CurrentUser,
    session: DbSession,
) -> OpportunityResponse:
    """Get opportunity details."""
    query = select(Opportunity).where(Opportunity.id == opportunity_id)
    result = await session.execute(query)
    opportunity = result.scalar_one_or_none()

    if not opportunity:
        raise HTTPException(status_code=404, detail="Opportunity not found")

    return OpportunityResponse.model_validate(opportunity)


@router.post("/sync", response_model=SyncResponse)
async def sync_opportunities(
    current_user: CurrentUser,
    session: DbSession,
    org_id: Annotated[str, Query(description="Organization ID")],
    naics_codes: Annotated[Optional[str], Query(description="Comma-separated NAICS codes to sync")] = None,
) -> SyncResponse:
    """Sync opportunities from SAM.gov for the organization's NAICS codes."""

    # Verify user is member of org
    member_query = select(OrganizationMember).where(
        and_(
            OrganizationMember.organization_id == org_id,
            OrganizationMember.user_id == current_user.id,
        )
    )
    member = (await session.execute(member_query)).scalar_one_or_none()
    if not member:
        raise HTTPException(status_code=403, detail="Not a member of this organization")

    # Get NAICS codes
    if not naics_codes:
        org_query = select(Organization).where(Organization.id == org_id)
        org = (await session.execute(org_query)).scalar_one_or_none()
        if org and org.naics_codes:
            import json
            try:
                naics_list = json.loads(org.naics_codes) if isinstance(org.naics_codes, str) else org.naics_codes
                if naics_list:
                    naics_codes = ",".join(naics_list)
            except:
                pass

    if not naics_codes:
        raise HTTPException(
            status_code=400,
            detail="No NAICS codes specified. Add NAICS codes to your organization or specify them in the request.",
        )

    # Check if SAM API key is configured
    if not settings.sam_api_key:
        raise HTTPException(
            status_code=503,
            detail="SAM.gov API key not configured. Please contact support.",
        )

    synced = 0
    errors = 0

    try:
        sam_service = SAMGovService()
        naics_list = [n.strip() for n in naics_codes.split(",")]

        # Search for recent opportunities (posted in last 90 days)
        result = await sam_service.search_opportunities(
            naics_codes=naics_list,
            posted_from=datetime.now(timezone.utc) - timedelta(days=90),
            posted_to=datetime.now(timezone.utc),
            limit=100,
        )

        opportunities_data = result.get("opportunitiesData", [])

        for opp_data in opportunities_data:
            try:
                parsed = sam_service.parse_opportunity(opp_data)

                # Check if opportunity already exists
                existing_query = select(Opportunity).where(
                    Opportunity.notice_id == parsed["notice_id"]
                )
                existing = (await session.execute(existing_query)).scalar_one_or_none()

                if existing:
                    # Update existing opportunity
                    for key, value in parsed.items():
                        if value is not None:
                            setattr(existing, key, value)
                    existing.last_synced_at = datetime.now(timezone.utc)
                else:
                    # Create new opportunity
                    new_opp = Opportunity(**parsed)
                    session.add(new_opp)

                synced += 1
            except Exception as e:
                errors += 1
                continue

        await session.commit()

    except Exception as e:
        raise HTTPException(
            status_code=503,
            detail=f"Failed to sync from SAM.gov: {str(e)}",
        )

    return SyncResponse(
        synced=synced,
        errors=errors,
        message=f"Successfully synced {synced} opportunities" + (f" with {errors} errors" if errors else ""),
    )


@router.post("/sync-ebuy", response_model=SyncResponse)
async def sync_ebuy_opportunities(
    current_user: CurrentUser,
    session: DbSession,
    org_id: Annotated[str, Query(description="Organization ID")],
    keywords: Annotated[Optional[str], Query(description="Search keywords")] = None,
) -> SyncResponse:
    """Sync opportunities from GSA eBuy Open."""

    # Verify user is member of org
    member_query = select(OrganizationMember).where(
        and_(
            OrganizationMember.organization_id == org_id,
            OrganizationMember.user_id == current_user.id,
        )
    )
    member = (await session.execute(member_query)).scalar_one_or_none()
    if not member:
        raise HTTPException(status_code=403, detail="Not a member of this organization")

    synced = 0
    errors = 0

    try:
        ebuy_service = EBuyOpenService()
        opportunities_data = await ebuy_service.search_opportunities(
            keywords=keywords,
            limit=100,
        )

        for parsed in opportunities_data:
            try:
                # Check if opportunity already exists
                existing_query = select(Opportunity).where(
                    Opportunity.notice_id == parsed["notice_id"]
                )
                existing = (await session.execute(existing_query)).scalar_one_or_none()

                if existing:
                    for key, value in parsed.items():
                        if value is not None:
                            setattr(existing, key, value)
                    existing.last_synced_at = datetime.now(timezone.utc)
                else:
                    new_opp = Opportunity(**parsed)
                    session.add(new_opp)

                synced += 1
            except Exception:
                errors += 1
                continue

        await session.commit()

    except Exception as e:
        raise HTTPException(
            status_code=503,
            detail=f"Failed to sync from GSA eBuy: {str(e)}",
        )

    return SyncResponse(
        synced=synced,
        errors=errors,
        message=f"Successfully synced {synced} opportunities from GSA eBuy"
        + (f" with {errors} errors" if errors else ""),
    )


