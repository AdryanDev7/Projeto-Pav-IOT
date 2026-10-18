import statistics

from services import validadores
from services.exceptions import NaoEncontradoError


class EstatisticaService:
    """Análise de dados: estatísticas descritivas das leituras de um sensor."""

    def __init__(self, sensor_repositorio, leitura_repositorio, anomalia_repositorio):
        self._sensor_repo = sensor_repositorio
        self._leitura_repo = leitura_repositorio
        self._anomalia_repo = anomalia_repositorio

    def do_sensor(self, sensor_id, inicio=None, fim=None):
        sensor = self._sensor_repo.buscar_por_id(sensor_id)
        if sensor is None:
            raise NaoEncontradoError("Sensor não encontrado.")

        inicio = validadores.data_hora(inicio, "inicio") if inicio else None
        fim = validadores.data_hora(fim, "fim") if fim else None

        leituras = self._leitura_repo.listar_filtrado(sensor_id, inicio, fim)
        valores = [float(leitura.valor) for leitura in leituras]

        resultado = {
            "sensor_id": sensor.id,
            "codigo_serial": sensor.codigo_serial,
            "total_leituras": len(valores),
            "media": None,
            "minimo": None,
            "maximo": None,
            "desvio_padrao": None,
            "total_anomalias": self._anomalia_repo.contar_por_sensor(sensor_id, inicio, fim),
        }
        if valores:
            resultado["media"] = round(statistics.mean(valores), 4)
            resultado["minimo"] = min(valores)
            resultado["maximo"] = max(valores)
            resultado["desvio_padrao"] = round(statistics.pstdev(valores), 4)
        return resultado
