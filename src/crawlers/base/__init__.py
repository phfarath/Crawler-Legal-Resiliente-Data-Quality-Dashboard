"""Base spiders."""

from src.crawlers.base.resilient_spider import ResilientSpider
from src.crawlers.base.selenium_spider import SeleniumSpider

__all__ = ["ResilientSpider", "SeleniumSpider"]
