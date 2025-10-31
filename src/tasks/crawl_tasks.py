"""Tasks relacionadas a execução de crawlers."""

from celery import shared_task
from scrapy.crawler import CrawlerProcess

from src.config.scrapy_settings import SCRAPY_SETTINGS
from src.crawlers.esaj.tjsp_spider import TJSPESAJSpider
from src.utils.logger import get_logger

logger = get_logger(__name__)


@shared_task(bind=True, name="tasks.run_tjsp_esaj")
def run_tjsp_esaj(self):
    """Executa spider TJSP eSAJ com resistência."""
    process = CrawlerProcess(SCRAPY_SETTINGS)

    logger.info("celery_task_start", task=self.name)
    process.crawl(TJSPESAJSpider)
    process.start()
    logger.info("celery_task_finished", task=self.name)
