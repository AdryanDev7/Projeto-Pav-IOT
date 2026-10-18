from flask import request

from controllers.base_controller import ListaController, ItemController, RecursoBase


class SensorListaController(ListaController):
    _MSG_CRIADO = "Sensor cadastrado com sucesso!"


class SensorItemController(ItemController):
    _MSG_ATUALIZADO = "Sensor atualizado com sucesso!"
    _MSG_EXCLUIDO = "Sensor deletado com sucesso!"


class SensorEstatisticaController(RecursoBase):
    """GET /sensores/<id>/estatisticas?inicio=...&fim=..."""

    def get(self, sensor_id):
        resultado = self._service.do_sensor(
            sensor_id,
            inicio=request.args.get("inicio"),
            fim=request.args.get("fim"),
        )
        return resultado, 200
