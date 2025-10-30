"""Modelos de domínio principais para decisões judiciais."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Optional


@dataclass
class Parte:
    """Representa uma parte do processo."""

    nome: str
    tipo: str
    documento: Optional[str] = None
    representante: Optional[str] = None
    oab: Optional[str] = None


@dataclass
class Documento:
    """Documentos associados à decisão."""

    tipo: str
    url: Optional[str] = None
    descricao: Optional[str] = None
    data_publicacao: Optional[datetime] = None


@dataclass
class JudicialDecision:
    """Estrutura principal de uma decisão judicial."""

    numero_cnj: str
    numero_processo: str
    classe: str
    assunto: Optional[str]
    sistema_origem: str
    partes: List[Parte]
    tribunal: str
    orgao_julgador: str
    relator: Optional[str]
    data_distribuicao: datetime
    data_julgamento: Optional[datetime]
    data_publicacao: Optional[datetime]
    ementa: str
    decisao: str
    documentos: List[Documento] = field(default_factory=list)
    hash_content: Optional[str] = None
    timestamp_coleta: datetime = field(default_factory=datetime.utcnow)
    versao_parser: str = "1.0.0"
    origem_url: Optional[str] = None
    portal: Optional[str] = None
    metadata: dict = field(default_factory=dict)
