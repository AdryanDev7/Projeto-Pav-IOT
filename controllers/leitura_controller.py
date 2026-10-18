from flask import request

from controllers.base_controller import ListaController, ItemController


class LeituraListaController(ListaController):
    _MSG_CRIADO = "Leitura registada com sucesso!"

    def get(self):
        # Filtros opcionais: /leituras?sensor_id=1&inicio=2026-10-01 00:00:00&fim=2026-10-31 23:59:59
        leituras = self._service.listar_filtrado(
            sensor_id=request.args.get("sensor_id"),
            inicio=request.args.get("inicio"),
            fim=request.args.get("fim"),
        )
        return leituras, 200


class LeituraItemController(ItemController):
    _MSG_ATUALIZADO = "Leitura atualizada com sucesso!"
    _MSG_EXCLUIDO = "Leitura deletada com sucesso!"
