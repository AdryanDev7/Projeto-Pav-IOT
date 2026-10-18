from flask import Blueprint
from flask_restful import Api

from repositories.localizacao_repository import LocalizacaoRepository
from repositories.sensor_repository import SensorRepository
from repositories.leitura_repository import LeituraRepository
from repositories.anomalia_repository import AnomaliaRepository

from services.localizacao_service import LocalizacaoService
from services.sensor_service import SensorService
from services.leitura_service import LeituraService
from services.anomalia_service import AnomaliaService
from services.estatistica_service import EstatisticaService

from routes.localizacao_routes import registrar_rotas_localizacao
from routes.sensor_routes import registrar_rotas_sensor
from routes.leitura_routes import registrar_rotas_leitura
from routes.anomalia_routes import registrar_rotas_anomalia


def registrar_rotas(app):
    """Monta repositórios -> services (injeção de dependência) e registra os endpoints em /api."""
    localizacao_repo = LocalizacaoRepository()
    sensor_repo = SensorRepository()
    leitura_repo = LeituraRepository()
    anomalia_repo = AnomaliaRepository()

    localizacao_service = LocalizacaoService(localizacao_repo, sensor_repo)
    sensor_service = SensorService(sensor_repo, localizacao_repo)
    leitura_service = LeituraService(leitura_repo, sensor_repo)
    anomalia_service = AnomaliaService(anomalia_repo, leitura_repo)
    estatistica_service = EstatisticaService(sensor_repo, leitura_repo, anomalia_repo)

    blueprint = Blueprint("api", __name__, url_prefix="/api")
    api = Api(blueprint)

    registrar_rotas_localizacao(api, localizacao_service)
    registrar_rotas_sensor(api, sensor_service, estatistica_service)
    registrar_rotas_leitura(api, leitura_service)
    registrar_rotas_anomalia(api, anomalia_service)

    app.register_blueprint(blueprint)
