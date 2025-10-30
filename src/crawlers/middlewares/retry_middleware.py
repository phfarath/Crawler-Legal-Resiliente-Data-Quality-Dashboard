"""Middleware de retry inteligente com backoff exponencial."""

import random
import time
from typing import Optional

from scrapy import Request
from scrapy.downloadermiddlewares.retry import RetryMiddleware

from src.utils.logger import get_logger

logger = get_logger(__name__)


class ResilientRetryMiddleware(RetryMiddleware):
    """Retry com jitter e controle de sessão."""

    def __init__(self, settings):
        super().__init__(settings)
        self.max_retry_times = settings.getint("RETRY_TIMES", 5)

    def process_exception(self, request: Request, exception, spider):  # type: ignore[override]
        logger.warning("request_exception", url=request.url, error=str(exception))
        return super().process_exception(request, exception, spider)

    def _retry(
        self,
        request: Request,
        reason: Optional[str] = None,
        spider=None,
    ):
        retries = request.meta.get("retry_times", 0) + 1

        if retries <= self.max_retry_times:
            delay = self._calculate_delay(retries)
            time.sleep(delay)
            logger.info(
                "retry_request",
                url=request.url,
                retries=retries,
                delay=delay,
                reason=str(reason),
            )
        return super()._retry(request, reason, spider)

    def _calculate_delay(self, retries: int) -> float:
        base = 2 ** retries
        jitter = random.uniform(0, 1)
        return min(base + jitter, 60.0)
