from config.database import db

class LeituraSensor(db.Model):
    __tablename__ = 'leituras_sensores'
    
    id = db.Column(db.Integer, primary_key=True)
    sensor_id = db.Column(db.Integer, db.ForeignKey('sensores.id'), nullable=False)
    valor = db.Column(db.Numeric(10, 4), nullable=False)
    nivel_bateria = db.Column(db.Integer, nullable=False)
    data_hora = db.Column(db.DateTime, nullable=False)
    
    anomalias = db.relationship('Anomalia', backref='leitura', lazy=True)