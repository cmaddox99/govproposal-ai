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

    # Get organization's NAICS codes if not specified
    if not naics_codes:
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
