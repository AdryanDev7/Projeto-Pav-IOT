from config.database import db
from entities.base import EntidadeBase


class Localizacao(EntidadeBase):
    __tablename__ = 'localizacoes'

    CAMPOS_EDITAVEIS = ("nome", "setor", "latitude", "longitude")

    nome = db.Column(db.String(100), nullable=False)
    setor = db.Column(db.String(50), nullable=False)
    latitude = db.Column(db.Numeric(10, 8), nullable=False)
    longitude = db.Column(db.Numeric(11, 8), nullable=False)

    # passive_deletes='all': o SQLAlchemy NUNCA mexe nos sensores ao apagar a localização.
    # Quem decide é o banco (ON DELETE RESTRICT) e o service (RN10).
    sensores = db.relationship('Sensor', backref='localizacao', lazy=True, passive_deletes='all')

    def to_dict(self):
        return {
            "id": self.id,
            "nome": self.nome,
            "setor": self.setor,
            "latitude": float(self.latitude),
            "longitude": float(self.longitude),
        }
