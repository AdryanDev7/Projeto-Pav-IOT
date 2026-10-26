from entities.models import Operador
from repositories.base_repository import BaseRepository


class OperadorRepository(BaseRepository):
    def __init__(self, db):
        super().__init__(db, Operador)

    def supervisores(self):
        return self._db.query(Operador).filter(Operador.perfil == "SUPERVISOR").all()
