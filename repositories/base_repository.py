from config.database import db


class BaseRepository:
    """
    Repositório genérico (HERANÇA): as operações de banco comuns a todas as entidades.
    Os repositórios específicos herdam daqui e só acrescentam consultas próprias.
    """

    def __init__(self, modelo):
        # CONSTRUTOR + ENCAPSULAMENTO: o modelo fica num atributo "privado" (_modelo)
        self._modelo = modelo

    def listar_todos(self):
        return db.session.query(self._modelo).order_by(self._modelo.id).all()

    def buscar_por_id(self, id):
        return db.session.get(self._modelo, id)

    def salvar(self, entidade):
        try:
            db.session.add(entidade)
            db.session.commit()
            return entidade
        except Exception:
            db.session.rollback()  # sem isto a sessão fica "quebrada" após um erro do banco
            raise

    def excluir(self, entidade):
        try:
            db.session.delete(entidade)
            db.session.commit()
        except Exception:
            db.session.rollback()
            raise
