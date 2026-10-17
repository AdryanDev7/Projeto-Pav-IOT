from entities.models import Localizacao
from config.database import db

class LocalizacaoRepository:
    @staticmethod
    def salvar(localizacao):
        db.session.add(localizacao)
        db.session.commit()
        return localizacao

    @staticmethod
    def listar_todas():
        return Localizacao.query.all()

    @staticmethod
    def buscar_por_id(localizacao_id):
        return Localizacao.query.get(localizacao_id)

    @staticmethod
    def deletar(localizacao):
        db.session.delete(localizacao)
        db.session.commit()

    @staticmethod
    def atualizar():
        db.session.commit()