from config.database import db
from entities.base import EntidadeBase


class Anomalia(EntidadeBase):
    __tablename__ = 'anomalias'

    CAMPOS_EDITAVEIS = ("leitura_id", "descricao_alerta", "severidade")

    leitura_id = db.Column(
        db.Integer,
        db.ForeignKey('leituras_sensores.id', ondelete='CASCADE'),
        nullable=False,
    )
    descricao_alerta = db.Column(db.Text, nullable=False)
    severidade = db.Column(db.String(20), nullable=False)

    def to_dict(self):
        return {
            "id": self.id,
            "leitura_id": self.leitura_id,
            "descricao_alerta": self.descricao_alerta,
            "severidade": self.severidade,
        }
