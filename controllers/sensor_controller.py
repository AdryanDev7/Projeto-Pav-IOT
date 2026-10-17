from flask import request, jsonify
from services.sensor_service import SensorService

class SensorController:
    @staticmethod
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

    @staticmethod
    def listar_sensores():
        sensores = SensorService.listar_sensores()
        return jsonify(sensores), 200

    @staticmethod
    def atualizar_sensor(sensor_id):
        try:
            dados = request.get_json()
            sensor = SensorService.atualizar_sensor(sensor_id, dados)
            return jsonify({
                "mensagem": "Sensor atualizado com sucesso!",
                "id": sensor.id
            }), 200
        except ValueError as e:
            return jsonify({"erro": str(e)}), 400
        except Exception as e:
            return jsonify({"erro": "Erro interno no servidor: " + str(e)}), 500

    @staticmethod
    def deletar_sensor(sensor_id):
        try:
            SensorService.deletar_sensor(sensor_id)
            return jsonify({"mensagem": "Sensor deletado com sucesso!"}), 200
        except ValueError as e:
            return jsonify({"erro": str(e)}), 404
        except Exception as e:
            return jsonify({"erro": "Erro interno no servidor: " + str(e)}), 500