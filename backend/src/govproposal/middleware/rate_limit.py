"""Rate limiting middleware using SlowAPI."""

import logging

from slowapi import Limiter
from slowapi.util import get_remote_address

from govproposal.config import settings

logger = logging.getLogger(__name__)


def _resolve_storage_uri() -> str:
    """Resolve storage URI, falling back to memory if Redis is unreachable."""
    if not settings.redis_url:
        return "memory://"
    try:
        import redis
        r = redis.from_url(settings.redis_url, socket_connect_timeout=2)
        r.ping()
        logger.info("Rate limiter using Redis backend")
        return settings.redis_url
    except Exception:
        logger.warning("Redis unreachable, rate limiter falling back to memory")
        return "memory://"


limiter = Limiter(
    key_func=get_remote_address,
    storage_uri=_resolve_storage_uri(),
    default_limits=["200/minute"],
)
