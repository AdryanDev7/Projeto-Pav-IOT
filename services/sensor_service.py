from entities.sensor import Sensor
from services import validadores
from services.base_service import BaseService
from services.exceptions import RegraNegocioError

STATUS_VALIDOS = ("Ativo", "Inativo", "Em Manutenção")


class SensorService(BaseService):
    _ENTIDADE = Sensor
    _MSG_NAO_ENCONTRADO = "Sensor não encontrado."
    _MSG_INTEGRIDADE = "Violação de integridade: código serial duplicado ou localização inexistente."

    def __init__(self, repositorio, localizacao_repositorio):
        super().__init__(repositorio)
        self._localizacao_repo = localizacao_repositorio

    def _validar(self, dados, id_atual=None):
        validadores.exigir_campos(dados, ("codigo_serial", "tipo", "localizacao_id", "nivel_bateria"))  # RN07
        codigo = validadores.texto(dados, "codigo_serial", 50)
        tipo = validadores.texto(dados, "tipo", 50)
        localizacao_id = validadores.inteiro(dados, "localizacao_id")
        bateria = validadores.inteiro(dados, "nivel_bateria")
        status = dados.get("status") or "Ativo"

        # RN04: bateria entre 0 e 100
        if not 0 <= bateria <= 100:
            raise RegraNegocioError("O nível de bateria deve estar entre 0 e 100.")

        # RN05: status controlado
        if status not in STATUS_VALIDOS:
            raise RegraNegocioError("Status inválido. Use: " + ", ".join(STATUS_VALIDOS) + ".")

        # RN03: o sensor só pode ser associado a uma localização que existe
        if self._localizacao_repo.buscar_por_id(localizacao_id) is None:
            raise RegraNegocioError("A localização informada não existe.")

        # RN02: código serial único
        existente = self._repo.buscar_por_codigo_serial(codigo)
        if existente is not None and existente.id != id_atual:
            raise RegraNegocioError("Já existe um sensor com este código serial.")

        return {
            "codigo_serial": codigo,
            "tipo": tipo,
            "status": status,
            "localizacao_id": localizacao_id,
            "nivel_bateria": bateria,
        }
    # Excluir sensor: leituras e anomalias saem em cascata (ON DELETE CASCADE no banco).
