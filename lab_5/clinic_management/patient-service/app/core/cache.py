from typing import Optional

import redis.asyncio as aioredis
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from starlette.requests import Request
from starlette.responses import Response

from app.core.config import settings

# Global reference to the Redis client for direct invalidation
redis_client: aioredis.Redis | None = None

# Cache prefix for this service
CACHE_PREFIX = "patient-svc"


def cache_key_builder(
    func,
    namespace: Optional[str] = "",
    *,
    request: Optional[Request] = None,
    response: Optional[Response] = None,
    args: tuple = (),
    kwargs: dict = {},
) -> str:
    """Creation of a stable and predictable cache key.

    Format: {prefix}:{namespace}:{path}
    For example: patient-svc:get_doctor:/api/doctors/1
    """
    path = request.url.path if request else "unknown"
    return f"{CACHE_PREFIX}:{namespace}:{path}"


async def init_cache() -> None:
    """Initialization of the Redis client and fastapi-cache backend."""
    global redis_client
    redis_client = aioredis.from_url(
        settings.REDIS_URL,
        encoding="utf-8",
        decode_responses=True,
    )
    FastAPICache.init(
        RedisBackend(redis_client),
        prefix=CACHE_PREFIX,
        key_builder=cache_key_builder,
    )


async def close_cache() -> None:
    """Close the connection with Redis."""
    global redis_client
    if redis_client:
        await redis_client.aclose()
        redis_client = None


async def invalidate_doctor(doctor_id: int) -> None:
    """Invalidate doctor cache by ID."""
    if not redis_client:
        return
    key = f"{CACHE_PREFIX}:get_doctor:/api/doctors/{doctor_id}"
    await redis_client.delete(key)


async def invalidate_patient(patient_id: int) -> None:
    """Invalidate patient cache by ID."""
    if not redis_client:
        return
    key = f"{CACHE_PREFIX}:get_patient:/api/patients/{patient_id}"
    await redis_client.delete(key)
