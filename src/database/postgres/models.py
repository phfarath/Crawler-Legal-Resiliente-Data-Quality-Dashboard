"""Modelos ORM do PostgreSQL."""

import uuid
from datetime import datetime

from sqlalchemy import Column, DateTime, String, Text, func
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class JudicialDecisionORM(Base):
    """Representação ORM da decisão judicial."""

    __tablename__ = "judicial_decisions"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    numero_cnj = Column(String(25), nullable=False, unique=True, index=True)
    numero_processo = Column(String(100), nullable=False)
    classe = Column(String(200), nullable=False)
    assunto = Column(String(500))
    sistema_origem = Column(String(50), nullable=False)
    partes = Column(JSONB, nullable=False)
    tribunal = Column(String(200), nullable=False)
    orgao_julgador = Column(String(200), nullable=False)
    relator = Column(String(200))
    data_distribuicao = Column(DateTime(timezone=True), nullable=False)
    data_julgamento = Column(DateTime(timezone=True))
    data_publicacao = Column(DateTime(timezone=True))
    ementa = Column(Text, nullable=False)
    decisao = Column(Text, nullable=False)
    documentos = Column(JSONB, default=list)
    hash_content = Column(String(64), nullable=False, unique=True)
    timestamp_coleta = Column(DateTime(timezone=True), default=datetime.utcnow)
    versao_parser = Column(String(20), default="1.0.0")
    origem_url = Column(String(1000))
    portal = Column(String(50))
    metadata_json = Column("metadata", JSONB, default=dict)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    __table_args__ = (
        {},
    )
