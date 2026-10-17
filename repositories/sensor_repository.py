from entities.sensor import Sensor
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
    def buscar_por_id(id):
        return Sensor.query.get(id)

    @staticmethod
    def excluir(sensor):
        db.session.delete(sensor)
        db.session.commit()