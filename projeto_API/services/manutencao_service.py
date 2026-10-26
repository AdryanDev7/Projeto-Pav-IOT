from datetime import timedelta

from config.excecoes import RegraVioladaErro
from config.settings import agora
from services.dependente_sensor_service import DependenteSensorService


class ManutencaoService(DependenteSensorService):
    nome_entidade = "Manutenção"

    def _validar(self, dados, operador):
        super()._validar(dados, operador)
        if dados.data_afericao and dados.data_afericao > agora() + timedelta(minutes=1):
            raise RegraVioladaErro("A data de aferição não pode estar no futuro.")
