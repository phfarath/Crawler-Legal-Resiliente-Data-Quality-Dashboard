"""Repositório MongoDB para documentos brutos."""

from datetime import datetime
from typing import Any, Dict, Optional

from src.database.mongodb.connection import get_mongodb_database
from src.utils.logger import get_logger

logger = get_logger(__name__)


class RawDocumentRepository:
    """Repositório para armazenamento de HTML e JSON brutos."""

    def __init__(self):
        self.db = get_mongodb_database()
        self.collection = self.db["raw_documents"]

    def save_raw_html(
        self,
        numero_cnj: str,
        html: str,
        url: str,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> str:
        """Salva HTML bruto de uma decisão judicial."""
        document = {
            "numero_cnj": numero_cnj,
            "html": html,
            "url": url,
            "metadata": metadata or {},
            "timestamp": datetime.utcnow(),
        }

        result = self.collection.insert_one(document)
        logger.info("raw_html_saved", numero_cnj=numero_cnj, doc_id=str(result.inserted_id))

        return str(result.inserted_id)

    def get_raw_html(self, numero_cnj: str) -> Optional[Dict[str, Any]]:
        """Recupera HTML bruto pelo número CNJ."""
        return self.collection.find_one({"numero_cnj": numero_cnj})

    def save_raw_json(
        self,
        numero_cnj: str,
        data: Dict[str, Any],
        url: str,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> str:
        """Salva resposta JSON bruta."""
        document = {
            "numero_cnj": numero_cnj,
            "data": data,
            "url": url,
            "metadata": metadata or {},
            "timestamp": datetime.utcnow(),
        }

        result = self.collection.insert_one(document)
        logger.info("raw_json_saved", numero_cnj=numero_cnj, doc_id=str(result.inserted_id))

        return str(result.inserted_id)
