import aioredis

from ..core.config import settings
from .redis import redis


async def connect_to_redis():
    redis.connection_pool = await aioredis.create_redis_pool(settings.redis_dsn, timeout=settings.timeout)
