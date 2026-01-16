import logging

logger = logging.getLogger(__name__)
from redis.asyncio import Redis
from src.config import settings


async def create_redis():
    redis = Redis(
        host=settings.redis.REDIS_HOST,
        port=settings.redis.REDIS_PORT,
        decode_responses=True,
        username="default",
    )
    await redis.ping()
    logger.info("Profile creation started")
    return redis
