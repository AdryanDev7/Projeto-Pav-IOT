from flask import Flask
from config.database import db
from entities.models import Localizacao, Sensor, LeituraSensor, Anomalia  # Importa os modelos para o db.create_all()

app = Flask(__name__)

# Configuração da conexão com o PostgreSQL do Docker (ajuste para 5433 na porta se necessário)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://postgres:123@localhost:5432/iot_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

@app.route('/')
def home():
    return {"status": "API de Sensores IoT a funcionar com sucesso!"}

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True, port=5000)