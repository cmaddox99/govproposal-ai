"""Repository layer for notifications."""

from sqlalchemy import func, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from govproposal.notifications.models import Notification


class NotificationRepository:
    """Repository for notification operations."""

    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def create(self, notification: Notification) -> Notification:
        self._session.add(notification)
        await self._session.flush()
        await self._session.refresh(notification)
        return notification

    async def list_for_user(
        self,
        user_id: str,
        unread_only: bool = False,
        limit: int = 50,
        offset: int = 0,
    ) -> tuple[list[Notification], int]:
        query = select(Notification).where(Notification.user_id == user_id)
        if unread_only:
            query = query.where(Notification.is_read.is_(False))

        count_query = select(func.count()).select_from(query.subquery())
        total = (await self._session.execute(count_query)).scalar_one()

        query = query.order_by(Notification.created_at.desc()).limit(limit).offset(offset)
        result = await self._session.execute(query)
        notifications = list(result.scalars().all())
        return notifications, total

    async def mark_as_read(self, notification_id: str, user_id: str) -> bool:
        stmt = (
            update(Notification)
            .where(Notification.id == notification_id, Notification.user_id == user_id)
            .values(is_read=True)
        )
        result = await self._session.execute(stmt)
        return result.rowcount > 0

    async def mark_all_read(self, user_id: str) -> int:
        stmt = (
            update(Notification)
            .where(Notification.user_id == user_id, Notification.is_read.is_(False))
            .values(is_read=True)
        )
        result = await self._session.execute(stmt)
        return result.rowcount

    async def unread_count(self, user_id: str) -> int:
        q = select(func.count()).select_from(Notification).where(
            Notification.user_id == user_id,
            Notification.is_read.is_(False),
        )
        return (await self._session.execute(q)).scalar_one()
