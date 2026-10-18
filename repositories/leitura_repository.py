from config.database import db
from entities.leitura import LeituraSensor
from repositories.base_repository import BaseRepository


class LeituraRepository(BaseRepository):
    def __init__(self):
        super().__init__(LeituraSensor)

    def listar_filtrado(self, sensor_id=None, inicio=None, fim=None):
        """Filtros opcionais por sensor e por período (data_hora entre inicio e fim)."""
        consulta = db.session.query(LeituraSensor)
        if sensor_id is not None:
            consulta = consulta.filter(LeituraSensor.sensor_id == sensor_id)
        if inicio is not None:
            consulta = consulta.filter(LeituraSensor.data_hora >= inicio)
        if fim is not None:
            consulta = consulta.filter(LeituraSensor.data_hora <= fim)
        return consulta.order_by(LeituraSensor.data_hora, LeituraSensor.id).all()
