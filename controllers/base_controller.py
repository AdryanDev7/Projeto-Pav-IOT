from functools import wraps

from flask import request
from flask_restful import Resource

from services.exceptions import NaoEncontradoError, RegraNegocioError


def tratar_erros(funcao):
    """Converte as exceções dos services em respostas HTTP com JSON claro."""
    @wraps(funcao)
    def wrapper(*args, **kwargs):
        try:
            return funcao(*args, **kwargs)
        except NaoEncontradoError as erro:
            return {"erro": str(erro)}, 404
        except RegraNegocioError as erro:
            return {"erro": str(erro)}, 400
        except Exception as erro:
            return {"erro": "Erro interno no servidor: " + str(erro)}, 500
    return wrapper


class RecursoBase(Resource):
    """Base de todos os controllers (HERANÇA): guarda o service e trata os erros."""
    method_decorators = [tratar_erros]

    def __init__(self, service):
        self._service = service  # recebido pelo construtor (injeção de dependência)

    @staticmethod
    def _corpo_json():
        dados = request.get_json(silent=True)
        if not isinstance(dados, dict):
            raise RegraNegocioError("O corpo da requisição deve ser um JSON (objeto) válido.")
        return dados


class ListaController(RecursoBase):
    """GET (listar) e POST (criar) em /recurso"""
    _MSG_CRIADO = "Registro criado com sucesso!"

    def get(self):
        return self._service.listar(), 200

    def post(self):
        criado = self._service.criar(self._corpo_json())
        return {"mensagem": self._MSG_CRIADO, "id": criado["id"], "dados": criado}, 201


class ItemController(RecursoBase):
    """GET (buscar), PUT (editar) e DELETE (excluir) em /recurso/<id>"""
    _MSG_ATUALIZADO = "Registro atualizado com sucesso!"
    _MSG_EXCLUIDO = "Registro excluído com sucesso!"

    def get(self, registro_id):
        return self._service.buscar(registro_id), 200

    def put(self, registro_id):
        atualizado = self._service.atualizar(registro_id, self._corpo_json())
        return {"mensagem": self._MSG_ATUALIZADO, "id": atualizado["id"], "dados": atualizado}, 200

    def delete(self, registro_id):
        self._service.deletar(registro_id)
        return {"mensagem": self._MSG_EXCLUIDO}, 200
