from flask import Blueprint, request, jsonify
from services.sensor_service import SensorService

sensor_bp = Blueprint('sensor_bp', __name__, url_prefix='/api/sensores')

@sensor_bp.route('', methods=['POST'])
def criar_sensor():
    try:
        dados = request.get_json()
        sensor = SensorService.criar_sensor(dados)
        return jsonify({
            "mensagem": "Sensor cadastrado com sucesso!",
            "sensor": {
                "id": sensor.id,
                "codigo_serial": sensor.codigo_serial,
                "tipo": sensor.tipo,
                "status": sensor.status
            }
        }), 201
    except ValueError as e:
        return jsonify({"erro": str(e)}), 400
    except Exception as e:
        return jsonify({"erro": "Erro interno no servidor: " + str(e)}), 500

@sensor_bp.route('', methods=['GET'])
def listar_sensores():
    sensores = SensorService.listar_sensores()
    return jsonify(sensores), 200

@sensor_bp.route('/<int:sensor_id>', methods=['DELETE'])
def deletar_sensor(sensor_id):
    try:
        SensorService.deletar_sensor(sensor_id)
        return jsonify({"mensagem": "Sensor deletado com sucesso!"}), 200
    except ValueError as e:
        return jsonify({"erro": str(e)}), 404