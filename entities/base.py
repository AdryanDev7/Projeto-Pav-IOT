from config.database import db


class EntidadeBase(db.Model):
    """
    Classe-base abstrata de todas as entidades (HERANÇA).
    Toda entidade tem um id e sabe se converter em dicionário (POLIMORFISMO:
    cada filha implementa o seu próprio to_dict).
    """
    __abstract__ = True

    # Campos que o PUT pode alterar (cada entidade define os seus)
    CAMPOS_EDITAVEIS = ()

    id = db.Column(db.Integer, primary_key=True)

    def to_dict(self):
        raise NotImplementedError("Cada entidade deve implementar to_dict().")
