"""Spider para TJSP através do sistema eSAJ."""

from typing import Any, Dict, Iterable

from scrapy.http import Response

from src.crawlers.base.resilient_spider import ResilientSpider
from src.utils.logger import get_logger

logger = get_logger(__name__)


class TJSPESAJSpider(ResilientSpider):
    """Spider para tribunal de justiça de SP via eSAJ."""

    name = "tjsp_esaj"
    portal = "esaj"
    allowed_domains = ["esaj.tjsp.jus.br"]
    start_urls = ["https://esaj.tjsp.jus.br/cpopg/open.do"]

    custom_settings = {
        **ResilientSpider.custom_settings,
        "DOWNLOAD_DELAY": 2,
    }

    def extract_data(self, response: Response) -> Dict[str, Any]:
        """Extrai dados de decisão judicial do eSAJ."""
        try:
            item = {
                "numero_cnj": self._extract_numero_cnj(response),
                "numero_processo": response.css(".unificado::text").get() or "",
                "classe": response.css(".classeProcesso::text").get() or "",
                "assunto": response.css(".assuntoProcesso::text").get(),
                "sistema_origem": "eSAJ",
                "tribunal": "TJSP",
                "orgao_julgador": response.css(".orgaoJulgador::text").get() or "",
                "relator": response.css(".relator::text").get(),
                "data_distribuicao": response.css(".dataDistribuicao::text").get() or "",
                "data_julgamento": response.css(".dataJulgamento::text").get(),
                "data_publicacao": response.css(".dataPublicacao::text").get(),
                "ementa": response.css(".ementa::text").getall() or [""],
                "decisao": response.css(".decisao::text").getall() or [""],
                "partes": self._extract_partes(response),
                "documentos": [],
                "origem_url": response.url,
                "portal": self.portal,
            }

            item["ementa"] = " ".join(item["ementa"])
            item["decisao"] = " ".join(item["decisao"])

            return item

        except Exception as exc:  # pylint: disable=broad-except
            logger.error("extract_error", url=response.url, error=str(exc))
            return {}

    def _extract_numero_cnj(self, response: Response) -> str:
        numero = response.css(".numeroProcesso::text").get() or ""
        return numero.strip()

    def _extract_partes(self, response: Response) -> list:
        partes = []
        for parte_div in response.css(".parte"):
            nome = parte_div.css(".nomeParte::text").get()
            tipo = parte_div.css(".tipoParte::text").get()
            if nome and tipo:
                partes.append(
                    {
                        "nome": nome.strip(),
                        "tipo": tipo.strip(),
                        "documento": None,
                        "representante": None,
                    }
                )
        return partes

    def get_alternative_selectors(self) -> Iterable[Dict[str, Any]]:
        """Fornece seletores alternativos se estrutura mudar."""
        return [
            {
                "numero_cnj": ".processo-numero::text",
                "classe": ".processo-classe::text",
            },
            {
                "numero_cnj": "#numeroProcesso::text",
                "classe": "#classeProcesso::text",
            },
        ]

    def extract_with_selectors(
        self,
        response: Response,
        selectors: Dict[str, Any],
    ) -> Dict[str, Any]:
        """Tenta extrair usando seletores alternativos."""
        return {
            key: response.css(selector).get()
            for key, selector in selectors.items()
        }
