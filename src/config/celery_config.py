"""Configuração do Celery."""

from celery import Celery

from src.config import settings

celery_app = Celery(
    "crawler_legal_resiliente",
    broker=f"amqp://{settings.rabbitmq_user}:{settings.rabbitmq_password}@"
    f"{settings.rabbitmq_host}:{settings.rabbitmq_port}{settings.rabbitmq_vhost}",
    backend=settings.redis_uri,
)

celery_app.conf.update(
    task_serializer="json",
    result_serializer="json",
    accept_content=["json"],
    timezone=settings.timezone,
    enable_utc=True,
    task_acks_late=True,
    worker_prefetch_multiplier=1,
)

celery_app.autodiscover_tasks(["src.tasks"])
