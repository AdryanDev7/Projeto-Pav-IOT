from entities.models import Leitura, Sensor
from repositories.base_repository import BaseRepository


class LeituraRepository(BaseRepository):
    def __init__(self, db):
        super().__init__(db, Leitura)

    def listar_filtrado(self, sensor_id=None, zona=None, limite=100):
        consulta = self._db.query(Leitura)
        if zona:
            consulta = consulta.join(Sensor, Sensor.id == Leitura.sensor_id).filter(Sensor.zona == zona)
        if sensor_id is not None:
            consulta = consulta.filter(Leitura.sensor_id == sensor_id)
        return (consulta.order_by(Leitura.registrada_em.desc(), Leitura.id.desc())
                .limit(limite).all())

    def _no_periodo(self, sensor_id, inicio, fim):
        consulta = self._db.query(Leitura).filter(Leitura.sensor_id == sensor_id)
        if inicio:
            consulta = consulta.filter(Leitura.registrada_em >= inicio)
        if fim:
            consulta = consulta.filter(Leitura.registrada_em <= fim)
        return consulta

    def validas_no_periodo(self, sensor_id, inicio=None, fim=None):
        """Leituras que contam para as médias oficiais (regra 2: sem SUSPEITA_RUIDO)."""
        return (self._no_periodo(sensor_id, inicio, fim)
                .filter(Leitura.flag != "SUSPEITA_RUIDO")
                .order_by(Leitura.registrada_em).all())

    def contar_ruido(self, sensor_id, inicio=None, fim=None) -> int:
        return (self._no_periodo(sensor_id, inicio, fim)
                .filter(Leitura.flag == "SUSPEITA_RUIDO").count())
