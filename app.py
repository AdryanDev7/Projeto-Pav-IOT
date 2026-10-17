from flask import Flask
from config.database import db
from entities.models import Localizacao, Sensor, LeituraSensor, Anomalia  # Importa os modelos para o db.create_all()
from routes.sensor_routes import sensor_bp
from routes.localizacao_routes import localizacao_bp
from routes.leitura_routes import leitura_bp
from routes.anomalia_routes import anomalia_bp

app = Flask(__name__)

# Configuração da conexão com o PostgreSQL do Docker (porta 5433)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://postgres:123@localhost:5433/iot_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

# Registra os Blueprints (rotas) da API
app.register_blueprint(sensor_bp)
app.register_blueprint(localizacao_bp)
app.register_blueprint(leitura_bp)
app.register_blueprint(anomalia_bp)

@app.route('/')
def home():
    return {"status": "API de Sensores IoT a funcionar com sucesso!"}

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True, port=5000)