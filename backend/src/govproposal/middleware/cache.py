"""Simple response caching decorator using Redis."""

import functools
import hashlib
import json
from typing import Callable

from govproposal.db.redis import get_redis


def cache_response(ttl_seconds: int = 60) -> Callable:
    """Cache endpoint responses in Redis. Falls through if Redis unavailable."""

    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        async def wrapper(*args, **kwargs):
            redis = await get_redis()
            if redis is None:
                return await func(*args, **kwargs)

            # Build cache key from function name and arguments
            key_data = f"{func.__module__}.{func.__qualname__}:{json.dumps(kwargs, default=str, sort_keys=True)}"
            cache_key = f"cache:{hashlib.sha256(key_data.encode()).hexdigest()}"

            try:
                cached = await redis.get(cache_key)
                if cached is not None:
                    return json.loads(cached)
            except Exception:
                pass

            result = await func(*args, **kwargs)

            try:
                await redis.setex(cache_key, ttl_seconds, json.dumps(result, default=str))
            except Exception:
                pass

            return result

        return wrapper

    return decorator
