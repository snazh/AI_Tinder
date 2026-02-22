import logging
from redis.asyncio import Redis
from src.config import settings

logger = logging.getLogger(__name__)

_redis: Redis | None = None


async def init_redis() -> None:
    global _redis
    _redis = Redis(
        host=settings.redis.REDIS_HOST,
        port=settings.redis.REDIS_PORT,
        decode_responses=True,
    )

    await _redis.ping()
    logger.info("Redis connected successfully")


async def close_redis() -> None:
    global _redis
    if _redis:
        await _redis.close()
        _redis = None


def get_redis() -> Redis:
    if _redis is None:
        raise RuntimeError("Redis not initialized")
    return _redis