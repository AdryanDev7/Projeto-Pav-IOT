from flask import Blueprint
from controllers.anomalia_controller import AnomaliaController

anomalia_bp = Blueprint('anomalia_bp', __name__, url_prefix='/api/anomalias')

anomalia_bp.route('', methods=['GET'])(AnomaliaController.listar_anomalias)
anomalia_bp.route('/<int:anomalia_id>', methods=['DELETE'])(AnomaliaController.deletar_anomalia)