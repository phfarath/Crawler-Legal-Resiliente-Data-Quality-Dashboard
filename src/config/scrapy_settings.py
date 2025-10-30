"""Configurações do Scrapy para spiders resilientes."""

from src.config import settings

SCRAPY_SETTINGS = {
    "BOT_NAME": "crawler_legal_resiliente",
    "ROBOTSTXT_OBEY": False,
    "DOWNLOAD_DELAY": settings.scrapy_download_delay,
    "CONCURRENT_REQUESTS": settings.scrapy_concurrent_requests,
    "RETRY_TIMES": settings.scrapy_retry_times,
    "AUTOTHROTTLE_ENABLED": settings.scrapy_autothrottle_enabled,
    "AUTOTHROTTLE_TARGET_CONCURRENCY": settings.scrapy_autothrottle_target_concurrency,
    "DOWNLOADER_MIDDLEWARES": {
        "src.crawlers.middlewares.proxy_middleware.ProxyRotationMiddleware": 610,
        "src.crawlers.middlewares.retry_middleware.ResilientRetryMiddleware": 620,
        "src.crawlers.middlewares.captcha_middleware.CaptchaSolverMiddleware": 630,
    },
    "ITEM_PIPELINES": {
        "src.pipelines.validation_pipeline.ValidationPipeline": 100,
        "src.pipelines.normalization_pipeline.NormalizationPipeline": 200,
        "src.pipelines.deduplication_pipeline.DeduplicationPipeline": 300,
        "src.pipelines.enrichment_pipeline.EnrichmentPipeline": 400,
        "src.pipelines.storage_pipeline.StoragePipeline": 500,
    },
    "LOG_LEVEL": settings.log_level,
    "USER_AGENT_LIST": [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/118.0 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 "
        "(KHTML, like Gecko) Version/14.0 Safari/605.1.15",
        "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:118.0) Gecko/20100101 Firefox/118.0",
    ],
}
