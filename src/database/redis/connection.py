"""Conexão com Redis."""

from functools import lru_cache

import redis

from src.config import settings


@lru_cache()
def get_redis_client() -> redis.Redis:
    return redis.from_url(
        settings.redis_uri,
        max_connections=settings.redis_max_connections,
        decode_responses=True,
    )
