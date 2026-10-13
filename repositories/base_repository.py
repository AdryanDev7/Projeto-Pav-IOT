from config.database import db

class BaseRepository:
    @staticmethod
    def salvar(model):
        db.session.add(model)
        db.session.commit()
        return model

    @staticmethod
    def deletar(model):
        db.session.delete(model)
        db.session.commit()

    @staticmethod
    def atualizar():
        db.session.commit()