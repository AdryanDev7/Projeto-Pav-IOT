from entities.models import Leitura, Sensor
from repositories.base_repository import BaseRepository


class SensorRepository(BaseRepository):
    def __init__(self, db):
        super().__init__(db, Sensor)

    def listar_filtrado(self, zona=None):
        consulta = self._db.query(Sensor)
        if zona:
            consulta = consulta.filter(Sensor.zona == zona)
        return consulta.order_by(Sensor.id).all()

    def contar_leituras(self, sensor_id: int) -> int:
        return self._db.query(Leitura).filter(Leitura.sensor_id == sensor_id).count()

    def ativos_online(self):
        """Sensores ativos que ainda não estão OFFLINE (usado pelo watchdog)."""
        return (self._db.query(Sensor)
                .filter(Sensor.ativo.is_(True), Sensor.status != "OFFLINE")
                .all())
