"""Repositório genérico. Os repositórios específicos HERDAM desta classe (herança)."""


class BaseRepository:
    def __init__(self, db, modelo):
        self._db = db          # encapsulamento: ninguém de fora mexe na sessão
        self.modelo = modelo

    def listar(self):
        return self._db.query(self.modelo).order_by(self.modelo.id).all()

    def listar_filtrado(self, zona=None):
        """Por padrão ignora a zona. Quem tem relação com zona sobrescreve (polimorfismo)."""
        return self.listar()

    def buscar(self, id_):
        return self._db.get(self.modelo, id_)

    def adicionar(self, obj):
        """Coloca na sessão SEM gravar. Permite agrupar várias mudanças em um commit só."""
        self._db.add(obj)
        return obj

    def confirmar(self):
        self._db.commit()

    def recarregar(self, obj):
        self._db.refresh(obj)

    def salvar(self, obj):
        self._db.add(obj)
        self._db.commit()
        self._db.refresh(obj)
        return obj

    def remover(self, obj):
        self._db.delete(obj)
        self._db.commit()
