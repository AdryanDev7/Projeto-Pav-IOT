from entities.localizacao import Localizacao
from config.database import db

class LocalizacaoRepository:
    @staticmethod
    def salvar(localizacao):
        db.session.add(localizacao)
        db.session.commit()
        return localizacao

    @staticmethod
    def listar_todos():
        return Localizacao.query.all()

    @staticmethod
    def buscar_por_id(id):
        return Localizacao.query.get(id)

    @staticmethod
    def excluir(localizacao):
        db.session.delete(localizacao)
        db.session.commit()