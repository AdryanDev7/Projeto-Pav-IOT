"""Agenda as rotinas de monitoramento com APScheduler (thread em segundo plano)."""
import logging

from apscheduler.schedulers.background import BackgroundScheduler

from config.database import SessionLocal
from config.settings import INTERVALO_JOBS_SEGUNDOS
from repositories.alerta_repository import AlertaRepository
from repositories.operador_repository import OperadorRepository
from repositories.sensor_repository import SensorRepository
from services.monitoramento_service import MonitoramentoService

log = logging.getLogger("iot.eventos")


def _executar(nome_metodo: str) -> None:
    """Cada execução abre a sua própria sessão (não há requisição HTTP aqui)."""
    db = SessionLocal()
    try:
        servico = MonitoramentoService(SensorRepository(db), AlertaRepository(db),
                                       OperadorRepository(db))
        getattr(servico, nome_metodo)()
    except Exception:
        db.rollback()
        log.exception(f"Falha na rotina {nome_metodo}")
    finally:
        db.close()


def criar_agendador() -> BackgroundScheduler:
    agendador = BackgroundScheduler()
    agendador.add_job(_executar, "interval", seconds=INTERVALO_JOBS_SEGUNDOS,
                      args=["verificar_inatividade"], id="watchdog")
    agendador.add_job(_executar, "interval", seconds=INTERVALO_JOBS_SEGUNDOS,
                      args=["escalonar_alertas"], id="escalonamento")
    return agendador
