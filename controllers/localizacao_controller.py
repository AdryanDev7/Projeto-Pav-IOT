from flask import request, jsonify
from services.localizacao_service import LocalizacaoService

class LocalizacaoController:
    @staticmethod
    def criar_localizacao():
        try:
            dados = request.get_json()
            localizacao = LocalizacaoService.criar_localizacao(dados)
            return jsonify({
                "mensagem": "Localização criada com sucesso!",
                "id": localizacao.id
            }), 201
        except ValueError as e:
            return jsonify({"erro": str(e)}), 400
        except Exception as e:
            return jsonify({"erro": "Erro interno no servidor: " + str(e)}), 500

    @staticmethod
    def listar_localizacoes():
        localizacoes = LocalizacaoService.listar_localizacoes()
        return jsonify(localizacoes), 200

    @staticmethod
    def atualizar_localizacao(localizacao_id):
        try:
            dados = request.get_json()
            localizacao = LocalizacaoService.atualizar_localizacao(localizacao_id, dados)
            return jsonify({
                "mensagem": "Localização atualizada com sucesso!",
                "id": localizacao.id
            }), 200
        except ValueError as e:
            return jsonify({"erro": str(e)}), 404
        except Exception as e:
            return jsonify({"erro": "Erro interno no servidor: " + str(e)}), 500