"""Event handlers that bridge events to notifications."""

import logging

from govproposal.db.base import async_session_maker
from govproposal.events.bus import Event, event_bus
from govproposal.events.types import EventTypes
from govproposal.notifications.service import NotificationService

logger = logging.getLogger(__name__)


async def _handle_proposal_created(event: Event) -> None:
    """Create notification when a proposal is created."""
    async with async_session_maker() as session:
        svc = NotificationService(session)
        user_id = event.data.get("actor_id")
        if not user_id:
            return
        await svc.create_notification(
            user_id=user_id,
            title="Proposal Created",
            message=f"Proposal '{event.data.get('title', 'Untitled')}' has been created.",
            notification_type="proposal_created",
            organization_id=event.data.get("organization_id"),
            resource_type="proposal",
            resource_id=event.data.get("proposal_id"),
        )
        await session.commit()


async def _handle_proposal_scored(event: Event) -> None:
    """Create notification when a proposal is scored."""
    async with async_session_maker() as session:
        svc = NotificationService(session)
        user_id = event.data.get("actor_id")
        if not user_id:
            return
        score = event.data.get("overall_score", "N/A")
        await svc.create_notification(
            user_id=user_id,
            title="Proposal Scored",
            message=f"Proposal scored with overall score: {score}",
            notification_type="proposal_scored",
            organization_id=event.data.get("organization_id"),
            resource_type="proposal",
            resource_id=event.data.get("proposal_id"),
        )
        await session.commit()


def register_event_handlers() -> None:
    """Register all event handlers. Called at application startup."""
    event_bus.subscribe(EventTypes.PROPOSAL_CREATED, _handle_proposal_created)
    event_bus.subscribe(EventTypes.PROPOSAL_SCORED, _handle_proposal_scored)
    logger.info("Event handlers registered")
