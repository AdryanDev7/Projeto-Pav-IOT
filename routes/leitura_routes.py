from controllers.leitura_controller import LeituraListaController, LeituraItemController


def registrar_rotas_leitura(api, service):
    kwargs = {"service": service}
    api.add_resource(LeituraListaController, "/leituras", resource_class_kwargs=kwargs)
    api.add_resource(LeituraItemController, "/leituras/<int:registro_id>", resource_class_kwargs=kwargs)
