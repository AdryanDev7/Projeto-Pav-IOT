from flask import request, jsonify
from services.leitura_service import LeituraService

class LeituraController:
    @staticmethod
    def criar_leitura():
        try:
            dados = request.get_json()
            leitura = LeituraService.criar_leitura(dados)
            return jsonify({
                "mensagem": "Leitura registada com sucesso!",
                "leitura_id": leitura.id
            }), 201
        except ValueError as e:
            return jsonify({"erro": str(e)}), 400
        except Exception as e:
            return jsonify({"erro": "Erro interno no servidor: " + str(e)}), 500

    @staticmethod
    def listar_leituras():
        leituras = LeituraService.listar_leituras()
        return jsonify(leituras), 200

    @staticmethod
    def deletar_leitura(leitura_id):
        try:
            LeituraService.deletar_leitura(leitura_id)
            return jsonify({"mensagem": "Leitura deletada com sucesso!"}), 200
        except ValueError as e:
            return jsonify({"erro": str(e)}), 404