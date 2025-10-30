"""Tasks de processamento de dados."""

from typing import List

from celery import shared_task

from src.database.postgres.repositories import JudicialDecisionRepository
from src.models.schemas import JudicialDecisionSchema
from src.utils.logger import get_logger

logger = get_logger(__name__)


@shared_task(bind=True, name="tasks.generate_quality_report")
def generate_quality_report(self) -> List[str]:
    repo = JudicialDecisionRepository()
    decisions = repo.list_recent(limit=20)
    report = [decision.numero_cnj for decision in decisions]
    logger.info("quality_report_generated", count=len(report))
    return report
