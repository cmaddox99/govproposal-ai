"""Tests for MFA service."""

import pytest
import sys
from pathlib import Path

# Add src to path for direct imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src"))

# Import directly from security module (doesn't need database)
from govproposal.identity.security import (
    generate_recovery_codes,
    generate_totp_secret,
    get_totp_uri,
    hash_recovery_code,
    verify_recovery_code,
    verify_totp,
)


class TestTOTPGeneration:
    """Test TOTP secret generation."""

    def test_generate_secret_length(self):
        """Generated secret should be 32 chars base32."""
        secret = generate_totp_secret()
        assert len(secret) == 32

    def test_generate_secret_unique(self):
        """Each generated secret should be unique."""
        secrets = [generate_totp_secret() for _ in range(10)]
        assert len(set(secrets)) == 10

    def test_generate_secret_is_base32(self):
        """Generated secret should be valid base32."""
        secret = generate_totp_secret()
        # Base32 uses A-Z and 2-7
        valid_chars = set("ABCDEFGHIJKLMNOPQRSTUVWXYZ234567")
        assert all(c in valid_chars for c in secret)


class TestTOTPUri:
    """Test TOTP provisioning URI generation."""

    def test_uri_contains_email(self):
        """URI should contain the user's email."""
        secret = generate_totp_secret()
        uri = get_totp_uri(secret, "test@example.com")
        assert "test%40example.com" in uri or "test@example.com" in uri

    def test_uri_contains_issuer(self):
        """URI should contain the issuer name."""
        secret = generate_totp_secret()
        uri = get_totp_uri(secret, "test@example.com")
        assert "GovProposalAI" in uri

    def test_uri_is_otpauth_format(self):
        """URI should be in otpauth format."""
        secret = generate_totp_secret()
        uri = get_totp_uri(secret, "test@example.com")
        assert uri.startswith("otpauth://totp/")


class TestTOTPVerification:
    """Test TOTP code verification."""

    def test_verify_valid_code(self):
        """Valid TOTP code should verify successfully."""
        import pyotp

        secret = generate_totp_secret()
        totp = pyotp.TOTP(secret)
        current_code = totp.now()

        assert verify_totp(secret, current_code) is True

    def test_verify_invalid_code(self):
        """Invalid TOTP code should fail verification."""
        secret = generate_totp_secret()
        assert verify_totp(secret, "000000") is False

    def test_verify_wrong_length_code(self):
        """Wrong length code should fail verification."""
        secret = generate_totp_secret()
        assert verify_totp(secret, "12345") is False
        assert verify_totp(secret, "1234567") is False


class TestRecoveryCodes:
    """Test recovery code generation and verification."""

    def test_generate_correct_count(self):
        """Should generate requested number of codes."""
        codes = generate_recovery_codes(10)
        assert len(codes) == 10

        codes = generate_recovery_codes(5)
        assert len(codes) == 5

    def test_codes_are_unique(self):
        """All generated codes should be unique."""
        codes = generate_recovery_codes(10)
        assert len(set(codes)) == 10

    def test_code_format(self):
        """Codes should be in XXXX-XXXX format."""
        codes = generate_recovery_codes(10)
        for code in codes:
            parts = code.split("-")
            assert len(parts) == 2
            assert len(parts[0]) == 4
            assert len(parts[1]) == 4
            # Should be uppercase hex
            assert all(c in "0123456789ABCDEF" for c in parts[0])
            assert all(c in "0123456789ABCDEF" for c in parts[1])

    def test_hash_recovery_code(self):
        """Hashing should produce consistent results."""
        code = "ABCD-1234"
        hash1 = hash_recovery_code(code)
        hash2 = hash_recovery_code(code)
        assert hash1 == hash2
        assert len(hash1) == 64  # SHA-256 hex

    def test_hash_normalizes_case(self):
        """Hashing should normalize case."""
        hash_upper = hash_recovery_code("ABCD-1234")
        hash_lower = hash_recovery_code("abcd-1234")
        assert hash_upper == hash_lower

    def test_hash_normalizes_dashes(self):
        """Hashing should handle codes with or without dashes."""
        hash_with_dash = hash_recovery_code("ABCD-1234")
        hash_without_dash = hash_recovery_code("ABCD1234")
        assert hash_with_dash == hash_without_dash

    def test_verify_recovery_code_valid(self):
        """Valid recovery code should verify."""
        code = "ABCD-1234"
        code_hash = hash_recovery_code(code)
        assert verify_recovery_code(code, code_hash) is True

    def test_verify_recovery_code_invalid(self):
        """Invalid recovery code should not verify."""
        code = "ABCD-1234"
        code_hash = hash_recovery_code(code)
        assert verify_recovery_code("WXYZ-9999", code_hash) is False

    def test_verify_recovery_code_case_insensitive(self):
        """Recovery code verification should be case insensitive."""
        code = "ABCD-1234"
        code_hash = hash_recovery_code(code)
        assert verify_recovery_code("abcd-1234", code_hash) is True
