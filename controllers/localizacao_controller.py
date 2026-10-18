from controllers.base_controller import ListaController, ItemController


class LocalizacaoListaController(ListaController):
    _MSG_CRIADO = "Localização criada com sucesso!"


class LocalizacaoItemController(ItemController):
    _MSG_ATUALIZADO = "Localização atualizada com sucesso!"
    _MSG_EXCLUIDO = "Localização deletada com sucesso!"
