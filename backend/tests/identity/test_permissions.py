"""Tests for permission system."""

import pytest
import sys
from pathlib import Path

# Add src to path for direct imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src"))

# Import directly from permissions module (doesn't need database)
from govproposal.identity.permissions import (
    ADMIN_PERMISSIONS,
    MEMBER_PERMISSIONS,
    OWNER_PERMISSIONS,
    SUPER_USER_PERMISSIONS,
    Permission,
    get_permissions_for_role,
    has_permission,
)


class TestPermissionMappings:
    """Test permission role mappings."""

    def test_member_has_basic_permissions(self):
        """Member role should have basic proposal and analysis permissions."""
        assert Permission.PROPOSAL_VIEW in MEMBER_PERMISSIONS
        assert Permission.PROPOSAL_EDIT in MEMBER_PERMISSIONS
        assert Permission.ANALYSIS_RUN in MEMBER_PERMISSIONS
        assert Permission.ANALYSIS_VIEW in MEMBER_PERMISSIONS

    def test_member_lacks_admin_permissions(self):
        """Member role should not have admin permissions."""
        assert Permission.PROPOSAL_CREATE not in MEMBER_PERMISSIONS
        assert Permission.PROPOSAL_DELETE not in MEMBER_PERMISSIONS
        assert Permission.ORG_USERS_MANAGE not in MEMBER_PERMISSIONS
        assert Permission.ORG_AUDIT_VIEW not in MEMBER_PERMISSIONS

    def test_admin_has_member_permissions(self):
        """Admin role should include all member permissions."""
        assert MEMBER_PERMISSIONS.issubset(ADMIN_PERMISSIONS)

    def test_admin_has_org_management_permissions(self):
        """Admin role should have organization management permissions."""
        assert Permission.ORG_USERS_MANAGE in ADMIN_PERMISSIONS
        assert Permission.ORG_SETTINGS_MANAGE in ADMIN_PERMISSIONS
        assert Permission.ORG_AUDIT_VIEW in ADMIN_PERMISSIONS
        assert Permission.ORG_TEMPLATES_MANAGE in ADMIN_PERMISSIONS

    def test_admin_lacks_platform_permissions(self):
        """Admin role should not have platform permissions."""
        assert Permission.PLATFORM_CONFIG not in ADMIN_PERMISSIONS
        assert Permission.PLATFORM_TENANTS not in ADMIN_PERMISSIONS
        assert Permission.PLATFORM_AUDIT not in ADMIN_PERMISSIONS

    def test_owner_has_admin_permissions(self):
        """Owner role should have all admin permissions."""
        assert ADMIN_PERMISSIONS.issubset(OWNER_PERMISSIONS)

    def test_super_user_has_platform_permissions(self):
        """Super user should have platform permissions."""
        assert Permission.PLATFORM_CONFIG in SUPER_USER_PERMISSIONS
        assert Permission.PLATFORM_TENANTS in SUPER_USER_PERMISSIONS
        assert Permission.PLATFORM_AUDIT in SUPER_USER_PERMISSIONS
        assert Permission.PLATFORM_FEATURES in SUPER_USER_PERMISSIONS


class TestGetPermissionsForRole:
    """Test get_permissions_for_role function."""

    def test_member_role(self):
        """Test member role permissions."""
        perms = get_permissions_for_role("member")
        assert perms == MEMBER_PERMISSIONS

    def test_admin_role(self):
        """Test admin role permissions."""
        perms = get_permissions_for_role("admin")
        assert perms == ADMIN_PERMISSIONS

    def test_owner_role(self):
        """Test owner role permissions."""
        perms = get_permissions_for_role("owner")
        assert perms == OWNER_PERMISSIONS

    def test_super_user_platform_role(self):
        """Test super user adds platform permissions."""
        perms = get_permissions_for_role("member", "super_user")
        assert MEMBER_PERMISSIONS.issubset(perms)
        assert SUPER_USER_PERMISSIONS.issubset(perms)

    def test_no_org_role(self):
        """Test no org role returns empty set."""
        perms = get_permissions_for_role(None)
        assert perms == set()

    def test_unknown_role(self):
        """Test unknown role returns empty set."""
        perms = get_permissions_for_role("unknown")
        assert perms == set()


class TestHasPermission:
    """Test has_permission function."""

    def test_member_has_proposal_view(self):
        """Member should have proposal view permission."""
        assert has_permission(Permission.PROPOSAL_VIEW, "member") is True

    def test_member_lacks_proposal_delete(self):
        """Member should not have proposal delete permission."""
        assert has_permission(Permission.PROPOSAL_DELETE, "member") is False

    def test_admin_has_org_users_manage(self):
        """Admin should have org users manage permission."""
        assert has_permission(Permission.ORG_USERS_MANAGE, "admin") is True

    def test_super_user_has_platform_config(self):
        """Super user should have platform config permission."""
        assert has_permission(Permission.PLATFORM_CONFIG, None, "super_user") is True

    def test_basic_user_lacks_platform_config(self):
        """Basic platform user should not have platform config."""
        assert has_permission(Permission.PLATFORM_CONFIG, "admin", "basic") is False
