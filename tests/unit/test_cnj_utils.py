"""Testes para utilidades CNJ."""

from src.utils.cnj_utils import (
    extract_cnj_components,
    normalize_cnj_number,
    validate_cnj_checksum,
    validate_cnj_format,
)


def test_validate_cnj_format():
    assert validate_cnj_format("0001234-56.2024.8.26.0100")
    assert not validate_cnj_format("1234-56.2024.8.26.0100")


def test_extract_cnj_components():
    components = extract_cnj_components("0001234-56.2024.8.26.0100")
    assert components["sequencial"] == "0001234"
    assert components["ano"] == "2024"


def test_validate_cnj_checksum():
    numero = "0000001-98.2023.8.26.0100"
    assert validate_cnj_checksum(numero)


def test_normalize_cnj_number():
    numero = "0000001 98 2023 8 26 0100"
    normalized = normalize_cnj_number(numero)
    assert normalized == "0000001-98.2023.8.26.0100"
