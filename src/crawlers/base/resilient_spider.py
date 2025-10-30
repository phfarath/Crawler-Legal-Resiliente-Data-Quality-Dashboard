"""Spider base com mecanismos de resiliência."""

from __future__ import annotations

import random
from abc import abstractmethod
from typing import Any, Dict, Iterable, List

import scrapy
from scrapy import Request
from scrapy.exceptions import IgnoreRequest
from tenacity import retry, retry_if_exception_type, stop_after_attempt, wait_exponential

from src.config import settings
from src.services.alert_service import AlertService
from src.services.portal_monitor import PortalMonitor
from src.utils.logger import get_logger
from src.utils.metrics import active_spiders, items_scraped, requests_total
from src.utils.proxy_manager import ProxyManager

logger = get_logger(__name__)


class ResilientSpider(scrapy.Spider):
    """Spider base com capacidades de auto recuperação."""

    custom_settings = {
        "RETRY_TIMES": settings.scrapy_retry_times,
        "CONCURRENT_REQUESTS": settings.scrapy_concurrent_requests,
        "DOWNLOAD_DELAY": settings.scrapy_download_delay,
        "AUTOTHROTTLE_ENABLED": settings.scrapy_autothrottle_enabled,
        "AUTOTHROTTLE_TARGET_CONCURRENCY": settings.scrapy_autothrottle_target_concurrency,
    }

    def __init__(self, *args: Any, **kwargs: Any):
        super().__init__(*args, **kwargs)
        self.failed_urls: List[str] = []
        self.portal_monitor = PortalMonitor()
        self.alert_service = AlertService()
        self.proxy_manager = ProxyManager()
        active_spiders.labels(portal=self.portal_name).inc()

    @property
    def portal_name(self) -> str:
        return getattr(self, "portal", self.name)

    def start_requests(self) -> Iterable[Request]:
        for url in self.start_urls:
            headers = self._build_headers()
            meta = {}
            proxy = self.proxy_manager.get_proxy()
            if proxy:
                meta["proxy"] = proxy

            yield Request(
                url,
                callback=self.parse,
                errback=self.handle_error,
                headers=headers,
                meta=meta,
                dont_filter=True,
            )

    def _build_headers(self) -> Dict[str, str]:
        user_agent = random.choice(settings_scrapy_user_agents())
        return {
            "User-Agent": user_agent,
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7",
        }

    def handle_error(self, failure: Any) -> None:
        request = failure.request
        url = getattr(request, "url", "desconhecida")
        logger.error("request_failed", url=url, error=str(failure))
        requests_total.labels(portal=self.portal_name, status="error").inc()
        self.failed_urls.append(url)

        if len(self.failed_urls) > 3:
            self.alert_service.send_alert(
                level="warning",
                message=f"Spider {self.name} acumulou falhas em {len(self.failed_urls)} URLs",
                metadata={"urls": self.failed_urls[-3:]},
            )

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=2, max=30),
        retry=retry_if_exception_type((IgnoreRequest, ConnectionError, TimeoutError)),
        reraise=True,
    )
    def parse(self, response: scrapy.http.Response) -> Any:
        requests_total.labels(portal=self.portal_name, status="success").inc()
        self.portal_monitor.record_response(response)

        if self.portal_monitor.detect_changes(response):
            logger.warning("portal_structure_changed", url=response.url)
            alternative_data = self.try_alternative_selectors(response)
            if alternative_data:
                items_scraped.labels(portal=self.portal_name, spider=self.name).inc()
                yield alternative_data
                return

        item = self.extract_data(response)
        if item:
            items_scraped.labels(portal=self.portal_name, spider=self.name).inc()
            yield item

    def try_alternative_selectors(self, response: scrapy.http.Response) -> Any:
        for selector in self.get_alternative_selectors():
            try:
                candidate = self.extract_with_selectors(response, selector)
                if self.validate_data(candidate):
                    logger.info("alternative_selector_success")
                    return candidate
            except Exception:  # pylint: disable=broad-except
                continue
        self.alert_service.send_alert(
            level="critical",
            message=f"Selectors alternativos falharam para {response.url}",
        )
        return None

    @abstractmethod
    def extract_data(self, response: scrapy.http.Response) -> Dict[str, Any]:
        raise NotImplementedError

    @abstractmethod
    def get_alternative_selectors(self) -> Iterable[Dict[str, Any]]:
        raise NotImplementedError

    @abstractmethod
    def extract_with_selectors(
        self, response: scrapy.http.Response, selectors: Dict[str, Any]
    ) -> Dict[str, Any]:
        raise NotImplementedError

    def validate_data(self, data: Dict[str, Any]) -> bool:
        return bool(data)

    def closed(self, reason: str) -> None:  # noqa: D401
        """Atualiza métricas ao finalizar spider."""
        active_spiders.labels(portal=self.portal_name).dec()
        logger.info("spider_closed", name=self.name, reason=reason)


def settings_scrapy_user_agents() -> List[str]:
    # Fallback caso não exista lista no settings
    return getattr(settings, "user_agent_list", [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/118.0 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 "
        "(KHTML, like Gecko) Version/14.0 Safari/605.1.15",
        "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:118.0) Gecko/20100101 Firefox/118.0",
    ])
