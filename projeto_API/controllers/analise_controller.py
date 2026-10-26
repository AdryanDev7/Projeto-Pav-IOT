class AnaliseController:
    def __init__(self, service):
        self._service = service

    def estatisticas(self, sensor_id, operador, inicio=None, fim=None):
        return self._service.estatisticas(sensor_id, operador, inicio, fim)

    def anomalias(self, sensor_id, operador, limiar=3.0):
        return self._service.anomalias(sensor_id, operador, limiar)
