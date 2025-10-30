"""Tasks assíncronas com Celery."""

from src.config.celery_config import celery_app

__all__ = ["celery_app"]
