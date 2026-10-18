# Importar todos os modelos aqui garante que o SQLAlchemy os conhece antes do db.create_all()
from entities.base import EntidadeBase
from entities.localizacao import Localizacao
from entities.sensor import Sensor
from entities.leitura import LeituraSensor
from entities.anomalia import Anomalia
