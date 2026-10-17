from flask import Blueprint, request, jsonify
from services.leitura_service import LeituraService

leitura_bp = Blueprint('leitura_bp', __name__, url_prefix='/api/leituras')

@leitura_bp.route('', methods=['POST'])
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

@leitura_bp.route('', methods=['GET'])
def listar_leituras():
    leituras = LeituraService.listar_leituras()
    return jsonify(leituras), 200

@leitura_bp.route('/<int:leitura_id>', methods=['DELETE'])
def deletar_leitura(leitura_id):
    try:
        LeituraService.deletar_leitura(leitura_id)
        return jsonify({"mensagem": "Leitura deletada com sucesso!"}), 200
    except ValueError as e:
        return jsonify({"erro": str(e)}), 404