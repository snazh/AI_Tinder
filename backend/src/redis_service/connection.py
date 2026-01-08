"""Basic connection example.
"""

from redis.asyncio import Redis
from src.config import settings

redis_client = Redis(
    host=settings.redis.REDIS_HOST,
    port=settings.redis.REDIS_PORT,
    decode_responses=True,
    username="default",
    password="SLwkrf91GprlSSoq3F54ZWg3tjQJotqS",

)
