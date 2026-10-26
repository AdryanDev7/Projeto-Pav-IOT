"""Configurações gerais. Tudo que é 'número mágico' das regras de negócio fica aqui
e pode ser alterado por variável de ambiente (útil para demonstrar na apresentação
sem esperar 5 ou 15 minutos)."""
import os
from datetime import datetime, timezone


def agora() -> datetime:
    """Data/hora atual em UTC, sem fuso (naive), para gravar de forma consistente no banco."""
    return datetime.now(timezone.utc).replace(tzinfo=None)


def _inteiro(nome: str, padrao: int) -> int:
    return int(os.getenv(nome, str(padrao)))


DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://iot:iot123@localhost:5432/iotdb")

JANELA_DELTA_SEGUNDOS = _inteiro("JANELA_DELTA_SEGUNDOS", 5)        # regra 2
PERSISTENCIA_LEITURAS = _inteiro("PERSISTENCIA_LEITURAS", 3)        # regra 3
FATOR_WATCHDOG = _inteiro("FATOR_WATCHDOG", 3)                      # regra 4 (3x o intervalo)
AGREGACAO_SEGUNDOS = _inteiro("AGREGACAO_SEGUNDOS", 300)            # regra 5 (5 min)
DIAS_CALIBRACAO = _inteiro("DIAS_CALIBRACAO", 180)                  # regra 7
SEGUNDOS_ESCALONAMENTO = _inteiro("SEGUNDOS_ESCALONAMENTO", 900)    # regra 9 (15 min)
INTERVALO_JOBS_SEGUNDOS = _inteiro("INTERVALO_JOBS_SEGUNDOS", 60)   # frequência das rotinas
