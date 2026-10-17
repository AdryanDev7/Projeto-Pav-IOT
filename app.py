from flask import Flask
from config.database import init_app, db
from routes.localizacao_routes import localizacao_bp
from routes.sensor_routes import sensor_bp
from routes.leitura_routes import leitura_bp
from routes.anomalia_routes import anomalia_bp

app = Flask(__name__)

# Inicializa a base de dados a partir da camada de config
init_app(app)

# Registo dos Blueprints (Rotas)
app.register_blueprint(localizacao_bp)
app.register_blueprint(sensor_bp)
app.register_blueprint(leitura_bp)
app.register_blueprint(anomalia_bp)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Cria as tabelas se não existirem
    app.run(host='0.0.0.0', port=5000, debug=True)