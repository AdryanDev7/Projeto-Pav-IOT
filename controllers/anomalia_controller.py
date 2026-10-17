from services.anomalia_service import AnomaliaService
from flask import jsonify

class AnomaliaController:
    @staticmethod
    def listar_anomalias():
        anomalias = AnomaliaService.listar_anomalias()
        return jsonify(anomalias), 200

    @staticmethod
    def deletar_anomalia(anomalia_id):
        try:
            AnomaliaService.deletar_anomalia(anomalia_id)
            return jsonify({"mensagem": "Anomalia deletada com sucesso!"}), 200
        except ValueError as e:
            return jsonify({"erro": str(e)}), 404