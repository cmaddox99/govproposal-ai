"""Service layer for identity operations."""

from datetime import datetime, timedelta, timezone

from sqlalchemy.ext.asyncio import AsyncSession

from govproposal.identity.exceptions import (
    AccountLockedError,
    InvalidCredentialsError,
    InvalidMFACodeError,
    InvalidTokenError,
    MFARequiredError,
    OrganizationNotFoundError,
    TokenExpiredError,
    UserNotFoundError,
)
from govproposal.identity.models import User
from govproposal.identity.repository import (
    MFARecoveryCodeRepository,
    OrganizationRepository,
    PasswordResetRepository,
    UserRepository,
    UserSessionRepository,
)
from govproposal.identity.schemas import (
    MFACompleteResponse,
    MFASetupResponse,
    OrganizationMemberResponse,
    OrganizationResponse,
    RecoveryCodesResponse,
    TokenResponse,
    UserCreate,
    UserResponse,
)
from govproposal.identity.security import (
    create_access_token,
    create_mfa_token,
    create_refresh_token,
    generate_recovery_codes,
    generate_reset_token,
    generate_totp_secret,
    get_totp_uri,
    hash_password,
    hash_recovery_code,
    hash_token,
    validate_mfa_token,
    validate_refresh_token,
    verify_password,
    verify_recovery_code,
    verify_totp,
)


