from flask import Blueprint
from controllers.sensor_controller import SensorController

sensor_bp = Blueprint('sensor_bp', __name__, url_prefix='/api/sensores')

sensor_bp.route('', methods=['POST'])(SensorController.criar_sensor)
sensor_bp.route('', methods=['GET'])(SensorController.listar_sensores)
sensor_bp.route('/<int:sensor_id>', methods=['DELETE'])(SensorController.delete_sensor if hasattr(SensorController, 'delete_sensor') else SensorController.deletar_sensor)