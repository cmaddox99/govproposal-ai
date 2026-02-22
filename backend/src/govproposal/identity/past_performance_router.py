"""Past Performance API router."""

from fastapi import APIRouter, HTTPException, status
from sqlalchemy import select

from govproposal.identity.dependencies import (
    CurrentUser,
    DbSession,
    require_org_admin,
    require_org_member,
)
from govproposal.identity.models import OrgPastPerformance
from govproposal.identity.schemas import (
    PastPerformanceCreate,
    PastPerformanceResponse,
    PastPerformanceUpdate,
)

router = APIRouter(
    prefix="/api/v1/organizations/{org_id}/past-performance",
    tags=["past-performance"],
)


@router.post("", response_model=PastPerformanceResponse, status_code=status.HTTP_201_CREATED)
async def create_past_performance(
    org_id: str,
    data: PastPerformanceCreate,
    current_user: CurrentUser,
    session: DbSession,
) -> PastPerformanceResponse:
    """Create a past performance record."""
    await require_org_member(org_id, current_user, session)

    record = OrgPastPerformance(
        organization_id=org_id,
        **data.model_dump(),
    )
    session.add(record)
    await session.commit()
    await session.refresh(record)

    return PastPerformanceResponse.model_validate(record)


@router.get("", response_model=list[PastPerformanceResponse])
async def list_past_performance(
    org_id: str,
    current_user: CurrentUser,
    session: DbSession,
) -> list[PastPerformanceResponse]:
    """List all past performance records for an organization."""
    await require_org_member(org_id, current_user, session)

    query = (
        select(OrgPastPerformance)
        .where(OrgPastPerformance.organization_id == org_id)
        .order_by(OrgPastPerformance.created_at.desc())
    )
    result = await session.execute(query)
    records = result.scalars().all()

    return [PastPerformanceResponse.model_validate(r) for r in records]


@router.get("/{pp_id}", response_model=PastPerformanceResponse)
async def get_past_performance(
    org_id: str,
    pp_id: str,
    current_user: CurrentUser,
    session: DbSession,
) -> PastPerformanceResponse:
    """Get a specific past performance record."""
    await require_org_member(org_id, current_user, session)

    query = select(OrgPastPerformance).where(
        OrgPastPerformance.id == pp_id,
        OrgPastPerformance.organization_id == org_id,
    )
    result = await session.execute(query)
    record = result.scalar_one_or_none()

    if not record:
        raise HTTPException(status_code=404, detail="Past performance record not found")

    return PastPerformanceResponse.model_validate(record)


@router.put("/{pp_id}", response_model=PastPerformanceResponse)
async def update_past_performance(
    org_id: str,
    pp_id: str,
    data: PastPerformanceUpdate,
    current_user: CurrentUser,
    session: DbSession,
) -> PastPerformanceResponse:
    """Update a past performance record."""
    await require_org_admin(org_id, current_user, session)

    query = select(OrgPastPerformance).where(
        OrgPastPerformance.id == pp_id,
        OrgPastPerformance.organization_id == org_id,
    )
    result = await session.execute(query)
    record = result.scalar_one_or_none()

    if not record:
        raise HTTPException(status_code=404, detail="Past performance record not found")

    update_data = data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(record, field, value)

    await session.commit()
    await session.refresh(record)

    return PastPerformanceResponse.model_validate(record)


@router.delete("/{pp_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_past_performance(
    org_id: str,
    pp_id: str,
    current_user: CurrentUser,
    session: DbSession,
) -> None:
    """Delete a past performance record."""
    await require_org_admin(org_id, current_user, session)

    query = select(OrgPastPerformance).where(
        OrgPastPerformance.id == pp_id,
        OrgPastPerformance.organization_id == org_id,
    )
    result = await session.execute(query)
    record = result.scalar_one_or_none()

    if not record:
        raise HTTPException(status_code=404, detail="Past performance record not found")

    await session.delete(record)
    await session.commit()
