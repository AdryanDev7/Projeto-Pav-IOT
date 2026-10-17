from config.database import db

class Localizacao(db.Model):
    __tablename__ = 'localizacoes'
    
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    setor = db.Column(db.String(50), nullable=False)
    latitude = db.Column(db.Numeric(10, 8), nullable=False)
    longitude = db.Column(db.Numeric(11, 8), nullable=False)
    
    sensores = db.relationship('Sensor', backref='localizacao', lazy=True)