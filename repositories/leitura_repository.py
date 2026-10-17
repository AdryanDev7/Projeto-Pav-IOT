from entities.leitura import LeituraSensor
from config.database import db

class LeituraRepository:
    @staticmethod
    def salvar(leitura):
        db.session.add(leitura)
        db.session.commit()
        return leitura

    @staticmethod
    def listar_todos():
        return LeituraSensor.query.all()

    @staticmethod
    def buscar_por_id(id):
        return LeituraSensor.query.get(id)

    @staticmethod
    def excluir(leitura):
        db.session.delete(leitura)
        db.session.commit()