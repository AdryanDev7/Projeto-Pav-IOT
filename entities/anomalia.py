from config.database import db

class Anomalia(db.Model):
    __tablename__ = 'anomalias'
    
    id = db.Column(db.Integer, primary_key=True)
    leitura_id = db.Column(db.Integer, db.ForeignKey('leituras_sensores.id'), nullable=False)
    descricao_alerta = db.Column(db.Text, nullable=False)
    severidade = db.Column(db.String(20), nullable=False)