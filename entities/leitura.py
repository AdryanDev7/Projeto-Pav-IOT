from config.database import db
from entities.base import EntidadeBase


class LeituraSensor(EntidadeBase):
    __tablename__ = 'leituras_sensores'

    CAMPOS_EDITAVEIS = ("sensor_id", "valor", "nivel_bateria", "data_hora")

    sensor_id = db.Column(
        db.Integer,
        db.ForeignKey('sensores.id', ondelete='CASCADE'),
        nullable=False,
    )
    valor = db.Column(db.Numeric(10, 4), nullable=False)
    nivel_bateria = db.Column(db.Integer, nullable=False)
    data_hora = db.Column(db.DateTime, nullable=False)

    anomalias = db.relationship(
        'Anomalia', backref='leitura', lazy=True,
        cascade='all, delete-orphan', passive_deletes=True,
    )

    def to_dict(self):
        return {
            "id": self.id,
            "sensor_id": self.sensor_id,
            "valor": float(self.valor),
            "nivel_bateria": self.nivel_bateria,
            "data_hora": self.data_hora.strftime("%Y-%m-%d %H:%M:%S"),
        }
