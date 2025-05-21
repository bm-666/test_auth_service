import redis.asyncio as redis

from config.settings import settings

# Инициализация Redis-клиента с асинхронной поддержкой.
redis_client = redis.from_url(
    url=settings.get_redis_connect_url(), decode_responses=True
)
