import os

from flask import Flask

import entities  # noqa: F401  (registra os modelos no SQLAlchemy)
from config.database import init_app, db
from routes import registrar_rotas


def criar_app():
    app = Flask(__name__)
    app.config['RESTFUL_JSON'] = {'ensure_ascii': False}  # acentos legíveis no JSON

    init_app(app)
    registrar_rotas(app)

    with app.app_context():
        db.create_all()  # cria as tabelas que ainda não existirem

    return app


app = criar_app()

if __name__ == '__main__':
    depurar = os.getenv("FLASK_DEBUG", "1") == "1"
    app.run(host='0.0.0.0', port=5000, debug=depurar)
