"""Camada de cache Redis."""

import json
from datetime import datetime, timedelta
from typing import Any, Optional

from src.database.redis.connection import get_redis_client


class RedisCache:
    """Fornece operações de cache usando Redis."""

    def __init__(self, namespace: str = "crawler"):
        self.client = get_redis_client()
        self.namespace = namespace

    def _key(self, key: str) -> str:
        return f"{self.namespace}:{key}"

    def set(self, key: str, value: Any, ttl: Optional[int] = None) -> None:
        data = json.dumps({"value": value, "stored_at": datetime.utcnow().isoformat()})
        self.client.set(self._key(key), data, ex=ttl)

    def get(self, key: str) -> Optional[Any]:
        data = self.client.get(self._key(key))
        if not data:
            return None
        payload = json.loads(data)
        return payload.get("value")

    def delete(self, key: str) -> None:
        self.client.delete(self._key(key))

    def increment(self, key: str, amount: int = 1) -> int:
        return self.client.incr(self._key(key), amount)

    def set_with_expiration(self, key: str, value: Any, expires_in: timedelta) -> None:
        ttl = int(expires_in.total_seconds())
        self.set(key, value, ttl=ttl)
