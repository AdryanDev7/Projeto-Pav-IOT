from controllers.sensor_controller import (
    SensorListaController,
    SensorItemController,
    SensorEstatisticaController,
)


def registrar_rotas_sensor(api, service, estatistica_service):
    kwargs = {"service": service}
    api.add_resource(SensorListaController, "/sensores", resource_class_kwargs=kwargs)
    api.add_resource(SensorItemController, "/sensores/<int:registro_id>", resource_class_kwargs=kwargs)
    api.add_resource(
        SensorEstatisticaController,
        "/sensores/<int:sensor_id>/estatisticas",
        resource_class_kwargs={"service": estatistica_service},
    )
