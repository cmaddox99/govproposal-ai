"""Pydantic schemas for identity module."""

from datetime import datetime

from pydantic import BaseModel, EmailStr, Field


# User schemas
class UserCreate(BaseModel):
    """Schema for user registration."""

    email: EmailStr
    password: str = Field(..., min_length=8, max_length=128)


class UserResponse(BaseModel):
    """Schema for user response."""

    id: str
    email: str
    is_active: bool
    is_verified: bool
    mfa_enabled: bool
    mfa_required: bool
    platform_role: str
    created_at: datetime

    model_config = {"from_attributes": True}


class UserWithOrgResponse(UserResponse):
    """Schema for user with organization membership info."""

    org_role: str | None = None
    organization_id: str | None = None


# Auth schemas
class LoginRequest(BaseModel):
    """Schema for login request."""

    email: EmailStr
    password: str


class TokenResponse(BaseModel):
    """Schema for token response."""

    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class RefreshTokenRequest(BaseModel):
    """Schema for refresh token request."""

    refresh_token: str


class PasswordResetRequest(BaseModel):
    """Schema for password reset request."""

    email: EmailStr


class PasswordResetConfirm(BaseModel):
    """Schema for password reset confirmation."""

    token: str
    new_password: str = Field(..., min_length=8, max_length=128)


class PasswordChangeRequest(BaseModel):
    """Schema for password change."""

    current_password: str
    new_password: str = Field(..., min_length=8, max_length=128)


# MFA schemas
class MFASetupResponse(BaseModel):
    """Schema for MFA setup response."""

    secret: str
    provisioning_uri: str
    qr_code_base64: str | None = None


class MFAVerifyRequest(BaseModel):
    """Schema for MFA verification."""

    code: str = Field(..., min_length=6, max_length=6)


class MFACompleteResponse(BaseModel):
    """Schema for MFA setup completion."""

    recovery_codes: list[str]
    message: str = "MFA enabled successfully"


class MFAChallengeRequest(BaseModel):
    """Schema for MFA challenge during login."""

    mfa_token: str
    code: str = Field(..., min_length=6, max_length=6)


class RecoveryCodeRequest(BaseModel):
    """Schema for recovery code login."""

    mfa_token: str
    recovery_code: str


class RecoveryCodesResponse(BaseModel):
    """Schema for recovery codes response."""

    recovery_codes: list[str]
    message: str = "Recovery codes generated"


class MFADisableRequest(BaseModel):
    """Schema for disabling MFA."""

    password: str


# Organization schemas
class OrganizationCreate(BaseModel):
    """Schema for organization creation."""

    name: str = Field(..., min_length=1, max_length=255)
    slug: str = Field(..., min_length=1, max_length=100, pattern=r"^[a-z0-9-]+$")


class OrganizationResponse(BaseModel):
    """Schema for organization response."""

    id: str
    name: str
    slug: str
    is_active: bool
    contact_email: str | None = None
    phone: str | None = None
    address: str | None = None
    uei_number: str | None = None
    cage_code: str | None = None
    duns_number: str | None = None
    naics_codes: list[str] | None = None
    created_at: datetime

    model_config = {"from_attributes": True}


class OrganizationUpdate(BaseModel):
    """Schema for organization update."""

    name: str | None = None
    contact_email: str | None = None
    phone: str | None = None
    address: str | None = None
    uei_number: str | None = None
    cage_code: str | None = None
    duns_number: str | None = None
    naics_codes: list[str] | None = None


class OrganizationMemberResponse(BaseModel):
    """Schema for organization member response."""

    id: str
    user_id: str
    email: str
    role: str
    invited_at: datetime
    joined_at: datetime | None

    model_config = {"from_attributes": True}


# Admin schemas
class InviteUserRequest(BaseModel):
    """Schema for inviting a user to organization."""

    email: EmailStr
    role: str = Field(default="member", pattern=r"^(member|admin)$")


class InviteResponse(BaseModel):
    """Schema for invite response."""

    id: str
    email: str
    role: str
    invited_at: datetime
    message: str = "User invited successfully"


class RoleChangeRequest(BaseModel):
    """Schema for changing user role."""

    role: str = Field(..., pattern=r"^(member|admin|owner)$")


class OrgUserResponse(BaseModel):
    """Schema for organization user response."""

    id: str
    user_id: str
    email: str
    role: str
    is_active: bool
    mfa_enabled: bool
    invited_at: datetime
    joined_at: datetime | None

    model_config = {"from_attributes": True}


# Platform admin schemas
class TenantResponse(BaseModel):
    """Schema for tenant (organization) response."""

    id: str
    name: str
    slug: str
    is_active: bool
    member_count: int
    created_at: datetime


class TenantStatusRequest(BaseModel):
    """Schema for updating tenant status."""

    is_active: bool


class FeatureToggleResponse(BaseModel):
    """Schema for feature toggle response."""

    feature: str
    enabled: bool
    description: str | None = None


class FeatureToggleRequest(BaseModel):
    """Schema for updating feature toggle."""

    enabled: bool


class FeatureTogglesResponse(BaseModel):
    """Schema for all feature toggles."""

    features: list[FeatureToggleResponse]


# Session schemas
class SessionResponse(BaseModel):
    """Schema for session response."""

    id: str
    ip_address: str | None
    user_agent: str | None
    created_at: datetime
    expires_at: datetime
    is_current: bool = False


class SessionListResponse(BaseModel):
    """Schema for session list response."""

    sessions: list[SessionResponse]


# Generic response
class MessageResponse(BaseModel):
    """Generic message response."""

    message: str
