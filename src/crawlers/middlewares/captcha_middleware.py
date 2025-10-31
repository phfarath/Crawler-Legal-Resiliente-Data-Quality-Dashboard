"""Middleware para resolução automática de CAPTCHAs."""

from typing import Optional

from scrapy import Request
from scrapy.http import Response

from src.config import settings
from src.utils.logger import get_logger

logger = get_logger(__name__)


class CaptchaSolverMiddleware:
    """Detecta e resolve CAPTCHAs automaticamente."""

    def __init__(self):
        self.api_key = settings.captcha_api_key
        self.solver_type = settings.captcha_solver

    def process_response(self, request: Request, response: Response, spider):  # type: ignore[override]
        # Detecta presença de CAPTCHA
        if self._has_captcha(response):
            logger.warning("captcha_detected", url=request.url)
            # Em um cenário real, aqui chamaríamos serviço de resolução:
            # solution = self.solve_captcha(response)
            # return self.retry_request_with_solution(request, solution)
            pass

        return response

    def _has_captcha(self, response: Response) -> bool:
        """Detecta CAPTCHAs comuns."""
        captcha_indicators = [
            b"recaptcha",
            b"captcha",
            b"g-recaptcha",
            b"hcaptcha",
        ]
        body_lower = response.body.lower()
        return any(indicator in body_lower for indicator in captcha_indicators)

    def solve_captcha(self, response: Response) -> Optional[str]:
        """
        Resolve CAPTCHA usando serviço externo.
        
        Implementação real deveria integrar com 2captcha, AntiCaptcha, etc.
        """
        # TODO: Implementar integração real com serviço de resolução
        # Exemplo com 2captcha:
        # from twocaptcha import TwoCaptcha
        # solver = TwoCaptcha(self.api_key)
        # result = solver.recaptcha(sitekey=sitekey, url=url)
        # return result['code']

        logger.info("captcha_solver_called", solver=self.solver_type)
        return None
