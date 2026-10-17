from entities.models import LeituraSensor
from config.database import db

class LeituraRepository:
    @staticmethod
    def salvar(leitura):
        db.session.add(leitura)
        db.session.commit()
        return leitura

    @staticmethod
    def listar_todas():
        return LeituraSensor.query.all()

    @staticmethod
    def buscar_por_id(leitura_id):
        return LeituraSensor.query.get(leitura_id)

    @staticmethod
    def deletar(leitura):
        db.session.delete(leitura)
        db.session.commit()