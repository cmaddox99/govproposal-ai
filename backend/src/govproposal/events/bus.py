"""In-process event bus."""

import asyncio
import logging
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Callable, Coroutine

logger = logging.getLogger(__name__)


@dataclass
class Event:
    """Domain event."""
    type: str
    data: dict[str, Any] = field(default_factory=dict)
    timestamp: datetime = field(default_factory=lambda: datetime.now(timezone.utc))


class EventBus:
    """Simple in-process pub/sub event bus.

    Designed so it can be swapped for Redis Streams later.
    """

    def __init__(self) -> None:
        self._handlers: dict[str, list[Callable[[Event], Coroutine]]] = {}

    def subscribe(self, event_type: str, handler: Callable[[Event], Coroutine]) -> None:
        """Register a handler for an event type."""
        self._handlers.setdefault(event_type, []).append(handler)

    async def publish(self, event: Event) -> None:
        """Publish an event to all subscribed handlers."""
        handlers = self._handlers.get(event.type, [])
        for handler in handlers:
            try:
                await handler(event)
            except Exception:
                logger.exception("Error in event handler for %s", event.type)


# Singleton
event_bus = EventBus()
