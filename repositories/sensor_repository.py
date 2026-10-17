from entities.models import Sensor
from config.database import db

class SensorRepository:
    @staticmethod
    def salvar(sensor):
        db.session.add(sensor)
        db.session.commit()
        return sensor

    @staticmethod
    def listar_todos():
        return Sensor.query.all()

    @staticmethod
    def buscar_por_id(sensor_id):
        return Sensor.query.get(sensor_id)

    @staticmethod
    def deletar(sensor):
        db.session.delete(sensor)
        db.session.commit()