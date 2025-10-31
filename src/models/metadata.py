"""Modelos auxiliares para metadados de coleta."""

from datetime import datetime
from typing import Dict, Optional

from pydantic import BaseModel, Field


class CollectionMetadata(BaseModel):
    """Metadados sobre execuções de crawling."""

    portal: str
    spider: str
    total_coletado: int = 0
    total_erros: int = 0
    tempo_medio_processamento: float = 0.0
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    observacoes: Optional[str] = None
    parametros_utilizados: Dict[str, str] = Field(default_factory=dict)


class PortalStatus(BaseModel):
    """Status de monitoramento de um portal."""

    portal: str
    status: str
    latencia_media: float
    taxa_sucesso: float
    ultima_atualizacao: datetime = Field(default_factory=datetime.utcnow)
    alerta: Optional[str] = None
