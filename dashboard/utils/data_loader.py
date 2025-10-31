"""Funções para carregar dados no dashboard."""

from typing import Dict, List, Tuple

from src.database.postgres.repositories import JudicialDecisionRepository

repo = JudicialDecisionRepository()


def load_dashboard_data(portal: str, tribunal: str) -> Tuple[Dict[str, str], List[Dict], Dict[str, int]]:
    decisions_orm = repo.list_recent(limit=50)
    decisions = [
        {
            "Número CNJ": decision.numero_cnj,
            "Classe": decision.classe,
            "Tribunal": decision.tribunal,
            "Órgão Julgador": decision.orgao_julgador,
            "Data Distribuição": decision.data_distribuicao,
        }
        for decision in decisions_orm
        if (portal == "Todos" or decision.portal == portal)
        and (not tribunal or decision.tribunal == tribunal)
    ]

    coverage: Dict[str, int] = {}
    for decision in decisions:
        tribunal_name = decision["Tribunal"]
        coverage[tribunal_name] = coverage.get(tribunal_name, 0) + 1

    metrics = {
        "Processos Coletados": str(len(decisions)),
        "Portais Ativos": str(len({d.get("Tribunal") for d in decisions})),
    }

    return metrics, decisions, coverage
