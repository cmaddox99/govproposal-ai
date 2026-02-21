"""Repository layer for identity models."""

from datetime import datetime, timezone

from sqlalchemy import func, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from govproposal.identity.exceptions import (
    OrganizationSlugExistsError,
    UserAlreadyExistsError,
)
from govproposal.identity.models import (
    MFARecoveryCode,
    Organization,
    OrganizationMember,
    PasswordResetToken,
    User,
    UserSession,
)


class UserRepository:
    """Repository for User operations."""

    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def create(self, email: str, password_hash: str) -> User:
        """Create a new user."""
        user = User(email=email, password_hash=password_hash)
        self._session.add(user)
        try:
            await self._session.flush()
            await self._session.refresh(user)
            return user
        except IntegrityError as e:
            await self._session.rollback()
            if "users_email" in str(e):
                raise UserAlreadyExistsError() from e
            raise

    async def get_by_id(self, user_id: str) -> User | None:
        """Get user by ID."""
        result = await self._session.execute(select(User).where(User.id == user_id))
        return result.scalar_one_or_none()

    async def get_by_email(self, email: str) -> User | None:
        """Get user by email."""
        result = await self._session.execute(
            select(User).where(User.email == email.lower())
        )
        return result.scalar_one_or_none()

    async def update(self, user: User) -> User:
        """Update a user."""
        await self._session.flush()
        await self._session.refresh(user)
        return user

    async def exists_by_email(self, email: str) -> bool:
        """Check if user exists by email."""
        result = await self._session.execute(
            select(func.count()).select_from(User).where(User.email == email.lower())
        )
        return result.scalar_one() > 0


class OrganizationRepository:
    """Repository for Organization operations."""

    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def create(self, name: str, slug: str) -> Organization:
        """Create a new organization."""
        org = Organization(name=name, slug=slug.lower())
        self._session.add(org)
        try:
            await self._session.flush()
            await self._session.refresh(org)
            return org
        except IntegrityError as e:
            await self._session.rollback()
            if "organizations_slug_key" in str(e):
                raise OrganizationSlugExistsError() from e
            raise

    async def get_by_id(self, org_id: str) -> Organization | None:
        """Get organization by ID."""
        result = await self._session.execute(
            select(Organization).where(Organization.id == org_id)
        )
        return result.scalar_one_or_none()

    async def get_by_slug(self, slug: str) -> Organization | None:
        """Get organization by slug."""
        result = await self._session.execute(
            select(Organization).where(Organization.slug == slug.lower())
        )
        return result.scalar_one_or_none()

    async def list_all(
        self, limit: int = 100, offset: int = 0
    ) -> tuple[list[Organization], int]:
        """List all organizations with pagination."""
        count_query = select(func.count()).select_from(Organization)
        count_result = await self._session.execute(count_query)
        total = count_result.scalar_one()

        query = (
            select(Organization)
            .order_by(Organization.created_at.desc())
            .limit(limit)
            .offset(offset)
        )
        result = await self._session.execute(query)
        orgs = list(result.scalars().all())

        return orgs, total

    async def update(self, org: Organization) -> Organization:
        """Update an organization."""
        await self._session.flush()
        await self._session.refresh(org)
        return org

    async def get_member(self, org_id: str, user_id: str) -> OrganizationMember | None:
        """Get organization member."""
        result = await self._session.execute(
            select(OrganizationMember).where(
                OrganizationMember.organization_id == org_id,
                OrganizationMember.user_id == user_id,
            )
        )
        return result.scalar_one_or_none()

    async def add_member(
        self, org_id: str, user_id: str, role: str = "member"
    ) -> OrganizationMember:
        """Add a member to organization."""
        member = OrganizationMember(
            organization_id=org_id,
            user_id=user_id,
            role=role,
            joined_at=datetime.now(timezone.utc),
        )
        self._session.add(member)
        await self._session.flush()
        await self._session.refresh(member)
        return member

    async def update_member_role(
        self, org_id: str, user_id: str, role: str
    ) -> OrganizationMember | None:
        """Update member's role."""
        member = await self.get_member(org_id, user_id)
        if member:
            member.role = role
            await self._session.flush()
            await self._session.refresh(member)
        return member

    async def remove_member(self, org_id: str, user_id: str) -> bool:
        """Remove member from organization."""
        member = await self.get_member(org_id, user_id)
        if member:
            await self._session.delete(member)
            await self._session.flush()
            return True
        return False

    async def list_members(
        self, org_id: str, limit: int = 100, offset: int = 0
    ) -> tuple[list[OrganizationMember], int]:
        """List organization members."""
        count_query = (
            select(func.count())
            .select_from(OrganizationMember)
            .where(OrganizationMember.organization_id == org_id)
        )
        count_result = await self._session.execute(count_query)
        total = count_result.scalar_one()

        query = (
            select(OrganizationMember)
            .where(OrganizationMember.organization_id == org_id)
            .order_by(OrganizationMember.invited_at.desc())
            .limit(limit)
            .offset(offset)
        )
        result = await self._session.execute(query)
        members = list(result.scalars().all())

        return members, total

    async def get_user_organizations(self, user_id: str) -> list[OrganizationMember]:
        """Get all organizations a user belongs to."""
        query = select(OrganizationMember).where(
            OrganizationMember.user_id == user_id
        )
        result = await self._session.execute(query)
        return list(result.scalars().all())

    async def get_member_count(self, org_id: str) -> int:
        """Get count of members in organization."""
        result = await self._session.execute(
            select(func.count())
            .select_from(OrganizationMember)
            .where(OrganizationMember.organization_id == org_id)
        )
        return result.scalar_one()


