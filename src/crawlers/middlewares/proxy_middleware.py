"""Middleware para rotação de proxies."""

from typing import Optional

from scrapy import Request
from scrapy.http import Response

from src.config import settings
from src.utils.logger import get_logger
from src.utils.proxy_manager import ProxyManager

logger = get_logger(__name__)


class ProxyRotationMiddleware:
    """Rotaciona proxies para cada requisição."""

    def __init__(self):
        self.enabled = settings.proxy_enabled
        self.proxy_manager = ProxyManager()

    def process_request(self, request: Request, spider):  # type: ignore[override]
        if not self.enabled:
            return None

        proxy = self.proxy_manager.get_proxy()
        if proxy:
            request.meta["proxy"] = proxy
            logger.debug("proxy_assigned", proxy=proxy)
        return None

    def process_exception(self, request: Request, exception, spider):  # type: ignore[override]
        proxy: Optional[str] = request.meta.get("proxy")
        if proxy:
            self.proxy_manager.mark_proxy_failed(proxy)
            logger.warning("proxy_marked_failed", proxy=proxy, error=str(exception))
        return None
