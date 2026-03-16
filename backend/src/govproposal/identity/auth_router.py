"""Authentication API router."""

from typing import Annotated

from fastapi import APIRouter, Depends, Header, Request, status

from govproposal.middleware.rate_limit import limiter
from govproposal.identity.dependencies import (
    AuthSvc,
    CurrentUser,
    DbSession,
    MFASvc,
    get_auth_service,
    get_mfa_service,
)
from govproposal.security.service import AuditService
from govproposal.identity.schemas import (
    LoginRequest,
    MFAChallengeRequest,
    MFACompleteResponse,
    MFADisableRequest,
    MFASetupResponse,
    MFAVerifyRequest,
    MessageResponse,
    PasswordChangeRequest,
    PasswordResetConfirm,
    PasswordResetRequest,
    RecoveryCodeRequest,
    RecoveryCodesResponse,
    RefreshTokenRequest,
    TokenResponse,
    UserCreate,
    UserResponse,
)

router = APIRouter(prefix="/api/v1/auth", tags=["auth"])


def _get_client_ip(request: Request) -> str | None:
    """Extract client IP from request."""
    forwarded = request.headers.get("x-forwarded-for")
    if forwarded:
        return forwarded.split(",")[0].strip()
    return request.client.host if request.client else None


def _get_user_agent(request: Request) -> str | None:
    """Extract user agent from request."""
    return request.headers.get("user-agent")


@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
@limiter.limit("5/minute")
async def register(
    data: UserCreate,
    service: AuthSvc,
    session: DbSession,
    request: Request,
) -> UserResponse:
    """Register a new user account."""
    result = await service.register(data)

    audit = AuditService(session)
    await audit.log_event(
        event_type="user_registered",
        action="New user registered",
        actor_id=result.id,
        actor_email=result.email,
        resource_type="user",
        resource_id=result.id,
        ip_address=_get_client_ip(request),
    )

    return result


@router.post("/login", response_model=TokenResponse)
@limiter.limit("10/minute")
async def login(
    data: LoginRequest,
    service: AuthSvc,
    request: Request,
) -> TokenResponse:
    """Authenticate user and get access tokens.

    If MFA is enabled, returns 403 with mfa_token for use with /mfa/challenge.
    """
    ip_address = _get_client_ip(request)
    user_agent = _get_user_agent(request)

    result = await service.login(
        email=data.email,
        password=data.password,
        ip_address=ip_address,
        user_agent=user_agent,
    )

    # If MFA is required, MFARequiredError will be raised by service
    # which returns 403 with mfa_token
    return result


@router.post("/refresh", response_model=TokenResponse)
async def refresh_tokens(
    data: RefreshTokenRequest,
    service: AuthSvc,
    request: Request,
) -> TokenResponse:
    """Refresh access and refresh tokens."""
    ip_address = _get_client_ip(request)
    user_agent = _get_user_agent(request)

    return await service.refresh_tokens(
        refresh_token=data.refresh_token,
        ip_address=ip_address,
        user_agent=user_agent,
    )


@router.post("/password-reset/request", response_model=MessageResponse)
@limiter.limit("3/minute")
async def request_password_reset(
    data: PasswordResetRequest,
    service: AuthSvc,
    request: Request,
) -> MessageResponse:
    """Request a password reset email."""
    await service.request_password_reset(data.email)
    return MessageResponse(
        message="If an account exists with this email, a reset link will be sent"
    )


@router.post("/password-reset/confirm", response_model=MessageResponse)
async def confirm_password_reset(
    data: PasswordResetConfirm,
    service: AuthSvc,
) -> MessageResponse:
    """Confirm password reset with token."""
    await service.confirm_password_reset(data.token, data.new_password)
    return MessageResponse(message="Password reset successfully")


@router.post("/password/change", response_model=MessageResponse)
async def change_password(
    data: PasswordChangeRequest,
    service: AuthSvc,
    current_user: CurrentUser,
    session: DbSession,
    request: Request,
) -> MessageResponse:
    """Change current user's password."""
    await service.change_password(
        user=current_user,
        current_password=data.current_password,
        new_password=data.new_password,
    )

    audit = AuditService(session)
    await audit.log_event(
        event_type="password_changed",
        action="User password changed",
        actor_id=current_user.id,
        actor_email=current_user.email,
        resource_type="user",
        resource_id=current_user.id,
        ip_address=_get_client_ip(request),
    )

    return MessageResponse(message="Password changed successfully")


@router.get("/me", response_model=UserResponse)
async def get_current_user_info(current_user: CurrentUser) -> UserResponse:
    """Get current user information."""
    return UserResponse.model_validate(current_user)


# MFA Endpoints


@router.post("/mfa/setup", response_model=MFASetupResponse)
async def setup_mfa(
    current_user: CurrentUser,
    service: MFASvc,
) -> MFASetupResponse:
    """Initialize MFA setup. Returns QR code URI."""
    return await service.setup_mfa(current_user)


@router.post("/mfa/verify", response_model=MFACompleteResponse)
async def verify_mfa_setup(
    data: MFAVerifyRequest,
    current_user: CurrentUser,
    service: MFASvc,
) -> MFACompleteResponse:
    """Verify code and complete MFA setup. Returns recovery codes."""
    return await service.complete_mfa_setup(current_user, data.code)


@router.post("/mfa/challenge", response_model=TokenResponse)
async def mfa_challenge(
    data: MFAChallengeRequest,
    service: AuthSvc,
    request: Request,
) -> TokenResponse:
    """Verify MFA code during login."""
    ip_address = _get_client_ip(request)
    user_agent = _get_user_agent(request)

    return await service.verify_mfa_login(
        mfa_token=data.mfa_token,
        code=data.code,
        ip_address=ip_address,
        user_agent=user_agent,
    )


@router.post("/mfa/recovery", response_model=TokenResponse)
async def use_recovery_code(
    data: RecoveryCodeRequest,
    service: AuthSvc,
    request: Request,
) -> TokenResponse:
    """Use recovery code for login."""
    ip_address = _get_client_ip(request)
    user_agent = _get_user_agent(request)

    return await service.verify_recovery_code_login(
        mfa_token=data.mfa_token,
        recovery_code=data.recovery_code,
        ip_address=ip_address,
        user_agent=user_agent,
    )


@router.post("/mfa/recovery-codes/regenerate", response_model=RecoveryCodesResponse)
async def regenerate_recovery_codes(
    current_user: CurrentUser,
    service: MFASvc,
) -> RecoveryCodesResponse:
    """Generate new recovery codes (invalidates old ones)."""
    return await service.regenerate_recovery_codes(current_user)


@router.post("/mfa/disable", response_model=MessageResponse)
async def disable_mfa(
    data: MFADisableRequest,
    current_user: CurrentUser,
    service: MFASvc,
    session: DbSession,
    request: Request,
) -> MessageResponse:
    """Disable MFA for current user."""
    await service.disable_mfa(current_user, data.password)

    audit = AuditService(session)
    await audit.log_event(
        event_type="mfa_disabled",
        action="MFA disabled",
        actor_id=current_user.id,
        actor_email=current_user.email,
        resource_type="user",
        resource_id=current_user.id,
        ip_address=_get_client_ip(request),
    )

    return MessageResponse(message="MFA disabled successfully")
