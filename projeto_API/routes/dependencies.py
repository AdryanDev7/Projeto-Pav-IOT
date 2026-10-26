"""Injeção de dependências do FastAPI: monta repository -> service -> controller por requisição."""
from typing import Optional

from fastapi import Depends, Header

from config.database import get_db
from config.excecoes import NaoAutenticadoErro
from controllers.alerta_controller import AlertaController
from controllers.analise_controller import AnaliseController
from controllers.leitura_controller import LeituraController
from controllers.manutencao_controller import ManutencaoController
from controllers.operador_controller import OperadorController
from controllers.sensor_controller import SensorController
from repositories.alerta_repository import AlertaRepository
from repositories.leitura_repository import LeituraRepository
from repositories.manutencao_repository import ManutencaoRepository
from repositories.operador_repository import OperadorRepository
from repositories.sensor_repository import SensorRepository
from services.alerta_service import AlertaService
from services.analise_service import AnaliseService
from services.leitura_service import LeituraService
from services.manutencao_service import ManutencaoService
from services.operador_service import OperadorService
from services.sensor_service import SensorService


def get_operador(x_operador_id: Optional[int] = Header(default=None), db=Depends(get_db)):
    """Identifica quem está chamando pelo cabeçalho X-Operador-Id.
    Simplificação didática: em produção seria login com senha + token JWT."""
    if x_operador_id is None:
        raise NaoAutenticadoErro("Cabeçalho 'X-Operador-Id' é obrigatório.")
    operador = OperadorRepository(db).buscar(x_operador_id)
    if operador is None:
        raise NaoAutenticadoErro(f"Operador {x_operador_id} não existe.")
    return operador


def get_sensor_controller(db=Depends(get_db)):
    return SensorController(SensorService(SensorRepository(db)))


def get_operador_controller(db=Depends(get_db)):
    return OperadorController(OperadorService(OperadorRepository(db)))


def get_manutencao_controller(db=Depends(get_db)):
    return ManutencaoController(ManutencaoService(ManutencaoRepository(db), SensorRepository(db)))


def get_alerta_controller(db=Depends(get_db)):
    return AlertaController(AlertaService(AlertaRepository(db), SensorRepository(db)))


def get_leitura_controller(db=Depends(get_db)):
    servico = LeituraService(LeituraRepository(db), SensorRepository(db),
                             AlertaRepository(db), ManutencaoRepository(db))
    return LeituraController(servico)


def get_analise_controller(db=Depends(get_db)):
    return AnaliseController(AnaliseService(LeituraRepository(db), SensorRepository(db)))
