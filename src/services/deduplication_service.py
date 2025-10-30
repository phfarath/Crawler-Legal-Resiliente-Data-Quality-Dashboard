"""Serviço de deduplicação cross pipeline."""

from src.database.redis.cache import RedisCache
from src.utils.logger import get_logger

logger = get_logger(__name__)


class DeduplicationService:
    """Mantém registro de hashes conhecidos no Redis."""

    def __init__(self):
        self.cache = RedisCache(namespace="dedup")

    def is_duplicate(self, hash_content: str) -> bool:
        key = f"hash:{hash_content}"
        if self.cache.get(key):
            return True
        self.cache.set(key, True)
        return False

    def reset(self) -> None:
        # Em um cenário real, usaríamos scan + delete
        logger.info("dedup_reset_not_implemented")
