"""Gerenciador de proxies com rotação."""

import random
from typing import List, Optional

from src.config import settings
from src.utils.logger import get_logger

logger = get_logger(__name__)


class ProxyManager:
    """Gerencia pool de proxies com rotação."""

    def __init__(self):
        self.proxies: List[str] = []
        self.current_index = 0
        self.load_proxies()

    def load_proxies(self) -> None:
        """Carrega proxies do provider configurado."""
        if not settings.proxy_enabled:
            logger.info("proxy_disabled")
            return

        # TODO: Integrar com provedores reais (Luminati, Oxylabs, BrightData)
        # Por enquanto, usa lista estática de exemplo
        self.proxies = self._load_static_proxies()

        if self.proxies:
            logger.info("proxies_loaded", count=len(self.proxies))
        else:
            logger.warning("no_proxies_loaded")

    def _load_static_proxies(self) -> List[str]:
        """Carrega proxies de lista estática (exemplo)."""
        # Em produção, isso viria de uma API externa ou arquivo configurado
        return [
            "http://proxy1.example.com:8080",
            "http://proxy2.example.com:8080",
            "http://proxy3.example.com:8080",
        ]

    def get_proxy(self) -> Optional[str]:
        """Retorna próximo proxy do pool."""
        if not self.proxies:
            return None

        proxy = self.proxies[self.current_index]
        self.current_index = (self.current_index + 1) % len(self.proxies)

        return proxy

    def get_random_proxy(self) -> Optional[str]:
        """Retorna proxy aleatório."""
        if not self.proxies:
            return None

        return random.choice(self.proxies)

    def mark_proxy_failed(self, proxy: str) -> None:
        """Marca proxy como falhado e remove do pool."""
        if proxy in self.proxies:
            self.proxies.remove(proxy)
            logger.warning("proxy_removed", proxy=proxy, remaining=len(self.proxies))

    def reload_proxies(self) -> None:
        """Recarrega lista de proxies."""
        self.load_proxies()
