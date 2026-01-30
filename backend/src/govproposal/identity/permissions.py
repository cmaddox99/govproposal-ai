"""Permission system for role-based access control."""

from enum import Enum
from typing import Optional, Set, List


class Permission(str, Enum):
    """All permissions available in the system."""

    # Proposal permissions
    PROPOSAL_VIEW = "proposal:view"
    PROPOSAL_EDIT = "proposal:edit"
    PROPOSAL_DELETE = "proposal:delete"
    PROPOSAL_CREATE = "proposal:create"

    # Analysis permissions
    ANALYSIS_RUN = "analysis:run"
    ANALYSIS_VIEW = "analysis:view"
    ANALYSIS_EXPORT = "analysis:export"

    # Admin permissions (Company Administrator)
    ORG_USERS_MANAGE = "org:users:manage"
    ORG_SETTINGS_MANAGE = "org:settings:manage"
    ORG_AUDIT_VIEW = "org:audit:view"
    ORG_TEMPLATES_MANAGE = "org:templates:manage"

    # Platform permissions (Super User only)
    PLATFORM_CONFIG = "platform:config"
    PLATFORM_TENANTS = "platform:tenants"
    PLATFORM_AUDIT = "platform:audit"
    PLATFORM_FEATURES = "platform:features"


# Role to permission mapping
MEMBER_PERMISSIONS: Set[Permission] = {
    Permission.PROPOSAL_VIEW,
    Permission.PROPOSAL_EDIT,
    Permission.ANALYSIS_RUN,
    Permission.ANALYSIS_VIEW,
}

ADMIN_PERMISSIONS: Set[Permission] = MEMBER_PERMISSIONS | {
    Permission.PROPOSAL_CREATE,
    Permission.PROPOSAL_DELETE,
    Permission.ANALYSIS_EXPORT,
    Permission.ORG_USERS_MANAGE,
    Permission.ORG_SETTINGS_MANAGE,
    Permission.ORG_AUDIT_VIEW,
    Permission.ORG_TEMPLATES_MANAGE,
}

OWNER_PERMISSIONS: Set[Permission] = ADMIN_PERMISSIONS  # Owner has all admin permissions

SUPER_USER_PERMISSIONS: Set[Permission] = {
    Permission.PLATFORM_CONFIG,
    Permission.PLATFORM_TENANTS,
    Permission.PLATFORM_AUDIT,
    Permission.PLATFORM_FEATURES,
}


def get_permissions_for_role(
    org_role: Optional[str], platform_role: str = "basic"
) -> Set[Permission]:
    """Get all permissions for a user based on their roles.

    Args:
        org_role: The user's role within the organization (owner, admin, member, or None)
        platform_role: The user's platform-level role (basic or super_user)

    Returns:
        Set of Permission enum values the user has access to
    """
    permissions: Set[Permission] = set()

    if org_role == "member":
        permissions |= MEMBER_PERMISSIONS
    elif org_role == "admin":
        permissions |= ADMIN_PERMISSIONS
    elif org_role == "owner":
        permissions |= OWNER_PERMISSIONS

    if platform_role == "super_user":
        permissions |= SUPER_USER_PERMISSIONS

    return permissions


def has_permission(
    permission: Permission,
    org_role: Optional[str],
    platform_role: str = "basic",
) -> bool:
    """Check if a role combination has a specific permission.

    Args:
        permission: The permission to check
        org_role: The user's role within the organization
        platform_role: The user's platform-level role

    Returns:
        True if the user has the permission, False otherwise
    """
    return permission in get_permissions_for_role(org_role, platform_role)


def get_all_permissions() -> List[Permission]:
    """Get a list of all available permissions."""
    return list(Permission)


def get_org_permissions() -> Set[Permission]:
    """Get all organization-level permissions (non-platform)."""
    return OWNER_PERMISSIONS


def get_platform_permissions() -> Set[Permission]:
    """Get all platform-level permissions."""
    return SUPER_USER_PERMISSIONS
