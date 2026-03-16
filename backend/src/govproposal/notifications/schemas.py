"""Pydantic schemas for notifications module."""

from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class NotificationResponse(BaseModel):
    id: str
    user_id: str
    organization_id: Optional[str]
    type: str
    priority: str
    title: str
    message: str
    is_read: bool
    resource_type: Optional[str]
    resource_id: Optional[str]
    created_at: datetime

    model_config = {"from_attributes": True}


class NotificationListResponse(BaseModel):
    items: list[NotificationResponse]
    total: int
    limit: int
    offset: int


class UnreadCountResponse(BaseModel):
    count: int
