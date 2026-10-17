from entities.models import Anomalia
from config.database import db

class AnomaliaRepository:
    @staticmethod
    def listar_todas():
        return Anomalia.query.all()

    @staticmethod
    def buscar_por_id(anomalia_id):
        return Anomalia.query.get(anomalia_id)

    @staticmethod
    def deletar(anomalia):
        db.session.delete(anomalia)
        db.session.commit()