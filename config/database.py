import os
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def init_app(app):
    # Fora do Docker: localhost:5433. Dentro do container, o compose injeta DATABASE_URL com host "db".
    db_url = os.getenv(
        "DATABASE_URL",
        "postgresql+psycopg2://postgres:postgres@localhost:5433/iot_database",
    )

    app.config['SQLALCHEMY_DATABASE_URI'] = db_url
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)
