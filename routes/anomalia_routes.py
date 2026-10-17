from flask import Blueprint, jsonify
from entities.models import Anomalia

anomalia_bp = Blueprint('anomalia_bp', __name__, url_prefix='/api/anomalias')

@anomalia_bp.route('', methods=['GET'])
def listar_anomalias():
    anomalias = Anomalia.query.all()
    resultado = [
        {
            "id": a.id,
            "leitura_id": a.leitura_id,
            "descricao_alerta": a.descricao_alerta,
            "severidade": a.severidade
        } for a in anomalias
    ]
    return jsonify(resultado), 200