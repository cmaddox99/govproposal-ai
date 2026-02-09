"""Organization API router."""

from typing import Annotated

from fastapi import APIRouter, Depends, Query, status

from govproposal.identity.dependencies import (
    CurrentUser,
    DbSession,
    OrgSvc,
    require_org_admin,
    require_org_member,
)
from govproposal.identity.schemas import (
    MessageResponse,
    OrganizationCreate,
    OrganizationMemberResponse,
    OrganizationResponse,
    OrganizationUpdate,
)
from govproposal.identity.models import Organization
from sqlalchemy import select
import json

router = APIRouter(prefix="/api/v1/organizations", tags=["organizations"])


@router.post("", response_model=OrganizationResponse, status_code=status.HTTP_201_CREATED)
async def create_organization(
    data: OrganizationCreate,
    current_user: CurrentUser,
    service: OrgSvc,
) -> OrganizationResponse:
    """Create a new organization with current user as owner."""
    return await service.create_organization(
        name=data.name,
        slug=data.slug,
        owner_id=current_user.id,
    )


@router.get("", response_model=list[OrganizationResponse])
async def list_organizations(
    current_user: CurrentUser,
    service: OrgSvc,
) -> list[OrganizationResponse]:
    """List organizations the current user belongs to."""
    return await service.list_user_organizations(current_user.id)


@router.get("/{org_id}", response_model=OrganizationResponse)
async def get_organization(
    org_id: str,
    current_user: CurrentUser,
    session: DbSession,
    service: OrgSvc,
) -> OrganizationResponse:
    """Get organization details."""
    # Verify membership
    await require_org_member(org_id, current_user, session)
    return await service.get_organization(org_id)


@router.get("/{org_id}/members", response_model=list[OrganizationMemberResponse])
async def list_organization_members(
    org_id: str,
    current_user: CurrentUser,
    session: DbSession,
    service: OrgSvc,
    limit: Annotated[int, Query(ge=1, le=100)] = 50,
    offset: Annotated[int, Query(ge=0)] = 0,
) -> list[OrganizationMemberResponse]:
    """List organization members."""
    await require_org_member(org_id, current_user, session)
    members, _ = await service.get_organization_members(org_id, limit, offset)
    return members


@router.put("/{org_id}", response_model=OrganizationResponse)
async def update_organization(
    org_id: str,
    data: OrganizationUpdate,
    current_user: CurrentUser,
    session: DbSession,
) -> OrganizationResponse:
    """Update organization details (admin/owner only)."""
    # Verify admin/owner role
    await require_org_admin(org_id, current_user, session)

    # Get organization
    query = select(Organization).where(Organization.id == org_id)
    result = await session.execute(query)
    org = result.scalar_one_or_none()

    if not org:
        from fastapi import HTTPException
        raise HTTPException(status_code=404, detail="Organization not found")

    # Update fields
    update_data = data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        if field == "naics_codes" and value is not None:
            # Store NAICS codes as JSON string
            setattr(org, field, json.dumps(value))
        else:
            setattr(org, field, value)

    await session.commit()
    await session.refresh(org)

    # Parse naics_codes back to list for response
    response_data = {
        "id": org.id,
        "name": org.name,
        "slug": org.slug,
        "is_active": org.is_active,
        "contact_email": org.contact_email,
        "phone": org.phone,
        "address": org.address,
        "uei_number": org.uei_number,
        "cage_code": org.cage_code,
        "duns_number": org.duns_number,
        "naics_codes": json.loads(org.naics_codes) if org.naics_codes else None,
        "created_at": org.created_at,
    }

    return OrganizationResponse(**response_data)
