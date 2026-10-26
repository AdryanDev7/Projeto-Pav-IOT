from entities.models import Manutencao, Sensor
from repositories.base_repository import BaseRepository


class ManutencaoRepository(BaseRepository):
    def __init__(self, db):
        super().__init__(db, Manutencao)

    def listar_filtrado(self, zona=None):
        consulta = self._db.query(Manutencao)
        if zona:
            consulta = consulta.join(Sensor, Sensor.id == Manutencao.sensor_id).filter(Sensor.zona == zona)
        return consulta.order_by(Manutencao.data_afericao.desc()).all()

    def ultima_afericao(self, sensor_id: int):
        return (self._db.query(Manutencao)
                .filter(Manutencao.sensor_id == sensor_id)
                .order_by(Manutencao.data_afericao.desc()).first())
