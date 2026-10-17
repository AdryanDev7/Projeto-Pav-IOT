import os
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def init_app(app):
    # Adicionado o '+psycopg2' para forçar o driver correto que instalamos
    db_url = os.getenv("DATABASE_URL", "postgresql+psycopg2://postgres:123@localhost:5433/iot_db")
    
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    db.init_app(app)