class PasswordResetRepository:
    """Repository for password reset tokens."""

    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def create(
        self, user_id: str, token_hash: str, expires_at: datetime
    ) -> PasswordResetToken:
        """Create a password reset token."""
        token = PasswordResetToken(
            user_id=user_id,
            token_hash=token_hash,
            expires_at=expires_at,
        )
        self._session.add(token)
        await self._session.flush()
        await self._session.refresh(token)
        return token

    async def get_by_hash(self, token_hash: str) -> PasswordResetToken | None:
        """Get token by hash."""
        result = await self._session.execute(
            select(PasswordResetToken).where(
                PasswordResetToken.token_hash == token_hash
            )
        )
        return result.scalar_one_or_none()

    async def mark_used(self, token: PasswordResetToken) -> PasswordResetToken:
        """Mark token as used."""
        token.used_at = datetime.now(timezone.utc)
        await self._session.flush()
        await self._session.refresh(token)
        return token


class MFARecoveryCodeRepository:
    """Repository for MFA recovery codes."""

    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def create_codes(
        self, user_id: str, code_hashes: list[str]
    ) -> list[MFARecoveryCode]:
        """Create recovery codes for a user."""
        codes = [
            MFARecoveryCode(user_id=user_id, code_hash=code_hash)
            for code_hash in code_hashes
        ]
        self._session.add_all(codes)
        await self._session.flush()
        for code in codes:
            await self._session.refresh(code)
        return codes

    async def delete_user_codes(self, user_id: str) -> int:
        """Delete all recovery codes for a user."""
        result = await self._session.execute(
            select(MFARecoveryCode).where(MFARecoveryCode.user_id == user_id)
        )
        codes = result.scalars().all()
        for code in codes:
            await self._session.delete(code)
        await self._session.flush()
        return len(codes)

    async def get_unused_codes(self, user_id: str) -> list[MFARecoveryCode]:
        """Get unused recovery codes for a user."""
        result = await self._session.execute(
            select(MFARecoveryCode).where(
                MFARecoveryCode.user_id == user_id,
                MFARecoveryCode.used_at.is_(None),
            )
        )
        return list(result.scalars().all())

    async def mark_used(self, code: MFARecoveryCode) -> MFARecoveryCode:
        """Mark a recovery code as used."""
        code.used_at = datetime.now(timezone.utc)
        await self._session.flush()
        await self._session.refresh(code)
        return code


class UserSessionRepository:
    """Repository for user sessions."""

    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def create(
        self,
        user_id: str,
        token_hash: str,
        expires_at: datetime,
        ip_address: str | None = None,
        user_agent: str | None = None,
    ) -> UserSession:
        """Create a new session."""
        session = UserSession(
            user_id=user_id,
            token_hash=token_hash,
            expires_at=expires_at,
            ip_address=ip_address,
            user_agent=user_agent,
        )
        self._session.add(session)
        await self._session.flush()
        await self._session.refresh(session)
        return session

    async def get_by_token_hash(self, token_hash: str) -> UserSession | None:
        """Get session by token hash."""
        result = await self._session.execute(
            select(UserSession).where(
                UserSession.token_hash == token_hash,
                UserSession.revoked_at.is_(None),
            )
        )
        return result.scalar_one_or_none()

    async def get_user_sessions(
        self, user_id: str, include_revoked: bool = False
    ) -> list[UserSession]:
        """Get all sessions for a user."""
        query = select(UserSession).where(UserSession.user_id == user_id)
        if not include_revoked:
            query = query.where(UserSession.revoked_at.is_(None))
        query = query.order_by(UserSession.created_at.desc())
        result = await self._session.execute(query)
        return list(result.scalars().all())

    async def revoke(self, session: UserSession) -> UserSession:
        """Revoke a session."""
        session.revoked_at = datetime.now(timezone.utc)
        await self._session.flush()
        await self._session.refresh(session)
        return session

    async def revoke_all_user_sessions(
        self, user_id: str, except_session_id: str | None = None
    ) -> int:
        """Revoke all sessions for a user."""
        query = select(UserSession).where(
            UserSession.user_id == user_id,
            UserSession.revoked_at.is_(None),
        )
        if except_session_id:
            query = query.where(UserSession.id != except_session_id)

        result = await self._session.execute(query)
        sessions = result.scalars().all()
        now = datetime.now(timezone.utc)
        for sess in sessions:
            sess.revoked_at = now
        await self._session.flush()
        return len(sessions)
