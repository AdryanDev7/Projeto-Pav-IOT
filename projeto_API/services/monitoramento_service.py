"""Rotinas periódicas em segundo plano: watchdog (regra 4) e escalonamento (regra 9)."""
import logging
from datetime import timedelta

from config import settings
from config.settings import agora

log_eventos = logging.getLogger("iot.eventos")
log_notificacoes = logging.getLogger("iot.notificacoes")


class MonitoramentoService:
    def __init__(self, sensores, alertas, operadores):
        self._sensores = sensores
        self._alertas = alertas
        self._operadores = operadores

    def verificar_inatividade(self):
        """REGRA 4: sensor sem enviar dados por 3x o seu intervalo vira OFFLINE."""
        momento = agora()
        for sensor in self._sensores.ativos_online():
            if sensor.ultima_comunicacao is None:
                continue                       # nunca enviou nada: não há o que comparar
            limite = timedelta(seconds=settings.FATOR_WATCHDOG * sensor.intervalo_segundos)
            if momento - sensor.ultima_comunicacao > limite:
                sensor.status = "OFFLINE"
                log_eventos.warning(f"WATCHDOG sensor_id={sensor.id} '{sensor.nome}' -> OFFLINE "
                                    f"(sem dados há mais de {int(limite.total_seconds())}s)")
        self._sensores.confirmar()

    def escalonar_alertas(self):
        """REGRA 9: alerta ALTA não reconhecido no prazo é escalonado para a supervisão."""
        corte = agora() - timedelta(seconds=settings.SEGUNDOS_ESCALONAMENTO)
        supervisores = ", ".join(s.nome for s in self._operadores.supervisores()) or "(nenhum cadastrado)"
        for alerta in self._alertas.altos_sem_reconhecimento_antes_de(corte):
            alerta.status = "ESCALONADO"
            log_notificacoes.error(
                f"ESCALONAMENTO alerta_id={alerta.id} sensor_id={alerta.sensor_id}: sem reconhecimento "
                f"em {settings.SEGUNDOS_ESCALONAMENTO}s. Aviso enviado à supervisão: {supervisores}")
        self._alertas.confirmar()
