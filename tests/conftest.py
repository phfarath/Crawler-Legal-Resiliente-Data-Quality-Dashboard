"""Fixtures pytest compartilhadas."""

import pytest


@pytest.fixture
def sample_decision():
    return {
        "numero_cnj": "0001234-56.2024.8.26.0100",
        "numero_processo": "1000001-23.2024.8.26.0100",
        "classe": "Apelação Cível",
        "assunto": "Direito Civil - Contratos",
        "sistema_origem": "eSAJ",
        "tribunal": "TJSP",
        "orgao_julgador": "1ª Câmara de Direito Privado",
        "relator": "Des. João Silva",
        "data_distribuicao": "2024-01-10T10:00:00",
        "ementa": "APELAÇÃO CÍVEL. Contrato de prestação de serviços...",
        "decisao": "Pelo exposto, NEGO PROVIMENTO ao recurso...",
        "partes": [
            {"nome": "João da Silva", "tipo": "Autor"},
        ],
    }
