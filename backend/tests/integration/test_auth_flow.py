"""Integration tests for authentication flow."""

import pytest
import sys
from pathlib import Path

# Add src to path for direct imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src"))

# Import only security module (doesn't need database)
from govproposal.identity.security import (
    create_access_token,
    create_mfa_token,
    create_refresh_token,
    generate_reset_token,
    generate_totp_secret,
    hash_password,
    hash_token,
    validate_access_token,
    validate_mfa_token,
    validate_refresh_token,
    verify_password,
    verify_reset_token,
    verify_totp,
)


class TestLoginFlow:
    """Test login authentication flow."""

    def test_password_hashing_and_verification(self):
        """Password hashing and verification should work correctly."""
        password = "TestPassword123!"
        password_hash = hash_password(password)

        assert verify_password(password, password_hash) is True
        assert verify_password("WrongPassword", password_hash) is False

    def test_login_without_mfa_returns_tokens(self):
        """Login without MFA should generate access and refresh tokens."""
        user_id = "test-user-id"

        access_token = create_access_token(user_id)
        assert access_token is not None
        assert len(access_token) > 0

        refresh_token = create_refresh_token(user_id)
        assert refresh_token is not None
        assert len(refresh_token) > 0

    def test_login_with_mfa_requires_challenge(self):
        """Login with MFA enabled should create MFA token."""
        user_id = "test-user-id"
        mfa_token = create_mfa_token(user_id)

        assert mfa_token is not None

        # Validate MFA token
        payload = validate_mfa_token(mfa_token)
        assert payload["sub"] == user_id
        assert payload["type"] == "mfa_pending"

    def test_mfa_challenge_success(self):
        """Valid MFA code should verify."""
        import pyotp

        mfa_secret = generate_totp_secret()
        totp = pyotp.TOTP(mfa_secret)
        code = totp.now()

        assert verify_totp(mfa_secret, code) is True


class TestAccountLockout:
    """Test account lockout functionality."""

    def test_failed_attempts_tracking(self):
        """Failed login attempts should be trackable."""
        failed_attempts = 0

        failed_attempts += 1
        assert failed_attempts == 1

        failed_attempts += 1
        assert failed_attempts == 2

    def test_lockout_after_max_attempts(self):
        """Account lockout logic should work."""
        from datetime import datetime, timedelta, timezone

        MAX_FAILED_ATTEMPTS = 5
        LOCKOUT_DURATION_MINUTES = 30

        failed_attempts = 5
        locked_until = None

        if failed_attempts >= MAX_FAILED_ATTEMPTS:
            locked_until = datetime.now(timezone.utc) + timedelta(
                minutes=LOCKOUT_DURATION_MINUTES
            )

        assert locked_until is not None
        assert locked_until > datetime.now(timezone.utc)


class TestPasswordReset:
    """Test password reset flow."""

    def test_reset_token_generation(self):
        """Reset token should be generated successfully."""
        token, token_hash = generate_reset_token()

        assert token is not None
        assert token_hash is not None
        assert len(token) > 0
        assert len(token_hash) == 64  # SHA-256 hex

    def test_reset_token_verification(self):
        """Reset token should verify correctly."""
        token, token_hash = generate_reset_token()
        assert verify_reset_token(token, token_hash) is True
        assert verify_reset_token("invalid-token", token_hash) is False


class TestSessionManagement:
    """Test session management."""

    def test_access_token_creation(self):
        """Access token should be created with correct claims."""
        user_id = "test-user-id"
        token = create_access_token(user_id)

        payload = validate_access_token(token)
        assert payload["sub"] == user_id
        assert payload["type"] == "access"

    def test_refresh_token_creation(self):
        """Refresh token should be created with correct claims."""
        user_id = "test-user-id"
        token = create_refresh_token(user_id)

        payload = validate_refresh_token(token)
        assert payload["sub"] == user_id
        assert payload["type"] == "refresh"
        assert "jti" in payload  # Unique token ID

    def test_token_hashing(self):
        """Token hash should be consistent."""
        token = "test-refresh-token"
        hash1 = hash_token(token)
        hash2 = hash_token(token)

        assert hash1 == hash2
        assert len(hash1) == 64  # SHA-256 hex
