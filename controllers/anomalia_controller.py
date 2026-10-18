from controllers.base_controller import ListaController, ItemController


class AnomaliaListaController(ListaController):
    _MSG_CRIADO = "Anomalia registada com sucesso!"


class AnomaliaItemController(ItemController):
    _MSG_ATUALIZADO = "Anomalia atualizada com sucesso!"
    _MSG_EXCLUIDO = "Anomalia deletada com sucesso!"
