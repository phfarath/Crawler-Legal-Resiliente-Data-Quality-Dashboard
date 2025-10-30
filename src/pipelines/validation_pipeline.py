"""Pipeline de validação de dados."""

from typing import Any, Dict

from pydantic import ValidationError
from scrapy import Spider
from scrapy.exceptions import DropItem

from src.models.schemas import JudicialDecisionSchema
from src.utils.cnj_utils import validate_cnj_checksum, validate_cnj_format
from src.utils.logger import get_logger
from src.utils.metrics import duplicates_found

logger = get_logger(__name__)


class ValidationPipeline:
    """Valida estrutura e conteúdo dos itens capturados."""

    def process_item(self, item: Dict[str, Any], spider: Spider) -> Dict[str, Any]:
        try:
            # Valida usando Pydantic
            validated = JudicialDecisionSchema(**item)

            # Validações adicionais
            self._validate_cnj_number(validated.numero_cnj)
            self._validate_dates(validated)
            self._validate_parties(validated.partes)

            logger.info(
                "item_validated",
                numero_cnj=validated.numero_cnj,
                spider=spider.name,
            )

            return validated.dict()

        except ValidationError as exc:
            logger.error(
                "validation_failed",
                error=str(exc),
                item=item.get("numero_cnj", "unknown"),
            )
            raise DropItem(f"Validação falhou: {exc}") from exc

    def _validate_cnj_number(self, numero_cnj: str) -> None:
        if not validate_cnj_format(numero_cnj):
            raise ValueError(f"Formato CNJ inválido: {numero_cnj}")

        if not validate_cnj_checksum(numero_cnj):
            raise ValueError(f"Dígito verificador CNJ inválido: {numero_cnj}")

    def _validate_dates(self, item: JudicialDecisionSchema) -> None:
        if item.data_julgamento:
            if item.data_julgamento < item.data_distribuicao:
                raise ValueError("data_julgamento anterior a data_distribuicao")

        if item.data_publicacao:
            if item.data_publicacao < item.data_distribuicao:
                raise ValueError("data_publicacao anterior a data_distribuicao")

    def _validate_parties(self, partes: list) -> None:
        if not partes:
            raise ValueError("Processo deve conter ao menos uma parte")
