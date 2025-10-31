"""Schemas de validação usando Pydantic."""

from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, Field, validator


class ParteSchema(BaseModel):
    """Schema de validação para Parte."""

    nome: str = Field(..., min_length=1, max_length=500)
    tipo: str = Field(..., min_length=1, max_length=100)
    documento: Optional[str] = Field(None, max_length=50)
    representante: Optional[str] = Field(None, max_length=500)
    oab: Optional[str] = Field(None, max_length=20)

    class Config:
        json_schema_extra = {
            "example": {
                "nome": "João da Silva",
                "tipo": "Autor",
                "documento": "123.456.789-00",
                "representante": "Dr. José Santos",
                "oab": "SP123456",
            }
        }


class DocumentoSchema(BaseModel):
    """Schema de validação para Documento."""

    tipo: str = Field(..., min_length=1, max_length=100)
    url: Optional[str] = Field(None, max_length=1000)
    descricao: Optional[str] = Field(None, max_length=500)
    data_publicacao: Optional[datetime] = None

    class Config:
        json_schema_extra = {
            "example": {
                "tipo": "Sentença",
                "url": "https://exemplo.com/documento.pdf",
                "descricao": "Sentença de Procedência",
                "data_publicacao": "2024-01-15T10:00:00",
            }
        }


class JudicialDecisionSchema(BaseModel):
    """Schema de validação para Decisão Judicial."""

    numero_cnj: str = Field(..., min_length=25, max_length=25)
    numero_processo: str = Field(..., min_length=1, max_length=100)
    classe: str = Field(..., min_length=1, max_length=200)
    assunto: Optional[str] = Field(None, max_length=500)
    sistema_origem: str = Field(..., min_length=1, max_length=50)
    partes: List[ParteSchema] = Field(..., min_items=1)
    tribunal: str = Field(..., min_length=1, max_length=100)
    orgao_julgador: str = Field(..., min_length=1, max_length=200)
    relator: Optional[str] = Field(None, max_length=200)
    data_distribuicao: datetime
    data_julgamento: Optional[datetime] = None
    data_publicacao: Optional[datetime] = None
    ementa: str = Field(..., min_length=10)
    decisao: str = Field(..., min_length=10)
    documentos: List[DocumentoSchema] = Field(default_factory=list)
    hash_content: Optional[str] = Field(None, max_length=64)
    timestamp_coleta: datetime = Field(default_factory=datetime.utcnow)
    versao_parser: str = Field(default="1.0.0", max_length=20)
    origem_url: Optional[str] = Field(None, max_length=1000)
    portal: Optional[str] = Field(None, max_length=50)
    metadata: dict = Field(default_factory=dict)

    @validator("numero_cnj")
    def validate_numero_cnj(cls, v: str) -> str:
        """Valida formato do número CNJ."""
        import re

        pattern = r"^\d{7}-\d{2}\.\d{4}\.\d\.\d{2}\.\d{4}$"
        if not re.match(pattern, v):
            raise ValueError(
                f"Formato CNJ inválido: {v}. Esperado: NNNNNNN-DD.AAAA.J.TR.OOOO"
            )
        return v

    @validator("data_julgamento", "data_publicacao")
    def validate_dates_after_distribuicao(cls, v: Optional[datetime], values: dict) -> Optional[datetime]:
        """Valida que datas de julgamento/publicação são após distribuição."""
        if v and "data_distribuicao" in values:
            if v < values["data_distribuicao"]:
                raise ValueError(
                    f"Data deve ser posterior à data de distribuição"
                )
        return v

    class Config:
        json_schema_extra = {
            "example": {
                "numero_cnj": "0001234-56.2024.8.26.0100",
                "numero_processo": "1000001-23.2024.8.26.0100",
                "classe": "Apelação Cível",
                "assunto": "Direito Civil - Contratos",
                "sistema_origem": "eSAJ",
                "tribunal": "TJSP",
                "orgao_julgador": "1ª Câmara de Direito Privado",
                "relator": "Des. João Silva",
                "data_distribuicao": "2024-01-10T10:00:00",
                "ementa": "APELAÇÃO CÍVEL. Contrato de prestação de serviços...",
                "decisao": "Pelo exposto, NEGO PROVIMENTO ao recurso...",
            }
        }
