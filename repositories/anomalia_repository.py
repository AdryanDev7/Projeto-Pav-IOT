from config.database import db
from entities.anomalia import Anomalia
from entities.leitura import LeituraSensor
from repositories.base_repository import BaseRepository


class AnomaliaRepository(BaseRepository):
    def __init__(self):
        super().__init__(Anomalia)

    def contar_por_sensor(self, sensor_id, inicio=None, fim=None):
        """Quantas anomalias existem nas leituras de um sensor (com período opcional)."""
        consulta = (
            db.session.query(Anomalia)
            .join(LeituraSensor, Anomalia.leitura_id == LeituraSensor.id)
            .filter(LeituraSensor.sensor_id == sensor_id)
        )
        if inicio is not None:
            consulta = consulta.filter(LeituraSensor.data_hora >= inicio)
        if fim is not None:
            consulta = consulta.filter(LeituraSensor.data_hora <= fim)
        return consulta.count()
