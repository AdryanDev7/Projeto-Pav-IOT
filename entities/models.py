from config.database import db

class Localizacao(db.Model):
    __tablename__ = 'localizacoes'
    
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    setor = db.Column(db.String(50), nullable=False)
    latitude = db.Column(db.Numeric(10, 8), nullable=False)
    longitude = db.Column(db.Numeric(11, 8), nullable=False)
    
    sensores = db.relationship('Sensor', backref='localizacao', lazy=True)

class Sensor(db.Model):
    __tablename__ = 'sensores'
    
    id = db.Column(db.Integer, primary_key=True)
    codigo_serial = db.Column(db.String(50), unique=True, nullable=False)
    tipo = db.Column(db.String(50), nullable=False)
    status = db.Column(db.String(20), nullable=False, default='Ativo')
    localizacao_id = db.Column(db.Integer, db.ForeignKey('localizacoes.id'), nullable=False)
    
    leituras = db.relationship('LeituraSensor', backref='sensor', lazy=True)

class LeituraSensor(db.Model):
    __tablename__ = 'leituras_sensores'
    
    id = db.Column(db.Integer, primary_key=True)
    sensor_id = db.Column(db.Integer, db.ForeignKey('sensores.id'), nullable=False)
    valor = db.Column(db.Numeric(10, 4), nullable=False)
    nivel_bateria = db.Column(db.Integer, nullable=False)
    data_hora = db.Column(db.DateTime, nullable=False)
    
    anomalias = db.relationship('Anomalia', backref='leitura', lazy=True)

class Anomalia(db.Model):
    __tablename__ = 'anomalias'
    
    id = db.Column(db.Integer, primary_key=True)
    leitura_id = db.Column(db.Integer, db.ForeignKey('leituras_sensores.id'), nullable=False)
    descricao_alerta = db.Column(db.Text, nullable=False)
    severidade = db.Column(db.String(20), nullable=False)