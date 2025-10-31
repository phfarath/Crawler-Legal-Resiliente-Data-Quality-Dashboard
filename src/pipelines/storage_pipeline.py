"""Pipeline de persistência de dados nos bancos."""

from typing import Any, Dict

from scrapy import Spider

from src.config import settings
from src.database.mongodb.repositories import RawDocumentRepository
from src.database.opensearch.indexing import OpenSearchIndexer
from src.database.postgres.repositories import JudicialDecisionRepository
from src.utils.logger import get_logger

logger = get_logger(__name__)


class StoragePipeline:
    """Persiste itens validados nos diferentes storages."""

    def __init__(self):
        self.pg_repo = JudicialDecisionRepository()
        self.mongo_repo = RawDocumentRepository() if settings.enable_mongodb else None
        self.opensearch = OpenSearchIndexer() if settings.enable_opensearch else None

    def open_spider(self, spider: Spider):
        if self.opensearch:
            self.opensearch.create_index()

    def process_item(self, item: Dict[str, Any], spider: Spider) -> Dict[str, Any]:
        # PostgreSQL: dados estruturados
        self.pg_repo.save(item)

        # MongoDB: HTML/JSON bruto (se disponível)
        if self.mongo_repo and "raw_html" in item:
            self.mongo_repo.save_raw_html(
                numero_cnj=item["numero_cnj"],
                html=item["raw_html"],
                url=item.get("origem_url", ""),
                metadata=item.get("metadata", {}),
            )

        # OpenSearch: indexação para busca full-text
        if self.opensearch:
            self.opensearch.index_document(
                doc_id=item["numero_cnj"],
                document=item,
            )

        logger.info("item_persisted", numero_cnj=item["numero_cnj"])
        return item
