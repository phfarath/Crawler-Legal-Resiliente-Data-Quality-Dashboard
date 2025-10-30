"""Validadores auxiliares."""

import re
from datetime import datetime
from typing import Iterable, Optional

from dateutil import parser


def validate_non_empty(value: str, field_name: str) -> str:
    """Valida que string não é vazia."""
    if not value or not value.strip():
        raise ValueError(f"{field_name} não pode ser vazio")
    return value.strip()


def validate_date(value: str, field_name: str) -> datetime:
    """Normaliza string de data para datetime."""
    try:
        return parser.parse(value, dayfirst=True)
    except (ValueError, TypeError) as exc:
        raise ValueError(f"{field_name} inválido: {value}") from exc


def validate_cpf(cpf: str) -> bool:
    """Valida CPF usando algoritmo de dígito verificador."""
    cpf = re.sub(r"\D", "", cpf)
    if len(cpf) != 11 or cpf == cpf[0] * 11:
        return False

    def calc_digit(nums: Iterable[int]) -> int:
        total = sum(v * (idx + 2) for idx, v in enumerate(reversed(nums)))
        mod = total % 11
        return 0 if mod < 2 else 11 - mod

    digits = list(map(int, cpf))
    check1 = calc_digit(digits[:9])
    check2 = calc_digit(digits[:10])

    return digits[9] == check1 and digits[10] == check2


def validate_cnpj(cnpj: str) -> bool:
    """Valida CNPJ com dígito verificador."""
    cnpj = re.sub(r"\D", "", cnpj)
    if len(cnpj) != 14 or cnpj == cnpj[0] * 14:
        return False

    def calc_digit(nums: Iterable[int]) -> int:
        weights = [6, 5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]
        s = sum(n * w for n, w in zip(nums, weights[-len(nums) :]))
        remainder = s % 11
        return 0 if remainder < 2 else 11 - remainder

    digits = list(map(int, cnpj))
    check1 = calc_digit(digits[:12])
    check2 = calc_digit(digits[:13])

    return digits[12] == check1 and digits[13] == check2


def sanitize_text(value: Optional[str]) -> Optional[str]:
    """Remove espaços extras e normaliza texto."""
    if value is None:
        return None
    cleaned = re.sub(r"\s+", " ", value)
    return cleaned.strip()
