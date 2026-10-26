"""Cria os loggers do sistema. Os arquivos ficam em ./logs (mapeado como volume no Docker)."""
import logging
import os

ARQUIVOS = {
    "iot.rejeitadas": "logs/leituras_rejeitadas.log",   # regra 1
    "iot.notificacoes": "logs/notificacoes.log",        # regra 9
    "iot.eventos": "logs/eventos.log",                  # alertas, atuadores, watchdog
}


def configurar_logs() -> None:
    os.makedirs("logs", exist_ok=True)
    formato = logging.Formatter("%(asctime)s | %(levelname)s | %(message)s")
    for nome, arquivo in ARQUIVOS.items():
        logger = logging.getLogger(nome)
        if logger.handlers:          # evita duplicar handlers se chamado duas vezes
            continue
        logger.setLevel(logging.INFO)
        for handler in (logging.FileHandler(arquivo, encoding="utf-8"), logging.StreamHandler()):
            handler.setFormatter(formato)
            logger.addHandler(handler)
        logger.propagate = False
