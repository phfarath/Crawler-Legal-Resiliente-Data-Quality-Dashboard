"""Utilitários para número CNJ (Conselho Nacional de Justiça)."""

import re
from typing import Dict, Optional


def validate_cnj_format(numero_cnj: str) -> bool:
    """
    Valida formato do número CNJ.
    
    Formato: NNNNNNN-DD.AAAA.J.TR.OOOO
    
    Args:
        numero_cnj: Número CNJ a validar
        
    Returns:
        True se válido, False caso contrário
    """
    pattern = r"^\d{7}-\d{2}\.\d{4}\.\d\.\d{2}\.\d{4}$"
    return bool(re.match(pattern, numero_cnj))


def extract_cnj_components(numero_cnj: str) -> Optional[Dict[str, str]]:
    """
    Extrai componentes do número CNJ.
    
    Args:
        numero_cnj: Número CNJ no formato NNNNNNN-DD.AAAA.J.TR.OOOO
        
    Returns:
        Dicionário com componentes ou None se inválido
        
    Exemplo:
        >>> extract_cnj_components("0001234-56.2024.8.26.0100")
        {
            'sequencial': '0001234',
            'digito': '56',
            'ano': '2024',
            'segmento': '8',
            'tribunal': '26',
            'origem': '0100'
        }
    """
    if not validate_cnj_format(numero_cnj):
        return None

    pattern = r"^(\d{7})-(\d{2})\.(\d{4})\.(\d)\.(\d{2})\.(\d{4})$"
    match = re.match(pattern, numero_cnj)

    if not match:
        return None

    return {
        "sequencial": match.group(1),
        "digito": match.group(2),
        "ano": match.group(3),
        "segmento": match.group(4),
        "tribunal": match.group(5),
        "origem": match.group(6),
    }


def validate_cnj_checksum(numero_cnj: str) -> bool:
    """
    Valida dígito verificador do número CNJ.
    
    Args:
        numero_cnj: Número CNJ completo
        
    Returns:
        True se dígito válido, False caso contrário
    """
    components = extract_cnj_components(numero_cnj)
    if not components:
        return False

    # Calcula dígito verificador
    num_str = (
        components["origem"]
        + components["ano"]
        + components["segmento"]
        + components["tribunal"]
        + components["sequencial"]
    )

    remainder = int(num_str) % 97
    calculated_digit = 98 - remainder

    expected_digit = int(components["digito"])

    return calculated_digit == expected_digit


def get_tribunal_name(tribunal_code: str) -> str:
    """
    Retorna nome do tribunal pelo código.
    
    Args:
        tribunal_code: Código de 2 dígitos do tribunal
        
    Returns:
        Nome do tribunal
    """
    tribunais = {
        "01": "STF - Supremo Tribunal Federal",
        "02": "CNJ - Conselho Nacional de Justiça",
        "03": "STJ - Superior Tribunal de Justiça",
        "04": "JF - Justiça Federal",
        "05": "JT - Justiça do Trabalho",
        "06": "JE - Justiça Eleitoral",
        "07": "JM - Justiça Militar da União",
        "08": "TJDFT - Tribunal de Justiça do Distrito Federal e Territórios",
        "09": "TJAC - Tribunal de Justiça do Acre",
        "10": "TJAL - Tribunal de Justiça de Alagoas",
        "11": "TJAP - Tribunal de Justiça do Amapá",
        "12": "TJAM - Tribunal de Justiça do Amazonas",
        "13": "TJBA - Tribunal de Justiça da Bahia",
        "14": "TJCE - Tribunal de Justiça do Ceará",
        "15": "TJES - Tribunal de Justiça do Espírito Santo",
        "16": "TJGO - Tribunal de Justiça de Goiás",
        "17": "TJMA - Tribunal de Justiça do Maranhão",
        "18": "TJMT - Tribunal de Justiça de Mato Grosso",
        "19": "TJMS - Tribunal de Justiça de Mato Grosso do Sul",
        "20": "TJMG - Tribunal de Justiça de Minas Gerais",
        "21": "TJPA - Tribunal de Justiça do Pará",
        "22": "TJPB - Tribunal de Justiça da Paraíba",
        "23": "TJPR - Tribunal de Justiça do Paraná",
        "24": "TJPE - Tribunal de Justiça de Pernambuco",
        "25": "TJPI - Tribunal de Justiça do Piauí",
        "26": "TJSP - Tribunal de Justiça de São Paulo",
        "27": "TJRJ - Tribunal de Justiça do Rio de Janeiro",
        "28": "TJRN - Tribunal de Justiça do Rio Grande do Norte",
        "29": "TJRS - Tribunal de Justiça do Rio Grande do Sul",
        "30": "TJRO - Tribunal de Justiça de Rondônia",
        "31": "TJRR - Tribunal de Justiça de Roraima",
        "32": "TJSC - Tribunal de Justiça de Santa Catarina",
        "33": "TJSE - Tribunal de Justiça de Sergipe",
        "34": "TJTO - Tribunal de Justiça de Tocantins",
    }

    return tribunais.get(tribunal_code, f"Tribunal desconhecido ({tribunal_code})")


def get_segmento_name(segmento_code: str) -> str:
    """
    Retorna nome do segmento judicial pelo código.
    
    Args:
        segmento_code: Código de 1 dígito do segmento
        
    Returns:
        Nome do segmento
    """
    segmentos = {
        "1": "Supremo Tribunal Federal",
        "2": "Conselho Nacional de Justiça",
        "3": "Superior Tribunal de Justiça",
        "4": "Justiça Federal",
        "5": "Justiça do Trabalho",
        "6": "Justiça Eleitoral",
        "7": "Justiça Militar da União",
        "8": "Justiça Estadual",
        "9": "Justiça Militar Estadual",
    }

    return segmentos.get(segmento_code, f"Segmento desconhecido ({segmento_code})")


def normalize_cnj_number(numero: str) -> Optional[str]:
    """
    Normaliza número CNJ removendo espaços e caracteres especiais inválidos.
    
    Args:
        numero: Número CNJ possivelmente com formatação inconsistente
        
    Returns:
        Número CNJ normalizado ou None se inválido
    """
    # Remove espaços
    numero = numero.strip()

    # Tenta diferentes padrões
    patterns = [
        r"(\d{7})-?(\d{2})\.?(\d{4})\.?(\d)\.?(\d{2})\.?(\d{4})",
        r"(\d{7})(\d{2})(\d{4})(\d)(\d{2})(\d{4})",
    ]

    for pattern in patterns:
        match = re.match(pattern, numero)
        if match:
            return f"{match.group(1)}-{match.group(2)}.{match.group(3)}.{match.group(4)}.{match.group(5)}.{match.group(6)}"

    return None
