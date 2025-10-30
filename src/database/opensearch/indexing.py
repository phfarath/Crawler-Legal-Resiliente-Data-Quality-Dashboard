"""Indexação de documentos no OpenSearch."""

from typing import Dict

from opensearchpy import OpenSearch
from opensearchpy.exceptions import NotFoundError

from src.config import settings
from src.database.opensearch.connection import get_opensearch_client
from src.utils.logger import get_logger

logger = get_logger(__name__)


class OpenSearchIndexer:
    """Gerencia indexação de documentos."""

    def __init__(self):
        self.client: OpenSearch = get_opensearch_client()
        self.index_name = settings.opensearch_index

    def create_index(self) -> None:
        """Cria índice se não existir."""
        if self.client.indices.exists(index=self.index_name):
            logger.info("index_already_exists", index=self.index_name)
            return

        mapping = {
            "mappings": {
                "properties": {
                    "numero_cnj": {"type": "keyword"},
                    "numero_processo": {"type": "keyword"},
                    "classe": {"type": "keyword"},
                    "assunto": {"type": "text"},
                    "tribunal": {"type": "keyword"},
                    "ementa": {
                        "type": "text",
                        "analyzer": "brazilian",
                    },
                    "decisao": {
                        "type": "text",
                        "analyzer": "brazilian",
                    },
                    "data_distribuicao": {"type": "date"},
                    "data_julgamento": {"type": "date"},
                    "data_publicacao": {"type": "date"},
                    "timestamp_coleta": {"type": "date"},
                }
            }
        }

        self.client.indices.create(index=self.index_name, body=mapping)
        logger.info("index_created", index=self.index_name)

    def index_document(self, doc_id: str, document: Dict) -> None:
        """Indexa documento."""
        self.client.index(index=self.index_name, id=doc_id, body=document)
        logger.info("document_indexed", id=doc_id)

    def bulk_index(self, documents: list) -> None:
        """Indexa múltiplos documentos."""
        from opensearchpy import helpers

        actions = [
            {
                "_index": self.index_name,
                "_id": doc["numero_cnj"],
                "_source": doc,
            }
            for doc in documents
        ]

        helpers.bulk(self.client, actions)
        logger.info("bulk_indexed", count=len(documents))
