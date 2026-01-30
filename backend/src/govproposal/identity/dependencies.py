"""FastAPI dependencies for identity module."""

from typing import Annotated

import jwt
from fastapi import Depends, Header
from sqlalchemy.ext.asyncio import AsyncSession

from govproposal.db.base import get_db
from govproposal.identity.exceptions import (
    AuthenticationError,
    ForbiddenError,
    InsufficientPermissionsError,
    InvalidTokenError,
    MFASetupRequiredError,
    NotOrgMemberError,
    TokenExpiredError,
)
from govproposal.identity.models import User
from govproposal.identity.permissions import Permission, get_permissions_for_role
from govproposal.identity.repository import OrganizationRepository, UserRepository
from govproposal.identity.security import validate_access_token
from govproposal.identity.service import AuthService, MFAService, OrganizationService

# Type aliases for session dependency
DbSession = Annotated[AsyncSession, Depends(get_db)]


async def get_current_user(
    authorization: Annotated[str, Header()],
    session: DbSession,
) -> User:
    """Get the current authenticated user from JWT token.

    Args:
        authorization: The Authorization header value (Bearer token)
        session: Database session

    Returns:
        The authenticated User

    Raises:
        AuthenticationError: If no token provided
        InvalidTokenError: If token is invalid
        TokenExpiredError: If token has expired
    """
    if not authorization or not authorization.startswith("Bearer "):
        raise AuthenticationError("No authentication token provided")

    token = authorization[7:]  # Remove "Bearer " prefix

    try:
        payload = validate_access_token(token)
    except jwt.ExpiredSignatureError as e:
        raise TokenExpiredError() from e
    except jwt.InvalidTokenError as e:
        raise InvalidTokenError() from e

    user_id = payload.get("sub")
    if not user_id:
        raise InvalidTokenError()

    user_repo = UserRepository(session)
    user = await user_repo.get_by_id(user_id)

    if not user:
        raise InvalidTokenError()

    if not user.is_active:
        raise AuthenticationError("User account is disabled")

    return user


# Type alias for current user dependency
CurrentUser = Annotated[User, Depends(get_current_user)]


async def get_current_user_with_mfa_check(
    user: CurrentUser,
) -> User:
    """Verify MFA is set up if required.

    Args:
        user: The current authenticated user

    Returns:
        The authenticated User

    Raises:
        MFASetupRequiredError: If MFA is required but not set up
    """
    if user.mfa_required and not user.mfa_enabled:
        raise MFASetupRequiredError()
    return user


# Type alias for MFA-verified user
MFAVerifiedUser = Annotated[User, Depends(get_current_user_with_mfa_check)]


async def require_permission(
    permission: Permission,
    org_id: str,
    user: CurrentUser,
    session: DbSession,
) -> User:
    """Require user has specific permission in organization.

    Args:
        permission: The required permission
        org_id: The organization ID
        user: The current user
        session: Database session

    Returns:
        The authenticated User

    Raises:
        NotOrgMemberError: If user is not a member of the organization
        InsufficientPermissionsError: If user lacks the required permission
    """
    org_repo = OrganizationRepository(session)
    member = await org_repo.get_member(org_id, user.id)

    if not member:
        raise NotOrgMemberError()

    user_permissions = get_permissions_for_role(member.role, user.platform_role)

    if permission not in user_permissions:
        raise InsufficientPermissionsError(permission.value)

    return user


async def require_org_member(
    org_id: str,
    user: CurrentUser,
    session: DbSession,
) -> User:
    """Require user is a member of the organization.

    Args:
        org_id: The organization ID
        user: The current user
        session: Database session

    Returns:
        The authenticated User

    Raises:
        NotOrgMemberError: If user is not a member
    """
    org_repo = OrganizationRepository(session)
    member = await org_repo.get_member(org_id, user.id)

    if not member:
        raise NotOrgMemberError()

    return user


async def require_org_admin(
    org_id: str,
    user: CurrentUser,
    session: DbSession,
) -> User:
    """Require user has admin or owner role in organization.

    Args:
        org_id: The organization ID
        user: The current user
        session: Database session

    Returns:
        The authenticated User

    Raises:
        NotOrgMemberError: If user is not a member
        ForbiddenError: If user is not admin or owner
    """
    org_repo = OrganizationRepository(session)
    member = await org_repo.get_member(org_id, user.id)

    if not member:
        raise NotOrgMemberError()

    if member.role not in ("admin", "owner"):
        raise ForbiddenError("Admin or owner role required")

    return user


async def require_org_owner(
    org_id: str,
    user: CurrentUser,
    session: DbSession,
) -> User:
    """Require user has owner role in organization.

    Args:
        org_id: The organization ID
        user: The current user
        session: Database session

    Returns:
        The authenticated User

    Raises:
        NotOrgMemberError: If user is not a member
        ForbiddenError: If user is not owner
    """
    org_repo = OrganizationRepository(session)
    member = await org_repo.get_member(org_id, user.id)

    if not member:
        raise NotOrgMemberError()

    if member.role != "owner":
        raise ForbiddenError("Owner role required")

    return user


async def require_super_user(
    user: CurrentUser,
) -> User:
    """Require platform super user role.

    Args:
        user: The current user

    Returns:
        The authenticated User

    Raises:
        ForbiddenError: If user is not a super user
    """
    if user.platform_role != "super_user":
        raise ForbiddenError("Super user access required")
    return user


# Type alias for super user
SuperUser = Annotated[User, Depends(require_super_user)]


def get_auth_service(session: DbSession) -> AuthService:
    """Get AuthService instance."""
    return AuthService(session)


def get_mfa_service(session: DbSession) -> MFAService:
    """Get MFAService instance."""
    return MFAService(session)


def get_org_service(session: DbSession) -> OrganizationService:
    """Get OrganizationService instance."""
    return OrganizationService(session)


# Type aliases for service dependencies
AuthSvc = Annotated[AuthService, Depends(get_auth_service)]
MFASvc = Annotated[MFAService, Depends(get_mfa_service)]
OrgSvc = Annotated[OrganizationService, Depends(get_org_service)]
