from config.database import db
from entities.sensor import Sensor
from repositories.base_repository import BaseRepository


class SensorRepository(BaseRepository):
    def __init__(self):
        super().__init__(Sensor)

    def buscar_por_codigo_serial(self, codigo_serial):
        return db.session.query(Sensor).filter_by(codigo_serial=codigo_serial).first()

    def existe_por_localizacao(self, localizacao_id):
        consulta = db.session.query(Sensor).filter_by(localizacao_id=localizacao_id)
        return db.session.query(consulta.exists()).scalar()
