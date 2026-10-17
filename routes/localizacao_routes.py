from flask import Blueprint, request, jsonify
from services.localizacao_service import LocalizacaoService

localizacao_bp = Blueprint('localizacao_bp', __name__, url_prefix='/api/localizacoes')

@localizacao_bp.route('', methods=['POST'])
def criar():
    try:
        dados = request.get_json()
        loc = LocalizacaoService.criar_localizacao(dados)
        return jsonify({"mensagem": "Localização criada com sucesso!", "id": loc.id}), 201
    except ValueError as e:
        return jsonify({"erro": str(e)}), 400
    except Exception as e:
        return jsonify({"erro": str(e)}), 500

@localizacao_bp.route('', methods=['GET'])
def listar():
    locs = LocalizacaoService.listar_localizacoes()
    return jsonify(locs), 200

@localizacao_bp.route('/<int:id>', methods=['PUT'])
def atualizar(id):
    try:
        dados = request.get_json()
        loc = LocalizacaoService.atualizar_localizacao(id, dados)
        return jsonify({"mensagem": "Localização atualizada com sucesso!"}), 200
    except ValueError as e:
        return jsonify({"erro": str(e)}), 404
    except Exception as e:
        return jsonify({"erro": str(e)}), 500

@localizacao_bp.route('/<int:id>', methods=['DELETE'])
def deletar(id):
    try:
        LocalizacaoService.deletar_localizacao(id)
        return jsonify({"mensagem": "Localização deletada com sucesso!"}), 200
    except ValueError as e:
        return jsonify({"erro": str(e)}), 404
    except Exception as e:
        return jsonify({"erro": str(e)}), 500