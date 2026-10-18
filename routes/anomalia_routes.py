from controllers.anomalia_controller import AnomaliaListaController, AnomaliaItemController


def registrar_rotas_anomalia(api, service):
    kwargs = {"service": service}
    api.add_resource(AnomaliaListaController, "/anomalias", resource_class_kwargs=kwargs)
    api.add_resource(AnomaliaItemController, "/anomalias/<int:registro_id>", resource_class_kwargs=kwargs)
