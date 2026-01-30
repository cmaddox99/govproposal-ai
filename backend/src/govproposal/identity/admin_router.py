"""Organization admin API router."""

from typing import Annotated

from fastapi import APIRouter, Depends, Query, status

from govproposal.identity.dependencies import (
    CurrentUser,
    DbSession,
    OrgSvc,
    require_org_admin,
    require_org_owner,
)
from govproposal.identity.models import User
from govproposal.identity.repository import OrganizationRepository, UserRepository
from govproposal.identity.schemas import (
    InviteResponse,
    InviteUserRequest,
    MessageResponse,
    OrgUserResponse,
    RoleChangeRequest,
)

router = APIRouter(prefix="/api/v1/organizations/{org_id}", tags=["organization-admin"])


@router.get("/users", response_model=list[OrgUserResponse])
async def list_org_users(
    org_id: str,
    current_user: CurrentUser,
    session: DbSession,
    service: OrgSvc,
    limit: Annotated[int, Query(ge=1, le=100)] = 50,
    offset: Annotated[int, Query(ge=0)] = 0,
) -> list[OrgUserResponse]:
    """List all users in organization. Requires admin role."""
    await require_org_admin(org_id, current_user, session)

    org_repo = OrganizationRepository(session)
    user_repo = UserRepository(session)

    members, _ = await org_repo.list_members(org_id, limit, offset)

    users = []
    for member in members:
        user = await user_repo.get_by_id(member.user_id)
        if user:
            users.append(
                OrgUserResponse(
                    id=member.id,
                    user_id=user.id,
                    email=user.email,
                    role=member.role,
                    is_active=user.is_active,
                    mfa_enabled=user.mfa_enabled,
                    invited_at=member.invited_at,
                    joined_at=member.joined_at,
                )
            )

    return users


@router.post("/users/invite", response_model=InviteResponse, status_code=status.HTTP_201_CREATED)
async def invite_user(
    org_id: str,
    data: InviteUserRequest,
    current_user: CurrentUser,
    session: DbSession,
    service: OrgSvc,
) -> InviteResponse:
    """Invite user to organization. Requires admin role."""
    await require_org_admin(org_id, current_user, session)

    member = await service.invite_user(org_id, data.email, data.role)

    return InviteResponse(
        id=member.id,
        email=member.email,
        role=member.role,
        invited_at=member.invited_at,
    )


@router.put("/users/{user_id}/role", response_model=OrgUserResponse)
async def change_user_role(
    org_id: str,
    user_id: str,
    data: RoleChangeRequest,
    current_user: CurrentUser,
    session: DbSession,
    service: OrgSvc,
) -> OrgUserResponse:
    """Change user's role. Requires owner role to change to/from owner."""
    # Check if changing to/from owner role - requires owner permission
    org_repo = OrganizationRepository(session)
    member = await org_repo.get_member(org_id, user_id)

    if data.role == "owner" or (member and member.role == "owner"):
        await require_org_owner(org_id, current_user, session)
    else:
        await require_org_admin(org_id, current_user, session)

    updated_member = await service.change_member_role(org_id, user_id, data.role)

    user_repo = UserRepository(session)
    user = await user_repo.get_by_id(user_id)

    return OrgUserResponse(
        id=updated_member.id,
        user_id=user_id,
        email=user.email if user else "",
        role=updated_member.role,
        is_active=user.is_active if user else False,
        mfa_enabled=user.mfa_enabled if user else False,
        invited_at=updated_member.invited_at,
        joined_at=updated_member.joined_at,
    )


@router.delete("/users/{user_id}", response_model=MessageResponse)
async def remove_user(
    org_id: str,
    user_id: str,
    current_user: CurrentUser,
    session: DbSession,
    service: OrgSvc,
) -> MessageResponse:
    """Remove user from organization. Requires admin role."""
    await require_org_admin(org_id, current_user, session)

    # Prevent removing self
    if user_id == current_user.id:
        from govproposal.identity.exceptions import ForbiddenError

        raise ForbiddenError("Cannot remove yourself from the organization")

    # Prevent removing owner (must transfer ownership first)
    org_repo = OrganizationRepository(session)
    member = await org_repo.get_member(org_id, user_id)
    if member and member.role == "owner":
        from govproposal.identity.exceptions import ForbiddenError

        raise ForbiddenError("Cannot remove organization owner")

    removed = await service.remove_member(org_id, user_id)
    if not removed:
        from govproposal.identity.exceptions import UserNotFoundError

        raise UserNotFoundError()

    return MessageResponse(message="User removed from organization")
