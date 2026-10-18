from entities.anomalia import Anomalia
from services import validadores
from services.base_service import BaseService
from services.exceptions import RegraNegocioError

SEVERIDADES_VALIDAS = ("Baixa", "Média", "Alta", "Crítica")


class AnomaliaService(BaseService):
    _ENTIDADE = Anomalia
    _MSG_NAO_ENCONTRADO = "Anomalia não encontrada."
    _MSG_INTEGRIDADE = "Violação de integridade: a leitura informada não existe."

    def __init__(self, repositorio, leitura_repositorio):
        super().__init__(repositorio)
        self._leitura_repo = leitura_repositorio

    def _validar(self, dados, id_atual=None):
        validadores.exigir_campos(dados, ("leitura_id", "descricao_alerta", "severidade"))  # RN07
        leitura_id = validadores.inteiro(dados, "leitura_id")
        descricao = validadores.texto(dados, "descricao_alerta", 500)
        severidade = validadores.texto(dados, "severidade", 20)

        if severidade not in SEVERIDADES_VALIDAS:
            raise RegraNegocioError("Severidade inválida. Use: " + ", ".join(SEVERIDADES_VALIDAS) + ".")

        if self._leitura_repo.buscar_por_id(leitura_id) is None:
            raise RegraNegocioError("A leitura informada não existe.")

        return {
            "leitura_id": leitura_id,
            "descricao_alerta": descricao,
            "severidade": severidade,
        }
