from controllers.localizacao_controller import LocalizacaoListaController, LocalizacaoItemController


def registrar_rotas_localizacao(api, service):
    kwargs = {"service": service}
    api.add_resource(LocalizacaoListaController, "/localizacoes", resource_class_kwargs=kwargs)
    api.add_resource(LocalizacaoItemController, "/localizacoes/<int:registro_id>", resource_class_kwargs=kwargs)
