"""Notifications API router."""

from typing import Annotated

from fastapi import APIRouter, Depends, Query

from govproposal.identity.dependencies import CurrentUser, DbSession
from govproposal.notifications.schemas import (
    NotificationListResponse,
    NotificationResponse,
    UnreadCountResponse,
)
from govproposal.notifications.service import NotificationService

router = APIRouter(prefix="/api/v1/notifications", tags=["notifications"])


def get_notification_service(session: DbSession) -> NotificationService:
    return NotificationService(session)


NotifSvc = Annotated[NotificationService, Depends(get_notification_service)]


@router.get("", response_model=NotificationListResponse)
async def list_notifications(
    current_user: CurrentUser,
    service: NotifSvc,
    unread_only: Annotated[bool, Query()] = False,
    limit: Annotated[int, Query(ge=1, le=100)] = 50,
    offset: Annotated[int, Query(ge=0)] = 0,
) -> NotificationListResponse:
    """Get notifications for current user."""
    items, total = await service.get_user_notifications(
        current_user.id, unread_only, limit, offset
    )
    return NotificationListResponse(
        items=[NotificationResponse.model_validate(n) for n in items],
        total=total, limit=limit, offset=offset,
    )


@router.get("/unread-count", response_model=UnreadCountResponse)
async def get_unread_count(
    current_user: CurrentUser,
    service: NotifSvc,
) -> UnreadCountResponse:
    """Get unread notification count."""
    count = await service.get_unread_count(current_user.id)
    return UnreadCountResponse(count=count)


@router.put("/{notification_id}/read")
async def mark_notification_read(
    notification_id: str,
    current_user: CurrentUser,
    service: NotifSvc,
) -> dict:
    """Mark a notification as read."""
    await service.mark_read(notification_id, current_user.id)
    return {"status": "ok"}


@router.put("/read-all")
async def mark_all_notifications_read(
    current_user: CurrentUser,
    service: NotifSvc,
) -> dict:
    """Mark all notifications as read."""
    count = await service.mark_all_read(current_user.id)
    return {"status": "ok", "marked_read": count}
