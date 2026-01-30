"""Security utilities for authentication."""

import secrets
from datetime import datetime, timedelta, timezone
from hashlib import sha256
from typing import Optional, Dict, List, Tuple, Any

import jwt
import pyotp
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError

from govproposal.config import settings

# Password hasher with OWASP recommended settings
_password_hasher = PasswordHasher(
    time_cost=3,
    memory_cost=65536,
    parallelism=4,
    hash_len=32,
    salt_len=16,
)


def hash_password(password: str) -> str:
    """Hash a password using Argon2id."""
    return _password_hasher.hash(password)


def verify_password(password: str, password_hash: str) -> bool:
    """Verify a password against its hash."""
    try:
        _password_hasher.verify(password_hash, password)
        return True
    except VerifyMismatchError:
        return False


def create_access_token(
    user_id: str,
    expires_delta: Optional[timedelta] = None,
    additional_claims: Optional[Dict[str, Any]] = None,
) -> str:
    """Create a JWT access token."""
    if expires_delta is None:
        expires_delta = timedelta(minutes=settings.jwt_access_token_expire_minutes)

    expire = datetime.now(timezone.utc) + expires_delta
    payload = {
        "sub": user_id,
        "exp": expire,
        "iat": datetime.now(timezone.utc),
        "type": "access",
    }
    if additional_claims:
        payload.update(additional_claims)

    return jwt.encode(payload, settings.jwt_secret_key, algorithm=settings.jwt_algorithm)


def create_refresh_token(
    user_id: str,
    expires_delta: Optional[timedelta] = None,
) -> str:
    """Create a JWT refresh token."""
    if expires_delta is None:
        expires_delta = timedelta(days=settings.jwt_refresh_token_expire_days)

    expire = datetime.now(timezone.utc) + expires_delta
    payload = {
        "sub": user_id,
        "exp": expire,
        "iat": datetime.now(timezone.utc),
        "type": "refresh",
        "jti": secrets.token_hex(16),  # Unique token ID for revocation
    }

    return jwt.encode(payload, settings.jwt_secret_key, algorithm=settings.jwt_algorithm)


def create_mfa_token(user_id: str) -> str:
    """Create a temporary token for MFA verification flow."""
    expire = datetime.now(timezone.utc) + timedelta(minutes=5)
    payload = {
        "sub": user_id,
        "exp": expire,
        "iat": datetime.now(timezone.utc),
        "type": "mfa_pending",
    }
    return jwt.encode(payload, settings.jwt_secret_key, algorithm=settings.jwt_algorithm)


def decode_token(token: str) -> dict:
    """Decode and validate a JWT token."""
    return jwt.decode(
        token,
        settings.jwt_secret_key,
        algorithms=[settings.jwt_algorithm],
    )


def validate_access_token(token: str) -> dict:
    """Validate an access token and return payload."""
    payload = decode_token(token)
    if payload.get("type") != "access":
        raise jwt.InvalidTokenError("Invalid token type")
    return payload


def validate_refresh_token(token: str) -> dict:
    """Validate a refresh token and return payload."""
    payload = decode_token(token)
    if payload.get("type") != "refresh":
        raise jwt.InvalidTokenError("Invalid token type")
    return payload


def validate_mfa_token(token: str) -> dict:
    """Validate an MFA pending token and return payload."""
    payload = decode_token(token)
    if payload.get("type") != "mfa_pending":
        raise jwt.InvalidTokenError("Invalid token type")
    return payload


def generate_reset_token() -> Tuple[str, str]:
    """Generate a password reset token.

    Returns:
        Tuple of (plain_token, token_hash)
    """
    token = secrets.token_urlsafe(32)
    token_hash = sha256(token.encode()).hexdigest()
    return token, token_hash


def verify_reset_token(token: str, token_hash: str) -> bool:
    """Verify a password reset token against its hash."""
    return sha256(token.encode()).hexdigest() == token_hash


def generate_totp_secret() -> str:
    """Generate a new TOTP secret."""
    return pyotp.random_base32()


def get_totp_uri(secret: str, email: str) -> str:
    """Get the OTP Auth URI for QR code generation."""
    totp = pyotp.TOTP(secret)
    return totp.provisioning_uri(name=email, issuer_name=settings.mfa_issuer_name)


def verify_totp(secret: str, code: str) -> bool:
    """Verify a TOTP code.

    Args:
        secret: The user's TOTP secret
        code: The code to verify

    Returns:
        True if valid, False otherwise
    """
    totp = pyotp.TOTP(secret)
    return totp.verify(code, valid_window=1)


def generate_recovery_codes(count: int = 10) -> List[str]:
    """Generate MFA recovery codes.

    Args:
        count: Number of codes to generate

    Returns:
        List of recovery codes in format XXXX-XXXX
    """
    codes = []
    for _ in range(count):
        code = secrets.token_hex(4).upper()
        formatted = f"{code[:4]}-{code[4:]}"
        codes.append(formatted)
    return codes


def hash_recovery_code(code: str) -> str:
    """Hash a recovery code for storage."""
    # Normalize: remove dashes, uppercase
    normalized = code.replace("-", "").upper()
    return sha256(normalized.encode()).hexdigest()


def verify_recovery_code(code: str, code_hash: str) -> bool:
    """Verify a recovery code against its hash."""
    return hash_recovery_code(code) == code_hash


def hash_token(token: str) -> str:
    """Hash a token for storage (session tokens, etc.)."""
    return sha256(token.encode()).hexdigest()
