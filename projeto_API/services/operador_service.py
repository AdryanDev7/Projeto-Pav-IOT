from config.excecoes import ConflitoErro
from services.autorizacao import exigir_supervisor
from services.base_service import BaseService


class OperadorService(BaseService):
    nome_entidade = "Operador"

    def _autorizar(self, operador, obj, escrita):
        if escrita:
            exigir_supervisor(operador)      # só supervisor cria/edita/exclui operadores

    def _antes_de_remover(self, obj, operador):
        if obj.id == operador.id:
            raise ConflitoErro("Você não pode excluir o seu próprio usuário.")

    def listar_para_login(self):
        """Lista simplificada usada na tela de login da interface (sem autenticação)."""
        return self._repo.listar()
