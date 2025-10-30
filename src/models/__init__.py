"""Modelos de dados."""

from src.models.judicial_decision import (
    Documento,
    JudicialDecision,
    Parte,
)
from src.models.schemas import JudicialDecisionSchema

__all__ = [
    "JudicialDecision",
    "Parte",
    "Documento",
    "JudicialDecisionSchema",
]
