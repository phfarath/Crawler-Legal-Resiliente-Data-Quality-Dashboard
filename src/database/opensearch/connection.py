"""Conexão com OpenSearch."""

from functools import lru_cache

from opensearchpy import OpenSearch

from src.config import settings


@lru_cache()
def get_opensearch_client() -> OpenSearch:
    return OpenSearch(
        hosts=[{"host": settings.opensearch_host, "port": settings.opensearch_port}],
        http_auth=(settings.opensearch_user, settings.opensearch_password),
        use_ssl=True,
        verify_certs=False,
        ssl_show_warn=False,
    )
