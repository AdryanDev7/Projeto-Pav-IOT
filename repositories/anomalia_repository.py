from entities.anomalia import Anomalia
from config.database import db

class AnomaliaRepository:
    @staticmethod
    def salvar(anomalia):
        db.session.add(anomalia)
        db.session.commit()
        return anomalia

    @staticmethod
    def listar_todos():
        return Anomalia.query.all()

    @staticmethod
    def buscar_por_id(id):
        return Anomalia.query.get(id)

    @staticmethod
    def excluir(anomalia):
        db.session.delete(anomalia)
        db.session.commit()