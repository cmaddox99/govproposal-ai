"""MFA-specific service functionality.

This module is imported by the main service module but provides
a clear separation of MFA concerns.
"""

from sqlalchemy.ext.asyncio import AsyncSession

from govproposal.identity.exceptions import InvalidMFACodeError
from govproposal.identity.models import User
from govproposal.identity.repository import MFARecoveryCodeRepository, UserRepository
from govproposal.identity.schemas import (
    MFACompleteResponse,
    MFASetupResponse,
    RecoveryCodesResponse,
)
from govproposal.identity.security import (
    generate_recovery_codes,
    generate_totp_secret,
    get_totp_uri,
    hash_recovery_code,
    verify_password,
    verify_recovery_code,
    verify_totp,
)


class MFAService:
    """Service for MFA operations."""

    def __init__(self, session: AsyncSession) -> None:
        self._session = session
        self._user_repo = UserRepository(session)
        self._recovery_repo = MFARecoveryCodeRepository(session)

    async def setup_mfa(self, user: User) -> MFASetupResponse:
        """Initialize MFA setup.

        Generates a new TOTP secret and provisioning URI for the user.
        The secret is stored but MFA is not yet enabled.

        Args:
            user: The user to set up MFA for

        Returns:
            MFASetupResponse with secret and provisioning URI
        """
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
        """Complete MFA setup after code verification.

        Verifies the TOTP code, enables MFA, and generates recovery codes.

        Args:
            user: The user completing MFA setup
            code: The TOTP code from authenticator app

        Returns:
            MFACompleteResponse with recovery codes

        Raises:
            InvalidMFACodeError: If code is invalid or no secret is set
        """
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

    async def verify_code(self, user: User, code: str) -> bool:
        """Verify a TOTP code for the user.

        Args:
            user: The user to verify code for
            code: The TOTP code to verify

        Returns:
            True if code is valid, False otherwise
        """
        if not user.mfa_secret:
            return False
        return verify_totp(user.mfa_secret, code)

    async def verify_recovery_code(self, user: User, recovery_code: str) -> bool:
        """Verify and consume a recovery code.

        Args:
            user: The user to verify code for
            recovery_code: The recovery code to verify

        Returns:
            True if code was valid and consumed, False otherwise
        """
        codes = await self._recovery_repo.get_unused_codes(user.id)
        for code_record in codes:
            if verify_recovery_code(recovery_code, code_record.code_hash):
                await self._recovery_repo.mark_used(code_record)
                return True
        return False

    async def disable_mfa(self, user: User, password: str) -> None:
        """Disable MFA for user.

        Args:
            user: The user to disable MFA for
            password: The user's password for verification

        Raises:
            InvalidCredentialsError: If password is incorrect
        """
        from govproposal.identity.exceptions import InvalidCredentialsError

        if not verify_password(password, user.password_hash):
            raise InvalidCredentialsError()

        user.mfa_enabled = False
        user.mfa_secret = None
        await self._user_repo.update(user)

        # Delete recovery codes
        await self._recovery_repo.delete_user_codes(user.id)

    async def regenerate_recovery_codes(self, user: User) -> RecoveryCodesResponse:
        """Generate new recovery codes (invalidates old ones).

        Args:
            user: The user to regenerate codes for

        Returns:
            RecoveryCodesResponse with new codes

        Raises:
            InvalidMFACodeError: If MFA is not enabled
        """
        if not user.mfa_enabled:
            raise InvalidMFACodeError()

        codes = generate_recovery_codes(10)
        code_hashes = [hash_recovery_code(code) for code in codes]

        await self._recovery_repo.delete_user_codes(user.id)
        await self._recovery_repo.create_codes(user.id, code_hashes)

        return RecoveryCodesResponse(recovery_codes=codes)

    async def get_remaining_recovery_codes_count(self, user: User) -> int:
        """Get count of remaining unused recovery codes.

        Args:
            user: The user to check

        Returns:
            Number of unused recovery codes
        """
        codes = await self._recovery_repo.get_unused_codes(user.id)
        return len(codes)
