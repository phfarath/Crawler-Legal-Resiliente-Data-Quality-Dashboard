"""Busca em OpenSearch."""

from typing import Dict, List

from opensearchpy import OpenSearch

from src.config import settings
from src.database.opensearch.connection import get_opensearch_client


class OpenSearchSearcher:
    """Realiza buscas full-text."""

    def __init__(self):
        self.client: OpenSearch = get_opensearch_client()
        self.index_name = settings.opensearch_index

    def search(self, query: str, size: int = 10) -> List[Dict]:
        body = {
            "size": size,
            "query": {
                "multi_match": {
                    "query": query,
                    "fields": ["ementa^2", "decisao", "assunto"],
                    "type": "best_fields",
                }
            },
        }

        response = self.client.search(index=self.index_name, body=body)
        hits = response.get("hits", {}).get("hits", [])
        return [hit["_source"] for hit in hits]
