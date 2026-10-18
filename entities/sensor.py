from config.database import db
from entities.base import EntidadeBase


class Sensor(EntidadeBase):
    __tablename__ = 'sensores'

    CAMPOS_EDITAVEIS = ("codigo_serial", "tipo", "status", "localizacao_id", "nivel_bateria")

    codigo_serial = db.Column(db.String(50), unique=True, nullable=False)
    tipo = db.Column(db.String(50), nullable=False)
    status = db.Column(db.String(20), nullable=False, default='Ativo')
    localizacao_id = db.Column(
        db.Integer,
        db.ForeignKey('localizacoes.id', ondelete='RESTRICT'),
        nullable=False,
    )
    nivel_bateria = db.Column(db.Integer, nullable=False)

    # Ao apagar um sensor, o banco apaga as leituras em cascata (ON DELETE CASCADE).
    leituras = db.relationship(
        'LeituraSensor', backref='sensor', lazy=True,
        cascade='all, delete-orphan', passive_deletes=True,
    )

    def to_dict(self):
        return {
            "id": self.id,
            "codigo_serial": self.codigo_serial,
            "tipo": self.tipo,
            "status": self.status,
            "localizacao_id": self.localizacao_id,
            "nivel_bateria": self.nivel_bateria,
        }
