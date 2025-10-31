"""Monitoramento de portais para detectar mudanças estruturais."""

import hashlib
from typing import Any, Dict, Optional

from scrapy.http import Response

from src.database.redis.cache import RedisCache
from src.utils.logger import get_logger

logger = get_logger(__name__)


class PortalMonitor:
    """Monitora estrutura dos portais para detectar mudanças."""

    def __init__(self):
        self.cache = RedisCache(namespace="portal_monitor")

    def record_response(self, response: Response) -> None:
        """Registra estrutura da resposta para baseline."""
        portal = self._extract_portal_name(response.url)
        structure_hash = self._generate_structure_hash(response)

        baseline = self.cache.get(f"{portal}_baseline")
        if not baseline:
            self.cache.set(f"{portal}_baseline", structure_hash)
            logger.info("baseline_created", portal=portal)

    def detect_changes(self, response: Response) -> bool:
        """Detecta se estrutura do portal mudou."""
        portal = self._extract_portal_name(response.url)
        current_hash = self._generate_structure_hash(response)

        baseline = self.cache.get(f"{portal}_baseline")
        if not baseline:
            return False

        if current_hash != baseline:
            similarity = self._calculate_similarity(current_hash, baseline)
            if similarity < 0.7:
                logger.warning(
                    "portal_structure_changed",
                    portal=portal,
                    similarity=similarity,
                )
                return True

        return False

    def _extract_portal_name(self, url: str) -> str:
        if "esaj" in url:
            return "esaj"
        if "pje" in url:
            return "pje"
        if "eproc" in url:
            return "eproc"
        return "unknown"

    def _generate_structure_hash(self, response: Response) -> str:
        body = response.body[:10000]
        return hashlib.md5(body).hexdigest()

    def _calculate_similarity(self, hash1: str, hash2: str) -> float:
        if hash1 == hash2:
            return 1.0
        matching = sum(c1 == c2 for c1, c2 in zip(hash1, hash2))
        return matching / len(hash1)
