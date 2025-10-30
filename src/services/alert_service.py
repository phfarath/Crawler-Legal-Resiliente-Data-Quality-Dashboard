"""Serviço de envio de alertas."""

from typing import Any, Dict, Optional

import requests

from src.config import settings
from src.utils.logger import get_logger

logger = get_logger(__name__)


class AlertService:
    """Centraliza envio de alertas (Slack, email, Sentry)."""

    def __init__(self):
        self.slack_webhook = settings.slack_webhook_url
        self.alert_email = settings.alert_email

    def send_alert(
        self,
        level: str,
        message: str,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> None:
        payload = {
            "level": level,
            "message": message,
            "metadata": metadata or {},
        }

        logger.warning("alert_emitted", **payload)
        self._send_slack(payload)

    def _send_slack(self, payload: Dict[str, Any]) -> None:
        if not self.slack_webhook or self.slack_webhook == "chave-api-servico":
            return

        try:
            requests.post(self.slack_webhook, json=payload, timeout=5)
        except requests.RequestException as exc:
            logger.error("alert_slack_failed", error=str(exc))
