"""Endpoints para decisões judiciais."""

from typing import List, Optional

from fastapi import APIRouter, HTTPException, Query

from src.database.postgres.repositories import JudicialDecisionRepository
from src.models.schemas import JudicialDecisionSchema

router = APIRouter()
repo = JudicialDecisionRepository()


@router.get("/", response_model=List[JudicialDecisionSchema])
def list_decisions(
    limit: int = Query(50, ge=1, le=1000),
    tribunal: Optional[str] = None,
):
    """Lista decisões judiciais."""
    decisions = repo.list_recent(limit=limit)
    return [
        JudicialDecisionSchema.from_orm(d) for d in decisions
        if tribunal is None or d.tribunal == tribunal
    ]


@router.get("/{numero_cnj}", response_model=JudicialDecisionSchema)
def get_decision(numero_cnj: str):
    """Busca decisão por número CNJ."""
    decision = repo.get_by_cnj(numero_cnj)
    if not decision:
        raise HTTPException(status_code=404, detail="Decisão não encontrada")
    return JudicialDecisionSchema.from_orm(decision)
