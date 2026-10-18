"""Funções de validação reutilizadas pelos services (programação estruturada)."""
import math
from datetime import datetime

from services.exceptions import RegraNegocioError


def exigir_campos(dados, campos):
    """RN07: todos os campos obrigatórios precisam estar presentes e não vazios."""
    for campo in campos:
        valor = dados.get(campo)
        if valor is None or (isinstance(valor, str) and not valor.strip()):
            raise RegraNegocioError(f"O campo '{campo}' é obrigatório.")


def texto(dados, campo, tamanho_max):
    valor = dados.get(campo)
    if not isinstance(valor, str):
        raise RegraNegocioError(f"O campo '{campo}' deve ser um texto.")
    valor = valor.strip()
    if len(valor) > tamanho_max:
        raise RegraNegocioError(f"O campo '{campo}' aceita no máximo {tamanho_max} caracteres.")
    return valor


def inteiro(dados, campo):
    valor = dados.get(campo)
    try:
        if isinstance(valor, bool):
            raise ValueError
        if isinstance(valor, float) and not valor.is_integer():
            raise ValueError
        return int(valor)
    except (TypeError, ValueError):
        raise RegraNegocioError(f"O campo '{campo}' deve ser um número inteiro.")


def decimal(dados, campo):
    valor = dados.get(campo)
    try:
        if isinstance(valor, bool):
            raise ValueError
        numero = float(valor)
    except (TypeError, ValueError):
        raise RegraNegocioError(f"O campo '{campo}' deve ser um número válido.")
    if not math.isfinite(numero):  # bloqueia NaN e infinito
        raise RegraNegocioError(f"O campo '{campo}' deve ser um número válido.")
    return numero


def data_hora(valor, campo):
    """Aceita datetime ou texto 'AAAA-MM-DD HH:MM:SS' (também 'AAAA-MM-DDTHH:MM:SS')."""
    if isinstance(valor, datetime):
        resultado = valor
    elif isinstance(valor, str):
        try:
            resultado = datetime.fromisoformat(valor.strip())
        except ValueError:
            raise RegraNegocioError(f"O campo '{campo}' deve estar no formato AAAA-MM-DD HH:MM:SS.")
    else:
        raise RegraNegocioError(f"O campo '{campo}' deve estar no formato AAAA-MM-DD HH:MM:SS.")
    if resultado.tzinfo is not None:
        resultado = resultado.astimezone().replace(tzinfo=None)
    return resultado
