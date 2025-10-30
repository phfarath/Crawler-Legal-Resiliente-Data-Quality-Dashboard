"""Pipeline de normalização de dados."""

from typing import Any, Dict

import pandas as pd
from scrapy import Spider

from src.utils.cnj_utils import normalize_cnj_number
from src.utils.logger import get_logger
from src.utils.validators import sanitize_text

logger = get_logger(__name__)


class NormalizationPipeline:
    """Aplica transformações e normalizações ao item."""

    def process_item(self, item: Dict[str, Any], spider: Spider) -> Dict[str, Any]:
        item["numero_cnj"] = self._normalize_cnj(item["numero_cnj"])
        item["classe"] = sanitize_text(item.get("classe"))
        item["assunto"] = sanitize_text(item.get("assunto"))
        item["ementa"] = sanitize_text(item.get("ementa"))
        item["decisao"] = sanitize_text(item.get("decisao"))
        item["tribunal"] = sanitize_text(item.get("tribunal"))
        item["orgao_julgador"] = sanitize_text(item.get("orgao_julgador"))

        for parte in item.get("partes", []):
            parte["nome"] = sanitize_text(parte.get("nome"))
            parte["tipo"] = sanitize_text(parte.get("tipo"))
            parte["documento"] = sanitize_text(parte.get("documento"))

        item = self._normalize_dates(item)

        logger.info("item_normalized", numero_cnj=item.get("numero_cnj"))
        return item

    def _normalize_cnj(self, numero_cnj: str) -> str:
        normalized = normalize_cnj_number(numero_cnj)
        if not normalized:
            raise ValueError(f"Não foi possível normalizar CNJ: {numero_cnj}")
        return normalized

    def _normalize_dates(self, item: Dict[str, Any]) -> Dict[str, Any]:
        for key in ["data_distribuicao", "data_julgamento", "data_publicacao"]:
            if item.get(key):
                item[key] = pd.to_datetime(item[key])
        return item
