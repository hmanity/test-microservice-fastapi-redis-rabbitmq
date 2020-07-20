from aioredis import Redis


class RedisDB:
    connection_pool: Redis


redis = RedisDB()


async def get_redis() -> Redis:
    return redis.connection_pool


async def get_pipe():
    return redis.connection_pool.pipeline()


async def to_stream(r: Redis, stream: str, msg: str):
    await r.xadd(stream, msg)
