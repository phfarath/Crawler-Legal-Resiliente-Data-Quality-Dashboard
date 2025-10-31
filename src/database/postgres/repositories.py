"""Repositórios de acesso a dados no PostgreSQL."""

from datetime import datetime
from typing import Iterable, List, Optional

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from src.database.postgres.connection import get_session
from src.database.postgres.models import JudicialDecisionORM
from src.utils.logger import get_logger

logger = get_logger(__name__)


class JudicialDecisionRepository:
    """Acesso a dados de decisões judiciais."""

    def save(self, data: dict) -> JudicialDecisionORM:
        with get_session() as session:
            return self._save(session, data)

    def _save(self, session: Session, data: dict) -> JudicialDecisionORM:
        existing = session.execute(
            select(JudicialDecisionORM).where(JudicialDecisionORM.numero_cnj == data["numero_cnj"])
        ).scalar_one_or_none()

        if existing:
            for key, value in data.items():
                setattr(existing, key, value)
            existing.updated_at = datetime.utcnow()
            logger.info("decision_updated", numero_cnj=data["numero_cnj"])
            return existing

        decision = JudicialDecisionORM(**data)
        session.add(decision)
        try:
            session.flush()
            logger.info("decision_saved", numero_cnj=data["numero_cnj"])
            return decision
        except IntegrityError as exc:
            session.rollback()
            logger.error(
                "decision_save_conflict",
                numero_cnj=data["numero_cnj"],
                error=str(exc),
            )
            raise

    def exists_hash(self, hash_content: str) -> bool:
        with get_session() as session:
            result = session.execute(
                select(JudicialDecisionORM.id).where(JudicialDecisionORM.hash_content == hash_content)
            ).scalar_one_or_none()
            return result is not None

    def list_recent(self, limit: int = 50) -> List[JudicialDecisionORM]:
        with get_session() as session:
            return (
                session.query(JudicialDecisionORM)
                .order_by(JudicialDecisionORM.created_at.desc())
                .limit(limit)
                .all()
            )

    def get_by_cnj(self, numero_cnj: str) -> Optional[JudicialDecisionORM]:
        with get_session() as session:
            return (
                session.query(JudicialDecisionORM)
                .filter(JudicialDecisionORM.numero_cnj == numero_cnj)
                .one_or_none()
            )
