"""Pipeline para enriquecimento de dados."""

from typing import Any, Dict

from scrapy import Spider

from src.models.metadata import CollectionMetadata
from src.utils.cnj_utils import extract_cnj_components, get_segmento_name, get_tribunal_name
from src.utils.logger import get_logger

logger = get_logger(__name__)


class EnrichmentPipeline:
    """Adiciona metadados derivados e enriquecimentos."""

    def process_item(self, item: Dict[str, Any], spider: Spider) -> Dict[str, Any]:
        components = extract_cnj_components(item["numero_cnj"])
        if components:
            item.setdefault("metadata", {})
            item["metadata"].update(
                {
                    "sequencial": components["sequencial"],
                    "segmento_codigo": components["segmento"],
                    "segmento_nome": get_segmento_name(components["segmento"]),
                    "tribunal_codigo": components["tribunal"],
                    "tribunal_nome": get_tribunal_name(components["tribunal"]),
                    "origem_codigo": components["origem"],
                }
            )

        item.setdefault("metadata", {})
        item["metadata"].update(
            {
                "spider": spider.name,
                "portal": getattr(spider, "portal", "desconhecido"),
                "environment": spider.settings.get("ENVIRONMENT", "development"),
            }
        )

        logger.info("item_enriched", numero_cnj=item["numero_cnj"])
        return item