class AuthService:
    """Service for authentication operations."""

    MAX_FAILED_ATTEMPTS = 5
    LOCKOUT_DURATION_MINUTES = 30

    def __init__(self, session: AsyncSession) -> None:
        self._session = session
        self._user_repo = UserRepository(session)
        self._reset_repo = PasswordResetRepository(session)
        self._recovery_repo = MFARecoveryCodeRepository(session)
        self._session_repo = UserSessionRepository(session)

    async def register(self, data: UserCreate) -> UserResponse:
        """Register a new user."""
        password_hash = hash_password(data.password)
        user = await self._user_repo.create(
            email=data.email.lower(),
            password_hash=password_hash,
        )
        return UserResponse.model_validate(user)

    async def login(
        self,
        email: str,
        password: str,
        ip_address: str | None = None,
        user_agent: str | None = None,
    ) -> TokenResponse | str:
        """Authenticate user and return tokens or MFA token.

        Returns:
            TokenResponse if MFA not required, or MFA token string if MFA required
        """
        user = await self._user_repo.get_by_email(email.lower())
        if not user:
            raise InvalidCredentialsError()

        # Check account lockout
        if user.locked_until and user.locked_until > datetime.now(timezone.utc):
            raise AccountLockedError(locked_until=user.locked_until.isoformat())

        # Verify password
        if not verify_password(password, user.password_hash):
            await self._handle_failed_login(user)
            raise InvalidCredentialsError()

        # Reset failed attempts on successful password verification
        user.failed_login_attempts = 0
        user.locked_until = None
        await self._user_repo.update(user)

        # Check if MFA is required
        if user.mfa_enabled:
            mfa_token = create_mfa_token(user.id)
            raise MFARequiredError(mfa_token=mfa_token)

        # Generate tokens
        return await self._create_tokens(user, ip_address, user_agent)

    async def verify_mfa_login(
        self,
        mfa_token: str,
        code: str,
        ip_address: str | None = None,
        user_agent: str | None = None,
    ) -> TokenResponse:
        """Verify MFA code and complete login."""
        try:
            payload = validate_mfa_token(mfa_token)
        except Exception as e:
            raise InvalidTokenError() from e

        user = await self._user_repo.get_by_id(payload["sub"])
        if not user or not user.mfa_secret:
            raise InvalidTokenError()

        if not verify_totp(user.mfa_secret, code):
            raise InvalidMFACodeError()

        return await self._create_tokens(user, ip_address, user_agent)

    async def verify_recovery_code_login(
        self,
        mfa_token: str,
        recovery_code: str,
        ip_address: str | None = None,
        user_agent: str | None = None,
    ) -> TokenResponse:
        """Verify recovery code and complete login."""
        try:
            payload = validate_mfa_token(mfa_token)
        except Exception as e:
            raise InvalidTokenError() from e

        user = await self._user_repo.get_by_id(payload["sub"])
        if not user:
            raise InvalidTokenError()

        # Find and validate recovery code
        codes = await self._recovery_repo.get_unused_codes(user.id)
        for code_record in codes:
            if verify_recovery_code(recovery_code, code_record.code_hash):
                await self._recovery_repo.mark_used(code_record)
                return await self._create_tokens(user, ip_address, user_agent)

        raise InvalidMFACodeError()

    async def _create_tokens(
        self,
        user: User,
        ip_address: str | None = None,
        user_agent: str | None = None,
    ) -> TokenResponse:
        """Create access and refresh tokens."""
        access_token = create_access_token(user.id)
        refresh_token = create_refresh_token(user.id)

        # Track session
        expires_at = datetime.now(timezone.utc) + timedelta(days=7)
        await self._session_repo.create(
            user_id=user.id,
            token_hash=hash_token(refresh_token),
            expires_at=expires_at,
            ip_address=ip_address,
            user_agent=user_agent,
        )

        return TokenResponse(
            access_token=access_token,
            refresh_token=refresh_token,
        )

    async def _handle_failed_login(self, user: User) -> None:
        """Handle failed login attempt."""
        user.failed_login_attempts += 1

        if user.failed_login_attempts >= self.MAX_FAILED_ATTEMPTS:
            user.locked_until = datetime.now(timezone.utc) + timedelta(
                minutes=self.LOCKOUT_DURATION_MINUTES
            )

        await self._user_repo.update(user)

    async def refresh_tokens(
        self, refresh_token: str, ip_address: str | None = None, user_agent: str | None = None
    ) -> TokenResponse:
        """Refresh access and refresh tokens."""
        try:
            payload = validate_refresh_token(refresh_token)
        except Exception as e:
            raise TokenExpiredError() from e

        # Verify session is valid
        token_hash = hash_token(refresh_token)
        session = await self._session_repo.get_by_token_hash(token_hash)
        if not session:
            raise InvalidTokenError()

        user = await self._user_repo.get_by_id(payload["sub"])
        if not user or not user.is_active:
            raise InvalidTokenError()

        # Revoke old session and create new tokens
        await self._session_repo.revoke(session)
        return await self._create_tokens(user, ip_address, user_agent)

    async def request_password_reset(self, email: str) -> str | None:
        """Request password reset.

        Returns:
            The reset token if user exists, None otherwise.
            In production, always return None and send email instead.
        """
        user = await self._user_repo.get_by_email(email.lower())
        if not user:
            return None

        token, token_hash = generate_reset_token()
        expires_at = datetime.now(timezone.utc) + timedelta(hours=1)
        await self._reset_repo.create(user.id, token_hash, expires_at)

        return token

    async def confirm_password_reset(self, token: str, new_password: str) -> None:
        """Confirm password reset."""
        from govproposal.identity.security import verify_reset_token

        # Find valid token
        from hashlib import sha256

        token_hash = sha256(token.encode()).hexdigest()
        reset_token = await self._reset_repo.get_by_hash(token_hash)

        if not reset_token:
            raise InvalidTokenError()

        if reset_token.used_at:
            raise InvalidTokenError()

        if reset_token.expires_at < datetime.now(timezone.utc):
            raise TokenExpiredError()

        # Update password
        user = await self._user_repo.get_by_id(reset_token.user_id)
        if not user:
            raise UserNotFoundError()

        user.password_hash = hash_password(new_password)
        user.last_password_change = datetime.now(timezone.utc)
        user.failed_login_attempts = 0
        user.locked_until = None
        await self._user_repo.update(user)

        # Mark token as used
        await self._reset_repo.mark_used(reset_token)

        # Revoke all sessions
        await self._session_repo.revoke_all_user_sessions(user.id)

    async def change_password(
        self, user: User, current_password: str, new_password: str
    ) -> None:
        """Change user password."""
        if not verify_password(current_password, user.password_hash):
            raise InvalidCredentialsError()

        user.password_hash = hash_password(new_password)
        user.last_password_change = datetime.now(timezone.utc)
        await self._user_repo.update(user)


