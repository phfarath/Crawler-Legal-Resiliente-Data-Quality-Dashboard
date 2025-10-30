"""Pipeline de deduplicação usando hash e MinHash."""

import hashlib
from typing import Any, Dict

from datasketch import MinHash, MinHashLSH
from scrapy import Spider
from scrapy.exceptions import DropItem

from src.utils.logger import get_logger
from src.utils.metrics import duplicates_found

logger = get_logger(__name__)


class DeduplicationPipeline:
    """Detecta e remove duplicatas."""

    def __init__(self):
        self.lsh = MinHashLSH(threshold=0.8, num_perm=128)
        self.seen_hashes: set = set()

    def process_item(self, item: Dict[str, Any], spider: Spider) -> Dict[str, Any]:
        # Método 1: Hash exato
        content_hash = self._generate_content_hash(item)

        if content_hash in self.seen_hashes:
            duplicates_found.labels(tipo="exact").inc()
            logger.warning("duplicate_exact", numero_cnj=item.get("numero_cnj"))
            raise DropItem("Duplicata exata")

        # Método 2: MinHash para fuzzy matching
        minhash = self._generate_minhash(item)
        if self.lsh.query(minhash):
            duplicates_found.labels(tipo="fuzzy").inc()
            logger.warning("duplicate_fuzzy", numero_cnj=item.get("numero_cnj"))
            raise DropItem("Duplicata fuzzy (similaridade > 80%)")

        self.seen_hashes.add(content_hash)
        self.lsh.insert(content_hash, minhash)
        item["hash_content"] = content_hash

        logger.info("item_unique", numero_cnj=item.get("numero_cnj"))
        return item

    def _generate_content_hash(self, item: Dict[str, Any]) -> str:
        content = f"{item['numero_cnj']}{item.get('ementa', '')}{item.get('decisao', '')}"
        return hashlib.sha256(content.encode("utf-8")).hexdigest()

    def _generate_minhash(self, item: Dict[str, Any]) -> MinHash:
        text = f"{item.get('ementa', '')} {item.get('decisao', '')}"

        minhash = MinHash(num_perm=128)
        for word in text.lower().split():
            minhash.update(word.encode("utf8"))

        return minhash
