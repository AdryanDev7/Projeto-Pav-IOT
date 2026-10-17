from config.database import db

class Sensor(db.Model):
    __tablename__ = 'sensores'
    
    id = db.Column(db.Integer, primary_key=True)
    codigo_serial = db.Column(db.String(50), unique=True, nullable=False)
    tipo = db.Column(db.String(50), nullable=False)
    status = db.Column(db.String(20), nullable=False, default='Ativo')
    localizacao_id = db.Column(db.Integer, db.ForeignKey('localizacoes.id'), nullable=False)
    nivel_bateria = db.Column(db.Integer, nullable=False) 
    
    leituras = db.relationship('LeituraSensor', backref='sensor', lazy=True)