class MFAService:
    """Service for MFA operations."""

    def __init__(self, session: AsyncSession) -> None:
        self._session = session
        self._user_repo = UserRepository(session)
        self._recovery_repo = MFARecoveryCodeRepository(session)

    async def setup_mfa(self, user: User) -> MFASetupResponse:
        """Initialize MFA setup."""
        secret = generate_totp_secret()
        provisioning_uri = get_totp_uri(secret, user.email)

        # Store secret temporarily (not enabled yet)
        user.mfa_secret = secret
        await self._user_repo.update(user)

        return MFASetupResponse(
            secret=secret,
            provisioning_uri=provisioning_uri,
        )

    async def complete_mfa_setup(self, user: User, code: str) -> MFACompleteResponse:
        """Complete MFA setup after code verification."""
        if not user.mfa_secret:
            raise InvalidMFACodeError()

        if not verify_totp(user.mfa_secret, code):
            raise InvalidMFACodeError()

        # Enable MFA
        user.mfa_enabled = True
        await self._user_repo.update(user)

        # Generate recovery codes
        codes = generate_recovery_codes(10)
        code_hashes = [hash_recovery_code(code) for code in codes]

        # Delete old codes and create new ones
        await self._recovery_repo.delete_user_codes(user.id)
        await self._recovery_repo.create_codes(user.id, code_hashes)

        return MFACompleteResponse(recovery_codes=codes)

    async def disable_mfa(self, user: User, password: str) -> None:
        """Disable MFA for user."""
        if not verify_password(password, user.password_hash):
            raise InvalidCredentialsError()

        user.mfa_enabled = False
        user.mfa_secret = None
        await self._user_repo.update(user)

        # Delete recovery codes
        await self._recovery_repo.delete_user_codes(user.id)

    async def regenerate_recovery_codes(self, user: User) -> RecoveryCodesResponse:
        """Generate new recovery codes (invalidates old ones)."""
        if not user.mfa_enabled:
            raise InvalidMFACodeError()

        codes = generate_recovery_codes(10)
        code_hashes = [hash_recovery_code(code) for code in codes]

        await self._recovery_repo.delete_user_codes(user.id)
        await self._recovery_repo.create_codes(user.id, code_hashes)

        return RecoveryCodesResponse(recovery_codes=codes)


class OrganizationService:
    """Service for organization operations."""

    def __init__(self, session: AsyncSession) -> None:
        self._session = session
        self._org_repo = OrganizationRepository(session)
        self._user_repo = UserRepository(session)

    async def create_organization(
        self, name: str, slug: str, owner_id: str
    ) -> OrganizationResponse:
        """Create a new organization with owner."""
        org = await self._org_repo.create(name=name, slug=slug)
        await self._org_repo.add_member(org.id, owner_id, role="owner")
        return OrganizationResponse.model_validate(org)

    async def get_organization(self, org_id: str) -> OrganizationResponse:
        """Get organization by ID."""
        org = await self._org_repo.get_by_id(org_id)
        if not org:
            raise OrganizationNotFoundError()
        return OrganizationResponse.model_validate(org)

    async def list_user_organizations(self, user_id: str) -> list[OrganizationResponse]:
        """List all organizations a user belongs to."""
        memberships = await self._org_repo.get_user_organizations(user_id)
        orgs = []
        for membership in memberships:
            org = await self._org_repo.get_by_id(membership.organization_id)
            if org:
                orgs.append(OrganizationResponse.model_validate(org))
        return orgs

    async def get_organization_members(
        self, org_id: str, limit: int = 100, offset: int = 0
    ) -> tuple[list[OrganizationMemberResponse], int]:
        """Get organization members."""
        members, total = await self._org_repo.list_members(org_id, limit, offset)
        member_responses = []
        for member in members:
            user = await self._user_repo.get_by_id(member.user_id)
            if user:
                member_responses.append(
                    OrganizationMemberResponse(
                        id=member.id,
                        user_id=member.user_id,
                        email=user.email,
                        role=member.role,
                        invited_at=member.invited_at,
                        joined_at=member.joined_at,
                    )
                )
        return member_responses, total

    async def invite_user(
        self, org_id: str, email: str, role: str = "member"
    ) -> OrganizationMemberResponse:
        """Invite a user to organization."""
        user = await self._user_repo.get_by_email(email.lower())
        if not user:
            raise UserNotFoundError()

        member = await self._org_repo.add_member(org_id, user.id, role)
        return OrganizationMemberResponse(
            id=member.id,
            user_id=user.id,
            email=user.email,
            role=member.role,
            invited_at=member.invited_at,
            joined_at=member.joined_at,
        )

    async def change_member_role(
        self, org_id: str, user_id: str, new_role: str
    ) -> OrganizationMemberResponse:
        """Change a member's role."""
        member = await self._org_repo.update_member_role(org_id, user_id, new_role)
        if not member:
            raise UserNotFoundError()

        user = await self._user_repo.get_by_id(user_id)
        if not user:
            raise UserNotFoundError()

        return OrganizationMemberResponse(
            id=member.id,
            user_id=user_id,
            email=user.email,
            role=member.role,
            invited_at=member.invited_at,
            joined_at=member.joined_at,
        )

    async def remove_member(self, org_id: str, user_id: str) -> bool:
        """Remove a member from organization."""
        return await self._org_repo.remove_member(org_id, user_id)
