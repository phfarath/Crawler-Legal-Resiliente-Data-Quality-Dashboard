"""Suporte para spiders baseadas em Selenium."""

from __future__ import annotations

import random
import time
from typing import Any, Dict

from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from undetected_chromedriver import Chrome

from src.config import settings
from src.services.alert_service import AlertService
from src.utils.logger import get_logger
from src.utils.proxy_manager import ProxyManager

logger = get_logger(__name__)


class SeleniumSpider:
    """Base para spiders que precisam de renderização JavaScript."""

    def __init__(self) -> None:
        self.proxy_manager = ProxyManager()
        self.alert_service = AlertService()
        self.driver = self._setup_driver()
        self.wait = WebDriverWait(self.driver, 20)

    def _setup_driver(self) -> webdriver.Chrome:
        options = webdriver.ChromeOptions()
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--no-sandbox")
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option("useAutomationExtension", False)
        options.add_argument(f"user-agent={self._get_random_user_agent()}")

        if settings.selenium_headless:
            options.add_argument("--headless=new")

        proxy = self.proxy_manager.get_proxy()
        if proxy:
            options.add_argument(f"--proxy-server={proxy}")

        driver = Chrome(options=options)

        driver.execute_cdp_cmd(
            "Page.addScriptToEvaluateOnNewDocument",
            {
                "source": """
                Object.defineProperty(navigator, 'webdriver', {
                    get: () => undefined
                });
                """,
            },
        )

        return driver

    def _get_random_user_agent(self) -> str:
        agents = [
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
            "(KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 "
            "(KHTML, like Gecko) Version/17.0 Safari/605.1.15",
            "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:118.0) Gecko/20100101 Firefox/118.0",
        ]
        return random.choice(agents)

    def scrape_page(self, url: str, wait_selector: str) -> Dict[str, Any]:
        try:
            self.driver.get(url)
            self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, wait_selector)))
            self._simulate_human_behavior()
            html = self.driver.page_source
            return {
                "url": url,
                "html": html,
            }
        except TimeoutException as exc:
            logger.error("selenium_timeout", url=url)
            self.alert_service.send_alert(
                level="warning",
                message=f"Timeout ao carregar {url}",
            )
            raise exc

    def _simulate_human_behavior(self) -> None:
        total_height = self.driver.execute_script("return document.body.scrollHeight")
        for position in range(0, total_height, 200):
            self.driver.execute_script("window.scrollTo(0, arguments[0]);", position)
            time.sleep(random.uniform(0.1, 0.3))
        time.sleep(random.uniform(1, 2))

    def close(self) -> None:
        try:
            self.driver.quit()
        except Exception:  # pylint: disable=broad-except
            logger.warning("selenium_driver_close_failed")
