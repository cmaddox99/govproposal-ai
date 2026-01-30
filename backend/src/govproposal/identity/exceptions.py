"""Identity module exceptions."""

from fastapi import HTTPException, status


class AuthenticationError(HTTPException):
    """Raised when authentication fails."""

    def __init__(self, detail: str = "Authentication failed"):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={"code": "authentication_error", "message": detail},
            headers={"WWW-Authenticate": "Bearer"},
        )


class InvalidCredentialsError(AuthenticationError):
    """Raised when credentials are invalid."""

    def __init__(self):
        super().__init__(detail="Invalid email or password")


class TokenExpiredError(AuthenticationError):
    """Raised when a token has expired."""

    def __init__(self):
        super().__init__(detail="Token has expired")


class InvalidTokenError(AuthenticationError):
    """Raised when a token is invalid."""

    def __init__(self):
        super().__init__(detail="Invalid token")


class MFARequiredError(HTTPException):
    """Raised when MFA verification is required."""

    def __init__(self, mfa_token: str):
        super().__init__(
            status_code=status.HTTP_403_FORBIDDEN,
            detail={
                "code": "mfa_required",
                "message": "MFA verification required",
                "mfa_token": mfa_token,
            },
        )


class MFASetupRequiredError(HTTPException):
    """Raised when MFA setup is required before proceeding."""

    def __init__(self):
        super().__init__(
            status_code=status.HTTP_403_FORBIDDEN,
            detail={
                "code": "mfa_setup_required",
                "message": "MFA setup is required for your account",
            },
        )


class InvalidMFACodeError(HTTPException):
    """Raised when MFA code is invalid."""

    def __init__(self):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={"code": "invalid_mfa_code", "message": "Invalid MFA code"},
        )


class ForbiddenError(HTTPException):
    """Raised when user lacks permission for an action."""

    def __init__(self, detail: str = "Access denied"):
        super().__init__(
            status_code=status.HTTP_403_FORBIDDEN,
            detail={"code": "forbidden", "message": detail},
        )


class AccountLockedError(HTTPException):
    """Raised when account is locked due to failed attempts."""

    def __init__(self, locked_until: str | None = None):
        detail = {"code": "account_locked", "message": "Account is temporarily locked"}
        if locked_until:
            detail["locked_until"] = locked_until
        super().__init__(status_code=status.HTTP_423_LOCKED, detail=detail)


class UserNotFoundError(HTTPException):
    """Raised when user is not found."""

    def __init__(self):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"code": "user_not_found", "message": "User not found"},
        )


class OrganizationNotFoundError(HTTPException):
    """Raised when organization is not found."""

    def __init__(self):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"code": "organization_not_found", "message": "Organization not found"},
        )


class UserAlreadyExistsError(HTTPException):
    """Raised when trying to create a user that already exists."""

    def __init__(self):
        super().__init__(
            status_code=status.HTTP_409_CONFLICT,
            detail={"code": "user_exists", "message": "User with this email already exists"},
        )


class OrganizationSlugExistsError(HTTPException):
    """Raised when organization slug is already taken."""

    def __init__(self):
        super().__init__(
            status_code=status.HTTP_409_CONFLICT,
            detail={"code": "slug_exists", "message": "Organization with this slug already exists"},
        )


class NotOrgMemberError(ForbiddenError):
    """Raised when user is not a member of the organization."""

    def __init__(self):
        super().__init__(detail="Not a member of this organization")


class InsufficientPermissionsError(ForbiddenError):
    """Raised when user lacks required permission."""

    def __init__(self, permission: str):
        super().__init__(detail=f"Missing required permission: {permission}")
