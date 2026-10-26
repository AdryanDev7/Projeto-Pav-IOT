from config.excecoes import ConflitoErro, RegraVioladaErro
from config.limites import LIMITES_FISICOS
from entities.atuador import ESTADOS_ATUADOR
from services.autorizacao import exigir_zona
from services.base_service import BaseService


class SensorService(BaseService):
    nome_entidade = "Sensor"

    def _autorizar(self, operador, obj, escrita):
        exigir_zona(operador, obj.zona)                           # regra 10

    def _validar(self, dados, operador):
        # regra 10: operador não pode cadastrar/mover sensor para outra zona
        exigir_zona(operador, dados.zona)

        minimo, maximo = LIMITES_FISICOS[dados.tipo]
        if not (minimo <= dados.limite_seguranca <= maximo):
            raise RegraVioladaErro(
                f"O limite de segurança ({dados.limite_seguranca}) deve estar dentro do "
                f"intervalo físico do tipo {dados.tipo}: {minimo} a {maximo}.")

        if dados.atuador_estado is not None and dados.atuador_estado not in ESTADOS_ATUADOR[dados.atuador_tipo]:
            raise RegraVioladaErro(
                f"Estado '{dados.atuador_estado}' é incompatível com atuador {dados.atuador_tipo}. "
                f"Use: {', '.join(ESTADOS_ATUADOR[dados.atuador_tipo])}.")

    def _ajustar(self, obj):
        # se o estado ficou vazio ou não combina com o tipo do atuador, usa o estado inicial do tipo
        if obj.atuador_estado not in ESTADOS_ATUADOR[obj.atuador_tipo]:
            obj.atuador_estado = ESTADOS_ATUADOR[obj.atuador_tipo][0]

    def _antes_de_remover(self, obj, operador):
        # regra 8: telemetria é imutável, então não se apaga sensor que já tem histórico
        if self._repo.contar_leituras(obj.id) > 0:
            raise ConflitoErro(
                "Este sensor possui histórico de telemetria (imutável) e não pode ser excluído. "
                "Desative-o (campo 'ativo') para preservar a rastreabilidade.")
