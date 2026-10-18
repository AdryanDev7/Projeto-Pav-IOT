from entities.localizacao import Localizacao
from repositories.base_repository import BaseRepository


class LocalizacaoRepository(BaseRepository):
    def __init__(self):
        super().__init__(Localizacao)
