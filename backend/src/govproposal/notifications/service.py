"""Service layer for notifications."""

from sqlalchemy.ext.asyncio import AsyncSession

from govproposal.notifications.models import Notification
from govproposal.notifications.repository import NotificationRepository


class NotificationService:
    """Service for notification operations."""

    def __init__(self, session: AsyncSession) -> None:
        self._session = session
        self._repo = NotificationRepository(session)

    async def create_notification(
        self,
        user_id: str,
        title: str,
        message: str,
        notification_type: str = "system",
        priority: str = "medium",
        organization_id: str | None = None,
        resource_type: str | None = None,
        resource_id: str | None = None,
    ) -> Notification:
        notification = Notification(
            user_id=user_id,
            organization_id=organization_id,
            type=notification_type,
            priority=priority,
            title=title,
            message=message,
            resource_type=resource_type,
            resource_id=resource_id,
        )
        return await self._repo.create(notification)

    async def get_user_notifications(
        self,
        user_id: str,
        unread_only: bool = False,
        limit: int = 50,
        offset: int = 0,
    ) -> tuple[list[Notification], int]:
        return await self._repo.list_for_user(user_id, unread_only, limit, offset)

    async def mark_read(self, notification_id: str, user_id: str) -> bool:
        return await self._repo.mark_as_read(notification_id, user_id)

    async def mark_all_read(self, user_id: str) -> int:
        return await self._repo.mark_all_read(user_id)

    async def get_unread_count(self, user_id: str) -> int:
        return await self._repo.unread_count(user_id)
