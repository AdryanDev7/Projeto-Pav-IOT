from entities.localizacao import Localizacao
from services import validadores
from services.base_service import BaseService
from services.exceptions import RegraNegocioError


class LocalizacaoService(BaseService):
    _ENTIDADE = Localizacao
    _MSG_NAO_ENCONTRADO = "Localização não encontrada."
    _MSG_EXCLUSAO_BLOQUEADA = "Não é possível excluir esta localização pois existem sensores associados."

    def __init__(self, repositorio, sensor_repositorio):
        super().__init__(repositorio)
        self._sensor_repo = sensor_repositorio

    def _validar(self, dados, id_atual=None):
        validadores.exigir_campos(dados, ("nome", "setor", "latitude", "longitude"))  # RN07
        latitude = validadores.decimal(dados, "latitude")
        longitude = validadores.decimal(dados, "longitude")

        # RN01: coordenadas geográficas válidas
        if not -90 <= latitude <= 90:
            raise RegraNegocioError("A latitude deve estar entre -90 e 90.")
        if not -180 <= longitude <= 180:
            raise RegraNegocioError("A longitude deve estar entre -180 e 180.")

        return {
            "nome": validadores.texto(dados, "nome", 100),
            "setor": validadores.texto(dados, "setor", 50),
            "latitude": latitude,
            "longitude": longitude,
        }

    def _antes_de_excluir(self, localizacao):
        # RN10: não apaga localização que ainda tem sensores (evita registros órfãos)
        if self._sensor_repo.existe_por_localizacao(localizacao.id):
            raise RegraNegocioError(self._MSG_EXCLUSAO_BLOQUEADA)
