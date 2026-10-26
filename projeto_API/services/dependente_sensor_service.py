"""Base para entidades que pertencem a um Sensor (Manutenção e Alerta).
A zona do recurso é a zona do sensor dono dele (regra 10)."""
from config.excecoes import NaoEncontradoErro
from services.autorizacao import exigir_zona
from services.base_service import BaseService


class DependenteSensorService(BaseService):
    def __init__(self, repo, sensor_repo):
        super().__init__(repo)
        self._sensores = sensor_repo

    def _sensor_ou_404(self, sensor_id):
        sensor = self._sensores.buscar(sensor_id)
        if sensor is None:
            raise NaoEncontradoErro(f"Sensor {sensor_id} não encontrado.")
        return sensor

    def _validar(self, dados, operador):
        sensor_id = getattr(dados, "sensor_id", None)
        if sensor_id is not None:
            exigir_zona(operador, self._sensor_ou_404(sensor_id).zona)

    def _montar(self, dados):
        obj = super()._montar(dados)
        obj.sensor = self._sensor_ou_404(obj.sensor_id)
        return obj

    def _autorizar(self, operador, obj, escrita):
        exigir_zona(operador, obj.sensor.zona)
